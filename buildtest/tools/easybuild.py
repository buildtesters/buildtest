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
easybuild specific modules related to toolchain and easyconfigs

:author: Shahzeb Siddiqui (Pfizer)
"""
import os
import re
import sys
import logging
import subprocess

from buildtest.tools.config import logID, config_opts
from buildtest.tools.file import stripHiddenFile, isHiddenFile, string_in_file
from buildtest.tools.utility import get_appname, get_appversion, get_toolchain_name, get_toolchain_version


# module trees in BUILDTEST_MODULE_ROOT as a list
def get_module_root():
    modroot = []
    for tree in config_opts['BUILDTEST_MODULE_ROOT']:
        if os.path.exists(tree):
            modroot.append(tree)
        else:
            print ("Unable to find directory: %s specified in BUILDTEST_MODULE_ROOT",tree)
            sys.exit(1)
    return modroot

def get_toolchains():
        """
        return the set of toolchains found in the easyconfig directory
        """
        toolchain = [
        "ClangGCC",
        "CrayCCE",
        "CrayGNU",
        "CrayIntel",
        "CrayPGI",
        "GCC",
        "GCCcore",
        "GNU",
        "PGI",
        "cgmpich",
        "cgmpolf",
        "cgmvapich2",
        "cgmvolf",
        "cgompi",
        "cgoolf",
        "dummy",
        "foss",
        "gcccuda",
        "gimkl",
        "gimpi",
        "gmacml",
        "gmpich",
        "gmpich2",
        "gmpolf",
        "gmvapich2",
        "gmvolf",
        "goalf",
        "gompi",
        "gompic",
        "goolf",
        "goolfc",
        "gpsmpi",
        "gpsolf",
        "gqacml",
        "iccifort",
        "iccifortcuda",
        "ictce",
        "iimkl",
        "iimpi",
        "iimpic",
        "iiqmpi",
        "impich",
        "impmkl",
        "intel",
        "intel-para",
        "intelcuda",
        "iomkl",
        "iompi",
        "ipsmpi",
        "iqacml",
        "ismkl",
        "pomkl",
        "pompi",
        "xlcxlf",
        "xlmpich",
        "xlmpich2",
        "xlmvapich2",
        "xlompi",
        ]

        logger = logging.getLogger(logID)
        logger.info("List of EB Toolchains")
        logger.info("--------------------------------------")
        logger.info("EB Toolchains = %s", toolchain)

        return toolchain

def find_easyconfigs_from_modulelist(modulelist):
    """return a list of easyconfigs from a list of module files"""
    # list to store easyconfigs
    ec_list = []
    # list to store if no easyconfigs found sometimes, found eb didn't generate easybuild directory where logs, easyconfig are placed.
    no_ec_list = []
    # look for variable root in modulefile
    search_str = "local root ="
    for module in  modulelist:
        # if variable root found in module file then read file and find value assigned to root to get root of software
        if string_in_file(search_str,module):
            content = open(module).readlines()
            for line in content:
                if line.startswith(search_str):
                    root_path = line.split()[-1]
                    root_path = root_path.replace('"','')
                    # trying to find directory easybuild inside the root of the installation directory of an application
                    easybuild_path = os.path.join(root_path,"easybuild")
                    # if directory exist then run the find command
                    if os.path.exists(easybuild_path):
                        cmd = "find " + easybuild_path + " -type f -name *.eb "
                        ret = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
                        easyconfig = ret.communicate()[0].rstrip().decode("utf-8")

                        #easyconfig = easyconfig.strip("\n")

                        # only add easyconfigs to list using find command. This also avoids adding empty entries when no file was found
                        if os.path.exists(easyconfig):
                            ec_list.append(easyconfig)
                        else:
                            no_ec_list.append("Could not find easyconfig in " + easybuild_path)
                    else:
                        print ("Unable to find directory: %s", easybuild_path)
                        no_ec_list.append("Could not find directory: " + easybuild_path)
                    break
                else:
                    continue
        else:
            no_ec_list.append("Reading File: " + module + " doesn't look like an easybuild generated module. Unable to find variable root")
    #print (ec_list,type(ec_list))

    return ec_list,no_ec_list

def find_easyconfigs():
    """ returns easyconfigs files from a module tree. """
    from buildtest.tools.modules import get_module_list

    ec_list = []
    no_ec_list = []
    modulelist = get_module_list()

    ec_list,no_ec_list = find_easyconfigs_from_modulelist(modulelist)

    # if one or more easyconfigs found then display the path to easyconfigs
    if len(ec_list) > 0:
        print ("List of easyconfigs found in MODULETREES: ", config_opts['BUILDTEST_MODULE_ROOT'])
        print
        print ("ID   |    easyconfig path")
        print ("-----|--------------------------------------------------------------------")
        count = 1
        for ec in ec_list:
            print ((str(count) + "\t |").expandtabs(4),ec)
            count = count + 1
    else:
        print ("No easyconfigs found!")

    if len(no_ec_list) > 0:
        print
        print ("Unable to find easyconfigs for the following, please investigate this issue! \n")

        for no_ec in  no_ec_list:
            print (no_ec)

    print ("Total easyconfigs found: ", len(ec_list))
    print ("Total module files searched: ", len(modulelist))


def is_easybuild_app():
    """ returns True if an easyconfig file found in installation directory """
    app_name = get_appname()
    app_ver = get_appversion()

    modulefiles = []
    modtrees = get_module_root()
    for tree in modtrees:
        for root, dirs, files in os.walk(tree):
            for file in files:
                # skipping files that are symbolic links
                if os.path.islink(os.path.join(root,file)):
                    continue

                # only add module file to list specified by -s <app>/<version>. The file name will be the version and directory will be the application name
                if os.path.splitext(file)[0] == app_ver and os.path.basename(root) == app_name:
                    modulefiles.append(os.path.join(root,file))

    ec_list, no_ec_list = find_easyconfigs_from_modulelist(modulefiles)
    # if no easyconfigs found then ec_list will be empty so we should stop and report this application is not built by easybuild. This feature can be changed in future
    if len(ec_list) == 0:
        print ("Application: %s is not built from Easybuild, cannot find easyconfig file in installation directory", os.path.join(app_name,app_ver))
        sys.exit(1)

    return
