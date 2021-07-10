import os
import shutil

import pytest
from buildtest.cli.build import BuildTest
from buildtest.config import SiteConfiguration
from buildtest.system import BuildTestSystem
from buildtest.utils.file import walk_tree


def test_pbs():

    """Need to figure out a PBS environment where to run this regression test."""
    if not shutil.which("pbsnodes"):
        pytest.skip("Test runs only on PBS Cluster, must have pbsnodes command")

    here = os.path.dirname(os.path.abspath(__file__))
    settings_file = os.path.join(here, "settings", "pbs.yml")
    system = BuildTestSystem()
    system.check()

    bc = SiteConfiguration(settings_file)
    bc.detect_system()
    bc.validate()

    buildspec_files = walk_tree(os.path.join(here, "examples", "pbs"))

    cmd = BuildTest(
        configuration=bc, buildspecs=buildspec_files, buildtest_system=system
    )
    cmd.build()
