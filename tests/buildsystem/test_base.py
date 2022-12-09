"""
BuildspecParser: testing functions
"""

import os

import pytest
from buildtest.buildsystem.builders import Builder
from buildtest.buildsystem.parser import BuildspecParser
from buildtest.cli.compilers import BuildtestCompilers
from buildtest.config import SiteConfiguration
from buildtest.defaults import DEFAULT_SETTINGS_FILE
from buildtest.exceptions import (
    BuildTestError,
    InvalidBuildspec,
    InvalidBuildspecExecutor,
    InvalidBuildspecSchemaType,
)
from buildtest.executors.setup import BuildExecutor
from buildtest.system import BuildTestSystem
from buildtest.utils.file import walk_tree

testroot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
here = os.path.dirname(os.path.abspath(__file__))


def test_BuildspecParser(tmp_path):
    config = SiteConfiguration(DEFAULT_SETTINGS_FILE)
    config.detect_system()
    config.validate()
    executors = BuildExecutor(config)

    system = BuildTestSystem()

    # Invalid path to buildspec file should exit
    with pytest.raises(InvalidBuildspec):
        BuildspecParser(buildspec="", buildexecutor=executors)

    # Passing 'None' will raise an error
    with pytest.raises(InvalidBuildspec):
        BuildspecParser(buildspec=None, buildexecutor=executors)

    directory = os.path.join(here, "invalid_buildspecs")
    fnames = [
        os.path.join(directory, "invalid_type.yml"),
        os.path.join(directory, "missing_type.yml"),
    ]
    # Testing buildspecs with invalid schema type
    for buildspec in fnames:
        print("Processing buildspec: ", buildspec)
        with pytest.raises(InvalidBuildspecSchemaType):
            BuildspecParser(buildspec, executors)

    # Testing buildspecs with invalid executor
    with pytest.raises(InvalidBuildspecExecutor):
        BuildspecParser(
            buildspec=os.path.join(directory, "invalid_executor.yml"),
            buildexecutor=executors,
        )

    with pytest.raises(InvalidBuildspecExecutor):
        BuildspecParser(
            buildspec=os.path.join(directory, "missing_executor.yml"),
            buildexecutor=executors,
        )

    directory = os.path.join(here, "invalid_builds")
    # invalid builds for compiler schema tests. These tests will raise BuildTestError exception upon building
    # even though they are valid buildspecs.\
    bc = BuildtestCompilers(configuration=config)
    for buildspec in walk_tree(directory, ".yml"):
        buildspecfile = os.path.join(directory, buildspec)
        print("Processing buildspec", buildspecfile)
        bp = BuildspecParser(buildspecfile, executors)

        with pytest.raises(BuildTestError):
            builder = Builder(
                bp=bp,
                buildtest_compilers=bc,
                buildexecutor=executors,
                configuration=config,
                filters=[],
                testdir=tmp_path,
                buildtest_system=system,
            )
            builders = builder.get_builders()
            for test in builders:
                test.build()

    # Examples folder
    valid_buildspecs_directory = os.path.join(here, "valid_buildspecs")

    # A directory is not allowed either, this will raise an error.
    with pytest.raises(InvalidBuildspec):
        BuildspecParser(buildspec=valid_buildspecs_directory, buildexecutor=executors)

    # Test loading Buildspec files
    for buildspec in walk_tree(valid_buildspecs_directory, ".yml"):
        buildspecfile = os.path.join(valid_buildspecs_directory, buildspec)
        bp = BuildspecParser(buildspec=buildspecfile, buildexecutor=executors)
        assert hasattr(bp, "recipe")
        assert hasattr(bp, "buildspec")
        assert hasattr(bp, "buildexecutors")

        filters = []

        builders = Builder(
            bp=bp,
            buildtest_compilers=bc,
            buildexecutor=executors,
            configuration=config,
            filters=filters,
            testdir=tmp_path,
            buildtest_system=system,
        )
        builders = builders.get_builders()
        assert builders

        for builder in builders:

            # Builders (on init) set up metadata attribute
            assert hasattr(builder, "metadata")

            # Invoking build will build the test script
            # and write test
            builder.build()
