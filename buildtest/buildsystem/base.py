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
from buildtest.exceptions import BuildTestError
from buildtest.utils.file import create_dir, resolve_path, write_file
from buildtest.utils.timer import Timer
from buildtest.utils.shell import Shell


class BuilderBase(ABC):
    """The BuilderBase is an abstract class that implements common functions for
       any kind of builder.
    """

    def __init__(self, name, recipe, buildspec, testdir=None):
        """The BuilderBase provides common functions for any builder. The builder
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

        self.metadata["name"] = self.name
        self.metadata["buildspec"] = buildspec
        self.metadata["recipe"] = recipe
        self.metadata["tags"] = recipe.get("tags")
        self.metadata["result"] = {}

        # A builder is required to define the type attribute
        if not hasattr(self, "type"):
            sys.exit(
                "A builder base is required to define the 'type' as a class variable"
            )

        # The type must match the type of the builder
        self.recipe = recipe

        self.metadata["schemafile"] = os.path.basename(
            schema_table[f"{self.recipe['type']}-v1.0.schema.json"]["path"]
        )

        self.executor = self.recipe.get("executor")
        self.executor_type = self.detect_executor()
        self.metadata["executor"] = self.executor
        # The default shell will be bash

        self.default_shell = Shell()

        self.shell = Shell(self.recipe.get("shell", "bash"))

        # set shebang to value defined in Buildspec, if not defined then get one from Shell class
        self.shebang = (
            self.recipe.get("shebang") or f"{self.shell.shebang} {self.shell.opts}"
        )
        self.logger.debug("Using shell %s", self.shell.name)
        self.logger.debug(f"Shebang used for test: {self.shebang}")

    def detect_executor(self):
        """Return executor type based on executor property. The executor is in
           format <type>.<name> so we check for keywords that start with known executor
           types ``local``, ``slurm``, ``lsf``, ``cobalt``
        """
        executor_types = ["local", "slurm", "lsf", "cobalt"]
        for name in executor_types:
            if self.executor.startswith(name):
                return name

    def get_test_extension(self):
        """Return the test extension, which depends on the shell used. Based
           on the value of ``shell`` key we return the shell extension.

           shell: bash --> sh (default)

           :return: returns test extension based on shell type
           :rtype: str
        """

        self.logger.debug("Setting test extension to 'sh'")
        return "sh"

    def start(self):
        """Keep internal time for start of test. We start timer by calling Timer class"""

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
        """This method is the setup operation to get ready to build test which
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
        """Get Scheduler Directives for LSF, Slurm or Cobalt if we are processing
           test with one of the executor types. This method will return a list
           of string containing scheduler directives generally found at top of script.
           If test is local executor we return an empty list """

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
            # lines += [f"#COBALT --output {self.name}.out"]
            # lines += [f"#COBALT --error {self.name}.err"]

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
        """Set permission 755 on executable"""

        # Change permission of the file to executable
        os.chmod(
            self.metadata["testpath"],
            stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH,
        )
        self.logger.debug(
            f"Applying permission 755 to {self.metadata['testpath']} so that test can be executed"
        )

    def _write_test(self):
        """This method is responsible for invoking ``generate_script`` that
           formulates content of testscript which is implemented in each subclass.
           Next we write content to file and apply 755 permission on script so
           it has executable permission.
        """

        # Implementation to write file generate.sh
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
        if self.shell.name == "python":
            python_content = self.generate_script()
            python_content = "\n".join(python_content)
            script_path = "%s.py" % os.path.join(self.stage_dir, self.name)
            write_file(script_path, python_content)
            shutil.copy2(
                script_path, os.path.join(self.run_dir, os.path.basename(script_path))
            )
            lines += [f"python {script_path}"]
        else:
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


class ScriptBuilder(BuilderBase):
    type = "script"

    def generate_script(self):
        """This method builds the testscript content based on the builder type. For ScriptBuilder we
           need to add the shebang, environment variables and the run section. Environment variables are
           declared first followed by run section

           :return: return content of test script
           :rtype: list
        """

        lines = []
        # Add environment variables
        lines += self.get_environment()

        # Add variables
        lines += self.get_variables()

        # Add run section
        lines += [self.recipe.get("run")]

        return lines


