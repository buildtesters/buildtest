"""
BuilderBase class is an abstract class that defines common
functions for any types of builders. Each type schema (script, compiler, spack)
is implemented as separate Builder which extends BuilderBase class.
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
from buildtest.defaults import BUILDTEST_EXECUTOR_DIR, console
from buildtest.exceptions import RuntimeFailure
from buildtest.executors.job import Job
from buildtest.schemas.defaults import schema_table
from buildtest.utils.command import BuildTestCommand
from buildtest.utils.file import create_dir, read_file, write_file
from buildtest.utils.shell import Shell, is_csh_shell
from buildtest.utils.timer import Timer
from buildtest.utils.tools import deep_get


class BuilderBase(ABC):
    """The BuilderBase is an abstract class that implements common functions used for building and running test.

    buildtest will create a builder object which resembles a test. The builder will contains metadata that is unique
    to each builder that is captured in the report file upon completion of test.

    """

    def __init__(
        self, name, recipe, buildspec, executor, buildexecutor, testdir, numprocs=None
    ):
        """The BuilderBase provides common functions for any builder. The builder
        is an instance of BuilderBase. The initializer method will setup the builder
        attributes based on input test by ``name`` parameter.

        Args:
            name (str): Name of test in buildspec recipe
            recipe (str): The loaded test section from the buildspec file
            buildspec (str): Full path to buildspec file
            buildexecutor (:obj:`buildtest.executors.setup.BuildExecutor`): An instance of BuildExecutor class used for accessing executors
            testdir (str): Test directory where tests are written. Must be full path on filesystem.
        """

        self.name = name

        self.metadata = {}

        self.duration = 0

        self.numprocs = numprocs
        self._retry = 1
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

        # used for storing output content
        self._output = None
        # used for storing error content
        self._error = None

        # strip .yml extension from file name
        file_name = re.sub("[.](yml)", "", os.path.basename(buildspec))
        self.testdir = os.path.join(testdir, self.executor, file_name, self.name)

        self.logger = logging.getLogger(__name__)

        self.logger.debug(f"Processing Buildspec File: {self.buildspec}")
        self.logger.debug(f"Processing Test: {self.name}")

        # get type attribute from Executor class (local, slurm, cobalt, pbs, lsf)
        self.executor_type = buildexecutor.executors[self.executor].type
        self.buildexecutor = buildexecutor

        # Generate a unique id for the build based
        self.test_uid = str(uuid.uuid4())

        self._set_metadata_values()
        self.shell_detection()
        self.sched_init()

    def shell_detection(self):
        """Detect shell and shebang used for test script"""

        # The default shell will be bash
        self.default_shell = Shell()

        self.shell = Shell(self.recipe.get("shell", "bash"))

        # set shebang to value defined in Buildspec, if not defined then get one from Shell class
        self.shebang = (
            self.recipe.get("shebang") or f"{self.shell.shebang} {self.shell.opts}"
        )
        self.logger.debug("Using shell %s", self.shell.name)
        self.logger.debug(f"Shebang used for test: {self.shebang}")

    def _set_metadata_values(self):
        """This method sets ``self.metadata`` that contains metadata for each builder object."""
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

        self.metadata["description"] = self.recipe.get("description") or ""

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
        self.metadata["check"] = {"returncode": "N/A", "regex": "N/A", "runtime": "N/A"}

        self.metadata["metrics"] = {}

        # used to store job id from batch scheduler
        self.metadata["jobid"] = None
        # used to store job metrics for given JobID from batch scheduler
        self.metadata["job"] = {}

        self.metadata["full_id"] = self.test_uid
        self.metadata["id"] = self.test_uid[:8]

    def get_test_extension(self):
        """Return the test extension, which depends on the shell type. By default we return `sh`
        file extension for all shells except for `csh` which will return "csh" extension.

        Returns
            str: Returns test extension name for generated test.
        """

        # for csh we return shell extension 'csh'
        if is_csh_shell(self.shell.name):
            return "csh"

        # default file extension
        return "sh"

    def _is_local_executor(self):
        """Return True if current builder executor type is LocalExecutor otherwise returns False.

        Returns:
            bool: returns True if builder is using executor type LocalExecutor otherwise returns False

        """

        # import issue when putting this at top of file
        from buildtest.executors.local import LocalExecutor

        if isinstance(self.buildexecutor.executors[self.executor], LocalExecutor):
            return True

        return False

    def is_batch_job(self):
        """Return True/False if builder.job attribute is of type Job instance if not returns False.
        This method indicates if builder has a job submitted to queue
        """

        if isinstance(self.job, Job):
            return True

        return False

    def start(self):
        """Keep internal timer for test using class :class:`buildtest.utils.timer.Timer`. This method will start the timer for builder which is invoked upon running test."""

        # self.timer = Timer()
        self.timer.start()

    def stop(self):
        """Stop internal timer for builder."""
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

    def retry(self, retry):
        self._retry = retry

    def run(self, cmd):
        """Run the test and record the starttime and start timer. We also return the instance
        object of type BuildTestCommand which is used by Executors for processing output and error

        Returns:
            If success, the return type is an object of type :class:`buildtest.utils.command.BuildTestCommand`

            If their is a failure (non-zero) returncode we retry test and if it doesn't pass we
            raise exception of :class:`buildtest.exceptions.RuntimeFailure`
        """

        # self.runcmd = self.run_command()
        self.metadata["command"] = cmd

        console.print(f"[blue]{self}[/]: Running Test via command: [cyan]{cmd}[/cyan]")

        self.starttime()
        self.start()

        command = BuildTestCommand(cmd)
        command.execute()

        self.logger.debug(f"Running Test via command: {cmd}")
        ret = command.returncode()
        err_msg = " ".join(command.get_error())

        if ret == 0 or self._is_local_executor():
            return command

        err = f"{self} failed to submit job with returncode: {ret} \n"
        console.print(f"[red]{err}")
        console.print(f"[red]{err_msg}")

        ########## Retry for failed tests  ##########

        print(
            f"{self}: Detected failure in running test, will attempt to retry test: {self._retry} times"
        )
        for run in range(1, self._retry + 1):
            print(f"{self}: Run - {run}/{self._retry}")
            command = BuildTestCommand(cmd)
            command.execute()

            self.logger.debug(f"Running Test via command: {cmd}")
            ret = command.returncode()
            err_msg = " ".join(command.get_error())

            # if we recieve a returncode of 0 return immediately with the instance of command
            if ret == 0:
                return command

            err = f"{self} failed to submit job with returncode: {ret} \n"
            console.print(f"[red]{err}")
            console.print(f"[red]{err_msg}")

        raise RuntimeFailure(err)

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
        is seconds.
        """

        runtime = self._endtime - self._starttime
        self._runtime = runtime.total_seconds()
        self.metadata["result"]["runtime"] = self._runtime

    def get_runtime(self):
        """Return runtime of test"""
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
        """If builder completes execution of test this method will return ``True`` otherwise returns ``False``.
        A builder could fail due to job cancellation, failure to submit job or raise exception during the run phase.
        In those case, this method will return ``False``."""
        return self._buildstate is True

    def is_failure(self):
        """Return True if builder fails to run test."""
        return self._buildstate is False

    def is_unknown(self):
        """Returns True if builder state is unknown which is the state if job is still running"""
        return self._buildstate is None

    def run_command(self):
        """Command used to run the build script. buildtest will change into the stage directory (self.stage_dir)
        before running the test.
        """

        return f"sh {os.path.basename(self.build_script)}"

    def copy_stage_files(self):
        """Copy output and error file into test root directory."""

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
        includes the following:

        1. Creating Test directory and stage directory
        2. Resolve full path to generated test script and build script
        3. Copy all files from buildspec directory to stage directory
        """

        create_dir(self.testdir)

        # num_content = len(os.listdir(self.testdir))
        # the testid is incremented for every run, this can be done by getting
        # length of all files in testdir and creating a directory. Subsequent
        # runs will increment this counter

        self.test_root = os.path.join(self.testdir, self.test_uid[:8])

        create_dir(self.test_root)

        msg = f"Creating test directory: {self.test_root}"
        self.logger.debug(msg)
        console.print(f"[blue]{self}:[/] {msg}")

        self.metadata["testroot"] = self.test_root

        self.stage_dir = os.path.join(self.test_root, "stage")

        # create stage and run directories
        create_dir(self.stage_dir)
        msg = f"Creating the stage directory: {self.stage_dir}"
        self.logger.debug(msg)

        console.print(f"[blue]{self}:[/] {msg}")

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
        use local executors

        Returns:
            list: a list to show generated command used to run test.

            Test can be run without any argument with path to script: ``/path/to/script.sh``
            Test can be run with shell name followed by path to script: ``bash /path/to/script.sh``
            Test can be run with shell name, shell options and path to script: ``bash -x /path/to/script.sh``
        """

        if not self.recipe.get("shell") or self.recipe.get("shell") == "python":
            return [self.testpath]

        if not self.shell.opts:
            return [self.shell.name, self.testpath]

        return [self.shell.name, self.shell.opts, self.testpath]

    def _default_test_variables(self):
        """Return a list of lines inserted in build script that define buildtest specific variables
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
        """This method will write the content of build script that is run for when invoking
        the builder run method. Upon creating file we set permission of builder script to 755
        so test can be run.
        """

        lines = ["#!/bin/bash"]

        lines += self._default_test_variables()
        lines.append("# source executor startup script")

        lines += [
            f"source {os.path.join(BUILDTEST_EXECUTOR_DIR, self.executor, 'before_script.sh')}"
        ]

        lines.append("# Run generated script")
        # local executor
        if self._is_local_executor():
            cmd = self._emit_command()

            lines += [" ".join(cmd)]
        # batch executor
        else:
            launcher = self.buildexecutor.executors[self.executor].launcher_command(
                self.numprocs
            )
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
        self.metadata["build_script"] = self.build_script

        # self.runcmd = self.run_command()
        # self.metadata["command"] = self.runcmd

        console.print(f"[blue]{self}:[/] Writing build script: {self.build_script}")

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

        self.burstbuffer = self.recipe.get("BB") or deep_get(
            self.recipe, "executors", self.executor, "BB"
        )
        self.datawarp = self.recipe.get("DW") or deep_get(
            self.recipe, "executors", self.executor, "DW"
        )

    def get_slurm_directives(self):
        """Get #SBATCH lines based on ``sbatch`` property by calling :class:`buildtest.buildsystem.batch.SlurmBatchScript`"""
        jobscript = SlurmBatchScript(sbatch=self.sbatch)
        lines = jobscript.get_headers()
        lines += [f"#SBATCH --job-name={self.name}"]
        lines += [f"#SBATCH --output={self.name}.out"]
        lines += [f"#SBATCH --error={self.name}.err"]

        return lines

    def get_lsf_directives(self):
        """Get #BSUB lines based on ``bsub`` property by calling :class:`buildtest.buildsystem.batch.LSFBatchScript`"""
        jobscript = LSFBatchScript(bsub=self.bsub)
        lines = jobscript.get_headers()
        lines += [f"#BSUB -J {self.name}"]
        lines += [f"#BSUB -o {self.name}.out"]
        lines += [f"#BSUB -e {self.name}.err"]

        return lines

    def get_pbs_directives(self):
        """Get #PBS lines based on ``pbs`` property by calling :class:`buildtest.buildsystem.batch.PBSBatchScript`"""
        jobscript = PBSBatchScript(pbs=self.pbs)
        lines = jobscript.get_headers()
        lines += [f"#PBS -N {self.name}"]

        return lines

    def get_cobalt_directives(self):
        """Get #COBALT lines based on ``cobalt`` property by calling :class:`buildtest.buildsystem.batch.CobaltBatchScript`"""
        jobscript = CobaltBatchScript(cobalt=self.cobalt)
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
        """Get Burst Buffer directives (**#BB**) lines specified by ``BB`` property

        Args:
            burstbuffer (str): Burst Buffer configuration specified by ``BB`` property in buildspec

        Returns:
            list: List of string values containing containing ``#BB`` directives written in test
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
        """Get Cray Data Warp directives (**#DW**) lines specified by ``DW`` property.

        Args:
            datawarp (str): Data Warp configuration specified by ``DW`` property in buildspec

        Returns:
            list: List of string values containing containing ``#DW`` directives written in test
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

        Args:
            env (dict): list of environment variables defined by ``env`` property in buildspec
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

        Args:
            variables (dict): list of variable defined by ``vars`` property in buildspec
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
        """This method is called after test is complete. This method will copy files from stage directory
        such as output, error and test script. We will check state of test and mark job is complete.
        """

        self._output = read_file(self.metadata["outfile"])
        self._error = read_file(self.metadata["errfile"])

        self.metadata["output"] = self._output
        self.metadata["error"] = self._error

        self.copy_stage_files()

        # need these lines after self.copy_stage_files()
        console.print(
            f"[blue]{self}[/]: Writing output file -  [green1]{self.metadata['outfile']}"
        )
        console.print(
            f"[blue]{self}[/]: Writing error file - [red3]{self.metadata['errfile']}"
        )

        self.check_test_state()

        self.add_metrics()

        # mark job is success if it finished all post run steps
        self.success()

    def _check_regex(self):
        """This method conducts a regular expression check using
        `re.search <https://docs.python.org/3/library/re.html#re.search>`_
        with regular expression defined in Buildspec. User must specify an
        output stream (stdout, stderr) to select when performing regex. In
        buildtest, this would read the .out or .err file based on stream and
        run the regular expression to see if there is a match. This method
        will return a boolean True indicates there is a match otherwise False
        if ``regex`` object not defined or ``re.search`` doesn't find a match.

        Returns:
            bool: Returns True if their is a regex match otherwise returns False.
        """

        regex_match = False

        if not self.status.get("regex"):
            return regex_match

        file_stream = None
        if self.status["regex"]["stream"] == "stdout":
            self.logger.debug(
                f"Detected regex stream 'stdout' so reading output file: {self.metadata['outfile']}"
            )
            content = self.output()

            file_stream = self.metadata["outfile"]

        elif self.status["regex"]["stream"] == "stderr":
            self.logger.debug(
                f"Detected regex stream 'stderr' so reading error file: {self.metadata['errfile']}"
            )
            content = self.error()

            file_stream = self.metadata["errfile"]
        self.logger.debug(f"Applying re.search with exp: {self.status['regex']['exp']}")

        regex = re.search(self.status["regex"]["exp"], content)

        console.print(
            f"[blue]{self}[/]: performing regular expression - '{self.status['regex']['exp']}' on file: {file_stream}"
        )
        if regex:
            console.print(
                f"[blue]{self}[/]: Regular Expression Match - [green]Success![/]"
            )
        else:
            console.print(
                f"[blue]{self}[/]: Regular Expression Match - [red]Failed![/]"
            )

        # perform a regex search based on value of 'exp' key defined in Buildspec with content file (output or error)
        return regex is not None

    def _returncode_check(self):
        """Check status check of ``returncode`` field if specified in status property."""

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
            console.print(
                f"[blue]{self}[/]: Checking returncode - {self.metadata['result']['returncode']} is matched in list {buildspec_returncode}"
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
        """This method is responsible for detecting state of test (PASS/FAIL) based on returncode or regular expression."""

        self.metadata["result"]["state"] = "FAIL"

        if self.metadata["result"]["returncode"] == 0:
            self.metadata["result"]["state"] = "PASS"

        # if status is defined in Buildspec, then check for returncode and regex
        if self.status:

            slurm_job_state_match = False

            # returncode_match is boolean to check if reference returncode matches return code from test
            returncode_match = self._returncode_check()

            # check regex against output or error stream based on regular expression
            # defined in status property. Return value is a boolean
            regex_match = self._check_regex()

            runtime_match = self._check_runtime()

            self.metadata["check"]["regex"] = regex_match
            self.metadata["check"]["runtime"] = runtime_match
            self.metadata["check"]["returncode"] = returncode_match

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
            else:
                self.metadata["result"]["state"] = "FAIL"

            # if 'state' property is specified explicitly honor this value regardless of what is calculated
            if self.status.get("state"):
                self.metadata["result"]["state"] = self.status["state"]

    def __str__(self):
        return f"{self.name}/{self.metadata['id']}"

    def __repr__(self):
        return self.__str__()
