from buildtest.cli.debugreport import print_debug_info
from buildtest.config import SiteConfiguration
from buildtest.system import BuildTestSystem


def test_debug_report():
    system = BuildTestSystem()
    system.check()

    config = SiteConfiguration()
    print_debug_report(system, config)
