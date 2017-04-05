#!/usr/bin/python
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
parser.add_argument("-v", "--verbose", help="increase verbosity level", type=int, choices=[1,2])

args = parser.parse_args()


# convert args into a dictionary
args_dict=vars(args)

#print get_module_list(BUILDTEST_MODULEROOT)
#print get_unique_software(BUILDTEST_MODULEROOT)
#sys.exit(1)
verbose=0
if args_dict["verbose"] >= 1:
	print "===================================================================="
	print "BUILDTEST ROOT DIRECTORY: ", BUILDTEST_ROOT
	print "BUILDTEST SOURCE DIRECTORY: ", BUILDTEST_SOURCEDIR
	print "BUILDTEST EASYCONFIGDIR: ", BUILDTEST_EASYCONFIGDIR
	print "BUILDTEST TEST DIRECTORY :", BUILDTEST_TESTDIR
	print "===================================================================="
	print 
	verbose=args_dict["verbose"]

if args_dict["list_toolchain"] == True:
	toolchain_set=get_toolchain(BUILDTEST_EASYCONFIGDIR)
	print """ 
		List of Toolchains:
		--------------------
	      """
	print_set(toolchain_set)
if args_dict["list_unique_software"] == True:
	software_set=get_unique_software(BUILDTEST_MODULEROOT)
	print """
	       List of Unique Software: 
	       ---------------------------- """
	print_set(software_set)	
if args_dict["software_version_relation"] == True:
	software_version_dict=module_version_relation(BUILDTEST_MODULEROOT)
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

appname=software[0]
appversion=software[1]
tcname=toolchain[0]
tcversion=toolchain[1]
if args.software != None:
	# checking if its a valid software
	ret = software_exists(software)
	if verbose >= 1:
		print "Software:",appname,appversion, "  found in system"

	# checking if its a valid toolchain 
	ret = toolchain_exists(software,toolchain)
	if verbose >= 1:
		print "Toolchain:",tcname,tcversion, "  found in system"

	# check that the software,toolchain match the easyconfig.
	check_software_version_in_easyconfig(BUILDTEST_EASYCONFIGDIR,software,toolchain)
	
	generate_binary_test(software,toolchain,verbose)
	
        configdir=BUILDTEST_SOURCEDIR + appname + "/config/"
        codedir=BUILDTEST_SOURCEDIR + appname + "/code/"
	# if config directory exists then process .yaml files to build source test
	if os.path.isdir(configdir):
	        for filename in os.listdir(configdir):
        	        filepath=configdir+filename
			configmap=parse_config(software,toolchain,filepath,codedir)		
			# error processing config file, then parse_config will return an empty dictionary
			if len(configmap) == 0:
				continue
			generate_source_test(software,toolchain,configmap,codedir,verbose)