class CompilerBuilder(BuilderBase):
    type = "compiler"

    # Fortran Extensions Links:
    # https://software.intel.com/content/www/us/en/develop/documentation/fortran-compiler-developer-guide-and-reference/top/compiler-setup/using-the-command-line/understanding-file-extensions.html
    # Fortran Extensions: http://fortranwiki.org/fortran/show/File+extensions
    lang_ext_table = {
        ".c": "C",
        ".cc": "C++",
        ".cxx": "C++",
        ".cpp": "C++",
        ".c++": "C++",
        ".f90": "Fortran",
        ".F90": "Fortran",
        ".f95": "Fortran",
        ".f03": "Fortran",
        ".f": "Fortran",
        ".F": "Fortran",
        ".FOR": "Fortran",
        ".for": "Fortran",
        ".FTN": "Fortran",
        ".ftn": "Fortran",
    }

    cc = None
    cxx = None
    fc = None
    ldflags = None
    cflags = None
    cxxflags = None
    fflags = None
    cppflags = None
    executable = None

    def set_cc(self, cc):
        self.cc = cc

    def set_cxx(self, cxx):
        self.cxx = cxx

    def set_fc(self, fc):
        self.fc = fc

    def set_cflags(self, cflags):
        self.cflags = cflags

    def set_fflags(self, fflags):
        self.fflags = fflags

    def set_cxxflags(self, cxxflags):
        self.cxxflags = cxxflags

    def set_cppflags(self, cppflags):
        self.cppflags = cppflags

    def set_ldflags(self, ldflags):
        self.ldflags = ldflags

    def get_cc(self):
        return self.cc

    def get_cxx(self):
        return self.cxx

    def get_fc(self):
        return self.fc

    def get_cflags(self):
        return self.cflags

    def get_cxxflags(self):
        return self.cxxflags

    def get_fflags(self):
        return self.fflags

    def get_cppfilags(self):
        return self.cppflags

    def get_ldflags(self):
        return self.ldflags

    def get_path(self):
        """This method returns the full path for GNU Compilers: ``gcc``, ``g++``, ``gfortran``"""
        path = {
            self.cc: shutil.which(self.cc),
            self.cxx: shutil.which(self.cxx),
            self.fc: shutil.which(self.fc),
        }
        return path

    def resolve_source(self, source):
        """This method resolves full path to source file, it checks for absolute path first before checking relative
           path that is relative to Buildspec recipe.
        """

        source_relpath = resolve_path(source) or resolve_path(
            os.path.join(
                os.path.dirname(self.buildspec), self.compiler_recipe["source"]
            )
        )
        # raise error if we can't find source file to compile
        if not source_relpath:
            sys.exit(
                f"Failed to resolve path specified by key 'source': {self.compiler_recipe['source']}"
            )

        return source_relpath

    def get_modules(self, modules):
        """Return a list of modules as a list"""
        assert isinstance(modules, dict)
        module_cmd = []
        # if purge is True and defined add module purge
        if modules.get("purge"):
            module_cmd += ["module purge"]
        #
        if modules.get("load"):
            for name in modules.get("load"):
                module_cmd += [f"module load {name}"]

        if modules.get("swap"):
            module_cmd += ["module swap " + " ".join(modules.get("swap"))]
        return module_cmd

    def build_run_cmd(self):
        """This method builds the run command which refers to how to run the generated binary after compilation."""
        self.run_dict = self.recipe.get("run")

        run = []

        if self.run_dict:
            # add launcher in front of execution if defined
            run.append(self.run_dict.get("launcher"))

        run.append(f"./{self.executable}")

        if self.run_dict:
            # add args after executable if defined
            run.append(self.run_dict.get("args"))

        # remove None object if found in list this would be present if launcher and args key are not defined
        run = [cmd for cmd in run if cmd]

        return run

    def set_executable_name(self, name=None):
        """This method set the executable name. One may specify a custom name to executable via ``name``
           argument. Otherwise the executable is using the filename of ``self.sourcefile`` and adding ``.exe``
           extension at end.
        """

        if name:
            return name

        return "%s.exe" % os.path.basename(self.sourcefile)

    def lookup_compilers(self, compiler):
        """ Return compiler wrapper based on compiler name

        :param compiler: name of compiler
        :return: return a dictionary that has list of compiler wrappers for C, C++, and Fortran
        """

        self.compiler_lookup = {
            "gnu": {"cc": "gcc", "cxx": "g++", "fc": "gfortran"},
            "intel": {"cc": "icc", "cxx": "icpc", "fc": "ifort"},
            "pgi": {"cc": "pgcc", "cxx": "pgc++", "fc": "pgfortran"},
            "cray": {"cc": "cc", "cxx": "CC", "fc": "ftn"},
            "clang": {"cc": "clang", "cxx": "clang++", "fc": None},
            "cuda": {"cc": "nvcc", "cxx": "nvcc", "fc": None},
        }
        return self.compiler_lookup.get(compiler)

    def setup(self):

        self.compiler_recipe = self.recipe.get("build")
        self.sourcefile = self.compiler_recipe["source"]

        detected_compilers = self.lookup_compilers(self.compiler_recipe.get("name"))
        self.cc = self.compiler_recipe.get("cc") or detected_compilers["cc"]
        self.cxx = self.compiler_recipe.get("cxx") or detected_compilers["cxx"]
        self.fc = self.compiler_recipe.get("fc") or detected_compilers["fc"]

        self.cflags = self.compiler_recipe.get("cflags")
        self.fflags = self.compiler_recipe.get("fflags")
        self.cxxflags = self.compiler_recipe.get("cxxflags")
        self.ldflags = self.compiler_recipe.get("ldflags")
        self.cppflags = self.compiler_recipe.get("cppflags")
        self.pre_build = self.recipe.get("pre_build")
        self.post_build = self.recipe.get("post_build")
        self.pre_run = self.recipe.get("pre_run")
        self.post_run = self.recipe.get("post_run")

        # set executable name and assign to self.executable
        self.executable = self.set_executable_name()
        self.lang = self.detect_lang(self.sourcefile)
        self.compile_cmd = self.generate_compile_cmd()

        self.run_cmd = self.build_run_cmd()

    def generate_script(self):
        """This method will build the test content from a Buildspec that uses compiler schema. We need a 'compiler'
           and 'source' key which specifies the source files to compile. We resolve the source file path which can
           be an absolute value or relative path with respect to Buildspec. The file extension of sourcefile is used
           to detect the Programming Language which is used to lookup the compiler wrapper based on Language + Compiler.
           During compiler detection, we set class variables ``self.cc``, ``self.cxx``. ``self.fc``, ``self.cflags``,
           ``self.cxxflags``, ``self.fflags``, ``self.cppflags``. ``self.ldflags``. Finally we generate the compile
           command and add each instruction to ``lines`` which contains content of test. Upon completion, we return
           a list that contains content of the test.
        """

        self.setup()

        # every test starts with shebang line
        # lines = [self.shebang]
        lines = []

        # get environment variables
        lines += self.get_environment()
        # get variables
        lines += self.get_variables()

        # if 'module' defined in Buildspec add modules to test
        if self.recipe.get("module"):
            lines += self.get_modules(self.recipe.get("module"))

        if self.pre_build:
            lines.append(self.pre_build)
        # add compile command
        lines.append(" ".join(self.compile_cmd))

        if self.post_build:
            lines.append(self.post_build)

        if self.pre_run:
            lines.append(self.pre_run)
        # add run command
        lines.append(" ".join(self.run_cmd))

        if self.post_run:
            lines.append(self.post_run)

        return lines

    def detect_lang(self, sourcefile):
        """This method will return the Programming Language based by looking up  file extension of source file."""

        ext = os.path.splitext(sourcefile)[1]

        # if ext not in self.lang_ext_table then raise an error. This table consist of all file extensions that map to a Programming Language
        if ext not in self.lang_ext_table:
            raise BuildTestError(
                f"Unable to detect Program Language based on extension: {ext} in file {sourcefile}"
            )
        # Set Programming Language based on ext. Programming Language could be (C, C++, Fortran)
        lang = self.lang_ext_table[ext]
        return lang

    def generate_compile_cmd(self):
        """This method generates the compilation line and returns the output as a list. The compilation line depends
           on the the language detected that is stored in variable ``self.lang``.
        """

        cmd = []
        # Generate C compilation line
        if self.lang == "C":
            cmd = [
                self.cc,
                self.cppflags,
                self.cflags,
                "-o",
                self.executable,
                self.sourcefile,
                self.ldflags,
            ]

        # Generate C++ compilation line
        elif self.lang == "C++":
            cmd = [
                self.cxx,
                self.cppflags,
                self.cxxflags,
                "-o",
                self.executable,
                self.sourcefile,
                self.ldflags,
            ]

        # Generate Fortran compilation line
        elif self.lang == "Fortran":
            cmd = [
                self.fc,
                self.cppflags,
                self.fflags,
                "-o",
                self.executable,
                self.sourcefile,
                self.ldflags,
            ]
        # remove any None from list
        return list(filter(None, cmd))
