"""
BuildExecutor: testing functions
"""

import os

from jsonschema.exceptions import ValidationError

from buildtest.buildsystem.builders import Builder
from buildtest.buildsystem.parser import BuildspecParser
from buildtest.config import BuildtestConfiguration
from buildtest.defaults import DEFAULT_SETTINGS_SCHEMA, DEFAULT_SETTINGS_FILE
from buildtest.executors.setup import BuildExecutor
from buildtest.schemas.defaults import custom_validator
from buildtest.schemas.utils import load_schema, load_recipe


pytest_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_build_executor(tmp_path):

    bc = BuildtestConfiguration(DEFAULT_SETTINGS_FILE)

    # Load BuildExecutor
    be = BuildExecutor(bc)
    # We should have a total of 5 executors (local.bash, local.sh, local.csh, local.zsh, local.python)
    assert len(be.executors) == 5
    assert list(be.executors.keys()) == [
        "generic.local.bash",
        "generic.local.sh",
        "generic.local.csh",
        "generic.local.zsh",
        "generic.local.python",
    ]

    # Making sure all executors are created properly by inspecting their class attribute.
    # All executors have a class attribute 'type'
    for name, executor in be.executors.items():
        assert hasattr(executor, "type")

    examples_dir = os.path.join(pytest_root, "buildsystem", "valid_buildspecs")
    for buildspec in os.listdir(examples_dir):
        buildspec = os.path.join(examples_dir, buildspec)
        try:
            bp = BuildspecParser(buildspec)
        except (SystemExit, ValidationError):
            continue

        bp_filters = {"tags": None}
        builders = Builder(bp=bp, filters=bp_filters, testdir=tmp_path)
        valid_builders = builders.get_builders()

        # build each test and then run it
        for builder in valid_builders:
            builder.build()
            be.run(builder)
            assert builder.metadata["result"]
