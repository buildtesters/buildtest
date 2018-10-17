############################################################################
#
#  Copyright 2017-2018
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
buildtest yaml subcommand entry point

@author: Shahzeb Siddqiui (shahzebmsiddiqui@gmail.com)
"""

import os
import sys
import yaml
from datetime import datetime

from buildtest.tools.config import config_opts
from buildtest.tools.file import create_dir
from buildtest.tools.software import get_unique_software, get_software_stack, get_toolchain_stack, get_binaries_from_application
from buildtest.tools.system import check_system_package_installed, get_binaries_from_systempackage, systempackage_installed_list


def func_yaml_subcmd(args):
    """ entry point to _buildtest yaml """

    if args.software:
        create_software_yaml(args.software, args.rebuild, args.overwrite)

    if args.package:
        create_system_yaml(args.package, args.rebuild, args.overwrite)

    if args.all_software:
        create_all_software_yaml(args.rebuild, args.overwrite)

    if args.all_package:
        create_all_system_yaml(args.rebuild, args.overwrite)

    sys.exit(0)


def create_system_yaml(name, rebuild=False, overwrite=False):
    """ create YAML configuration for binary test for system package """

    destdir = os.path.join(config_opts['BUILDTEST_CONFIGS_REPO_SYSTEM'],name)
    yamlfile = os.path.join(destdir,"command.yaml")

    # if yaml file exists and --rebuild, --overwrite is not specified then do nothing and return from method
    if os.path.isfile(yamlfile) and not rebuild and not overwrite:
        print(f"File already exist: {yamlfile}")
        return
    # if yaml file exist and --rebuild is specified.
    elif os.path.isfile(yamlfile) and rebuild and not overwrite:
        yamlfile = os.path.join(destdir, datetime.now().strftime("command_%H_%M_%d_%m_%Y.yaml"))
    elif os.path.isfile(yamlfile) and overwrite:
        print(f"Overwriting content of yaml file: {yamlfile}")

    # if directory is not present then create it
    create_dir(destdir)

    # check if package is installed in system before creating yaml files
    check_system_package_installed(name)

    # get binary from system package
    binary = get_binaries_from_systempackage(name)
    # get_binary_from_application return None if there are no binaries found in application.
    if binary == None:
        return
    binary_list = []
    [binary_list.extend(["which " + value]) for value in binary.values()]

    fd = open(yamlfile,"w")
    description = {"description": "Binary test for " + name}
    yaml.dump(description,fd,default_flow_style=False)
    binarydict = { "binaries": binary_list }
    with open(yamlfile, 'a') as outfile:
        yaml.dump(binarydict, outfile, default_flow_style=False)

    print ("Please check YAML file ", yamlfile, " and fix test accordingly")


def create_software_yaml(module_name, rebuild=False, overwrite=False):
    """ create yaml configuration for software packages """

    binary = get_binaries_from_application(module_name)
    # get_binary_from_application return None if there are no binaries found in application.
    if binary == None:
        return
    toolchain_stack = get_toolchain_stack()
    toolchain_name = [name.split("/")[0] for name in toolchain_stack]
    # get module version
    module_version = module_name.split("/")[1]
    # remove any toolchain from module version when figuring path to yaml file
    for tc in toolchain_name:
        idx = module_version.find(tc)

        if idx != -1:
            module_name = module_name.split("/")[0] + "/" + module_version[0:idx-1]



    lowercase_module_name = module_name.lower()
    destdir = os.path.join(config_opts['BUILDTEST_CONFIGS_REPO_SOFTWARE'],lowercase_module_name)
    yamlfile = os.path.join(destdir,"command.yaml")
    # if yaml file exists and --rebuild, --overwrite is not specified then do nothing and return from method
    if os.path.isfile(yamlfile) and not rebuild and not overwrite:
        print(f"File already exist: {yamlfile}")
        return
    # if yaml file exist and --rebuild is specified.
    elif os.path.isfile(yamlfile) and rebuild and not overwrite:
        yamlfile = os.path.join(destdir, datetime.now().strftime("command_%H_%M_%d_%m_%Y.yaml"))
    elif os.path.isfile(yamlfile) and overwrite:
        print(f"Overwriting content of yaml file: {yamlfile}")


    # if directory is not present then create it
    create_dir(destdir)

    binary_list = []
    #print (binary)

    #for value in binary.values():
    #    print(value,type(value))
        #binary_list.extend("which" + value)
    [binary_list.extend(["which " + value]) for value in binary.values()]
    binarydict = { "binaries": binary_list }

    fd = open(yamlfile,"w")
    description = {"description": "Binary test for " + module_name}
    yaml.dump(description,fd,default_flow_style=False)


    with open(yamlfile, 'a') as outfile:
        yaml.dump(binarydict, outfile, default_flow_style=False)

    print ("Please check YAML file ", yamlfile, " and fix test accordingly")


def create_all_software_yaml(rebuild=False,overwrite=False):
    """ run create_software_yaml for every application in software stack """
    list = get_software_stack()
    for item in list:
        create_software_yaml(item,rebuild,overwrite)

def create_all_system_yaml(rebuild=False,overwrite=False):
    """ run create_system_yaml for every system package installed in system """
    list = systempackage_installed_list()
    for item in list:
        create_system_yaml(item,rebuild,overwrite)
