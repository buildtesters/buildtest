"""
This module implements all the list operation in buildtest which include the
following:
1. List Software (buildtest list --software)
2. List Full Module Name and associated module file (buildtest list --modules)
3. List easyconfigs from module tree (buildtest list --easyconfigs)
"""

import os
from termcolor import colored, cprint
from buildtest.tools.modules import module_obj
from buildtest.tools.easybuild import find_easyconfigs


def func_list_subcmd(args):
    """This method is the entry point for ``buildtest list`` subcommand.

    :param args: dict of command line arguments passed
    :type args: dict, required
    """

    if args.easyconfigs:
        find_easyconfigs()
    if args.software:
        list_software()
    if args.modules:
        list_modules()


def list_software():
    """This method gets unique software from spider and prints the software
    with total count. This method invokes **get_unique_modules()** which is part
    of **BuildTestModule** and module_obj is an instance object.

    This method implements ``buildtest list --software``.
    """

    module_stack = module_obj.get_unique_modules()

    for item in module_stack:
        print(item)

    print("\n")
    print("Total Software Packages: ", len(module_stack))


def list_modules():
    """This method prints the Full Module Name and ModuleFile Path. This
    method invokes method **get_module_spider_json()**, **get_version()**,
    **get_unique_modules()** from **BuildTestModule** class where module_obj is an
    instance of BuildTestModule.

    Modules with .lua extension are printed in green using **cprint()**.
    A total count of lua,non-lua, and total modules are reported

    This method implements  ``buildtest list --modules``.
    """

    module_dict = module_obj.get_module_spider_json()
    lmod_version = module_obj.get_version()
    major_ver = lmod_version[0]

    module_stack = module_obj.get_unique_modules()

    text = """
    Full Module Name                     |      ModuleFile Path
-----------------------------------------|----------------------------- """
    print(text)

    count = 0
    lua_modules = non_lua_modules = 0

    for module in module_stack:
        for mpath in module_dict[module].keys():
            count += 1
            fullName = ""
            if major_ver == 6:
                fullName = module_dict[module][mpath]["full"]
            elif major_ver == 7:
                fullName = module_dict[module][mpath]["fullName"]

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
