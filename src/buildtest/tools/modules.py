"""
This python module does the following
	 - get module listing
	 - get unique application
	 - list easybuild/spack modules
	 - get unique application version
	 - Run module load test
	 - Return all parent modules
	 - List modules that depend on other modules
	 - check if easyconfig passes
	 - Get module permutation choices
"""
import json
import os
import subprocess
from termcolor import cprint

from buildtest.tools.config import (
    config_opts,
    BUILDTEST_CONFIG_FILE,
    BUILDTEST_MODULE_FILE,
)
from buildtest.tools.file import string_in_file, is_dir
from buildtest.tools.modulesystem.module_difference import diff_trees
from buildtest.tools.modulesystem.collection import get_buildtest_module_collection


def func_module_subcmd(args):
    """Entry point for "buildtest module" subcommand.

    :param args: command line arguments passed to buildtest
    :type args: dict, required
    """

    if args.diff_trees:
        diff_trees(args.diff_trees)

    if args.easybuild:
        check_easybuild_module()

    if args.spack:
        check_spack_module()

    if args.module_deps:
        find_module_deps(args.module_deps)


class BuildTestModule:
    """This class BuildTestModule provides methods to retrieve
    unique modules (get_unique_modules()), unique modules by full name
    (get_unique_fname_modules()), list of module file paths (get_module_file_path()),
    get parent modules (get_parent_modules()).

    In addition this method can retrieve spider dictionary using get_module_spider_json()
    and Lmod version using get_version()
    """

    def __init__(self):
        """Constructor method. The constructor will run spider command and store the output
        in self.module_dict
        """
        self.moduletree = ":".join(map(str, config_opts["BUILDTEST_MODULEPATH"]))

        cmd = f"$LMOD_DIR/spider -o spider-json {self.moduletree}"
        out = subprocess.check_output(cmd, shell=True).decode("utf-8")
        self.module_dict = json.loads(out)
        self.major_ver = self.get_version()[0]


    def get_module_spider_json(self):
        """Returns self.module_dict which is the json output of spider.

        :rtype: dict
        """
        return self.module_dict

    def get_unique_modules(self):
        """Return a sorted list of unique keys (software name). If
        BUILDTEST_SPIDER_VIEW == all then it will return all keys
        from spider otherwise it will return keys whose module file path
        is in BUILDTEST_MODULEPATH

        :rtype: list
        """

        # return all keys when BUILDTEST_SPIDER_VIEW is all
        if config_opts["BUILDTEST_SPIDER_VIEW"] == "all":
            return sorted(list(self.module_dict.keys()))
        # return all keys whose module file path is part of
        # BUILDTEST_MODULEPATH
        else:
            unique_modules_set = set()
            for module in self.module_dict.keys():
                for mpath in self.module_dict[module].keys():
                    for tree in config_opts["BUILDTEST_MODULEPATH"]:
                        if tree in mpath:
                            unique_modules_set.add(module)
                            break

            return sorted(list(unique_modules_set))

    def list_modules(self):
        """This method gets unique software from spider and prints the software
           with total count. This method invokes **get_unique_modules()** which is part
           of **BuildTestModule** and module_obj is an instance object.

           This method implements ``buildtest list --software``.
           """
        text = """
            Full Module Name                     |      ModuleFile Path
        -----------------------------------------|----------------------------- """
        print(text)

        count = 0
        lua_modules = non_lua_modules = 0

        for module in self.get_unique_modules():
            for mpath in self.module_dict[module].keys():
                count += 1
                fullName = ""
                if self.major_ver == 6:
                    fullName = self.module_dict[module][mpath]["full"]
                elif self.major_ver >= 7:
                    fullName = self.module_dict[module][mpath]["fullName"]

                # print lua modules in green
                if os.path.splitext(mpath)[1] == ".lua":
                    text = (fullName + "\t |").expandtabs(40) + "\t" + mpath
                    cprint(text, "green")
                    lua_modules += 1
                else:
                    print((fullName + "\t |").expandtabs(40) + "\t" + mpath)
                    non_lua_modules += 1

        print("\n")
        print(f"Total Software Modules: {count}")
        msg = f"Total LUA Modules: {lua_modules}"
        cprint(msg, "green")
        print(f"Total non LUA Modules: {non_lua_modules}")

    def get_unique_fname_modules(self):
        """Return a sorted list of unique canonical fullname of module where abspath
        to module is in one of the directories defined by BUILDTEST_MODULEPATH. Full
        module name can be retrieved using key "full" in Lmod 6 and "fullName" in Lmod 7

        :rtype: list
        """
        software_set = set()

        for module in self.get_unique_modules():
            for mpath in self.module_dict[module].keys():
                fname = ""
                if self.major_ver == 6:
                    fname = self.module_dict[module][mpath]["full"]
                elif self.major_ver >= 7:
                    fname = self.module_dict[module][mpath]["fullName"]

                software_set.add(fname)

        return sorted(list(software_set))

    def get_modulefile_path(self):
        """Return a list of absolute path for all module files.

        :rtype: list
        """
        module_path_list = []

        for k in self.get_unique_modules():
            for mpath in self.module_dict[k].keys():
                module_path_list.append(mpath)

        return module_path_list

    def get_parent_modules(self, modname):
        """Get Parent module for a module name. This can be retrieved by
        key "parent" in Lmod 6 or "parentAA" in Lmod 7.

        :param modname: full canonical module name
        :type modname: str, required

        :return: list of parent module combination
        :rtype: list
        """
        for key in self.module_dict.keys():
            for mod_file in self.module_dict[key].keys():
                mod_full_name = parent_mod_name = ""

                if self.major_ver == 6:
                    mod_full_name = self.module_dict[key][mod_file]["full"]
                elif self.major_ver >= 7:
                    mod_full_name = self.module_dict[key][mod_file]["fullName"]

                if modname == mod_full_name:
                    if self.major_ver == 6:
                        parent_mod_name = self.module_dict[key][mod_file]["parent"]
                    elif self.major_ver >= 7:
                        # for modules that dont have any parent the dictionary
                        # does not declare parentAA key in Lmod 7. in that
                        # case return empty list
                        if "parentAA" not in self.module_dict[key][mod_file]:
                            parent_mod_name = []
                        # otherwise retrieve first index from parentAA.
                        # ParentAA is a list of list
                        else:
                            parent_mod_name = self.module_dict[key][mod_file][
                                "parentAA"
                            ][0]

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
        """Return Lmod major version.

        :rtype: int
        """
        cmd = os.getenv("LMOD_VERSION")
        version = [int(v) for v in cmd.split(".")]
        return version


