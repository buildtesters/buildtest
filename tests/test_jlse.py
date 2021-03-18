import os
import pytest
import socket
from buildtest.menu.build import BuildTest

def test_jlse():
    hostname = socket.getfqdn()
    if not hostname.endswith("alcf.anl.gov"):
        pytest.skip("Test runs only on JLSE Login Nodes with domain name alcf.anl.gov")

    here = os.path.dirname(os.path.abspath(__file__))
    configuration = os.path.join(here, "settings", "jlse.yml")

    buildspec_files = os.path.join(here, "examples", "jlse", "hostname.yml")
    cmd = BuildTest(config_file=configuration, buildspecs=[buildspec_files])
    cmd.build()
