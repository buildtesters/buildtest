"""
BuildspecParser is will validate a Buildspec file with the global schema
and each test will be validated with one of the subschemnas based on the
type field. The BuilderBase is the base class for all builders that
expose functions to run builds.
"""

import logging
import os
import re

from buildtest.defaults import console
from buildtest.exceptions import BuildspecError, BuildTestError
from buildtest.executors.setup import BuildExecutor
from buildtest.schemas.defaults import custom_validator, schema_table
from buildtest.schemas.utils import load_recipe
from buildtest.utils.file import is_dir, resolve_path


class BuildspecParser:
    """A BuildspecParser is responsible for validating a Buildspec file with JSON Schema.

    The type (e.g., script) and version are derived from reading in
    the file, and then matching to a Buildspec schema.

    The schemas are located in folder `buildtest/schemas <https://github.com/buildtesters/buildtest/tree/devel/buildtest/schemas>`_,
    we load the schema dictionary and validate each buildspec with global schema and a sub-schema based on the
    ``type`` field. If the schema fails validation check, then we stop immediately.
    """

    def __init__(self, buildspec, buildexecutor):
        """The init method will run some checks against buildspec before loading
        buildspec. buildtest will validate the entire buildspec with
        `global.schema.json <https://github.com/buildtesters/buildtest/blob/devel/buildtest/schemas/global.schema.json>`_
        and validate each test section with the designated
        type schema. For instance of test includes ``type: script`` we will validate the test with schema
        `script-v1.0.schema.json <https://github.com/buildtesters/buildtest/blob/devel/buildtest/schemas/script-v1.0.schema.json>`_.

        If there is any error during the init method, an exception will be raised.

        Args:
            buildspec (str): Full path to buildspec file
            buildexecutor (buildtest.executors.setup.BuildExecutor): Instance object of class BuildExecutor used for accessing executors which is created based on configuration file

        Raises:
            BuildTestError: Raise exception if there is issue with buildexecutor, or buildspec is not resolved to file path. If buildspec is a directory path we raise an exception
        """

        self.logger = logging.getLogger(__name__)

        if not isinstance(buildexecutor, BuildExecutor):
            raise BuildTestError(
                "Invalid type argument for 'buildexecutor', must be of type BuildExecutor"
            )

        self.buildexecutors = buildexecutor

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

        if not self.recipe:
            msg = f"[red]Unable to load buildspec file: {self.buildspec}. The file appears to be invalid"
            console.print(msg)
            raise BuildTestError(msg)

        # validate each schema defined in the recipes
        self.validate()

    def __str__(self):
        return "[buildspec-parser]"

    def __repr__(self):
        return "[buildspec-parser]"

    def _check_schema_type(self, test):
        """Check ``type`` field is a valid sub-schema and verify ``type`` + ``version`` will resolve to a schema file.

        Args:
            test (str): Name of test in ``buildspecs`` property of buildspec file

        Raises:
            BuildspecError: If there is no match with ``type`` property in test with available schema types
        """

        # extract type field from test, if not found set to None
        self.schema_type = self.recipe["buildspecs"][test].get("type")

        # if type not found in section, raise an error since every test
        # must be associated to a schema which is controlled by 'type' key
        if not self.schema_type:
            msg = f"Did not find 'type' key in test section: {test}"
            raise BuildspecError(self.buildspec, msg)

        self.logger.info("Detected field 'type: %s'", self.schema_type)

        # Ensure we have a Buildspec recipe with a valid type
        if self.schema_type not in schema_table["types"]:
            msg = f"type {self.schema_type} is not known to buildtest."
            raise BuildspecError(self.buildspec, msg)

        self.logger.info(
            "Checking '%s' in supported type schemas: %s",
            self.schema_type,
            schema_table["types"],
        )

        # And that there is a version file
        if self.schema_version not in schema_table["versions"][self.schema_type]:
            msg = f"version {self.schema_version} is not known for schema type: {self.schema_type}. Valid options for schema type are: {schema_table['versions'][self.schema_type]}"
            raise BuildspecError(self.buildspec, msg)

        self.logger.info(
            "Checking version '%s' in version list: %s",
            self.schema_version,
            schema_table["versions"][self.schema_type],
        )

    def _check_executor(self, test):
        """This method checks if ``executor`` property is not None and executor
        value is found in list of available executors.

        Args:
            test (str): Name of test in ``buildspecs`` property of buildspec file

        Raises:
            BuildspecError: If there is no match with ``executor`` property in test with list of available executors
        """

        # extract type field from test, if not found
        executor = self.recipe["buildspecs"][test].get("executor")

        if not executor:
            raise BuildspecError(self.buildspec, "No 'executor' key found in buildspec")

        match = False
        for name in self.buildexecutors.list_executors():
            if re.match(executor, name):
                match = True
                break

        if not match:
            raise BuildspecError(
                self.buildspec,
                f"Unable to find executor: {executor} in {self.buildexecutors.list_executors()}",
            )

        self.logger.debug(
            f"Executor: {executor} found in executor list: {self.buildexecutors.list_executors()}"
        )

    def validate(self):
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

        self.schema_version = self.recipe.get("version")

        # validate all test instances in 'buildspecs' property. The validation
        # consist of checking schema type, executor name and validating each section
        # with sub schema

        for test in self.get_test_names():

            self.logger.info(
                "Validating test - '%s' in recipe: %s" % (test, self.buildspec)
            )

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

    def get_test_names(self):
        """Return a list of test names from a buildspec file. The test names are defined under the 'buildspecs' property"""
        return self.recipe.get("buildspecs").keys()
