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

from buildtest.tools.file import create_dir, create_file

def func_collection_subcmd(args):
    """Entry point for buildtest module collection"""
    print (args)
    if args.add:
        add_collection()
    if args.list:
        list_collection()
    if args.remove is not None:
        remove_collection(args.remove)

def add_collection():
    """Save modules as a module collection in a json file """
    fname = os.path.join(os.getenv("BUILDTEST_ROOT"), "var", "default.json")


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

        fd = open(fname,'r')
        content = json.load(fd)
        fd = open(fname,'w')
        content["collection"].append(module_list)
        json.dump(content, sys.stdout, indent=4)
        json.dump(content,fd,indent=4)
        print ("\n")
        print(f"Updating collection file: {fname}")

def remove_collection(index):
    """Remove a module collection"""
    fname = os.path.join(os.getenv("BUILDTEST_ROOT"), "var", "default.json")
    fd = open(fname,"r")
    content = json.load(fd)
    fd.close()

    fd = open(fname, "w")
    print (f"Removing Collection Index: {index}")
    print (content["collection"][index])

    del content["collection"][index]
    print(f"Updating collection file: {fname}")
    print ("\n")
    json.dump(content,fd,indent=4)
    json.dump(content, sys.stdout, indent=4)
    fd.close()

def list_collection():
    """List module collections."""
    fname = os.path.join(os.getenv("BUILDTEST_ROOT"),"var","default.json")

    fd = open(fname,'r')
    dict = json.load(fd)
    count = 0
    for x in dict["collection"]:
        print (f"{count}: {x}")
        count += 1

def get_collection_length():
    """Read collection file default.json and return length of collection"""
    file = os.path.join(os.getenv("BUILDTEST_ROOT"),"var","default.json")
    with open(file,"r") as infile:
        json_module = json.load(infile)

    return (len(json_module["collection"]))

def get_buildtest_module_collection(id):
    """Retrieve collection id from default.json"""
    file = os.path.join(os.getenv("BUILDTEST_ROOT"), "var", "default.json")
    with open(file, "r") as infile:
        json_module = json.load(infile)
    return json_module["collection"][id]