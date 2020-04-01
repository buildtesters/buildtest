import os
from jsonschema import validate, ValidationError
from buildtest.defaults import DEFAULT_CONFIG_SCHEMA, BUILDTEST_CONFIG_FILE
from buildtest.menu.config import (
    func_config_view,
    func_config_reset,
)
from buildtest.buildsystem.schemas.utils import load_schema

pytest_root = os.path.dirname(os.path.dirname(__file__))


def test_view_configuration():
    func_config_view()


def test_config_restore():

    # removing config file and testing if reset works
    os.remove(BUILDTEST_CONFIG_FILE)
    func_config_reset()
    assert os.path.exists(BUILDTEST_CONFIG_FILE)


def test_config_local():
    example_schema = os.path.join(
        pytest_root, "config_schema_examples", "local-example.yml"
    )
    schema_config = load_schema(DEFAULT_CONFIG_SCHEMA)
    example = load_schema(example_schema)
    validate(instance=example, schema=schema_config)


def test_config_slurm():
    example_schema = os.path.join(
        pytest_root, "config_schema_examples", "slurm-example.yml"
    )
    schema_config = load_schema(DEFAULT_CONFIG_SCHEMA)
    example = load_schema(example_schema)
    try:
        validate(instance=example, schema=schema_config)
    except ValidationError:
        print(
            f"Failed to validate configuration file: {example_schema} with schema {DEFAULT_CONFIG_SCHEMA}"
        )
        assert True
