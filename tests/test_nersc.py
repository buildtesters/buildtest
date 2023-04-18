import os
import socket
import tempfile

import pytest
from buildtest.cli.build import BuildTest
from buildtest.cli.buildspec import BuildspecCache
from buildtest.cli.compilers import BuildtestCompilers, compiler_find, compiler_test
from buildtest.config import SiteConfiguration
from buildtest.defaults import BUILDTEST_ROOT
from buildtest.system import BuildTestSystem


class TestNersc:
    hostname = socket.getfqdn()
    here = os.path.dirname(os.path.abspath(__file__))

    if not hostname.startswith("login"):
        pytest.skip("This test runs on Perlmutter Login nodes ('login*')")

    settings_file = os.path.join(here, "settings", "nersc.yml")

    system = BuildTestSystem()

    bc = SiteConfiguration(settings_file)
    bc.detect_system()
    bc.validate(moduletool="lmod")
    BuildspecCache(rebuild=True, configuration=bc)

    def test_slurm_hostname(self):
        cmd = BuildTest(
            configuration=self.bc,
            buildspecs=[
                os.path.join(
                    BUILDTEST_ROOT, "tests", "examples", "perlmutter", "hostname.yml"
                )
            ],
            buildtest_system=self.system,
            poll_interval=5,
            maxpendtime=120,
            numprocs=[1, 4],
        )
        cmd.build()

    def test_slurm_max_pend(self):
        cmd = BuildTest(
            configuration=self.bc,
            buildspecs=[
                os.path.join(
                    os.getenv("BUILDTEST_ROOT"),
                    "tests",
                    "examples",
                    "perlmutter",
                    "hold_job.yml",
                )
            ],
            buildtest_system=self.system,
            poll_interval=5,
            maxpendtime=10,
        )
        with pytest.raises(SystemExit):
            cmd.build()

    def test_compiler_find(self):
        # testing buildtest config compilers find
        compilers = BuildtestCompilers(configuration=self.bc)
        compilers.find_compilers()

        # test entry point for 'buildtest config compilers find --detailed'
        compiler_find(configuration=self.bc, detailed=True)

    def test_compiler_test(self):
        # testing buildtest config compilers test
        compiler_test(configuration=self.bc)

    def test_compiler_find_alternative_filepath(self):
        # testing buildtest config compilers find
        compilers = BuildtestCompilers(configuration=self.bc)
        compilers.find_compilers()

        # test entry point for 'buildtest config compilers find --file'
        temp_path = tempfile.NamedTemporaryFile(dir=os.path.expanduser("~"))
        compiler_find(configuration=self.bc, filepath=temp_path.name)
        temp_path.close()
