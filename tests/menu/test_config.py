import os
import pytest
from buildtest.defaults import DEFAULT_SETTINGS_SCHEMA, SCHEMA_ROOT
from buildtest.menu.config import (
    func_config_view,
    func_config_validate,
    func_config_summary,
    func_config_executors,
    func_config_system
)
from buildtest.utils.file import walk_tree
from buildtest.schemas.defaults import custom_validator
from buildtest.schemas.utils import load_schema, load_recipe

pytest_root = os.path.dirname(os.path.dirname(__file__))


@pytest.mark.cli
def test_config_systems():
    schema_files = os.path.join(SCHEMA_ROOT, "examples", "settings.schema.json", "valid")
    # run 'buildtest config systems' against all valid configuration files
    for settings_file in os.listdir(schema_files):
        bc_file = os.path.join(schema_files, settings_file)
        func_config_system(settings_file=bc_file)

@pytest.mark.cli
def test_view_configuration():
    func_config_view()


def test_valid_config_schemas():

    valid_schema_dir = os.path.join(pytest_root, "examples", "config_schemas", "valid")
    schema_config = load_schema(DEFAULT_SETTINGS_SCHEMA)
    for schema in walk_tree(valid_schema_dir, ".yml"):
        example = load_recipe(os.path.abspath(schema))
        custom_validator(recipe=example, schema=schema_config)


@pytest.mark.cli
def test_config_validate():

    func_config_validate()


@pytest.mark.cli
def test_config_summary():

    func_config_summary()


@pytest.mark.cli
def test_config_executors():
    class args:
        json = True

    # run buildtest config executors --json
    func_config_executors(args)

    class args:
        json = False

    # run buildtest config executors
    func_config_executors(args)
