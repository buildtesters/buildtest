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

hostname = socket.getfqdn()
here = os.path.dirname(os.path.abspath(__file__))

settings_file = os.path.join(here, "settings", "nersc.yml")


def test_cori_burstbuffer():
    # This test must run on Cori Login nodes which are cori[01-20].nersc.gov.

    if not hostname.startswith("cori"):
        pytest.skip("This test runs on Cori Login nodes ('cori*')")

    system = BuildTestSystem()

    bc = SiteConfiguration(settings_file)
    bc.detect_system()
    bc.validate(moduletool="environment-modules")
    BuildspecCache(rebuild=True, configuration=bc)
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
        stage="build",
    )
    cmd.build()


def test_cori_slurm_hostname():
    if not hostname.startswith("cori"):
        pytest.skip("This test runs on Cori Login nodes ('cori*')")

    system = BuildTestSystem()

    bc = SiteConfiguration(settings_file)
    bc.detect_system()
    bc.validate(moduletool="environment-modules")

    cmd = BuildTest(
        configuration=bc,
        buildspecs=[
            os.path.join(BUILDTEST_ROOT, "tests", "examples", "cori", "hostname.yml")
        ],
        buildtest_system=system,
        poll_interval=5,
        maxpendtime=120,
        numprocs=[1, 4],
    )
    cmd.build()


def test_cori_slurm_max_pend():
    if not hostname.startswith("cori"):
        pytest.skip("This test runs on Cori Login nodes ('cori*')")

    bc = SiteConfiguration(settings_file)
    bc.detect_system()
    bc.validate(moduletool="environment-modules")

    system = BuildTestSystem()

    cmd = BuildTest(
        configuration=bc,
        buildspecs=[
            os.path.join(
                os.getenv("BUILDTEST_ROOT"), "tests", "examples", "cori", "hold_job.yml"
            )
        ],
        buildtest_system=system,
        poll_interval=5,
        maxpendtime=10,
    )
    with pytest.raises(SystemExit):
        cmd.build()


def test_cori_slurm_file_exists():
    if not hostname.startswith("cori"):
        pytest.skip("This test runs on Cori Login nodes ('cori*')")

    bc = SiteConfiguration(settings_file)
    bc.detect_system()
    bc.validate(moduletool="environment-modules")

    system = BuildTestSystem()

    cmd = BuildTest(
        configuration=bc,
        buildspecs=[
            os.path.join(
                os.getenv("BUILDTEST_ROOT"), "tests", "examples", "cori", "exists.yml"
            )
        ],
        buildtest_system=system,
        poll_interval=5,
        maxpendtime=120,
    )
    cmd.build()


def test_compiler_find_cori():
    if not hostname.startswith("cori"):
        pytest.skip("This test runs on Cori Login nodes ('cori*')")

    bc = SiteConfiguration(settings_file)
    bc.detect_system()
    bc.validate(moduletool="environment-modules")

    # testing buildtest config compilers find
    compilers = BuildtestCompilers(configuration=bc)
    compilers.find_compilers()

    # test entry point for 'buildtest config compilers find --detailed'
    compiler_find(configuration=bc, detailed=True)


def test_compiler_test_cori():
    if not hostname.startswith("cori"):
        pytest.skip("This test runs on Cori Login nodes ('cori*')")

    bc = SiteConfiguration(settings_file)
    bc.detect_system()
    bc.validate(moduletool="environment-modules")

    # testing buildtest config compilers test
    compiler_test(configuration=bc)


def test_compiler_find_perlmutter():
    if not hostname.startswith("login"):
        pytest.skip("This test runs on Perlmutter Login nodes ('login*')")

    bc = SiteConfiguration(settings_file)
    bc.detect_system()
    bc.validate(moduletool="lmod")

    # testing buildtest config compilers find
    compilers = BuildtestCompilers(configuration=bc)
    compilers.find_compilers()

    # test entry point for 'buildtest config compilers find --detailed'
    compiler_find(configuration=bc, detailed=True)


def test_compiler_test_perlmutter():
    if not hostname.startswith("login"):
        pytest.skip("This test runs on Perlmutter Login nodes ('login*')")

    bc = SiteConfiguration(settings_file)
    bc.detect_system()
    bc.validate(moduletool="lmod")

    # testing buildtest config compilers test
    compiler_test(configuration=bc)


def test_compiler_find_alternative_filepath():
    if not hostname.startswith("login"):
        pytest.skip("This test runs on Perlmutter Login nodes ('login*')")
        
    bc = SiteConfiguration(settings_file)
    bc.detect_system()
    bc.validate(moduletool="lmod")

    # testing buildtest config compilers find
    compilers = BuildtestCompilers(configuration=bc)
    compilers.find_compilers()

    # test entry point for 'buildtest config compilers find --file'
    temp_path = tempfile.NamedTemporaryFile(dir=os.path.expanduser("~"))
    compiler_find(configuration=bc, filepath=temp_path.name)
    temp_path.close()
