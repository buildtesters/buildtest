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

import subprocess
import time
from framework.env import *
from framework.tools.software import *
def print_version():
	print "buildtest version: " + BUILDTEST_VERSION

def check_buildtest_setup():
	print "=============================================="
	print "buildtest configuration check"
	print "=============================================="
	
	print "Checking buildtest environment variables ..."

	ec = 0

	time.sleep(0.2)
	if not os.path.exists(os.environ["BUILDTEST_ROOT"]):
		ec = 1
		print "STATUS: BUILDTEST_ROOT is not set ... FAILED"
	else:
		print "STATUS: BUILDTEST_ROOT ... PASSED"


	time.sleep(0.2)
	if not os.path.exists(os.environ["BUILDTEST_SOURCEDIR"]):
		ec = 1
		print "STATUS: BUILDTEST_SOURCEDIR is not set ... FAILED"
	else:
		print "STATUS: BUILDTEST_SOURCEDIR ... PASSED" 

	
	time.sleep(0.2)
	if not os.path.exists(os.environ["BUILDTEST_TESTDIR"]):
		ec = 1
		print "STATUS: BUILDTEST_TESTDIR is not set ... FAILED"
	else:
		print "STATUS: BUILDTEST_TESTDIR ... PASSED"



	time.sleep(0.2)
	if not os.path.exists(os.environ["BUILDTEST_MODULE_EBROOT"]):
		ec = 1
		print "STATUS: BUILDTEST_MODULE_EBROOT is not set"
	else:
		print "STATUS: BUILDTEST_MODULE_EBROOT ... PASSED"
	

	time.sleep(0.2)
	if not os.path.exists(os.environ["BUILDTEST_EASYCONFIGDIR"]):
		ec = 1
		print "STATUS: BUILDTEST_EASYCONFIGDIR is not set ... FAILED"
	else:
		print "STATUS: BUILDTEST_EASYCONFIGDIR ... PASSED"
	

	time.sleep(0.2)
	if os.environ["BUILDTEST_MODULE_NAMING_SCHEME"] == "FNS" or  os.environ["BUILDTEST_MODULE_NAMING_SCHEME"] == "HMNS":
		print "STATUS: BUILDTEST_MODULE_NAMING_SCHEME ... PASSED"
		print "BUILDTEST_MODULE_NAMING_SCHEME is set to: ", os.environ["BUILDTEST_MODULE_NAMING_SCHEME"]
	else:
		ec = 1
		print "STATUS: BUILDTEST_MODULE_NAMING_SCHEME is set to: " + BUILDTEST_MODULE_NAMING_SCHEME
		print "Valid values for BUILDTEST_MODULE_NAMING_SCHEME are: [HMNS, FNS]"


	time.sleep(0.2)
	if not os.path.exists(os.environ["BUILDTEST_R_DIR"]):
		ec = 1
		print "STATUS: BUILDTEST_R_DIR is not set"
	else:
		print "STATUS: BUILDTEST_R_DIR ... PASSED"


	time.sleep(0.2)
	if not os.path.exists(os.environ["BUILDTEST_PERL_DIR"]):
		ec = 1
		print "STATUS: BUILDTEST_PERL_DIR is not set ... FAILED"
	else:
		print "STATUS: BUILDTEST_PERL_DIR ... PASSED"
	

	time.sleep(0.2)
	if not os.path.exists(os.environ["BUILDTEST_PYTHON_DIR"]):
		ec = 1
		print "STATUS: BUILDTEST_PYTHON_DIR is not set ... FAILED"
	else:
		print "STATUS: BUILDTEST_PYTHON_DIR ... PASSED"

	if ec == 0:
		print "buildtest environment variable PASSED!"

	time.sleep(0.2)

	cmd = "module --version"
	ret = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	(outputmsg,errormsg) = ret.communicate()
	ec = ret.returncode

	if ec == 0:
		print "Detecting module command .... "
		print outputmsg, errormsg

	else:
		print "module commmand not found in system"
		print outputmsg, errormsg


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
	(outputmsg) = ret.communicate()[0]
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


def load_modules():
        """
        return a string that loads the software and toolchain module. 
        """
	
	appname = get_appname()
	appversion = get_appversion()
	tcname = get_toolchain_name()
	tcversion = get_toolchain_version()

        header="""
#!/bin/sh
module purge
"""
        # for dummy toolchain you can load software directly. Ensure a clean environment by running module purge
        if tcname == "dummy":
		moduleload = "module load " + appname + "/" + appversion  + "\n"
        else:
		if BUILDTEST_MODULE_NAMING_SCHEME == "HMNS":
			moduleload = "module load " + tcname + "/" + tcversion + "\n"
			moduleload += "module load " + appname + "/" + appversion + "\n"
		elif BUILDTEST_MODULE_NAMING_SCHEME == "FNS":
			moduleload = "module load " + tcname + "/" + tcversion + "\n"
			toolchain_name = appname + "-" + tcversion
			appversion = appversion.replace(toolchain_name,'')
			if appversion[-1] == "-":
				appversion = appversion[:-1]

			moduleload += " module load " + appname + "/" + appversion + "-" + tcname + "-" + tcversion + "\n"

	header = header + moduleload
        return header


def print_dictionary(dictionary):
        """
        prints the content of dictionary
        """
	count = 1
        for key in dictionary:
		
                print (str(count) + "\t |").expandtabs(4) , "\t" + (key + "\t |" ).expandtabs(25) + "\t", sset(dictionary[key])
		count = count + 1

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

