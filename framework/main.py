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


from framework.env import BUILDTEST_ROOT, BUILDTEST_LOGDIR, BUILDTEST_MODULE_NAMING_SCHEME, BUILDTEST_SOURCEDIR, BUILDTEST_TESTDIR, BUILDTEST_MODULE_EBROOT, BUILDTEST_EASYCONFIGDIR, BUILDTEST_JOB_EXTENSION, logID
from framework.runtest import runtest_menu
from framework.test.binarytest import generate_binary_test
from framework.test.sourcetest import recursive_gen_test
from framework.test.testsets import run_testset
from framework.tools.check_setup import check_buildtest_setup
from framework.tools.easybuild import list_toolchain, toolchain_exists, check_software_version_in_easyconfig
from framework.tools.generate_yaml import create_system_yaml
from framework.tools.menu import buildtest_menu
from framework.tools.scan import scantest
# from framework.tools.software import get_appname, get_appversion, get_toolchain_name, get_toolchain_version
from framework.tools.software import get_unique_software, software_version_relation, software_exists
from framework.tools.utility import  print_set
from framework.tools.utility import get_appname, get_appversion, get_toolchain_name, get_toolchain_version
from framework.tools.version import buildtest_version

import subprocess
import argparse
import logging
from datetime import datetime
import fnmatch
import glob

def main():
	module=""
	version=""

	args = buildtest_menu()


	# convert args into a dictionary
	args_dict = vars(args)
	
	version = args_dict["version"]
	check_setup = args_dict["check_setup"]
	findconfig = args_dict["findconfig"]
	findtest = args_dict["findtest"]
	software = args_dict["software"]
	toolchain = args_dict["toolchain"]
	list_toolchain_flag = args_dict["list_toolchain"]
	list_unique_software = args_dict["list_unique_software"]
	sw_ver_relation = args_dict["software_version_relation"]
	scan = args_dict["scantest"]
	BUILDTEST_MODULE_NAMING_SCHEME= args_dict["module_naming_scheme"]
	system = args_dict["system"]
	testset = args_dict["testset"]
	runtest = args_dict["runtest"]
	sysyaml = args_dict["sysyaml"]
	ebyaml = args_dict["ebyaml"]
	jobtemplate = args_dict["job_template"]
	
	if version == True:
		buildtest_version()
		sys.exit(1)

	if check_setup == True:
		check_buildtest_setup()
		sys.exit(1)

	if runtest == True:
		runtest_menu()
	
	if scan == True:
		scantest()

	if list_toolchain_flag == True:
                toolchain_set=list_toolchain()
                text = """ \n
                         List of Toolchains:
                         -------------------- \n"""
                print text
                print_set(toolchain_set)

                sys.exit(0)

        if list_unique_software == True:
                software_set=get_unique_software(BUILDTEST_MODULE_EBROOT)
                text =  """ \n
                       List of Unique Software:
                       ---------------------------- \n """
                print text
                print_set(software_set)

                sys.exit(0)

        if sw_ver_relation == True:
                software_version_relation(BUILDTEST_MODULE_EBROOT)
                sys.exit(0)

	if jobtemplate != None:
		if not os.path.isfile(jobtemplate):
			print "Cant file job template file", jobtemplate
			sys.exit(1)

		# checking if extension is job template file extension is valid to detect type of scheduler
		if os.path.splitext(jobtemplate)[1]  not in BUILDTEST_JOB_EXTENSION:
			print "Invalid file extension, must be one of the following extension", BUILDTEST_JOB_EXTENSION
			sys.exit(1)

	if sysyaml != None:
		create_system_yaml(sysyaml)
	
	if ebyaml != None:
		raise NotImplementedError

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

	# generate system pkg test
	if system != None:
		systempkg = args.system
		if systempkg == "all":

			logger.info("Generating all system package tests from YAML files in %s", os.path.join(BUILDTEST_SOURCEDIR,"system"))

			os.environ["BUILDTEST_LOGDIR"] = os.path.join(logdir,"system","all")
			systempkg_list = os.listdir(os.path.join(BUILDTEST_SOURCEDIR,"system"))

			logger.info("List of system packages to test: %s ", systempkg_list)

			for pkg in systempkg_list:
				generate_binary_test(args_dict,pkg)
		else:
			os.environ["BUILDTEST_LOGDIR"] = os.path.join(logdir,"system",systempkg)
			#logcontent += systempkg_generate_binary_test(systempkg,verbose,logdir)
			generate_binary_test(args_dict,systempkg)


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
		software_exists(software)
	

		# only check toolchain argument with module tree if its not dummy toolchain
		if ["dummy","dummy"] != toolchain:
			# checking if toolchain argument has a valid module file
			software_exists(toolchain)

		# checking if its a valid toolchain 
		toolchain_exists(toolchain)
	

		# check that the software,toolchain match the easyconfig.
		ret=check_software_version_in_easyconfig(BUILDTEST_EASYCONFIGDIR)
		# generate_binary_test(software,toolchain,verbose)
	
		source_app_dir=os.path.join(BUILDTEST_SOURCEDIR,"ebapps",appname)

	        configdir=os.path.join(source_app_dir,"config")
	        codedir=os.path.join(source_app_dir,"code")
		os.environ["BUILDTEST_LOGDIR"]=os.path.join(BUILDTEST_ROOT,"log",appname,appversion,tcname,tcversion)
		logdir=os.environ["BUILDTEST_LOGDIR"]


		logger.debug("Source App Directory: %s",  source_app_dir)
		logger.debug("Config Directory: %s ", configdir)
		logger.debug("Code Directory: %s", codedir)

		generate_binary_test(args_dict,None)
		# this generates all the compilation tests found in application directory ($BUILDTEST_SOURCEDIR/ebapps/<software>)
		recursive_gen_test(configdir,codedir)
	
		# if flag --testset is set, then 
		if testset !=  None:
			run_testset(args_dict, testset)
	
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

