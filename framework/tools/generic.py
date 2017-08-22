############################################################################ 
# 
#  Copyright 2017 
# 
#   https://github.com/shahzebsiddiqui/buildtest-framework
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

import subprocess
import time
from framework.env import *
def print_version():
	print "buildtest version: " + BUILDTEST_VERSION

def check_buildtest_setup():
	print "=============================================="
	print "buildtest configuration check"
	print "=============================================="
	
	print "Checking buildtest environment variables ..."
	time.sleep(0.5)

	ec = 0

	print "Checking BUILDTEST_ROOT ..."
	time.sleep(0.5)
	if not os.path.exists(os.environ["BUILDTEST_ROOT"]):
		ec = 1
		print "STATUS: BUILDTEST_ROOT is not set ... FAILED"
	else:
		print "STATUS: BUILDTEST_ROOT ... PASSED"


	print "Checking BUILDTEST_SOURCEDIR ..."
	time.sleep(0.5)
	if not os.path.exists(os.environ["BUILDTEST_SOURCEDIR"]):
		ec = 1
		print "STATUS: BUILDTEST_SOURCEDIR is not set ... FAILED"
	else:
		print "STATUS: BUILDTEST_SOURCEDIR ... PASSED" 

	
	print "Checking BUILDTEST_TESTDIR ..."
	time.sleep(0.5)
	if not os.path.exists(os.environ["BUILDTEST_TESTDIR"]):
		ec = 1
		print "STATUS: BUILDTEST_TESTDIR is not set ... FAILED"
	else:
		print "STATUS: BUILDTEST_TESTDIR ... PASSED"



	print "Checking BUILDTEST_MODULE_EBROOT ..."
	time.sleep(0.5)
	if not os.path.exists(os.environ["BUILDTEST_MODULE_EBROOT"]):
		ec = 1
		print "STATUS: BUILDTEST_MODULE_EBROOT is not set"
	else:
		print "STATUS: BUILDTEST_MODULE_EBROOT ... PASSED"
	

	print "Checking BUILDTEST_EASYCONFIGDIR ..."
	time.sleep(0.5)
	if not os.path.exists(os.environ["BUILDTEST_EASYCONFIGDIR"]):
		ec = 1
		print "STATUS: BUILDTEST_EASYCONFIGDIR is not set ... FAILED"
	else:
		print "STATUS: BUILDTEST_EASYCONFIGDIR ... PASSED"
	

	print "Checking BUILDTEST_R_DIR ..."
	time.sleep(0.5)
	if not os.path.exists(os.environ["BUILDTEST_R_DIR"]):
		ec = 1
		print "STATUS: BUILDTEST_R_DIR is not set"
	else:
		print "STATUS: BUILDTEST_R_DIR ... PASSED"


	print "Checking BUILDTEST_PERL_DIR ..."
	time.sleep(0.5)
	if not os.path.exists(os.environ["BUILDTEST_PERL_DIR"]):
		ec = 1
		print "STATUS: BUILDTEST_PERL_DIR is not set ... FAILED"
	else:
		print "STATUS: BUILDTEST_PERL_DIR ... PASSED"
	

	print "Checking BUILDTEST_PYTHON_DIR ..."
	time.sleep(0.5)
	if not os.path.exists(os.environ["BUILDTEST_PYTHON_DIR"]):
		ec = 1
		print "STATUS: BUILDTEST_PYTHON_DIR is not set ... FAILED"
	else:
		print "STATUS: BUILDTEST_PYTHON_DIR ... PASSED"

	if ec == 0:
		print "buildtest environment variable PASSED!"

	print "Checking module command ..."
	time.sleep(0.5)

	cmd = "module --version"
	ret = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	ret.communicate()
	ec = ret.returncode
	if ec == 0:
		print "module command found!:"

	# detecting whether we have Lmod or environment-modules
	# query Lmod rpm 
	cmd = "rpm -q Lmod"
	ret = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	(outputmsg,errormsg) = ret.communicate()
	ec = ret.returncode
	if ec == 0:
		print "System detected Lmod found package - ", outputmsg


	cmd = "rpm -q environment-modules"
	ret = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	(outputmsg,errormsg) = ret.communicate()
	ec = ret.returncode
	if ec == 0:
		print "System detected environment-modules found package - ", outputmsg

	


def add_arg_to_runcmd(runcmd,arglist):
        # add each argument to runcmd
        for arg in arglist:
        # skip argument if value is not specified, by default set to None
                if arg == None:
                        continue
                # in case argument is not a string, convert it anyways
                runcmd+= " " + str(arg)
        return runcmd


def load_modules(software,toolchain):
        """
        return a string that loads the software and toolchain module. 
        """
        # for dummy toolchain you can load software directly. Ensure a clean environment by running module purge
        if toolchain[0] == "dummy":
                header="""
#!/bin/sh
module purge
module load """ + software[0] + "/" + software[1] + """
"""
        else:
                header="""
#!/bin/sh
module purge
module load """ + toolchain[0] + "/" + toolchain[1] + """
module load """ + software[0] + "/" + software[1] + """
"""

        return header


def print_dictionary(dictionary):
        """
        prints the content of dictionary
        """
        for key in dictionary:
                print key, sset(dictionary[key])

def print_set(setcollection):
        """
        prints the content of set 
        """
        for item in setcollection:
                print item
		BUILDTEST_LOGCONTENT.append(item + "\n")
class sset(set):
    def __str__(self):
        return ', '.join([str(i) for i in self])

