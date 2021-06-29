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
from buildtest.defaults import BUILDTEST_EXECUTOR_DIR
from buildtest.exceptions import ExecutorError
from buildtest.buildsystem.batch import (
    SlurmBatchScript,
    LSFBatchScript,
    CobaltBatchScript,
    PBSBatchScript,
)
from buildtest.schemas.defaults import schema_table
from buildtest.utils.command import BuildTestCommand
from buildtest.utils.file import create_dir, write_file, read_file
from buildtest.utils.timer import Timer
from buildtest.utils.shell import Shell


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

        # The type must match the type of the builder
        self.recipe = recipe

        self.executor = executor

        # For batch jobs this variable is an instance of Job class which would be one of the subclass
        self.job = None

        # Controls the state of the builder object, a complete job  will set
        # this value to True. A job cancellation or job failure in submission will set this to False
        self.state = None

        # keeps track of job state as job progress through queuing system. This is
        # applicable for builders using batch executor.
        self.job_state = None

        # this value holds the 'status' property from the schema which is assigned in the subclass
        self.status = None

        self.buildspec = buildspec
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

    def _set_metadata_values(self):
        """This method sets self.metadata that contains metadata for each builder object."""
        self.metadata["name"] = self.name
        self.metadata["buildspec"] = self.buildspec

        # store recipe
        # self.metadata["recipe"] = self.recipe

        # store tags
        self.metadata["tags"] = self.recipe.get("tags")
        # store executor name
        self.metadata["executor"] = self.executor

        # store schemafile used for validating
        self.metadata["schemafile"] = os.path.basename(
            schema_table[f"{self.recipe['type']}-v1.0.schema.json"]["path"]
        )

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

        # used to store compiler name used the test. Only applicable with compiler schema
        self.metadata["compiler"] = None

        self.metadata["result"] = {}
        self.metadata["result"]["state"] = "N/A"
        self.metadata["result"]["returncode"] = "-1"
        self.metadata["result"]["runtime"] = 0

        # used to store job id from batch scheduler
        self.metadata["jobid"] = None
        # used to store job metrics for given JobID from batch scheduler
        self.metadata["job"] = None
        # Generate a unique id for the build based on key and unique string
        self.metadata["full_id"] = self._generate_unique_id()
        self.metadata["id"] = self.metadata["full_id"][:8]

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

    def start(self):
        """Keep internal time for start of test. We start timer by calling
        Timer class
        """

        self.timer = Timer()
        self.timer.start()

    def stop(self):
        """Stop  timer of test and calculate duration."""

        self.duration += self.timer.stop()

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

        if ret != 0:
            err = f"[{self.metadata['name']}] failed to submit job with returncode: {ret} \n"
            raise ExecutorError(err)

        return command

    def starttime(self):
        """This method will record the starttime when job starts execution by using ``datetime.datetime.now()``"""
        self._starttime = datetime.datetime.now()

        # this is recorded in the report file
        self.metadata["result"]["starttime"] = self._starttime.strftime("%Y/%m/%d %X")

    def endtime(self):
        """This method is called upon termination of job, we get current time using ``datetime.datetime.now()`` and calculate runtime of job"""
        self._endtime = datetime.datetime.now()

        # this is recorded in the report file
        self.metadata["result"]["endtime"] = self._endtime.strftime("%Y/%m/%d %X")

        self.runtime()

    def runtime(self):
        # Calculate runtime of job by calculating delta between endtime and starttime.

        runtime = self._endtime - self._starttime
        self.metadata["result"]["runtime"] = runtime.total_seconds()

    def complete(self):
        """This method is invoked to indicate that builder job is complete after polling job."""
        self.state = "COMPLETE"

    def incomplete(self):
        """This method indicates that builder job is not complete after polling job either job was
        cancelled by scheduler or job failed to run.
        """
        self.state = "INCOMPLETE"

    def run_command(self):
        """Command used to run the build script. buildtest will change into the stage directory (self.stage_dir)
        before running the test.
        """

        return f"sh {os.path.basename(self.build_script)}"

    def copy_stage_files(self):
        """Copy output and error file into test root directory since stage directory will be removed."""

        shutil.copy2(
            self.metadata["outfile"],
            os.path.join(self.test_root, os.path.basename(self.metadata["outfile"])),
        )
        shutil.copy2(
            self.metadata["errfile"],
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
        num_content = len(os.listdir(self.testdir))
        # the testid is incremented for every run, this can be done by getting
        # length of all files in testdir and creating a directory. Subsequent
        # runs will increment this counter

        self.test_root = os.path.join(self.testdir, str(num_content))

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

        self.metadata["testpath"] = self.testpath

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
            return [self.metadata["testpath"]]

        if not self.shell.opts:
            return [self.shell.name, self.metadata["testpath"]]

        return [self.shell.name, self.shell.opts, self.metadata["testpath"]]

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
            lines += [" ".join(launcher) + " " + f"{self.metadata['testpath']}"]

        lines.append("\n")
        lines.append("# Get return code")
        lines.append("returncode=$?")
        lines.append("\n")
        lines.append("# Exit with return code")
        lines.append("exit $returncode")

        lines = "\n".join(lines)
        write_file(self.build_script, lines)
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

        self.logger.info(f"Opening Test File for Writing: {self.metadata['testpath']}")

        write_file(self.metadata["testpath"], lines)

        self.metadata["test_content"] = lines

        self._set_execute_perm(self.metadata["testpath"])
        # copy testpath to run_dir
        shutil.copy2(
            self.metadata["testpath"],
            os.path.join(self.test_root, os.path.basename(self.metadata["testpath"])),
        )

    def _get_scheduler_directives(self, bsub, sbatch, cobalt, pbs, batch):
        """Get Scheduler Directives for LSF, Slurm or Cobalt if we are processing
        test with one of the executor types. This method will return a list
        of string containing scheduler directives generally found at top of script.
        If test is local executor we return an empty list

        :param bsub: bsub property from buildspec
        :param sbatch: sbatch property from buildspec
        :param cobalt: cobalt property  from buildspec
        :param pbs: pbs property  from buildspec
        :param batch: batch property from buildspec
        """

        lines = []
        if self.executor_type == "local":
            return

        if self.executor_type == "lsf":
            script = LSFBatchScript(batch, bsub)

            lines += script.get_headers()
            lines += [f"#BSUB -J {self.name}"]
            lines += [f"#BSUB -o {self.name}.out"]
            lines += [f"#BSUB -e {self.name}.err"]

        elif self.executor_type == "slurm":

            script = SlurmBatchScript(batch, sbatch)
            lines += script.get_headers()
            lines += [f"#SBATCH --job-name={self.name}"]
            lines += [f"#SBATCH --output={self.name}.out"]
            lines += [f"#SBATCH --error={self.name}.err"]

        elif self.executor_type == "cobalt":
            script = CobaltBatchScript(batch, cobalt)
            lines += script.get_headers()
            lines += [f"#COBALT --jobname {self.name}"]

        elif self.executor_type == "pbs":
            script = PBSBatchScript(batch, pbs)
            lines += script.get_headers()
            lines += [f"#PBS -N {self.name}"]

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
        for arg in burstbuffer:
            lines += [f"#BB {arg} "]

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
        for arg in datawarp:
            lines += [f"#DW {arg}"]

        return lines

    def _set_execute_perm(self, fname):
        """Apply chmod 755 to input file name. The path must be an absolute path to script"""
        """Set permission to 755 on executable"""

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

            # tcsh, csh,  environment variable declaration is setenv KEY VALUE
            elif re.fullmatch("(tcsh|csh|/bin/tcsh|/bin/csh)$", shell):
                for k, v in env.items():
                    lines.append("setenv %s %s" % (k, v))

            else:
                self.logger.warning(
                    f"{shell} is not supported, skipping environment variables."
                )

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
                    lines.append("%s=%s" % (k, v))

            # tcsh, csh variable declaration is set KEY=VALUE
            elif re.fullmatch("(tcsh|csh|/bin/tcsh|/bin/csh)$", shell):
                for k, v in variables.items():
                    lines.append("set %s=%s" % (k, v))

            else:
                self.logger.warning(
                    f"{shell} is not supported, skipping environment variables."
                )
        return lines

    def _generate_unique_id(self):
        """Generate a unique build id using ``uuid.uuid4()``."""

        unique_id = str(uuid.uuid4())
        return unique_id

    @abstractmethod
    def generate_script(self):
        """Build the testscript content implemented in each subclass"""

    def __str__(self):
        return (
            f"builder object created with test name: {self.name} "
            f"for schema type: {self.type} "
            f"with ID: {self.metadata['full_id']}"
        )

    def __repr__(self):
        return self.__str__()
