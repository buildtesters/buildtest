import os
from shutil import copy
from buildtest.tools.config import config_opts, BUILDTEST_CONFIG_FILE, BUILDTEST_CONFIG_BACKUP_FILE, DEFAULT_CONFIG_FILE
def func_config_edit(args=None):
    """Edit buildtest configuration in editor. This implements ``buildtest config edit``"""

    os.system(f"{config_opts['EDITOR']} {BUILDTEST_CONFIG_FILE}")


def func_config_view(args=None):
    """View buildtest configuration file. This implements ``buildtest config view``"""

    os.system(f"cat {BUILDTEST_CONFIG_FILE}")


def func_config_restore(args=None):
    """Restore buildtest configuration from backup file. This implements ``buildtest config restore``"""
    if os.path.isfile(BUILDTEST_CONFIG_BACKUP_FILE):
        copy(BUILDTEST_CONFIG_BACKUP_FILE, BUILDTEST_CONFIG_FILE)
        print(f"Restore configuration from backup file: {BUILDTEST_CONFIG_BACKUP_FILE}")
    else:
        print(f"Can't find backup file: {BUILDTEST_CONFIG_BACKUP_FILE}")
        print(f"Resorting from default configuration: {DEFAULT_CONFIG_FILE}")
        copy(DEFAULT_CONFIG_FILE, BUILDTEST_CONFIG_FILE)
        copy(DEFAULT_CONFIG_FILE, BUILDTEST_CONFIG_BACKUP_FILE)