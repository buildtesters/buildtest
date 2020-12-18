"""
Utility and helper functions for schemas.
"""

import json
import logging
import os
import sys
import yaml

here = os.path.dirname(os.path.abspath(__file__))

from buildtest.exceptions import BuildTestError


def load_schema(path):
    """Load a json schema file, the file extension must be '.schema.json'

    :param path: the path to the schema file.
    :type path: str
    """

    logger = logging.getLogger(__name__)

    if not os.path.exists(path):
        sys.exit("schema file %s does not exist." % path)

    if not path.endswith(".schema.json"):
        msg = "Invalid extension for schema must be on of the following: '.schema.json'"
        logger.error(msg)
        sys.exit(msg)

    with open(path, "r") as fd:
        schema = json.loads(fd.read())

    logger.debug(f"Successfully loaded schema file: {path}")
    return schema


def load_recipe(path):
    """Load a yaml recipe file. The file must be in .yml extension
    for buildtest to load.

    :param path: the path to the recipe file.
    :type path: str
    """

    if not os.path.exists(path):
        sys.exit("Check if file exists %s" % path)

    if not path.endswith(".yml"):
        sys.exit("File must end in .yml extension")

    with open(path, "r") as fd:
        content = yaml.load(fd.read(), Loader=yaml.SafeLoader)
    return content


def get_schema_fullpath(schema_file, name=None):
    """Return the full path of a schema file

    :param schema_file: the path to the schema file.
    :type schema_file: str
    :param name: the schema type. If not provided, derived from filename.
    :type name: str, optional
    """
    if not name:
        name = schema_file.split("-v", 1)[0]
    schema_file = os.path.join(here, schema_file)
    return schema_file
