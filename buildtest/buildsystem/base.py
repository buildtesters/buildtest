"""
BuildConfig: loader and manager for build configurations, and schema validation
Copyright (C) 2020 Vanessa Sochat. 

BuildConfig is intended to read in a configuration file with one or 
more buildtest setups defined, and then generate builders based on the type 
of each. The BuilderBase is the base class for all builders that 
expose functions to run builds.
"""

import datetime
import os
import re
import shutil
import stat
import sys

from copy import deepcopy
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from buildtest.log import init_logfile, init_log
from buildtest.defaults import (
    BUILDTEST_SHELL,
    build_sections,
    variable_sections,
)
from buildtest.utils.file import create_dir
from buildtest.utils.command import BuildTestCommand
from buildtest.buildsystem.schemas.utils import (
    load_schema,
    load_recipe,
    get_schemas_available,
    here,
)

known_sections = variable_sections + build_sections


class BuildConfig:
    """A BuildConfig is a base class for a build configuration.
       The type (e.g., script) and version are derived from reading in
       the file, and then matching to a buildtest schema, each of which is
       developed at https://github.com/HPC-buildtest/schemas and added to
       subfolders named accordingly under buildtest/buildsystem/schemas.
       The schema object can load in a general test configuration file
       to validate it, and then match it to a schema available.
       If the version of a schema is not specified, we use the latest.
       If the schema fails validation check, then we stop immediately.
    """

    # Metadata keys are not considered build sections
    metadata = ["version"]

    def __init__(self, config_file):
        """initiate a build configuration file, meaning that we read in the
           file, match it to a schema provided by buildtest, and validate it.

           Parameters:

           config_file: the pull path to the configuration file, must exist.
        """
        self.recipe = None

        # Read the lookup to get schemas available
        self.lookup = get_schemas_available()

        # Load the configuration file, fails on any error
        self.load(config_file)

    def load(self, config_file):
        """Load a config file. We check that it exists, and that it is valid.
           we exit on any error, as the config is not loadable.

           Parameters:

           config_file: the pull path to the configuration file, must exist.
        """
        self.config_file = os.path.abspath(config_file)

        if not os.path.exists(self.config_file):
            sys.exit("Build configuration %s does not exist." % self.config_file)

        elif os.path.isdir(self.config_file):
            sys.exit(
                "Please provide a file path (not a directory path) to a build recipe."
            )

        # all test configs must pass global validation (sets self.recipe)
        self._validate_global()

        # validate each schema defined in the recipes
        self._validate()

    def __str__(self):
        return "[buildtest-build-config]"

    def __repr__(self):
        return "[buildtest-build-config]"

    # Validation

    def _validate(self):
        """Given a loaded recipe, validate that the type is known in the lookup
           to buildtest. If a version is provided, honor it. If not, use latest.
           We also don't allow repeated keys in the same file.
        """

        version = self.recipe.get("version", "latest")
        seen = set()
        for name, section in self.recipe.items():

            if name == "version":
                continue

            # Check for repeated keys
            elif name in seen:
                sys.exit("Invalid recipe: %s is repeated more than once." % name)
            seen.add(name)

            # Ensure we have a recipe for it
            if section["type"] not in self.lookup.keys():
                sys.exit("type %s is not known to buildtest." % section["type"])

            # And that there is a version file
            if version not in self.lookup[section["type"]]:
                sys.exit(
                    "version %s is not known for type %s. Try using latest." % version,
                    section["type"],
                )

            # Finally, validate the section against the schema
            schema_file = os.path.join(
                here, section["type"], self.lookup[section["type"]][version]
            )
            validate(instance=section, schema=load_schema(schema_file))

    def _validate_global(self, config_file=None):
        """The global validation ensures that the overall structure of the
           file is sound for further parsing. We load in the outer.schema.json
           for this purpose. The function also allows a custom config to be 
           to extend the usage of the class.
        """

        config_file = config_file or self.config_file
        outer_schema = load_schema(os.path.join(here, "outer.schema.json"))
        self.recipe = load_recipe(config_file)
        try:
            validate(instance=self.recipe, schema=outer_schema)
        except ValidationError:
            sys.exit(
                "Test configuration %s does not pass validation of the outer schema."
                % config_file
            )

    # Builders

    def get_builders(self, testdir=None):
        """Based on a loaded configuration file, return the correct builder
           for each based on the type. Each type is associated with a known 
           Builder class.
        """

        builders = []
        if self.recipe:
            for name in self.keys():
                recipe_config = self.recipe[name]

                # Add the builder based on the type
                if recipe_config["type"] == "script":
                    builders.append(
                        ScriptBuilder(
                            name, recipe_config, self.config_file, testdir=testdir
                        )
                    )
                else:
                    print(
                        "%s is not recognized by buildtest, skipping."
                        % recipe_config["type"]
                    )

        return builders

    def keys(self):
        """Return the list of keys for the loaded recipe, not including
           the metadata keys defined for any global recipe.
        """

        keys = []
        if self.recipe:
            keys = [x for x in self.recipe.keys() if x not in self.metadata]
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

    def __init__(self, name, recipe_config, config_file=None, testdir=None):
        """initiate a builder base. A recipe configuration (loaded) is required.
           this can be handled easily with the BuildConfig class:

           bc = BuildConfig(config_file)
           recipe_config = bc.get("section_name")
           builder = ScriptBuilder(recipe_config)

           Parameters:

           name: a name for the build recipe (required)
           recipe_config: the loaded section from the config_file for the user.
           config_file: the pull path to the configuration file, must exist.
        """

        self.name = name
        self.pwd = os.getcwd()
        self.result = {}
        self.build_id = None
        self.metadata = {}
        self.config_file = config_file
        self.config_name = re.sub("[.](yml|yaml)", "", os.path.basename(config_file))
        self.testdir = testdir or os.path.join(
            os.getcwd(), ".buildtest", self.config_name
        )

        # A builder is required to define the type attribute
        if not hasattr(self, "type"):
            sys.exit(
                "A builder base is required to define the 'type' as a class variable"
            )

        # The recipe must be loaded as a dictionary
        if not isinstance(recipe_config, dict):
            sys.exit(
                "Please load a recipe configuration before providing to the builder."
            )

        # The type must match the type of the builder
        self.recipe = recipe_config
        if self.recipe.get("type") != self.type:
            sys.exit(
                "Mismatch in type. Builder expects %s but found %s."
                % (self.type, self.recipe.get("type"))
            )

    def __str__(self):
        return "[builder-%s-%s]" % (self.type, self.name)

    def __repr__(self):
        return self.__str__()

    def _get_testdir(self):
        """Based on the testfile path, return the testing directory.

           Returns: full path to testing directory
        """
        testpath = os.path.expandvars(self.metadata["testpath"])
        return os.path.dirname(testpath)

    def _create_test_folders(self):
        """Create all needed test folders on init, and add their paths
           to self.metadata.
        """
        testdir = self._get_testdir()
        create_dir(testdir)
        for folder in ["run", "log"]:
            name = "%sdir" % folder
            self.metadata[name] = os.path.join(testdir, folder)
            create_dir(self.metadata[name])

    def _init_logger(self, to_file=True):
        """Initialize the logger. This is called at the end of prepare_run,
           so the testpath is defined with the build id.
        """

        if to_file:
            self.metadata["logfile"] = os.path.join(
                self.metadata["logdir"], "%s.log" % self.build_id
            )
            self.logger = init_logfile(self.metadata["logfile"])
        else:
            self.logger = init_log()

    def get_test_extension(self):
        """Return the test extension, which depends on the shell used. Based
           on the value of ``shell`` key we return the shell extension.

           shell: python --> py
           shell: bash --> sh (default)
        """

        shell = self.get_shell()
        if "python" in shell:
            return "py"

        return "sh"

    def get_environment(self):
        """Take the environment section, return a list of lines to add
           to the start of the testscript. Return lines that define
           variables specific to the shell.

           Returns: list of lines to add to beginning of test script.
        """
        env = []
        pairs = self.recipe.get("env")
        shell = self.get_shell()

        # If we are using a python shell, we need to import os first
        if "python" in shell:
            env.append("import os")

        # Parse environment depending on expected shell
        if pairs:

            # Handles bash and sh
            if re.search("(bash|sh)$", shell):
                [env.append("%s=%s" % (k, v)) for k, v in pairs.items()]

            # python interpreter can be a shell
            elif "python" in shell:
                [env.append("os.putenv('%s','%s')" % (k, v)) for k, v in pairs.items()]

            else:
                self.logger.warning(
                    f"{shell} is not supported, skipping environment variables."
                )

        return env

    def get_shell(self):
        """Return the shell defined in the recipe, or default to bash."""

        return self.recipe.get("shell", BUILDTEST_SHELL)

    def run_wrapper(func):
        """The run wrapper will execute any prepare_run and finish_run 
           sections around some main run function (run or dry_run).
           A return the result. The show_prepare function
           log updates to the terminal for the user. The function sets
           self.result and also returns it to the calling function.
        """

        def wrapper(self):
            self.prepare_run()
            self.show_prepare()
            self.result = func(self)
            self.finish_run()
            return self.result

        return wrapper

    def finish_run(self):
        """Finish up the run (not sure what might go here yet, other than
           honoring a custom subclass function.
        """

        # If the subclass has a _finish_run function, honor it
        if hasattr(self, "_finish_run"):
            self._finish_run()

    def prepare_run(self, testdir=None):
        """Prepare run provides shared functions to set up metadata and
           class data structures that are used by both run and dry_run
           This section cannot be reached without a valid, loaded recipe.
        """

        # Generate a unique id for the build based on key and unique string
        self.build_id = self._generate_build_id()

        # History is returned at the end of a run
        self.history = {}
        self.history["TESTS"] = []

        # Metadata includes known sections in a config recipe (pre/post_run, env)
        # These should all be validated for type, format, by the schema validator
        self.metadata = {}
        for known_section in known_sections:
            if known_section in self.recipe:
                self.metadata[known_section] = self.recipe.get(known_section)

        # Every build recipe has a shell (defaults to BUILDTEST_SHELL_DEFAULT
        self.metadata["shell"] = self.get_shell()

        # Derive the path to the test script
        self.metadata["testpath"] = "%s.%s" % (
            os.path.join(self.testdir, self.name),
            self.get_test_extension(),
        )
        self.metadata["testdir"] = os.path.dirname(self.metadata["testpath"])

        # The start time to print for the user
        self.metadata["start_time"] = datetime.datetime.now()

        # If the subclass has a _prepare_run class, honor it
        if hasattr(self, "_prepare_run"):
            self._prepare_run()

        # pre_build, build, post_build, pre_run, run, post_run, env and shell
        # are already both added to metadata

    @run_wrapper
    def run(self):
        """Run the builder associated with the loaded recipe.
           This parent class handles shared starting functions for each step
           and then calls the subclass function (_run) if it exists.

           Parameters:
           testdir: the directory to write tests to. Defaults to os.getcwd()
        """

        # Create test directory and run folder they don't exist
        self._create_test_folders()
        self._init_logger()
        testfile = self._write_test()
        result = self.run_tests(testfile)
        return result

    def run_tests(self, testfile):
        """The shared _run function will run a test file, which must be
           provided. This is called by run() after generation of the
           test file, and it return a result object (dict).
        """

        # Keep a result object
        result = {}
        result["START_TIME"] = self.get_formatted_time("start_time")
        result["LOGFILE"] = self.metadata.get("logfile", "")
        result["BUILD_ID"] = self.build_id

        # Change to the test directory
        os.chdir(self._get_testdir())

        # Run the test file using the shell
        cmd = [self.get_shell(), testfile]
        command = BuildTestCommand(cmd)
        out, err = command.execute()

        # Record the ending time
        self.metadata["end_time"] = datetime.datetime.now()

        # Keep an output file
        run_output_file = os.path.join(
            self.metadata.get("rundir"), "%s.out" % self.build_id
        )

        # Run the test file, print output to file
        with open(run_output_file, "w") as fd:

            fd.write("Test Name:" + self.build_id + "\n")
            fd.write("Return Code: %s \n" % command.returncode)

            if out:
                fd.write("---------- START OF TEST OUTPUT ---------------- \n")
                fd.write("\n".join(out))
                fd.write("------------ END OF TEST OUTPUT ---------------- \n")
            if err:
                fd.write("---------- START OF TEST ERROR ---------------- \n")
                fd.write("\n".join(err))
                fd.write("------------ END OF TEST ERROR ---------------- \n")

        result["RETURN_CODE"] = command.returncode
        result["END_TIME"] = self.get_formatted_time("end_time")

        # Print the test result for the user
        if command.returncode == 0:
            print("{:<40} {}".format("[RUNNING TEST]", "PASSED"))
        else:
            print("{:<40} {}".format("[RUNNING TEST]", "FAILED"))

        print("Writing results to " + run_output_file)

        # Return to starting directory for next test
        os.chdir(self.pwd)
        return result

    def get_formatted_time(self, key, fmt="%m/%d/%Y %X"):
        """Given some timestamp key in self.metadata, return a pretty printed
           version of it. This is intended to log in the console for the user.

           Parameters:

           key: The key to look up in the metadata
           fmt: the format string to use
        """
        timestamp = self.metadata.get(key, "")
        if timestamp:
            timestamp = timestamp.strftime(fmt)
        return timestamp

    def show_prepare(self):
        """Print basic run information to the user, if defined, before the run."""

        start_time = self.get_formatted_time("start_time")

        print("{:_<80}".format(""))
        print("{:>40} {}".format("start time:", self.metadata.get("start_time")))

        if self.config_file:
            print("{:>40} {}".format("configuration file:", self.config_file))
        print("{:>40} {}".format("testdir:", self.metadata.get("testdir")))
        print("{:>40} {}".format("testpath:", self.metadata.get("testpath")))
        print("{:>40} {}".format("logpath:", self.metadata.get("logfile")))
        print("{:_<80}".format(""))

        print("\n\n")
        print("{:<40} {}".format("STAGE", "VALUE"))
        print("{:_<80}".format(""))

    @run_wrapper
    def dry_run(self):
        """Akin to a build preview, we prepare and finish a run, but only
           print the script to the screen without writing or running files.
        """

        # Dry run just prints the testing script
        self._init_logger(to_file=False)
        lines = self._get_test_lines()
        print("\n".join(lines))

    def _generate_build_id(self):
        """Generate a build id based on the recipe name, and datetime."""

        now = datetime.datetime.now().strftime("%m-%d-%Y-%H-%M")
        return "%s_%s" % (self.name, now)

    def _write_test(self, lines=None):
        """Given test metadata, write test content."""

        # If no lines provided, generate
        if not lines:
            lines = self._get_test_lines()

        # '$HOME/.buildtest/testdir/<name>/<name>_<timestamp>.sh'
        # This will put output (latest run) in same directory - do we want this?
        testpath = os.path.expandvars(self.metadata["testpath"])
        testdir = os.path.dirname(testpath)

        self.logger.info(f"Opening Test File for Writing: {testpath}")

        # Open the test file and write contents
        with open(testpath, "w") as fd:
            fd.write("\n".join(lines))

        # Change permission of the file to executable
        os.chmod(
            testpath,
            stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH,
        )
        print("{:<40} {}".format("[WRITING TEST]", "PASSED"))
        return testpath

    def _get_test_lines(self):
        """Given test metadata, get test lines to write to file or show."""

        lines = []
        shell = shutil.which(self.get_shell())

        if not shell:
            shell = BUILDTEST_SHELL

        lines += [f"#!{shell}"]

        # Add environment variables
        lines += self.get_environment()

        # Add lines from each build section
        for section in build_sections:
            if section in self.metadata:
                lines += [self.metadata.get(section)] or []

        return lines


class ScriptBuilder(BuilderBase):
    type = "script"
