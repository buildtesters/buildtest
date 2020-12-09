"""
BuildspecParser: testing functions
"""

import pytest
import os

from buildtest.buildsystem.parser import BuildspecParser
from buildtest.buildsystem.builders import Builder
from buildtest.exceptions import BuildTestError

testroot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
here = os.path.dirname(os.path.abspath(__file__))


def test_BuildspecParser(tmp_path):

    # Invalid path to buildspec file should exit
    with pytest.raises(SystemExit):
        BuildspecParser("")

    # Passing 'None' will raise an error
    with pytest.raises(SystemExit):
        BuildspecParser(None)

    directory = os.path.join(here, "invalid_buildspecs")
    builders = []
    for buildspec in os.listdir(directory):
        buildspec = os.path.join(directory, buildspec)
        print("Processing buildspec: ", buildspec)
        with pytest.raises(SystemExit):
            BuildspecParser(buildspec)

    # Examples folder
    valid_buildspecs_directory = os.path.join(here, "valid_buildspecs")

    # A directory is not allowed either, this will raise an error.
    with pytest.raises(SystemExit):
        BuildspecParser(valid_buildspecs_directory)

    # Test loading Buildspec files
    for buildspec in os.listdir(valid_buildspecs_directory):
        buildspec = os.path.join(valid_buildspecs_directory, buildspec)
        bp = BuildspecParser(buildspec)
        assert bp.recipe
        assert bp.buildspec
        assert bp.executors

        filters = {"tags": None, "executors": None}

        builders = Builder(bp, filters=filters, testdir=tmp_path)
        builders = builders.get_builders()
        assert builders

        for builder in builders:

            # Builders (on init) don't have metadata or build_id
            assert builder.metadata

            # the following keys below are defined in metadata upon init
            for k in ["name", "buildspec", "recipe"]:
                assert k in builder.metadata

            # Invoking build will setup test metadata by adding few more keys to metadata
            # and write test
            builder.build()
            assert builder.metadata
