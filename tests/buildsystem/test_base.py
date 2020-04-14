"""
BuildspecParser: testing functions
Copyright (c) 2020 Vanessa Sochat.
"""

import pytest
import os

from buildtest.buildsystem.base import BuildspecParser
from buildtest.defaults import supported_schemas

here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_load_configs():

    # Examples folder
    examples_dir = os.path.join(here, "testdir")

    # An empty path evaluated to be a directory should exit
    with pytest.raises(SystemExit) as e_info:
        BuildspecParser("")

    # Test loading config files
    for config_file in os.listdir(examples_dir):
        config_file = os.path.join(examples_dir, config_file)
        bp = BuildspecParser(config_file)

        # The lookup should have the base schema
        # {'script': {'0.0.1': 'script-v0.0.1.schema.json', 'latest': 'script-v0.0.1.schema.json'}}
        for supported_schema in supported_schemas:
            assert supported_schema in bp.lookup

        # The test configs (currently) each have two builders
        # [[builder-script-login_node_check], [builder-script-slurm_check]]
        builders = bp.get_builders()
        assert len(builders) == 2

        for builder in builders:

            # Builders (on init) don't have metadata or build_id
            assert not builder.metadata
            assert not builder.build_id

            # Manually run prepare_run to define the above (this is usually handled by run)
            builder.prepare_run()

            for key in ["shell"]:
                assert key in builder.metadata
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
