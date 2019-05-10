############################################################################
#
#  Copyright 2017-2019
#
#  https://github.com/HPC-buildtest/buildtest-framework
#
#  This file is part of buildtest.
#
#  buildtest is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  buildtest is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with buildtest.  If not, see <http://www.gnu.org/licenses/>.
#############################################################################


"""
This module implements all the list operation in buildtest which include the
following:
1. List software (buildtest list -ls)
2. List Software and associated module file (buildtest list -svr)
3. List easyconfigs in module tree (buildtest list --easyconfigs)
"""

import json
import os
import sys
from termcolor import colored, cprint

from buildtest.tools.config import config_opts
from buildtest.tools.modules import module_obj
from buildtest.tools.easybuild import find_easyconfigs



def func_list_subcmd(args):
    """ This method is the entry point for buildtest list subcommand."""

    if args.easyconfigs:
        find_easyconfigs()
    if args.software:
        list_software(args)
    if args.modules:
        list_modules(args)



def list_software(args):
    """ This method gets unique software from spider. """

    module_stack = module_obj.get_unique_modules()

    [ print (item) for item in module_stack]

    print ("\n")
    print ("Total Software Packages: ", len(module_stack))


def list_modules(args):
    """ This method implements  buildtest list -svr """

    module_dict = module_obj.get_module_spider_json()
    lmod_version = module_obj.get_version()
    major_ver = lmod_version[0]

    module_stack = module_obj.get_unique_modules()


    text = """
    Full Module Name                     |      ModuleFile Path
-----------------------------------------|----------------------------- """
    print (text)

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

            if os.path.splitext(mpath)[1] == ".lua":
                text = (fullName + "\t |").expandtabs(40) + "\t" + mpath
                cprint(text, 'green')
                lua_modules += 1
            else:
                print((fullName + "\t |").expandtabs(40) + "\t" + mpath)
                non_lua_modules += 1

    print ("\n")
    print (f"Total Software Modules: {count}")
    msg = f"Total LUA Modules: {lua_modules}"
    cprint(msg,'green')
    print(f"Total non LUA Modules: {non_lua_modules}")