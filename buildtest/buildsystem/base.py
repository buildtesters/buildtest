"""
BuildConfig: loader and manager for build configurations, and schema validation
Copyright (C) 2020 Vanessa Sochat.
"""

import os
import json
import re
import sys
import yaml

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from buildtest.buildsystem.schemas.utils import (
    load_schema,
    load_recipe,
    get_schemas_available,
    here,
)


supported_schemas = ["script"]


class BuildConfig:
    """A BuildConfig is a base class for a build test configuration.
       The type (e.g., script) and version are derived from reading in
       the file, and then matching to a buildtest schema, each of which is
       developed at https://github.com/HPC-buildtest/schemas and added to
       subfolders named accordingly under buildtest/tools/buildsystem/schemas.
       The schema object can load in a general test configuration file
       to validate it, and then match it to a schema available.
       If the version of a schema is not specified, we use the latest.
       If the schema fails validation, we also don't continue.
    """

    def __init__(self, config_file):
        """initiate a build configuration file, meaning that we read in the
           file, match it to a schema provided by buildtest, and 
           validate it

           Parameters
           ==========
           config_file: the pull path to the configuration file, must exist.
        """
        self.config_file = os.path.abspath(config_file)

        if not os.path.exists(self.config_file):
            sys.exit("Build configuration %s does not exist." % self.config_file)

        elif os.path.isdir(self.config_file):
            sys.exit(
                "Please provide a file path (not a directory path) to a build recipe."
            )

        # Read the lookup
        self.lookup = get_schemas_available()

        # all test configs must pass global validation (sets self.recipe)
        self._validate_global()

        # validate each schema defined in the recipes
        self._validate()


    def __str__(self):
        return "[buildtest-build-config]"

    def __repr__(self):
        return "[buildtest-build-config]"

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
            if version not in self.lookup[section['type']]:
                sys.exit("version %s is not known for type %s. Try using latest." % version, section['type'])

            # Finally, validate the section against the schema
            schema_file = os.path.join(here, section['type'], self.lookup[section['type']][version])
            validate(instance=section, schema=load_schema(schema_file))



    def _validate_global(self, config_file=None):
        """the global validation ensures that the overall structure of the
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
