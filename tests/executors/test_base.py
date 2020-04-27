"""
BuildExecutor: testing functions
"""

import pytest
import os

from jsonschema import validate
from buildtest.executors.base import BuildExecutor
from buildtest.buildsystem.schemas.utils import load_schema
from buildtest.defaults import DEFAULT_SETTINGS_SCHEMA

pytest_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_build_executor():
    example_schema = os.path.join(
        pytest_root, "examples", "config_schemas", "valid", "combined-example.yml"
    )
    settings_schema = load_schema(DEFAULT_SETTINGS_SCHEMA)
    example = load_schema(example_schema)
    validate(instance=example, schema=settings_schema)

    # Load BuildExecutor
    be = BuildExecutor(example)

    # We should have loaded a local and slurm executor, and one defualt
    # {'local': [executor-local-local], 'slurm': [executor-slurm-slurm]}
    assert len(be.executors) == 3

    # Each should have
    for name, executor in be.executors.items():
        assert hasattr(executor, "_settings")

        if name == "slurm":
            assert executor.launcher == "srun"