def get_all_parents():
    """Retrieve all parent modules. This is used as choice field to
    buildtest module -d <parent-module>. This retrieves parent
    module by reading modules.json

    :return: list of unique parent combination.
    :rtype: List
    """

    fd = open(BUILDTEST_MODULE_FILE, "r")
    module_json = json.load(fd)
    fd.close()

    parent_set = set()
    for module in module_json.keys():
        for mpath in module_json[module].keys():
            for parent_comb in module_json[module][mpath]["parent"]:
                for parent_module in parent_comb:
                    parent_set.add(parent_module)

    return sorted(list(parent_set))


module_obj = BuildTestModule()


def find_module_deps(parent_module):
    """Return a list of absolute path to module file that depends on a parent module.
    This method implements "buildtest module -d". This module reads
    modules.json and finds the absolute path for parent module file. Next
    it reads reads the parent module file and prints the content. Afterwards
    it searches for all modules that contains parent module in key "parent" and
    adds modulefile  path to list.

    :param parent_module: full canonical name of parent module
    :type parent_module: str, required
    """

    parent_list_found = []

    fd = open(BUILDTEST_MODULE_FILE, "r")
    module_json = json.load(fd)
    fd.close()
    # find the parent module file path in order to read and print module file
    for mod in module_json.keys():
        for mpath in module_json[mod].keys():
            if module_json[mod][mpath]["fullName"] == parent_module:
                filepath = mpath
                break
    print(f"Module File: {filepath}")

    # add module file path where parent module is found in "parent" key
    for mod in module_json.keys():
        for mpath in module_json[mod].keys():
            for parent_list in module_json[mod][mpath]["parent"]:
                if parent_module in parent_list:
                    parent_list_found.append(mpath)
                    break

    print(f"Modules that depend on {parent_module}")
    for file in parent_list_found:
        print(file)

    print("\n")
    print(f"Total Modules Found: {len(parent_list_found)}")


def find_modules(module_args):
    """Return a list of module load commands from modules.json

    :param module_args: comma separated list of modules
    :type module_args: str, required

    :return: a list of full canonical module names to be used for module load
    :rtype: List
    """

    module_list = module_args.split(",")
    fd = open(BUILDTEST_MODULE_FILE, "r")
    json_module = json.load(fd)

    all_modules = []
    for i in module_list:
        if i not in json_module.keys():
            print(f"{i} not in dictionary. Skipping to next module")
            continue
        for mpath in json_module[i].keys():
            # no parent combination then simply add module and go to next entry
            if len(json_module[i][mpath]["parent"]) == 0:
                # all_modules is a nested list using tmp to add fullName to list which
                # can be added to a nested list
                tmp = []
                tmp.append(json_module[i][mpath]["fullName"])
                all_modules.append(tmp)
                continue

            for parent in json_module[i][mpath]["parent"]:
                parent.append(json_module[i][mpath]["fullName"])
                all_modules.append(parent)

                # load the first parent combination, if BUILDTEST_PARENT_MODULE_SEARCH=first then terminate asap
                if config_opts["BUILDTEST_PARENT_MODULE_SEARCH"] == "first":
                    break

    module_cmd_list = []
    for i in all_modules:
        module_cmd = " ".join(str(name) for name in i)
        module_cmd_list.append(f"module load {module_cmd}")

    return module_cmd_list


