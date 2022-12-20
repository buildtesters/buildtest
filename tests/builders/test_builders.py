import os

import pytest
from buildtest.buildsystem.builders import Builder
from buildtest.buildsystem.parser import BuildspecParser
from buildtest.cli.build import BuildTest
from buildtest.cli.compilers import BuildtestCompilers
from buildtest.config import SiteConfiguration
from buildtest.defaults import DEFAULT_SETTINGS_FILE
from buildtest.executors.setup import BuildExecutor
from buildtest.system import BuildTestSystem

here = os.path.dirname(os.path.abspath(__file__))

config = SiteConfiguration(DEFAULT_SETTINGS_FILE)
config.detect_system()
config.validate()
executors = BuildExecutor(config)
system = BuildTestSystem()
bc = BuildtestCompilers(configuration=config)


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
