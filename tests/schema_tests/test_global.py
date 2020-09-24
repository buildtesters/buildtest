import os
import re
import pytest

from jsonschema.exceptions import ValidationError
from buildtest.defaults import SCHEMA_ROOT
from buildtest.schemas.defaults import custom_validator
from buildtest.schemas.utils import load_recipe, load_schema

schema_name = "global"
schema_file = f"{schema_name}.schema.json"
schema_path = os.path.join(SCHEMA_ROOT, schema_file)

global_schema_examples = os.path.join(SCHEMA_ROOT, "examples", schema_file)


def check_invalid_recipes(recipes, invalids, loaded):
    """This method validates all recipes found in tests/invalid/global with global schema: global/global.schema.json"""

    for recipe in recipes:
        assert recipe
        assert re.search("(yml|yaml)$", recipe)

        recipe_path = os.path.join(invalids, recipe)
        content = load_recipe(recipe_path)

        with pytest.raises(ValidationError) as excinfo:
            custom_validator(recipe=content, schema=loaded)
        print(excinfo.type, excinfo.value)
        print("Recipe File: %s  should be invalid" % recipe_path)


def check_valid_recipes(recipes, valids, loaded):
    """This method validates all recipes found in tests/valid/global with global schema: global/global.schema.json"""

    for recipe in recipes:
        assert recipe
        assert re.search("(yml|yaml)$", recipe)
        recipe_path = os.path.join(valids, recipe)
        content = load_recipe(recipe_path)

        custom_validator(recipe=content, schema=loaded)
        print("Recipe File: %s should be valid" % recipe_path)


@pytest.mark.schema
def test_global_examples():
    """This validates all valid/invalid examples for global schema"""

    loaded = load_schema(schema_path)
    assert isinstance(loaded, dict)

    invalid_dir = os.path.abspath(os.path.join(global_schema_examples, "invalid"))
    valid_dir = os.path.abspath(os.path.join(global_schema_examples, "valid"))

    assert invalid_dir
    assert valid_dir

    invalid_recipes = os.listdir(invalid_dir)
    valid_recipes = os.listdir(valid_dir)

    assert invalid_recipes
    assert valid_recipes

    print(f"Detected Invalid Global Directory: {invalid_dir}")
    print(f"Detected Valid Global Directory: {valid_dir}")
    print(f"Invalid Recipes: {invalid_recipes}")
    print(f"Valid Recipes: {valid_recipes}")

    check_invalid_recipes(invalid_recipes, invalid_dir, loaded)
    check_valid_recipes(valid_recipes, valid_dir, loaded)
