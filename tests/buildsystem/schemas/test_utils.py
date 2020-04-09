import os
import pytest
import uuid

from buildtest.buildsystem.schemas.utils import load_schema, load_recipe

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.mark.xfail(
    reason="Invalid File Extension for loading schema", raises=SystemExit
)
def test_load_schema_invalid_ext():

    # invalid file extension should fail
    load_schema(os.path.join(root, "README.rst"))


@pytest.mark.xfail(reason="Invalid File Path when loading recipe", raises=SystemExit)
def test_load_recipe_invalid_path():
    invalid_file = str(uuid.uuid4())
    load_recipe(invalid_file)
