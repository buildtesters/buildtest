import os
import socket

import pytest
from buildtest.cli.build import BuildTest
from buildtest.cli.compilers import BuildtestCompilers
from buildtest.config import SiteConfiguration
from buildtest.system import BuildTestSystem

hostname = socket.getfqdn()
here = os.path.dirname(os.path.abspath(__file__))


def test_ascent():
    # this test must run on Ascent system with domain '.ascent.olcf.ornl.gov' otherwise its skipped

    if not hostname.endswith("ascent.olcf.ornl.gov"):
        pytest.skip("This test must run on domain ascent.olcf.ornl.gov")

    settings_file = os.path.join(here, "settings", "ascent.yml")

    bc = SiteConfiguration(settings_file)
    bc.detect_system()
    bc.validate()

    system = BuildTestSystem()

    buildspec_files = os.path.join(here, "examples", "ascent", "hostname.yml")
    cmd = BuildTest(
        configuration=bc,
        buildspecs=[buildspec_files],
        buildtest_system=system,
        numprocs=[1, 2],
    )
    cmd.build()

    # This job will be held indefinitely but job will be cancelled by scheduler after 15sec once job pending time has reached max_pend_time
    buildspec_files = os.path.join(here, "examples", "ascent", "hold_job.yml")
    cmd = BuildTest(
        configuration=bc,
        buildspecs=[buildspec_files],
        buildtest_system=system,
        max_pend_time=15,
    )
    with pytest.raises(SystemExit):
        cmd.build()


def test_compilers_find_ascent():

    if not hostname.endswith("ascent.olcf.ornl.gov"):
        pytest.skip("This test must run on domain ascent.olcf.ornl.gov")

    settings_file = os.path.join(here, "settings", "ascent.yml")

    bc = SiteConfiguration(settings_file)
    bc.detect_system()
    bc.validate()

    # testing buildtest config compilers find
    bc = BuildtestCompilers(configuration=bc)
    bc.find_compilers()
