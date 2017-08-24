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
	BUILDTEST_LOGCONTENT.append("-------------------------------- \n")
	BUILDTEST_LOGCONTENT.append("func: get_unique_software \n")
	BUILDTEST_LOGCONTENT.append("-------------------------------- \n")
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

		BUILDTEST_LOGCONTENT.append("Unique Software Packages from module tree: " + moduletree + "\n")
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


	print module_set
	# for every software in set, search easyconfig files to find version tag to get software to version relationship
	for item in  module_set:
		print "item=",item
		easyconfigfiles=os.popen("find " + os.path.join(BUILDTEST_EASYCONFIGDIR,item) + " -name *.eb -type f"). read().rstrip()
		print "ebfiles=",easyconfigfiles
		listofebfiles=easyconfigfiles.split("\n")
		version_set=set()
		# for software package X, get all version and store them in a set to avoid duplicate addition, only care for unique versions on the system
		for ebfile in listofebfiles:
			# extract version tag from easyconfig, there is a case where altversion = gets picked up so only get 1st entry which should be version
			cmd="""grep "version =" """ + ebfile + """ | cut -f3 -d " " | head -n 1"""
			version=os.popen(cmd).read().rstrip()
			# remove the leading and trailing ' character
			version_set.add(version[1:-1])
			
		# store version set in dictionary that is indexed by software
		module_dict[item]=version_set
	return module_dict

def get_toolchain(easyconfigdir):
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
	return toolchain

def software_exists(software,verbose):
	"""
	checks whether software exist, there must be a module file present with the 
	same name specified as the argument. 
	"""
	success_msg = "Checking Software: " + software[0] + "/" + software[1] + "  ... SUCCESS"  
	fail_msg = "Checking Software: " + software[0] + "/" + software[1] + " ... FAILED"
	if len(software) != 2:
		print fail_msg
		msg = "Too many arguments, -s takes argument <software>,<version> \n"
		print msg
		BUILDTEST_LOGCONTENT.append(msg)
		update_logfile(verbose)
		sys.exit(1)
	
	softwarecollection=get_unique_software_version(BUILDTEST_MODULE_EBROOT)
	software_name=software[0]+" "+software[1]
	if software_name not in softwarecollection:
		print fail_msg
		msg = "Can't find software: " +  software_name + "\n"
		print msg
                BUILDTEST_LOGCONTENT.append(msg)
                update_logfile(verbose)
		sys.exit(1)

	text = "Software:" + str(software) + " found in system \n"
	BUILDTEST_LOGCONTENT.append(text)
	
        print success_msg

def toolchain_exists(toolchain,verbose):
	"""
	checks to see if toolchain passed on command line exist in toolchain list
	"""
	success_msg = "Checking Toolchain: " + toolchain[0] + "/" + toolchain[1] + " ... SUCCESS"
	fail_msg = "Checking Toolchain: " + toolchain[0] + "/" + toolchain[1] + " ... FAILED"
        # catch all exception cases for invalid value for -t flag
        if len(toolchain) != 2:
		print fail_msg
                msg =  "Too many arguments, -t takes argument <toolchain-name>,<toolchain-version> \n"
                print msg
		BUILDTEST_LOGCONTENT.append(msg)
		update_logfile(verbose)
                sys.exit(1)

	toolchain_list=get_toolchain(BUILDTEST_EASYCONFIGDIR)
	tcname = toolchain[0]
	tcversion = toolchain[1]
	toolchain_name = tcname + "/" + tcversion
	BUILDTEST_LOGCONTENT.append("-------------------------------------------\n")
	BUILDTEST_LOGCONTENT.append("func: toolchain_exists \n")
	BUILDTEST_LOGCONTENT.append("-------------------------------------------\n")

	# report error if toolchain is not found in toolchain list. toolchain list only
	# contains the name of toolchain and not the version
	if tcname not in toolchain_list:
		print fail_msg
		msg = "Can't find toolchain: " + tcname + "\n"
		print msg
		BUILDTEST_LOGCONTENT.append(msg)
	        update_logfile(verbose)
		sys.exit(1)

	msg = "Toolchain + " + toolchain_name + " found in system"
	BUILDTEST_LOGCONTENT.append(msg)
	print success_msg

