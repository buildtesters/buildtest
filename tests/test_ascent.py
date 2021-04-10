import os
import pytest
import socket
from buildtest.cli.build import BuildTest
from buildtest.cli.compilers import BuildtestCompilers
from buildtest.system import BuildTestSystem


def test_ascent():
    # this test must run on Ascent system with domain '.ascent.olcf.ornl.gov' otherwise its skipped

    hostname = socket.getfqdn()
    if not hostname.endswith("ascent.olcf.ornl.gov"):
        pytest.skip("This test must run on domain ascent.olcf.ornl.gov")

    here = os.path.dirname(os.path.abspath(__file__))
    settings_file = os.path.join(here, "settings", "ascent.yml")
    system = BuildTestSystem()
    system.check()

    buildspec_files = os.path.join(here, "examples", "ascent", "hostname.yml")
    cmd = BuildTest(
        config_file=settings_file, buildspecs=[buildspec_files], buildtest_system=system
    )
    cmd.build()

    # testing buildtest config compilers find
    bc = BuildtestCompilers(settings_file=settings_file)
    bc.find_compilers()
