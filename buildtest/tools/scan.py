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
This python module will implement the --scantest feature of buildtest

:author: Shahzeb Siddiqui (Pfizer)
"""

import os
import subprocess
import sys
from buildtest.tools.config import config_opts
from buildtest.tools.software import get_unique_software

def scantest():

    applist = get_unique_software()
    BUILDTEST_CONFIGS_REPO = config_opts['BUILDTEST_CONFIGS_REPO']
    eblist_sourcedir =  os.listdir(config_opts['BUILDTEST_CONFIGS_REPO_SOFTWARE'])

    ebapps_common=  set(applist) & set(eblist_sourcedir)

    print ("\n")
    print ("Software Packages that can be tested with buildtest")
    print ("---------------------------------------------------")

    software_test_list = []
    for x in ebapps_common:
        software_config_dir = os.path.join(config_opts['BUILDTEST_CONFIGS_REPO_SOFTWARE'],x)
        yaml_found=False
        for root, subdir, files in os.walk(software_config_dir):
            for file in files:
                if os.path.splitext(file)[1] == ".yaml":
                    yaml_found=True
        if yaml_found:
                software_test_list.append(x)

    software_test_list.sort()
    for x in software_test_list:
        print (x)



    syspkg_sourcedir = os.listdir(config_opts['BUILDTEST_CONFIGS_REPO_SYSTEM'])

    system_test_list = []

    print ("\n")
    print ("System Packages that can be tested with buildtest")
    print ("---------------------------------------------------")

    for pkg in syspkg_sourcedir:
        cmd = "rpm -q " + pkg
        ret = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        (output,errormsg) = ret.communicate()

        output = output.rstrip()

        if ret.returncode == 0:
            system_test_list.append(pkg)

    system_test_list.sort()
    for x in system_test_list:
        print (x)
    sys.exit(0)
