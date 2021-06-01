"""
BuildExecutor: manager for test executors
"""

import logging
import os
import re
from buildtest.utils.file import read_file


class BaseExecutor:
    """The BaseExecutor is an abstract base class for all executors."""

    type = "base"

    def __init__(self, name, settings, site_configs):
        """Initiate a base executor, meaning we provide a name (also held
        by the BuildExecutor base that holds it) and the loaded dictionary
        of config opts to parse.

        :param name: a name for the base executor and key provided in the configuration file
        :type name: str, required
        :param settings: executor settings from configuration file for a particular executor instance (``local.bash``)
        :type settings: dict, required
        :param site_configs: loaded buildtest configuration
        :type site_configs: instance of SiteConfiguration, required
        """

        self.logger = logging.getLogger(__name__)
        self.name = name
        self._settings = settings
        self._buildtestsettings = site_configs
        self.load()
        self.result = {}

    def load(self):
        """Load a particular configuration based on the name. This method
        should set defaults for the executor, and will vary based on the
        class.
        """

    def run(self):
        """The run step basically runs the build. This is run after setup
        so we are sure that the builder is defined. This is also where
        we set the result to return.
        """

    def __str__(self):
        return "%s.%s" % (self.type, self.name)

    def __repr__(self):
        return self.__str__()

    def _check_regex(self, builder):
        """This method conducts a regular expression check using ``re.search``
        with regular expression defined in Buildspec. User must specify an
        output stream (stdout, stderr) to select when performing regex. In
        buildtest, this would read the .out or .err file based on stream and
        run the regular expression to see if there is a match. This method
        will return a boolean True indicates there is a match otherwise False
        if ``regex`` object not defined or ``re.search`` doesn't find a match.

        :param builder: instance of BuilderBase class
        :type builder: BuilderBase (subclass)

        :return: A boolean return True/False based on if re.search is successful or not
        :rtype: bool
        """

        regex_match = False

        if not builder.status.get("regex"):
            return regex_match

        if builder.status["regex"]["stream"] == "stdout":
            self.logger.debug(
                f"Detected regex stream 'stdout' so reading output file: {builder.metadata['outfile']}"
            )
            content = read_file(builder.metadata["outfile"])

        elif builder.status["regex"]["stream"] == "stderr":
            self.logger.debug(
                f"Detected regex stream 'stderr' so reading error file: {builder.metadata['errfile']}"
            )
            content = read_file(builder.metadata["errfile"])

        self.logger.debug(
            f"Applying re.search with exp: {builder.status['regex']['exp']}"
        )

        # perform a regex search based on value of 'exp' key defined in Buildspec with content file (output or error)
        return re.search(builder.status["regex"]["exp"], content) is not None

    def _returncode_check(self, builder):
        """Check status check of ``returncode`` field if specified in status
        property.

        :param builder: instance of BuilderBase class
        :type builder: BuilderBase (subclass)
        """

        returncode_match = False

        if builder.status.get("returncode"):
            # returncode can be an integer or list of integers

            buildspec_returncode = builder.status["returncode"]

            # if buildspec returncode field is integer we convert to list for check
            if isinstance(buildspec_returncode, int):
                buildspec_returncode = [buildspec_returncode]

            self.logger.debug("Conducting Return Code check")
            self.logger.debug(
                "Status Return Code: %s   Result Return Code: %s"
                % (
                    buildspec_returncode,
                    builder.metadata["result"]["returncode"],
                )
            )
            # checks if test returncode matches returncode specified in Buildspec and assign boolean to returncode_match
            returncode_match = (
                builder.metadata["result"]["returncode"] in buildspec_returncode
            )

        return returncode_match

    def _check_runtime(self, builder):
        """This method will return a boolean (True/False) based on runtime specified in buildspec and check with test runtime.
        User can specify both `min` and `max`, or just specify `min` or `max`.

        """

        if not builder.status.get("runtime"):
            return False

        min_time = builder.status["runtime"].get("min") or 0
        max_time = builder.status["runtime"].get("max")

        # if both min and max are specified
        if min_time and max_time:
            self.logger.debug(
                f"Checking test: {builder.name} runtime: {builder.metadata['result']['runtime']} is greater than min: {float(min_time)} and less than max: {float(max_time)}"
            )
            return (
                float(min_time)
                < builder.metadata["result"]["runtime"]
                < float(max_time)
            )

        # if min specified
        if min_time and not max_time:
            self.logger.debug(
                f"Checking test: {builder.name} runtime: {builder.metadata['result']['runtime']} is greater than min: {float(min_time)}"
            )
            return float(min_time) < builder.metadata["result"]["runtime"]

        # if max specified
        if not min_time and max_time:
            self.logger.debug(
                f"Checking test: {builder.name} runtime: {builder.metadata['result']['runtime']} is less than max: {float(max_time)}"
            )
            return builder.metadata["result"]["runtime"] < float(max_time)

    def check_test_state(self, builder):
        """This method is responsible for detecting state of test (PASS/FAIL)
        based on returncode or regular expression.

        :param builder: instance of BuilderBase class
        :type builder: BuilderBase (subclass)
        """

        builder.metadata["result"]["state"] = "FAIL"
        # if status is defined in Buildspec, then check for returncode and regex
        if builder.status:

            slurm_job_state_match = False

            # returncode_match is boolean to check if reference returncode matches return code from test
            returncode_match = self._returncode_check(builder)

            # check regex against output or error stream based on regular expression
            # defined in status property. Return value is a boolean
            regex_match = self._check_regex(builder)

            runtime_match = self._check_runtime(builder)

            # if slurm_job_state_codes defined in buildspec.
            # self.builder.metadata["job"] only defined when job run through SlurmExecutor
            if builder.status.get("slurm_job_state") and builder.metadata.get("job"):
                slurm_job_state_match = (
                    builder.status["slurm_job_state"]
                    == builder.metadata["job"]["State"]
                )

            self.logger.info(
                "ReturnCode Match: %s Regex Match: %s Slurm Job State Match: %s"
                % (returncode_match, regex_match, slurm_job_state_match)
            )

            if (
                returncode_match
                or regex_match
                or slurm_job_state_match
                or runtime_match
            ):
                builder.metadata["result"]["state"] = "PASS"

        # if status is not defined we check test returncode, by default 0 is PASS and any other return code is a FAIL
        else:
            if builder.metadata["result"]["returncode"] == 0:
                builder.metadata["result"]["state"] = "PASS"

        # Return to starting directory for next test
        os.chdir(builder.pwd)
