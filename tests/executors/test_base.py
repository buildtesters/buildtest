"""
BuildExecutor: testing functions
"""

import os

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from buildtest.executors.base import BuildExecutor
from buildtest.schemas.utils import load_schema
from buildtest.defaults import DEFAULT_SETTINGS_SCHEMA
from buildtest.buildsystem.base import BuildspecParser

pytest_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_build_executor(tmp_path):
    example_schema = os.path.join(
        pytest_root, "examples", "config_schemas", "valid", "combined-example.yml"
    )
    settings_schema = load_schema(DEFAULT_SETTINGS_SCHEMA)
    example = load_schema(example_schema)
    validate(instance=example, schema=settings_schema)

    # Load BuildExecutor
    be = BuildExecutor(example)
    # We should have a total of 5 executors, 3 local, 1 ssh, 1 slurm executor
    assert len(be.executors) == 5
    assert list(be.executors.keys()) == [
        "local.bash",
        "local.sh",
        "local.python",
        "ssh.localhost",
        "slurm.haswell",
    ]

    # Each should have
    for name, executor in be.executors.items():
        assert hasattr(executor, "_settings")

    examples_dir = os.path.join(pytest_root, "examples", "buildspecs")
    for buildspec in os.listdir(examples_dir):
        buildspec = os.path.join(examples_dir, buildspec)
        try:
            bp = BuildspecParser(buildspec)
        except (SystemExit, ValidationError):
            continue

        builders = bp.get_builders(tmp_path)
        print(builders)
        # build each test and then run it
        for builder in builders:
            builder.build()
            result = be.run(builder)
            assert result
