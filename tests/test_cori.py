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

settings_file = os.path.join(here, "settings", "cori.yml")

bc = SiteConfiguration(settings_file)
bc.detect_system()
bc.validate()

system = BuildTestSystem()
system.check()


def test_cori_burstbuffer():
    # This test must run on Cori Login nodes which are cori[01-20].nersc.gov.

    if not hostname.startswith("cori"):
        pytest.skip("This test runs on Cori Login nodes ('cori*')")

    cmd = BuildTest(
        configuration=bc,
        buildspecs=[
            os.path.join(
                os.getenv("BUILDTEST_ROOT"),
                "tests",
                "examples",
                "cori",
                "burstbuffer.yml",
            )
        ],
        buildtest_system=system,
        poll_interval=5,
        max_pend_time=30,
    )
    cmd.build()


def test_cori_slurm_hostname():

    if not hostname.startswith("cori"):
        pytest.skip("This test runs on Cori Login nodes ('cori*')")

    cmd = BuildTest(
        configuration=bc,
        buildspecs=[
            os.path.join(
                os.getenv("BUILDTEST_ROOT"), "tests", "examples", "cori", "hostname.yml"
            )
        ],
        buildtest_system=system,
        poll_interval=5,
        max_pend_time=30,
    )
    cmd.build()


def test_cori_slurm_max_pend():

    if not hostname.startswith("cori"):
        pytest.skip("This test runs on Cori Login nodes ('cori*')")

    cmd = BuildTest(
        configuration=bc,
        buildspecs=[
            os.path.join(
                os.getenv("BUILDTEST_ROOT"), "tests", "examples", "cori", "hold_job.yml"
            )
        ],
        buildtest_system=system,
        poll_interval=5,
        max_pend_time=10,
    )
    with pytest.raises(SystemExit):
        cmd.build()


def test_compiler_find_cori():

    if not hostname.startswith("cori"):
        pytest.skip("This test runs on Cori Login nodes ('cori*')")

    # testing buildtest config compilers find
    compilers = BuildtestCompilers(configuration=bc)
    compilers.find_compilers()
