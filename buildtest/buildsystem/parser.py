"""
BuildspecParser is intended to read in a Buildspec file with one or
more test blocks, and then generate builders based on the type
of each. The BuilderBase is the base class for all builders that
expose functions to run builds.
"""

import logging
import os
import sys
from buildtest.config import load_settings
from buildtest.executors.setup import BuildExecutor
from buildtest.schemas.utils import load_recipe
from buildtest.schemas.defaults import schema_table, custom_validator
from buildtest.utils.file import resolve_path, is_dir
from buildtest.system import BuildTestSystem

from buildtest.buildsystem.base import ScriptBuilder, CompilerBuilder

configuration = load_settings()
master_executors = BuildExecutor(configuration)
executors = master_executors.executors.keys()


class BuildspecParser:
    """A BuildspecParser is a base class for loading and validating a Buildspec file.
       The type (e.g., script) and version are derived from reading in
       the file, and then matching to a Buildspec schema.

       The schemas are located in buildtest/schemas, we load the schema dictionary
       and validate each buildspec with global schema and a sub-schema based on the
       type field.

       If the version of a schema is not specified, we use the latest.
       If the schema fails validation check, then we stop immediately.
    """

    def __init__(self, buildspec):
        """The init method will run some checks against buildspec before loading
           buildspec. We retrieve available schemas via method
           ``get_schemas_available`` and check if ``type`` in buildspec
           match available schema. We validate the entire buildspec with
           global.schema.json and validate each test section with the designated
           type schema. If there is any error during the init method, an
           exception will be raised.

           :param buildspec: the pull path to the Buildspec file, must exist.
           :type buildspec: str, required
        """

        self.logger = logging.getLogger(__name__)
        self.executors = list(executors)
        # if invalid input for buildspec
        if not buildspec:
            sys.exit("Invalid input type for Buildspec, must be of type 'string'.")

        self.buildspec = resolve_path(buildspec)

        if not self.buildspec:
            sys.exit("There is no file named: %s " % buildspec)

        if is_dir(self.buildspec):
            sys.exit(
                f"Detected {self.buildspec} is a directory, please provide a file path (not a directory path) to BuildspecParser."
            )

        self.recipe = load_recipe(self.buildspec)
        # ensure self.recipe exists after loading recipe
        assert self.recipe

        # validate each schema defined in the recipes
        self._validate()

    def __str__(self):
        return "[buildspec-parser]"

    def __repr__(self):
        return "[buildspec-parser]"

    def _check_schema_type(self, test):
        """Check ``type`` field is a valid sub-schema and verify ``type`` + ``version``
           will resolve to a schema file.
        """

        # extract type field from test, if not found set to None
        self.schema_type = self.recipe["buildspecs"][test].get("type")

        # if type not found in section, raise an error since every test
        # must be associated to a schema which is controlled by 'type' key
        if not self.schema_type:
            sys.exit(f"Did not find 'type' key in test section: {test}")

        self.logger.info("Detected field 'type: %s'", self.schema_type)

        # Ensure we have a Buildspec recipe with a valid type
        if self.schema_type not in schema_table["types"]:
            sys.exit("type %s is not known to buildtest." % self.schema_type)

        self.logger.info(
            "Checking %s in supported type schemas: %s",
            self.schema_type,
            schema_table["types"],
        )

        # And that there is a version file
        if self.schema_version not in schema_table["versions"][self.schema_type]:
            sys.exit(
                "version %s is not known for schema type %s. Valid options are: %s"
                % (
                    self.schema_version,
                    self.schema_type,
                    schema_table["versions"][self.schema_type],
                )
            )
        self.logger.info(
            "Checking version '%s' in version list: %s",
            self.schema_version,
            schema_table["versions"][self.schema_type],
        )

    def _check_executor(self, test):

        # extract type field from test, if not found set to None
        executor = self.recipe["buildspecs"][test].get("executor") or None

        if executor not in self.executors:
            sys.exit(
                f"executor: {executor} not found in executor list: {self.executors}"
            )

    def _validate(self):
        """This method will validate the entire buildspec file with global schema
           and each test section with a sub-schema. The global validation ensures
           that the overall structure of the file is sound for further parsing.
           We load in the global.schema.json for this purpose.

           A buildspec is composed of one or more tests, each section is validated
           with a sub-schema. The ``type`` field is used for sub-schema lookup
           from schema library. Finally we validate loaded recipe with sub-schema
        """

        self.logger.info(
            f"Validating {self.buildspec} with schema: {schema_table['global.schema.json']['path']}"
        )
        custom_validator(
            recipe=self.recipe, schema=schema_table["global.schema.json"]["recipe"]
        )

        self.schema_version = self.recipe.get("version", "latest")

        assert isinstance(self.recipe.get("buildspecs"), dict)

        for test in self.recipe["buildspecs"].keys():

            self.logger.info(
                "Validating test - '%s' in recipe: %s" % (test, self.buildspec)
            )

            # the buildspec section must be an dict where test is defined. If
            # it's not a dict then we should raise an error.
            assert isinstance(self.recipe["buildspecs"].get(test), dict)

            self._check_schema_type(test)
            self._check_executor(test)

            self.schema_file = os.path.basename(
                schema_table[f"{self.schema_type}-v{self.schema_version}.schema.json"][
                    "path"
                ]
            )
            custom_validator(
                recipe=self.recipe["buildspecs"][test],
                schema=schema_table[
                    f"{self.schema_type}-v{self.schema_version}.schema.json"
                ]["recipe"],
            )

    # Builders
    def _skip_tests_by_executor(self, recipe, testname, executor_filter=None):
        """This method returns a boolean if tests need to be skipped by executors. If
           executor in buildspec not found match in executor filter we skip test. This
           check is performed only if executor_filter is passed. The executor_filter
           is usually set if user runs ``buildtest build --executor``

           :param recipe: loaded buildspec recipe as dictionary
           :type recipe: dict
           :param testname: name of test instance in buildspec file
           :type testname: str
           :param executor_filter: A list of executor name to filter test.
           :type executor_filter: list, optional
           :return: A boolean to determine if test is skipped
           :rtype: bool
        """

        # if input 'buildtest build --executor' is set we filter test by
        # executor name. For now we skip all test that don't belong in executor list.
        if executor_filter and recipe.get("executor") not in executor_filter:
            print(
                f"[{testname}] test is skipped because it is not in executor filter list: {executor_filter}"
            )
            return True

        return False

    def _skip_tests_by_tags(self, recipe, name, tag_filter=None):
        """ This method determines if test should be skipped based on tag names specified
            in filter field. The parameter ``tag_filter`` is a list of tag names typically
            specified with ``buildtest build --tags`` which must be checked with buildspec
            tags.

            :param recipe: loaded buildspec recipe as dictionary
            :param name: An instance of test from buildspec file
            :param tag_filter: A list of tag names to filter test. If tag filter not defined we return False
            :return: Returns a boolean True/False which determines if test is skipped.
            :rtype: bool
        """

        if tag_filter:
            # if tags field in buildspec is empty, then we skip test only if user filters by tags
            if not recipe.get("tags"):
                return True

            found = False
            for tagname in tag_filter:
                if tagname in recipe.get("tags"):
                    found = True

            if not found:
                print(
                    f"[{name}] test is skipped because it is not in tag filter list: {tag_filter}"
                )
                return True

        return False

    def _skip_tests_run_only(self, recipe, name, system):
        """ This method will skip tests based on ``run_only`` field from buildspec. Checks
            are performed based on conditionals and if any conditional is not met we skip test.

            :param recipe: loaded buildspec recipe as dictionary
            :param name: name of test from buildspec file
            :param system: An instance of ``BuildTestSystem`` class
            :return: Returns a boolean to see if test is skipped based on ``run_only`` property
            :rtype: bool
        """
        # if run_only field set, check if all conditions match before proceeding with test
        if recipe.get("run_only"):

            # skip test if host scheduler is not one specified via 'scheduler' field
            if recipe["run_only"].get("scheduler") and (
                recipe["run_only"].get("scheduler") not in system.system["scheduler"]
            ):
                msg = f"[{name}] test is skipped because ['run_only']['scheduler'] got value: {recipe['run_only']['scheduler']} but detected scheduler: {system.system['scheduler']}."
                print(msg)
                self.logger.info(msg)
                return True

            # skip test if current user is not one specified in 'user' field
            if recipe["run_only"].get("user") and (
                recipe["run_only"].get("user") != os.getenv("USER")
            ):
                msg = f"[{name}] test is skipped because ['run_only']['user'] got value: {recipe['run_only']['user']} but detected user: {os.getenv('USER')}."
                print(msg)
                self.logger.info(msg)
                return True

            # skip test if host platform is not equal to value specified by 'platform' field
            if recipe["run_only"].get("platform") and (
                recipe["run_only"].get("platform") != system.system["platform"]
            ):
                msg = f"[{name}] test is skipped because ['run_only']['platform'] got value: {recipe['run_only']['platform']} but detected platform: {system.system['platform']}."
                print(msg)
                self.logger.info(msg)
                return True

            # skip test if host platform is not equal to value specified by 'platform' field
            if recipe["run_only"].get("linux_distro"):
                if system.system["os"] not in recipe["run_only"]["linux_distro"]:
                    msg = f"[{name}] test is skipped because ['run_only']['linux_distro'] got value: {recipe['run_only']['linux_distro']} but detected platform: {system.system['os']}."
                    print(msg)
                    self.logger.info(msg)
                    return True

        return False

    def get_builders(self, testdir, rebuild=1, tag_filter=None, executor_filter=None):
        """ Based on a loaded Buildspec file, return the correct builder
            for each based on the type. Each type is associated with a known
            Builder class.

            :param testdir: Test Destination directory, specified by --testdir
            :type testdir: str
            :param rebuild: Number of rebuilds for a tesst this is specified by ``buildtest build --rebuild``. Defaults to 1
            :type rebuild: int, optional
            :param tag_filter: A list of input tags (``buildtest build --tags`` option) to filter builders
            :type tag_filter: list, optional
            :param executor_filter: A list of input executors (``buildtest build --executor`` option) to filter builders
        """

        system = BuildTestSystem()
        builders = []

        for count in range(rebuild):

            for name in self.keys():
                recipe = self.recipe["buildspecs"][name]

                if recipe.get("skip"):
                    print(f"[{name}] test is skipped.")
                    continue

                if self._skip_tests_by_executor(recipe, name, executor_filter):
                    continue

                if self._skip_tests_by_tags(recipe, name, tag_filter):
                    continue

                if self._skip_tests_run_only(recipe, name, system):
                    continue

                # Add the builder based on the type
                if recipe["type"] == "script":
                    builders.append(
                        ScriptBuilder(name, recipe, self.buildspec, testdir=testdir,)
                    )
                elif recipe["type"] == "compiler":
                    builders.append(
                        CompilerBuilder(name, recipe, self.buildspec, testdir=testdir)
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
            keys = [x for x in self.recipe["buildspecs"].keys()]
        return keys

    def get(self, name):
        """Given the name of a section (typically a build configuration name)
        return the loaded section from self.recipe. If you need to parse
        through just section names, use self.keys() to filter out metadata.
        """

        return self.recipe.get(name)
