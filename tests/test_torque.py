import os

import pytest

from buildtest.cli.build import BuildTest
from buildtest.config import SiteConfiguration
from buildtest.exceptions import BuildTestError
from buildtest.scheduler.detection import Torque


def test_torque():
    torque = Torque()
    if not torque.active():
        pytest.skip("Test must run on torque scheduler")

    here = os.path.dirname(os.path.abspath(__file__))
    settings_file = os.path.join(here, "settings", "torque.yml")

    bc = SiteConfiguration(settings_file)
    bc.detect_system()
    bc.validate()

    cmd = BuildTest(
        configuration=bc,
        buildspecs=[os.path.join(here, "examples", "torque", "sleep.yml")],
        poll_interval=5,
    )
    cmd.build()

    with pytest.raises(BuildTestError):
        cmd = BuildTest(
            configuration=bc,
            buildspecs=[os.path.join(here, "examples", "torque", "sleep_cancel.yml")],
            poll_interval=1,
            maxpendtime=2,
        )
        cmd.build()

    cmd = BuildTest(
        configuration=bc,
        buildspecs=[os.path.join(here, "examples", "torque", "sleep.yml")],
        numprocs=[1, 2, 4],
        poll_interval=5,
    )
    cmd.build()

    def test_invalid_executor():

        torque = Torque()
        if not torque.active():
            pytest.skip("Test must run on torque scheduler")

        here = os.path.dirname(os.path.abspath(__file__))
        settings_file = os.path.join(
            here, "settings", "invalid", "torque_invalid_executor.yml"
        )

        bc = SiteConfiguration(settings_file)
        bc.detect_system()
        bc.validate()
