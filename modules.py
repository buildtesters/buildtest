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
from utilities import *
import os
import sys

def get_module_list(moduletree):
"""
returns a complete list of modules found in module tree
"""
	find_cmd_module=os.popen("find " + moduletree + " -type f """).read()
        modulelist=find_cmd_module.rstrip().split('\n')
	return modulelist

def get_unique_software(moduletree):
"""
returns a set of software packages found in the module tree
"""
	modulelist=get_module_list(moduletree)
	module_set=set()
	for module in modulelist:
                # extract the module name from filepath
		modulename=os.popen("dirname " + module + " | xargs basename ").read().rstrip()
		module_set.add(modulename)
	return sorted(module_set)

def get_unique_software_version(moduletree):
"""
returns a set of software-version collection found in module files. Duplicates are 
ignored for instance, same package version is built with two different toolchains
"""
	modulelist=get_module_list(moduletree)
        moduleversion_set=set()
        for module in modulelist:
                # extract the module name and version from the file path returned from find
                modulename=os.popen("dirname " + module + " | xargs basename ").read().rstrip()
                version=os.popen("basename " + module ).read().rstrip()

		# skip .version files
		if version == ".version":
			continue

                # if modulefile is lua extension then strip extension from version
                if version[-4:] == ".lua":
                        version=version[:-4]
                
		moduleversion_set.add(modulename+" "+version)

        #print module_set
	return sorted(moduleversion_set)

def module_version_relation(moduletree):
"""
relationship between software name and version. The function will return a 
dictionary with key values as software name and values will be a set of version
"""
	modulelist=get_module_list(moduletree)
	module_set=get_unique_software(moduletree)
	# dictionary used for keeping a relationship between software name and its corresponding versions found as modulefiles
	module_dict = {}

	# for every software in set, search easyconfig files to find version tag to get software to version relationship
	for item in  module_set:
		easyconfigfiles=os.popen("find " + BUILDTEST_EASYCONFIGDIR +  item + " -name *.eb -type f"). read().rstrip()
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
	easyconfigfiles=os.popen("find " + easyconfigdir +  " -name *.eb -type f ").read().rstrip().split("\n")

	# only care about unique toolchains
	toolchain=set()

	# find all toolchains in the easyconfig files
        for ebfile in easyconfigfiles:
                cmd="""grep "toolchain =" """ + ebfile + """ | cut -f4 -d " " | tr -d "'," """
                toolchain_name=os.popen(cmd).read().rstrip()
                cmd="""grep "toolchain =" """ + ebfile + """ | cut -f6 -d " " | tr -d "}'" """
                toolchain_version=os.popen(cmd).read().rstrip()
		toolchain.add(toolchain_name+" "+toolchain_version)
	return toolchain

def software_exists(software):
"""
checks whether software exist, there must be a module file present with the 
same name specified as the argument. 
"""
	if len(software) != 2:
		print "Too many arguments, -s takes argument <software>,<version>"
		sys.exit(1)
	
	softwarecollection=get_unique_software_version(BUILDTEST_MODULEROOT)
	software_name=software[0]+" "+software[1]
	if software_name not in softwarecollection:
		print "Can't find software: ", software_name
		sys.exit(1)
	
def toolchain_exists(software,toolchain):
"""
checks to see if toolchain passed on command line exist in toolchain list
"""
	toolchain_list=get_toolchain(BUILDTEST_EASYCONFIGDIR)

	# if toolchain is installed as hidden file then strip the "." prior to checking in list
	if isHiddenFile(toolchain[1]) == True:
		strip_version=stripHiddenFile(toolchain[1])
		toolchain_name=toolchain[0]+" "+strip_version
	else:
		toolchain_name=toolchain[0]+" "+toolchain[1]

	# catch all exception cases in invalid value for -t flag
	if len(toolchain) != 2:
		print "Too many arguments, -t takes argument <toolchain-name>,<toolchain-version>"
		sys.exit(1)
	# check if toolchain is in list
	if toolchain_name not in toolchain_list:
		print "Can't find toolchain: ", toolchain_name
		sys.exit(1)

def check_software_version_in_easyconfig(moduletree,software,toolchain):
"""
return True if name,version+versionsuffix,toolchain from command line is found 
from easyconfig, False otherwise
"""
	appname=software[0]
	appversion=software[1]	
	tcname=toolchain[0]	
	tcversion=toolchain[1]

	
	cmd="find " + os.path.join(moduletree,appname)  + " -name *.eb -type f"         
	easyconfigfiles=os.popen(cmd). read().rstrip().split("\n")

	# boolean value to check if eb file found with parameters for software and toolchain
	match=False    

	# if user is testing a software package that is a hidden module file, strip the leading "." for checking
	if isHiddenFile(appversion):
		appversion = stripHiddenFile(appversion)

	# if user specified a toolchain version that is a hidden module file, strip leading "." 
	if isHiddenFile(tcversion):
		tcversion = stripHiddenFile(tcversion)

	for ebfile in easyconfigfiles:
		# get name tag from easyconfig
		cmd="""grep "name = " """ + ebfile + """ | cut -f3 -d " " """
		name=os.popen(cmd).read()
	
		# get version tag from easyconfig, possibility for multiple occurence so get 1st entry
		cmd="""grep "version = " """ + ebfile + """ | cut -f3 -d " " | head -n1 """
		version=os.popen(cmd).read()

		cmd=""" grep "toolchain = " """ + ebfile + """ | cut -f4 -d " " | tr -d "," """
		toolchain_name=os.popen(cmd).read()


		cmd=""" grep "toolchain = " """ + ebfile + """ | cut -f6 -d " " | tr -d "}" """
		toolchain_version=os.popen(cmd).read()

		# strip character ' and newline
		name=name.replace('\'','')
	        name=name.replace('\n','') 
		version=version.replace('\'', '')
		version=version.replace('\n','')
		toolchain_name=toolchain_name.replace('\'','')
		toolchain_name=toolchain_name.replace('\n','')
		toolchain_version=toolchain_version.replace('\'','')
		toolchain_version=toolchain_version.replace('\n','')
		
		# get name of eb file and remove .eb extension
		ebname=os.popen("basename " + ebfile).read()
		ebname=ebname[:-4]
		
		# in case toolchain version uses '' set it to dummy 
		if toolchain_version == '':
			toolchain_version="dummy"
		# alter eb_name_format for dummy toolchain
		if toolchain_name == "dummy":
			eb_name_format=name+"-"+version
		else:
			# eb name format used for comparison to calculate versionsuffx
			eb_name_format=name+"-"+version+"-"+toolchain_name+"-"+toolchain_version

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


		# master condition to determine if easyconfig parameter match argument for software and toolchain
		if tcname == "dummy" and tcversion == "dummy":
			if name == appname and version_versionsuffix == appversion:
				return True
		else:
			if name == appname and version_versionsuffix == appversion and toolchain_name == tcname and toolchain_version == tcversion:
				return True

	# mismatch in easyconfig entries for name,version+versionsuffix, and toolchain with specified entries
	if match == False:
		print "Can't find easyconfig file with argument:"
		print "software= ", software[0]
        	print "version:", software[1]
		print "toolchain name:",toolchain[0]
		print "toolchain version:", toolchain[1]
		sys.exit(1)

