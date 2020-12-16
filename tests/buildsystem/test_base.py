"""
BuildspecParser: testing functions
"""

import pytest
import os


from buildtest.buildsystem.builders import Builder
from buildtest.buildsystem.parser import BuildspecParser
from buildtest.exceptions import BuildTestError
from buildtest.utils.file import walk_tree

testroot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
here = os.path.dirname(os.path.abspath(__file__))


def test_BuildspecParser(tmp_path):

    # Invalid path to buildspec file should exit
    with pytest.raises(BuildTestError):
        BuildspecParser("")

    # Passing 'None' will raise an error
    with pytest.raises(BuildTestError):
        BuildspecParser(None)

    directory = os.path.join(here, "invalid_buildspecs")
    builders = []
    for buildspec in walk_tree(directory, ".yml"):
        buildspecfile = os.path.join(directory, buildspec)
        print("Processing buildspec: ", buildspecfile)
        with pytest.raises(BuildTestError):
            BuildspecParser(buildspecfile)

    # Examples folder
    valid_buildspecs_directory = os.path.join(here, "valid_buildspecs")

    # A directory is not allowed either, this will raise an error.
    with pytest.raises(BuildTestError):
        BuildspecParser(valid_buildspecs_directory)

    # Test loading Buildspec files
    for buildspec in walk_tree(valid_buildspecs_directory, ".yml"):
        buildspecfile = os.path.join(valid_buildspecs_directory, buildspec)
        bp = BuildspecParser(buildspecfile)
        assert bp.recipe
        assert bp.buildspec
        assert bp.executors

        filters = {"tags": None, "executors": None}

        builders = Builder(bp, filters=filters, testdir=tmp_path)
        builders = builders.get_builders()
        assert builders

        for builder in builders:

            # Builders (on init) set up metadata attribute
            assert builder.metadata

            # Invoking build will build the test script
            # and write test
            builder.build()
