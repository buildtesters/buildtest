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
This python module does the following
	 - get module listing
	 - get unique application
	 - get unique application version
	 - get easybuild toolchains
 	 - check if software exists based on argument -s
	 - check if toolchain exists based on argument -t
	 - check if easyconfig passes

:author: Shahzeb Siddiqui (Pfizer)
"""
from framework.env import *
from framework.tools.file import *
from framework.tools.software import *
import logging
import os
import sys


def get_module_list(moduletree):
	"""
	returns a complete list of modules found in module tree
	"""
	find_cmd_module=os.popen("find " + moduletree + " -type f """).read()
        modulelist=find_cmd_module.rstrip().split('\n')
	return modulelist

def get_unique_software(moduletrees):
	"""
	returns a set of software packages found in the module tree
	"""
	logger = logging.getLogger(logID)
	logger.info("Traversing Module Tree: %s to find all unique software", moduletrees)

	moduletreelist=moduletrees.split(":")
	module_set=set()
	for moduletree in moduletreelist:
		modulelist=get_module_list(moduletree)
		module_set=set()
		for module in modulelist:
                	# extract the module name from filepath
			modulename=os.path.basename(os.path.dirname(module))
			#modulename=os.popen(os.path.basename(module)).read().rstrip()
			module_set.add(modulename)

	logger.info("List of modules found:")
	logger.info("----------------------------------------")
	logger.info("Software = %s", list(module_set))
	return sorted(module_set)

def get_unique_software_version(moduletree):
	"""
	returns a set of software-version collection found in module files. Duplicates are 
	ignored for instance, same package version is built with two different toolchains
	"""
        moduleversion_set=set()
	modulelist=get_module_list(moduletree)
		
  	for module in modulelist:
               	# extract the module name and version from the file path returned from find
		modulename = os.path.basename(os.path.dirname(module))
		version=os.path.basename(module)
		# skip .version files
		if version == ".version":
			continue

	        # if modulefile is lua extension then strip extension from version
                if version[-4:] == ".lua":
               	        version=version[:-4]
                
		moduleversion_set.add(modulename+" "+version)

	return sorted(moduleversion_set)

def module_version_relation(moduletree):
	"""
	relationship between software name and version. The function will return a 
	dictionary with key values as software name and values will be a set of version
	"""
	modulelist=get_module_list(moduletree)

	module_set=get_unique_software(moduletree)
	# This set contains one entry of sorted lists of modules, need to iterate over list and not set.
	#module_set = module_set[0]

	# dictionary used for keeping a relationship between software name and its corresponding versions found as modulefiles
	module_dict = {}

	logger = logging.getLogger(logID)
	logger.info("Calculating Application Modules with corresponding versions ...")

	# for every app iterate over module tree and add unique version in set, then add this to a dictionary. That way 
	# a dictionary can reference via key,value where key is application name and value is the list of versions
	for item in  module_set:
		version_set = set()
		logger.debug("Application: %s", item)
		for app in modulelist:
			#logger.debug("ModuleFile: %s", app)
			name = os.path.basename(os.path.dirname(app))

			if item != name:
				continue


			version = os.path.basename(app)
			version = os.path.splitext(version)[0]
			logger.debug("Extracting Version: %s from ModuleFile: %s", version, app)

			# only add module version to set when module name is found in tree
			#if item == name:
			version_set.add(version)
			logger.debug("APPLICATION: %s - Adding %s to version_set: %s ",name, version, list(version_set))

		module_dict[item] = version_set

	return module_dict

