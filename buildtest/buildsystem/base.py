"""
BuilderBase class is an abstract class that defines common
functions for any types of builders. Each type schema (script, compiler)
is implemented as separate Builder.

ScriptBuilder class implements 'type: script'
CompilerBuilder class implements 'type: compiler'
"""
import datetime
import getpass
import logging
import os
import re
import shutil
import socket
import stat
import uuid
from abc import ABC, abstractmethod
from pathlib import Path

from buildtest.buildsystem.batch import (
    CobaltBatchScript,
    LSFBatchScript,
    PBSBatchScript,
    SlurmBatchScript,
)
from buildtest.defaults import BUILDTEST_EXECUTOR_DIR
from buildtest.exceptions import ExecutorError
from buildtest.executors.job import Job
from buildtest.schemas.defaults import schema_table
from buildtest.utils.command import BuildTestCommand
from buildtest.utils.file import create_dir, read_file, write_file
from buildtest.utils.shell import Shell
from buildtest.utils.timer import Timer
from buildtest.utils.tools import deep_get


class BuilderBase(ABC):
    """The BuilderBase is an abstract class that implements common functions for
    any kind of builder.
    """

    def __init__(self, name, recipe, buildspec, executor, buildexecutor, testdir):
        """The BuilderBase provides common functions for any builder. The builder
        is an instance of BuilderBase. The initializer method will setup the builder
        attributes based on input test by ``name`` parameter.

        :param name: Name of test in Buildspec recipe
        :type name: str, required
        :param recipe: the loaded section from the buildspec for the user.
        :type recipe: dict, required
        :param buildspec: the pull path to the Buildspec file, must exist.
        :type buildspec: str, required
        :param buildexecutor: an instance of BuildExecutor class defines Executors from configuration file
        :type buildexecutor: BuildExecutor, required
        :param testdir: Test Destination directory where to write test
        :type testdir: str, optional
        """

        self.name = name
        self.pwd = os.getcwd()
        self.result = {}
        self.metadata = {}

        self.duration = 0

        self.timer = Timer()

        # store state of builder which can be True/False. This value is changed by self.success(), self.failure()
        self._buildstate = None

        # The type must match the type of the builder
        self.recipe = recipe

        self.executor = executor

        # For batch jobs this variable is an instance of Job class which would be one of the subclass
        self.job = None

        # Controls the state of the builder object, a complete job  will set
        # this value to True. A job cancellation or job failure in submission will set this to False
        self.state = None

        # this value holds the 'status' property from the buildspec
        self.status = None

        # this value hosts the 'metrics' property from the buildspec
        self.metrics = None

        self.buildspec = buildspec

        # used to lookup variables if 'vars' key is defined.
        self.variable_lookup = {}
        # used to lookup environment variables if 'envs' key is defined.
        self.envs_lookup = {}

        # strip .yml extension from file name
        file_name = re.sub("[.](yml)", "", os.path.basename(buildspec))
        self.testdir = os.path.join(testdir, self.executor, file_name, self.name)

        self.logger = logging.getLogger(__name__)

        self.logger.debug(f"Processing Buildspec: {self.buildspec}")
        self.logger.debug(f"Processing Buildspec section: {self.name}")

        # get type attribute from Executor class (local, slurm, cobalt, pbs, lsf)
        self.executor_type = buildexecutor.executors[self.executor].type
        self.buildexecutor = buildexecutor
        self._set_metadata_values()

        # The default shell will be bash
        self.default_shell = Shell()

        self.shell = Shell(self.recipe.get("shell", "bash"))

        # set shebang to value defined in Buildspec, if not defined then get one from Shell class
        self.shebang = (
            self.recipe.get("shebang") or f"{self.shell.shebang} {self.shell.opts}"
        )
        self.logger.debug("Using shell %s", self.shell.name)
        self.logger.debug(f"Shebang used for test: {self.shebang}")

        # shell_type is used to classify compatible shells which are matched by executor shell.
        self.shell_type = None
        if self.shell.name in ["sh", "bash", "zsh", "/bin/sh", "/bin/bash", "/bin/zsh"]:
            self.shell_type = "bash"
        elif self.shell.name in ["csh", "tcsh", "/bin/csh", "/bin/tcsh"]:
            self.shell_type = "csh"
        elif self.shell.name in ["python"]:
            self.shell_type = "python"

        self.sched_init()

    def _set_metadata_values(self):
        """This method sets self.metadata that contains metadata for each builder object."""
        self.metadata["name"] = self.name
        self.metadata["buildspec"] = self.buildspec

        # store tags
        self.metadata["tags"] = self.recipe.get("tags")
        # store executor name
        self.metadata["executor"] = self.executor

        # store schemafile used for validating
        self.metadata["schemafile"] = os.path.basename(
            schema_table[f"{self.recipe['type']}-v1.0.schema.json"]["path"]
        )

        # used for storing output content
        self._output = None
        # used for storing error content
        self._error = None

        # store output content of test
        self.metadata["output"] = None
        # store error content of test
        self.metadata["error"] = None

        # store current hostname
        self.metadata["hostname"] = socket.gethostname()
        # store current username
        self.metadata["user"] = getpass.getuser()

        # root of test directory
        self.metadata["testroot"] = None
        # location of stage directory in test root
        self.metadata["stagedir"] = None

        self.metadata["description"] = self.recipe.get("description")

        # location of test script
        self.metadata["testpath"] = None

        # store content of buildspec file
        self.metadata["buildspec_content"] = read_file(self.buildspec)
        # used to store content of test
        self.metadata["test_content"] = None
        self.metadata["buildscript_content"] = None

        # used to store compiler name used the test. Only applicable with compiler schema
        self.metadata["compiler"] = None

        self.metadata["result"] = {"state": "N/A", "returncode": "-1", "runtime": 0}

        self.metadata["metrics"] = {}

        # used to store job id from batch scheduler
        self.metadata["jobid"] = None
        # used to store job metrics for given JobID from batch scheduler
        self.metadata["job"] = {}
        # Generate a unique id for the build based on key and unique string
        self.test_uid = self._generate_unique_id()
        self.metadata["full_id"] = self.test_uid
        self.metadata["id"] = self.test_uid[:8]

    def _generate_unique_id(self):
        """Generate a unique build id using ``uuid.uuid4()``."""

        unique_id = str(uuid.uuid4())
        return unique_id

    def get_test_extension(self):
        """Return the test extension, which depends on the shell used. Based
        on the value of ``shell`` key we return the shell extension.

        shell: bash --> sh (default)

        :return: returns test extension based on shell type
        :rtype: str
        """

        # for python shell or bash shell type we return 'sh' extension
        if self.shell_type == "python" or self.shell_type == "bash":
            return "sh"

        if self.shell_type == "csh":
            return "csh"

    def is_batch_job(self):
        """Return True/False if builder.job attribute is of type Job instance if not returns False.
        This method indicates if builder has a job submitted to queue"""

        if isinstance(self.job, Job):
            return True

        return False

    def start(self):
        """Keep internal time for start of test. We start timer by calling
        Timer class
        """
        # self.timer = Timer()
        self.timer.start()

    def stop(self):
        """Stop timer of test and calculate duration."""
        # self.duration += self.timer.stop()
        self.timer.stop()

    def build(self):
        """This method is responsible for invoking setup, creating test
        directory and writing test. This method is called from an instance
        object of this class that does ``builder.build()``.
        """

        self._build_setup()
        self._write_test()
        self._write_build_script()

    def run(self):
        """Run the test and record the starttime and start timer. We also return the instance
        object of type BuildTestCommand which is used by Executors for processing output and error
        """

        self.starttime()
        self.start()
        command = BuildTestCommand(self.runcmd)
        command.execute()

        self.logger.debug(f"Running Test via command: {self.runcmd}")
        ret = command.returncode()
        err_msg = " ".join(command.get_error())

        if ret != 0:
            err = f"[{self.metadata['name']}/{self.test_uid}] failed to submit job with returncode: {ret} \n"
            print(err)
            print(err_msg)
            raise ExecutorError(err)

        return command

    def starttime(self):
        """This method will record the starttime when job starts execution by using
        ``datetime.datetime.now()``
        """

        self._starttime = datetime.datetime.now()

        # this is recorded in the report file
        self.metadata["result"]["starttime"] = self._starttime.strftime("%Y/%m/%d %X")

    def endtime(self):
        """This method is called upon termination of job, we get current time using
        ``datetime.datetime.now()`` and calculate runtime of job
        """

        self._endtime = datetime.datetime.now()

        # this is recorded in the report file
        self.metadata["result"]["endtime"] = self._endtime.strftime("%Y/%m/%d %X")

        self.runtime()

    def runtime(self):
        """Calculate runtime of job by calculating delta between endtime and starttime. The unit of measure
        is seconds."""

        runtime = self._endtime - self._starttime
        self._runtime = runtime.total_seconds()
        self.metadata["result"]["runtime"] = self._runtime

    def get_runtime(self):
        return self._runtime

    def success(self):
        """This method is invoked to indicate that builder job is complete after polling job."""
        self._buildstate = True

    def failure(self):
        """This method indicates that builder job is not complete after polling job either job was
        cancelled by scheduler or job failed to run.
        """
        self._buildstate = False

    def is_complete(self):
        """Return True/False depending on state of builder and if it ran to completion it will return
        ``True`` otherwise returns ``False``. A builder could fail due to job cancellation, failure to
        submit job or raise exception during the run phase. In those case, this method will return ``False``"""
        return self._buildstate == True

    def is_failure(self):
        """Return True if builder fails to run test."""
        return self._buildstate == False

    def is_unknown(self):
        return self._buildstate is None

    def run_command(self):
        """Command used to run the build script. buildtest will change into the stage directory (self.stage_dir)
        before running the test.
        """

        return f"sh {os.path.basename(self.build_script)}"

    def copy_stage_files(self):
        """Copy output and error file into test root directory since stage directory will be removed."""

        shutil.copy2(
            os.path.join(self.stage_dir, os.path.basename(self.metadata["outfile"])),
            os.path.join(self.test_root, os.path.basename(self.metadata["outfile"])),
        )
        shutil.copy2(
            os.path.join(self.stage_dir, os.path.basename(self.metadata["errfile"])),
            os.path.join(self.test_root, os.path.basename(self.metadata["errfile"])),
        )

        # update outfile and errfile metadata records which show up in report file
        self.metadata["outfile"] = os.path.join(
            self.test_root, os.path.basename(self.metadata["outfile"])
        )
        self.metadata["errfile"] = os.path.join(
            self.test_root, os.path.basename(self.metadata["errfile"])
        )

    def _build_setup(self):
        """This method is the setup operation to get ready to build test which
        includes getting unique build id, setting up metadata object to store
        test details such as where test will be located and directory of test.
        This section cannot be reached without a valid, loaded recipe.
        """

        create_dir(self.testdir)

        # num_content = len(os.listdir(self.testdir))
        # the testid is incremented for every run, this can be done by getting
        # length of all files in testdir and creating a directory. Subsequent
        # runs will increment this counter

        self.test_root = os.path.join(self.testdir, self.test_uid[:8])

        create_dir(self.test_root)
        self.metadata["testroot"] = self.test_root

        self.stage_dir = os.path.join(self.test_root, "stage")

        # create stage and run directories
        create_dir(self.stage_dir)
        self.logger.debug("Creating the stage directory: %s ", self.stage_dir)

        self.metadata["stagedir"] = self.stage_dir

        # Derive the path to the test script
        self.testpath = "%s.%s" % (
            os.path.join(self.stage_dir, self.name),
            self.get_test_extension(),
        )
        self.testpath = os.path.expandvars(self.testpath)

        self.metadata["testpath"] = os.path.join(
            self.test_root, os.path.basename(self.testpath)
        )

        self.build_script = f"{os.path.join(self.stage_dir, self.name)}_build.sh"

        # copy all files relative to buildspec file into stage directory
        for fname in Path(os.path.dirname(self.buildspec)).glob("*"):
            if fname.is_dir():
                shutil.copytree(
                    fname, os.path.join(self.stage_dir, os.path.basename(fname))
                )
            elif fname.is_file():
                shutil.copy2(fname, self.stage_dir)

    def _emit_command(self):
        """This method will return a shell command used to invoke the script that is used for tests that
        use local executors"""

        if not self.recipe.get("shell") or self.recipe.get("shell") == "python":
            return [self.testpath]

        if not self.shell.opts:
            return [self.shell.name, self.testpath]

        return [self.shell.name, self.shell.opts, self.testpath]

    def _default_test_variables(self):
        """Return a list of lines inserted in testscript that define buildtest specific variables
        that can be referenced when writing tests. The buildtest variables all start with BUILDTEST_*
        """

        lines = []
        lines.append("\n")
        lines.append(
            "############# START VARIABLE DECLARATION ########################"
        )
        lines.append(f"export BUILDTEST_TEST_NAME={self.name}")
        lines.append(f"export BUILDTEST_TEST_ROOT={self.test_root}")
        lines.append(
            f"export BUILDTEST_BUILDSPEC_DIR={os.path.dirname(self.buildspec)}"
        )
        lines.append(f"export BUILDTEST_STAGE_DIR={self.stage_dir}")
        lines.append(f"export BUILDTEST_TEST_ID={self.metadata['full_id']}")
        lines.append(
            "############# END VARIABLE DECLARATION   ########################"
        )
        lines.append("\n")
        return lines

    def _write_build_script(self):
        """This method will write the build script used for running the test"""

        lines = ["#!/bin/bash"]
        lines += self._default_test_variables()
        lines.append("# source executor startup script")

        lines += [
            f"source {os.path.join(BUILDTEST_EXECUTOR_DIR, self.executor, 'before_script.sh')}"
        ]

        lines.append("# Run generated script")
        # local executor
        if self.buildexecutor.executors[self.executor].type == "local":
            cmd = self._emit_command()

            lines += [" ".join(cmd)]
        # batch executor
        else:
            launcher = self.buildexecutor.executors[self.executor].launcher_command()
            lines += [" ".join(launcher) + " " + f"{self.testpath}"]

        lines.append("# Get return code")
        lines.append("returncode=$?")

        lines.append("# Exit with return code")
        lines.append("exit $returncode")

        lines = "\n".join(lines)
        write_file(self.build_script, lines)
        self.metadata["buildscript_content"] = lines
        self.logger.debug(f"Writing build script: {self.build_script}")
        self._set_execute_perm(self.build_script)

        # copying build script into test_root directory since stage directory will be removed
        dest = os.path.join(self.test_root, os.path.basename(self.build_script))
        shutil.copy2(self.build_script, dest)
        self.logger.debug(f"Copying build script to: {dest}")

        self.build_script = dest

        self.runcmd = self.run_command()
        self.metadata["command"] = self.runcmd

    def _write_test(self):
        """This method is responsible for invoking ``generate_script`` that
        formulates content of testscript which is implemented in each subclass.
        Next we write content to file and apply 755 permission on script so
        it has executable permission.
        """

        # Implementation to write file generate.sh
        lines = []

        lines += self.generate_script()

        lines = "\n".join(lines)

        self.logger.info(f"Opening Test File for Writing: {self.testpath}")

        write_file(self.testpath, lines)

        self.metadata["test_content"] = lines

        self._set_execute_perm(self.testpath)
        # copy testpath to run_dir
        shutil.copy2(
            self.testpath,
            os.path.join(self.test_root, os.path.basename(self.testpath)),
        )

    def sched_init(self):
        """This method will resolve scheduler fields: 'sbatch', 'pbs', 'bsub', 'cobalt'"""
        self.sbatch = deep_get(
            self.recipe, "executors", self.executor, "sbatch"
        ) or self.recipe.get("sbatch")
        self.bsub = deep_get(
            self.recipe, "executors", self.executor, "bsub"
        ) or self.recipe.get("bsub")
        self.pbs = deep_get(
            self.recipe, "executors", self.executor, "pbs"
        ) or self.recipe.get("pbs")
        self.cobalt = deep_get(
            self.recipe, "executors", self.executor, "cobalt"
        ) or self.recipe.get("cobalt")
        self.batch = self.recipe.get("batch")

        self.burstbuffer = self.recipe.get("BB") or deep_get(
            self.recipe, "executors", self.executor, "BB"
        )
        self.datawarp = self.recipe.get("DW") or deep_get(
            self.recipe, "executors", self.executor, "DW"
        )

    def get_slurm_directives(self):
        """Get #SBATCH lines based on ``sbatch`` property"""
        jobscript = SlurmBatchScript(sbatch=self.sbatch, batch=self.batch)
        lines = jobscript.get_headers()
        lines += [f"#SBATCH --job-name={self.name}"]
        lines += [f"#SBATCH --output={self.name}.out"]
        lines += [f"#SBATCH --error={self.name}.err"]

        return lines

    def get_lsf_directives(self):
        """Get #BSUB lines based on ``bsub`` property"""
        jobscript = LSFBatchScript(bsub=self.bsub, batch=self.batch)
        lines = jobscript.get_headers()
        lines += [f"#BSUB -J {self.name}"]
        lines += [f"#BSUB -o {self.name}.out"]
        lines += [f"#BSUB -e {self.name}.err"]

        return lines

    def get_pbs_directives(self):
        """Get #PBS lines based on ``pbs`` property"""
        jobscript = PBSBatchScript(pbs=self.pbs, batch=self.batch)
        lines = jobscript.get_headers()
        lines += [f"#PBS -N {self.name}"]

        return lines

    def get_cobalt_directives(self):
        """Get #COBALT lines based on ``cobalt`` property"""
        jobscript = CobaltBatchScript(cobalt=self.cobalt, batch=self.batch)
        lines = jobscript.get_headers()
        lines += [f"#COBALT --jobname {self.name}"]

        return lines

    def get_job_directives(self):
        """This method returns a list of lines containing the scheduler directives"""
        lines = []

        if self.sbatch:
            sbatch_lines = self.get_slurm_directives()
            lines.append("####### START OF SCHEDULER DIRECTIVES #######")
            lines += sbatch_lines
            lines.append("####### END OF SCHEDULER DIRECTIVES   #######")

        if self.bsub:
            bsub_lines = self.get_lsf_directives()
            lines.append("####### START OF SCHEDULER DIRECTIVES #######")
            lines += bsub_lines
            lines.append("####### END OF SCHEDULER DIRECTIVES   #######")

        if self.pbs:
            pbs_lines = self.get_pbs_directives()
            lines.append("####### START OF SCHEDULER DIRECTIVES #######")
            lines += pbs_lines
            lines.append("####### END OF SCHEDULER DIRECTIVES   #######")

        if self.cobalt:
            cobalt_lines = self.get_cobalt_directives()
            lines.append("####### START OF SCHEDULER DIRECTIVES #######")
            lines += cobalt_lines
            lines.append("####### END OF SCHEDULER DIRECTIVES   #######")

        return lines

    def _get_burst_buffer(self, burstbuffer):
        """Get Burst Buffer directives (#BB) lines specified by BB property

        :param burstbuffer: Burst Buffer configuration specified by BB property
        :type burstbuffer: dict, required
        :return: list of burst buffer directives
        :rtype: list
        """

        if not burstbuffer:
            return

        lines = []
        lines.append("####### START OF BURST BUFFER DIRECTIVES #######")
        for arg in burstbuffer:
            lines += [f"#BB {arg} "]

        lines.append("####### END OF BURST BUFFER DIRECTIVES   #######")
        return lines

    def _get_data_warp(self, datawarp):
        """Get Cray Data Warp directives (#DW) lines specified by DW property.

        :param datawarp: Data Warp configuration specified by DW property
        :type datawarp: dict, required
        :return: list of data warp directives
        :rtype: list
        """

        if not datawarp:
            return

        lines = []
        lines.append("####### START OF DATAWARP DIRECTIVES #######")
        for arg in datawarp:
            lines += [f"#DW {arg}"]

        lines.append("####### END OF DATAWARP DIRECTIVES   #######")
        return lines

    def _set_execute_perm(self, fname):
        """Set permission to 755 for a given file. The filepath must be an absolute path to file"""

        # Change permission of the file to executable
        os.chmod(
            fname,
            stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH,
        )
        self.logger.debug(
            f"Applying permission 755 to {fname} so that test can be executed"
        )

    def _get_environment(self, env):
        """Retrieve a list of environment variables defined in buildspec and
        return them as list with the shell equivalent command

        :return: list of environment variable lines to add to test script.
        :rtype: list
        """

        lines = []

        shell = self.shell.name
        # Parse environment depending on expected shell
        if env:

            # bash, sh, zsh environment variable declaration is export KEY=VALUE
            if re.fullmatch("(bash|sh|zsh|/bin/bash|/bin/sh|/bin/zsh)$", shell):
                for k, v in env.items():
                    lines.append("export %s=%s" % (k, v))
                    self.envs_lookup[k] = v

            # tcsh, csh,  environment variable declaration is setenv KEY VALUE
            elif re.fullmatch("(tcsh|csh|/bin/tcsh|/bin/csh)$", shell):
                for k, v in env.items():
                    lines.append("setenv %s %s" % (k, v))
                    self.envs_lookup[k] = v

            else:
                self.logger.warning(
                    f"{shell} is not supported, skipping environment variables."
                )

        if lines:
            lines.insert(0, "# Declare environment variables")
            lines.append("\n")
        return lines

    def _get_variables(self, variables):
        """Retrieve a list of  variables defined in buildspec and
        return them as list with the shell equivalent command.

        :return: list of variables variable lines to add to test script.
        :rtype: list
        """

        lines = []

        shell = self.shell.name
        # Parse environment depending on expected shell
        if variables:

            # bash, sh, zsh variable declaration is KEY=VALUE
            if re.fullmatch("(bash|sh|zsh|/bin/bash|/bin/sh|/bin/zsh)$", shell):
                for k, v in variables.items():
                    self.variable_lookup[k] = v
                    lines.append("%s=%s" % (k, v))

            # tcsh, csh variable declaration is set KEY=VALUE
            elif re.fullmatch("(tcsh|csh|/bin/tcsh|/bin/csh)$", shell):
                for k, v in variables.items():
                    self.variable_lookup[k] = v
                    lines.append("set %s=%s" % (k, v))

            else:
                self.logger.warning(
                    f"{shell} is not supported, skipping environment variables."
                )

        if lines:
            lines.insert(0, "# Declare shell variables")
            lines.append("\n")
        return lines

    def add_metrics(self):
        """This method will update the metrics field stored in ``self.metadata['metrics']``. The ``metrics``
        property can be defined in the buildspdec to assign value to a metrics name based on regular expression,
        environment or variable assignment.
        """
        if not self.metrics:
            return

        for key in self.metrics.keys():

            # default value of metric is empty string
            self.metadata["metrics"][key] = ""

            # apply regex on stdout/stderr and assign value to metrics
            if self.metrics[key].get("regex"):

                if self.metrics[key]["regex"]["stream"] == "stdout":
                    content = self._output
                elif self.metrics[key]["regex"]["stream"] == "stderr":
                    content = self._error

                pattern = re.search(self.metrics[key]["regex"]["exp"], content)

                # if pattern match found we assign value to metric
                if pattern:
                    self.metadata["metrics"][key] = pattern.group()

            # variable assignment
            elif self.metrics[key].get("vars"):
                self.metadata["metrics"][key] = self.variable_lookup.get(
                    self.metrics[key]["vars"]
                )

            # environment variable assignment
            elif self.metrics[key].get("env"):
                self.metadata["metrics"][key] = self.envs_lookup.get(
                    self.metrics[key]["env"]
                )

        # convert all metrics to string types
        for key in self.metadata["metrics"].keys():
            self.metadata["metrics"][key] = str(self.metadata["metrics"][key])

    def output(self):
        """Return output content"""
        return self._output

    def error(self):
        """Return error content"""
        return self._error

    @abstractmethod
    def generate_script(self):
        """Build the testscript content implemented in each subclass"""

    def post_run_steps(self):

        self._output = read_file(self.metadata["outfile"])
        self._error = read_file(self.metadata["errfile"])

        self.metadata["output"] = self._output
        self.metadata["error"] = self._error

        self.copy_stage_files()
        self.check_test_state()

        self.add_metrics()

        # mark job is success if it finished all post run steps
        self.success()

    def _check_regex(self):
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

        if not self.status.get("regex"):
            return regex_match

        if self.status["regex"]["stream"] == "stdout":
            self.logger.debug(
                f"Detected regex stream 'stdout' so reading output file: {self.metadata['outfile']}"
            )
            content = self.output()

        elif self.status["regex"]["stream"] == "stderr":
            self.logger.debug(
                f"Detected regex stream 'stderr' so reading error file: {self.metadata['errfile']}"
            )
            content = self.error()

        self.logger.debug(f"Applying re.search with exp: {self.status['regex']['exp']}")

        # perform a regex search based on value of 'exp' key defined in Buildspec with content file (output or error)
        return re.search(self.status["regex"]["exp"], content) is not None

    def _returncode_check(self):
        """Check status check of ``returncode`` field if specified in status
        property.
        """

        returncode_match = False

        # if 'returncode' field set for 'status' check the returncode if its not set we return False
        if "returncode" in self.status.keys():

            # returncode can be an integer or list of integers
            buildspec_returncode = self.status["returncode"]

            # if buildspec returncode field is integer we convert to list for check
            if isinstance(buildspec_returncode, int):
                buildspec_returncode = [buildspec_returncode]

            self.logger.debug("Conducting Return Code check")
            self.logger.debug(
                "Status Return Code: %s   Result Return Code: %s"
                % (
                    buildspec_returncode,
                    self.metadata["result"]["returncode"],
                )
            )
            # checks if test returncode matches returncode specified in Buildspec and assign boolean to returncode_match
            returncode_match = (
                self.metadata["result"]["returncode"] in buildspec_returncode
            )

        return returncode_match

    def _check_runtime(self):
        """This method will return a boolean (True/False) based on runtime specified in buildspec and check with test runtime.
        User can specify both `min` and `max`, or just specify `min` or `max`.
        """

        if not self.status.get("runtime"):
            return False

        min_time = self.status["runtime"].get("min") or 0
        max_time = self.status["runtime"].get("max")

        actual_runtime = self.get_runtime()

        # if both min and max are specified
        if min_time and max_time:
            self.logger.debug(
                f"Checking test: {self.name} runtime: {actual_runtime} is greater than min: {float(min_time)} and less than max: {float(max_time)}"
            )
            return float(min_time) < actual_runtime < float(max_time)

        # if min specified
        if min_time and not max_time:
            self.logger.debug(
                f"Checking test: {self.name} runtime: {actual_runtime} is greater than min: {float(min_time)}"
            )
            return float(min_time) < actual_runtime

        # if max specified
        if not min_time and max_time:
            self.logger.debug(
                f"Checking test: {self.name} runtime: {actual_runtime} is less than max: {float(max_time)}"
            )
            return actual_runtime < float(max_time)

    def check_test_state(self):
        """This method is responsible for detecting state of test (PASS/FAIL)
        based on returncode or regular expression.
        """

        self.metadata["result"]["state"] = "FAIL"
        # if status is defined in Buildspec, then check for returncode and regex
        if self.status:

            slurm_job_state_match = False

            # returncode_match is boolean to check if reference returncode matches return code from test
            returncode_match = self._returncode_check()

            # check regex against output or error stream based on regular expression
            # defined in status property. Return value is a boolean
            regex_match = self._check_regex()

            runtime_match = self._check_runtime()

            # if slurm_job_state_codes defined in buildspec.
            # self.builder.metadata["job"] only defined when job run through SlurmExecutor
            if self.status.get("slurm_job_state") and self.metadata.get("job"):
                slurm_job_state_match = (
                    self.status["slurm_job_state"] == self.metadata["job"]["State"]
                )

            self.logger.info(
                "ReturnCode Match: %s Regex Match: %s Slurm Job State Match: %s"
                % (returncode_match, regex_match, slurm_job_state_match)
            )

            # if any of checks is True we set the 'state' to PASS
            state = any(
                [returncode_match, regex_match, slurm_job_state_match, runtime_match]
            )
            if state:
                self.metadata["result"]["state"] = "PASS"

        # if status is not defined we check test returncode, by default 0 is PASS and any other return code is a FAIL
        else:
            if self.metadata["result"]["returncode"] == 0:
                self.metadata["result"]["state"] = "PASS"

        # Return to starting directory for next test
        os.chdir(self.pwd)

    def __str__(self):
        return f"{self.name}/{self.metadata['id']}"

    def __repr__(self):
        return self.__str__()
