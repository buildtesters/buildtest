import os
from shutil import copy
from buildtest.config import config_opts
from buildtest.defaults import (
    BUILDTEST_CONFIG_FILE,
    BUILDTEST_CONFIG_BACKUP_FILE,
    DEFAULT_CONFIG_FILE,
)


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
        print(f"Restoring from default configuration: {DEFAULT_CONFIG_FILE}")
        copy(DEFAULT_CONFIG_FILE, BUILDTEST_CONFIG_FILE)
        copy(DEFAULT_CONFIG_FILE, BUILDTEST_CONFIG_BACKUP_FILE)


def show_configuration():
    """This method display buildtest configuration to terminal and this
       implements command buildtest show --config.
    """
    exclude_list = ["BUILDTEST_VERSION"]

    for key in sorted(config_opts):
        if key in exclude_list:
            continue

        if key == "BUILDTEST_MODULEPATH":
            tree = ""
            for mod_tree in config_opts[key]:
                tree += mod_tree + ":"

            # remove last colon
            tree = tree[:-1]
            print((f"{key} \t =").expandtabs(50), tree)
        # print all keys in module dictionary
        elif key in ["module", "build"]:
            module_keys = config_opts[key].keys()

            for m in module_keys:
                if isinstance(config_opts[key][m], dict):
                    for k, v in config_opts[key][m].items():
                        print((f"{key}[{m}][{k}] \t =").expandtabs(50), v)
                else:
                    print((f"{key}[{m}] \t =").expandtabs(50), config_opts[key][m])

        else:
            print((f"{key} \t =").expandtabs(50), f"{config_opts[key]}")
