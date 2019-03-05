############################################################################
#
#  Copyright 2017-2019
#
#  https://github.com/HPC-buildtest/buildtest-framework
#
#  This file is part of buildtest.
#
#  buildtest is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  buildtest is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with buildtest.  If not, see <http://www.gnu.org/licenses/>.
#############################################################################

"""
All CMake related functions necessary for writing configuration when writing
the tests.
"""


import os
import shutil
import logging

from buildtest.tools.config import config_opts, logID
from buildtest.tools.file import create_dir, create_file,string_in_file
from buildtest.tools.utility import get_appname, get_appversion


def init_CMakeList(filename):
    """ This method writes the content of BUILDTEST_ROOT/CMakeLists.txt. """

    header = """
cmake_minimum_required(VERSION 2.8)
include(CTest)
ENABLE_TESTING()
add_subdirectory(""" + config_opts['BUILDTEST_TESTDIR'] + ")"

    try:

        fd=open(filename, 'w')
        fd.write(header)
        fd.close()
    except FileNotFoundError as err_msg:
        print(err_msg)
        raise


def update_cmakelists(filename, tag):
    """ This method updates CMakeLists.txt with tag add_subdirectory() that has
        name of subdirectory where CMakeList.txt resides.

        :param filename: CMakeLists.txt that needs to be updated
        :param tag: Name of the subdirectory to be be added in CMakeLists.txt
    """
    fd=open(filename, 'r')
    content=fd.read().strip().split("\n")
    cmd="add_subdirectory("+tag+")"
    if cmd not in content:
        fd.close()
        fd=open(filename, 'a')
        fd.write(cmd+"\n")
        fd.close()
    else:
        fd.close()

def add_test_to_CMakeLists(app_destdir,subdir,cmakelist,testname):
    """ This method inserts the add_test() command in CMakeLists.txt used for
        adding tests so ctest can run the test."""

    fd=open(cmakelist, 'a')
    logger = logging.getLogger(logID)
    shell_type = config_opts['BUILDTEST_SHELL']
    app_name = get_appname()
    app_version = get_appversion()

    if subdir != "":
        parent_cmakelist = os.path.join(app_destdir, "CMakeLists.txt")
        cmake_content = "add_subdirectory(" + subdir + ") \n"
        ret = string_in_file(cmake_content, parent_cmakelist)
        if not ret:
            fd1=open(parent_cmakelist, 'a')
            fd1.write(cmake_content)
            fd1.close()


    # the add_test command is a directive that can be added in CMakeLists.txt
    # to run tests in ctest framework. See
    # https://cmake.org/cmake/help/v3.0/command/add_test.html.
    add_test_str = "add_test(NAME {}-{}-{} COMMAND {} {} ".format(app_name,
                                                                  app_version,
                                                                  testname,
                                                                  shell_type,
                                                                  testname)
    add_test_str += "\t WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} ) \n"

    # dont overwrite add_test if it already exist in file due to repeated runs
    if not string_in_file(add_test_str, cmakelist):
        fd.write(add_test_str)

    fd.close()
    logger.debug("Updating File " + cmakelist + " with: " + add_test_str + "\n")


