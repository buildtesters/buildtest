import os
import tempfile

import pytest

from buildtest.schemas.utils import load_recipe, load_schema

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.mark.utility
@pytest.mark.xfail(
    reason="Invalid File Extension for loading schema", raises=SystemExit
)
def test_load_schema_invalid_ext():

    # invalid file extension should fail
    load_schema(os.path.join(root, "README.rst"))


@pytest.mark.utility
@pytest.mark.xfail(reason="Invalid File Path for loading schema", raises=SystemExit)
def test_load_schema_invalid_path():
    fp = tempfile.NamedTemporaryFile()
    assert os.path.exists(fp.name)
    fp.close()

    print(f"Loading Schema from file: {fp.name}")
    # tempfile will remove file upon closing file stream so we expect load_schema to raise error when we have invalid file
    load_schema(fp.name)


@pytest.mark.utility
@pytest.mark.xfail(reason="Invalid File Path when loading recipe", raises=SystemExit)
def test_load_recipe_invalid_path():

    fp = tempfile.NamedTemporaryFile()
    assert os.path.exists(fp.name)
    fp.close()

    print(f"Loading YAML recipe from file: {fp.name}")

    load_recipe(fp.name)


@pytest.mark.utility
@pytest.mark.xfail(reason="YAML File must end in  .yml extension", raises=SystemExit)
def test_load_recipe_extension():
    load_recipe(os.path.join(root, "README.rst"))
