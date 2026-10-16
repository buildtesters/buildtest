import getpass
import os
import shutil

import pytest

from buildtest.cli.build import BuildTest
from buildtest.cli.buildspec import BuildspecCache
from buildtest.config import SiteConfiguration
from buildtest.defaults import BUILDTEST_ROOT


@pytest.mark.spack
def test_spack_examples():
    # Spack integration tests require the buildtest Spack tutorial container,
    # which is based on the SC25 Spack tutorial image.
    if not (getpass.getuser() in ["root", "spack", "runner"] and shutil.which("spack")):
        pytest.skip(
            "Unable to run this test; requires the "
            "ghcr.io/buildtesters/buildtest_spack:spack-sc25 container"
        )

    configuration = SiteConfiguration(
        settings_file=os.path.join(
            BUILDTEST_ROOT, "buildtest", "settings", "spack_container.yml"
        )
    )
    configuration.detect_system()
    configuration.validate()

    print("config: ", configuration.file)
    # ensure we rebuild cache file before running any buildspecs commands
    bp = BuildspecCache(rebuild=True, configuration=configuration)
    bp.print_tags()

    cmd = BuildTest(configuration=configuration, tags=["spack"], dry_run=True)
    cmd.build()
