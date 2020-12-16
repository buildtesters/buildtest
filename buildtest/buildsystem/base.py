"""
BuilderBase class is an abstract class that defines common
functions for any types of builders. Each type schema (script, compiler)
is implemented as separate Builder.

ScriptBuilder class implements 'type: script'
CompilerBuilder class implements 'type: compiler'
"""


import logging
import os
import re
import shutil
import stat
import sys
import uuid
from abc import ABC, abstractmethod
from buildtest.buildsystem.batch import (
    SlurmBatchScript,
    LSFBatchScript,
    CobaltBatchScript,
)
from buildtest.defaults import executor_root
from buildtest.schemas.defaults import schema_table
from buildtest.utils.file import create_dir, write_file
from buildtest.utils.timer import Timer
from buildtest.utils.shell import Shell


class BuilderBase(ABC):
    """ The BuilderBase is an abstract class that implements common functions for
        any kind of builder.
    """

    def __init__(self, name, recipe, buildspec, testdir=None):
        """ The BuilderBase provides common functions for any builder. The builder
            is an instance of BuilderBase. The initializer method will setup the builder
            attributes based on input test by ``name`` parameter.

            :param name: Name of test in Buildspec recipe
            :type name: str, required
            :param recipe: the loaded section from the buildspec for the user.
            :type recipe: dict, required
            :param buildspec: the pull path to the Buildspec file, must exist.
            :type buildspec: str, required
            :param testdir: Test Destination directory where to write test
            :type testdir: str, optional
        """

        self.name = name
        self.pwd = os.getcwd()
        self.result = {}
        self.metadata = {}

        self.duration = 0
        self.job_state = None

        # ensure buildspec ends with .yml extension
        assert os.path.basename(buildspec).endswith(".yml")

        self.buildspec = buildspec
        file_name = re.sub("[.](yml)", "", os.path.basename(buildspec))
        self.testdir = os.path.join(
            testdir, recipe.get("executor"), file_name, self.name
        )

        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"Processing Buildspec: {self.buildspec}")
        self.logger.debug(f"Processing Buildspec section: {self.name}")

        # A builder is required to define the type attribute
        if not hasattr(self, "type"):
            sys.exit(
                "A builder base is required to define the 'type' as a class variable"
            )

        # The type must match the type of the builder
        self.recipe = recipe

        self.executor = self.recipe.get("executor")
        self.executor_type = self.detect_executor()

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

    def _set_metadata_values(self):
        """This method sets self.metadata that contains metadata for each builder object."""
        self.metadata["name"] = self.name
        self.metadata["buildspec"] = self.buildspec
        self.metadata["recipe"] = self.recipe
        self.metadata["tags"] = self.recipe.get("tags")
        self.metadata["result"] = {}
        self.metadata["result"]["state"] = "N/A"
        self.metadata["result"]["returncode"] = "-1"
        self.metadata["result"]["runtime"] = 0
        self.metadata["schemafile"] = os.path.basename(
            schema_table[f"{self.recipe['type']}-v1.0.schema.json"]["path"]
        )
        self.metadata["executor"] = self.executor

    def detect_executor(self):
        """ Return executor type based on executor property. The executor is in
            format <type>.<name> so we check for keywords that start with known executor
            types ``local``, ``slurm``, ``lsf``, ``cobalt``
        """
        executor_types = ["local", "slurm", "lsf", "cobalt"]
        for name in executor_types:
            if self.executor.startswith(name):
                return name

    def get_test_extension(self):
        """ Return the test extension, which depends on the shell used. Based
            on the value of ``shell`` key we return the shell extension.

            shell: bash --> sh (default)

            :return: returns test extension based on shell type
            :rtype: str
        """

        self.logger.debug("Setting test extension to 'sh'")
        return "sh"

    def start(self):
        """ Keep internal time for start of test. We start timer by calling
            Timer class
        """

        self.timer = Timer()
        self.timer.start()

    def stop(self):
        """Stop  timer of test and calculate duration."""

        self.duration += self.timer.stop()

    def build(self):
        """ This method is responsible for invoking setup, creating test
            directory and writing test. This method is called from an instance
            object of this class that does ``builder.build()``.
        """

        self._build_setup()
        self._write_test()
        self._create_symlinks()

    def _build_setup(self):
        """ This method is the setup operation to get ready to build test which
            includes getting unique build id, setting up metadata object to store
            test details such as where test will be located and directory of test.
            This section cannot be reached without a valid, loaded recipe.
        """

        # Generate a unique id for the build based on key and unique string
        self.metadata["full_id"] = self._generate_unique_id()
        self.metadata["id"] = self.metadata["full_id"][:8]

        create_dir(self.testdir)
        num_content = len(os.listdir(self.testdir))
        # the testid is incremented for every run, this can be done by getting
        # length of all files in testdir and creating a directory. Subsequent
        # runs will increment this counter
        self.test_id = os.path.join(self.testdir, str(num_content))
        create_dir(self.test_id)

        self.stage_dir = os.path.join(self.test_id, "stage")
        self.run_dir = os.path.join(self.test_id, "run")
        # create stage and run directories
        create_dir(self.stage_dir)
        create_dir(self.run_dir)

        # Derive the path to the test script
        self.metadata["testpath"] = "%s.%s" % (
            os.path.join(self.stage_dir, "generate"),
            self.get_test_extension(),
        )
        self.metadata["testpath"] = os.path.expandvars(self.metadata["testpath"])
        self.metadata["testroot"] = self.test_id

    def _get_scheduler_directives(self):
        """ Get Scheduler Directives for LSF, Slurm or Cobalt if we are processing
            test with one of the executor types. This method will return a list
            of string containing scheduler directives generally found at top of script.
            If test is local executor we return an empty list
        """

        lines = []
        if self.executor_type == "local":
            return

        if self.executor_type == "lsf":
            script = LSFBatchScript(self.recipe.get("batch"), self.recipe.get("bsub"))

            lines += script.get_headers()
            lines += [f"#BSUB -J {self.name}"]
            lines += [f"#BSUB -o {self.name}.out"]
            lines += [f"#BSUB -e {self.name}.err"]

        elif self.executor_type == "slurm":

            script = SlurmBatchScript(
                self.recipe.get("batch"), self.recipe.get("sbatch")
            )
            lines += script.get_headers()
            lines += [f"#SBATCH --job-name={self.name}"]
            lines += [f"#SBATCH --output={self.name}.out"]
            lines += [f"#SBATCH --error={self.name}.err"]

        elif self.executor_type == "cobalt":
            script = CobaltBatchScript(
                self.recipe.get("batch"), self.recipe.get("cobalt")
            )
            lines += script.get_headers()
            lines += [f"#COBALT --jobname {self.name}"]

        return lines

    def _get_burst_buffer(self):
        """Get Burst Buffer directives (#BB) lines"""

        lines = []
        if not self.recipe.get("BB"):
            return

        for arg in self.recipe.get("BB"):
            lines += ["#BB " + arg]

        return lines

    def _get_data_warp(self):
        """Get Cray Data Warp directives (#DW) lines"""

        lines = []
        if not self.recipe.get("DW"):
            return

        for arg in self.recipe.get("DW"):
            lines += ["#DW " + arg]

        return lines

    def _set_execute_perm(self):
        """Set permission to 755 on executable"""

        # Change permission of the file to executable
        os.chmod(
            self.metadata["testpath"],
            stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH,
        )
        self.logger.debug(
            f"Applying permission 755 to {self.metadata['testpath']} so that test can be executed"
        )

    def _get_test_heading(self):
        """Returns the declaration of test content which is includes the shebang, scheduler
           directives and source executor before script """

        # start of each test should have the shebang
        lines = [self.shebang]

        # if shell is python the generated testscript will be run via bash, we invoke
        # python script in bash script.
        if self.shell.name == "python":
            lines = [self.default_shell.shebang]

        batch_directives_lines = self._get_scheduler_directives()
        if batch_directives_lines:
            lines += batch_directives_lines

        burst_buffer_lines = self._get_burst_buffer()
        if burst_buffer_lines:
            lines += burst_buffer_lines

        data_warp_lines = self._get_data_warp()
        if data_warp_lines:
            lines += data_warp_lines

        lines += [
            f"source {os.path.join(executor_root, self.executor, 'before_script.sh')}"
        ]
        return lines

    def _write_test(self):
        """ This method is responsible for invoking ``generate_script`` that
            formulates content of testscript which is implemented in each subclass.
            Next we write content to file and apply 755 permission on script so
            it has executable permission.
        """

        # Implementation to write file generate.sh
        # start of each test should have the shebang
        lines = self._get_test_heading()

        lines += self.generate_script()

        lines += [
            f"source {os.path.join(executor_root, self.executor, 'after_script.sh')}"
        ]

        lines = "\n".join(lines)

        self.logger.info(f"Opening Test File for Writing: {self.metadata['testpath']}")

        write_file(self.metadata["testpath"], lines)

        self._set_execute_perm()
        # copy testpath to run_dir
        shutil.copy2(
            self.metadata["testpath"],
            os.path.join(self.run_dir, os.path.basename(self.metadata["testpath"])),
        )

    def _create_symlinks(self):
        """This method will retrieve all files relative to buildspec file and
        create symlinks in destination directory
        """
        buildspec_directory = os.path.dirname(self.buildspec)
        # list all files in current directory where buildspec file resides
        files = [
            os.path.join(buildspec_directory, file)
            for file in os.listdir(buildspec_directory)
        ]

        # create symlink for all files directory where buildspec file exists
        for file in files:
            os.symlink(
                file, os.path.join(self.test_id, "stage", os.path.basename(file))
            )

    def get_environment(self):
        """Retrieve a list of environment variables defined in buildspec and
        return them as list with the shell equivalent command

        :return: list of environment variable lines to add to test script.
        :rtype: list
        """

        env = []
        pairs = self.recipe.get("env", [])
        shell = self.shell.name
        # Parse environment depending on expected shell
        if pairs:

            # bash, sh, zsh environment variable declaration is export KEY=VALUE
            if re.fullmatch("(bash|sh|zsh|/bin/bash|/bin/sh|/bin/zsh)$", shell):
                for k, v in pairs.items():
                    env.append("export %s=%s" % (k, v))

            # tcsh, csh,  environment variable declaration is setenv KEY VALUE
            elif re.fullmatch("(tcsh|csh|/bin/tcsh|/bin/csh)$", shell):
                for k, v in pairs.items():
                    env.append("setenv %s %s" % (k, v))

            else:
                self.logger.warning(
                    f"{shell} is not supported, skipping environment variables."
                )

        return env

    def get_variables(self):
        """Retrieve a list of  variables defined in buildspec and
        return them as list with the shell equivalent command.

        :return: list of variables variable lines to add to test script.
        :rtype: list
        """

        variables = []
        pairs = self.recipe.get("vars", [])
        shell = self.shell.name
        # Parse environment depending on expected shell
        if pairs:

            # bash, sh, zsh variable declaration is KEY=VALUE
            if re.fullmatch("(bash|sh|zsh|/bin/bash|/bin/sh|/bin/zsh)$", shell):
                for k, v in pairs.items():
                    variables.append("%s=%s" % (k, v))

            # tcsh, csh variable declaration is set KEY=VALUE
            elif re.fullmatch("(tcsh|csh|/bin/tcsh|/bin/csh)$", shell):
                for k, v in pairs.items():
                    variables.append("set %s=%s" % (k, v))

            else:
                self.logger.warning(
                    f"{shell} is not supported, skipping environment variables."
                )
        return variables

    def _generate_unique_id(self):
        """Generate a unique build id using ``uuid.uuid4()``."""

        unique_id = str(uuid.uuid4())
        return unique_id

    @abstractmethod
    def generate_script(self):
        """Build the testscript content implemented in each subclass"""

    def __str__(self):
        return "[builder-%s-%s]" % (self.type, self.name)

    def __repr__(self):
        return self.__str__()
