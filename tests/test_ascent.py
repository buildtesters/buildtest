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

    ascent_examples_dir = os.path.join(here, "examples", "ascent")
    buildspec_files = [
        os.path.join(ascent_examples_dir, "hostname.yml"),
        os.path.join(ascent_examples_dir, "lsf_job_state.yml"),
    ]
    cmd = BuildTest(
        configuration=bc, buildspecs=[buildspec_files], buildtest_system=system
    )
    cmd.build()

    # This job will be held indefinitely but job will be cancelled by scheduler after 15sec once job pending time has reached maxpendtime
    buildspec_files = os.path.join(ascent_examples_dir, "hold_job.yml")
    cmd = BuildTest(
        configuration=bc,
        buildspecs=[buildspec_files],
        buildtest_system=system,
        maxpendtime=15,
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
