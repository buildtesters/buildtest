#!/usr/bin/env python
############################################################################
#
#  Copyright 2017
#
#   https://github.com/HPC-buildtest/buildtest-framework
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

from framework.runtest import runtest_menu
from framework.env import BUILDTEST_ROOT, BUILDTEST_LOGDIR, BUILDTEST_MODULE_NAMING_SCHEME, BUILDTEST_SOURCEDIR, BUILDTEST_TESTDIR, BUILDTEST_MODULE_EBROOT, BUILDTEST_EASYCONFIGDIR, logID
from framework.modules import get_unique_software, module_version_relation, list_toolchain, software_exists, toolchain_exists, check_software_version_in_easyconfig
from framework.testgen import generate_binary_test
from framework.master import recursive_gen_test
from framework.tools.generic import check_buildtest_setup, print_set
#from framework.tools.file import *
from framework.tools.scan import scantest
from framework.tools.software import get_appname, get_appversion, get_toolchain_name, get_toolchain_version
#from framework.parser.functions import *
from framework.parser.args import buildtest_parsermenu
from framework.parser.args import get_arg_version, get_arg_check_setup, get_arg_findconfig, get_arg_findtest, get_arg_software, get_arg_toolchain, get_arg_list_toolchain
from framework.parser.args import get_arg_list_unique_software, get_arg_software_version_relation, get_arg_scantest, get_arg_module_naming_scheme, get_arg_system
from framework.parser.args import get_arg_testset, get_arg_verbose, get_arg_runtest
#from framework.parser.parser import *
from framework.testmodules.testsets import run_testset

import subprocess
import argparse
import logging
from datetime import datetime
import fnmatch
import glob

