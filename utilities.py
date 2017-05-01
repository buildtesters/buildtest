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


import os

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

