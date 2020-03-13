import os
from buildtest.defaults import BUILDTEST_CONFIG_FILE


def test_config_file_exists():
    assert os.path.exists(BUILDTEST_CONFIG_FILE)
