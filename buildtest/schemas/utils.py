"""
Utility and helper functions for schemas.
"""

import json
import logging
import os
import re
import sys
import yaml

here = os.path.dirname(os.path.abspath(__file__))


def load_schema(path):
    """load a schema from file. We assume either a json or yml file by
       the extension. This allows for using the function to load either,
       as the user might have difference preferences.

       Parameters:

       path: the path to the schema file.
    """

    logger = logging.getLogger(__name__)

    if not os.path.exists(path):
        sys.exit("schema file %s does not exist." % path)

    with open(path, "r") as fd:
        if re.search("[.]json$", path):
            schema = json.loads(fd.read())
        elif re.search("[.]yml$", path):
            schema = yaml.load(fd.read(), Loader=yaml.SafeLoader)
        else:
            msg = "Invalid extension for schema must be on of the following: [.json, .yml]"
            logger.error(msg)
            sys.exit(msg)

    logger.debug(f"Successfully loaded schema file: {path}")
    return schema


def load_recipe(path):
    """load a yaml recipe file. The recipe is validated against a schema.

       Parameters:

       path: the path to the recipe file.
    """
    if not os.path.exists(path):
        sys.exit("test configuration file %s does not exist." % path)
    with open(path, "r") as fd:
        content = yaml.load(fd.read(), Loader=yaml.SafeLoader)
    return content


def get_schema_fullpath(schema_file, name=None):
    """Return the full path of a schema file (expected to be under schemas

       Parameters:

       schema_file: the path to the schema file.
       name: the schema type. If not provided, derived from filename.
    """
    if not name:
        name = schema_file.split("-v", 1)[0]
    schema_file = os.path.join(here, name, schema_file)
    return schema_file
