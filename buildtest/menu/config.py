import os
from shutil import copy
from buildtest.config import get_default_configuration
from buildtest.defaults import (
    BUILDTEST_CONFIG_FILE,
    DEFAULT_CONFIG_FILE,
)


def func_config_edit(args=None):
    """Edit buildtest configuration in editor. This implements ``buildtest config edit``"""

    config_opts = get_default_configuration()
    os.system(f"{config_opts['editor']} {BUILDTEST_CONFIG_FILE}")


def func_config_view(args=None):
    """View buildtest configuration file. This implements ``buildtest config view``"""

    os.system(f"cat {BUILDTEST_CONFIG_FILE}")


def func_config_reset(args=None):
    """Reset buildtest configuration by copying default configuration provided by buildtest to
       $HOME/.buildtest/settings.yml. This implements ``buildtest config reset`` command."""

    print(f"Restoring from default configuration: {DEFAULT_CONFIG_FILE}")
    copy(DEFAULT_CONFIG_FILE, BUILDTEST_CONFIG_FILE)
