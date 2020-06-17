"""
BuildspecParser: testing functions
"""

import pytest
import os

from buildtest.buildsystem.base import BuildspecParser

testroot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_BuildspecParser(tmp_path):

    type_schemas = ["script", "compiler"]

    # Examples folder
    examples_dir = os.path.join(testroot, "examples", "buildspecs")

    # An empty path evaluated to be a directory should exit
    with pytest.raises(SystemExit):
        BuildspecParser("")

    # Passing 'None' will raise an error
    with pytest.raises(SystemExit):
        BuildspecParser(None)

    # A directory is not allowed either, this will raise an error.
    with pytest.raises(SystemExit):
        BuildspecParser(examples_dir)

    # Test loading Buildspec files
    for buildspec in os.listdir(examples_dir):
        buildspec = os.path.join(examples_dir, buildspec)
        bp = BuildspecParser(buildspec)

        # The lookup should have the base schema
        # {'script': {'1.0': 'script-v1.0.schema.json', 'latest': 'script-v1.0.schema.json'}}
        for supported_schema in type_schemas:

            assert supported_schema in bp.schema_table

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

            for k in ["testpath", "testroot", "rundir", "build_id"]:
                assert k in builder.metadata
