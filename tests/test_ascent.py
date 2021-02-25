import os
import pytest
from buildtest.config import check_settings
from buildtest.menu.build import func_build_subcmd


def test_ascent():
    # ascent system has LMOD_SYSTEM_NAME set to "ascent" only run this test if this value is set
    if os.getenv("LMOD_SYSTEM_NAME") != "ascent":
        pytest.skip("Test runs only on ascent")

    here = os.path.dirname(os.path.abspath(__file__))
    ascent = os.path.join(here, "settings", "ascent.yml")
    settings = check_settings(ascent, retrieve_settings=True)

    buildspec_files = os.path.join(here, "examples", "ascent", "hostname.yml")

    class args:
        buildspec = [buildspec_files]
        debug = False
        stage = None
        testdir = None
        exclude = None
        tags = None
        executor = None
        filter_tags = None
        rebuild = None

    #  test job submission on Ascent
    func_build_subcmd(args, settings)
