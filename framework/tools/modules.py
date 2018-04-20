############################################################################
#
#  Copyright 2017
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

"""
This python module does the following
	 - get module listing
	 - get unique application
	 - get unique application version
	 - get easybuild toolchains
 	 - check if software exists based on argument -s
	 - check if toolchain exists based on argument -t
	 - check if easyconfig passes

:author: Shahzeb Siddiqui (Pfizer)
"""
import os
import sys

from framework.env import config_opts
from framework.tools.easybuild import get_module_ebroot
#from framework.tools.utility import get_appname, get_appversion, get_toolchain_name, get_toolchain_version


def get_module_list():
    """
    returns a complete list of modules and full path in module tree
    """
    modulefiles = []
    modtrees = get_module_ebroot()
    for tree in modtrees:
        for root, dirs, files in os.walk(tree):
            for file in files:
                # skipping files that are symbolic links
                if os.path.islink(os.path.join(root,file)):
                    continue

                if file == ".version":
                        continue

                modulefiles.append(os.path.join(root,file))

    return modulefiles

def load_modules(shell_type):
    """
    return a string that loads the software and toolchain module.
    """
    from framework.tools.menu import buildtest_menu
    args_dict = buildtest_menu().parse_options()
    software = args_dict.software
    toolchain = args_dict.toolchain

    #print software

    shell_magic = "#!/" + os.path.join("bin",shell_type)


    BUILDTEST_MODULE_NAMING_SCHEME = config_opts['BUILDTEST_MODULE_NAMING_SCHEME']
    header = shell_magic + "\n"
    header+= "module purge \n"
    # for dummy toolchain you can load software directly. Ensure a clean environment by running module purge
    if toolchain == None:
        moduleload = "module load " + software  + "\n"
    else:
        if BUILDTEST_MODULE_NAMING_SCHEME == "HMNS":
            moduleload = "module load " + toolchain + "\n"
            moduleload += "module load " + software + "\n"
        elif BUILDTEST_MODULE_NAMING_SCHEME == "FNS":
            moduleload = "module load " + software + "\n"
            print moduleload

    header = header + moduleload
    return header

def diff_trees(args_trees):
    """ display difference between module trees """

    # no comma found between two trees
    if args_trees.find(",") == -1:
        print "Usage: --diff-trees /path/to/tree1,/path/to/tree2"
        sys.exit(1)
    else:
        id = args_trees.find(",")
        tree1 = args_trees[0:id]
        tree2 = args_trees[id+1:len(args_trees)]
        if not os.path.exists(tree1):
            print "Path does not exist: ", tree1

        if not os.path.exists(tree2):
            print "Path does not exist: ", tree2

        modlist1 = []
        modlist2 = []

        for tree in tree1:
            for root, dirs, files in os.walk(tree1):
                for file in files:
                    # skipping files that are symbolic links
                    if os.path.islink(os.path.join(root,file)):
                        continue

                    parent_dir = os.path.basename(root)
                    modlist1.append(os.path.join(parent_dir,file))

        for tree in tree2:
            for root, dirs, files in os.walk(tree2):
                for file in files:
                    # skipping files that are symbolic links
                    if os.path.islink(os.path.join(root,file)):
                        continue

                    parent_dir = os.path.basename(root)
                    modlist2.append(os.path.join(parent_dir,file))

        diff_set =  set(modlist1).symmetric_difference(set(modlist2))
        if len(diff_set) == 0:
            print "No difference found between module tree: ", tree1, "and module tree:", tree2
            return

        print "\t\t\t Comparing Module Trees for differences in module files"
        print "\t\t\t -------------------------------------------------------"

        print
        print "Module Tree 1:", tree1
        print "Module Tree 2:", tree2
        print
        print "ID       |     Module                                                   |   Module Tree 1    |   Module Tree 2"
        print "---------|--------------------------------------------------------------|--------------------|----------------------"

        count = 1
        # print difference set
        for i in diff_set:
            module_in_tree = ""
            value1 = "NOT FOUND"
            value2 = "NOT FOUND"
            # finding which module tree the module belongs
            if i in modlist1:
                module_in_tree = tree1
            if i in modlist2:
                module_in_tree = tree2

            if module_in_tree == tree1:
                value1 = "FOUND"

            if module_in_tree == tree2:
                value2 = "FOUND"


            print (str(count) + "\t |").expandtabs(8), (i + "\t |").expandtabs(60) , (value1 + "\t |").expandtabs(18), value2
            count = count + 1
