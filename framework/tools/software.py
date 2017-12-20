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
Application & Toolchain name & version query functions

:author: Shahzeb Siddiqui (Pfizer)
"""

import os
import sys
import logging

from framework.env import BUILDTEST_MODULE_NAMING_SCHEME, BUILDTEST_MODULE_EBROOT, logID
from framework.tools.menu import buildtest_menu
from framework.tools.modules import get_module_list
from framework.tools.utility import sset

def get_appname():
	args_dict = buildtest_menu()
	software = get_arg_software(args_dict)
	software = software.split('/')
	return software[0]

def get_appversion():
        args_dict = buildtest_menu()
        software = get_arg_software(args_dict)
	software = software.split('/')
	if BUILDTEST_MODULE_NAMING_SCHEME == "FNS":
		tc = get_toolchain()
		appversion = software[1].replace(tc,'')
		if appversion[-1] == "-":
			appversion = appversion[:-1]
			return appversion
	else:
		return software[1]				

def get_application_name():
	return get_appname() + '-' + get_appversion()

def get_toolchain():
	return get_toolchain_name() + '-' + get_toolchain_version()
	
def get_toolchain_name():
        args_dict = buildtest_menu()
        toolchain = get_arg_toolchain(args_dict)
	
	# checking if toolchain is defined in argument
	if toolchain is  None:	
		return ""
	else:
		toolchain = toolchain.split("/")
		return toolchain[0]

def get_toolchain_version():
        args_dict = buildtest_menu()
        toolchain = get_arg_toolchain(args_dict)

	# checking if toolchain is defined in argument
	if toolchain is None:
		return ""
	else:
		toolchain = toolchain.split("/")
		return toolchain[1]


def get_unique_software():
        """
        returns a set of software packages found in the module tree
        """
        logger = logging.getLogger(logID)
        logger.info("Traversing Module Tree: %s to find all unique software", BUILDTEST_MODULE_EBROOT)

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


def get_unique_software_version():
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

                moduleversion_set.add(modulename+" "+version)

        return sorted(moduleversion_set)


def software_version_relation():
        """
        relationship between software name and version. The function will return a
        dictionary with key values as software name and values will be a set of version
        """
        modulelist=get_module_list()

        module_set=get_unique_software()
        # This set contains one entry of sorted lists of modules, need to iterate over list and not set.
        #module_set = module_set[0]

        # dictionary used for keeping a relationship between software name and its corresponding versions found as modulefiles
        module_dict = {}


        # for every app iterate over module tree and add unique version in set, then add this to a dictionary. That way
        # a dictionary can reference via key,value where key is application name and value is the list of versions
        for item in  module_set:
                version_set = set()
                for app in modulelist:
                        #logger.debug("ModuleFile: %s", app)
                        name = os.path.basename(os.path.dirname(app))

                        if item != name:
                                continue


                        version = os.path.basename(app)
                        version = os.path.splitext(version)[0]

                        # only add module version to set when module name is found in tree
                        version_set.add(version + " (" + app +")")

                module_dict[item] = version_set

        return module_dict

def software_exists(software):
        """
        checks whether software exist, there must be a module file present with the
        same name specified as the argument.
        """

        success_msg = "Checking Software: " + software[0] + "/" + software[1] + "  ... SUCCESS"
        fail_msg = "Checking Software: " + software[0] + "/" + software[1] + " ... FAILED"

        logger = logging.getLogger(logID)

        logger.debug("Checking argument list length for software, must be equal to 2")
        if len(software) != 2:
                print fail_msg
                msg = "Too many arguments, -s takes argument <software>,<version> \n"
                print msg
                logger.error("%s",msg)
                sys.exit(1)

        softwarecollection=get_unique_software_version()
        software_name=software[0]+" "+software[1]

        logger.debug("Checking %s is found in software version list", software_name)

        if software_name not in softwarecollection:
                print fail_msg
                msg = "Can't find software: " +  software_name + "\n"
                print msg
                logger.error("%s",fail_msg)
                sys.exit(1)

        logger.info("%s",success_msg)

        print success_msg



