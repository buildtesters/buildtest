############################################################################
#
#  Copyright 2017-2019
#
#   https://github.com/HPC-buildtest/buildtest-framework
#
#  This file is part of buildtest.
#
#    buildtest is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    buildtest is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with buildtest.  If not, see <http://www.gnu.org/licenses/>.
#############################################################################


import yaml
from buildtest.tools.config import config_opts, BUILDTEST_CONFIG_FILE
from buildtest.tools.file import is_dir


def module_tree_add(tree_list):
    """adding a module tree to BUILDTEST_MODULEPATH in configuration file"""

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
    """ remove a module tree from BUILDTEST_MODULEPATH in configuration file"""

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
    """set a module tree to BUILDTEST_MODULEPATH in configuration file"""

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