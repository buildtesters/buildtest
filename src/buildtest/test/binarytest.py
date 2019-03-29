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
buildtest will create a test for each binary command found in the software or system package
based on $PATH. For system package it will search standard Linux path where binaries are
installed such as /usr/bin, /usr/sbin, etc...
For application it will search for binaries found in $PATH set by module file
"""

import logging
import os
import stat


from buildtest.tools.config import config_opts, logID
from buildtest.tools.cmake import init_CMakeList, setup_software_cmake, \
    setup_system_cmake, add_test_to_CMakeLists
from buildtest.tools.file import string_in_file
from buildtest.tools.modules import module_obj
from buildtest.tools.software import get_binaries_from_application
from buildtest.tools.system import get_binaries_from_systempackage, \
    BuildTestCommand
from buildtest.tools.utility import get_appname, get_appversion



def generate_binary_test(name,test_type=None):
    """This method generates binary test. For software the modules and any
    parent modules are loaded in advance. A separate test is created for each
    binary command. Every test is written in BUILDTEST_TESTDIR in the
    appropriate subdirectory to distinguish between different
    application version. Each test is added to CMakeLists.txt. In each test
    the command "which" is run against every binary to ensure file exists."""
    subdir=""

    # top level CMakeList.txt should be in same parent directory where BUILDTEST_TESTDIR is created
    toplevel_cmakelist_file=os.path.join(os.path.dirname(config_opts['BUILDTEST_TESTDIR']),"CMakeLists.txt")
    testingdir_cmakelist_file=os.path.join(config_opts['BUILDTEST_TESTDIR'],"CMakeLists.txt")

    # ------------- NEED TO IMPLEMENT THIS AGAIN. OHPC Binary Test will be broken since we wont be reading from yaml file
    #if config_opts["BUILDTEST_OHPC"]:
    #    commandfile = os.path.join(config_opts["BUILDTEST_CONFIGS_REPO"],"buildtest/ohpc",name.lower(),"command.yaml")



    logger = logging.getLogger(logID)

    logger.debug("This is a %s binary test", test_type)


    # if CMakeLists.txt does not exist in top-level directory, create the header
    if os.path.isfile(toplevel_cmakelist_file) == False:
        logger.warning("File: %s was not found, will create it automatically",
                       toplevel_cmakelist_file)
        init_CMakeList(toplevel_cmakelist_file)

    # if BUILDTEST_TESTDIR/CMakeLists.txt does not exist, then create it
    if os.path.isfile(testingdir_cmakelist_file) == False:
        logger.warning("File: %s  was not found, will create it automatically",
                       testingdir_cmakelist_file)
        fd=open(testingdir_cmakelist_file,'w')
        fd.close()

    print ("--------------------------------------------")
    print ("[STAGE 1]: Building Binary Tests")
    print ("--------------------------------------------")
    binary_tests = []
    preload_modules = ""
    if test_type == "software":

        #name = get_appname()
        test_destdir,test_destdir_cmakelist = setup_software_cmake()
        print ("Detecting Software:" + name )
        binary_tests = get_binaries_from_application(name)

        parent_module = module_obj.get_parent_modules(name)
        for item in parent_module:
            preload_modules += f"module try-load {item};"
        print (preload_modules)
    else:
        print ("Detecting System Package: " + name)
        test_destdir,test_destdir_cmakelist = setup_system_cmake(name)
        binary_tests = get_binaries_from_systempackage(name)

    count = 0
    shell_path =  BuildTestCommand().which(config_opts["BUILDTEST_SHELL"])[
        0]
    for key in binary_tests:
        count = count + 1
        name_str=key.replace(" ","_")

        # replace / with _ when creating testname for yaml configuration that have path name
        name_str = name_str.replace("/","_")

        testname=name_str+"."+config_opts["BUILDTEST_SHELL"]
        testpath=os.path.join(test_destdir,testname)

        logger.debug("Creating and Opening  test file: %s for writing ",  testpath)
        fd=open(testpath,'w')

        shell_magic = f"#!{shell_path}"
        fd.write(shell_magic + "\n")

        if test_type == "software":
            fd.write(f"{preload_modules} \n")
            fd.write(f"module load {name} \n")

        fd.write("which " + key)
        fd.close()

        # setting perm to 755 on testscript
        os.chmod(testpath, stat.S_IRWXU |  stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH |  stat.S_IXOTH)
        # reading test script for writing content of test in logcontent
        fd=open(testpath,'r')
        content=fd.read().splitlines()
        fd.close()

        logger.info("Content of test file: %s ", testpath)
        logger.info("[START TEST-BLOCK]")
        for line in content:
                logger.info("%s", line)

        logger.info("[END TEST-BLOCK]")

        if test_type == "software":
            add_test_to_CMakeLists(test_destdir,
                                   subdir,
                                   test_destdir_cmakelist,
                                   testname)
        else:
            logger.debug("Updating CMakeList file: %s", test_destdir_cmakelist)
            fd=open(test_destdir_cmakelist,'a')
            add_test_str="add_test(NAME system-" + name + "-" + testname + "\t COMMAND " + config_opts["BUILDTEST_SHELL"] + " " + testname + "\t WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}) \n"

            if not string_in_file(add_test_str,test_destdir_cmakelist):
                logger.debug("Adding content: %s ",  add_test_str)
                fd.write(add_test_str)

    fd.close()

    print
    print ("Generating ", count, " binary tests")
    print ("Binary Tests are written in ", test_destdir)