def check_software_version_in_easyconfig(easyconfig_repo,software,toolchain, verbose):
	"""
	return True if name,version+versionsuffix,toolchain from command line is found 
	from easyconfig, False otherwise
	"""
	success_msg = "Checking easyconfig file ... SUCCESS"
	fail_msg = "Checking easyconfig file ... FAILED"
	appname,appversion=software
	tcname,tcversion=toolchain
	
        # if user is testing a software package that is a hidden module file, strip the leading "." for checking
        if isHiddenFile(appversion):
                appversion = stripHiddenFile(appversion)
                BUILDTEST_LOGCONTENT.append("Stripping leading . from application version: " + appversion + "\n")

        # if user specified a toolchain version that is a hidden module file, strip leading "." 
        if isHiddenFile(tcversion):
                tcversion = stripHiddenFile(tcversion)
                BUILDTEST_LOGCONTENT.append("Stripping leading . from toolchain version: " + tcversion + "\n")


	cmd="find " + easyconfig_repo  + " -name " + appname+"-"+appversion+"*.eb -type f"         
	easyconfigfiles=os.popen(cmd).read().rstrip().split("\n")

	BUILDTEST_LOGCONTENT.append("--------------------------------------------- \n")
	BUILDTEST_LOGCONTENT.append("func: check_software_version_in_easyconfig \n")
	BUILDTEST_LOGCONTENT.append("--------------------------------------------- \n")

	BUILDTEST_LOGCONTENT.append("buildtest will search the following eb files \n")
	for ebfile in easyconfigfiles:
		BUILDTEST_LOGCONTENT.append(ebfile + "\n")

	# boolean value to check if eb file found with parameters for software and toolchain
	match=False    

	for ebfile in easyconfigfiles:
		# get name tag from easyconfig
		cmd="""grep "name = " """ + ebfile + """ | cut -f3 -d " " """
		BUILDTEST_LOGCONTENT.append("executing command: " + cmd + "\n")
		
		name=os.popen(cmd).read()
		BUILDTEST_LOGCONTENT.append("result: " + name + "\n")

		# get version tag from easyconfig, possibility for multiple occurence so get 1st entry
		cmd="""grep "version = " """ + ebfile + """ | cut -f3 -d " " | head -n1 """
		BUILDTEST_LOGCONTENT.append("executing command: " + cmd + "\n")
		version=os.popen(cmd).read()
		BUILDTEST_LOGCONTENT.append("result: "  + version + "\n")

		cmd=""" grep "toolchain = " """ + ebfile + """ | cut -f4 -d " " | tr -d "," """
		BUILDTEST_LOGCONTENT.append("executing command: " + cmd + "\n")
		toolchain_name=os.popen(cmd).read()
		BUILDTEST_LOGCONTENT.append("result: " + toolchain_name + "\n")


		cmd=""" grep "toolchain = " """ + ebfile + """ | cut -f6 -d " " | tr -d "}" """
		BUILDTEST_LOGCONTENT.append("executing command: " + cmd + "\n")
		toolchain_version=os.popen(cmd).read()
		BUILDTEST_LOGCONTENT.append(toolchain_version + "\n")

		# strip character ' and newline
		name=name.replace('\'','')
	        name=name.replace('\n','') 
		version=version.replace('\'', '')
		version=version.replace('\n','')
		toolchain_name=toolchain_name.replace('\'','')
		toolchain_name=toolchain_name.replace('\n','')
		toolchain_version=toolchain_version.replace('\'','')
		toolchain_version=toolchain_version.replace('\n','')
	

		BUILDTEST_LOGCONTENT.append("Before Stripping characters \n")
		BUILDTEST_LOGCONTENT.append("name: " + name + "\n")
		BUILDTEST_LOGCONTENT.append("version: " + version + "\n")
		BUILDTEST_LOGCONTENT.append("toolchain name:" + toolchain_name + "\n")
		BUILDTEST_LOGCONTENT.append("toolchain version:" + toolchain_version + "\n")

		BUILDTEST_LOGCONTENT.append("\n")
                BUILDTEST_LOGCONTENT.append("After Stripping characters ' and newline \n")
                BUILDTEST_LOGCONTENT.append("name: " + name + "\n")
                BUILDTEST_LOGCONTENT.append("version: " + version + "\n")
                BUILDTEST_LOGCONTENT.append("toolchain name:" + toolchain_name + "\n")
                BUILDTEST_LOGCONTENT.append("toolchain version:" + toolchain_version + "\n")
		BUILDTEST_LOGCONTENT.append("\n")


		# get name of eb file and remove .eb extension
		ebname=os.popen("basename " + ebfile).read()
		BUILDTEST_LOGCONTENT.append("easyconfig file= " + ebname)

		ebname=ebname[:-4]
		BUILDTEST_LOGCONTENT.append("stripping file extension .eb \n")
		BUILDTEST_LOGCONTENT.append("easyconfig file:"+ ebname + "\n")
		
		#print "local logcontent"
		#print logcontent
		# in case toolchain version uses '' set it to dummy 
		if toolchain_version == '':
			toolchain_version="dummy"
		# alter eb_name_format for dummy toolchain
		if toolchain_name == "dummy":
			eb_name_format=name+"-"+version
		else:
			# eb name format used for comparison to calculate versionsuffx
			eb_name_format=name+"-"+version+"-"+toolchain_name+"-"+toolchain_version

		BUILDTEST_LOGCONTENT.append("eb name format using string concat of <name>-<version>-<toolchain-name>-<toolchain-version> \n")
		BUILDTEST_LOGCONTENT.append("eb name format string: " + eb_name_format + "\n")

		# There is no version suffix when file name is just software-version-toolchain
		# determine starting position index in easyconfig filename to calculate versionsuffix. If its a dummy toolchain start with version, otherwise from toolchain version
		if toolchain_name == "dummy":
			startpos=ebname.find(version)+len(version)
		else:
			# extract version suffix 
			startpos=ebname.find(toolchain_version)+len(toolchain_version)
		endpos=len(ebname)
		versionsuffix=ebname[startpos:endpos]

		# variable used for comparison
		version_versionsuffix=version + versionsuffix

		BUILDTEST_LOGCONTENT.append("Extracting version suffix from eb name: " + ebname + "\n")
		BUILDTEST_LOGCONTENT.append("Version Suffix: " + versionsuffix + "\n")
		BUILDTEST_LOGCONTENT.append("Version + Version Suffix: " + version_versionsuffix + "\n")

		if name == appname and version_versionsuffix == appversion and toolchain_name == tcname and toolchain_version == tcversion:
			BUILDTEST_LOGCONTENT.append("Comparing strings: the following strings \n") 
			BUILDTEST_LOGCONTENT.append("name:" + name + " with appname = " + appname + " AND ")
			BUILDTEST_LOGCONTENT.append("version_versionsuffix: " + version_versionsuffix + " with appversion: " + appversion + " AND ")
			BUILDTEST_LOGCONTENT.append("toolchain_name: " + toolchain_name + " with tcname: " + tcname + " AND ")
			BUILDTEST_LOGCONTENT.append("toolchain_version: " + toolchain_version + "with tcversion: " + tcversion + "\n")
			print success_msg
			return True

	# mismatch in easyconfig entries for name,version+versionsuffix, and toolchain with specified entries
	if match == False:
		print fail_msg
	 	msg = "ERROR: Attempting to  find easyconfig file  " + appname + "-" + appversion + "-" + tcname + "-" + tcversion + ".eb"
		print msg
		BUILDTEST_LOGCONTENT.append(msg)
		update_logfile(verbose)
		sys.exit(1)
