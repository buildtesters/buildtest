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
    BUILDTEST_MODULE_FILE
)


from buildtest.tools.file import string_in_file, walk_tree
from buildtest.tools.modulesystem.module_difference import diff_trees
from buildtest.tools.modulesystem.collection import get_buildtest_module_collection


class BuildTestModule:
    """This class ``BuildTestModule`` parses content of Lmod spider and implements several methods used by buildtest.
        The following methods are implemented:
      ``get_module_spider_json()`` - get full content of spider as json object
      ``get_unique_modules()`` - get unique module names (i.e top level key of spider)
      ``get_modulefile_path()`` - get list of all absolute path to modulefiles
      ``get_parent_modules()`` - get parent module entry
      ``get_version()`` - retrieves Lmod version
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

    def get_modulefile_path(self):
        """Return a list of absolute path for all module files.

        :rtype: list
        """
        module_path_list = []

        for k in self.get_unique_modules():
            for mpath in self.module_dict[k].keys():
                if config_opts["BUILDTEST_SPIDER_VIEW"] == "current":
                    # only add full canonical module name if module file location is in one of the trees defined by BUILDTEST_MODULEPATH
                    for tree in config_opts["BUILDTEST_MODULEPATH"]:
                        if tree in mpath:
                            module_path_list.append(mpath)
                            break
                else:
                    module_path_list.append(mpath)

        return sorted(module_path_list)

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
        :return: a list of integers containing Lmod version
        :rtype: list
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
    filepath = ""
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
            if os.path.basename(module_json[mod][mpath]["fullName"]).startswith(".version") or os.path.basename(module_json[mod][mpath]["fullName"]).startswith(
                ".modulerc"):
                continue

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
                # only add the first parent module combination and then break loop.
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

    module_stack = module_obj.get_modulefile_path()
    module_dict = module_obj.get_module_spider_json()
    lmod_major_ver = module_obj.get_version()[0]
    out_file = f"{config_opts['BUILDTEST_TESTDIR']}/modules-load.out"
    err_file = f"{config_opts['BUILDTEST_TESTDIR']}/modules-load.err"

    fd_out = open(out_file, "w")
    fd_err = open(err_file, "w")
    failed_modules = []
    passed_modules = []
    count = 0
    # variable used to break out of nested loop during module loadtest
    break_loop = False
    login_shell = config_opts["module"]["loadtest"]["login"]
    purge_modules = config_opts["module"]["loadtest"]["purge_modules"]
    numtest = config_opts["module"]["loadtest"]["numtest"]
    # override login value if specified from command line
    if args.login:
        login_shell = args.login
    # override purge_modules if specified from command line
    if args.purge_modules:
        purge_modules = args.purge_modules

    if args.numtest:
        numtest = args.numtest


    for key in module_dict.keys():
        for mpath in module_dict[key].keys():
            if mpath not in module_stack:
                continue


            fname = ""
            parent_modules = []
            if lmod_major_ver == 6:
                fname = module_dict[key][mpath]["full"]
                parent_modules = module_dict[key][mpath]["parent"][0].split(":")[1:]
            elif lmod_major_ver >= 7:
                fname = module_dict[key][mpath]["fullName"]
                if "parentAA" not in module_dict[key][mpath]:
                    parent_modules = []
                else:
                    parent_modules = module_dict[key][mpath]["parentAA"][0]

            # need to skip module loadtest for any modules that have .version or .modulerc in name
            if os.path.basename(fname).startswith(".version") or os.path.basename(fname).startswith(".modulerc"):
                continue
            cmd = []

            # invoke login shell (bash --login -c)
            if login_shell:
                cmd.append("bash")
                cmd.append("--login")
                cmd.append("-c")

            # if purge_modules set then run "module purge" before loading modules
            if purge_modules:
                cmd.append("module purge;")
            for item in parent_modules:
                cmd.append(f"module try-load {item}; ")
            cmd.append(f"module load {fname};")
            module_load_cmd = " ".join(cmd)

            ret = subprocess.Popen(
                module_load_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )

            out, err = ret.communicate()
            count+=1
            if ret.returncode == 0:
                msg = (
                    f"RUN: {count}  STATUS: PASSED - "
                    f"Testing module command: {module_load_cmd} ( File: {mpath} )"
                )
                print(msg)
                passed_modules.append(mpath)

                fd_out.write(msg + "\n")
                fd_out.write(module_load_cmd + "\n")
            else:
                msg = (
                    f"RUN: {count} STATUS: FAILED - "
                    f"Testing module command: {module_load_cmd} ( File: {mpath} )"
                )
                print(msg)
                failed_modules.append(mpath)

                fd_err.write(msg + "\n")
                fd_err.write(module_load_cmd + "\n")

                for line in err.decode("utf-8").splitlines():
                    fd_err.write(line)
            print("{:_<80}".format(""))

            # exit module loadtest if numtest is reached
            if count >= numtest and numtest > 0:
                break_loop = True
                break
        # exit module loadtest when numtest limit is reached
        if break_loop:
            break

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

    return

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
    """Return a module load or module restore string from active module, user collection, or buildtest module collection
    :rtype: list
    :param user_collection: Lmod user collection name passed as argument (``--collection``) to buildtest
    :param buildtest_module_collection:  module collection index passed as argument (``--module-collection``) to buildtest
    :return: Return a list of modules based on the type of modules passed to this method
    """
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
        return

def list_software():
    """This method gets unique software from spider and prints the software
    with total count. This method invokes ``get_unique_modules()`` which is part
    of ``BuildTestModule`` and module_obj is an instance object.

    This method implements ``buildtest module --software``.
    """

    module_stack = module_obj.get_unique_modules()

    for item in module_stack:
        print(item)

    print("\n")
    print("Total Software Packages: ", len(module_stack))

def list_modules(args):
    """This method gets unique software from spider and prints the software
       with total count.

       This method implements ``buildtest module list``.
       """

    querylimit = config_opts["module"]["list"]["querylimit"]
    module_filter_include = config_opts["module"]["list"]["filter"]["include"]
    exclude_version_files = config_opts["module"]["list"]["exclude_version_files"]

    # override option if command line option --querylimit is passed
    if args.querylimit:
        querylimit = args.querylimit
    # override option if command line option --filter-include is passed
    if args.filter_include:
        module_filter_include = args.filter_include
    # override option if command line option --exclude-version-files is passed
    if args.exclude_version_files:
        exclude_version_files = args.exclude_version_files

    text = """
    Full Module Name                     |      ModuleFile Path
