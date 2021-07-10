import os

import pytest
from buildtest.defaults import SCHEMA_ROOT
from buildtest.schemas.defaults import custom_validator
from buildtest.schemas.utils import load_recipe, load_schema

schema_file = "settings.schema.json"
settings_schema = os.path.join(SCHEMA_ROOT, schema_file)
settings_schema_examples = os.path.join(SCHEMA_ROOT, "examples", schema_file)


@pytest.mark.schema
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
