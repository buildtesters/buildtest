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
from buildtest.defaults import (
    BUILDTEST_SHELL,
    build_sections,
    variable_sections,
)
from buildtest.exceptions import BuildTestError
from buildtest.utils.command import BuildTestCommand
from buildtest.utils.file import create_dir, is_dir, resolve_path, read_file, write_file
from buildtest.utils.shell import Shell

known_sections = variable_sections + build_sections


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
    metadata = ["version"]

    def __init__(self, buildspec):
        """initiate a build configuration file, meaning that we read in the
           file, match it to a schema provided by buildtest, and validate it.

           Parameters:

           :param buildspec: the pull path to the Buildspec file, must exist.
           :type buildspec: str, required
        """

        self.logger = logging.getLogger(__name__)

        self.recipe = None

        # Read the lookup to get schemas available
        self.lookup = get_schemas_available()

        self.logger.debug(
            f"buildtest found the available schema: {self.lookup} in schema library"
        )

        # Load the Buildspec file, fails on any error
        self.load(buildspec)

    def load(self, buildspec):
        """Load a Buildspec file. We check that it exists, and that it is valid.
           we exit on any error, as the config is not loadable.

           Parameters:

           :param buildspec: the pull path to the configuration file, must exist.
           :type buildspec: str, required
        """

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

        # Buildspec must pass global validation (sets self.recipe)
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
                sys.exit(
                    "Invalid Buildspec recipe: %s is repeated more than once." % name
                )
            seen.add(name)

            # Ensure we have a Buildspec recipe with a valid type
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

    def _validate_global(self, buildspec=None):
        """The global validation ensures that the overall structure of the
           file is sound for further parsing. We load in the global.schema.json
           for this purpose. The function also allows a custom Buildspec to
           extend the usage of the class.
        """

        buildspec = buildspec or self.buildspec
        global_schema_file = os.path.join(here, "global.schema.json")

        outer_schema = load_schema(global_schema_file)
        self.recipe = load_recipe(buildspec)

        self.logger.debug(f"Validating {buildspec} with schema: {global_schema_file}")
        validate(instance=self.recipe, schema=outer_schema)
        self.logger.debug("Validation was successful")

    # Builders

    def get_builders(self, testdir=None):
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
                recipe = self.recipe[name]

                # Add the builder based on the type
                if recipe["type"] == "script":
                    builders.append(
                        ScriptBuilder(name, recipe, self.buildspec, testdir=testdir)
                    )
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

    def __init__(self, name, recipe, buildspec=None, testdir=None):
        """Initiate a builder base. A recipe configuration (loaded) is required.
           this can be handled easily with the BuildspecParser class:

           bp = BuildspecParser(buildspec)
           recipe = bp.get("section_name")
           builder = ScriptBuilder(recipe)

           Parameters:

           :param name: a name for the Buildspec recipe
           :type name: str, required
           :param recipe: the loaded section from the buildspec for the user.
           :type recipe: dict, required
           :param buildspec: the pull path to the Buildspec file, must exist.
           :type buildspec: str, optional
           :param testdir: Test Destination directory where to write test
           :type testdir: str, optional
        """

        self.name = name
        self.pwd = os.getcwd()
        self.result = {}
        self.build_id = None
        self.metadata = {}
        self.buildspec = buildspec
        self.config_name = re.sub("[.](yml|yaml)", "", os.path.basename(buildspec))
        self.testdir = testdir or os.path.join(
            os.getcwd(), ".buildtest", self.config_name
        )
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f"Processing Buildspec: {self.buildspec}")
        self.logger.debug(f"Processing Buildspec section: {self.name}")
        # A builder is required to define the type attribute
        if not hasattr(self, "type"):
            sys.exit(
                "A builder base is required to define the 'type' as a class variable"
            )

        # The recipe must be loaded as a dictionary
        if not isinstance(recipe, dict):
            sys.exit("Please load a Buildspec recipe before providing to the builder.")

        # The type must match the type of the builder
        self.recipe = recipe
        if self.recipe.get("type") != self.type:
            sys.exit(
                "Mismatch in type. Builder expects %s but found %s."
                % (self.type, self.recipe.get("type"))
            )
        # The default shell will be bash
        shell = Shell()
        # if 'shell' key  is defined in Buildspec let's override the default shell
        if self.recipe.get("shell"):
            shell = Shell(self.recipe.get("shell"))

        self.shell = shell.get()

        # set shebang to value defined in Buildspec, if not defined then get one from Shell class
        self.shebang = self.recipe.get("shebang") or self.shell["shebang"]

        self.logger.debug(f"Shell Details: {self.shell}")
        self.logger.debug(f"Shebang: {self.shebang}")

    def __str__(self):
        return "[builder-%s-%s]" % (self.type, self.name)

    def __repr__(self):
        return self.__str__()

    def _get_testdir(self):
        """Based on the testfile path, return the testing directory.

           Returns: full path to testing directory
        """
        return os.path.dirname(self.metadata["testpath"])

    def _create_test_folders(self):
        """Create all needed test folders on init, and add their paths
           to self.metadata.
        """

        testdir = self._get_testdir()
        create_dir(testdir)
        for folder in ["run"]:
            name = "%sdir" % folder
            self.metadata[name] = os.path.join(testdir, folder)
            create_dir(self.metadata[name])

    def get_test_extension(self):
        """Return the test extension, which depends on the shell used. Based
           on the value of ``shell`` key we return the shell extension.

           shell: python --> py
           shell: bash --> sh (default)

           :return: returns test extension based on shell type
           :rtype: str
        """

        if "python" in self.shell["name"]:
            self.logger.debug("Setting test extension to 'py'")
            return "py"

        self.logger.debug("Setting test extension to 'sh'")
        return "sh"

    def get_environment(self):
        """Take the environment section, return a list of lines to add
           to the start of the testscript. Return lines that define
           variables specific to the shell.

           :return: list of environment variable lines to add to test script.
           :rtype: list
        """

        env = []
        pairs = self.recipe.get("env")
        shell = self.shell["name"]

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

    def run_wrapper(func):
        """The run wrapper will execute any prepare_run and finish_run 
           sections around some main run function (run or dry_run).
           A return the result. The function sets self.result and also
           returns it to the calling function.
        """

        def wrapper(self):
            self.prepare_run()
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

        # Metadata includes known sections in a Buildspec (pre/post_run, env)
        # These should all be validated for type, format, by the Buildspec schema
        self.metadata = {}
        for known_section in known_sections:
            if known_section in self.recipe:
                self.metadata[known_section] = self.recipe.get(known_section)

        # Get the shell (sh, bash) for writing testscript. A Buildspec could specify this via ``shell`` key
        self.metadata["shell"] = self.shell

        # Derive the path to the test script
        self.metadata["testpath"] = "%s.%s" % (
            os.path.join(self.testdir, self.name),
            self.get_test_extension(),
        )
        self.metadata["testpath"] = os.path.expandvars(self.metadata["testpath"])
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
        """Run the builder associated with the loaded Buildspec recipe.
           This parent class handles shared starting functions for each step
           and then calls the subclass function (_run) if it exists.

           Parameters:
           testdir: the directory to write tests to. Defaults to os.getcwd()
        """

        # Create test directory and run folder they don't exist
        self._create_test_folders()
        testfile = self._write_test()
        result = self.run_tests(testfile)
        return result

    def check_returncode(self, recipe_returncode, result_returncode):
        """ This method checks if return code from Buildspec recipe matches
            return code from test. The return type is a bool either 'True'/'False'
            depending if the return codes match

            Parameters:

            :param recipe_returncode: return code specified in recipe
            :type recipe_returncode: int, required
            :param result_returncode: return code from test
            :type result_returncode: int, required
            :return: A boolean return True/False based on conditional equality
            :rtype: bool
        """

        return recipe_returncode == result_returncode

    def check_regex(self, regex):
        """ This method conducts a regular expression check using 're.search' with regular
            expression defined in Buildspec. User must specify an output stream (stdout, stderr)
            to select when performing regex. In buildtest, this would read the .out or .err file
            based on stream and run the regular expression to see if there is a match.

            Parameters:

            :param regex: Regular expression object defined in Buildspec file
            :type regex: str, required
            :return:  A boolean return True/False based on if re.search is successful or not
            :rtype: bool
        """

        if regex["stream"] == "stdout":
            self.logger.debug(
                f"Detected regex stream 'stdout' so reading output file: {self.metadata['outfile']}"
            )
            content = read_file(self.metadata["outfile"])

        elif regex["stream"] == "stderr":
            self.logger.debug(
                f"Detected regex stream 'stderr' so reading error file: {self.metadata['errfile']}"
            )
            content = read_file(self.metadata["errfile"])

        self.logger.debug(f"Applying re.search with exp: {regex['exp']}")

        # perform a regex search based on value of 'exp' key defined in Buildspec with content file (output or error)
        return re.search(regex["exp"], content) != None

    def run_tests(self, testfile):
        """The shared _run function will run a test file, which must be
           provided. This is called by run() after generation of the
           test file, and it return a result object (dict).

           Parameters:

           :param testfile: Generated testfile by buildtest as a result of a Buildspec. This file is now executed based on the executor type
           :type testfile: str, required
        """

        # Keep a result object
        result = {}
        result["START_TIME"] = self.get_formatted_time("start_time")
        result["LOGFILE"] = self.metadata.get("logfile", "")
        result["BUILD_ID"] = self.build_id

        # Change to the test directory
        os.chdir(self._get_testdir())
        self.logger.debug(f"Changing to directory {self._get_testdir()}")

        # command to run the test
        cmd = []
        # build the run command that includes the shell path, shell options and path to test file
        cmd += [self.shell["path"], self.shell["opts"], testfile]
        self.metadata["command"] = " ".join(cmd)
        self.logger.debug(f"Running Test via command: {self.metadata['command']}")

        command = BuildTestCommand(self.metadata["command"])
        out, err = command.execute()

        # Record the ending time
        self.metadata["end_time"] = datetime.datetime.now()

        # Keep an output file
        run_output_file = os.path.join(self.metadata.get("rundir"), self.build_id)

        self.metadata["outfile"] = run_output_file + ".out"
        self.metadata["errfile"] = run_output_file + ".err"

        # write output of test to .out file

        out = "\n".join(out)
        err = "\n".join(err)

        self.logger.debug(f"Writing run output to file: {self.metadata['outfile']}")
        write_file(self.metadata["outfile"], out)

        # write error from test to .err file
        self.logger.debug(f"Writing run error to file: {self.metadata['errfile']}")
        write_file(self.metadata["errfile"], err)

        self.logger.debug(f"Return code: {command.returncode} for test: {testfile}")
        result["RETURN_CODE"] = command.returncode
        result["END_TIME"] = self.get_formatted_time("end_time")

        status = self.recipe.get("status")

        test_state = "FAIL"

        # if status is defined in Buildspec, then check for returncode and regex
        if status:

            # returncode_match is boolean to check if reference returncode matches return code from test
            returncode_match = True

            # regex_match is boolean to check if output/error stream matches regex defined in Buildspec,
            # if no regex is defined we set this to True since we do a logical AND
            regex_match = True

            if "returncode" in status:
                self.logger.debug("Conducting Return Code check")
                self.logger.debug(
                    "Status Return Code: %s   Result Return Code: %s"
                    % (status["returncode"], result["RETURN_CODE"])
                )
                # self.check_returncode checks if test returncode matches returncode specified in Buildspec.
                # The return value is a bool
                returncode_match = self.check_returncode(
                    status["returncode"], result["RETURN_CODE"]
                )

            if "regex" in status:
                self.logger.debug("Conducting Regular Expression check")
                # self.check_regex  applies regular expression check specified in Buildspec with output or error
                # stream. self.check_regex returns a boolean (True/False) by using re.search
                regex_match = self.check_regex(status["regex"])

            self.logger.info(
                "ReturnCode Match: %s Regex Match: %s "
                % (returncode_match, regex_match)
            )

            if returncode_match and regex_match:
                test_state = "PASS"

        # if status is not defined we check test returncode, by default 0 is PASS and any other return code is a FAIL
        else:
            if command.returncode == 0:
                test_state = "PASS"

        # this variable is used later when counting all the pass/fail test in buildtest/menu/build.py
        result["TEST_STATE"] = test_state

        print(
            "{:<30} {:<30} {:<30} {:<30}".format(
                self.config_name, self.name, result["TEST_STATE"], self.buildspec
            )
        )

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

    @run_wrapper
    def dry_run(self):
        """Akin to a build preview, we prepare and finish a run, but only
           print the script to the screen without writing or running files.
        """

        # Dry run just prints the testing script
        lines = self._get_test_lines()
        print("\n".join(lines))

    def _generate_build_id(self):
        """Generate a build id based on the Buildspec name, and datetime."""

        now = datetime.datetime.now().strftime("%m-%d-%Y-%H-%M")
        return "%s_%s" % (self.name, now)

    def _write_test(self, lines=None):
        """Given test metadata, write test content."""

        # If no lines provided, generate
        if not lines:
            lines = self._get_test_lines()

        # '$HOME/.buildtest/testdir/<name>/<name>_<timestamp>.sh'
        # This will put output (latest run) in same directory - do we want this?
        testpath = self.metadata["testpath"]

        self.logger.info(f"Opening Test File for Writing: {testpath}")

        # Open the test file and write contents
        with open(testpath, "w") as fd:
            fd.write("\n".join(lines))

        # Change permission of the file to executable
        os.chmod(
            testpath,
            stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH,
        )
        self.logger.debug(
            f"Applying permission 755 to {testpath} so that test can be executed"
        )
        return testpath

    def _get_test_lines(self):
        """Given test metadata, get test lines to write to file or show.

           :return: return content of test script
           :rtype: list
        """

        # start of each test should have the shebang
        lines = [self.shebang]

        # Add environment variables
        lines += self.get_environment()

        # Add lines from each build section
        for section in build_sections:
            if section in self.metadata:
                lines += [self.metadata.get(section)] or []

        return lines


class ScriptBuilder(BuilderBase):
    type = "script"