-----------------------------------------|----------------------------- """
    print(text)

    count = 0
    lua_modules = non_lua_modules = 0

    modfile_abspaths = module_obj.get_modulefile_path()
    module_dict = module_obj.get_module_spider_json()
    lmod_major_version = module_obj.get_version()[0]
    # print (module_filter_include)
    # for module in self.get_unique_modules():
    dict = {}
    for module in module_dict.keys():
        for mpath in module_dict[module].keys():
            # skip to next entry if modulefile not found in list of modulefile paths
            if mpath not in modfile_abspaths:
                continue

            fullName = ""
            if lmod_major_version == 6:
                fullName = module_dict[module][mpath]["full"]
            elif lmod_major_version >= 7:
                fullName = module_dict[module][mpath]["fullName"]

            if exclude_version_files:
                if os.path.basename(fullName).startswith(".version") or os.path.basename(fullName).startswith(
                        ".modulerc"):
                    continue

            # if filter include list is not empty, then only add module full name that correspond to list.
            if len(module_filter_include) > 0:
                strip_fname_by_slash = ""
                # print (fullName,fullName.index("/"))
                if fullName.find("/") > 0:
                    strip_fname_by_slash = fullName.split("/")[0]
                else:
                    strip_fname_by_slash = fullName

                if strip_fname_by_slash in module_filter_include:
                    dict[mpath] = fullName
            # otherwise add all modules
            else:
                dict[mpath] = fullName

    for mpath, fname in dict.items():
        count += 1
        # print lua modules in green
        if os.path.splitext(mpath)[1] == ".lua":
            text = (fname + "\t |").expandtabs(40) + "\t" + mpath
            cprint(text, "green")
            lua_modules += 1
        else:
            print((fname + "\t |").expandtabs(40) + "\t" + mpath)
            non_lua_modules += 1

        # only print modules up to the query limit and query limit is a non-negative number
        if count >= querylimit and querylimit > 0:
            break

    print("\n")
    print(f"Total Software Modules: {count}")
    msg = f"Total LUA Modules: {lua_modules}"
    cprint(msg, "green")
    print(f"Total non LUA Modules: {non_lua_modules}")

def list_all_parent_modules():
    """Implements method ``buildtest module --list-all-parents``"""
    parent_modules = get_all_parents()

    fd = open(BUILDTEST_MODULE_FILE, "r")
    module_json = json.load(fd)
    fd.close()

    # find abspath of parent module file and print the parent module and modulefile path
    for x in parent_modules:
        for module in module_json.keys():
            for mpath in module_json[module].keys():
                if module_json[module][mpath]["fullName"] in x:
                    print (x, mpath)

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

    if args.list_all_parents:
        list_all_parent_modules()

    if args.software:
        list_software()