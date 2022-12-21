import os

from buildtest.cli.build import BuildTest
from buildtest.config import SiteConfiguration
from buildtest.defaults import DEFAULT_SETTINGS_FILE
from buildtest.system import BuildTestSystem

here = os.path.dirname(os.path.abspath(__file__))

config = SiteConfiguration(DEFAULT_SETTINGS_FILE)
config.detect_system()
config.validate()
system = BuildTestSystem()


def test_assert_ge():

    cmd = BuildTest(
        buildspecs=[os.path.join(here, "assert_ge.yml")],
        buildtest_system=system,
        configuration=config,
    )
    cmd.build()


def test_assert_eq():
    cmd = BuildTest(
        buildspecs=[os.path.join(here, "assert_eq.yml")],
        buildtest_system=system,
        configuration=config,
    )
    cmd.build()
