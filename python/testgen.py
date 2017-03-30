from setup import *
import os.path 
import os, sys
def generate_binary_test(software,toolchain):
	toplevel_cmakelist_file=BUILDTEST_ROOT + "CMakeLists.txt"
	testingdir_cmakelist_file=BUILDTEST_TESTDIR + "CMakeLists.txt"
	swname = software[0]
	commandfile=BUILDTEST_SOURCEDIR + swname + "/command.txt"  

	print commandfile

	# if CMakeLists.txt does not exist in top-level directory, create the header
	if os.path.isfile(toplevel_cmakelist_file) == False:
		init_CMakeList(toplevel_cmakelist_file)
	# if BUILDTEST_TESTDIR/CMakeLists.txt does not exist, then create it
	if os.path.isfile(testingdir_cmakelist_file) == False:
		fd=open(testingdir_cmakelist_file,'w')
		fd.close()
	# if command.txt does not exist then report error
	if os.path.isfile(commandfile) == False:
		print "Error cannot find file:", commandfile
		sys.exit(1)
	else:
	    process_binary_file(commandfile,software,toolchain)


	
# read binary file (command.txt) and create template shell script 
def process_binary_file(filename,software,toolchain):
	name,version=software
	toolchain_name,toolchain_version=toolchain
	print "values",name,version,toolchain_name,toolchain_version
	# if top level software directory is not present, create it
	test_name_dir=BUILDTEST_TESTDIR + name
	test_version_dir=test_name_dir + "/" + version
	test_toolchain_name_dir=test_version_dir + "/" + toolchain_name
	test_toolchain_version_dir=test_toolchain_name_dir + "/" + toolchain_version

	test_cmakelist = BUILDTEST_TESTDIR + "/CMakeLists.txt"
	test_name_cmakelist = test_name_dir + "/CMakeLists.txt"
	test_version_cmakelist = test_version_dir + "/CMakeLists.txt"
	test_toolchain_name_cmakelist = test_toolchain_name_dir + "/CMakeLists.txt"
	test_toolchain_version_cmakelist = test_toolchain_version_dir + "/CMakeLists.txt"

	# create directories if they don't exist
	# Directory Format: <software>/<version>/toolchain-name>/<toolchain-version>
	if not os.path.isdir(test_name_dir):
		print "creating directory:", test_name_dir
		os.mkdir(test_name_dir)
	if not os.path.isdir(test_version_dir):
		print "creating directory:", test_version_dir
		os.mkdir(test_version_dir)
	if not os.path.isdir(test_toolchain_name_dir):
		print "creating directory:", test_toolchain_name_dir
		os.mkdir(test_toolchain_name_dir)
	if not os.path.isdir(test_toolchain_version_dir):
		print "creating directory:", test_toolchain_version_dir
		os.mkdir(test_toolchain_version_dir)

	# create CMakeList.txt file in each directory of <software>/<version>/<toolchain-name>/<toolchain-version> if it doesn't exist
	if not os.path.isfile(test_name_cmakelist):
		fd=open(test_name_cmakelist,'w')
		fd.close()
	
	if not os.path.isfile(test_version_cmakelist):
		fd=open(test_version_cmakelist,'w')
		fd.close()

	if not os.path.isfile(test_toolchain_name_cmakelist):
		fd=open(test_toolchain_name_cmakelist,'w')
		fd.close()

	if not os.path.isfile(test_toolchain_version_cmakelist):
		fd=open(test_toolchain_version_cmakelist,'w')
		fd.close()
	
	check_CMakeLists(test_cmakelist,name)
	check_CMakeLists(test_name_cmakelist,version)
	check_CMakeLists(test_version_cmakelist,toolchain_name)
	check_CMakeLists(test_toolchain_name_cmakelist,toolchain_version)

		
	fd=open(filename,'r')
	content=fd.read()
	print content,type(content)
	#for line in content:

# used for writing CMakeLists.txt with tag <software>, <version>, & toolchain
def check_CMakeLists(filename,tag):
	cmd="cat " + filename + " | grep " + tag + " | wc -l"
	count=int(os.popen(cmd).read())
	# if add_subdirectory(<version>) not found in CMakeLists.txt then add it to file
	if count == 0:
		fd=open(filename,'w')
		fd.write("add_subdirectory(" + tag + ")")
		fd.close()
		
#def write_binary_test(filename):
def init_CMakeList(filename):
	header = """ 
cmake_minimum_required(VERSION 2.8)
include(CTest)
ENABLE_TESTING()
add_subdirectory(""" + BUILDTEST_TESTDIR + ")"
	print filename
	fd=open(filename,'w')
	fd.write(header)
	fd.close()
