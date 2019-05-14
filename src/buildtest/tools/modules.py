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

"""
This python module does the following
	 - get module listing
	 - get unique application
	 - get unique application version
 	 - check if software exists based on argument -s
	 - check if toolchain exists based on argument -t
	 - check if easyconfig passes
"""
import json
import os
import sys
import subprocess
import yaml
from buildtest.tools.config import config_opts, BUILDTEST_CONFIG_FILE
from buildtest.tools.file import string_in_file, is_dir


def func_module_subcmd(args):
    """ entry point for buildtest module subcommand """

    if args.diff_trees:
        diff_trees(args.diff_trees)

    if args.easybuild:
        check_easybuild_module()

    if args.spack:
        check_spack_module()

def func_module_tree_subcmd(args):
    """ Entry point for buildtest module tree subcommand """
    if args.list:
        [print (tree) for tree in config_opts["BUILDTEST_MODULEPATH"]]

    if args.add:
        module_tree_add(args.add)

    if args.rm:
        module_tree_rm(args.rm)

class BuildTestModule():
    def __init__(self):

        self.moduletree = ':'.join(map(str,config_opts["BUILDTEST_MODULEPATH"] ))

        cmd = f"$LMOD_DIR/spider -o spider-json {self.moduletree}"
        out = subprocess.check_output(cmd, shell=True).decode("utf-8")
        self.module_dict = json.loads(out)
        version = self.get_version()
        self.major_ver = version[0]
    def get_module_spider_json(self):
        return self.module_dict
    def get_unique_modules(self):
        """Return a list of unique keys (software name) from spider"""

        # return all keys when BUILDTEST_SPIDER_VIEW is all
        if config_opts["BUILDTEST_SPIDER_VIEW"] == "all":
            return sorted(list(self.module_dict.keys()))
        # return all keys whose module file path is part of
        # BUILDTEST_MODULEPATH
        else:
            unique_modules_set = set()
            for module in self.module_dict.keys():
                # unique_modules_set.add(module)
                for mpath in self.module_dict[module].keys():
                    for tree in config_opts["BUILDTEST_MODULEPATH"]:
                        if tree in mpath:
                            unique_modules_set.add(module)
                            break

            return sorted(list(unique_modules_set))


    def get_unique_fname_modules(self):
        """Return a list of unique canonical fullname of module
        where abspath to module is in one of the
        directories defined by BUILDTEST_MODULEPATH"""
        software_set = set()

        for module in self.get_unique_modules():
            for mpath in self.module_dict[module].keys():
                fname = ""
                if self.major_ver == 6:
                    fname = self.module_dict[module][mpath]["full"]
                elif self.major_ver == 7:
                    fname = self.module_dict[module][mpath]["fullName"]

                software_set.add(fname)


        return sorted(list(software_set))

    def get_modulefile_path(self):
        """Return a list of absolute path for all module files"""
        module_path_list  = []

        for k in self.get_unique_modules():
            for mpath in self.module_dict[k].keys():
                module_path_list.append(mpath)

        return module_path_list

    def get_parent_modules(self,modname):
        """Get Parent module for specified module file."""
        for key in self.module_dict.keys():
            for mod_file in self.module_dict[key].keys():
                mod_full_name = parent_mod_name = ""

                if self.major_ver == 6:
                    mod_full_name = self.module_dict[key][mod_file]["full"]
                elif self.major_ver == 7:
                    mod_full_name = self.module_dict[key][mod_file]["fullName"]

                if modname == mod_full_name:
                    if self.major_ver == 6:
                        parent_mod_name = self.module_dict[key][mod_file]["parent"]
                    elif self.major_ver == 7:
                        # for modules that dont have any parent the dictionary
                        # does not declare parentAA key in Lmod 7. in that
                        # case return empty list
                        if "parentAA" not in self.module_dict[key][mod_file]:
                            parent_mod_name = []
                        # otherwise retrieve first index from parentAA.
                        # ParentAA is a list of list
                        else:
                            parent_mod_name = self.module_dict[key][mod_file]["parentAA"][0]

                        return parent_mod_name

                    mod_parent_list = parent_mod_name
                    parent_module = []
                    # parent: is a list, only care about one entry which
                    # contain list of modules to be loaded separated by :
                    # First entry is default:<mod1>:<mod2> so skip first
                    # element

                    for entry in mod_parent_list[0].split(":")[1:]:
                        parent_module.append(entry)

                    return parent_module

        return []
    def get_version(self):
        """Return Lmod version"""
        cmd = os.getenv("LMOD_VERSION")
        version = [int(v) for v in cmd.split(".")]
        return version

def find_modules(module_args):
    """Return a list of module load commands from modules.json """

    module_list = module_args.split(",")
    fd = open(os.path.join(os.getenv("BUILDTEST_ROOT"), "var",
                           "modules.json"), "r")
    json_module = json.load(fd)

    all_modules = []
    for i in module_list:
        if i not in json_module.keys():
            print(f"{i} not in dictionary. Skipping to next module")
            continue
        for mpath in json_module[i].keys():
            for parent in json_module[i][mpath]["parent"]:
                parent.append(json_module[i][mpath]["fullName"])
                all_modules.append(parent)
                if config_opts["BUILDTEST_PARENT_MODULE_SEARCH"] == "first":
                    break

    module_cmd_list = []
    for i in all_modules:
        module_cmd = ' '.join(str(name) for name in i)
        module_cmd_list.append(f"module load {module_cmd}")

    return module_cmd_list

