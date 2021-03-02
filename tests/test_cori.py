import os
import pytest
from buildtest.config import BuildTestCommand


def test_cori():

    if os.getenv("NERSC_HOST") != "cori":
        pytest.skip("Test runs only on Cori")

    here = os.path.dirname(os.path.abspath(__file__))
    cori_configuration = os.path.join(here, "settings", "cori.config.yml")

    buildspec_files = os.path.join(here, "examples", "cori_buildspecs", "hostname.yml")
    cmd = BuildTestCommand(config_file=cori_configuration, buildspec=[buildspec_files])
    cmd.build()
