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

from framework.env import logID, config_opts
from framework.tools.easybuild import list_toolchain, get_module_ebroot
from framework.tools.modules import get_module_list
from framework.tools.utility import sset


def get_unique_software():
        """
        returns a set of software packages found in the module tree
        """
        modtrees = get_module_ebroot()
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
	toolchains = list_toolchain()

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

        module_set=get_unique_software()

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
