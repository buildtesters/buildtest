"""
BuilderBase class is an abstract class that defines common
functions for any types of builders. Each type schema (script, compiler)
is implemented as separate Builder.

ScriptBuilder class implements 'type: script'
CompilerBuilder class implements 'type: compiler'
"""

import datetime
import logging
import os
import re
import shutil
import stat
import sys

from buildtest.defaults import executor_root
from buildtest.schemas.defaults import schema_table
from buildtest.exceptions import BuildTestError
from buildtest.utils.file import create_dir, resolve_path, write_file
from buildtest.utils.shell import Shell


class BuilderBase:
    """The BuilderBase is an abstract class that implements common functions for
       any kind of builder.
    """

    def __init__(self, name, recipe, buildspec, testdir=None):
        """Initiate a builder base. A recipe configuration (loaded) is required.
           this can be handled easily with the BuildspecParser class:


           Parameters:

           :param name: a name for the Buildspec recipe
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
        self.buildspec = buildspec
        self.config_name = re.sub("[.](yml|yaml)", "", os.path.basename(buildspec))
        self.testdir = os.path.join(
            testdir, recipe.get("executor"), self.config_name, self.name
        )

        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"Processing Buildspec: {self.buildspec}")
        self.logger.debug(f"Processing Buildspec section: {self.name}")

        self.metadata["name"] = self.name
        self.metadata["buildspec"] = buildspec
        self.metadata["recipe"] = recipe

        # A builder is required to define the type attribute
        if not hasattr(self, "type"):
            sys.exit(
                "A builder base is required to define the 'type' as a class variable"
            )

        # The type must match the type of the builder
        self.recipe = recipe

        self.metadata["schemafile"] = os.path.basename(
            schema_table[self.recipe["type"]]["path"]
        )

        self.executor = self.recipe.get("executor")
        self.metadata["executor"] = self.executor
        # The default shell will be bash

        self.shell = Shell(self.recipe.get("shell", "bash"))

        # set shebang to value defined in Buildspec, if not defined then get one from Shell class
        self.shebang = self.recipe.get("shebang") or self.shell.shebang
        self.logger.debug("Using shell %s", self.shell.name)
        self.logger.debug(f"Shebang used for test: {self.shebang}")

    def __str__(self):
        return "[builder-%s-%s]" % (self.type, self.name)

    def __repr__(self):
        return self.__str__()

    def get_test_extension(self):
        """Return the test extension, which depends on the shell used. Based
           on the value of ``shell`` key we return the shell extension.

           shell: python --> py
           shell: bash --> sh (default)

           :return: returns test extension based on shell type
           :rtype: str
        """

        if "python" in self.shell.name:
            self.logger.debug("Setting test extension to 'py'")
            return "py"

        self.logger.debug("Setting test extension to 'sh'")
        return "sh"

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

            # Handles bash and sh
            if re.search("(bash|sh)$", shell):
                [env.append("export %s=%s" % (k, v)) for k, v in pairs.items()]

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

        env = []
        pairs = self.recipe.get("vars", [])
        shell = self.shell.name

        # Parse environment depending on expected shell
        if pairs:

            # Handles bash and sh
            if re.search("(bash|sh)$", shell):
                [env.append("%s=%s" % (k, v)) for k, v in pairs.items()]

            else:
                self.logger.warning(
                    f"{shell} is not supported, skipping environment variables."
                )

        return env

    def get_sbatch(self):

        lines = []
        sbatch = self.recipe.get("sbatch")

        if sbatch:

            for sbatch_cmd in sbatch:
                lines.append(f"#SBATCH {sbatch_cmd}")

            # if buildspec using slurm executor define job name, output and error file in job script
            if self.executor.startswith("slurm"):
                lines.append(f"#SBATCH -J {self.name}")
                lines.append(f"#SBATCH -o {self.name}-%j.out")
                lines.append(f"#SBATCH -e {self.name}-%j.err")

        return lines

    def get_bsub(self):

        lines = []
        bsub = self.recipe.get("bsub")

        if bsub:

            for bsub_cmd in bsub:
                lines.append(f"#BSUB {bsub_cmd}")

            if self.executor.startswith("lsf"):
                lines.append(f"#BSUB -J {self.name}")
                lines.append(f"#BSUB -o {self.name}-%J.out")
                lines.append(f"#BSUB -e {self.name}-%J.err")

        return lines

    def build(self):
        """ This method is responsible for invoking setup, creating test
            directory and writing test. This method is called from an instance
            object of this class that does ``builder.build()``.
        """

        self._build_setup()
        self._write_test()

    def _build_setup(self):
        """This method is the setup operation to get ready to build test which
           includes getting unique build id, setting up metadata object to store
           test details such as where test will be located and directory of test.
           This section cannot be reached without a valid, loaded recipe.
        """

        # Generate a unique id for the build based on key and unique string
        self.metadata["build_id"] = self._generate_build_id()

        # Derive the path to the test script
        self.metadata["generate_test"] = "%s.%s" % (
            os.path.join(self.testdir, "generate"),
            self.get_test_extension(),
        )
        self.metadata["generate_test"] = os.path.expandvars(
            self.metadata["generate_test"]
        )
        self.metadata["testroot"] = os.path.dirname(self.metadata["generate_test"])

        create_dir(self.metadata["testroot"])

    def _generate_build_id(self):
        """Generate a build id based on the Buildspec name, and datetime."""

        now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
        return "%s_%s" % (self.name, now)

    def _write_test(self):
        """This method is responsible for invoking ``generate_script`` that
           formulates content of testscript which is implemented in each subclass.
           Next we write content to file and apply 755 permission on script so
           it has executable permission.
        """

        # Implementation to write file generate.sh

        lines = self.generate_script()
        lines = "\n".join(lines)

        self.logger.info(
            f"Opening Test File for Writing: {self.metadata['generate_test']}"
        )

        write_file(self.metadata["generate_test"], lines)

        # Change permission of the file to executable
        os.chmod(
            self.metadata["generate_test"],
            stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH,
        )
        self.logger.debug(
            f"Applying permission 755 to {self.metadata['generate_test']} so that test can be executed"
        )

        # Implementation to write file run_script.sh

        run_script = os.path.join(self.testdir, "run.sh")

        content = [self.shebang]
        content.append("set -e")
        content.append(
            f"source {os.path.join(executor_root, self.executor, 'before_script.sh')}"
        )
        command = [
            self.shell.path,
            self.shell.opts,
            "./" + os.path.basename(self.metadata["generate_test"]),
        ]

        content.append(" ".join(command))
        content.append(
            f"source {os.path.join(executor_root, self.executor, 'after_script.sh')}"
        )

        content = "\n".join(content) + "\n"
        write_file(run_script, content)

        os.chmod(
            run_script,
            stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH,
        )
        self.metadata["testpath"] = run_script

    def generate_script(self):
        """Build the testscript content implemented in each subclass"""
        pass


class ScriptBuilder(BuilderBase):
    type = "script"

    def generate_script(self):
        """This method builds the testscript content based on the builder type. For ScriptBuilder we
           need to add the shebang, environment variables and the run section. Environment variables are
           declared first followed by run section

           :return: return content of test script
           :rtype: list
        """

        # start of each test should have the shebang
        lines = [self.shebang]

        if self.recipe.get("sbatch"):

            sbatch = self.get_sbatch()
            if sbatch:
                lines += sbatch
        elif self.recipe.get("bsub"):

            bsub = self.get_bsub()
            if bsub:
                lines += bsub

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
        return [module for module in modules]

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
        # return self.simple_run()

    def set_executable_name(self, name=None):
        """This method set the executable name. One may specify a custom name to executable via ``name``
           argument. Otherwise the executable is using the filename of ``self.sourcefile`` and adding ``.exe``
           extension at end.
        """

        if name:
            return name

        return "%s.exe" % os.path.basename(self.sourcefile)

    def setup(self):

        self.compiler_recipe = self.recipe.get("build")
        self.sourcefile = self.resolve_source(self.compiler_recipe["source"])

        self.cc = self.compiler_recipe.get("cc") or self.cc
        self.fc = self.compiler_recipe.get("fc") or self.fc
        self.cxx = self.compiler_recipe.get("cxx") or self.cxx
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
        lines = [self.shebang]

        # get sbatch commmands
        lines += self.get_sbatch()
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


class GNUCompiler(CompilerBuilder):

    cc = "gcc"
    cxx = "g++"
    fc = "gfortran"


class IntelCompiler(CompilerBuilder):

    cc = "icc"
    cxx = "icpc"
    fc = "ifort"


class PGICompiler(CompilerBuilder):

    cc = "pgcc"
    cxx = "pgc++"
    fc = "pgfortran"


class CrayCompiler(CompilerBuilder):

    cc = "cc"
    cxx = "CC"
    fc = "ftn"
