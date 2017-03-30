from setup import *
from utilities import *
import os
import sys

# returns a complete list of modules found in the moduletree
def get_module_list(moduletree):
	find_cmd_module=os.popen("find " + moduletree + " -type f """).read()
        modulelist=find_cmd_module.rstrip().split('\n')
	return modulelist
# returns a set of software packages found in the module tree
def get_unique_software(moduletree):
	modulelist=get_module_list(moduletree)
	module_set=set()
	for module in modulelist:
                # extract the module name from filepath
		modulename=os.popen("dirname " + module + " | xargs basename ").read().rstrip()
		module_set.add(modulename)
	return sorted(module_set)
# returns a set of software-version collection found in module files. Duplicates are ignored for instance, same package version is built with two different toolchains
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
                
		moduleversion_set.add(modulename+" "+version)

        #print module_set
	return sorted(moduleversion_set)
# relationship between software name and version. The function will return a dictionary with key values as software name and values will be a set of version
def module_version_relation(moduletree):
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
	easyconfigfiles=os.popen("find " + easyconfigdir +  " -name *.eb -type f ").read().rstrip().split("\n")
        #print easyconfigfiles,type(easyconfigfiles)
	toolchain=set()
        for ebfile in easyconfigfiles:
                cmd="""grep "toolchain =" """ + ebfile + """ | cut -f4 -d " " | tr -d "'," """
                toolchain_name=os.popen(cmd).read().rstrip()
                cmd="""grep "toolchain =" """ + ebfile + """ | cut -f6 -d " " | tr -d "}'" """
                toolchain_version=os.popen(cmd).read().rstrip()
		toolchain.add(toolchain_name+" "+toolchain_version)
	return toolchain

# checks whether software exist, there must be a module file present with the same name specified as the argument. 
def software_exists(software):
	if len(software) != 2:
		print "Too many arguments, -s takes argument <software>,<version>"
		sys.exit(1)
	
	softwarecollection=get_unique_software_version(BUILDTEST_MODULEROOT)
	software_name=software[0]+" "+software[1]
	if software_name not in softwarecollection:
		print "Can't find software: ", software_name
		sys.exit(1)
	
	return True
# checks to see if toolchain passed on command line exist in toolchain list
def toolchain_exists(software,toolchain):
	toolchain_list=get_toolchain(BUILDTEST_EASYCONFIGDIR)

	# if toolchain is installed as hidden file then strip the "." prior to checking in list
	if isHiddenFile(toolchain[1]) == True:
		strip_version=stripHiddenFile(toolchain[1])
		toolchain_name=toolchain[0]+" "+strip_version
	else:
		toolchain_name=toolchain[0]+" "+toolchain[1]
	if len(toolchain) != 2:
		print "Too many arguments, -t takes argument <toolchain-name>,<toolchain-version>"
		sys.exit(1)
	# check if toolchain is in list
	if toolchain_name not in toolchain_list:
		print "Can't find toolchain: ", toolchain_name
		sys.exit(1)
	return True

# return True if name,version+versionsuffix,toolchain from command line is found from easyconfig, False otherwise
def check_software_version_in_easyconfig(moduletree,software,toolchain):
	software_dir=software[0]
	cmd="find " + moduletree + software_dir  + " -name *.eb -type f"         
	easyconfigfiles=os.popen(cmd). read().rstrip().split("\n")

	# boolean value to check if eb file found with parameters for software and toolchain
	match=False    

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
		print "ebname,eb_name_format",ebname,eb_name_format
		print "version/versionsuffix=",version,version_versionsuffix
		print "name/ver",software

		if toolchain[0] == "dummy" and toolchain[1] == "dummy":
			if name == software[0] and version_versionsuffix == software[1]:
				return True
		else:
			# master condition
			if name == software[0] and version_versionsuffix == software[1] and toolchain_name == toolchain[0] and toolchain_version == toolchain[1]:
				return True

	# mismatch in easyconfig entries for name,version+versionsuffix, and toolchain with specified entries
	if match == False:
		print "Can't find easyconfig file with argument:"
		print "software= ", software[0]
        	print "version:", software[1]
		print "toolchain name:",toolchain[0]
		print "toolchain version:", toolchain[1]
		sys.exit(1)


"""
	modulelist=get_module_list(moduletree)
	moduleversion_set=get_unique_software_version(moduletree)
	toolchain_set=set()
	# create relationship between software,version to toolchain.
	# Process all easyconfig file, store name, version, versionsuffix, toolchain name, toolchain version as a tuple entry in a list. Extract version suffix by doing a diff between eb file and "name-version-toolchain". Loop over list and compare name/version with moduleversion_set and extract toolchain name/version from list and store in moduleversion_toolchain_set
	easyconfigfiles=os.popen("find " + BUILDTEST_EASYCONFIGDIR +  " -name *.eb" " -type f ").read().rstrip().split("\n")
	#print easyconfigfiles,type(easyconfigfiles)
	name_version_toolchain_list=[]
	for ebfile in easyconfigfiles:
		# possibility there could be more than one entry for name in easyconfig, so limit to 1st entry which should be name of package
		name=os.popen(cmd).read().rstrip()

		# there can be more than one entry for version in easyconfig
		version=os.popen(cmd).read().rstrip()
                toolchain_name=os.popen(cmd).read().rstrip()
                toolchain_version=os.popen(cmd).read().rstrip()
		
		cmd="basename " + ebfile 
		ebfilename=os.popen(cmd).read().strip()
		# remove .eb extension
		ebfilename=ebfilename[:-3]
		
		#print  "file=", ebfilename
		# version suffix with dummy toolchain
		if toolchain_name == "dummy":
			position=ebfilename.index(version)+len(version)			
		else:
			position=ebfilename.index(toolchain_version)+len(toolchain_version)

		versionsuffix=ebfilename[position:]
		name_version_toolchain_list.append([name,version,versionsuffix,toolchain_name,toolchain_version])
		#print "name/version=",name,version, "toolchain=",toolchain_name,toolchain_version,"pos=",position,"versionsuffix=", versionsuffix
	#print name_version_toolchain_list
	for nameversion in moduleversion_set:
		print nameversion
	sys.exit(1)
	for item in name_version_toolchain_list:
		#print item
		for nameversion in moduleversion_set:
			nameversion.strip(',')
			name_version_versionsuffix=item[0]+item[1]+item[2]
			#print item,nameversion,name_version_versionsuffix
			#if nameversion == name_version_versionsuffix:
			#	print nameversion, name_version_versionsuffix, item
			
		# when toolchain version is '' change it to dummy
		if len(item[4]) == 0:
			item[4] = "dummy"
		toolchain_set.add(item[3]+"-"+item[4])
	#print_dictionary(moduleversion_toolchain_set)  
	modver_tc_set={}	
	#for setitem in toolchain_set:
	#	print setitem
	sys.exit(1)
"""

