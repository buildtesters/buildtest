import os
import pytest
from buildtest.menu.build import BuildTest


def test_ascent():
    # ascent system has LMOD_SYSTEM_NAME set to "ascent" only run this test if this value is set
    if os.getenv("LMOD_SYSTEM_NAME") != "ascent":
        pytest.skip("Test runs only on ascent")

    here = os.path.dirname(os.path.abspath(__file__))
    ascent = os.path.join(here, "settings", "ascent.yml")

    buildspec_files = os.path.join(here, "examples", "cori_buildspecs", "hostname.yml")
    cmd = BuildTest(config_file=ascent, buildspec=[buildspec_files])
    cmd.build()
