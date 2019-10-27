import yaml
from buildtest.tools.config import config_opts, BUILDTEST_CONFIG_FILE
from buildtest.tools.file import is_dir

def func_module_tree_subcmd(args):
    """ Entry point for ``buildtest module tree`` subcommand """

    if args.list:
        [print (tree) for tree in config_opts["BUILDTEST_MODULEPATH"]]

    if args.add:
        module_tree_add(args.add)

    if args.rm:
        module_tree_rm(args.rm)

    if args.set:
        module_tree_set(args.set)

def module_tree_add(tree_list):
    """This method adds a module tree to BUILDTEST_MODULEPATH in configuration file.
    This implemenents command ``buildtest module tree -a <tree>``

    :param tree_list: colon separated list of the root of module trees
    :type tree_list: str, required
    :return: Update configuration file with updated value for BUILDTEST_MODULEPATH
    """

    fd = open(BUILDTEST_CONFIG_FILE, "r")
    content = yaml.safe_load(fd)
    fd.close()

    for tree in tree_list:
        is_dir(tree)
        content["BUILDTEST_MODULEPATH"].append(tree)

    # converting to set to avoid adding duplicate entries
    module_tree_set = set(content["BUILDTEST_MODULEPATH"])
    module_tree_set.add(tree)

    content["BUILDTEST_MODULEPATH"] = list(module_tree_set)

    fd = open(BUILDTEST_CONFIG_FILE, "w")
    yaml.dump(content, fd, default_flow_style=False)
    fd.close()

    print(f"Adding module tree: {tree_list}")
    print(f"Configuration File: {BUILDTEST_CONFIG_FILE} has been updated")

def module_tree_rm(tree_list):
    """ This method removes a module tree from BUILDTEST_MODULEPATH in configuration file.
    This implements command ``buildtest module tree -r <tree>``

    :param tree_list: root of a module tree
    :type tree_list: str, required
    :return: Update configuration file with updated value for BUILDTEST_MODULEPATH
    """

    fd = open(BUILDTEST_CONFIG_FILE,"r")
    content = yaml.safe_load(fd)
    for tree in tree_list:
        if tree in content["BUILDTEST_MODULEPATH"]:
            content["BUILDTEST_MODULEPATH"].remove(tree)

    fd.close()

    fd = open(BUILDTEST_CONFIG_FILE,"w")
    yaml.dump(content,fd,default_flow_style=False)
    fd.close()
    print (f"Removing module tree: {tree_list}")
    print (f"Configuration File: {BUILDTEST_CONFIG_FILE} has been updated")

def module_tree_set(tree):
    """This method override BUILDTEST_MODULEPATH to the user specified tree. This will
    update the configuration file and implements command ``buildtest module tree -s <path>``

    :param tree: root of module tree to set for variable BUILDTEST_MODULEPATH
    :type tree: str, required
    :return: Update configuration file with updated value for BUILDTEST_MODULEPATH
    """

    fd = open(BUILDTEST_CONFIG_FILE, "r")
    content = yaml.safe_load(fd)
    fd.close()


    is_dir(tree)
    content["BUILDTEST_MODULEPATH"] = []
    content["BUILDTEST_MODULEPATH"].append(tree)

    fd = open(BUILDTEST_CONFIG_FILE, "w")
    yaml.dump(content, fd, default_flow_style=False)
    fd.close()

    print(f"Setting module tree: {tree}")
    print(f"Configuration File: {BUILDTEST_CONFIG_FILE} has been updated")