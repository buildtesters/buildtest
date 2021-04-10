import os
import pytest
import socket
from buildtest.cli.build import BuildTest
from buildtest.cli.compilers import BuildtestCompilers
from buildtest.system import BuildTestSystem
from buildtest.utils.file import walk_tree


def test_cori():
    # This test must run on Cori Login nodes which are cori[01-20].nersc.gov.
    hostname = socket.getfqdn()
    if not hostname.startswith("cori"):
        pytest.skip("This test runs on Cori Login nodes ('cori*')")
    here = os.path.dirname(os.path.abspath(__file__))
    settings_file = os.path.join(here, "settings", "cori.yml")

    buildspec_files = walk_tree(
        os.path.join(os.getenv("BUILDTEST_ROOT"), "tests", "examples", "cori"), ".yml"
    )

    system = BuildTestSystem()
    system.check()
    cmd = BuildTest(
        config_file=settings_file, buildspecs=buildspec_files, buildtest_system=system
    )
    cmd.build()

    # testing buildtest config compilers find
    bc = BuildtestCompilers(settings_file=settings_file)
    bc.find_compilers()
