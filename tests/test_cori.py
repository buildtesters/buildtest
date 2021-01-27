import os
import pytest
from buildtest.config import check_settings
from buildtest.menu.build import func_build_subcmd


def test_cori():

    if os.getenv("NERSC_HOST") != "cori":
        pytest.skip("Test runs only on Cori")

    here = os.path.dirname(os.path.abspath(__file__))
    cori_configuration = os.path.join(here, "settings", "cori.config.yml")
    settings = check_settings(cori_configuration, retrieve_settings=True)

    buildspec_files = os.path.join(here, "examples", "cori_buildspecs", "hostname.yml")

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

    #  test job submission on Cori
    func_build_subcmd(args, settings)
