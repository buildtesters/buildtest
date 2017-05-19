
############################################################################
#
#  Copyright 2017
#
#   https://github.com/shahzebsiddiqui/buildtest
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

import sys
import os
sys.path.insert(0,os.path.abspath('.'))

from setup import *
from modules import *
from testgen import *
from master import *
from tools.generic import *
from tools.file import *
from parser import *
from testmodules.testsets import *

import subprocess
import argparse
module=""
version=""

parser = argparse.ArgumentParser()
parser.add_argument("-fc","--findconfig", help= """" Find buildtest YAML config files 
						     To find all yaml config files use -fc all """)
parser.add_argument("-ft", "--findtest", help="""Find buildtest generated test scripts
					      	     To find all test scripts use -ft all """)
parser.add_argument("-s", "--software", help=" Specify software package to test")
parser.add_argument("-t", "--toolchain",help=" Specify toolchain for the software package") 
parser.add_argument("-lt", "--list-toolchain",help="retrieve toolchain used based on the easyconfig files provided by BUILDTEST_EASYCONFIGDIR", action="store_true")
parser.add_argument("-ls", "--list-unique-software",help="retrieve all unique software found in your module tree specified by BUILDTEST_MODULETREE", action="store_true")
parser.add_argument("-svr", "--software-version-relation", help="retrieve a relationship between software and version found in module files", action="store_true")
parser.add_argument("--system", help=""" Build test for system packages
					 To build all system package test use --system all """)
parser.add_argument("--testset", help="Select the type of test set to run (python,mpi,ruby,perl,R)", choices=["python","R","mpi","ruby","perl"])
parser.add_argument("-v", "--verbose", help="increase verbosity level", type=int, choices=[1,2])

args = parser.parse_args()


# convert args into a dictionary
args_dict=vars(args)

verbose=0

# logdir where log file will be rewritten. logdir can change based on parameter -s and --system
logdir = os.path.join(BUILDTEST_ROOT,"log")
logcontent=""

logcontent += "------------------------------------------- \n"
logcontent += "buildtest \n"
logcontent += "------------------------------------------- \n"


if args_dict["verbose"] >= 1:
	text = "==================================================================== " + "\n"
	text += "BUILDTEST ROOT DIRECTORY: " + BUILDTEST_ROOT + "\n" 
	text += "BUILDTEST SOURCE DIRECTORY: " + BUILDTEST_SOURCEDIR +"\n"
	text += "BUILDTEST EASYCONFIGDIR: " + BUILDTEST_EASYCONFIGDIR + "\n"
	text += "BUILDTEST MODULE_EBROOT: " + BUILDTEST_MODULE_EBROOT + "\n"
	text += "BUILDTEST TEST DIRECTORY:" + BUILDTEST_TESTDIR + "\n"
	text += "==================================================================== " + "\n"
	print text
	print

	
	logcontent += text

	verbose=args_dict["verbose"]



