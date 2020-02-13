import yaml
import os
import sys
from shutil import copy
BUILDTEST_VERSION = "0.7.6"
# root of buildtest-framework repository
BUILDTEST_ROOT = os.getenv("BUILDTEST_ROOT")
# json file used by buildtest to write build meta-data
BUILDTEST_BUILD_LOGFILE = os.path.join(os.getenv("BUILDTEST_ROOT"), "var", "build.json")
# dictionary used for storing status of builds
BUILDTEST_BUILD_HISTORY = {}

buildtest_home_conf_dir = os.path.join(os.getenv("HOME"), ".buildtest")
# variable used to store buildtest configuration file in $HOME/.buildtest/settings.yml
BUILDTEST_CONFIG_FILE = os.path.join(buildtest_home_conf_dir, "settings.yml")
BUILDTEST_CONFIG_BACKUP_FILE = os.path.join(buildtest_home_conf_dir, "settings.yml.bak")
# json file used for storing buildtest module collections
BUILDTEST_MODULE_COLLECTION_FILE = os.path.join(
    os.getenv("BUILDTEST_ROOT"), "var", "collection.json"
)
BUILDTEST_MODULE_FILE = os.path.join(os.getenv("BUILDTEST_ROOT"), "var", "modules.json")
# DEFAULT_CONFIG_FILE is the default buildtest configuration found in root of buildtest-framework repo
DEFAULT_CONFIG_FILE = os.path.join(os.getenv("BUILDTEST_ROOT"), "settings.yml")
EDITOR_LIST = ["vim", "emacs", "nano"]
# TESTCONFIG_ROOT is the root directory where test configurations are found
TESTCONFIG_ROOT = os.path.join(os.getenv("BUILDTEST_ROOT"), "toolkit", "suite")
# check if $HOME/.buildtest exists, if not create directory
if not os.path.isdir(buildtest_home_conf_dir):
    print(
        f"Creating buildtest configuration directory: \
            {buildtest_home_conf_dir}"
    )
    os.makedirs(buildtest_home_conf_dir)

# if the file $HOME/.buildtest/settings.yml does not exist copy the default file
# into the appropriate location
if not os.path.exists(BUILDTEST_CONFIG_FILE):
    copy(DEFAULT_CONFIG_FILE, BUILDTEST_CONFIG_FILE)
    copy(DEFAULT_CONFIG_FILE, BUILDTEST_CONFIG_BACKUP_FILE)


# load the configuration file
fd = open(BUILDTEST_CONFIG_FILE, "r")
config_opts = yaml.safe_load(fd)

# if BUILDTEST_MODULEPATH is empty list then check if MODULEPATH is defined
# and set result to BUILDTEST_MODULEPATH
if len(config_opts["BUILDTEST_MODULEPATH"]) == 0:

    if os.getenv("MODULEPATH") == None:
        config_opts["BUILDTEST_MODULEPATH"] = []
    else:
        # otherwise set this to MODULEPATH
        tree_list = []
        # check each directory in MODULEPATH and add it to BUILDTEST_MODULEPATH
        for tree in os.getenv("MODULEPATH").split(":"):
            if os.path.isdir(tree):
                tree_list.append(tree)
            # else:
            # print (f"Skipping module tree {tree} because path does not exist")
        config_opts["BUILDTEST_MODULEPATH"] = tree_list

config_opts["BUILDTEST_VERSION"] = BUILDTEST_VERSION

logID = "buildtest"

config_yaml_keys = {
    "BUILDTEST_MODULEPATH": type([]),
    "EDITOR": type("str"),
    "build": {
        "testdir": type("str"),
        "module": {
            "type": type(dict),
            "purge": {
                "type": type(bool)
            },
        },
    },
    "module": {
        "list": {
            "type": type(dict),

            "exclude_version_files": {
                "type": type("str")
            },
            "filter": {
                "type": type(dict),
                "include": {
                    "type": type([])
                },
            },
            "querylimit": {
                "type": type(int)
            },
        },
        "loadtest": {
            "type": type(dict),
            "login": {
                "type": type(bool)
            },
            "purge_modules": {
                "type": type(bool)
            },
            "numtest": {
                "type": type(int)
            },
        }
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
        print(
            f"Please pick a valid editor option from the following: {EDITOR_LIST}"
        )
        ec = 1

    if config_opts["build"]["testdir"]:
        config_opts["build"]["testdir"] = os.path.expandvars(config_opts["build"]["testdir"])
        # create the directory if it doesn't exist
        if not os.path.isdir(config_opts["build"]["testdir"]):
            dir = config_opts["build"]["testdir"]
            print (f"creating directory: {dir}")
            os.makedirs(config_opts["build"]["testdir"])

    if ec:
        print("CONFIGURATION CHECK FAILED")
        print(f"Check your configuration: {BUILDTEST_CONFIG_FILE}")
        sys.exit(1)


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
        elif key in ["module","build"]:
            module_keys = config_opts[key].keys()

            for m in module_keys:
                if isinstance(config_opts[key][m],dict):
                    for k,v in config_opts[key][m].items():
                        print((f"{key}[{m}][{k}] \t =").expandtabs(50), v)
                else:
                    print((f"{key}[{m}] \t =").expandtabs(50), config_opts[key][m])

        else:
            print((f"{key} \t =").expandtabs(50), f"{config_opts[key]}")
