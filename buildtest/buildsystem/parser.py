"""
BuildspecParser is intended to read in a Buildspec file with one or
more test blocks, and then generate builders based on the type
of each. The BuilderBase is the base class for all builders that
expose functions to run builds.
"""

import logging
import os
from buildtest.config import buildtest_configuration
from buildtest.exceptions import BuildTestError
from buildtest.executors.setup import BuildExecutor
from buildtest.schemas.utils import load_recipe
from buildtest.schemas.defaults import schema_table, custom_validator
from buildtest.utils.file import resolve_path, is_dir


class BuildspecParser:
    """A BuildspecParser is a base class for loading and validating a Buildspec file.
    The type (e.g., script) and version are derived from reading in
    the file, and then matching to a Buildspec schema.

    The schemas are located in buildtest/schemas, we load the schema dictionary
    and validate each buildspec with global schema and a sub-schema based on the
    ``type`` field. If the schema fails validation check, then we stop immediately.
    """

    def __init__(self, buildspec, buildexecutor):
        """The init method will run some checks against buildspec before loading
        buildspec. We retrieve available schemas via method
        ``get_schemas_available`` and check if ``type`` in buildspec
        match available schema. We validate the entire buildspec with
        global.schema.json and validate each test section with the designated
        type schema. If there is any error during the init method, an
        exception will be raised.

        :param buildspec: the pull path to the Buildspec file, must exist.
        :type buildspec: str, required
        :param buildexecutor: an instance of BuildExecutor class defines Executors from configuration file
        :type buildexecutor: BuildExecutor, required
        """

        self.logger = logging.getLogger(__name__)

        if not isinstance(buildexecutor, BuildExecutor):
            raise BuildTestError(
                "Invalid type argument for 'buildexecutor', must be of type BuildExecutor"
            )

        self.buildexecutors = buildexecutor.list_executors()

        # if invalid input for buildspec
        if not buildspec:
            raise BuildTestError(
                "Invalid input type for Buildspec, must be of type 'string'."
            )

        self.buildspec = resolve_path(buildspec)

        if not self.buildspec:
            raise BuildTestError("There is no file named: %s " % buildspec)

        if is_dir(self.buildspec):
            raise BuildTestError(
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
            raise BuildTestError(f"Did not find 'type' key in test section: {test}")

        self.logger.info("Detected field 'type: %s'", self.schema_type)

        # Ensure we have a Buildspec recipe with a valid type
        if self.schema_type not in schema_table["types"]:
            raise BuildTestError(
                "type %s is not known to buildtest." % self.schema_type
            )

        self.logger.info(
            "Checking '%s' in supported type schemas: %s",
            self.schema_type,
            schema_table["types"],
        )

        # And that there is a version file
        if self.schema_version not in schema_table["versions"][self.schema_type]:
            raise BuildTestError(
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
        """This method checks if ``executor`` property is not None and executor
        value is found in list of available executors.

        :param test: name of test in ``buildspecs`` property in buildspec file
        :type test: str, required
        """

        # extract type field from test, if not found set to None
        executor = self.recipe["buildspecs"][test].get("executor") or None

        if executor not in self.buildexecutors:
            raise BuildTestError(
                f"executor: {executor} not found in executor list: {self.buildexecutors}"
            )
        self.logger.debug(
            f"Executor: {executor} found in executor list: {self.buildexecutors}"
        )

    def _validate(self):
        """This method will validate the entire buildspec file with global schema
        and each test section with a sub-schema. The global validation ensures
        that the overall structure of the file is sound for further parsing.
        We load in the global.schema.json for this purpose.

        A buildspec is composed of one or more tests, each section is validated
        with a sub-schema. The ``type`` field is used for sub-schema lookup
        from schema library. Finally we validate loaded recipe with sub-schema.
        """

        self.logger.info(
            f"Validating {self.buildspec} with schema: {schema_table['global.schema.json']['path']}"
        )
        custom_validator(
            recipe=self.recipe, schema=schema_table["global.schema.json"]["recipe"]
        )

        self.schema_version = self.recipe.get("version", "latest")

        assert isinstance(self.recipe.get("buildspecs"), dict)

        # validate all test instances in 'buildspecs' property. The validation
        # consist of checking schema type, executor name and validating each section
        # with sub schema
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
            # validate test instance with sub schema
            custom_validator(
                recipe=self.recipe["buildspecs"][test],
                schema=schema_table[
                    f"{self.schema_type}-v{self.schema_version}.schema.json"
                ]["recipe"],
            )
