import os
import pytest
import random
import string


from buildtest.schemas.utils import load_schema, load_recipe

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.mark.utility
@pytest.mark.xfail(
    reason="Invalid File Extension for loading schema", raises=SystemExit
)
def test_load_schema_invalid_ext():

    # invalid file extension should fail
    load_schema(os.path.join(root, "README.rst"))


@pytest.mark.utility
@pytest.mark.xfail(reason="Invalid File Path when loading recipe", raises=SystemExit)
def test_load_recipe_invalid_path():

    invalid_file = "".join(random.choice(string.ascii_letters) for i in range(10))
    print(invalid_file, type(invalid_file))
    load_recipe(invalid_file)
