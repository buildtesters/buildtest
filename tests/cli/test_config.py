import os

import pytest
from buildtest.cli.config import (
    validate_config,
    view_configuration,
    view_executors,
    view_summary,
    view_system,
)
from buildtest.config import SiteConfiguration
from buildtest.defaults import DEFAULT_SETTINGS_SCHEMA, SCHEMA_ROOT
from buildtest.executors.setup import BuildExecutor
from buildtest.schemas.defaults import custom_validator
from buildtest.schemas.utils import load_recipe, load_schema
from buildtest.system import BuildTestSystem
from buildtest.utils.file import walk_tree

pytest_root = os.path.dirname(os.path.dirname(__file__))

configuration = SiteConfiguration()
configuration.detect_system()
configuration.validate()


@pytest.mark.cli
def test_config_systems():

    schema_files = os.path.join(
        SCHEMA_ROOT, "examples", "settings.schema.json", "valid"
    )
    # run 'buildtest config systems' against all valid configuration files
    for config_examples in os.listdir(schema_files):
        fname = os.path.join(schema_files, config_examples)
        configuration = SiteConfiguration(fname)
        view_system(configuration)


@pytest.mark.cli
def test_view_configuration():
    view_configuration(configuration)


def test_valid_config_schemas():

    valid_schema_dir = os.path.join(pytest_root, "examples", "config_schemas", "valid")
    schema_config = load_schema(DEFAULT_SETTINGS_SCHEMA)
    for schema in walk_tree(valid_schema_dir, ".yml"):
        example = load_recipe(os.path.abspath(schema))
        custom_validator(recipe=example, schema=schema_config)


@pytest.mark.cli
def test_config_validate():
    validate_config(configuration)


@pytest.mark.cli
def test_config_summary():
    system = BuildTestSystem()
    system.check()
    view_summary(configuration=configuration, buildtestsystem=system)


@pytest.mark.cli
def test_config_executors():
    buildexecutor = BuildExecutor(configuration)

    # run buildtest config executors --json
    view_executors(
        configuration=configuration,
        buildexecutor=buildexecutor,
        json_format=True,
        yaml_format=False,
    )

    # run buildtest config executors --yaml
    view_executors(
        configuration=configuration,
        buildexecutor=buildexecutor,
        json_format=False,
        yaml_format=True,
    )

    # run buildtest config executors
    view_executors(
        configuration=configuration,
        buildexecutor=buildexecutor,
        json_format=False,
        yaml_format=False,
    )
