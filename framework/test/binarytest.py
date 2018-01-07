############################################################################
#
#  Copyright 2017
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
This python module generates the binary test by processing all yaml
files and create .sh scripts along with the CMakeLists configuration. There
is only 1 binary yaml file that can generate multiple binary test

:author: Shahzeb Siddiqui (Pfizer)

"""
import logging
import os
import yaml
from shutil import copyfile
from framework.env import BUILDTEST_ROOT, BUILDTEST_TESTDIR, BUILDTEST_SOURCEDIR, logID
from framework.test.job import generate_job
from framework.tools.cmake import init_CMakeList, setup_software_cmake, setup_system_cmake
from framework.tools.utility import get_appname, get_appversion, get_toolchain_name, get_toolchain_version
from framework.tools.file import create_dir
from framework.tools.modules import load_modules


def generate_binary_test(args_dict,pkg):
        """
        This function generates binary test from command.yaml file. For ebapps apps the module
        and any toolchain is loaded in advance. Each entry in command.yaml will generate a
        separate testscript from this function. All tests will be stored in BUILDTEST_TESTDIR.
        This function makes sure command.yaml exists and CMakeLists.txt is present in all
        subdirectories in BUILDTEST_TESTDIR.
        """

        # variable to indicate if it is a software or system package for binary test
        test_type=""

        toplevel_cmakelist_file=os.path.join(BUILDTEST_ROOT,"CMakeLists.txt")
        testingdir_cmakelist_file=os.path.join(BUILDTEST_TESTDIR,"CMakeLists.txt")
	
	software = args_dict.software
	system = args_dict.system

        #software=get_arg_software(args_dict)
        #system=get_arg_system(args_dict)

        # determine whether we are running a binary test on ebapp or system package
        if software is not None:
                software=software.split("/")
                appname,appversion=software
                configdir=os.path.join(BUILDTEST_SOURCEDIR,"ebapps",appname)
                test_type="software"
        elif system is not None:
                configdir=os.path.join(BUILDTEST_SOURCEDIR,"system",pkg)
                test_type="system"

        commandfile=os.path.join(configdir,"command.yaml")

        logger = logging.getLogger(logID)

        logger.debug("This is a %s binary test", test_type)
        logger.debug("Processing YAML file: %s", commandfile)

        # if CMakeLists.txt does not exist in top-level directory, create the header
        if os.path.isfile(toplevel_cmakelist_file) == False:
                logger.warning("File: %s was not found, will create it automatically", toplevel_cmakelist_file)
                init_CMakeList(toplevel_cmakelist_file)

        if not os.path.exists(BUILDTEST_TESTDIR):
                logger.debug("Creating Directory: %s ", BUILDTEST_TESTDIR)
                create_dir(BUILDTEST_TESTDIR)

        # if BUILDTEST_TESTDIR/CMakeLists.txt does not exist, then create it
        if os.path.isfile(testingdir_cmakelist_file) == False:
                logger.warning("File: %s  was not found, will create it automatically", testingdir_cmakelist_file)
                fd=open(testingdir_cmakelist_file,'w')
                fd.close()

        # if command.yaml does not exist then report error
        if os.path.isfile(commandfile) == False:
                msg =  "Cannot find command file:" +  commandfile + "Skipping binary test for package:", pkg
                logger.error("%s", msg)
                return


        # if all checks have passed then proceed with generating test
        process_binary_file(commandfile,args_dict,test_type,pkg)

def process_binary_file(filename,args_dict,test_type,pkg):
        """
        Module responsible for actually creating the test scripts for binary tests along
        with CMakeLists.txt in subdirectories under $BUILDTEST_TESTDIR. This module
        is used for generating binary tests for both system and ebapps tests.
        """

        logger = logging.getLogger(logID)
	shell_type = ""
	if args_dict.shell:
		shell_type = args_dict.shell
        if test_type == "software":

                name = get_appname()
                version = get_appversion()
                toolchain_name = get_toolchain_name()
                toolchain_version = get_toolchain_version()

                test_destdir,test_destdir_cmakelist = setup_software_cmake()


		print "[BINARYTEST]: Processing YAML file for ", os.path.join(name,version), os.path.join(toolchain_name,toolchain_version), " at ", filename
               # load preamble for test-script that initializes environment.
                header=load_modules(shell_type)

        else:
                system=args_dict.system
		print "[BINARYTEST]: Processing YAML file for ", pkg , " at ", filename
                test_destdir,test_destdir_cmakelist = setup_system_cmake(pkg)



        logger.info("Reading File: %s", filename)
        fd=open(filename,'r')
        content=yaml.load(fd)
        logger.debug("Loading YAML content")
        # if key binaries is not in yaml file, exit program
        if "binaries" not in content:
                logger.error("Can't find key: binaries in file %s", filename)
                print "Can't find key: binaries in file %s", filename
                sys.exit(1)

        # create a binary test script for each key,value item in dictionary
        binarydict=content["binaries"]
        # keep track of number of binary test
        count = 0

        for key in binarydict:
                count = count + 1
                name_str=key.replace(" ","_")
		
		# replace / with _ when creating testname for yaml configuration that have path name
		name_str = name_str.replace("/","_")

                testname=name_str+"."+shell_type
                testpath=os.path.join(test_destdir,testname)

                logger.debug("Creating and Opening  test file: %s for writing ",  testpath)
                fd=open(testpath,'w')

                if test_type == "software":
                        fd.write(header)
                else:
			shell_magic = "#!/" + os.path.join("bin",shell_type)
			fd.write(shell_magic + "\n")
                        fd.write("module purge \n")
                fd.write(key)
                fd.close()

                # reading test script for writing content of test in logcontent
                fd=open(testpath,'r')
                content=fd.read().splitlines()
                fd.close()

                logger.info("Content of test file: %s ", testpath)
                logger.info("[START TEST-BLOCK]")
                for line in content:
                        logger.info("%s", line)


                logger.info("[END TEST-BLOCK]")


                logger.debug("Updating CMakeList file: %s", test_destdir_cmakelist)
                fd=open(test_destdir_cmakelist,'a')
                if test_type == "software":
                        # modify add_test string when toolchain is not defined
                        if len(toolchain_name) == 0:
                                add_test_str="add_test(NAME " + name + "-" + version + "-" + testname + "\t COMMAND " + shell_type + " " + testname + "\t WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}) \n"
                        else:
                                add_test_str="add_test(NAME " + name + "-" + version + "-" + toolchain_name + "-" + toolchain_version + "-" + testname + "\t COMMAND " + shell_type + " " + testname + "\t WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}) \n"
                else:
                        add_test_str="add_test(NAME system-" + pkg + "-" + testname + "\t COMMAND " + shell_type + " " + testname + "\t WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}) \n"


                logger.debug("Adding content: %s ",  add_test_str)
                fd.write(add_test_str)
		fd.close()

		if args_dict.job_template is not None:
			generate_job(testpath,shell_type,args_dict.job_template, content)

        print
        if test_type == "system":
                print "Generating " + str(count) + " binary tests for package: " + pkg
        else:
                print "Generating " + str(count) + " binary tests for Application: " + name + "/" + version

        print "Binary Tests are written in " + test_destdir


