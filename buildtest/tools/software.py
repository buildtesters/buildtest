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
Application & Toolchain name & version query functions

:author: Shahzeb Siddiqui (Pfizer)
"""

import os
import logging
import stat
import subprocess
import sys


from buildtest.tools.config import logID, config_opts
from buildtest.tools.easybuild import get_toolchains, get_module_root
from buildtest.tools.modules import get_module_list
from buildtest.tools.utility import sset


def get_unique_software():
    """
    returns a set of software packages found in the module tree
    """
    modtrees = get_module_root()
    logger = logging.getLogger(logID)

    logger.info("Traversing Module Tree: %s to find all unique software", modtrees)

    #moduletreelist=moduletrees.split(":")
    module_set=set()
    #for moduletree in moduletreelist:
    modulelist=get_module_list()

    # extract module name and add to module set
    for module in modulelist:
	    # extract the module name from filepath
        modulename=os.path.basename(os.path.dirname(module))
        module_set.add(modulename)

    logger.info("List of modules found:")
    logger.info("----------------------------------------")
    logger.info("Software = %s", list(module_set))
    return sorted(module_set)


def get_software_stack():
    """
    returns a set of software-version collection found in module files. Duplicates are
    ignored for instance, same package version is built with two different toolchains
    """
    moduleversion_set=set()
    modulelist=get_module_list()

    for module in modulelist:
        # extract the module name and version from the file path returned from find
        modulename = os.path.basename(os.path.dirname(module))
        version=os.path.basename(module)

        ext = os.path.splitext(version)[1]
        # skip .version files
        if ext == ".version":
            continue

        # if modulefile is lua extension then strip extension from version
        if ext == ".lua":
            version=os.path.splitext(version)[0]

        moduleversion_set.add(modulename+"/"+version)

    return sorted(moduleversion_set)

def get_toolchain_stack():
	""" return a list of toolchain used as choices for -t option in
	buildtest menu"""


	software_stack = get_software_stack()
	toolchains = get_toolchains()

	modified_toolchain_list = []
	for app in software_stack:
		# get app name, format: <app>/<version>
		appname = app.split("/")[0]
		# if software is part of easybuild toolchain list
		if appname in toolchains:
			modified_toolchain_list.append(app)

	return modified_toolchain_list


def software_version_relation():
    """
    relationship between software name and version. The function will return a
    dictionary with key values as software name and values will be a set of version
    """
    modulelist=get_module_list()

    # dictionary used for keeping a relationship between software name and its corresponding modulefile
    module_dict = {}
    # create a dictionary where key is modulefile path and the value is application name
    for app in modulelist:
        module_dict[app] = os.path.basename(os.path.dirname(app))

    return module_dict

def ebyaml_choices():
    """return a list of software packages for which you can generate yaml configuration for binary testing"""

    yaml_apps = os.listdir(config_opts['BUILDTEST_CONFIGS_REPO_SOFTWARE'])

    software_list = get_software_stack()
    #print yaml_apps
    remove_app_list = []

    for module in software_list:
        name = module
        # if directory found in BUILDTEST_CONFIGS_REPO/ebapps then add module to remove list  assuming command.yaml is present in directory
        if name.lower() in yaml_apps:
            remove_app_list.append(module)

    # remove module choices which already have a directory and possible command.yaml
    for item in remove_app_list:
        software_list.remove(item)

    return software_list

def get_binaries_from_application(module):
    """ return a list of binaries from $PATH variable defined in module file"""

    cmd = "module show " + module

    ret = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ret.communicate()[1].decode("utf-8")
    path_str = "prepend_path(\"PATH\","

    path_list = []
    for line in output.splitlines():
        #print line, line.find(path_str)
        if line.find(path_str) != -1:
            # need to extract directory from  a string in the following format
            # prepend_path("PATH","/nfs/grid/software/easybuild/IvyBridge/redhat/7.3/software/GCCcore/6.4.0/bin")

            start_index = line.index(",") +2
            end_index = line.rfind("\"")
            # add directory to list that is being set by PATH variable in module file
            path_list.append(line[start_index:end_index])

    if len(path_list)  ==  0:
        print ("No $PATH set in your module ", module, "  so no possible binaries can be found")
        return None

    binaries = {}
    for dir in path_list:
        # check for files only if directory exists
        for executable in os.listdir(dir):
            executable_filepath = os.path.join(dir,executable)

            # skip loop if it is not a file
            if not os.path.isfile(executable_filepath):
                continue
            # check only files that are executable
            statmode = os.stat(executable_filepath)[stat.ST_MODE] & (stat.S_IXUSR|stat.S_IXGRP|stat.S_IXOTH)
            # only add files that are executable

            ret = subprocess.Popen("sha256sum " + executable_filepath, shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output = ret.communicate()[0].decode("utf-8")
            sha256sum = output.split(" ")[0]


            if statmode and not os.path.islink(executable_filepath):
                # only add binaries with unique sha256 sum
                if sha256sum not in binaries.keys():
                    binaries[sha256sum] = executable

    return binaries
