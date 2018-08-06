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
This module generates yaml configuration files

:author: Shahzeb Siddiqui (Pfizer)
"""

import os
import sys
import yaml

from buildtest.tools.config import config_opts
from buildtest.tools.file import create_dir
from buildtest.tools.software import get_unique_software, get_toolchain_stack, get_binaries_from_application
from buildtest.tools.system import check_system_package_installed, get_binaries_from_systempackage

def create_system_yaml(name):
    """ create YAML configuration for binary test for system package """

    destdir = os.path.join(config_opts['BUILDTEST_CONFIGS_REPO_SYSTEM'],name)
    yamlfile = os.path.join(destdir,"command.yaml")

    # if yaml file exists then exit out
    if os.path.isfile(yamlfile):
        print "YAML file already exists, please check: ", yamlfile
        sys.exit(0)

    # if directory is not present then create it
    create_dir(destdir)

    # check if package is installed in system before creating yaml files
    check_system_package_installed(name)

    # get binary from system package
    binary = get_binaries_from_systempackage(name)

    binary_list = []
    [binary_list.extend([value]) for key,value in binary.items()]

    fd = open(yamlfile,"w")
    binarydict = { "binaries": binary_list }
    with open(yamlfile, 'a') as outfile:
        yaml.dump(binarydict, outfile, default_flow_style=False)

    print "Please check YAML file", yamlfile, " and fix test accordingly"
    sys.exit(0)

def create_software_yaml(module_name):
    """ create yaml configuration for software packages """

    binary = get_binaries_from_application(module_name)

    toolchain_stack = get_toolchain_stack()
    toolchain_name = [name.split("/")[0] for name in toolchain_stack]
    # get module version
    module_version = module_name.split("/")[1]
    # remove any toolchain from module version when figuring path to yaml file
    for tc in toolchain_name:
        idx = module_version.find(tc)

        if idx != -1:
            module_name = module_name.split("/")[0] + "/" + module_version[0:idx-1]



    module_name = module_name.lower()
    destdir = os.path.join(config_opts['BUILDTEST_CONFIGS_REPO_SOFTWARE'],module_name)
    yamlfile = os.path.join(destdir,"command.yaml")
    # if yaml file exists then exit out
    if os.path.isfile(yamlfile):
        print "YAML file already exists, please check: ", yamlfile
        sys.exit(0)

    # if directory is not present then create it
    create_dir(destdir)

    binary_list = []
    [binary_list.extend([value]) for key,value in binary.items()]

    fd = open(yamlfile,"w")
    binarydict = { "binaries": binary_list }
    with open(yamlfile, 'a') as outfile:
        yaml.dump(binarydict, outfile, default_flow_style=False)

    print "Please check YAML file", yamlfile, " and fix test accordingly"
    sys.exit(0)
