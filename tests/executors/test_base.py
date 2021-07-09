"""
BuildExecutor: testing functions
"""

import os

from jsonschema.exceptions import ValidationError

from buildtest.buildsystem.builders import Builder
from buildtest.buildsystem.parser import BuildspecParser
from buildtest.config import SiteConfiguration
from buildtest.exceptions import BuildspecError, BuildTestError
from buildtest.executors.setup import BuildExecutor

pytest_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_build_executor(tmp_path):

    bc = SiteConfiguration()
    bc.detect_system()
    bc.validate()

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
            bp = BuildspecParser(buildspec, be)
        except (BuildTestError, BuildspecError, ValidationError):
            continue

        bp_filters = {"tags": None}
        builders = Builder(
            bp=bp,
            buildexecutor=be,
            configuration=bc,
            filters=bp_filters,
            testdir=tmp_path,
        )
        valid_builders = builders.get_builders()

        # build each test and then run it
        for builder in valid_builders:
            builder.build()
            be.run(builder)
            assert builder.metadata["result"]
