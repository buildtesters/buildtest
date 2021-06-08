"""
BuildspecParser: testing functions
"""

import pytest
import os


from buildtest.buildsystem.builders import Builder
from buildtest.buildsystem.parser import BuildspecParser
from buildtest.config import SiteConfiguration
from buildtest.defaults import DEFAULT_SETTINGS_FILE
from buildtest.exceptions import BuildTestError, BuildspecError
from buildtest.executors.setup import BuildExecutor
from buildtest.utils.file import walk_tree

testroot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
here = os.path.dirname(os.path.abspath(__file__))


def test_BuildspecParser(tmp_path):
    config = SiteConfiguration(DEFAULT_SETTINGS_FILE)
    config.detect_system()
    config.validate()
    executors = BuildExecutor(config)

    # Invalid path to buildspec file should exit
    with pytest.raises(BuildTestError):
        BuildspecParser("", executors)

    # Passing 'None' will raise an error
    with pytest.raises(BuildTestError):
        BuildspecParser(None, executors)

    directory = os.path.join(here, "invalid_buildspecs")

    for buildspec in walk_tree(directory, ".yml"):
        buildspecfile = os.path.join(directory, buildspec)
        print("Processing buildspec: ", buildspecfile)
        with pytest.raises(BuildspecError):
            BuildspecParser(buildspecfile, executors)

    directory = os.path.join(here, "invalid_builds")
    # invalid builds for compiler schema tests. These tests will raise BuildTestError exception upon building
    # even though they are valid buildspecs.\
    for buildspec in walk_tree(directory, ".yml"):
        buildspecfile = os.path.join(directory, buildspec)
        print("Processing buildspec", buildspecfile)
        bp = BuildspecParser(buildspecfile, executors)

        with pytest.raises(BuildTestError):
            builder = Builder(
                bp=bp,
                buildexecutor=executors,
                configuration=config,
                filters=[],
                testdir=tmp_path,
            )
            builders = builder.get_builders()
            for test in builders:
                test.build()

    # Examples folder
    valid_buildspecs_directory = os.path.join(here, "valid_buildspecs")

    # A directory is not allowed either, this will raise an error.
    with pytest.raises(BuildTestError):
        BuildspecParser(valid_buildspecs_directory, executors)

    # Test loading Buildspec files
    for buildspec in walk_tree(valid_buildspecs_directory, ".yml"):
        buildspecfile = os.path.join(valid_buildspecs_directory, buildspec)
        bp = BuildspecParser(buildspecfile, executors)
        assert hasattr(bp, "recipe")
        assert hasattr(bp, "buildspec")
        assert hasattr(bp, "buildexecutors")

        filters = []

        builders = Builder(
            bp=bp,
            buildexecutor=executors,
            configuration=config,
            filters=filters,
            testdir=tmp_path,
        )
        builders = builders.get_builders()
        assert builders

        for builder in builders:

            # Builders (on init) set up metadata attribute
            assert hasattr(builder, "metadata")

            # Invoking build will build the test script
            # and write test
            builder.build()
