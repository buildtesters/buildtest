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
Functions for system package
"""

import json
import os
import platform
import re
import stat
import sys
import subprocess

from buildtest.tools.modules import module_obj


class BuildTestCommand():
    ret = []
    out = ""
    err = ""
    def execute(self,cmd):
        """ execute a system command and return output and error"""
        self.ret = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (self.out,self.err) = self.ret.communicate()
        self.out = self.out.decode("utf-8")
        self.err = self.err.decode("utf-8")
        return (self.out,self.err)
    def which(self,cmd):
        """ run which against the command """
        which_cmd = "which " + cmd
        self.ret = subprocess.Popen(which_cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (self.out,self.err) = self.ret.communicate()
        self.out = self.out.decode("utf-8")
        self.err = self.err.decode("utf-8")
        return (self.out,self.err)
    def returnCode(self):
        return self.ret.returncode
    def get_output(self):
        return self.out
    def get_error(self):
        return self.err

class BuildTestSystem():
    system = {}

    def __init__(self):
        """ checking site configuration """

        self.system["OS_NAME"] = platform.linux_distribution()[0]
        self.system["OS_VERSION"] = platform.linux_distribution()[1]
        self.system["SYSTEM"] = platform.system()
        self.system["KERNEL_RELEASE"] = platform.release()
        self.system["PROCESSOR_FAMILY"] = platform.processor()
        self.system["HOSTNAME"] = platform.node()
        self.system["PYTHON_VERSION"] = platform.python_version()
        self.system["PLATFORM"] = platform.platform()
        self.system["LIBC_VERSION"] = platform.libc_ver()[1]
        self.system["SCHEDULER"] = self.check_scheduler()
        if self.system["SYSTEM"] == 'Linux':
            #logger.debug("Trying to determine total memory size on Linux via /proc/meminfo")
            meminfo = open('/proc/meminfo').read()
            mem_mo = re.match(r'^MemTotal:\s*(\d+)\s*kB', meminfo, re.M)
            if mem_mo:
                self.system["MEMORY_TOTAL"] = int(mem_mo.group(1)) / 1024

        cmd = BuildTestCommand()
        cmd.execute("env")
        self.system["ENV"] = cmd.get_output()

        cmd.which("python")
        self.system["PYTHON"]= cmd.get_output()

        if self.system["SCHEDULER"] == "LSF":
            self.get_lsf_configuration()
        if self.system["SCHEDULER"] == "SLURM":
            self.get_slurm_configuration()

        self.get_modules()

        module_coll_dict = {
            "collection": []
        }
        fname = os.path.join(os.getenv("BUILDTEST_ROOT"), "var","default.json")
        if not os.path.exists(fname):
            with open(fname, "w") as outfile:
                json.dump(module_coll_dict, outfile, indent=4)

    def get_system(self):
        return self.system        
    def get_lsf_configuration(self):
        """ return lsf queues and compute nodes part of the LSF cluster"""
        cmd = BuildTestCommand()
        query = """ bqueues | cut -d " " -f 1 """

        cmd.execute(query)
        out = cmd.get_output()

        queue_names = out.split("\n")
        # remove the first and last entry. First entry is just header and last entry is empty string
        del queue_names[0]
        del queue_names[-1]


        self.system["QUEUES"] = queue_names

        query = """ bhosts -w | cut -d " " -f 1 """
        cmd.execute(query)
        out = cmd.get_output()

        compute_nodes =  out.split("\n")
        del compute_nodes[0]
        del compute_nodes[-1]

        self.system["COMPUTENODES"] = compute_nodes

    def get_slurm_configuration(self):
        """ return slurm queues and compute nodes part of the SLURM cluster"""
        pass

    def check_scheduler(self):
        """ check for batch scheduler"""
        lsf_cmd = BuildTestCommand()
        lsf_cmd.execute("bhosts")
        lsf_ec_code = lsf_cmd.returnCode()

        slurm_cmd = BuildTestCommand()
        slurm_cmd.execute("sinfo")
        slurm_ec_code = slurm_cmd.returnCode()

        if lsf_ec_code == 0:
            return "LSF"
        if slurm_ec_code == 0:
            return "SLURM"

        return None

    def check_system_requirements(self):
        """ checking system requirements"""
        req_pass=True
        # If system is not Linux

        if self.system["SYSTEM"] != "Linux":
            req_pass=False

        # Check if LMOD_CMD is defined which is an environment variable set typically if LMOD is installed
        # There are many ways to check if Lmod is installed
        lmod_dir = os.getenv("LMOD_CMD")

        if lmod_dir == None:
            req_pass=False

        if self.system["OS_NAME"] != "Red Hat Enterprise Linux Server":
            req_pass=False

        if self.system["SCHEDULER"] == None:
            req_pass=False

        if not req_pass:
            msg = """
System Requirements not satisfied.

Requirements:
1. System must be Linux
2. Lmod must be installed
3. Operating System: RHEL
4. Scheduler must be LSF or SLURM
"""
            print(msg)
            sys.exit(1)
    def get_modules(self):
        module_dict = module_obj.get_module_spider_json()
        keys = module_dict.keys()
        json_dict = {}
        for key in keys:
            json_dict[key] = {}
            for mpath in module_dict[key].keys():

                fullname = module_dict[key][mpath]["full"]
                parent = module_dict[key][mpath]["parent"]

                json_dict[key][mpath] = {}
                json_dict[key][mpath]["fullName"] = fullname
                json_dict[key][mpath]["parent"] = []
                for entry in parent:
                    json_dict[key][mpath]["parent"].append(entry.split(":")[1:])

        module_json_file = os.path.join(os.getenv("BUILDTEST_ROOT"), "var",
                                        "modules.json")
        with open(module_json_file,"w") as outfile:
            json.dump(json_dict, outfile, indent=4)


def get_module_collection():
    """Return user Lmod module collection"""
    return subprocess.getoutput("module -t savelist").split("\n")


def get_binaries_from_systempackage(pkg):
    """ get binaries from system package that typically install in standard linux path and only those that are executable """

    bindirs = [ "/usr/bin", "/bin", "/sbin", "/usr/sbin", "/usr/local/bin", "/usr/local/sbin" ]
    cmd = BuildTestCommand()
    query = "rpm -ql " + pkg
    cmd.execute(query)
    output = cmd.get_output()

    temp = output.splitlines()
    output = temp

    binaries = []

    for file in output:
        # if file doesn't exist but found during rpm -ql then skip file.
        if not os.path.isfile(file):
            continue

        # check only files that are executable
        statmode = os.stat(file)[stat.ST_MODE] & (stat.S_IXUSR|stat.S_IXGRP|stat.S_IXOTH)

        # only add executable files found in array bindirs
        if statmode and os.path.dirname(file) in bindirs and not os.path.islink(file):
            binaries.append(file)

    if len(binaries) == 0:
        print ("There are no binaries found in package: ", pkg)
        return []

    return binaries

def systempackage_installed_list():
    """return a list of installed system packages in a machine"""

    cmd = BuildTestCommand()
    query = """ rpm -qa --qf "%{NAME}\n" """
    cmd.execute(query)
    pkglist = cmd.get_output()

    pkglist = pkglist.split("\n")

    # delete last element which is an empty string
    del pkglist[-1]
    return pkglist
