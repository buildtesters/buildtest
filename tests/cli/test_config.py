import os
import pytest
from buildtest.defaults import (
    DEFAULT_SETTINGS_SCHEMA,
    SCHEMA_ROOT,
    DEFAULT_SETTINGS_FILE,
)
from buildtest.cli.config import (
    view_configuration,
    validate_config,
    view_summary,
    view_executors,
    view_system,
)
from buildtest.config import check_settings
from buildtest.executors.setup import BuildExecutor
from buildtest.utils.file import walk_tree
from buildtest.schemas.defaults import custom_validator
from buildtest.schemas.utils import load_schema, load_recipe
from buildtest.system import BuildTestSystem

pytest_root = os.path.dirname(os.path.dirname(__file__))


@pytest.mark.cli
def test_config_systems():
    schema_files = os.path.join(
        SCHEMA_ROOT, "examples", "settings.schema.json", "valid"
    )
    # run 'buildtest config systems' against all valid configuration files
    for settings_file in os.listdir(schema_files):
        bc_file = os.path.join(schema_files, settings_file)
        view_system(settings_file=bc_file)


@pytest.mark.cli
def test_view_configuration():
    view_configuration()


def test_valid_config_schemas():

    valid_schema_dir = os.path.join(pytest_root, "examples", "config_schemas", "valid")
    schema_config = load_schema(DEFAULT_SETTINGS_SCHEMA)
    for schema in walk_tree(valid_schema_dir, ".yml"):
        example = load_recipe(os.path.abspath(schema))
        custom_validator(recipe=example, schema=schema_config)


@pytest.mark.cli
def test_config_validate():
    validate_config()


@pytest.mark.cli
def test_config_summary():
    system = BuildTestSystem()
    system.check()
    view_summary(system)


@pytest.mark.cli
def test_config_executors():
    configuration = check_settings(DEFAULT_SETTINGS_FILE)
    buildexecutor = BuildExecutor(configuration)

    # run buildtest config executors --json
    view_executors(buildexecutor=buildexecutor, json_format=True, yaml_format=False)

    # run buildtest config executors --yaml
    view_executors(buildexecutor=buildexecutor, json_format=False, yaml_format=True)

    # run buildtest config executors
    view_executors(buildexecutor=buildexecutor, json_format=False, yaml_format=False)
