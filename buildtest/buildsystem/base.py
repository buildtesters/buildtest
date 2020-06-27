"""
BuildspecParser is intended to read in a Buildspec file with one or
more test blocks, and then generate builders based on the type
of each. The BuilderBase is the base class for all builders that
expose functions to run builds.
"""

import datetime
import logging
import os
import re
import shutil
import stat
import sys

from jsonschema import validate

from buildtest.buildsystem.schemas.utils import (
    load_schema,
    load_recipe,
    get_schemas_available,
    here,
)
from buildtest.exceptions import BuildTestError
from buildtest.utils.file import create_dir, is_dir, resolve_path, write_file
from buildtest.utils.shell import Shell


class BuildspecParser:
    """A BuildspecParser is a base class for loading and validating a Buildspec file.
       The type (e.g., script) and version are derived from reading in
       the file, and then matching to a Buildspec schema, each of which is
       developed at https://github.com/buildtesters/schemas and added to
       subfolders named accordingly under buildtest/buildsystem/schemas.
       The schema object can load in a general Buildspec file
       to validate it, and then match it to a Buildspec Schema available.
       If the version of a schema is not specified, we use the latest.
       If the schema fails validation check, then we stop immediately.
    """

    # Metadata keys are not considered build sections
    metadata = ["version", "maintainers"]

    def __init__(self, buildspec):
        """The init method will run some checks against buildspec before loading
           buildspec. We retrieve available schemas via method
           ``get_schemas_available`` and check if ``type`` in buildspec
           match available schema. We validate the entire buildspec with
           global.schema.json and validate each test section with the designated
           type schema. If there is any error during the init method, an
           exception will be raised.

           Parameters:

           :param buildspec: the pull path to the Buildspec file, must exist.
           :type buildspec: str, required
        """

        self.logger = logging.getLogger(__name__)

        # Read the lookup to get schemas available
        self.schema_table = get_schemas_available()

        self.logger.debug(
            f"buildtest found the available schema: {self.schema_table} in schema library"
        )

        # if invalid input for buildspec
        if not buildspec:
            sys.exit("Invalid input type for Buildspec, must be of type 'string'.")

        self.buildspec = resolve_path(buildspec)

        if not self.buildspec:
            sys.exit("Can't process input: %s " % buildspec)

        if is_dir(self.buildspec):
            sys.exit(
                f"Detected {self.buildspec} is a directory, please provide a file path (not a directory path) to BuildspecParser."
            )

        self.recipe = load_recipe(self.buildspec)

        # Buildspec must pass global validation (sets self.recipe)
        self._validate_global()

        # validate each schema defined in the recipes
        self._validate()

    def __str__(self):
        return "[buildspec-parser]"

    def __repr__(self):
        return "[buildspec-parser]"

    def _validate_global(self):
        """The global validation ensures that the overall structure of the
           file is sound for further parsing. We load in the global.schema.json
           for this purpose. The function also allows a custom Buildspec to
           extend the usage of the class.
        """

        global_schema_file = os.path.join(here, "global.schema.json")

        outer_schema = load_schema(global_schema_file)

        self.logger.debug(
            f"Validating {self.buildspec} with schema: {global_schema_file}"
        )

        validate(instance=self.recipe, schema=outer_schema)

        self.logger.debug("Validation was successful")

    # Validation

    def _validate(self):
        """Given a loaded recipe, validate that the type is known in the lookup
           to buildtest. If a version is provided, honor it. If not, use latest.
           We also don't allow repeated keys in the same file.
        """

        self.schema_version = self.recipe.get("version", "latest")

        for name in self.recipe["buildspecs"].keys():

            if name in self.metadata:
                continue

            # the buildspec section must be an dict where test is defined. If
            # it's not a dict then we should raise an error.
            if not isinstance(self.recipe["buildspecs"][name], dict):
                sys.exit(f"Section: {self.recipe[name]} must be a dictionary")

            # extract type field from test, if not found set to None
            type = self.recipe.get("buildspecs").get(name).get("type") or None

            # if type not found in section, raise an error since we every test
            # must be associated to a schema which is controlled by 'type' key
            if not type:
                sys.exit(f"Did not find 'type' key in test section: {name}")

            # Ensure we have a Buildspec recipe with a valid type
            if type not in self.schema_table.keys():
                sys.exit("type %s is not known to buildtest." % type)

            # And that there is a version file
            if self.schema_version not in self.schema_table[type]:
                sys.exit(
                    "version %s is not known for type %s. Try using latest."
                    % (self.schema_version, self.schema_table[type])
                )

            # Finally, validate the section against the schema
            self.schema_file = os.path.join(
                here, type, self.schema_table[type][self.schema_version]
            )

            validate(
                instance=self.recipe["buildspecs"][name],
                schema=load_schema(self.schema_file),
            )

    # Builders

    def get_builders(self, testdir):
        """Based on a loaded Buildspec file, return the correct builder
           for each based on the type. Each type is associated with a known
           Builder class.

           Parameters:

           :param testdir: Test Destination directory, specified by --testdir
           :type testdir: str, optional
        """

        builders = []
        if self.recipe:
            for name in self.keys():
                recipe = self.recipe["buildspecs"][name]
                # Add the builder based on the type
                if recipe["type"] == "script":
                    builders.append(
                        ScriptBuilder(
                            name,
                            recipe,
                            self.buildspec,
                            self.schema_version,
                            testdir=testdir,
                        )
                    )
                elif recipe["type"] == "compiler":
                    if recipe["compiler"].get("name") == "gnu":
                        builders.append(
                            GNUCompiler(
                                name,
                                recipe,
                                self.buildspec,
                                self.schema_version,
                                testdir=testdir,
                            )
                        )
                    elif recipe["compiler"].get("name") == "intel":
                        builders.append(
                            IntelCompiler(
                                name,
                                recipe,
                                self.buildspec,
                                self.schema_version,
                                testdir=testdir,
                            )
                        )
                    elif recipe["compiler"].get("name") == "pgi":
                        builders.append(
                            PGICompiler(
                                name,
                                recipe,
                                self.buildspec,
                                self.schema_version,
                                testdir=testdir,
                            )
                        )
                    elif recipe["compiler"].get("name") == "cray":
                        builders.append(
                            CrayCompiler(
                                name,
                                recipe,
                                self.buildspec,
                                self.schema_version,
                                testdir=testdir,
                            )
                        )
                    else:
                        continue

                else:
                    print(
                        "%s is not recognized by buildtest, skipping." % recipe["type"]
                    )
        return builders

    def keys(self):
        """Return the list of keys for the loaded Buildspec recipe, not including
           the metadata keys defined for any global recipe.
        """

        keys = []
        if self.recipe:
            keys = [x for x in self.recipe["buildspecs"].keys()]
        return keys

    def get(self, name):
        """Given the name of a section (typically a build configuration name)
           return the loaded section from self.recipe. If you need to parse
           through just section names, use self.keys() to filter out metadata.
        """

        return self.recipe.get(name)