# when no argument is specified to -fc then output all yaml files
if args.findconfig == "all": 
	findCMD = "find " + BUILDTEST_SOURCEDIR + " -name \"*.yaml\" -type f"
	ret = subprocess.Popen(findCMD,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	(output,err) = ret.communicate()
	print output
	sys.exit(1)
# otherwise report yaml file based on argument. If -fc is not specified then args.findconfig is set
# to None and we don't want to run this section unless a -fc is specified along with an argument other than
# all
elif args.findconfig != None:
	find_arg = args_dict["findconfig"]
	findCMD = "find " + BUILDTEST_SOURCEDIR + " -name \"*" + find_arg + "*.yaml\" -type f"
	ret = subprocess.Popen(findCMD,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	(output,err) = ret.communicate()
	print output
	sys.exit(1)

# report all buildtest generated test scripts
if args.findtest == "all":
	# running command: find $BUILDTEST_TESTDIR -name "*.sh" -type f
	findCMD = "find " + BUILDTEST_TESTDIR + " -name \"*.sh\" -type f"
	print findCMD
	ret = subprocess.Popen(findCMD,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	(output,err) = ret.communicate()
	print output
	sys.exit(1)
# otherwise report test scripts based on argument. If -ft is not specified then args.findtest is None
# so we don't want to run section below everytime. Only when -ft is specified
elif args.findtest != None:
	find_arg = args_dict["findtest"]
	print find_arg, type(find_arg)
	findCMD = "find " + BUILDTEST_TESTDIR + " -name \"*" + find_arg + "*.sh\" -type f"
	# running command: find $BUILDTEST_SOURCEDIR -name "*<find_arg>*.sh" -type f
	ret = subprocess.Popen(findCMD,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	(output,err) = ret.communicate()
	print output
	sys.exit(1)

if args_dict["list_toolchain"] == True:
	toolchain_set,logcontent_substr=get_toolchain(BUILDTEST_EASYCONFIGDIR)
	logcontent+=logcontent_substr
	text = """ 
		List of Toolchains:
		--------------------
	      """
	print text

	print_set(toolchain_set)

if args_dict["list_unique_software"] == True:
	software_set,logcontent_substr=get_unique_software(BUILDTEST_MODULE_EBROOT)
	logcontent+=logcontent_substr
	print """
	       List of Unique Software: 
	       ---------------------------- """
	print_set(software_set)	
if args_dict["software_version_relation"] == True:
	software_version_dict=module_version_relation(BUILDTEST_MODULE_EBROOT)
	text = """
		Software Version Relationship:
		-------------------------------
		"""
	print text
	print_dictionary(software_version_dict)

	logcontent += text +"\n"
	for item in software_version_dict:
		logcontent+= item + " " + str(sset(software_version_dict[item])) + "\n"

testset=""
if args.testset: 
	testset=args.testset

# generate system pkg test
if args.system:
	systempkg = args.system
	if systempkg == "all":

		logdir = os.path.join(BUILDTEST_ROOT,"log","system","all")
		systempkg_list = os.listdir(os.path.join(BUILDTEST_SOURCEDIR,"system"))
		logcontent += "System Packages: \n"
		logcontent += str(systempkg_list) + "\n"
		for pkg in systempkg_list:
			logcontent += systempkg_generate_binary_test(pkg,verbose,logdir)
	else:
		logdir = os.path.join(BUILDTEST_ROOT,"log","system",systempkg)
		logcontent += systempkg_generate_binary_test(systempkg,verbose,logdir)


testset=""
if args.testset:
        testset=args.testset

# when -s is specified
if args.software != None:
	
        software=args.software.split("/")
	appname,appversion=get_software_name_version(software)

	# default value assuming toolchain is not specified
	tcname="dummy"
	tcversion="dummy"
	toolchain=""
	if args.toolchain != None:
        	toolchain=args.toolchain.split("/")
	else:
	        toolchain="dummy/dummy".split("/")
	

	tcname=toolchain[0]
	tcversion=toolchain[1]

	# checking if its a valid software
	logcontent += software_exists(software,verbose)

	# checking if its a valid toolchain 
	toolchain_exists(software,toolchain)
	if verbose >= 1:
		text = "Toolchain:" + tcname + " " + tcversion + " found in system \n"
		print text
		logcontent += text

	# check that the software,toolchain match the easyconfig.
	ret,logcontent_substr=check_software_version_in_easyconfig(BUILDTEST_EASYCONFIGDIR,software,toolchain)
	logcontent+=logcontent_substr
	# generate_binary_test(software,toolchain,verbose)
	
	source_app_dir=os.path.join(BUILDTEST_SOURCEDIR,"ebapps",appname)

        configdir=os.path.join(source_app_dir,"config")
        codedir=os.path.join(source_app_dir,"code")
	logdir=os.path.join(BUILDTEST_ROOT,"log",appname,appversion,tcname,tcversion)

	logcontent += "Source App Directory:" +  source_app_dir + "\n"
	logcontent += "Config Directory: " + configdir + "\n"
	logcontent += "Code Directory:" + codedir + "\n"

	logcontent += generate_binary_test(software,toolchain,source_app_dir,verbose,logdir)
	# this generates all the compilation tests found in application directory ($BUILDTEST_SOURCEDIR/ebapps/<software>)
	logcontent += recursive_gen_test(software,toolchain,configdir,codedir,verbose, logdir)

	# if flag --testset is set, then 
	if testset !=  None:
		logcontent+=run_testset(software,toolchain,testset,verbose)
	
update_logfile(logdir,logcontent,verbose)
