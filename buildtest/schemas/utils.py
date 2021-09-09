"""
Utility and helper functions for schemas.
"""

import logging
import os
import sys

import yaml
from buildtest.utils.file import load_json

here = os.path.dirname(os.path.abspath(__file__))


def load_schema(path):
    """Load a json schema file, the file extension must be **.schema.json**

    Args:
        path (str): Path to schema file

    Return:
        dict: Return loaded schema as JSON document

    Raises:
         SystemExit: If filepath doesn't exist or schema file doesn't ends in **.schema.json**
    """

    logger = logging.getLogger(__name__)

    if not os.path.exists(path):
        sys.exit("schema file %s does not exist." % path)

    if not path.endswith(".schema.json"):
        msg = "Invalid extension for schema must be on of the following: '.schema.json'"
        logger.error(msg)
        sys.exit(msg)

    schema = load_json(path)

    logger.debug(f"Successfully loaded schema file: {path}")
    return schema


def load_recipe(path):
    """Load a yaml recipe file. The file must be in **.yml** extension for buildtest to load.

    Args:
        path (str): The full path to buildspec recipe

    Returns:
        dict: a dict containing buildspec that is defined in YAML format

    Raises:
        SystemExit: If filepath doesn't exist or doesn't end in **.yml** extension
    """

    if not os.path.exists(path):
        sys.exit("Check if file exists %s" % path)

    if not path.endswith(".yml"):
        sys.exit("File must end in .yml extension")

    with open(path, "r") as fd:
        content = yaml.load(fd.read(), Loader=yaml.SafeLoader)
    return content
