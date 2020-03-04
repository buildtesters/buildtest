import json
import os
import shutil
import sys
import yaml

from buildtest import BUILDTEST_VERSION
from buildtest.tools.file import create_dir
from buildtest.tools.defaults import (
    BUILDTEST_BUILD_LOGFILE,
    BUILDTEST_CONFIG_FILE,
    BUILDTEST_CONFIG_BACKUP_FILE,
    BUILDTEST_ROOT,
    DEFAULT_CONFIG_FILE,
    EDITOR_LIST,
)


def create_config_files():
    """if default config files don't exist, create them
    """
    if not os.path.exists(BUILDTEST_CONFIG_FILE):
        shutil.copy(DEFAULT_CONFIG_FILE, BUILDTEST_CONFIG_FILE)
        shutil.copy(DEFAULT_CONFIG_FILE, BUILDTEST_CONFIG_BACKUP_FILE)


def create_logfile():
    """Create a logfile to keep track of messages for the user, if doesn't exist
    """
    if not os.path.exists(BUILDTEST_BUILD_LOGFILE):
        build_dict = {"build": {}}
        with open(BUILDTEST_BUILD_LOGFILE, "w") as outfile:
            json.dump(build_dict, outfile, indent=2)


def init():
    """Buildtest init should check that the buildtest user root exists,
       and that dependency files are created. This is called by 
       load_configuration.
    """
    # check if $HOME/.buildtest exists, if not create directory
    if not os.path.exists(BUILDTEST_ROOT):
        print(
            f"Creating buildtest configuration directory: \
                 {BUILDTEST_ROOT}"
        )
        os.mkdir(BUILDTEST_ROOT)

    # Create subfolders for var and root
    create_dir(os.path.join(BUILDTEST_ROOT, "var"))
    create_dir(os.path.join(BUILDTEST_ROOT, "root"))
    create_dir(os.path.join(BUILDTEST_ROOT, "site"))

    # Create config files, module files, and log file
    create_config_files()
    create_logfile()


config_yaml_keys = {
    "BUILDTEST_MODULEPATH": type([]),
    "EDITOR": type("str"),
    "build": {
        "testdir": type("str"),
        "module": {"type": type(dict), "purge": {"type": type(bool)}},
    },
}


def check_configuration():
    """Checks all keys in configuration file (settings.yml) are valid
       keys and ensure value of each key matches expected type . For some keys
       special logic is taken to ensure values are correct and directory path
       exists.

       Also check if module command is found.

       If any error is found buildtest will terminate immediately.
       :return: returns gracefully if all checks passes otherwise terminate immediately
       :rtype: exit code 1 if checks failed
    """
    ec = 0

    if config_opts["BUILDTEST_MODULEPATH"] == None:
        print(
            "Please specify a module tree to BUILDTEST_MODULEPATH"
            + f"in configuration {BUILDTEST_CONFIG_FILE}"
        )
    else:
        for module_root in config_opts["BUILDTEST_MODULEPATH"]:
            if not os.path.isdir(module_root):
                print(
                    f"{module_root} directory does not exist"
                    + " specified in BUILDTEST_MODULEPATH"
                )
                ec = 1

    if config_opts["EDITOR"] not in EDITOR_LIST:
        print(f"Invalid EDITOR key: {config_opts['EDITOR']}")
        print(f"Please pick a valid editor option from the following: {EDITOR_LIST}")
        ec = 1

    if config_opts["build"]["testdir"]:
        config_opts["build"]["testdir"] = os.path.expandvars(
            config_opts["build"]["testdir"]
        )
        # create the directory if it doesn't exist
        if not os.path.isdir(config_opts["build"]["testdir"]):
            dir = config_opts["build"]["testdir"]
            print(f"creating directory: {dir}")
            os.makedirs(config_opts["build"]["testdir"])

    if ec:
        print("CONFIGURATION CHECK FAILED")
        print(f"Check your configuration: {BUILDTEST_CONFIG_FILE}")
        sys.exit(1)


def load_configuration(config_path=None):
    """load the default configuration file.
    """
    init()

    config_path = config_path or BUILDTEST_CONFIG_FILE

    # load the configuration file
    with open(BUILDTEST_CONFIG_FILE, "r") as fd:
        config_opts = yaml.safe_load(fd)

    config_opts["BUILDTEST_VERSION"] = BUILDTEST_VERSION

    # if BUILDTEST_MODULEPATH is empty list then check if MODULEPATH is defined
    # and set result to BUILDTEST_MODULEPATH
    if not config_opts["BUILDTEST_MODULEPATH"]:
        if not os.getenv("MODULEPATH"):
            config_opts["BUILDTEST_MODULEPATH"] = []
        else:

            # otherwise set this to MODULEPATH
            tree_list = []

            # check each directory in MODULEPATH and add it to BUILDTEST_MODULEPATH
            for tree in os.getenv("MODULEPATH", "").split(":"):
                if os.path.isdir(tree):
                    tree_list.append(tree)

            config_opts["BUILDTEST_MODULEPATH"] = tree_list

    return config_opts


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


# Run on init, so we only load once
config_opts = load_configuration()
