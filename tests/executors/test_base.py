"""
BuildExecutor: testing functions
"""

import os

from jsonschema.exceptions import ValidationError

from buildtest.buildsystem.builders import Builder
from buildtest.buildsystem.parser import BuildspecParser
from buildtest.cli.compilers import BuildtestCompilers
from buildtest.config import SiteConfiguration
from buildtest.exceptions import BuildspecError, BuildTestError
from buildtest.executors.setup import BuildExecutor
from buildtest.system import BuildTestSystem

pytest_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_build_executor(tmp_path):
    bc = SiteConfiguration()
    bc.detect_system()
    bc.validate()

    # Load BuildExecutor
    be = BuildExecutor(bc)

    system = BuildTestSystem()

    # ensure we have the following executors valid
    assert "generic.local.bash" in list(be.names())

    # Making sure all executors are created properly by inspecting their class attribute.
    # All executors have a class attribute 'type'
    for executor in be.executors.values():
        assert hasattr(executor, "type")

    examples_dir = os.path.join(pytest_root, "buildsystem", "valid_buildspecs")

    valid_builders = []

    buildtest_compilers = BuildtestCompilers(configuration=bc)
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
            buildtest_system=system,
            buildtest_compilers=buildtest_compilers,
        )
        valid_builders += builders.get_builders()
    # build each test and then run it
    for builder in valid_builders:
        builder.build()

    be.run(valid_builders)
