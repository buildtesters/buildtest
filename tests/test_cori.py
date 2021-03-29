import os
import pytest
import socket
from buildtest.menu.build import BuildTest


def test_cori():
    # This test must run on Cori Login nodes which are cori[01-20].nersc.gov.
    hostname = socket.getfqdn()
    if not hostname.startswith("cori"):
        pytest.skip("This test runs on Cori Login nodes ('cori*')")

    here = os.path.dirname(os.path.abspath(__file__))
    cori_configuration = os.path.join(here, "settings", "cori.yml")

    buildspec_files = walk_tree(
        os.path.join(os.getenv("BUILDTEST_ROOT"), "tests", "examples"), ".yml"
    )
    cmd = BuildTest(config_file=cori_configuration, buildspecs=[buildspec_files])
    cmd.build()
