import pytest
from buildtest.cli.build import BuildTest
from buildtest.cli.buildspec import BuildspecCache
from buildtest.config import SiteConfiguration
from buildtest.system import BuildTestSystem

configuration = SiteConfiguration()
configuration.detect_system()
configuration.validate()


@pytest.mark.skip("Unable to run this test requires docker container")
def test_spack_examples():
    system = BuildTestSystem()
    system.check()

    # ensure we rebuild cache file before running any buildspecs commands
    BuildspecCache(rebuild=True, configuration=configuration)

    cmd = BuildTest(
        configuration=configuration,
        tags=["spack"],
        stage="build",
        buildtest_system=system,
    )
    cmd.build()
