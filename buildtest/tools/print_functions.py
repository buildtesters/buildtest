############################################################################
#
#  Copyright 2017-2018
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

print functions related to buildtest

:author: Shahzeb Siddiqui (Pfizer)
"""
import csv
import os
from buildtest.tools.utility import sset

def print_software_version_relation_csv(software_dict):
    """ print output of -svr in json"""
    filename = "software_list.csv"
    with open(filename,'w',newline='') as csvfile:
        fieldnames = ['software','modulefile' ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        keylist = software_dict.keys()
        keylist = sorted(keylist)
        for key in keylist:
            writer.writerow({"software": software_dict[key], "modulefile": key})
        print (f"Writing content to CSV file: {os.path.abspath(filename)}")

def print_software_version_relation(software_dict):
    """print output of -svr"""
    text = """
 ID  |        Software            |      ModuleFile Path
-----|----------------------------|----------------------------- """
    print (text)
    id = 0
    keylist = software_dict.keys()
    keylist = sorted(keylist)

    modulecnt = 0

    for key in keylist:
        id = id + 1
        #for value in sset(software_dict[key]):
        print ((str(id) + "\t |").expandtabs(4) , "\t" + (software_dict[key] + "\t |" ).expandtabs(25) + "\t" +  key)
        modulecnt += 1

    print ("Total Software Modules Found: ", modulecnt)


def print_software(software_set):
    """ print output of -ls"""
    count = 0
    text =  """
ID  |     Software
----|-----------------------------  """

    print (text)
    for item in software_set:
        count = count + 1
        print ((str(count) + "\t|").expandtabs(4), item)



    print ("Total Software Packages: ", count)

def print_toolchain(toolchain_set):
	count = 1
	text =  """
ID  |     Toolchains
----|-----------------------------  """

	print (text)
	for item in toolchain_set:
		print ((str(count) + "\t|").expandtabs(4), item)
		count = count + 1
