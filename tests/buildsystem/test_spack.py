import getpass
import os
import shutil

import pytest

from buildtest.cli.build import BuildTest
from buildtest.cli.buildspec import BuildspecCache
from buildtest.config import SiteConfiguration
from buildtest.system import BuildTestSystem

here = os.path.dirname(os.path.abspath(__file__))

@pytest.mark.spack
def test_spack_examples():
    # spack builds must run in container  ghcr.io/buildtesters/buildtest_spack:latest which comes with username 'spack' and home directory '/home/spack'
    # if not (getpass.getuser() == "spack" and os.path.expanduser("~") == "/home/spack"):
    if not (getpass.getuser() == "runner" and shutil.which("spack")):
        pytest.skip(
            "Unable to run this test requires docker container:  ghcr.io/buildtesters/buildtest_spack:latest"
        )

    system = BuildTestSystem()

    configuration = SiteConfiguration(
        settings_file=os.path.join(here, "spack_container.yml")
    )
    configuration.detect_system()
    configuration.validate()

    print("config: ", configuration.file)
    # ensure we rebuild cache file before running any buildspecs commands
    bp = BuildspecCache(rebuild=True, configuration=configuration)
    bp.print_tags()

    cmd = BuildTest(
        configuration=configuration,
        tags=["spack"],
        stage="build",
        buildtest_system=system,
    )
    cmd.build()
