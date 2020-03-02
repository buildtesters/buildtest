import os
import yaml
from buildtest.tools.config import config_opts, BUILDTEST_CONFIG_FILE
from buildtest.tools.file import is_dir
from buildtest.tools.modules import update_spider_file

def module_tree_list():
    """This method list module trees assigned to BUILDTEST_MODULEPATH"""
    [print(tree) for tree in config_opts["BUILDTEST_MODULEPATH"]]


def module_tree_add(tree_list):
    """This method adds a module tree to BUILDTEST_MODULEPATH in configuration file.
    This implemenents command ``buildtest module tree -a <tree>``

    :param tree_list: colon separated list of the root of module trees
    :type tree_list: str, required
    :return: Update configuration file with updated value for BUILDTEST_MODULEPATH
    """

    with open(BUILDTEST_CONFIG_FILE, "r") as fd:
        content = yaml.safe_load(fd)

    for tree in tree_list:
        is_dir(tree)
        tree = os.path.expandvars(tree)
        tree = os.path.expanduser(tree)
        content["BUILDTEST_MODULEPATH"].append(tree)

    # converting to set to avoid adding duplicate entries
    module_tree_set = set(content["BUILDTEST_MODULEPATH"])
    module_tree_set.add(tree)

    content["BUILDTEST_MODULEPATH"] = list(module_tree_set)

    with open(BUILDTEST_CONFIG_FILE, "w") as fd:
        yaml.dump(content, fd, default_flow_style=False)

    print(f"Adding module tree: {tree_list}")
    print(f"Configuration File: {BUILDTEST_CONFIG_FILE} has been updated")


def module_tree_rm(tree_list):
    """ This method removes a module tree from BUILDTEST_MODULEPATH in configuration file.
    This implements command ``buildtest module tree -r <tree>``

    :param tree_list: root of a module tree
    :type tree_list: str, required
    :return: Update configuration file with updated value for BUILDTEST_MODULEPATH
    """

    with open(BUILDTEST_CONFIG_FILE, "r") as fd:
        content = yaml.safe_load(fd)

    for tree in tree_list:
        tree = os.path.expandvars(tree)
        tree = os.path.expanduser(tree)
        if tree in content["BUILDTEST_MODULEPATH"]:
            content["BUILDTEST_MODULEPATH"].remove(tree)

    with open(BUILDTEST_CONFIG_FILE, "w") as fd:
        yaml.dump(content, fd, default_flow_style=False)

    print(f"Removing module tree: {tree_list}")
    print(f"Configuration File: {BUILDTEST_CONFIG_FILE} has been updated")


def module_tree_set(tree):
    """This method override BUILDTEST_MODULEPATH to the user specified tree. This will
    update the configuration file and implements command ``buildtest module tree -s <path>``

    :param tree: root of module tree to set for variable BUILDTEST_MODULEPATH
    :type tree: str, required
    :return: Update configuration file with updated value for BUILDTEST_MODULEPATH
    """

    with open(BUILDTEST_CONFIG_FILE, "r") as fd:
        content = yaml.safe_load(fd)

    is_dir(tree)
    content["BUILDTEST_MODULEPATH"].clear()
    content["BUILDTEST_MODULEPATH"].append(tree)

    with open(BUILDTEST_CONFIG_FILE, "w") as fd:
        yaml.dump(content, fd, default_flow_style=False)

    print(f"Setting module tree: {tree}")
    print(f"Configuration File: {BUILDTEST_CONFIG_FILE} has been updated")
