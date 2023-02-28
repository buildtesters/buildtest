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
    """This test buildspec using status check with  'assert_ge'"""
    cmd = BuildTest(
        buildspecs=[os.path.join(here, "assert_ge.yml")],
        buildtest_system=system,
        configuration=config,
    )
    cmd.build()


def test_assert_le():
    """This test buildspec using status check with  'assert_le'"""
    cmd = BuildTest(
        buildspecs=[os.path.join(here, "assert_le.yml")],
        buildtest_system=system,
        configuration=config,
    )
    cmd.build()


def test_assert_gt():
    """This test buildspec using status check with  'assert_gt'"""
    cmd = BuildTest(
        buildspecs=[os.path.join(here, "assert_gt.yml")],
        buildtest_system=system,
        configuration=config,
    )
    cmd.build()


def test_assert_lt():
    """This test buildspec using status check with  'assert_lt'"""
    cmd = BuildTest(
        buildspecs=[os.path.join(here, "assert_lt.yml")],
        buildtest_system=system,
        configuration=config,
    )
    cmd.build()


def test_assert_eq():
    """This test buildspec using status check with  'assert_eq'"""
    cmd = BuildTest(
        buildspecs=[os.path.join(here, "assert_eq.yml")],
        buildtest_system=system,
        configuration=config,
    )
    cmd.build()


def test_assert_ne():
    """This test buildspec using status check with  'assert_ne'"""
    cmd = BuildTest(
        buildspecs=[os.path.join(here, "assert_ne.yml")],
        buildtest_system=system,
        configuration=config,
    )
    cmd.build()


def test_assert_contains():
    """This test buildspec using status check with  'assert_contains'"""

    cmd = BuildTest(
        buildspecs=[os.path.join(here, "contains.yml")],
        buildtest_system=system,
        configuration=config,
    )
    cmd.build()


def test_assert_range():
    """This test buildspec using status check with  'assert_range'"""

    cmd = BuildTest(
        buildspecs=[os.path.join(here, "assert_range.yml")],
        buildtest_system=system,
        configuration=config,
    )
    cmd.build()


def test_assert_is_symlink():
    """This test buildspec using status check with  'is_symlink'"""
    cmd = BuildTest(
        buildspecs=[os.path.join(here, "is_symlink.yml")],
        buildtest_system=system,
        configuration=config,
    )
    cmd.build()


def test_assert_exists():
    """This test buildspec using status check with  'exists'"""
    cmd = BuildTest(
        buildspecs=[os.path.join(here, "exists.yml")],
        buildtest_system=system,
        configuration=config,
    )
    cmd.build()


def test_assert_is_file_is_dir():
    """This test buildspec using status check with  'is_dir' and 'is_file'"""
    cmd = BuildTest(
        buildspecs=[os.path.join(here, "file_and_dir_check.yml")],
        buildtest_system=system,
        configuration=config,
    )
    cmd.build()


def test_file_count():
    """This test buildspec using status check with  'file_count'"""
    cmd = BuildTest(
        buildspecs=[
            os.path.join(here, "file_count.yml"),
            os.path.join(here, "file_count_pattern.yml"),
            os.path.join(here, "file_count_filetype.yml"),
        ],
        buildtest_system=system,
        configuration=config,
    )
    cmd.build()
