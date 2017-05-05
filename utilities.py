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
import os
from datetime import datetime

def isHiddenFile(inputfile):
	"""
	creates a relationship between software-version to a toolchain. This will show 
	how a module file relates to a particular toolchain
	"""
	if os.path.isdir(inputfile) == True:
		return False
	
        cmd = "basename " + inputfile
	filename=os.popen(cmd).read().strip()
	if filename[0] == ".":
                return True
        else:
                return False

def create_dir(dirname,verbose):
        """
        Create directory if it doesn't exist
        """
        if not os.path.isdir(dirname):
                os.makedirs(dirname)
                if verbose >= 1:
                        print "Creating Directory: ",dirname

def create_file(filename,verbose):
        """
        Create an empty file if it doesn't exist
        """
        if not os.path.isfile(filename):
                fd=open(filename,'w')
                fd.close()
                if verbose >= 1:
                        print "Creating Empty File:", filename

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

def load_modules(software,toolchain):
        """
        return a string that loads the software and toolchain module. 
        """
        # for dummy toolchain you can load software directly. Ensure a clean environment by running module purge
        if toolchain[0] == "dummy":
                header="""
#!/bin/sh
module purge
module load """ + software[0] + "/" + software[1] + """
"""
        else:
                header="""
#!/bin/sh
module purge
module load """ + toolchain[0] + "/" + toolchain[1] + """
module load """ + software[0] + "/" + software[1] + """
"""

        return header

def update_logfile(logdir,logcontent,verbose):
	create_dir(logdir,verbose)	
	logfilename = datetime.now().strftime("buildtest_%H_%M_%d_%m_%Y.log")
        logfilepath = os.path.join(logdir,logfilename)

	print "Writing Log File: " + logfilepath

	fd = open(logfilepath,'w')
	fd.write(logcontent)
	fd.close()

def stripHiddenFile(file): 
	"""
	removes the leading "." character from file
	"""
        file=file[1:]
        return file  

def print_dictionary(dictionary):
	"""
	prints the content of dictionary
	"""
        for key in dictionary:
                print key, sset(dictionary[key])

def print_set(setcollection):
	"""
	prints the content of set 
	"""
	for item in setcollection:
		print item
class sset(set):
    def __str__(self):
        return ', '.join([str(i) for i in self])

