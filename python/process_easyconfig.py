from setup import *
import os
import sys

class sset(set):
    def __str__(self):
        return ', '.join([str(i) for i in self])


def get_module_list(moduletree):
	find_cmd_module=os.popen("find " + moduletree + " -type f").read()
        modulelist=find_cmd_module.rstrip().split('\n')
	return modulelist
def get_unique_software(moduletree):
	modulelist=get_module_list(moduletree)
	module_set=set()
	for module in modulelist:
                # extract the module name from filepath
		modulename=os.popen("dirname " + module + " | xargs basename ").read().rstrip()
		module_set.add(modulename)
	return module_set
def get_unique_software_version(moduletree):
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
                
		moduleversion_set.add(modulename+","+version)

        #print module_set
	return moduleversion_set
# relationship between software name and version. The function will return a dictionary with key values as software name and values will be a set of version
def module_version_relation(moduletree):
	modulelist=get_module_list(moduletree)
	module_set=get_unique_software(moduletree)
	# dictionary used for keeping a relationship between software name and its corresponding versions found as modulefiles
	module_dict = {}

	# for every software in set, search easyconfig files to find version tag to get software to version relationship
	for item in  module_set:
		easyconfigfiles=os.popen("find " + BUILDTEST_EASYCONFIGDIR +  item + " -name " + item + "*.eb" " -type f"). read().rstrip()
		listofebfiles=easyconfigfiles.split("\n")
		version_set=set()
		# for software package X, get all version and store them in a set to avoid duplicate addition, only care for unique versions on the system
		for ebfile in listofebfiles:
			# extract version tag from easyconfig, there is a case where altversion = gets picked up so only get 1st entry which should be version
			cmd="""grep "version =" """ + ebfile + """ | cut -f2 -d = | head -n 1"""
			version=os.popen(cmd).read().rstrip()
			# remove the leading and trailing ' character
			version_set.add(version[2:-1])
			
		# store version set in dictionary that is indexed by software
		module_dict[item]=version_set
	return module_dict
# creates a relationship between software-version to a toolchain to show. This will show how a module file relates to a particular toolchain
def isHiddenFile(file):
	if file[0] == ".":
		return True
	else:
		return False
def stripHiddenFile(file):
	file=file[1:]
	return file	
def moduleversion_toolchain_relation(moduletree):
	modulelist=get_module_list(moduletree)
	moduleversion_set=get_unique_software_version(moduletree)
	for item in moduleversion_set:
		nameversion_tuple=item.split(",")
		name=nameversion_tuple[0]
		version=nameversion_tuple[1]
		modifiedversion=version
		if isHiddenFile(version) == True:
			modifiedversion=stripHiddenFile(version)
		#print name, version
                easyconfigfiles=os.popen("find " + BUILDTEST_EASYCONFIGDIR +  name + " -name " + name +  "*.eb" " -type f | head -n 1"). read().split("\n")
		print easyconfigfiles
		# find the correct eb file that matches version + versionsuffix in easyconfig with version variable
		for ebfile in easyconfigfiles:
			print ebfile
                       	cmd="""grep "toolchain =" """ + ebfile + """ | cut -f4 -d " " | tr -d "'" """
			print cmd
                        toolchain_name=os.popen(cmd).read().rstrip()
                        cmd="""grep "toolchain =" """ + ebfile + """ | cut -f6 -d " " | tr -d "}'" """
			toolchain_version=os.popen(cmd).read().rstrip()
			print ebfile,toolchain_name, toolchain_version
			sys.exit(1)
			
			
		#print easyconfigfiles
	sys.exit(1)

        listofebfiles=easyconfigfiles.split("\n")
        version_set=set()
        # for software package X, get all version and store them in a set to avoid duplicate addition, only care for unique versions on the system
        for ebfile in listofebfiles:
                        # extract version tag from easyconfig, there is a case where altversion = gets picked up so only get 1st entry which should be version
        	cmd="""grep "version =" """ + ebfile + """ | cut -f2 -d = | head -n 1"""
                version=os.popen(cmd).read().rstrip()
                        #cmd="""grep "toolchain =" """ + ebfile + """ | cut -f3 -d " " | tr -d "{':" """
                        #toolchain_name=os.popen(cmd).read().rstrip()
                        #cmd="""grep "toolchain =" """ + ebfile + """ | cut -f6 -d " " | tr -d "}'" """
                        #toolchain_version=os.popen(cmd).read().rstrip()
                        # remove the leading and trailing ' character
                version_set.add(version[2:-1])

def print_module_version(moduleversion_dict):
	for key in moduleversion_dict:
		print key, sset(moduleversion_dict[key])

