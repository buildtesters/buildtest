import os
import re

import pytest
from buildtest.defaults import SCHEMA_ROOT
from buildtest.schemas.defaults import custom_validator
from buildtest.schemas.utils import load_recipe, load_schema
from jsonschema.exceptions import ValidationError

schema_name = "script"
schema_file = f"{schema_name}-v1.0.schema.json"
schema_path = os.path.join(SCHEMA_ROOT, schema_file)
schema_examples = os.path.join(SCHEMA_ROOT, "examples", schema_file)


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
                print("Testing %s from recipe %s should be invalid" % (name, recipe))
                custom_validator(recipe=content["buildspecs"][name], schema=loaded)
            print(excinfo.exconly())
            # print("Testing %s from recipe %s should be invalid" % (name, recipe))


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
            print(content["buildspecs"][name])
            custom_validator(recipe=content["buildspecs"][name], schema=loaded)
            print("Testing %s from recipe %s should be valid" % (name, recipe))


@pytest.mark.schema
def test_script_examples(tmp_path):
    """the script test_organization is responsible for all the schemas
    in the root of the repository, under <schema>/examples.
    A schema specific test is intended to run tests that
    are specific to a schema. In this case, this is the "script"
    folder. Invalid examples should be under ./invalid/script.
    """

    print("Testing schema %s" % schema_file)
    print("schema_path:", schema_path)
    loaded = load_schema(schema_path)
    assert isinstance(loaded, dict)

    # Assert is named correctly
    print("Getting version of %s" % schema_file)
    match = re.search(
        "%s-v(?P<version>[0-9]{1}[.][0-9]{1})[.]schema[.]json" % schema_name,
        schema_file,
    )
    assert match

    # Ensure we found a version
    assert match.groups()
    version = match["version"]

    # Ensure a version folder exists with invalids
    print("Checking that invalids exist for %s" % schema_file)
    invalids = os.path.join(schema_examples, "invalid")
    valids = os.path.join(schema_examples, "valid")

    assert invalids
    assert valids

    invalid_recipes = os.listdir(invalids)
    valid_recipes = os.listdir(valids)

    assert invalid_recipes
    assert valid_recipes

    check_valid_recipes(valid_recipes, valids, loaded, version)
    check_invalid_recipes(invalid_recipes, invalids, loaded, version)
