import json
import os
import yaml

from buildtest.defaults import SCHEMA_ROOT
from buildtest.schemas.defaults import custom_validator


schema_file = "settings.schema.json"
settings_schema = os.path.join(SCHEMA_ROOT, schema_file)
settings_schema_examples = os.path.join(SCHEMA_ROOT, "examples", schema_file)


def load_schema(path):
    """load a schema from file. We assume a json file"""
    with open(path, "r") as fd:
        schema = json.loads(fd.read())
    return schema


def load_recipe(path):
    """load a yaml recipe file"""
    with open(path, "r") as fd:
        content = yaml.load(fd.read(), Loader=yaml.SafeLoader)
    return content


def test_settings_examples():

    # load schema and ensure type is a dict
    recipe = load_schema(settings_schema)

    valid = os.path.join(settings_schema_examples, "valid")
    assert valid

    valid_recipes = os.listdir(valid)
    assert valid_recipes
    # check all valid recipes
    for example in valid_recipes:

        filepath = os.path.join(valid, example)
        print(f"Loading Recipe File: {filepath}")
        example_recipe = load_recipe(filepath)
        assert example_recipe

        print(f"Expecting Recipe File: {filepath} to be valid")
        custom_validator(recipe=example_recipe, schema=recipe)
