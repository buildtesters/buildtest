"""
BuildConfig: loader and manager for build configurations, and schema validation
Copyright (C) 2020 Vanessa Sochat.
"""

import datetime
import json
import os
import re
import sys
import yaml

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from buildtest.config import config_opts
from buildtest.defaults import logID
from buildtest.buildsystem.schemas.utils import (
    load_schema,
    load_recipe,
    get_schemas_available,
    here,
)

# each has a subfolder in buildtest/buildsystem/schemas/ with *.schema.json
supported_schemas = ["script"]

# global config sections that are known, added to buildbase.metadata
known_sections = ["env", "pre_run", "post_run"]


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

    # Metadata keys are not considered build sections
    metadata = ["version"]

    def __init__(self, config_file):
        """initiate a build configuration file, meaning that we read in the
           file, match it to a schema provided by buildtest, and 
           validate it

           Parameters
           ==========
           config_file: the pull path to the configuration file, must exist.
        """
        self.recipe = None
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

    # Builders

    def get_builders(self):
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
                    builders.append(ScriptBuilder(name, recipe_config))
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
           through just section names, use self.keys() to filter out metadata
        """
        return self.recipe.get(name)


class BuilderBase:
    """The BuilderBase is an abstract class that implements common functions for
       any kind of builder.
    """

    def __init__(self, name, recipe_config):
        """initiate a builder base. A recipe configuration (loaded) is required.
           this can be handled easily with the BuildConfig class:

           bc = BuildConfig(config_file)
           recipe_config = bc.get("section_name")
           builder = ScriptBuilder(recipe_config)

           Parameters
           ==========
           name: a name for the build recipe (required)
           config_file: the pull path to the configuration file, must exist.
        """
        self.name = name
        self.build_id = None

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

        # TODO need to add logger for builder here
        logger = logging.getLogger(logID)

    def _prepare_run(self):
        """Prepare run provides shared functions to set up metadata and
           class data structures that are used by both run and dry_run
           This section cannot be reached without a valid, loaded recipe
        """
        # Generate a unique id for the build based on key and unique string
        self.build_id = self._generate_build_id()

        # History is returned at the end of a run
        self.history = {}
        self.history["TESTS"] = []

        # Create a deep copy of config_opts for the build file
        self.options = deepcopy(config_opts)

        # Metadata includes known sections in a config recipe (pre/post_run, env)
        # These should all be validated for type, format, by the schema validator
        self.metadata = {}
        for known_section in known_sections:
            if known_section in self.recipe:
                self.metadata[known_section] = self.recipe.get(known_section)

        # TODO: look at what this function did, decide where to derive content.
        # likely this section should produce a base of metadata that can
        # be added to in the calling subclass, and then the result shown/run
        # content = singlesource_test.build_test_content()

    def run(self):
        """Given the name of a section in the loaded recipe, run the build.
           This parent class handles shared starting functions for each step
           and then calls the subclass function (_run) if it exists.
        """
        # Generate build id, history, and refreshed config options
        self._prepare_run()

        # Each subclass has a _run function to perform custom build operations
        if not hasattr(self, "_run"):
            raise NotImplementedError

        # Run the build for the subclass
        self._run()

    def dry_run(self):
        """Akin to a build preview
        """
        # Generate build id, history, and refreshed config options
        self._prepare_run()

        # Each subclass has a _run function to perform custom build operations
        if not hasattr(self, "_dry_run"):
            raise NotImplementedError

        # Run the build for the subclass
        self._dry_run()

    def _generate_build_id(self):
        """Generate a build id based on the recipe name, type, and datetime
        """
        now = datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-S")
        return "%s_%s_%s" % (self.name, self.type, now)

    def _write_test(self):
        """Given test metadata, write test content. (need to think this through)
        """
        raise NotImplementedError

    def _build_command(self):
        """Generate a command for a custom test configuration type
        """
        raise NotImplementedError


class ScriptBuilder(BuilderBase):

    type = "script"

    def _run(self):
        """Given the name of a section in the loaded recipe, run the build.
           We get here when the user calls run() for the parent class, 
           and metadata and a build id are prepared.
        """
        # TODO- this is where class specific work will use the self.metadata
        # To finish up and then write the test content. The write function
        # should be shared and provided by the builder base.
        # write the test to run
        self._write_test(self.content)

    def _build_command(self):
        """Generate a command for a custom test configuration type
        """
        raise NotImplementedError

    def _dry_run(self):
        """This will be run by the builder base after dry_run(). We don't
           write tests to file, but instead preview a build (not written)
        """
        # TODO reproduce this function with self.content, ideally use global function
        # dry_view(content)
