import json
import os
import pytest
import re
import yaml

from jsonschema.exceptions import ValidationError
from buildtest.defaults import SCHEMA_ROOT
from buildtest.schemas.defaults import custom_validator

here = os.path.dirname(os.path.abspath(__file__))
schemaroot = os.path.join(os.path.dirname(here), "schemas")

schema_name = "compiler"
schema_file = f"{schema_name}-v1.0.schema.json"
schema_path = os.path.join(SCHEMA_ROOT, schema_file)

compiler_schema_examples = os.path.join(SCHEMA_ROOT, "examples", schema_file)


def load_schema(path):
    """load a schema from file. We assume a json file
    """
    with open(path, "r") as fd:
        schema = json.loads(fd.read())
    return schema


def load_recipe(path):
    """load a yaml recipe file
    """
    with open(path, "r") as fd:
        content = yaml.load(fd.read(), Loader=yaml.SafeLoader)
    return content


def check_invalid_recipes(recipes, invalids, loaded, version):
    for recipe in recipes:
        assert recipe
        assert re.search("(yml|yaml)$", recipe)
        recipe_path = os.path.join(invalids, recipe)
        content = load_recipe(recipe_path)

        # Ensure version is correct in header
        assert content["version"] == version
        del content["version"]

        # For each section, assume folder type and validate
        for name in content["buildspecs"].keys():
            with pytest.raises(ValidationError) as excinfo:
                custom_validator(recipe=content["buildspecs"][name], schema=loaded)
            print(excinfo.type, excinfo.value)
            print("Testing %s from recipe %s should be invalid" % (name, recipe))


def check_valid_recipes(recipes, valids, loaded, version):
    for recipe in recipes:
        assert recipe
        assert re.search("(yml|yaml)$", recipe)
        recipe_path = os.path.join(valids, recipe)
        content = load_recipe(recipe_path)

        # Ensure version is correct in header
        assert content["version"] == version
        del content["version"]

        # For each section, assume folder type and validate
        for name in content["buildspecs"].keys():
            custom_validator(recipe=content["buildspecs"][name], schema=loaded)
            print("Testing %s from recipe %s should be valid" % (name, recipe))


def test_compiler_examples():

    loaded = load_schema(schema_path)
    assert isinstance(loaded, dict)

    # Assert is named correctly
    print("Getting version of %s" % schema_file)
    match = re.search(
        "%s-v(?P<version>[0-9]{1}[.][0-9]{1})[.]schema[.]json" % schema_name,
        schema_file,
    )
    print(match)
    assert match

    # Ensure we found a version
    assert match.groups()
    version = match["version"]

    invalids = os.path.join(compiler_schema_examples, "invalid")
    valids = os.path.join(compiler_schema_examples, "valid")
    print(invalids, valids)
    assert invalids
    assert valids

    invalid_recipes = os.listdir(invalids)
    valid_recipes = os.listdir(valids)

    assert invalid_recipes
    assert valid_recipes

    check_invalid_recipes(invalid_recipes, invalids, loaded, version)
    check_valid_recipes(valid_recipes, valids, loaded, version)
