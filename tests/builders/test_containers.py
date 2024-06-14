import os
import shutil

import pytest

from buildtest.cli.build import BuildTest
from buildtest.config import SiteConfiguration
from buildtest.defaults import BUILDTEST_ROOT, DEFAULT_SETTINGS_FILE
from buildtest.system import BuildTestSystem

here = os.path.dirname(os.path.abspath(__file__))

config = SiteConfiguration(DEFAULT_SETTINGS_FILE)
config.detect_system()
config.validate()
system = BuildTestSystem()


def test_docker_example():
    if not shutil.which("docker"):
        pytest.skip("docker is not available to run this test")

    cmd = BuildTest(
        buildspecs=[
            os.path.join(BUILDTEST_ROOT, "tutorials", "containers", "hello_world.yml")
        ],
        configuration=config,
    )
    cmd.build()


def test_singularity_example():
    if not shutil.which("singularity"):
        pytest.skip("singularity is not available to run this test")

    cmd = BuildTest(
        buildspecs=[
            os.path.join(
                BUILDTEST_ROOT, "tutorials", "containers", "hello_world_singularity.yml"
            )
        ],
        configuration=config,
    )
    cmd.build()