class BuilderBase:
    """The BuilderBase is an abstract class that implements common functions for
       any kind of builder.
    """

    def __init__(self, name, recipe, buildspec, version, testdir=None):
        """Initiate a builder base. A recipe configuration (loaded) is required.
           this can be handled easily with the BuildspecParser class:


           Parameters:

           :param name: a name for the Buildspec recipe
           :type name: str, required
           :param recipe: the loaded section from the buildspec for the user.
           :type recipe: dict, required
           :param buildspec: the pull path to the Buildspec file, must exist.
           :type buildspec: str, required
           :param version: Version specified in buildspec
           :type version: str, required
           :param testdir: Test Destination directory where to write test
           :type testdir: str, optional
        """

        self.name = name
        self.pwd = os.getcwd()
        self.result = {}
        self.metadata = {}
        self.buildspec = buildspec
        self.config_name = re.sub("[.](yml|yaml)", "", os.path.basename(buildspec))
        self.testdir = os.path.join(testdir, self.config_name)

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

        # get the schema name that this buildspec was validated with
        self.schema_table = get_schemas_available()
        type = self.recipe["type"]
        self.schemafile = self.schema_table[type][version]
        self.metadata["schemafile"] = self.schemafile

        self.executor = self.recipe.get("executor")
        self.metadata["executor"] = self.executor
        # The default shell will be bash
        self.shell = Shell(self.recipe.get("shell", "bash"))

        # set shebang to value defined in Buildspec, if not defined then get one from Shell class
        self.shebang = self.recipe.get("shebang") or self.shell.shebang

        self.logger.debug("Shell Details: ")
        self.logger.debug(f"Shell Name: {self.shell.name}")
        self.logger.debug(f"Shell Opts: {self.shell.opts}")
        self.logger.debug(f"Shell Path: {self.shell.path}")
        self.logger.debug(f"Shell Shebang: {self.shell.shebang}")

        self.logger.debug(f"Shebang used for test: {self.shebang}")

    def __str__(self):
        return "[builder-%s-%s]" % (self.type, self.name)

    def __repr__(self):
        return self.__str__()

    def _create_test_folders(self):
        """Create all needed test folders on init, and add their paths
           to self.metadata.
        """

        create_dir(self.metadata["testroot"])
        for folder in ["run"]:
            name = "%sdir" % folder
            self.metadata[name] = os.path.join(self.metadata["testroot"], folder)
            create_dir(self.metadata[name])

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

        return lines

    def build(self):
        """ This method is responsible for invoking setup, creating test
            directory and writing test.

        :return:
        """
        self._build_setup()
        self._create_test_folders()
        self._write_test()

    def _build_setup(self):
        """This method is the setup operation to get ready to build test which
           includes getting unique build id, setting up metadata object to store
           test details such as where test will be located and directory of test.
           This section cannot be reached without a valid, loaded recipe.
        """

        # Generate a unique id for the build based on key and unique string
        self.metadata["build_id"] = self._generate_build_id()

        # History is returned at the end of a run
        self.history = {}
        self.history["TESTS"] = []

        # Metadata includes known sections in a Buildspec
        # These should all be validated for type, format, by the Buildspec schema
        # self.metadata = {}

        # Derive the path to the test script
        self.metadata["testpath"] = "%s.%s" % (
            os.path.join(self.testdir, self.name),
            self.get_test_extension(),
        )
        self.metadata["testpath"] = os.path.expandvars(self.metadata["testpath"])
        self.metadata["testroot"] = os.path.dirname(self.metadata["testpath"])

    def _generate_build_id(self):
        """Generate a build id based on the Buildspec name, and datetime."""

        now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
        return "%s_%s" % (self.name, now)

    def _write_test(self):
        """This method is responsible for invoking ``_build_testcontent`` that
           formulates content of testscript which is implemented in each subclass.
           Next we write content to file and apply 755 permission on script so
           it has executable permission.
        """

        lines = self._build_testcontent()
        lines = "\n".join(lines)

        self.logger.info(f"Opening Test File for Writing: {self.metadata['testpath']}")

        write_file(self.metadata["testpath"], lines)

        # Change permission of the file to executable
        os.chmod(
            self.metadata["testpath"],
            stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH,
        )
        self.logger.debug(
            f"Applying permission 755 to {self.metadata['testpath']} so that test can be executed"
        )

    def _build_testcontent(self):
        """Build the testscript content implemented in each subclass"""
        pass


