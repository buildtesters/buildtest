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
This python module will implement the --scantest feature of buildtest

:author: Shahzeb Siddiqui (Pfizer)
"""

import os
import subprocess
import sys
from framework.env import config_opts
from framework.tools.software import get_unique_software

def scantest():

	applist = get_unique_software()
	BUILDTEST_CONFIGS_REPO = config_opts['DEFAULT']['BUILDTEST_CONFIGS_REPO']
	eblist_sourcedir =  os.listdir(os.path.join(BUILDTEST_CONFIGS_REPO,"ebapps"))

	ebapps_common=  set(applist) & set(eblist_sourcedir)
	ebapps_uncommon=  list(set(applist) - set(eblist_sourcedir))

	print """
****************************************
*     EB Apps with YAML configs:       *
****************************************
"""

	print "EBAPP            YAML TEST FOUND"
	print "----------------------------------------"
	for x in ebapps_common:
		cmd  = "find " + os.path.join(BUILDTEST_CONFIGS_REPO,"ebapps",x) + """ -type f -name *.yaml | wc -l"""
		ret = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		output = ret.communicate()[0]

		# removing new line character
		output = output.rstrip()
 		print (x + "\t\t" + output).expandtabs(10)
		#print " %-*s \t\t %s " % (x,output)

	print """
****************************************
*     EB Apps without YAML configs:    *
****************************************
"""
	print ebapps_uncommon

	syspkg_sourcedir = os.listdir(os.path.join(BUILDTEST_CONFIGS_REPO,"system"))


	print """
****************************************************
*     System Package with/without YAML configs:    *
****************************************************
"""

	for pkg in syspkg_sourcedir:
		cmd = "rpm -q " + pkg
		ret = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		(output,errormsg) = ret.communicate()

		output = output.rstrip()

		if ret.returncode == 0:
			print "Found YAML config for system package: ", output
		else:
			print "Could not find YAML config for system package:", output

	sys.exit(0)
