import os
from jsonschema import validate
from buildtest.defaults import DEFAULT_SETTINGS_SCHEMA, BUILDTEST_SETTINGS_FILE
from buildtest.menu.config import (
    func_config_view,
    func_config_reset,
    func_config_validate
)
from buildtest.utils.file import walk_tree
from buildtest.buildsystem.schemas.utils import load_schema

pytest_root = os.path.dirname(os.path.dirname(__file__))


def test_view_configuration():
    func_config_view()


def test_config_reset():

    # removing config file and testing if reset works
    os.remove(BUILDTEST_SETTINGS_FILE)
    func_config_reset()
    assert os.path.exists(BUILDTEST_SETTINGS_FILE)


def test_valid_config_schemas():

    valid_schema_dir = os.path.join(pytest_root, "examples", "config_schemas", "valid")
    schema_config = load_schema(DEFAULT_SETTINGS_SCHEMA)
    for schema in walk_tree(valid_schema_dir, ".yml"):
        example = load_schema(os.path.abspath(schema))
        validate(instance=example, schema=schema_config)

def test_config_validate():

    func_config_validate()