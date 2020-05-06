"""
BuildspecParser: testing functions
"""

import pytest
import os

from buildtest.buildsystem.base import BuildspecParser
from buildtest.defaults import supported_schemas

testroot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_BuildspecParser():

    # Examples folder
    examples_dir = os.path.join(testroot, "examples", "buildspecs")

    # An empty path evaluated to be a directory should exit
    with pytest.raises(SystemExit) as e_info:
        BuildspecParser("")

    # Passing 'None' will raise an error
    with pytest.raises(SystemExit) as e_info:
        BuildspecParser(None)

    # A directory is not allowed either, this will raise an error.
    with pytest.raises(SystemExit) as e_info:
        BuildspecParser(examples_dir)

    # Test loading Buildspec files
    for buildspec in os.listdir(examples_dir):
        buildspec = os.path.join(examples_dir, buildspec)
        bp = BuildspecParser(buildspec)

        # The lookup should have the base schema
        # {'script': {'0.0.1': 'script-v0.0.1.schema.json', 'latest': 'script-v0.0.1.schema.json'}}
        for supported_schema in supported_schemas:
            assert supported_schema in bp.lookup

        builders = bp.get_builders()

        for builder in builders:

            # Builders (on init) don't have metadata or build_id
            assert not builder.metadata
            assert not builder.build_id

            # Manually run prepare_run to define the above (this is usually handled by run)
            builder.prepare_run()
            for k in ["testpath", "testdir", "start_time"]:
                assert k in builder.metadata
            assert builder.build_id

            # If recipe had sections for pre_run, post_run, shell, they would be added here as well

            result = builder.run()
            for value in [
                "BUILD_ID",
                "START_TIME",
                "END_TIME",
                "RETURN_CODE",
                "LOGFILE",
            ]:
                assert value in result

            # Dry run should just print to screen
            result = builder.dry_run()
