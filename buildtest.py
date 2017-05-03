############################################################################
#
#  Copyright 2017
#
#   https://github.com/shahzebsiddiqui/BuildTest
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

from setup import *
from modules import *
from utilities import *
from testgen import *
from parser import *

import argparse
import sys
module=""
version=""

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--software", help=" Specify software package to test")
parser.add_argument("-t", "--toolchain",help=" Specify toolchain for the software package") 
parser.add_argument("-lt", "--list-toolchain",help="retrieve toolchain used based on the easyconfig files provided by BUILDTEST_EASYCONFIGDIR", action="store_true")
parser.add_argument("-ls", "--list-unique-software",help="retrieve all unique software found in your module tree specified by BUILDTEST_MODULETREE", action="store_true")
parser.add_argument("-svr", "--software-version-relation", help="retrieve a relationship between software and version found in module files", action="store_true")
parser.add_argument("--system", help=""" Build test for system packages
					 To build all system package test use --system all """)
parser.add_argument("-v", "--verbose", help="increase verbosity level", type=int, choices=[1,2])

args = parser.parse_args()


# convert args into a dictionary
args_dict=vars(args)
#print get_module_list(BUILDTEST_MODULEROOT)
#print get_unique_software(BUILDTEST_MODULEROOT)
#sys.exit(1)
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
	text += "BUILDTEST TEST DIRECTORY:" + BUILDTEST_TESTDIR + "\n"
	text += "==================================================================== " + "\n"
	print text
	print

	
	logcontent += text

	verbose=args_dict["verbose"]

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
	software_set,logcontent_substr=get_unique_software(BUILDTEST_MODULEROOT)
	logcontent+=logcontent_substr
	print """
	       List of Unique Software: 
	       ---------------------------- """
	print_set(software_set)	
if args_dict["software_version_relation"] == True:
	software_version_dict,logcontent_substr=module_version_relation(BUILDTEST_MODULEROOT)
	logcontent+=logcontent_substr
	print """
		Software Version Relationship:
		-------------------------------
		"""
	print_dictionary(software_version_dict)

if args.software:
	software=args.software.split("/")

# set toolchain to dummy when its not specified. 
if not args.toolchain:
	toolchain="dummy/dummy".split("/")
else:
	toolchain=args.toolchain.split("/")


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

# when -s is specified
if args.software != None:

	appname=software[0]
	appversion=software[1]

	# default value assuming toolchain is not specified
	tcname="dummy"
	tcversion="dummy"
	if args.toolchain != None:
		tcname=toolchain[0]
		tcversion=toolchain[1]
	

	# checking if its a valid software
	software_exists(software)
	if verbose >= 1:
		text = "Software:" + appname + " " + appversion + " found in system \n"
		print text
		logcontent += text + "\n"

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
	logdir = os.path.join(BUILDTEST_ROOT,"log",appname,appversion,tcname,tcversion)

	logcontent += "Source App Directory:" +  source_app_dir + "\n"
	logcontent += "Config Directory: " + configdir + "\n"
	logcontent += "Code Directory:" + codedir + "\n"

	logcontent += generate_binary_test(software,toolchain,source_app_dir,verbose,logdir)
	# if config directory exists then process .yaml files to build source test
	if os.path.isdir(configdir):
	        #for filename in os.listdir(configdir):
		for root,subdirs,files in os.walk(configdir):
			
        	        #filepath=configdir+filename
			for file in files:
				filepath=os.path.join(root,file)
				subdir=os.path.basename(root)
				# if there is no subdirectory in configdir that means subdir would be set to "config" so it can
				# be set to empty string in order to concat codedir and subdir. This way both subdirectory and 
				# and no subdirectory structure for yaml will work
				if subdir == "config":
					subdir = ""
				code_destdir=os.path.join(codedir,subdir)
				configmap=parse_config(software,toolchain,filepath,code_destdir)		
				# error processing config file, then parse_config will return an empty dictionary
				if len(configmap) == 0:
					continue
				logcontent+=generate_source_test(software,toolchain,configmap,code_destdir,verbose,subdir,logdir)

     
update_logfile(logdir,logcontent,verbose)
