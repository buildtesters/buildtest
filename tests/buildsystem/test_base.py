"""
BuildspecParser: testing functions
"""

import pytest
import os

from buildtest.buildsystem.parser import BuildspecParser

testroot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
here = os.path.dirname(os.path.abspath(__file__))


def test_BuildspecParser(tmp_path):

    # Examples folder
    valid_buildspecs_directory = os.path.join(here, "valid_buildspecs")
    # Invalid path to buildspec file should exit
    with pytest.raises(SystemExit):
        BuildspecParser("")

    # Passing 'None' will raise an error
    with pytest.raises(SystemExit):
        BuildspecParser(None)

    # A directory is not allowed either, this will raise an error.
    with pytest.raises(SystemExit):
        BuildspecParser(valid_buildspecs_directory)

    invalid_buildspecs_directory = os.path.join(here, "invalid_buildspecs")
    for buildspec in os.listdir(invalid_buildspecs_directory):
        buildspec = os.path.join(invalid_buildspecs_directory, buildspec)
        print("Processing buildspec: ", buildspec)
        with pytest.raises(SystemExit):
            BuildspecParser(buildspec)

    # Test loading Buildspec files
    for buildspec in os.listdir(valid_buildspecs_directory):
        buildspec = os.path.join(valid_buildspecs_directory, buildspec)
        bp = BuildspecParser(buildspec)

        builders = bp.get_builders(tmp_path)

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
