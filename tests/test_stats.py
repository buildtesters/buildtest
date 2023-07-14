from buildtest.cli.build import BuildTest
from buildtest.cli.buildspec import BuildspecCache
from buildtest.cli.report import Report
from buildtest.cli.stats import stats_cmd
from buildtest.config import SiteConfiguration
from buildtest.system import BuildTestSystem


def test_stats():
    configuration = SiteConfiguration()
    configuration.detect_system()
    configuration.validate()
    system = BuildTestSystem()

    BuildspecCache(rebuild=True, configuration=configuration)

    cmd = BuildTest(configuration=configuration, tags=["pass"], buildtest_system=system)
    cmd.build()

    report = Report(configuration=configuration)
    name = report.get_random_tests()
    stats_cmd(name[0], configuration=configuration)
