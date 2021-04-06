import os
import pytest
import socket
from buildtest.cli.build import BuildTest
from buildtest.cli.compilers import BuildtestCompilers


def test_jlse():
    hostname = socket.getfqdn()
    if not hostname.endswith("alcf.anl.gov"):
        pytest.skip("Test runs only on JLSE Login Nodes with domain name alcf.anl.gov")

    here = os.path.dirname(os.path.abspath(__file__))
    configuration = os.path.join(here, "settings", "jlse.yml")

    buildspec_files = os.path.join(here, "examples", "jlse", "hostname.yml")
    cmd = BuildTest(config_file=configuration, buildspecs=[buildspec_files])
    cmd.build()

    # testing buildtest config compilers find
    bc = BuildtestCompilers(settings_file=configuration)
    bc.find_compilers()
