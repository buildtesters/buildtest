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
from buildtest.tools.config import BUILDTEST_MODULE_COLLECTION_FILE,\
    BUILDTEST_MODULE_FILE, BUILDTEST_BUILD_LOGFILE, BUILDTEST_SYSTEM
from buildtest.tools.file import create_dir
from buildtest.tools.modules import module_obj

class BuildTestCommand():
    """Class method to invoke shell commands and retrieve output and error. This class
    makes use of **subprocess.Popen()** to run the shell command. This class has no
    **__init__()** method
    """

    ret = []
    out = ""
    err = ""
    def execute(self,cmd):
        """Execute a system command and return output and error

        :param cmd: shell command to execute
        :type cmd: str, required
        :return: Output and Error from shell command
        :rtype: two str objects
        """

        self.ret = subprocess.Popen(cmd,
                                    shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        (self.out, self.err) = self.ret.communicate()
        self.out = self.out.decode("utf-8")
        self.err = self.err.decode("utf-8")
        return (self.out,self.err)
    def which(self,cmd):
        """Run a ``which`` against the command.

        :param cmd: shell command to execute
        :type cmd: str, required
        :return: Output and Error from shell command
        :rtype: two str objects
        """

        which_cmd = "which " + cmd
        self.ret = subprocess.Popen(which_cmd,
                                    shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        (self.out, self.err) = self.ret.communicate()
        self.out = self.out.decode("utf-8")
        self.err = self.err.decode("utf-8")
        return (self.out, self.err)

    def returnCode(self):
        """Returns the return code from shell command

        :rtype: int
        """

        return self.ret.returncode
    def get_output(self):
        """Returns the output from shell command

        :rtype: str
        """

        return self.out

    def get_error(self):
        """Returns the error from shell command

        :rtype: str
        """

        return self.err

class BuildTestSystem():
    """BuildTestSystem is a class that detects system configuration and outputs the result
    in .run file which are generated upon test execution."""

    # class variable used for storing system configuration
    system = {}

    def __init__(self):
        """Constructor method for BuildTestSystem(). Defines all system configuration using
        class variable **system** which is a dictionary """

        distro_fname = platform.linux_distribution()[0]
        self.system["OS_NAME"]= distro_short(distro_fname)

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

        cmd.which("python")
        self.system["PYTHON"]= cmd.get_output()

        if self.system["SCHEDULER"] == "LSF":
            self.get_lsf_configuration()
        if self.system["SCHEDULER"] == "SLURM":
            from buildtest.tools.slurm import get_slurm_configuration
            self.system["QUEUES"],self.system["COMPUTENODES"] = get_slurm_configuration()

        cmd.execute("""lscpu | grep "Vendor" """)
        vendor_name = cmd.get_output()

        cmd.execute("""lscpu | grep "Model:" | cut -b 10-""")
        model_hex = hex(int(cmd.get_output()))

        if "GenuineIntel" in vendor_name:
            self.system["VENDOR"] = "Intel"
            arch = intel_cpuid_lookup(model_hex)
        self.system["ARCH"] = arch

        self.get_modules()

        module_coll_dict = {
            "collection": []
        }

        if not os.path.exists(BUILDTEST_SYSTEM):
            with open(BUILDTEST_SYSTEM,"w") as outfile:
                json.dump(self.system,outfile,indent=4)

        if not os.path.exists(BUILDTEST_MODULE_COLLECTION_FILE):
            with open(BUILDTEST_MODULE_COLLECTION_FILE, "w") as outfile:
                json.dump(module_coll_dict, outfile, indent=4)

        if not os.path.exists(BUILDTEST_BUILD_LOGFILE):
            build_dict = {"build":{}}
            with open(BUILDTEST_BUILD_LOGFILE, "w") as outfile:
                json.dump(build_dict,outfile,indent=4)

    def get_system(self):
        """Return class variable system that contains detail for system configuration

        :return: return ``self.system``
        :rtype: dict
        """

        return self.system        
    def get_lsf_configuration(self):
        """Return LSF queues and compute nodes part of the LSF cluster. It makes use
        of ``bhosts`` and ``bqueues`` command to retrieve queue and compute nodes.
        """

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

        compute_nodes = out.split("\n")
        del compute_nodes[0]
        del compute_nodes[-1]

        self.system["COMPUTENODES"] = compute_nodes


    def check_scheduler(self):
        """Check for batch scheduler. Currently checks for LSF or SLURM by running
        ``bhosts`` and ``sinfo`` command. It must be present in $PATH when running buildtest.

        :return: return string **LSF** or **SLURM**. If neither found returns **None**
        :rtype: str or None
        """

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
        """Checking system requirements."""
        req_pass=True
        # If system is not Linux

        if self.system["SYSTEM"] != "Linux":
            req_pass=False

        # Check if LMOD_CMD is defined which is an environment variable set typically if LMOD is installed
        # There are many ways to check if Lmod is installed
        lmod_dir = os.getenv("LMOD_CMD")

        if lmod_dir == None:
            req_pass=False
        """
        if self.system["SCHEDULER"] == None:
            req_pass=False
        """
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
        """"""
        module_dict = module_obj.get_module_spider_json()
        module_version = module_obj.get_version()
        module_major_version = module_version[0]
        keys = module_dict.keys()
        json_dict = {}
        for key in keys:
            json_dict[key] = {}
            for mpath in module_dict[key].keys():
                if module_major_version == 6:
                    fullname = module_dict[key][mpath]["full"]
                    parent = module_dict[key][mpath]["parent"]
                else:
                    fullname = module_dict[key][mpath]["fullName"]
                    if "parentAA" not in module_dict[key][mpath]:
                        parent = []
                    else:
                        parent = module_dict[key][mpath]["parentAA"]


                json_dict[key][mpath] = {}
                json_dict[key][mpath]["fullName"] = fullname
                json_dict[key][mpath]["parent"] = []
                if module_major_version == 6:
                    for entry in parent:
                        json_dict[key][mpath]["parent"].append(entry.split(":")[1:])
                else:
                    json_dict[key][mpath]["parent"] = parent

        create_dir(os.path.dirname(BUILDTEST_MODULE_FILE))
        with open(BUILDTEST_MODULE_FILE,"w") as outfile:
            json.dump(json_dict, outfile, indent=4)


def get_module_collection():
    """Return user Lmod module collection. Lmod collection can be retrieved
    using command: ``module -t savelist``

    :return: list of Lmod module collection
    :rtype: list
    """
    return subprocess.getoutput("module -t savelist").split("\n")

def get_binaries_from_systempackage(pkg):
    """ get binaries from system package that typically install in standard linux path and only those that are executable """

    bindirs = [ "/usr/bin", "/bin", "/sbin", "/usr/sbin", "/usr/local/bin",
                "/usr/local/sbin" ]
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
        statmode = os.stat(file)[stat.ST_MODE] & \
                   (stat.S_IXUSR|stat.S_IXGRP|stat.S_IXOTH)

        # only add executable files found in array bindirs
        if statmode and os.path.dirname(file) in bindirs:
            # skip symlinks when adding binaries
            if not os.path.islink(file):
                binaries.append(file)

    if len(binaries) == 0:
        print ("There are no binaries found in package: ", pkg)
        return []

    return binaries

def systempackage_installed_list():
    """Return a list of installed system packages in a machine"""

    cmd = BuildTestCommand()
    query = """ rpm -qa --qf "%{NAME}\n" """
    cmd.execute(query)
    pkglist = cmd.get_output()

    pkglist = pkglist.split("\n")

    # delete last element which is an empty string
    del pkglist[-1]
    return pkglist

def distro_short(distro_fname):
    """Map Long Linux Distribution Name to short name."""

    if "Red Hat Enterprise Linux Server" == distro_fname:
        return "rhel"
    elif "CentOS" == distro_fname:
        return "centos"
    elif "SUSE Linux Enterprise Server" == distro_fname:
        return "suse"

def intel_cpuid_lookup(model):
    """Lookup table to map Module Number to Architecture."""

    # Intel based : https://software.intel.com/en-us/articles/intel-architecture-and-processor-identification-with-cpuid-model-and-family-numbers
    model_numbers = {
        "0x55":     "SkyLake",
        "0x4f":     "Broadwell",
        "0x57":     "KnightsLanding",
        "0x3f":     "Haswell",
        "0x46":     "Haswell",
        "0x3e":     "IvyBridge",
        "0x3a":     "IvyBridge",
        "0x2a":     "SandyBridge",
        "0x2d":     "SandyBridge",
        "0x25":     "Westmere",
        "0x2c":     "Westmere",
        "0x2f":     "Westmere",
        "0x1e":     "Nehalem",
        "0x1a":     "Nehalem",
        "0x2e":     "Nehalem",
        "0x17":     "Penryn",
        "0x1D":     "Penryn",
        "0x0f":     "Merom"
    }
    if model in model_numbers:
        return model_numbers[model]
    else:
        print (f"Unable to find model {model}")