class ScriptBuilder(BuilderBase):
    type = "script"
    known_sections = ["type", "run"]

    def _build_testcontent(self):
        """This method builds the testscript content based on the builder type. For ScriptBuilder we
           need to add the shebang, environment variables and the run section. Environment variables are
           declared first followed by run section

           :return: return content of test script
           :rtype: list
        """

        # start of each test should have the shebang
        lines = [self.shebang]

        sbatch = self.get_sbatch()
        if sbatch:
            lines += sbatch

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

    def simple_run(self, workdir=None):
        """This method executes the binary without any argument. This is the most simple run.
        The method returns a list with the executable. User may specify a working directory via
        ``workdir`` to indicate the path to binary relative to their working directory. By default
        the executable is in the same directory as workdir so we can access executable as
        ``./{self.executable}``. If workdir is defined, it is simply added in front of executable path.

        Parameters:

        :param workdir: relative path to binary from working directory, if not specified it's assumed executable
                        is in working directory.
        :type workdir: str, optional
        :return: A list containing path to executable
        :rtype: list
        """

        if workdir:
            return [os.path.join(workdir, self.executable)]

        return [f"./{self.executable}"]

    def run_with_args(self, args):

        run = []
        run += self.simple_run()
        run.append(args)
        return run

    def build_run_cmd(self, args):
        """This method builds the run command which refers to how to run the generated binary after compilation."""
        if args:
            return self.run_with_args(args)

        return self.simple_run()

    def set_executable_name(self, name=None):
        """This method set the executable name. One may specify a custom name to executable via ``name``
           argument. Otherwise the executable is using the filename of ``self.sourcefile`` and adding ``.exe``
           extension at end.
        """

        if name:
            return name

        return "%s.exe" % os.path.basename(self.sourcefile)

    def setup(self):

        self.compiler_recipe = self.recipe.get("compiler")
        self.sourcefile = self.resolve_source(self.compiler_recipe["source"])

        # set executable name and assign to self.executable
        self.executable = self.set_executable_name()
        self.lang = self.detect_lang(self.sourcefile)
        self.compile_cmd = self.generate_compile_cmd()

        self.run_cmd = self.build_run_cmd(self.compiler_recipe.get("exec_args"))

        self.cflags = self.compiler_recipe.get("cflags")
        self.fflags = self.compiler_recipe.get("fflags")
        self.cxxflags = self.compiler_recipe.get("cxxflags")
        self.ldflags = self.compiler_recipe.get("ldflags")
        self.cppflags = self.compiler_recipe.get("cppflags")

    def _build_testcontent(self):
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

        # add compile command
        lines.append(" ".join(self.compile_cmd))
        # add run command
        lines.append(" ".join(self.run_cmd))

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
