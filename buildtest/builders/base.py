"""
BuilderBase class is an abstract class that defines common
functions for any types of builders. Each type schema (script, compiler, spack)
is implemented as separate Builder which extends BuilderBase class.
"""

import datetime
import getpass
import json
import logging
import os
import re
import shutil
import socket
import stat
import uuid
from abc import ABC, abstractmethod
from pathlib import Path

from buildtest.buildsystem.checks import (
    assert_eq_check,
    assert_ge_check,
    assert_range_check,
    exists_check,
    is_dir_check,
    is_file_check,
    regex_check,
    returncode_check,
    runtime_check,
)
from buildtest.cli.compilers import BuildtestCompilers
from buildtest.defaults import BUILDTEST_EXECUTOR_DIR, console
from buildtest.exceptions import BuildTestError, RuntimeFailure
from buildtest.scheduler.job import Job
from buildtest.scheduler.lsf import LSFJob
from buildtest.scheduler.pbs import PBSJob
from buildtest.scheduler.slurm import SlurmJob
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
        self,
        name,
        recipe,
        buildspec,
        executor,
        buildexecutor,
        testdir,
        numprocs=None,
        numnodes=None,
        compiler=None,
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

        self.compiler = compiler
        self.cc = None
        self.fc = None
        self.cxx = None
        self.cflags = None
        self.cxxflags = None
        self.fflags = None
        self.ldflags = None
        self.cppflags = None

        self.metadata = {}

        self.duration = 0

        self.numprocs = numprocs
        self.numnodes = numnodes
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
        self._state = "PENDING"

        # this value holds the 'status' property from the buildspec
        self.status = None

        # this value hosts the 'metrics' property from the buildspec
        self.metrics = None

        self.buildspec = buildspec

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
        self.testid = str(uuid.uuid4())

        self._dependency = False

        self._set_metadata_values()
        self.shell_detection()
        self.sched_init()

    @property
    def dependency(self):
        return self._dependency

    @dependency.setter
    def dependency(self, state):
        self._dependency = state

    def shell_detection(self):
        """Detect shell and shebang used for test script"""

        # if 'shell' property not defined in buildspec use this shell otherwise use the 'shell' property from the executor definition
        self.shell = Shell(
            self.recipe.get("shell")
            or self.buildexecutor.executors[self.executor].shell
        )

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
            schema_table[f"{self.recipe['type']}.schema.json"]["path"]
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
        self.metadata["summary"] = self.recipe.get("summary") or ""

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

        self.metadata["full_id"] = self.testid
        self.metadata["id"] = self.testid[:8]

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

    def is_local_executor(self):
        """Return True if current builder executor type is LocalExecutor otherwise returns False.

        Returns:
            bool: returns True if builder is using executor type LocalExecutor otherwise returns False

        """

        # import issue when putting this at top of file
        from buildtest.executors.local import LocalExecutor

        return isinstance(self.buildexecutor.executors[self.executor], LocalExecutor)

    def is_slurm_executor(self):
        """Return True if current builder executor type is LocalExecutor otherwise returns False.

        Returns:
            bool: returns True if builder is using executor type LocalExecutor otherwise returns False

        """

        # import issue when putting this at top of file
        from buildtest.executors.slurm import SlurmExecutor

        return isinstance(self.buildexecutor.executors[self.executor], SlurmExecutor)

    def is_batch_job(self):
        """Return True/False if builder.job attribute is of type Job instance if not returns False.
        This method indicates if builder has a job submitted to queue
        """

        return isinstance(self.job, Job)

    def start(self):
        """Keep internal timer for test using class :class:`buildtest.utils.timer.Timer`. This method will start the timer for builder which is invoked upon running test."""

        # self.timer = Timer()
        self.timer.start()

    def stop(self):
        """Stop internal timer for builder."""
        # self.duration += self.timer.stop()
        self.timer.stop()

    def retry(self, retry):
        self._retry = retry

    def build(self, modules=None, modulepurge=None, unload_modules=None):
        """This method is responsible for invoking setup, creating test
        directory and writing test. This method is called from an instance
        object of this class that does ``builder.build()``.

        args:
            modules (str, optional): Specify a list of modules to load in the build script
            modulepurge (bool, optional): A boolean to control whether 'module purge' is run before running test
            unload_modules (str, optional): Specify a list of modules to unload in the build script
        """

        self._build_setup()
        self._write_test()
        self._write_build_script(modules, modulepurge, unload_modules)

    def run(self, cmd, timeout=None):
        """Run the test and record the starttime and start timer. We also return the instance
        object of type BuildTestCommand which is used by Executors for processing output and error

        Returns:
            If success, the return type is an object of type :class:`buildtest.utils.command.BuildTestCommand`

            If their is a failure (non-zero) returncode we retry test and if it doesn't pass we
            raise exception of :class:`buildtest.exceptions.RuntimeFailure`
        """

        self.metadata["command"] = cmd

        console.print(f"[blue]{self}[/]: Current Working Directory : {os.getcwd()}")
        # capture output of 'env' and write to file 'build-env.sh' prior to running test
        command = BuildTestCommand("env")
        command.execute()
        content = "".join(command.get_output())
        self.metadata["buildenv"] = os.path.join(self.test_root, "build-env.txt")
        write_file(self.metadata["buildenv"], content)

        console.print(f"[blue]{self}[/]: Running Test via command: [cyan]{cmd}[/cyan]")

        self.record_starttime()
        self.running()
        self.start()

        command = BuildTestCommand(cmd)
        command.execute(timeout=timeout)

        self.logger.debug(f"Running Test via command: {cmd}")
        ret = command.returncode()
        err_msg = " ".join(command.get_error())

        if ret == 0 or self.is_local_executor():
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
            console.print(
                f"[blue]{self}[/]: Running Test via command: [cyan]{cmd}[/cyan]"
            )
            command.execute(timeout=timeout)

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

    def record_starttime(self):
        """This method will record the starttime when job starts execution by using
        ``datetime.datetime.now()``
        """

        self._starttime = datetime.datetime.now()

        # this is recorded in the report file
        self.metadata["result"]["starttime"] = self._starttime.strftime("%Y/%m/%d %X")

    def record_endtime(self):
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

    def state(self):
        return self._state

    def failed(self):
        """Mark test as failure by updating the ``self._state``. A fail test will not be reported in test report"""
        self._state = "FAILED"

    def complete(self):
        """Mark test as complete by updating the ``self._state``. A complete test assumes test ran to completion"""
        self._state = "COMPLETE"

    def running(self):
        self._state = "RUNNING"

    def is_pending(self):
        return self._state == "PENDING"

    def is_complete(self):
        """If builder completes execution of test this method will return ``True`` otherwise returns ``False``.
        A builder could fail due to job cancellation, failure to submit job or raise exception during the run phase.
        In those case, this method will return ``False``."""
        return self._state == "COMPLETE"

    def is_failed(self):
        """Return True if builder fails to run test."""
        return self._state == "FAILED"

    def is_running(self):
        """Return True if builder fails to run test."""
        return self._state == "RUNNING"

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

        self.test_root = os.path.join(self.testdir, self.testid[:8])

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

    def _write_build_script(self, modules=None, modulepurge=None, unload_modules=None):
        """This method will write the content of build script that is run for when invoking
        the builder run method. Upon creating file we set permission of builder script to 755
        so test can be run.
        """

        lines = ["#!/bin/bash"]

        lines += self._default_test_variables()
        lines.append("# source executor startup script")

        if modulepurge:
            lines.append("module purge")

        if unload_modules:
            lines.append("# Specify list of modules to unload")
            for module in unload_modules.split(","):
                lines.append(f"module unload {module}")

        if modules:
            lines.append("# Specify list of modules to load")
            for module in modules.split(","):

                lines.append(f"module load {module}")

        lines += [
            f"source {os.path.join(BUILDTEST_EXECUTOR_DIR, self.executor, 'before_script.sh')}"
        ]

        lines.append("# Run generated script")
        # local executor
        if self.is_local_executor():
            cmd = self._emit_command()

            lines += [" ".join(cmd)]
        # batch executor
        else:
            launcher = self.buildexecutor.executors[self.executor].launcher_command(
                numprocs=self.numprocs, numnodes=self.numnodes
            )
            lines += [" ".join(launcher) + " " + f"{self.testpath}"]

        lines.append("# Get return code")

        # for csh returncode is determined by $status environment, for bash,sh,zsh its $?
        if is_csh_shell(self.shell.name):
            lines.append("set returncode = $status")
        else:
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

        if is_csh_shell(self.shell.name):
            lines = [
                f"setenv BUILDTEST_TEST_NAME {self.name}",
                f"setenv BUILDTEST_TEST_ROOT {self.test_root}",
                f"setenv BUILDTEST_BUILDSPEC_DIR {os.path.dirname(self.buildspec)}",
                f"setenv BUILDTEST_STAGE_DIR {self.stage_dir}",
            ]
            if self.numnodes:
                lines.append(f"setenv BUILDTEST_NUMNODES {self.numnodes}")
            if self.numprocs:
                lines.append(f"setenv BUILDTEST_NUMPROCS {self.numprocs}")

            return lines

        lines = [
            f"export BUILDTEST_TEST_NAME={self.name}",
            f"export BUILDTEST_TEST_ROOT={self.test_root}",
            f"export BUILDTEST_BUILDSPEC_DIR={os.path.dirname(self.buildspec)}",
            f"export BUILDTEST_STAGE_DIR={self.stage_dir}",
        ]

        if self.numnodes:
            lines.append(f"export BUILDTEST_NUMNODES={self.numnodes}")
        if self.numprocs:
            lines.append(f"export BUILDTEST_NUMPROCS={self.numprocs}")

        return lines

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

    def get_job_directives(self):
        """This method returns a list of lines containing the scheduler directives"""
        lines = []

        if self.sbatch:
            for line in self.sbatch:
                lines.append(f"#SBATCH {line}")

            lines += [f"#SBATCH --job-name={self.name}"]
            lines += [f"#SBATCH --output={self.name}.out"]
            lines += [f"#SBATCH --error={self.name}.err"]

        if self.bsub:
            for line in self.bsub:
                lines.append(f"#BSUB {line}")

            lines += [f"#BSUB -J {self.name}"]
            lines += [f"#BSUB -o {self.name}.out"]
            lines += [f"#BSUB -e {self.name}.err"]

        if self.pbs:

            for line in self.pbs:
                lines.append(f"#PBS {line}")
            lines.append(f"#PBS -N {self.name}")

        if self.cobalt:

            for line in self.cobalt:
                lines.append(f"#COBALT {line}")
            lines.append(f"#COBALT --jobname={self.name}")

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
        self.logger.debug(f"Changing permission to 755 for script: {fname}")

    def _get_environment(self, env):
        """Retrieve a list of environment variables defined in buildspec and
        return them as list with the shell equivalent command

        Args:
            env (dict): list of environment variables defined by ``env`` property in buildspec
        """

        lines = []

        # if env not defined return immediately
        if not env:
            return

        if not isinstance(env, dict):
            raise BuildTestError(f"{env} must be a dict but got type: {type(env)}")

        # bash, sh, zsh environment variable declaration is export KEY=VALUE
        if re.fullmatch("(bash|sh|zsh|/bin/bash|/bin/sh|/bin/zsh)$", self.shell.name):
            for k, v in env.items():
                lines.append(f'export {k}="{v}"')

        # tcsh, csh,  environment variable declaration is setenv KEY VALUE
        elif re.fullmatch("(tcsh|csh|/bin/tcsh|/bin/csh)$", self.shell.name):
            for k, v in env.items():
                lines.append(f'setenv {k} "{v}"')

        else:
            self.logger.warning(
                f"{self.shell.name} is not supported, skipping environment variables."
            )
            return

        return lines

    def _get_variables(self, variables):
        """Retrieve a list of  variables defined in buildspec and
        return them as list with the shell equivalent command.

        Args:
            variables (dict): list of variable defined by ``vars`` property in buildspec
        """

        lines = []

        if not variables:
            return

        if not isinstance(variables, dict):
            raise BuildTestError(
                f"{variables} must be a dict but got type:  {type(variables)}"
            )

        # bash, sh, zsh variable declaration is KEY=VALUE
        if re.fullmatch("(bash|sh|zsh|/bin/bash|/bin/sh|/bin/zsh)$", self.shell.name):
            for k, v in variables.items():
                if v:
                    lines.append(f'{k}="{v}"')
                else:
                    lines.append(f"{k}=")

        # tcsh, csh variable declaration is set KEY=VALUE
        elif re.fullmatch("(tcsh|csh|/bin/tcsh|/bin/csh)$", self.shell.name):
            for k, v in variables.items():
                if v:
                    lines.append(f'set {k}="{v}"')
                else:
                    lines.append(f"set {k}=")

        else:
            self.logger.warning(
                f"{self.shell.name} is not supported, skipping environment variables."
            )
            return

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

                pattern = self.metrics[key]["regex"]["exp"]
                match = re.search(pattern, content)

                group_number = self.metrics[key]["regex"].get("item") or 0

                # if pattern match found we assign value to metric
                if match:
                    try:
                        self.metadata["metrics"][key] = match.group(group_number)
                    except IndexError:
                        self.metadata["metrics"][key] = ""

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

        # ensure we are back in stage directory before processing. For batch jobs like Slurm the
        # current working directory is changed to the submit line which can cause issues for file checks
        os.chdir(self.stage_dir)

        self._output = read_file(self.metadata["outfile"])
        self._error = read_file(self.metadata["errfile"])

        self.metadata["output"] = self._output
        self.metadata["error"] = self._error

        self.copy_stage_files()

        # need these lines after self.copy_stage_files()
        console.print(
            f"[blue]{self}[/]: Test completed in {self.metadata['result']['runtime']} seconds"
        )
        console.print(
            f"[blue]{self}[/]: Test completed with returncode: {self.metadata['result']['returncode']}"
        )
        console.print(
            f"[blue]{self}[/]: Writing output file -  [green1]{self.metadata['outfile']}"
        )
        console.print(
            f"[blue]{self}[/]: Writing error file - [red3]{self.metadata['errfile']}"
        )
        self.add_metrics()
        self.check_test_state()

        # self.add_metrics()

        # mark job is success if it finished all post run steps
        self.complete()

    def is_valid_metric(self, name):
        if name not in list(self.metadata["metrics"].keys()):
            return False

        return True

    def check_test_state(self):
        """This method is responsible for detecting state of test (PASS/FAIL) based on returncode or regular expression."""

        self.metadata["result"]["state"] = "FAIL"

        if self.metadata["result"]["returncode"] == 0:
            self.metadata["result"]["state"] = "PASS"

        # if status is defined in Buildspec, then check for returncode and regex
        if self.status:

            slurm_job_state_match = False
            pbs_job_state_match = False
            lsf_job_state_match = False
            assert_ge_match = False
            assert_eq_match = False
            assert_range_match = False
            assert_exists = False
            assert_is_dir = False
            assert_is_file = False

            # returncode_match is boolean to check if reference returncode matches return code from test
            returncode_match = returncode_check(self)

            # check regex against output or error stream based on regular expression
            # defined in status property. Return value is a boolean
            regex_match = regex_check(self)

            runtime_match = runtime_check(self)

            self.metadata["check"]["regex"] = regex_match
            self.metadata["check"]["runtime"] = runtime_match
            self.metadata["check"]["returncode"] = returncode_match

            if self.status.get("slurm_job_state") and isinstance(self.job, SlurmJob):
                slurm_job_state_match = (
                    self.status["slurm_job_state"] == self.job.state()
                )

            if self.status.get("pbs_job_state") and isinstance(self.job, PBSJob):
                pbs_job_state_match = self.status["pbs_job_state"] == self.job.state()

            if self.status.get("lsf_job_state") and isinstance(self.job, LSFJob):
                lsf_job_state_match = self.status["lsf_job_state"] == self.job.state()

            if self.status.get("assert_ge"):
                assert_ge_match = assert_ge_check(self)

            if self.status.get("assert_eq"):
                assert_eq_match = assert_eq_check(self)

            if self.status.get("assert_range"):

                assert_range_match = assert_range_check(self)

            if self.status.get("exists"):
                assert_exists = exists_check(builder=self)

            if self.status.get("is_dir"):
                assert_is_dir = is_dir_check(builder=self)

            if self.status.get("is_file"):
                assert_is_file = is_file_check(builder=self)

            # if any of checks is True we set the 'state' to PASS
            state = any(
                [
                    returncode_match,
                    regex_match,
                    slurm_job_state_match,
                    pbs_job_state_match,
                    lsf_job_state_match,
                    runtime_match,
                    assert_ge_match,
                    assert_eq_match,
                    assert_range_match,
                    assert_exists,
                    assert_is_dir,
                    assert_is_file,
                ]
            )
            if state:
                self.metadata["result"]["state"] = "PASS"
            else:
                self.metadata["result"]["state"] = "FAIL"

            # if 'state' property is specified explicitly honor this value regardless of what is calculated
            if self.status.get("state"):
                self.metadata["result"]["state"] = self.status["state"]

    def _process_compiler_config(self):
        """This method is responsible for setting cc, fc, cxx class variables based
        on compiler selection. The order of precedence is ``config``, ``default``,
        then buildtest setting. Compiler settings in 'config' takes highest precedence,
        this overrides any configuration in 'default'. Finally we resort to compiler
        configuration in buildtest setting if none defined. This method is responsible
        for setting cc, fc, cxx, cflags, cxxflags, fflags, ldflags, and cppflags.
        """
        bc = BuildtestCompilers(configuration=self.configuration)

        self.compiler_group = bc.compiler_name_to_group[self.compiler]
        self.logger.debug(
            f"[{self.name}]: compiler: {self.compiler} belongs to compiler group: {self.compiler_group}"
        )

        # compiler from buildtest settings
        self.bc_compiler = self.configuration.target_config["compilers"]["compiler"][
            self.compiler_group
        ][self.compiler]

        self.logger.debug(self.bc_compiler)
        # set compiler values based on 'default' property in buildspec. This can override
        # compiler setting defined in configuration file. If default is not set we load from buildtest settings for appropriate compiler.

        # set compiler variables to ones defined in buildtest configuration
        self.cc = self.bc_compiler["cc"]
        self.cxx = self.bc_compiler["cxx"]
        self.fc = self.bc_compiler["fc"]

        self.logger.debug(
            f"[{self.name}]: Compiler setting for {self.compiler} from configuration file"
        )
        self.logger.debug(
            f"[{self.name}]: {self.compiler}: {json.dumps(self.bc_compiler, indent=2)}"
        )

        # if default compiler setting provided in buildspec let's assign it.
        if deep_get(self.compiler_section, "default", self.compiler_group):
            self.cc = (
                self.compiler_section["default"][self.compiler_group].get("cc")
                or self.cc
            )
            self.fc = (
                self.compiler_section["default"][self.compiler_group].get("fc")
                or self.fc
            )
            self.cxx = (
                self.compiler_section["default"][self.compiler_group].get("cxx")
                or self.cxx
            )

            self.cflags = (
                self.compiler_section["default"][self.compiler_group].get("cflags")
                or self.cflags
            )
            self.cxxflags = (
                self.compiler_section["default"][self.compiler_group].get("cxxflags")
                or self.cxxflags
            )
            self.fflags = (
                self.compiler_section["default"][self.compiler_group].get("fflags")
                or self.fflags
            )
            self.ldflags = (
                self.compiler_section["default"][self.compiler_group].get("ldflags")
                or self.ldflags
            )
            self.cppflags = (
                self.compiler_section["default"][self.compiler_group].get("cppflags")
                or self.cppflags
            )
        # if compiler instance defined in config section read from buildspec. This overrides default section if specified
        if deep_get(self.compiler_section, "config", self.compiler):
            self.logger.debug(
                f"[{self.name}]: Detected compiler: {self.compiler} in 'config' scope overriding default compiler group setting for: {self.compiler_group}"
            )

            self.cc = (
                self.compiler_section["config"][self.compiler].get("cc") or self.cc
            )
            self.fc = (
                self.compiler_section["config"][self.compiler].get("fc") or self.fc
            )
            self.cxx = (
                self.compiler_section["config"][self.compiler].get("cxx") or self.cxx
            )
            self.cflags = (
                self.compiler_section["config"][self.compiler].get("cflags")
                or self.cflags
            )
            self.cxxflags = (
                self.compiler_section["config"][self.compiler].get("cxxflags")
                or self.cxxflags
            )
            self.fflags = (
                self.compiler_section["config"][self.compiler].get("fflags")
                or self.fflags
            )
            self.cppflags = (
                self.compiler_section["config"][self.compiler].get("cppflags")
                or self.cppflags
            )
            self.ldflags = (
                self.compiler_section["config"][self.compiler].get("ldflags")
                or self.ldflags
            )

        self.logger.debug(
            f"cc: {self.cc}, cxx: {self.cxx} fc: {self.fc} cppflags: {self.cppflags} cflags: {self.cflags} fflags: {self.fflags} ldflags: {self.ldflags}"
        )
        # this condition is a safety check before compiling code to ensure if all C, C++, Fortran compiler not set we raise error
        if not self.cc and not self.cxx and not self.fc:
            raise BuildTestError(
                "Unable to set C, C++, and Fortran compiler wrapper, please specify 'cc', 'cxx','fc' in your compiler settings in buildtest configuration or specify in buildspec file. "
            )

    def __str__(self):
        return f"{self.name}/{self.metadata['id']}"

    def __repr__(self):
        return self.__str__()
