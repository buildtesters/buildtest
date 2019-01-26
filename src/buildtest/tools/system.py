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

import logging
import os
import platform
import re
import stat
import sys
import subprocess
from stat import S_IXUSR, S_IXGRP, S_IXOTH
from buildtest.tools.config import config_opts, logID

system = {}

def check_system_package_installed(pkg):
    """ check if system package is installed and return True/False"""

    cmd = ""
    os_type = get_os_name()
    if os_type == "RHEL":
        cmd = "rpm -q " + pkg

    ret = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    ret.communicate()

    if ret.returncode == 0:
        return True
    else:
        print ("Please install system package: %s  before creating YAML file",pkg)
        sys.exit(1)

def get_binaries_from_systempackage(pkg):
    """ get binaries from system package that typically install in standard linux path and only those that are executable """

    bindirs = [ "/usr/bin", "/bin", "/sbin", "/usr/sbin", "/usr/local/bin", "/usr/local/sbin" ]
    cmd = ""
    os_type = get_os_name()
    if os_type == "RHEL":
        cmd = "rpm -ql " + pkg

    ret = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ret.communicate()[0].decode("utf-8")

    temp = output.splitlines()
    output = temp

    binaries = {}

    for file in output:
        # if file doesn't exist but found during rpm -ql then skip file.
        if not os.path.isfile(file):
            continue

        # check only files that are executable
        statmode = os.stat(file)[stat.ST_MODE] & (stat.S_IXUSR|stat.S_IXGRP|stat.S_IXOTH)

        ret = subprocess.Popen("sha256sum " + file, shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output = ret.communicate()[0].decode("utf-8")

        sha256sum = output.split(" ")[0]

        # only add executable files found in array bindirs
        if statmode and os.path.dirname(file) in bindirs and not os.path.islink(file):
            # only add binaries with unique sha256 sum
            if sha256sum not in binaries.keys():
                binaries[sha256sum] = file

    if len(binaries) == 0:
        print ("There are no binaries found in package: ", pkg)
        return None

    return binaries

def systempackage_installed_list():
    """return a list of installed system packages in a machine"""
    cmd = ""
    os_type = get_os_name()

    if os_type == 'RHEL':
        cmd = """ rpm -qa --qf "%{NAME}\n" """

    ret = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE)
    output = ret.communicate()[0].decode("utf-8")
    pkglist = output.split("\n")

    # delete last element which is a ""
    pkglist = pkglist[:-1]
    return pkglist

def get_os_name():
    """ Return Operating System Name"""
    os_name = platform.linux_distribution()[0].strip().lower()

    os_name_map = {
        'red hat enterprise linux server': 'RHEL',
        'scientific linux sl': 'SL',
        'scientific linux': 'SL',
        'suse linux enterprise server': 'SLES',
    }

    if os_name:
        return os_name_map.get(os_name, os_name)
    else:
        return UNKNOWN

def command_path(cmd):
    """return full path of a linux command"""
    find_cmd = "which " + cmd
    ret = subprocess.Popen(find_cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ret.communicate()[0].decode("utf-8")
    return output

def get_env_snapshot():
    """ return output of Linux command env  """
    ret = subprocess.Popen("env",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ret.communicate()[0].decode("utf-8")
    return output

def get_system_info():
    """ get system info and write in log file """

    system["OS_NAME"] = platform.linux_distribution()[0]
    system["OS_VERSION"] = platform.linux_distribution()[1]
    system["SYSTEM"] = platform.system()
    system["KERNEL_RELEASE"] = platform.release()
    system["PROCESSOR_FAMILY"] = platform.processor()
    system["HOSTNAME"] = platform.node()
    system["PYTHON_VERSION"] = platform.python_version()
    system["PLATFORM"] = platform.platform()
    system["LIBC_VERSION"] = platform.libc_ver()[1]
    system["PYTHON_ABSPATH"] = command_path("python")
    system["ENV"] = get_env_snapshot()

    if system == 'Linux':
        logger.debug("Trying to determine total memory size on Linux via /proc/meminfo")
        meminfo = open('/proc/meminfo').read()
        mem_mo = re.match(r'^MemTotal:\s*(\d+)\s*kB', meminfo, re.M)
        if mem_mo:
            system["MEMORY_TOTAL"] = int(mem_mo.group(1)) / 1024
