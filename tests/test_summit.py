import os
import socket

import pytest

from buildtest.cli.build import BuildTest
from buildtest.cli.buildspec import BuildspecCache
from buildtest.cli.compilers import BuildtestCompilers, compiler_test
from buildtest.config import SiteConfiguration

hostname = socket.getfqdn()
here = os.path.dirname(os.path.abspath(__file__))

settings_file = os.path.join(here, "settings", "summit.yml")


def test_summit():
    # this test must run on Ascent system with domain '.summit.olcf.ornl.gov' otherwise its skipped

    if not hostname.endswith("summit.olcf.ornl.gov"):
        pytest.skip("This test must run on domain summit.olcf.ornl.gov")

    bc = SiteConfiguration(settings_file)
    bc.detect_system()
    bc.validate(moduletool="lmod")
    BuildspecCache(rebuild=True, configuration=bc)

    examples_dir = os.path.join(here, "examples", "summit")
    buildspec_files = [
        os.path.join(examples_dir, "hostname.yml"),
        os.path.join(examples_dir, "lsf_job_state.yml"),
    ]
    cmd = BuildTest(configuration=bc, buildspecs=buildspec_files, poll_interval=10)
    cmd.build()

    # This job will be held indefinitely but job will be cancelled by scheduler after 15sec once job pending time has reached maxpendtime
    buildspec_files = [os.path.join(examples_dir, "hold_job.yml")]
    cmd = BuildTest(configuration=bc, buildspecs=buildspec_files, maxpendtime=15)
    with pytest.raises(SystemExit):
        cmd.build()


def test_compilers_find_ascent():
    if not hostname.endswith("summit.olcf.ornl.gov"):
        pytest.skip("This test must run on domain summit.olcf.ornl.gov")

    config = SiteConfiguration(settings_file)
    config.detect_system()
    config.validate(moduletool="lmod")

    # testing buildtest config compilers find
    bc = BuildtestCompilers(configuration=config)
    bc.find_compilers()

    # test all compilers
    compiler_test(configuration=config)

    # test specific compiler
    compiler_test(configuration=config, compiler_names=["gcc/9.1.0"])
