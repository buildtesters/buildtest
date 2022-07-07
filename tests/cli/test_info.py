from buildtest.cli.info import buildtest_info
from buildtest.config import SiteConfiguration
from buildtest.system import BuildTestSystem


def test_buildtest_info():

    config = SiteConfiguration()
    config.detect_system()
    config.validate()

    system = BuildTestSystem()
    buildtest_info(configuration=config, buildtest_system=system)
