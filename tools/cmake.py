############################################################################ 
# 
#  Copyright 2017 
# 
#   https://github.com/shahzebsiddiqui/buildtest 
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
from parser import *
from tools.file import *
def init_CMakeList(filename):
        """
        This is the content of BUILDTEST_ROOT/CMakeLists.txt
        """
        header = """ 
cmake_minimum_required(VERSION 2.8)
include(CTest)
ENABLE_TESTING()
add_subdirectory(""" + BUILDTEST_TESTDIR + ")"
        fd=open(filename,'w')
        fd.write(header)
        fd.close()


def update_CMakeLists(filename,tag, verbose):
        """
        used for writing CMakeLists.txt with tag <software>, <version>, & toolchain
        """
        fd=open(filename,'r')
        content=fd.read().strip().split("\n")
        cmd="add_subdirectory("+tag+")"
        if cmd not in content:
                fd.close()
                fd=open(filename,'a')
                fd.write(cmd+"\n")
                fd.close()
                if verbose >= 1:
                        print "writing:", cmd, "to file:",filename
        else:
                fd.close()

def add_test_to_CMakeLists(appname,appver,tcname,tcver,app_destdir,subdir,cmakelist,testname):
	""" update CMakeLists.txt with add_test command to allow ctest to run test """

	fd=open(cmakelist,'a')
	add_test_str=""

        # if YAML files are in subdirectory of config directory then update CMakeList
        # in app_destdir to add tag "add_subdirectory" for subdirectory so CMakeList
        # can find tests in subdirectory
	if subdir != "":
		# only update the app_destdir/CMakeLists.txt if subdirectory doesn't exist. This avoids
		# writing duplicate values when there are multiple tests in subdirectory
		parent_cmakelist = os.path.join(app_destdir,"CMakeLists.txt")
               	cmake_content="add_subdirectory("+subdir+") \n"
	 	ret = string_in_file(cmake_content,parent_cmakelist)
		if ret == False:
	               	fd1=open(parent_cmakelist,'a')
		        fd1.write(cmake_content)
        	       	fd1.close()

                # the string add_test in CMakeLists allows you to test script with ctest. The NAME tag is 
                # <name>-<version>-<toolchain-name>-<toolchain-version>-<subdir>-<testname>. This
                # naming scheme should allow buildtest to reuse same YAML configs for multiple version
                # built with any toolchains. Subdirectories come in handy when you need to organize tests 
		# effectively to avoid naming conflict
      		
		add_test_str="add_test(NAME " + appname + "-" + appver + "-" + tcname + "-" + tcver + "-"      + subdir + "-" + testname + "\t COMMAND sh " +  testname + "\t WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}) \n"
	else:
         	add_test_str="add_test(NAME " + appname + "-" + appver + "-" + tcname + "-" + tcver + "-"  + testname + "\t COMMAND sh " + testname + "\t WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}) \n"
	fd.write(add_test_str)
        fd.close()
	
	logcontent= "Updating File " + cmakelist + " with: " + add_test_str + "\n"
	return logcontent

