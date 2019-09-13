############################################################################
#
#  Copyright 2017-2019
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

This file implements methods on module collection that is invoked by "buildtest module collection"
"""
import os
import subprocess
import sys
import json

from buildtest.tools.config import BUILDTEST_MODULE_COLLECTION_FILE
from buildtest.tools.file import create_dir, create_file

def func_collection_subcmd(args):
    """Entry point for ``buildtest module collection``.

    :param args: command line arguments to buildtest
    :type args: dict, required
    """

    if args.add:
        add_collection()
    if args.list:
        list_collection()
    if args.update is not None:
        update_collection(args.update)
    if args.remove is not None:
        remove_collection(args.remove)

def add_collection():
    """This method save modules as a module collection in a json file. It updates
    the json file and prints content to STDOUT

    This method implements ``buildtest module collection -a`` command.
    """

    cmd = "module -t list"
    out = subprocess.getoutput(cmd)
    # output of module -t list when no modules are loaded is "No modules
    #  loaded"
    module_coll_dict = {
        "collection": []
    }
    # Update JSON file with a new module collection only if modules are loaded
    if out != "No modules loaded":
        module_list = out.split()

        create_dir(os.path.join(os.getenv("BUILDTEST_ROOT"),"var"))

        fd = open(BUILDTEST_MODULE_COLLECTION_FILE,'r')
        content = json.load(fd)
        fd = open(BUILDTEST_MODULE_COLLECTION_FILE,'w')
        content["collection"].append(module_list)
        json.dump(content, sys.stdout, indent=4)
        json.dump(content,fd,indent=4)
        print ("\n")
        print(f"Updating collection file: {BUILDTEST_MODULE_COLLECTION_FILE}")

def remove_collection(index):
    """This method removes a module collection from json file. It updates
    the json file and prints content to STDOUT

    This method implements ``buildtest module collection -r <ID>`` command.

    :param index: module index number in collection file to remove
    :type index: int, required
    """

    fd = open(BUILDTEST_MODULE_COLLECTION_FILE,"r")
    content = json.load(fd)
    fd.close()

    fd = open(BUILDTEST_MODULE_COLLECTION_FILE, "w")
    print (f"Removing Collection Index: {index}")
    print ("Modules to be removed:", content["collection"][index])

    del content["collection"][index]
    print(f"Updating collection file: {BUILDTEST_MODULE_COLLECTION_FILE}")
    print ("\n")
    json.dump(content,fd,indent=4)
    json.dump(content, sys.stdout, indent=4)
    fd.close()

def update_collection(index):
    """This method update a module collection with active modules in your environment.
    It updates the json file at index number specified and prints content to STDOUT

    This method implements ``buildtest module collection -u <ID>`` command.

    :param index: module collection index number to update with active modules
    :type index: int, required
    """
    """Update a module collection with active modules """

    fd = open(BUILDTEST_MODULE_COLLECTION_FILE,"r")
    content = json.load(fd)
    fd.close()

    cmd = "module -t list"
    out = subprocess.getoutput(cmd)
    if out == "No modules loaded":
        modules = []
    else:
        modules = out.split()
    fd = open(BUILDTEST_MODULE_COLLECTION_FILE, "w")
    print (f"Updating Collection Index: {index}")
    print ("Old Modules: ", content["collection"][index])
    content["collection"][index] = modules
    print ("New Modules: ", content["collection"][index])


    print(f"Updating collection file: {BUILDTEST_MODULE_COLLECTION_FILE}")
    print ("\n")
    json.dump(content,fd,indent=4)
    json.dump(content, sys.stdout, indent=4)
    fd.close()

def list_collection():
    """This method list all module collections from json file. If no module
    collection found, the method will return

    This method implements ``buildtest module collection --list`` command.
    """

    fd = open(BUILDTEST_MODULE_COLLECTION_FILE,'r')
    dict = json.load(fd)
    count = 0
    if len(dict["collection"]) == 0:
        print ("No module collection found.")
        return

    for x in dict["collection"]:
        print (f"{count}: {x}")
        count += 1

def get_collection_length():
    """Read collection file collection.json and return length of collection

    :rtype: int
    """
    with open(BUILDTEST_MODULE_COLLECTION_FILE,"r") as infile:
        json_module = json.load(infile)

    return (len(json_module["collection"]))

def get_buildtest_module_collection(id):
    """Retrieve collection id from collection.json
    :return: return module collection index
    :rtype: int
    """
    with open(BUILDTEST_MODULE_COLLECTION_FILE, "r") as infile:
        json_module = json.load(infile)
    return json_module["collection"][id]