import os
import pytest
from buildtest.menu.build import BuildTest
from buildtest.utils.command import BuildTestCommand


def test_ascent():
    # this test must run on Ascent system with domain '.ascent.olcf.ornl.gov' otherwise its skipped
    cmd = BuildTestCommand("hostname -f")
    cmd.execute()
    hostname = " ".join(cmd.get_output())
    if not hostname.endswith("ascent.olcf.ornl.gov"):
        pytest.skip("This test must run on domain ascent.olcf.ornl.gov")

    here = os.path.dirname(os.path.abspath(__file__))
    ascent = os.path.join(here, "settings", "ascent.yml")

    buildspec_files = os.path.join(here, "examples", "ascent", "hostname.yml")
    cmd = BuildTest(config_file=ascent, buildspecs=[buildspec_files])
    cmd.build()
