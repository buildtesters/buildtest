#!/usr/bin/env python
############################################################################
#
#  Copyright 2017
#
#   https://github.com/shahzebsiddiqui/buildtest-framework
#
#    This file is part of buildtest.
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
The entry point to buildtest

:author: Shahzeb Siddiqui (Pfizer)
"""

import sys
import os
sys.path.insert(0,os.path.abspath('.'))

from framework.runtest import *
from framework.env import *
from framework.modules import *
from framework.testgen import *
from framework.master import *
from framework.tools.generic import *
from framework.tools.file import *
from framework.parser.functions import *
from framework.parser.args import *
from framework.parser.parser import *
from framework.testmodules.testsets import *

import subprocess
import argparse

def main():
	module=""
	version=""

	parser = argparse.ArgumentParser()
	parser.add_argument("--check-setup", help="Check buildtest configuration and determine if you have it setup properly for testing",action="store_true")
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
	parser.add_argument("--runtest", help="Run the test interactively through runtest.py", action="store_true")
	parser.add_argument("-v", "--verbose", help="increase verbosity level", type=int, choices=[1,2])
	parser.add_argument("-V", "--version", help="show program version number and exit",action="store_true")
 
	args = parser.parse_args()


	# convert args into a dictionary
	args_dict = vars(args)

	version = get_arg_version(args_dict)
	check_setup = get_arg_check_setup(args_dict)
	findconfig = get_arg_findconfig(args_dict)
	findtest = get_arg_findtest(args_dict)
	software = get_arg_software(args_dict)
	toolchain = get_arg_toolchain(args_dict)
	list_toolchain = get_arg_list_toolchain(args_dict)
	list_unique_software = get_arg_list_unique_software(args_dict)
	software_version_relation = get_arg_software_version_relation(args_dict)
	system = get_arg_system(args_dict)
	testset = get_arg_testset(args_dict)
	verbose = get_arg_verbose(args_dict)
	runtest = get_arg_runtest(args_dict)

	if version == True:
		print_version()
		sys.exit(1)

	if check_setup == True:
		check_buildtest_setup()
		sys.exit(1)

	if runtest == True:
		runtest_menu()

	os.environ["BUILDTEST_LOGDIR"] = os.path.join(BUILDTEST_ROOT,"log")
	os.environ["BUILDTEST_LOGFILE"] = datetime.now().strftime("buildtest_%H_%M_%d_%m_%Y.log")
	logdir =  os.environ["BUILDTEST_LOGDIR"]
	logfile = os.environ["BUILDTEST_LOGFILE"]


	BUILDTEST_LOGCONTENT.append("------------------------------------------- \n")
	BUILDTEST_LOGCONTENT.append("buildtest \n")
	BUILDTEST_LOGCONTENT.append("------------------------------------------- \n")

	if verbose >= 1:
		text = "==================================================================== " + "\n"
		text += "BUILDTEST ROOT DIRECTORY: " + BUILDTEST_ROOT + "\n" 
		text += "BUILDTEST SOURCE DIRECTORY: " + BUILDTEST_SOURCEDIR +"\n"
		text += "BUILDTEST EASYCONFIGDIR: " + BUILDTEST_EASYCONFIGDIR + "\n"
		text += "BUILDTEST MODULE_EBROOT: " + BUILDTEST_MODULE_EBROOT + "\n"
		text += "BUILDTEST TEST DIRECTORY:" + BUILDTEST_TESTDIR + "\n"
		text += "==================================================================== " + "\n"
		print text
		print

	
		BUILDTEST_LOGCONTENT.append(text)

	# when no argument is specified to -fc then output all yaml files
	if findconfig == "all": 
		findCMD = "find " + BUILDTEST_SOURCEDIR + " -name \"*.yaml\" -type f"
		ret = subprocess.Popen(findCMD,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		(output,err) = ret.communicate()
		print output
		BUILDTEST_LOGCONTENT.append(output)
		update_logfile(verbose)
		sys.exit(1)
	# otherwise report yaml file based on argument. If -fc is not specified then args.findconfig is set
	# to None and we don't want to run this section unless a -fc is specified along with an argument other than
	# all
	elif findconfig != None:
		find_arg = args_dict["findconfig"]
		findCMD = "find " + BUILDTEST_SOURCEDIR + " -name \"*" + find_arg + "*.yaml\" -type f"
		ret = subprocess.Popen(findCMD,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		(output,err) = ret.communicate()
		print output
		BUILDTEST_LOGCONTENT.append(output)
		update_logfile(verbose)
		sys.exit(1)

	# report all buildtest generated test scripts
	if findtest == "all":
		# running command: find $BUILDTEST_TESTDIR -name "*.sh" -type f
		findCMD = "find " + BUILDTEST_TESTDIR + " -name \"*.sh\" -type f"
		ret = subprocess.Popen(findCMD,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		(output,err) = ret.communicate()
		print output
		BUILDTEST_LOGCONTENT.append(output)
		update_logfile(verbose)
		sys.exit(1)
	# otherwise report test scripts based on argument. If -ft is not specified then args.findtest is None
	# so we don't want to run section below everytime. Only when -ft is specified
	elif findtest != None:
		find_arg = args_dict["findtest"]
		findCMD = "find " + BUILDTEST_TESTDIR + " -name \"*" + find_arg + "*.sh\" -type f \n"
		# running command: find $BUILDTEST_SOURCEDIR -name "*<find_arg>*.sh" -type f
		ret = subprocess.Popen(findCMD,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		(output,err) = ret.communicate()
		print output
		BUILDTEST_LOGCONTENT.append(findCMD)
		BUILDTEST_LOGCONTENT.append(output)
		update_logfile(verbose)
		sys.exit(1)

	if list_toolchain == True:
		toolchain_set=get_toolchain(BUILDTEST_EASYCONFIGDIR)
		text = """ \n
			 List of Toolchains: 
			 -------------------- \n"""
		print text
		BUILDTEST_LOGCONTENT.append(text)
		print_set(toolchain_set)
		update_logfile(verbose)
		sys.exit(1)

	if list_unique_software == True:
		software_set=get_unique_software(BUILDTEST_MODULE_EBROOT)
		text =  """ \n
		       List of Unique Software: 
		       ---------------------------- \n """
		print text
		BUILDTEST_LOGCONTENT.append(text)
		print_set(software_set)	
		update_logfile(verbose)
		sys.exit(1)
	if software_version_relation == True:
		software_version_dict=module_version_relation(BUILDTEST_MODULE_EBROOT)
		text = """ \n
			Software Version Relationship:
			------------------------------- \n """
		print text
		BUILDTEST_LOGCONTENT.append(text)
		print_dictionary(software_version_dict)
	
		for item in software_version_dict:
			BUILDTEST_LOGCONTENT.append(item + " " + str(sset(software_version_dict[item])) + "\n")

		update_logfile(verbose)
		sys.exit(1)

	# generate system pkg test
	if system != None:
		systempkg = args.system
		if systempkg == "all":

			os.environ["BUILDTEST_LOGDIR"] = os.path.join(BUILDTEST_ROOT,"log","system","all")
			systempkg_list = os.listdir(os.path.join(BUILDTEST_SOURCEDIR,"system"))
			BUILDTEST_LOGCONTENT.append("System Packages: \n")

			for pkg in systempkg_list:
				generate_binary_test(args_dict,verbose,pkg)
		else:
			os.environ["BUILDTEST_LOGDIR"] = os.path.join(BUILDTEST_ROOT,"log","system",systempkg)
			#logcontent += systempkg_generate_binary_test(systempkg,verbose,logdir)
			generate_binary_test(args_dict,verbose,systempkg)

		update_logfile(verbose)
		sys.exit(1)
	# when -s is specified
	if software != None:
		software=software.split("/")

		# checking if software exists
		software_exists(software,verbose)
		appname,appversion=software

		if toolchain == None:
			toolchain = "dummy/dummy"
	
		toolchain=toolchain.split("/")
		# checking if its a valid toolchain 
		toolchain_exists(toolchain,verbose)
	
		tcname,tcversion=toolchain

	
		if verbose >= 1:
			text = "Toolchain:" + tcname + " " + tcversion + " found in system \n"
			print text

		# check that the software,toolchain match the easyconfig.
		ret=check_software_version_in_easyconfig(BUILDTEST_EASYCONFIGDIR,software,toolchain,verbose)
		# generate_binary_test(software,toolchain,verbose)
	
		source_app_dir=os.path.join(BUILDTEST_SOURCEDIR,"ebapps",appname)

	        configdir=os.path.join(source_app_dir,"config")
	        codedir=os.path.join(source_app_dir,"code")
		os.environ["BUILDTEST_LOGDIR"]=os.path.join(BUILDTEST_ROOT,"log",appname,appversion,tcname,tcversion)
		logdir=os.environ["BUILDTEST_LOGDIR"]


		BUILDTEST_LOGCONTENT.append("Source App Directory:" +  source_app_dir + "\n")
		BUILDTEST_LOGCONTENT.append("Config Directory: " + configdir + "\n")
		BUILDTEST_LOGCONTENT.append("Code Directory:" + codedir + "\n")

		generate_binary_test(args_dict,verbose,None)
		# this generates all the compilation tests found in application directory ($BUILDTEST_SOURCEDIR/ebapps/<software>)
		recursive_gen_test(software,toolchain,configdir,codedir,verbose)
	
		# if flag --testset is set, then 
		if testset !=  None:
			run_testset(software,toolchain,testset,verbose)
	
		update_logfile(verbose)

if __name__ == "__main__":
        main()