def list_toolchain():
	"""
	return the set of toolchains found in the easyconfig directory 
	"""
        toolchain = [
        "ClangGCC",
	"CrayCCE",
	"CrayGNU",
	"CrayIntel",
	"CrayPGI",
	"GCC",
	"GCCcore",
	"GNU",
	"PGI",
	"cgmpich",
	"cgmpolf",
	"cgmvapich2",
	"cgmvolf",
	"cgompi",
	"cgoolf",
	"dummy",
	"foss",
	"gcccuda",
 	"gimkl",
	"gimpi",
	"gmacml",
	"gmpich",
	"gmpich2",
	"gmpolf",
	"gmvapich2",
	"gmvolf",
	"goalf",
	"gompi",
	"gompic",
	"goolf",
	"goolfc",
        "gpsmpi",
	"gpsolf",
	"gqacml",
	"iccifort",
	"iccifortcuda",
	"ictce",
	"iimkl",
	"iimpi",
	"iimpic",
	"iiqmpi",
	"impich",
	"impmkl",
	"intel",
	"intel-para",
	"intelcuda",
	"iomkl",
	"iompi",
	"ipsmpi",
	"iqacml",
	"ismkl",
	"pomkl",
	"pompi",
	"xlcxlf",
	"xlmpich",
	"xlmpich2",
	"xlmvapich2",
	"xlompi",
        ]

	logger = logging.getLogger(logID)
	logger.info("List of EB Toolchains")
	logger.info("--------------------------------------")
	logger.info("EB Toolchains = %s", toolchain)

	return toolchain

def software_exists(software,verbose):
	"""
	checks whether software exist, there must be a module file present with the 
	same name specified as the argument. 
	"""

	success_msg = "Checking Software: " + software[0] + "/" + software[1] + "  ... SUCCESS"  
	fail_msg = "Checking Software: " + software[0] + "/" + software[1] + " ... FAILED"

	logger = logging.getLogger(logID)

	logger.debug("Checking argument list length for software, must be equal to 2")
	if len(software) != 2:
		print fail_msg
		msg = "Too many arguments, -s takes argument <software>,<version> \n"
		print msg
		logger.error("%s",msg)
		sys.exit(1)

	softwarecollection=get_unique_software_version(BUILDTEST_MODULE_EBROOT)
	software_name=software[0]+" "+software[1]

	logger.debug("Checking %s is found in software version list", software_name)

	if software_name not in softwarecollection:
		print fail_msg
		msg = "Can't find software: " +  software_name + "\n"
		print msg
                logger.error("%s",fail_msg)
		sys.exit(1)

	logger.info("%s",success_msg)
	
        print success_msg

def toolchain_exists(toolchain,verbose):
	"""
	checks to see if toolchain passed on command line exist in toolchain list
	"""
	success_msg = "Checking Toolchain: " + toolchain[0] + "/" + toolchain[1] + " ... SUCCESS"
	fail_msg = "Checking Toolchain: " + toolchain[0] + "/" + toolchain[1] + " ... FAILED"

	logger = logging.getLogger(logID)

        # catch all exception cases for invalid value for -t flag
        if len(toolchain) != 2:
		print fail_msg
                msg =  "Too many arguments, -t takes argument <toolchain-name>,<toolchain-version> \n"
                print msg
		logger.error("%s", msg)
                sys.exit(1)

	toolchain_list=list_toolchain()
	tcname = toolchain[0]
	tcversion = toolchain[1]
	toolchain_name = tcname + "/" + tcversion

	# report error if toolchain is not found in toolchain list. toolchain list only
	# contains the name of toolchain and not the version
	if tcname not in toolchain_list:
		print fail_msg
		msg = "Can't find toolchain: " + tcname + "\n"
		print msg
		logger.error("%s", msg)
		sys.exit(1)

	msg = "Toolchain + " + toolchain_name + " found in system"
	logger.info("%s",msg)
	print success_msg
	logger.info("%s",success_msg)

