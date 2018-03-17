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
This module generates yaml configuration files

:author: Shahzeb Siddiqui (Pfizer)
"""

import os
import sys
import yaml
from framework.env import config_opts
from framework.tools.software import get_unique_software
from framework.tools.system import check_system_package_installed, get_binaries_from_systempackage
def create_system_yaml(name):
	""" create YAML configuration for binary test for system package """
	BUILDTEST_MODULE_EBROOT = config_opts['DEFAULT']['BUILDTEST_MODULE_EBROOT']
	BUILDTEST_CONFIGS_REPO = config_opts['DEFAULT']['BUILDTEST_CONFIGS_REPO']
	softwarelist = get_unique_software(BUILDTEST_MODULE_EBROOT)
	destdir = os.path.join(BUILDTEST_CONFIGS_REPO,"system",name)
	yamlfile = os.path.join(destdir,"command.yaml")

	# if yaml file exists then exit out
	if os.path.isfile(yamlfile):
		print "YAML file already exists, please check: ", yamlfile
		sys.exit(0)

	# if directory is not present then create it
	if not os.path.isdir(destdir):
		print "creating directory ", destdir
		os.makedirs(destdir)

	# if package is not installed
	if check_system_package_installed(name) == False:
		print "Please install system package:", name, " before creating YAML file"
		sys.exit(0)

	# get binary from system package
	binary = get_binaries_from_systempackage(name)

	# no test, then stop immediately
	if len(binary) == 0:
		print "There are no binaries found in package: ", name
		sys.exit(0)

	fd = open(yamlfile,"w")
	binarydict = { "binaries": binary }
	with open(yamlfile, 'a') as outfile:
		yaml.dump(binarydict, outfile, default_flow_style=False)

	print "Please check YAML file", yamlfile, " and fix test accordingly"
	sys.exit(0)