def main():
	module=""
	version=""

	args = buildtest_parsermenu()


	# convert args into a dictionary
	args_dict = vars(args)

	version = get_arg_version(args_dict)
	check_setup = get_arg_check_setup(args_dict)
	findconfig = get_arg_findconfig(args_dict)
	findtest = get_arg_findtest(args_dict)
	software = get_arg_software(args_dict)
	toolchain = get_arg_toolchain(args_dict)
	list_toolchain_flag = get_arg_list_toolchain(args_dict)
	list_unique_software = get_arg_list_unique_software(args_dict)
	software_version_relation = get_arg_software_version_relation(args_dict)
	scan = get_arg_scantest(args_dict)
	BUILDTEST_MODULE_NAMING_SCHEME=get_arg_module_naming_scheme(args_dict)
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
	
	if scan == True:
		scantest()


	os.environ["BUILDTEST_LOGDIR"] = os.path.join(BUILDTEST_ROOT,"log")
	os.environ["BUILDTEST_LOGFILE"] = datetime.now().strftime("buildtest_%H_%M_%d_%m_%Y.log")
	logdir =  os.environ["BUILDTEST_LOGDIR"]
	logfile = os.environ["BUILDTEST_LOGFILE"]

	logpath = os.path.join(logdir,logfile)
	
	# if log directory is not created do it automatically. Typically first run in buildtest will 
	# after git clone will run into this condition
	if not os.path.exists(logdir):
		os.makedirs(logdir)
		print "Creating Log directory: ", logdir

	#logging.basicConfig(filename=logfile)
	logger = logging.getLogger(logID)
	fh = logging.FileHandler(logpath)
        formatter = logging.Formatter('%(asctime)s [%(filename)s:%(lineno)s - %(funcName)5s() ] - [%(levelname)s] %(message)s')
 	fh.setFormatter(formatter)
	logger.addHandler(fh)
	logger.setLevel(logging.DEBUG)

	cmd = "env | grep BUILDTEST"
	ret = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	output = ret.communicate()[0]
	output = output.split("\n")

	for line in output:
		logger.debug(line)

	# when no argument is specified to -fc then output all yaml files
	if findconfig == "all": 

		logger.info("List of YAML configs found")
                logger.info("----------------------------------")

		for root, dirs, files in os.walk(BUILDTEST_SOURCEDIR):
                        for file in files:
                                if file.endswith(".yaml"):
                                        print os.path.join(root,file)
                                        logger.info("%s",os.path.join(root,file))

		print "Writing Log file to:", logpath

		sys.exit(0)
	# otherwise report yaml file based on argument. If -fc is not specified then args.findconfig is set
	# to None and we don't want to run this section unless a -fc is specified along with an argument other than
	# all
	elif findconfig != None:

		find_arg = args_dict["findconfig"]

		logger.info("List of YAML configs found")
		logger.info("-----------------------------------")


 		for root, dirs, files in os.walk(BUILDTEST_SOURCEDIR):
                        for file in files:
                                if file.endswith(".yaml"):

                                        if find_arg in os.path.basename(file):
                                                print os.path.join(root,file)
                                                logger.info("%s",os.path.join(root,file))

		print "Writing Log file to:", logpath

		sys.exit(0)

	# report all buildtest generated test scripts
	if findtest == "all":

		logger.info("List of test found")
		logger.info("----------------------------------")
		for root, dirs, files in os.walk(BUILDTEST_TESTDIR):
			for file in files:
				if file.endswith(".sh"):
					print os.path.join(root,file)
					logger.info("%s",os.path.join(root,file))


		print "Writing Log file to:", logpath
		sys.exit(0)


	# otherwise report test scripts based on argument. If -ft is not specified then args.findtest is None
	# so we don't want to run section below everytime. Only when -ft is specified
	elif findtest != None:


		find_arg = args_dict["findtest"]

		
                logger.info("List of test found")
                logger.info("----------------------------------")
                for root, dirs, files in os.walk(BUILDTEST_TESTDIR):
                        for file in files:
                                if file.endswith(".sh"):

					if find_arg in os.path.basename(file):
						print os.path.join(root,file)
						logger.info("%s",os.path.join(root,file))

                print "Writing Log file to:", logpath

		sys.exit(0)

	if list_toolchain_flag == True:
		toolchain_set=list_toolchain()
		text = """ \n
			 List of Toolchains: 
			 -------------------- \n"""
		print text
		print_set(toolchain_set)

                print "Writing Log file to:", logpath
		sys.exit(0)

	if list_unique_software == True:
		software_set=get_unique_software(BUILDTEST_MODULE_EBROOT)
		text =  """ \n
		       List of Unique Software: 
		       ---------------------------- \n """
		print text
		print_set(software_set)	
		
		print "Writing Log file to:", logpath
		sys.exit(0)

	if software_version_relation == True:
		module_version_relation(BUILDTEST_MODULE_EBROOT)
		print "Writing Log file to:", logpath
		sys.exit(0)

	# generate system pkg test
	if system != None:
		systempkg = args.system
		if systempkg == "all":

			logger.info("Generating all system package tests from YAML files in %s", os.path.join(BUILDTEST_SOURCEDIR,"system"))

			os.environ["BUILDTEST_LOGDIR"] = os.path.join(logdir,"system","all")
			systempkg_list = os.listdir(os.path.join(BUILDTEST_SOURCEDIR,"system"))

			logger.info("List of system packages to test: %s ", systempkg_list)

			for pkg in systempkg_list:
				generate_binary_test(args_dict,verbose,pkg)
		else:
			os.environ["BUILDTEST_LOGDIR"] = os.path.join(logdir,"system",systempkg)
			#logcontent += systempkg_generate_binary_test(systempkg,verbose,logdir)
			generate_binary_test(args_dict,verbose,systempkg)


		# if log directory is not created then create directory recursively
		if not os.path.exists(os.environ["BUILDTEST_LOGDIR"]):
			os.makedirs(os.environ["BUILDTEST_LOGDIR"], 0755 )
			logger.warning("Directory not found: %s will create it", os.environ["BUILDTEST_LOGDIR"])

		#cmd = "mv " + logpath + " " + os.environ["BUILDTEST_LOGDIR"]
		#os.system(cmd)
		destpath = os.path.join(os.environ["BUILDTEST_LOGDIR"],logfile)
		os.rename(logpath, destpath)
		
		print "Writing Log file to:", os.path.join(os.environ["BUILDTEST_LOGDIR"],logfile)
		sys.exit(0)
	# when -s is specified
	if software != None:
		software=software.split("/")


                if toolchain == None:
                        toolchain = "dummy/dummy"

                toolchain=toolchain.split("/")

		appname=get_appname()
		appversion=get_appversion()
		tcname = get_toolchain_name()
		tcversion = get_toolchain_version()	

		logger.debug("Generating Test from EB Application")

		logger.debug("Software: %s", appname)
		logger.debug("Software Version: %s", appversion)
		logger.debug("Toolchain: %s", tcname)
		logger.debug("Toolchain Version: %s", tcversion)

		logger.debug("Checking if software: %s/%s exists",appname,appversion)

		# checking if software exists
		software_exists(software,verbose)
	

		# only check toolchain argument with module tree if its not dummy toolchain
		if ["dummy","dummy"] != toolchain:
			# checking if toolchain argument has a valid module file
			software_exists(toolchain,verbose)

		# checking if its a valid toolchain 
		toolchain_exists(toolchain,verbose)
	

		# check that the software,toolchain match the easyconfig.
		ret=check_software_version_in_easyconfig(BUILDTEST_EASYCONFIGDIR,verbose)
		# generate_binary_test(software,toolchain,verbose)
	
		source_app_dir=os.path.join(BUILDTEST_SOURCEDIR,"ebapps",appname)

	        configdir=os.path.join(source_app_dir,"config")
	        codedir=os.path.join(source_app_dir,"code")
		os.environ["BUILDTEST_LOGDIR"]=os.path.join(BUILDTEST_ROOT,"log",appname,appversion,tcname,tcversion)
		logdir=os.environ["BUILDTEST_LOGDIR"]


		logger.debug("Source App Directory: %s",  source_app_dir)
		logger.debug("Config Directory: %s ", configdir)
		logger.debug("Code Directory: %s", codedir)

		generate_binary_test(args_dict,verbose,None)
		# this generates all the compilation tests found in application directory ($BUILDTEST_SOURCEDIR/ebapps/<software>)
		recursive_gen_test(configdir,codedir,verbose)
	
		# if flag --testset is set, then 
		if testset !=  None:
			run_testset(args_dict, testset,verbose)
	
		if not os.path.isdir(logdir):
			cmd = "mkdir -p " + logdir
			os.system(cmd)
			logger.debug("Executing Command: %s", cmd)

			
		cmd = "mv " + logpath + " " + logdir
		os.system(cmd)
		logger.debug("Executing command: %s ", cmd)
		
		print "Writing Log file: ", os.path.join(logdir,logfile)

if __name__ == "__main__":
        main()

