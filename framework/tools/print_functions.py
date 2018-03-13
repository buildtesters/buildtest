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

from framework.tools.utility import sset 

def print_software_version_relation(software_dict):

        text = """
 ID  |        Software            |      Versions
-----|----------------------------|----------------------------- """
	print text
	count = 0
	keylist = software_dict.keys()
	keylist.sort()
        for key in keylist:
		count = count + 1
		for value in sset(software_dict[key]):
	        	print (str(count) + "\t |").expandtabs(4) , "\t" + (key + "\t |" ).expandtabs(25) + "\t" +  value
			

def print_software(software_set):
	count = 1
	text =  """
ID  |     Software
----|-----------------------------  """

	print text
	for item in software_set:
		print (str(count) + "\t|").expandtabs(4), "\t" + item 
		count = count + 1


def print_toolchain(toolchain_set):
	count = 1
	text =  """
ID  |     Toolchains
----|-----------------------------  """

	print text
	for item in toolchain_set:
		print (str(count) + "\t|").expandtabs(4), "\t" + item 
		count = count + 1
