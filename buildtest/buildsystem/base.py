"""
BuildConfig: loader and manager for build configurations, and schema validation
Copyright (C) 2020 Vanessa Sochat.
"""

from copy import deepcopy
import datetime
import json
import logging
import os
import re
import stat
import sys
import yaml

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from buildtest.config import config_opts
from buildtest.defaults import logID, BUILDTEST_SHELL_DEFAULT
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
        self.result = {}
        self.build_id = None
        self.metadata = {}

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

        self.logger = logging.getLogger(logID)

    def __str__(self):
        return "[builder-%s-%s]" % (self.type, self.name)

    def __repr__(self):
        return self.__str__()

    def prepare_run(self):
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

        # Every build recipe has a shell (defaults to BUILDTEST_SHELL_DEFAULT
        self.metadata["shell"] = self.recipe.get("shell", BUILDTEST_SHELL_DEFAULT)

        # Every test starts with cd to TESTDIR
        self.metadata["build"] = ["cd $TESTDIR"]

        # Define the testfile name based on config root and build_id
        self.execname = "%s.exec" % self.build_id

        # Derive the path to the test script TODO: this needs to have subfolder
        self.metadata["testpath"] = "%s.sh" % (
            os.path.join(self.options["build"]["testdir"], self.name, self.build_id)
        )

        # logger.debug(f"Source Directory: {self.srcdir}")
        # logger.debug(f"Source File: {self.srcfile}")

        # pre_run and post_run, env and shell are already both added to metadata
        # build_command is added after the subclass has a chance to update metadata

    def _prepare_run(self):
        """Implemented by the child class only if build metadata needs to be
           extended or customized. This means
           that the client updates self.metadata as follows:

           build: will have the cd $TESTDIR
           pre_run, post_run, shell: are already included if defined
        """
        pass

    def _build_command(self):
        """By default, we return an empty build command. It's up to the 
           subclass to implement generation of the build command, which
           is done during _prepare_run which is after prepare_run. This
           means that self.metadata is defined for known sections (pre_run,
           post_run, shell) and the recipe is loaded as self.recipe. 
           Custom variables (vars) could also be loaded here.
        """
        return ""

    def run(self):
        """Run the builder associated with the loaded recipe.
           This parent class handles shared starting functions for each step
           and then calls the subclass function (_run) if it exists.
        """
        # Generate build id, history, refreshed config options, and base tests
        self.prepare_run()

        # If the subclass has a _prepare_run class, honor it
        if hasattr(self, "_prepare_run"):
            self._prepare_run()

        # Write and run the test, sets result at self.result
        testfile = self._write_test()
        self._run(testfile)

        # If the subclass has a _finish_run function, honor it
        if hasattr(self, "_finish_run"):
            self._finish_run()

        return self.result

    def dry_run(self):
        """Akin to a build preview
        """
        # Generate build id, history, refreshed config options, and base tests
        self.prepare_run()

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
        # TODO derive test path should include build_id
        testpath = os.path.expandvars(self.metadata["testpath"])
        testdir = os.path.dirname(testpath)

        self.logger.info(f"Opening Test File for Writing: {testpath}")

        # Create test directory if doesn't exist
        if not os.path.exists(testdir):
            os.mkdir(testdir)

        # STOPPED HERE - need to get exact path (with subfolder) and write file

    def _build_command(self):
        """Generate a command for a custom test configuration type
        """
        raise NotImplementedError


class ScriptBuilder(BuilderBase):

    type = "script"

    def _build_command(self):
        """A script build command runs some string of commands using a shell.
        """
        return self.recipe.get("run", "")

    def _dry_run(self):
        """This will be run by the builder base after dry_run(). We don't
           write tests to file, but instead preview a build (not written)
        """
        # TODO reproduce this function with self.content, ideally use global function
        # dry_view(content)
        pass
