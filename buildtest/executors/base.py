"""
BuildExecutor: manager for test executors
"""

import logging
import os
import re

from buildtest.utils.file import write_file, read_file


class BaseExecutor:
    """The BaseExecutor is an abstract base class for all executors. All
       executors must have a listing of steps and dryrun_steps
    """

    steps = ["setup", "run"]
    type = "base"

    def __init__(self, name, settings, config_opts):
        """Initiate a base executor, meaning we provide a name (also held
        by the BuildExecutor base that holds it) and the loaded dictionary
        of config opts to parse.

        :param name: a name for the base executor and key provided in the configuration file
        :type name: string
        :param settings: the original config opts to extract variables from.
        :type settings: dict
        :param config_opts: loaded buildtest configuration
        :type config_opts: dict
        """

        self.logger = logging.getLogger(__name__)
        self.name = name
        self._settings = settings
        self._buildtestsettings = config_opts
        self.load()
        self.builder = None
        self.result = {}

    def load(self):
        """Load a particular configuration based on the name. This method
        should set defaults for the executor, and will vary based on the
        class.
        """
        pass

    def run(self):
        """The run step basically runs the build. This is run after setup
        so we are sure that the builder is defined. This is also where
        we set the result to return.
        """
        pass

    def __str__(self):
        return "%s.%s" % (self.type, self.name)

    def __repr__(self):
        return self.__str__()

    def get_formatted_time(self, key, fmt="%Y/%m/%d %X"):
        """Given some timestamp key in self.metadata, return a pretty printed
        version of it. This is intended to log in the console for the user.

        :param key: The key to look up in the metadata
        :type key: str
        :param fmt: The format string to use with datetime
        :type fmt: string
        """

        timestamp = self.builder.metadata.get(key, "")
        if timestamp:
            timestamp = timestamp.strftime(fmt)
        return timestamp

    def check_regex(self, regex):
        """This method conducts a regular expression check using ``re.search``
        with regular expression defined in Buildspec. User must specify an
        output stream (stdout, stderr) to select when performing regex. In
        buildtest, this would read the .out or .err file based on stream and run
        the regular expression to see if there is a match.

        :param regex: Regular expression object defined in Buildspec file
        :type regex: str
        :return: A boolean return True/False based on if re.search is successful or not
        :rtype: bool
        """

        if regex["stream"] == "stdout":
            self.logger.debug(
                f"Detected regex stream 'stdout' so reading output file: {self.builder.metadata['outfile']}"
            )
            content = read_file(self.builder.metadata["outfile"])

        elif regex["stream"] == "stderr":
            self.logger.debug(
                f"Detected regex stream 'stderr' so reading error file: {self.builder.metadata['errfile']}"
            )
            content = read_file(self.builder.metadata["errfile"])

        self.logger.debug(f"Applying re.search with exp: {regex['exp']}")

        # perform a regex search based on value of 'exp' key defined in Buildspec with content file (output or error)
        return re.search(regex["exp"], content) != None

    def write_testresults(self, out, err):
        """This method writes test results into output and error file.

        :param out: content of output stream
        :type out: list
        :param err: content of error stream
        :type err: list
        """

        # Keep an output file
        run_output_file = os.path.join(
            self.builder.metadata.get("testroot"), self.builder.metadata.get("id")
        )
        outfile = run_output_file + ".out"
        errfile = run_output_file + ".err"

        # write output of test to .out file
        out = "".join(out)
        err = "".join(err)

        self.logger.debug(f"Writing run output to file: {outfile}")
        write_file(outfile, out)

        # write error from test to .err file
        self.logger.debug(f"Writing run error to file: {errfile}")
        write_file(errfile, err)

        self.builder.metadata["outfile"] = outfile
        self.builder.metadata["errfile"] = errfile

    def check_test_state(self):
        """This method is responsible for detecting state of test (PASS/FAIL)
        based on returncode or regular expression.
        """

        status = self.builder.recipe.get("status")

        self.result["state"] = "FAIL"
        # if status is defined in Buildspec, then check for returncode and regex
        if status:

            # returncode_match is boolean to check if reference returncode matches return code from test
            returncode_match = False

            # regex_match is boolean to check if output/error stream matches regex defined in Buildspec,
            # if no regex is defined we set this to True since we do a logical AND
            regex_match = False

            slurm_job_state_match = False
            if status.get("returncode"):
                self.logger.debug("Conducting Return Code check")
                self.logger.debug(
                    "Status Return Code: %s   Result Return Code: %s"
                    % (status["returncode"], self.result["returncode"])
                )
                # checks if test returncode matches returncode specified in Buildspec and assign boolean to returncode_match
                returncode_match = status["returncode"] == self.result["returncode"]

            if status.get("regex"):
                self.logger.debug("Conducting Regular Expression check")
                # self.check_regex  applies regular expression check specified in Buildspec with output or error
                # stream. self.check_regex returns a boolean (True/False) by using re.search
                regex_match = self.check_regex(status["regex"])

            # if slurm_job_state_codes defined in buildspec.
            # self.builder.metadata["job"] only defined when job run through SlurmExecutor
            if status.get("slurm_job_state_codes") and self.builder.metadata.get("job"):
                slurm_job_state_match = (
                    status["slurm_job_state_codes"]
                    == self.builder.metadata["job"]["State"]
                )

            self.logger.info(
                "ReturnCode Match: %s Regex Match: %s Slurm Job State Match: %s"
                % (returncode_match, regex_match, slurm_job_state_match)
            )

            if returncode_match or regex_match or slurm_job_state_match:
                self.result["state"] = "PASS"

        # if status is not defined we check test returncode, by default 0 is PASS and any other return code is a FAIL
        else:
            if self.result["returncode"] == 0:
                self.result["state"] = "PASS"

        # Return to starting directory for next test
        os.chdir(self.builder.pwd)


class SSHExecutor(BaseExecutor):
    type = "ssh"
