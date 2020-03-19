"""
Utility and helper functions for schemas.
Copyright (C) 2020 Vanessa Sochat.
"""

import os
import json
from jsonschema import validate
import re
import sys
import yaml

here = os.path.dirname(os.path.abspath(__file__))


def load_schema(path):
    """load a schema from file. We assume a json file

       Parameters:

       path: the path to the schema file.
    """
    if not os.path.exists(path):
        sys.exit("schema file %s does not exist." % path)
    with open(path, "r") as fd:
        schema = json.loads(fd.read())
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


def get_latest(schema1, schema2):
    """between two schema files, compare versions and determine which is latest

       Parameters:

       schema1: the path to the first schema file.
       schema2: the path to the second schema file.
    """
    schema1_version = get_schema_version(schema1)
    schema2_version = get_schema_version(schema2)

    # Convert version to int to determine latest
    if int(schema1_version.replace(".", "")) > int(schema2_version.replace(".", "")):
        return schema1
    return schema2


def get_schema_version(schema):
    """Given a schema file, use the convention naming of
       <name>-v<version>.schema.json to derive the version

       Parameters:

       schema: the path to the schema file.
    """
    match = re.search(
        "v(?P<version>[0-9]{1}[.][0-9]{1}[.][0-9]{1})[.]schema[.]json", schema
    )
    if match:
        return match["version"]


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


def get_schemas_available():
    """Based on the schemas installed to buildtest under
       buildtest/buildsystem/schemas, return a lookup for names (e.g., script)
       versions, and their corresponding paths. The highest number is tagged
       as "latest"
    """
    lookup = {}
    schema_names = [
        x
        for x in os.listdir(here)
        if os.path.isdir(os.path.join(here, x)) and not x.startswith("_")
    ]
    for schema_name in schema_names:
        schema_dir = os.path.join(here, schema_name)
        schemas = [x for x in os.listdir(schema_dir) if x.endswith(".schema.json")]

        # Add the schema name to the lookup
        if schema_name not in lookup:
            lookup[schema_name] = {}

        # Keep track of latest filename for group
        latest = None

        for schema in schemas:
            version = get_schema_version(schema)
            if version:

                # Add the schema to lookup if we have version
                lookup[schema_name][version] = schema

                # Is this the latest?
                if not latest:
                    latest = schema
                else:
                    latest = get_latest(schema, latest)

        # Add the latest to the group
        if latest:
            lookup[schema_name]["latest"] = latest

    return lookup
