import os

import pytest
from buildtest.buildsystem.builders import Builder
from buildtest.buildsystem.parser import BuildspecParser
from buildtest.cli.compilers import BuildtestCompilers
from buildtest.config import SiteConfiguration
from buildtest.defaults import DEFAULT_SETTINGS_FILE
from buildtest.executors.setup import BuildExecutor
from buildtest.system import BuildTestSystem

here = os.path.dirname(os.path.abspath(__file__))


def test_assert_ge(tmp_path):
    config = SiteConfiguration(DEFAULT_SETTINGS_FILE)
    config.detect_system()
    config.validate()
    executors = BuildExecutor(config)
    system = BuildTestSystem()

    bp = BuildspecParser(
        buildspec=os.path.join(here, "assert_ge.yml"), buildexecutor=executors
    )
    bc = BuildtestCompilers(configuration=config)
    builder = Builder(
        bp=bp,
        buildtest_compilers=bc,
        buildexecutor=executors,
        configuration=config,
        filters=[],
        testdir=tmp_path,
        buildtest_system=system,
    )
    builders = builder.get_builders()
    for test in builders:
        test.build()