def check_software_version_in_easyconfig(easyconfig_repo, verbose):
	"""
	return True if name,version+versionsuffix,toolchain from command line is found 
	from easyconfig, False otherwise
	"""
	success_msg = "Checking easyconfig file ... SUCCESS"
	fail_msg = "Checking easyconfig file ... FAILED"
	appname = get_appname()
	appversion = get_appversion()
	tcname = get_toolchain_name()
	tcversion = get_toolchain_version()
	
	logger = logging.getLogger(logID)

        # if user is testing a software package that is a hidden module file, strip the leading "." for checking
        if isHiddenFile(appversion):
                appversion = stripHiddenFile(appversion)
                logger.debug("Stripping leading . from application version: %s ", appversion)

	# only check if toolchain version is a hidden module  when toolchain is specified by checking length
	if len(tcversion) != 0:
	        # if user specified a toolchain version that is a hidden module file, strip leading "." 
	        if isHiddenFile(tcversion) :
        	        tcversion = stripHiddenFile(tcversion)
                	logger.debug("Stripping leading . from toolchain version: ", tcversion)

	# for Flat Naming Scheme -s will take APP/Version-Toolchain so need to take Toolchain out for comparison
        if BUILDTEST_MODULE_NAMING_SCHEME == "FNS":
                arg_tc_name = toolchain[0] + "-" + toolchain[1]
                appversion = appversion.replace(arg_tc_name,'')
		logger.debug("Detected Module Naming Scheme is Flat Naming Scheme")
		logger.debug("Removing toolchain from module version for comparision")
		# stripping last character if which is a "-" because module version in FNS
		# is <version>-<toolchain>
                if appversion[-1] == "-":
                        appversion = appversion[:-1]

	
	cmd="find " + easyconfig_repo  + " -name " + appname+"-"+appversion+"*.eb -type f"         
	logger.debug("Attempting to find all easyconfigs based on appname = %s \t appversion = %s", appname, appversion)
	logger.debug("Executing Command: %s", cmd)
	easyconfigfiles=os.popen(cmd).read().rstrip().split("\n")
	# remove any empty elements in list when there is no eb files found
	easyconfigfiles = [x for x in easyconfigfiles if x]
	# if no easyconfig files found
	if len(easyconfigfiles) == 0:
		if len(tcversion) == 0:
		 	msg = "FAILED to find any easyconfig file with the name " + appname + "-" + appversion + ".eb"
		else:
		 	msg = "FAILED to find any easyconfig file with the name " + appname + "-" + appversion + "-" + tcname + "-" + tcversion + ".eb"
		print msg
		logger.error("%s",msg)
		sys.exit(1)

	# writing easyconfig file path to log
	for ebfile in easyconfigfiles:
		logger.debug("%s",ebfile)

	# boolean value to check if eb file found with parameters for software and toolchain
	match=False    
	for ebfile in easyconfigfiles:
		# get name tag from easyconfig
		cmd="""grep "name = " """ + ebfile + """ | cut -f3 -d " " """
		logger.debug("Executing command: %s ", cmd)
		
		name=os.popen(cmd).read()
		logger.debug("Result: %s", name)

		# get version tag from easyconfig, possibility for multiple occurence so get 1st entry
		cmd="""grep "version = " """ + ebfile + """ | cut -f3 -d " " | head -n1 """
		logger.debug("Executing command: %s", cmd)
		version=os.popen(cmd).read()
		logger.debug("Result: %s", version)

		cmd=""" grep "toolchain = " """ + ebfile + """ | cut -f4 -d " " | tr -d "," """
		logger.debug("Executing command: %s", cmd)
		toolchain_name=os.popen(cmd).read()
		logger.debug("Result: %s", toolchain_name)


		cmd=""" grep "toolchain = " """ + ebfile + """ | cut -f6 -d " " | tr -d "}" """
		logger.debug("Executing command: %s", cmd)
		toolchain_version=os.popen(cmd).read()
		logger.debug("Result: %s",toolchain_version)



		logger.debug("Before Stripping characters")
		logger.debug("name: %s \t version: %s \t toolchain name: %s \t toolchain version: %s", name, version, toolchain_name, toolchain_version)

		# strip character ' and newline
		name=name.replace('\'','')
	        name=name.replace('\n','') 
		version=version.replace('\'', '')
		version=version.replace('\n','')
		toolchain_name=toolchain_name.replace('\'','')
		toolchain_name=toolchain_name.replace('\n','')
		toolchain_version=toolchain_version.replace('\'','')
		toolchain_version=toolchain_version.replace('\n','')
	
		# if toolchain name is dummy in easyconfig, lets force it to "" so checking for dummy toolchain will be with empty quotes	
		if toolchain_name == "dummy":
			toolchain_name = ""
			toolchain_version = ""

		logger.debug("\n")
                logger.debug("After Stripping characters ' and newline")
		logger.debug("name: %s \t version: %s \t toolchain name: %s \t toolchain version: %s", name, version, toolchain_name, toolchain_version)


		# get name of eb file and remove .eb extension
		ebname=os.popen("basename " + ebfile).read()

		logger.debug("Before Stripping File extension(.eb) - FILE: %s", ebname)

		# stripping characters ".eb" plus newline character a total of 4 from end
		ebname=ebname[:-4]

		logger.debug("After Stripping File extension -  FILE: %s", ebname)
		
		# in case toolchain version uses '' set it to dummy 
		if toolchain_version == '':
			toolchain_version=""
		# alter eb_name_format for dummy toolchain
		if toolchain_name == "dummy":
			toolchain_name = ""
			eb_name_format=name+"-"+version
		else:
			# eb name format used for comparison to calculate versionsuffx
			eb_name_format=name+"-"+version+"-"+toolchain_name+"-"+toolchain_version


		# There is no version suffix when file name is just 
		# software-version-toolchain
		# determine starting position index in easyconfig filename to 
		# calculate versionsuffix. If its a dummy toolchain start with 
		# version, otherwise from toolchain version
		if toolchain_name == "":
			startpos=ebname.find(version)+len(version)
		else:
			# extract version suffix 
			startpos=ebname.find(toolchain_version)+len(toolchain_version)

		endpos=len(ebname)
		versionsuffix=ebname[startpos:endpos]

		# variable used for comparison
		version_versionsuffix=version + versionsuffix

		logger.debug("Extracting version suffix from eb name: %s",ebname)
		logger.debug("Version Suffix: %s", versionsuffix)
		logger.debug("Version + Version Suffix: %s", version_versionsuffix)



		logger.debug("All CONDITIONS must pass") 
		logger.debug("NAME String Comparision - STR1: %s \t STR2: %s", name, appname)
		logger.debug("VERSION String Comparision - STR1: %s \t STR2: %s", version_versionsuffix, appversion)
		logger.debug("TOOLCHAIN NAME String Comparision - STR1: %s \t STR2: %s", toolchain_name, tcname)
		logger.debug("TOOLCHAIN VERSION String Comparision - STR1: %s \t STR2: %s", toolchain_version, tcversion)
		# print name,version_versionsuffix, toolchain_name, toolchain_version
		# print appname, appversion, tcname, tcversion
		if name == appname and version_versionsuffix == appversion and toolchain_name == tcname and toolchain_version == tcversion:
			logger.debug("All Checks have PASSED!") 

			print success_msg
			if tcname == "":
				print "found easyconfig file: " + appname + "-" + appversion + ".eb"
			else:
				print "found easyconfig file: " + appname + "-" + appversion + "-" + tcname + "-" + tcversion + ".eb"
			return True
		else:
			logger.debug("All Checks failed to PASSED!") 

	# mismatch in easyconfig entries for name,version+versionsuffix, and toolchain with specified entries
	if match == False:
		if tcname == "":
		 	msg = "ERROR: Attempting to  find easyconfig file  " + appname + "-" + appversion + ".eb"
		else:
		 	msg = "ERROR: Attempting to  find easyconfig file  " + appname + "-" + appversion + "-" + tcname + "-" + tcversion + ".eb"
		print fail_msg
		print msg
		logger.error("%s",msg)
		sys.exit(1)