def module_load_test(args):
    """Perform module load test for all modules in BUILDTEST_MODULEPATH.
    Writes output of module load to file and redirects error to .err file.
    This method implements command: ``buildtest module loadtest``.

    :param args: commmand line arguments to buildtest
    :type args: dict, required
    :rtype: exit 0
    """

    module_stack = module_obj.get_unique_fname_modules()

    out_file = f"{config_opts['BUILDTEST_TESTDIR']}/modules-load.out"
    err_file = f"{config_opts['BUILDTEST_TESTDIR']}/modules-load.err"

    fd_out = open(out_file, "w")
    fd_err = open(err_file, "w")
    failed_modules = []
    passed_modules = []
    count = 0
    for mod_file in module_stack:
        count += 1
        cmd = []
        parent_modules = module_obj.get_parent_modules(mod_file)
        for item in parent_modules:
            cmd.append(f"module try-load {item}; ")
        cmd.append(f"module load {mod_file};")

        module_load_cmd = " ".join(cmd)

        ret = subprocess.Popen(
            module_load_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        out, err = ret.communicate()

        if ret.returncode == 0:
            msg = (
                f"RUN: {count}/{len(module_stack)} STATUS: PASSED - "
                f"Testing module command: {module_load_cmd}"
            )
            print(msg)
            passed_modules.append(mod_file)

            fd_out.write(msg + "\n")
            fd_out.write(module_load_cmd + "\n")
        else:
            msg = (
                f"RUN: {count}/{len(module_stack)} STATUS: FAILED - "
                f"Testing module command: {module_load_cmd}"
            )
            print(msg)
            failed_modules.append(mod_file)

            fd_err.write(msg + "\n")
            fd_err.write(module_load_cmd + "\n")

            for line in err.decode("utf-8").splitlines():
                fd_err.write(line)
        print("{:_<80}".format(""))
    fd_out.close()
    fd_err.close()
    print(f"Writing Results to {out_file}")
    print(f"Writing Results to {err_file}")

    print("{:_<80}".format(""))
    print("{:>40}".format("Module Load Summary"))
    print("{:<40} {}".format("Module Trees:", config_opts["BUILDTEST_MODULEPATH"]))
    print("{:<40} {}".format("PASSED: ", len(passed_modules)))
    print("{:<40} {}".format("FAILED: ", len(failed_modules)))
    print("{:_<80}".format(""))



def get_module_permutation_choices():
    """This method returns a choice field for module permutation option
    (``buildtest build --modules``). It will read json file BUILDTEST_MODULE_FILE and return
    list of keys found in the file.

    :return: List of unique software name
    :rtype: list
    """

    fd = open(BUILDTEST_MODULE_FILE, "r")
    content = json.load(fd)
    fd.close()
    return content.keys()


def check_easybuild_module():
    """This method reports modules that are built by easybuild. This implements
    command ``buildtest module --easybuild``
    """
    module_list = module_obj.get_modulefile_path()

    eb_string = "Built with EasyBuild version"
    count = 0
    print("Modules built with Easybuild")
    print("{:-<80}".format(""))
    for mpath in module_list:
        if string_in_file(eb_string, mpath):
            print(mpath)
            count += 1

    print("\n")
    print(f"Total Easybuild Modules: {count}")
    print(f"Total Modules Searched: {len(module_list)}")


def check_spack_module():
    """This method reports modules that are built by Spack. This implements
    command ``buildtest module --spack``
    """
    module_list = module_obj.get_modulefile_path()

    spack_string = "Module file created by spack"
    count = 0
    print("Modules built with Spack")
    print("{:-<80}".format(""))
    for mpath in module_list:
        if string_in_file(spack_string, mpath):
            print(mpath)
            count += 1

    print("\n")
    print(f"Total Spack Modules: {count}")
    print(f"Total Modules Searched: {len(module_list)}")


def module_selector(user_collection, buildtest_module_collection):
    """Return a module load or module restore string from active module, user collection, or buildtest module collection """
    modules = []
    if config_opts["BUILDTEST_MODULE_FORCE_PURGE"]:
        modules.append("module --force purge")
    else:
        modules.append("module purge")

    if buildtest_module_collection is not None:
        module_collection = get_buildtest_module_collection(buildtest_module_collection)
        modules += [f"module load {x}" for x in module_collection]
        return modules

    if user_collection is not None:
        modules += [f"module restore {user_collection}"]
        return modules

    cmd = "module -t list"
    out = subprocess.getoutput(cmd)

    # output of module -t list when no modules are loaded is "No modules
    #  loaded"

    if out != "No modules loaded":

        modules_load_list = [f"module load {x}" for x in out.split()]
        modules += modules_load_list
        return modules
