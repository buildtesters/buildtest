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
import yaml
import os
import subprocess
import sys
import json

from buildtest.tools.file import create_dir

def func_collection_subcmd(args):

    if args.add:
        add_collection()
    if args.list:
        list_collection()

def add_collection():
    """Save modules in a collection"""
    cmd = "module -t list"
    out = subprocess.getoutput(cmd)
    # output of module -t list when no modules are loaded is "No modules
    #  loaded"
    module_coll_dict = {
        "collection": []
    }
    if out != "No modules loaded":
        module_list = out.split()

        create_dir(os.path.join(os.getenv("BUILDTEST_ROOT"),"var"))
        fname = os.path.join(os.getenv("BUILDTEST_ROOT"),"var","default.json")

        # if file doesn't exist just add module directly to file
        if not os.path.exists(fname):
            fd = open(fname,"w")
            print (module_list,type(module_list))
            module_coll_dict["collection"].append(module_list)
            json.dump(module_coll_dict,fd,indent=4)
            fd.close()
        else:
            fd = open(fname,'r')
            content = json.load(fd)
            fd = open(fname,'w')
            content["collection"].append(module_list)
            json.dump(content,fd,indent=4)

        print(f"Updating collection file: {fname}")
def list_collection():
    """List module collections."""
    fname = os.path.join(os.getenv("BUILDTEST_ROOT"),"var","default.json")

    fd = open(fname,'r')
    dict = json.load(fd)
    count = 0
    for x in dict["collection"]:
        count+=1
        print (f"{count}: {x}")

