import os
import socket

import pytest
from buildtest.cli.build import BuildTest
from buildtest.cli.compilers import BuildtestCompilers
from buildtest.config import SiteConfiguration
from buildtest.system import BuildTestSystem
from buildtest.utils.file import walk_tree

hostname = socket.getfqdn()
here = os.path.dirname(os.path.abspath(__file__))


def test_cori():
    # This test must run on Cori Login nodes which are cori[01-20].nersc.gov.

    if not hostname.startswith("cori"):
        pytest.skip("This test runs on Cori Login nodes ('cori*')")

    settings_file = os.path.join(here, "settings", "cori.yml")

    buildspec_files = walk_tree(
        os.path.join(os.getenv("BUILDTEST_ROOT"), "tests", "examples", "cori"), ".yml"
    )

    bc = SiteConfiguration(settings_file)
    bc.detect_system()
    bc.validate()

    system = BuildTestSystem()
    system.check()
    cmd = BuildTest(
        configuration=bc, buildspecs=buildspec_files, buildtest_system=system
    )
    cmd.build()


def test_compiler_find_cori():

    if not hostname.startswith("cori"):
        pytest.skip("This test runs on Cori Login nodes ('cori*')")

    settings_file = os.path.join(here, "settings", "cori.yml")
    bc = SiteConfiguration(settings_file)
    bc.detect_system()
    bc.validate()

    # testing buildtest config compilers find
    bc = BuildtestCompilers(configuration=bc)
    bc.find_compilers()