def get_module_list_by_tree(mod_tree):
    """ returns a list of module file paths given a module tree """

    modulefiles = []

    is_dir(mod_tree)
    for root, dirs, files in os.walk(mod_tree):
        for file in files:
            if file.endswith(".lua") or string_in_file("#%Module",os.path.join(root,file)):
                modulefiles.append(os.path.join(root,file))

    return modulefiles

module_obj = BuildTestModule()

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
        content["BUILDTEST_MODULEPATH"].remove(tree)

    fd.close()

    fd = open(BUILDTEST_CONFIG_FILE,"w")
    yaml.dump(content,fd,default_flow_style=False)
    fd.close()
    print (f"Removing module tree: {tree_list}")
    print (f"Configuration File: {BUILDTEST_CONFIG_FILE} has been updated")

def module_load_test(args):
    """Perform module load test for all modules in BUILDTEST_MODULEPATH"""

    module_stack = module_obj.get_unique_fname_modules()


    out_file = "/tmp/modules-load.out"
    err_file = "/tmp/modules-load.err"

    fd_out = open(out_file,"w")
    fd_err = open(err_file, "w")
    failed_modules = []
    passed_modules = []
    count = 0
    for mod_file in module_stack:
        count+=1
        cmd = ""
        parent_modules = module_obj.get_parent_modules(mod_file)
        for item in parent_modules:
            cmd += "module try-load {};  ".format(item)
        cmd +=  "module load " + mod_file
        print (cmd)

        ret = subprocess.Popen(cmd,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        out,err = ret.communicate()

        if ret.returncode == 0:
            msg = f"RUN: {count}/{len(module_stack)} STATUS: PASSED - " \
                  f"Testing module: {mod_file}"
            print (msg)
            passed_modules.append(mod_file)

            fd_out.write(msg + "\n")
            fd_out.write(cmd + "\n")
        else:
            msg = f"RUN: {count}/{len(module_stack)} STATUS: FAILED - " \
                  f"Testing module: {mod_file}"
            print (msg)
            failed_modules.append(mod_file)

            fd_err.write(msg + "\n")
            fd_err.write(cmd + "\n")

            for line in err.decode("utf-8").splitlines():
                fd_err.write(line)
        print ("{:_<80}".format(""))
    fd_out.close()
    fd_err.close()
    print (f"Writing Results to {out_file}")
    print (f"Writing Results to {err_file}")


    print ("{:_<80}".format(""))
    print ("{:>40}".format("Module Load Summary"))
    print ("{:<40} {}".format("Module Trees:",
                              config_opts["BUILDTEST_MODULEPATH"]))
    print ("{:<40} {}".format("PASSED: ", len(passed_modules)))
    print ("{:<40} {}".format("FAILED: ", len(failed_modules)))
    print ("{:_<80}".format(""))
    sys.exit(0)

def diff_trees(args_trees):
    """ display difference between module trees """

    # no comma found between two trees
    if args_trees.find(",") == -1:
        print ("Usage: --diff-trees /path/to/tree1,/path/to/tree2")
        sys.exit(1)
    else:
        id = args_trees.find(",")
        tree1 = args_trees[0:id]
        tree2 = args_trees[id+1:len(args_trees)]

        is_dir(tree1)
        is_dir(tree2)

        modlist1 = []
        modlist2 = []

        list1 = get_module_list_by_tree(tree1)
        list2 = get_module_list_by_tree(tree2)

        # strip full path, just get a list module file in format app/version
        for file in list1:
            name = os.path.basename(os.path.dirname(file))
            # strip out any file extension (.lua)
            ver = os.path.basename(os.path.splitext(file)[0])
            modlist1.append(os.path.join(name,ver))

        for file in list2:
            name = os.path.basename(os.path.dirname(file))
            # strip out any file extension (.lua)
            ver = os.path.basename(os.path.splitext(file)[0])
            modlist2.append(os.path.join(name,ver))

        # convert list into set and do symmetric difference between two sets
        diff_set =  set(modlist1).symmetric_difference(set(modlist2))
        if len(diff_set) == 0:
            print ("No difference found between module tree: ", tree1, " and module tree: ", tree2)
        # print difference between two sets by printing module file and stating  FOUND or NOTFOUND in the appropriate columns for Module Tree 1 or 2
        else:
            print ("\t\t\t Comparing Module Trees for differences in module files")
            print ("\t\t\t -------------------------------------------------------")

            print
            print ("Module Tree 1: ", tree1)
            print ("Module Tree 2: ", tree2)
            print
            print ("ID       |     Module                                                   |   Module Tree 1    |   Module Tree 2")
            print ("---------|--------------------------------------------------------------|--------------------|----------------------")

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


                print ((str(count) + "\t |").expandtabs(8), (i + "\t |").expandtabs(60) , (value1 + "\t |").expandtabs(18), value2)
                count = count + 1

def check_easybuild_module():
    """This method reports modules that are built by easybuild."""
    module_list = module_obj.get_modulefile_path()

    eb_string = "Built with EasyBuild version"
    count = 0
    for mpath in module_list:
        if string_in_file(eb_string,mpath):
            print(f"Module: {mpath} is built with Easybuild")
            count+=1

    print ("\n")
    print (f"Total Easybuild Modules: {count}")
    print (f"Total Modules Searched: {len(module_list)}")

def check_spack_module():
    """Report modules that are built by spack"""
    module_list = module_obj.get_modulefile_path()

    spack_string = "Module file created by spack"
    count = 0
    for mpath in module_list:
        if string_in_file(spack_string, mpath):
            print(f"Module: {mpath} is built with Spack")
            count+=1

    print("\n")
    print(f"Total Spack Modules: {count}")
    print(f"Total Modules Searched: {len(module_list)}")
