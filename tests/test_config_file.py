import os
from buildtest.tools.config import (
    BUILDTEST_CONFIG_FILE,
    func_config_view,
    func_config_restore,
)


def test_config_file_exists():
    assert os.path.exists(BUILDTEST_CONFIG_FILE)


def test_view_configuration():
    func_config_view()


def test_config_restore():
    func_config_restore()