def setup_software_cmake():
    """Create the CMakeLists.txt for subdirectory in BUILDTEST_TESTDIR when
    buildtest software test."""
    logger = logging.getLogger(logID)

    name = get_appname()
    version = get_appversion()

    # if top level software directory is not present, create it
    test_ebapp_dir = os.path.join(config_opts['BUILDTEST_TESTDIR'], "ebapp")

    # variables to reference each subdirectory in <software>/<version>
    test_name_dir = os.path.join(test_ebapp_dir, name)
    test_version_dir = os.path.join(test_name_dir, version)


    # CMakeLists.txt assignment for each subdirectory from root to where test
    # will be written
    test_cmakelist = os.path.join(config_opts['BUILDTEST_TESTDIR'],
                                  "CMakeLists.txt")
    test_ebapp_cmakelist = os.path.join(test_ebapp_dir, "CMakeLists.txt")
    test_name_cmakelist = os.path.join(test_name_dir, "CMakeLists.txt")
    test_version_cmakelist = os.path.join(test_version_dir, "CMakeLists.txt")

    test_destdir = test_version_dir


    logger.debug("----------------------------------------")
    logger.debug("EB Directory Assignments")
    logger.debug("----------------------------------------")

    logger.debug("EB Directory in $BUILDTEST_TESTDIR: %s ", test_ebapp_dir)
    logger.debug("EB Application Directory: %s", test_name_dir)
    logger.debug("EB Application Version Directory: %s", test_version_dir)

    logger.debug("\n")
    logger.debug("Test Directory for EB Application: %s ", test_destdir)

    logger.debug("\n\n")

    logger.debug("----------------------------------------")
    logger.debug("EB CMakeList Assignments")
    logger.debug("----------------------------------------")

    logger.debug("$BUILDTEST_TESTDIR CMakeList Path: %s ", test_cmakelist)
    logger.debug("EB Application CMakeList Path: %s ", test_name_cmakelist)
    logger.debug("EB Application Version CMakeList Path: %s",
                 test_version_cmakelist)


    # when --clean-build is passed then buildtest should do a clean build
    if config_opts['BUILDTEST_CLEAN_BUILD']:
        # if test directory exist, delete it
        if os.path.isdir(test_destdir):
            shutil.rmtree(test_destdir)
            logger.debug("Removing test directory before creating test: %s",
                         test_destdir)

    # create destination directory if it does not exist
    create_dir(test_destdir)


    # create file CMakeList.txt file in each subdirectory
    create_file(test_cmakelist)
    create_file(test_ebapp_cmakelist)
    create_file(test_name_cmakelist)
    create_file(test_version_cmakelist)


    # update CMakeLists.txt with tags add_subdirectory() to properly
    # traverse directory to find tests
    update_cmakelists(test_cmakelist, "ebapp")
    update_cmakelists(test_ebapp_cmakelist, name)
    update_cmakelists(test_name_cmakelist, version)


    return test_destdir, os.path.join(test_destdir,"CMakeLists.txt")

def setup_system_cmake(pkg):
    """ Create CMakeLists.txt in BUILDTEST_TESTDIR and its sub directory when
    buildtest system package tests. """


    # top level system directory and system package directory
    test_system_dir = os.path.join(config_opts['BUILDTEST_TESTDIR'], "system")
    test_destdir = os.path.join(config_opts['BUILDTEST_TESTDIR'], "system", pkg)

    # top level CMakeLists.txt in testing directory
    test_cmakelist = os.path.join(config_opts['BUILDTEST_TESTDIR'],
                                  "CMakeLists.txt")

    # CMakeLists.txt that contains all system package directories to process
    test_cmakelist_pkg = os.path.join(config_opts['BUILDTEST_TESTDIR'],
                                      "system",
                                      "CMakeLists.txt")

    # CMakeLists.txt for dest dir where test are written.
    test_cmakelist_destdir = os.path.join(test_destdir, "CMakeLists.txt")

    logger = logging.getLogger(logID)

    logger.debug("Variables Assignments")
    logger.debug("----------------------------------")
    logger.debug("SYSTEM Test Directory: %s ", test_system_dir)
    logger.debug("Testscript Destination Directory: %s", test_destdir)
    logger.debug("CMakeList for BUILDTEST_TESTDIR: %s ", test_cmakelist)
    logger.debug("CMakeList for $BUILDTEST_TESTDIR/system: %s",
                 test_cmakelist_pkg)
    logger.debug("CMakeList for $BUILDTEST_TESTDIR/system/%s: %s",
                 pkg,
                 test_cmakelist_destdir)

    if config_opts['BUILDTEST_CLEAN_BUILD']:
        # if testdirectory exist, delete entire directory
        if os.path.isdir(test_destdir):
            shutil.rmtree(test_destdir)
            logger.debug("Removing directory: %s before creating tests ",
                         test_destdir)

    # create the destination directory
    create_dir(test_destdir)

    # create CMakeLists.txt files
    create_file(test_cmakelist)
    create_file(test_cmakelist_pkg)
    create_file(test_cmakelist_destdir)

    # update the CMakeLists.txt with the directive add_subdirectory()
    update_cmakelists(test_cmakelist, "system")
    update_cmakelists(test_cmakelist_pkg, pkg)

    logger.debug("Updating %s with add_subdirectory(system)", test_cmakelist)
    logger.debug("Updating %s with add_subdirectory(%s)", test_cmakelist_pkg,
                 pkg)

    return test_destdir, test_cmakelist_destdir
