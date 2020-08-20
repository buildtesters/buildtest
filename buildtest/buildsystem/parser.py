"""
BuildspecParser is intended to read in a Buildspec file with one or
more test blocks, and then generate builders based on the type
of each. The BuilderBase is the base class for all builders that
expose functions to run builds.
"""

import logging
import os
import sys
from jsonschema import validate
from buildtest.schemas.utils import load_recipe
from buildtest.schemas.defaults import schema_table
from buildtest.utils.file import resolve_path, is_dir

from buildtest.buildsystem.base import (
    ScriptBuilder,
    GNUCompiler,
    CrayCompiler,
    IntelCompiler,
    PGICompiler,
)


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

        self.logger.info(
            f"Validating {self.buildspec} with schema: {schema_table['global']['path']}"
        )

        validate(instance=self.recipe, schema=schema_table["global"]["recipe"])

    # Validation

    def _validate(self):
        """Given a loaded recipe, validate that the type is known in the lookup
           to buildtest. If a version is provided, honor it. If not, use latest.
           We also don't allow repeated keys in the same file.
        """

        self.schema_version = self.recipe.get("version", "latest")

        for name in self.recipe["buildspecs"].keys():

            self.logger.info(
                "Validating test - '%s' in recipe: %s" % (name, self.buildspec)
            )

            # the buildspec section must be an dict where test is defined. If
            # it's not a dict then we should raise an error.
            if not isinstance(self.recipe["buildspecs"][name], dict):
                sys.exit(f"Section: {self.recipe[name]} must be a dictionary")

            self.logger.info("%s is a dictionary", name)

            # extract type field from test, if not found set to None
            type = self.recipe.get("buildspecs").get(name).get("type") or None

            # if type not found in section, raise an error since we every test
            # must be associated to a schema which is controlled by 'type' key
            if not type:
                sys.exit(f"Did not find 'type' key in test section: {name}")

            self.logger.info("Detected field 'type: %s'", type)

            # Ensure we have a Buildspec recipe with a valid type
            if type not in schema_table["types"]:
                sys.exit("type %s is not known to buildtest." % type)

            self.logger.info(
                "Checking %s in supported type schemas: %s", type, schema_table["types"]
            )

            # And that there is a version file
            if self.schema_version not in schema_table[type]["versions"]:
                sys.exit(
                    "version %s is not known for schema type %s. Valid options are: %s"
                    % (self.schema_version, type, schema_table[type]["versions"])
                )
            self.logger.info(
                "Checking version '%s' in version list: %s",
                self.schema_version,
                schema_table[type]["versions"],
            )

            self.logger.info(
                "Validating test - '%s' with schemafile: %s"
                % (name, os.path.basename(schema_table[type]["path"]))
            )

            self.schema_file = os.path.basename(schema_table[type]["path"])
            validate(
                instance=self.recipe["buildspecs"][name],
                schema=schema_table[type]["recipe"],
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

                if recipe.get("skip"):
                    print(f"[{name}] test is skipped.")
                    continue

                # Add the builder based on the type
                if recipe["type"] == "script":
                    builders.append(
                        ScriptBuilder(name, recipe, self.buildspec, testdir=testdir,)
                    )
                elif recipe["type"] == "compiler":
                    if recipe["build"].get("name") == "gnu":
                        builders.append(
                            GNUCompiler(name, recipe, self.buildspec, testdir=testdir,)
                        )
                    elif recipe["build"].get("name") == "intel":
                        builders.append(
                            IntelCompiler(
                                name, recipe, self.buildspec, testdir=testdir,
                            )
                        )
                    elif recipe["build"].get("name") == "pgi":
                        builders.append(
                            PGICompiler(name, recipe, self.buildspec, testdir=testdir,)
                        )
                    elif recipe["build"].get("name") == "cray":
                        builders.append(
                            CrayCompiler(name, recipe, self.buildspec, testdir=testdir,)
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
