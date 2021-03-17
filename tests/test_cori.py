import os
import pytest
from buildtest.menu.build import BuildTest
from buildtest.utils.command import BuildTestCommand

def test_cori():
    # This test must run on Cori Login nodes which are cori[01-20].nersc.gov.
    hostname = " ".join(BuildTestCommand("hostname -f").get_output())

    if not hostname.endswith("nersc.gov") or not hostname.startswith("cori"):
        pytest.skip(
            "This test runs only on domain 'nersc.gov' with machine names that start with 'cori*'"
        )

    here = os.path.dirname(os.path.abspath(__file__))
    cori_configuration = os.path.join(here, "settings", "cori.yml")

    buildspec_files = os.path.join(here, "examples", "cori", "hostname.yml")
    cmd = BuildTest(config_file=cori_configuration, buildspecs=[buildspec_files])
    cmd.build()
