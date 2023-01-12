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


def test_assert_le():

    cmd = BuildTest(
        buildspecs=[os.path.join(here, "assert_le.yml")],
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


def test_assert_range():
    cmd = BuildTest(
        buildspecs=[os.path.join(here, "assert_range.yml")],
        buildtest_system=system,
        configuration=config,
    )
    cmd.build()


def test_assert_exists():
    cmd = BuildTest(
        buildspecs=[os.path.join(here, "exists.yml")],
        buildtest_system=system,
        configuration=config,
    )
    cmd.build()


def test_assert_is_file_is_dir():
    cmd = BuildTest(
        buildspecs=[os.path.join(here, "file_and_dir_check.yml")],
        buildtest_system=system,
        configuration=config,
    )
    cmd.build()
