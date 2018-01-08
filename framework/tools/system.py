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
:author: Shahzeb Siddiqui (Pfizer)

Functions for system package 
"""

import os
import stat
from stat import S_IXUSR, S_IXGRP, S_IXOTH
import subprocess
from framework.env import BUILDTEST_SOURCEDIR

def check_system_package_installed(pkg):
	""" check if system package is installed and return True/False"""

	cmd = "rpm -q " + pkg
        ret = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        ret.communicate()

	if ret.returncode == 0:
		return True
	else:
		return False
	
def get_binaries_from_systempackage(pkg):
	""" get binaries from system package that typically install in standard linux path and only those that are executable """

	bindirs = [ "/usr/bin", "/bin", "/sbin", "/usr/sbin", "/usr/local/bin", "/usr/local/sbin" ]

	cmd = "rpm -ql " + pkg  
        ret = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        (output,err) = ret.communicate()
	
	temp = output.splitlines()
	output = temp
	
	binarylist = []

	for file in output:
		# if file doesn't exist but found during rpm -ql then skip file. 
		if not os.path.isfile(file):
			continue

		# check only files that are executable
		statmode = os.stat(file)[stat.ST_MODE] & (stat.S_IXUSR|stat.S_IXGRP|stat.S_IXOTH)

		# only add executable files found in array bindirs
		if statmode and os.path.dirname(file) in bindirs:
			binarylist.append(file)

	return binarylist

def systempackage_list():
	dir = os.path.join(BUILDTEST_SOURCEDIR,"system")
	return os.listdir(dir)

def systempackage_installed_list():
	cmd = """ rpm -qa --qf "%{NAME}\n" """
	ret = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE)
	output = ret.communicate()[0]
	pkglist = output.split("\n")
	# delete last element which is a ""
	pkglist = pkglist[:-1]
	return pkglist



