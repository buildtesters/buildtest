import os
from shutil import copy
from buildtest.config import get_default_settings
from buildtest.defaults import (
    BUILDTEST_SETTINGS_FILE,
    DEFAULT_SETTINGS_FILE,
)


def func_config_edit(args=None):
    """Edit buildtest configuration in editor. This implements ``buildtest config edit``"""

    config_opts = get_default_settings()
    os.system(f"{config_opts['config']['editor']} {BUILDTEST_SETTINGS_FILE}")


def func_config_view(args=None):
    """View buildtest configuration file. This implements ``buildtest config view``"""

    os.system(f"cat {BUILDTEST_SETTINGS_FILE}")


def func_config_reset(args=None):
    """Reset buildtest configuration by copying default configuration provided by buildtest to
       $HOME/.buildtest/settings.yml. This implements ``buildtest config reset`` command."""

    print(f"Restoring from default configuration: {DEFAULT_SETTINGS_FILE}")
    copy(DEFAULT_SETTINGS_FILE, BUILDTEST_SETTINGS_FILE)
