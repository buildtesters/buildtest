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
Support for building ruby package tests and checks if ruby libraries exists


:author: Shahzeb Siddiqui (Pfizer)
"""

import logging
import os
import subprocess
import sys
import stat

from buildtest.test.job import generate_job
from buildtest.tools.config import config_opts, logID
from buildtest.tools.file import create_dir
from buildtest.tools.modules import load_modules
from buildtest.tools.utility import get_appname, get_appversion, get_toolchain_name, get_toolchain_version


def ruby_pkg_choices():
    """ return a list of ruby packages for --ruby-package option """
    ruby_choices =  os.listdir(config_opts['BUILDTEST_RUBY_TESTDIR'])
    return ruby_choices

def check_ruby_package(Ruby_gem):
    """ check if ruby gem exist for request ruby module, if it exists create test otherwise skip test creation"""

    logger = logging.getLogger(logID)

    appname=get_appname()
    appver=get_appversion()

    BUILDTEST_MODULE_NAMING_SCHEME = config_opts['BUILDTEST_MODULE_NAMING_SCHEME']
    cmd = "module purge; module load " + os.path.join(appname,appver) + "; gem list -i " + Ruby_gem

    if BUILDTEST_MODULE_NAMING_SCHEME == "HMNS":
        tcname = get_toolchain_name()
        tcver = get_toolchain_version()
        if len(tcname) > 0:
            cmd = "module purge; module load " + os.path.join(tcname,tcver) + "; module load " + os.path.join(appname,appver) + "; gem list - i " + Ruby_gem

    logger.debug("Check Ruby gem:" + Ruby_gem)
    logger.debug("Running command - " + cmd)

    ret = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    ret.communicate()
    ret_code = ret.returncode
    if ret_code != 0:
        print ( Ruby_gem, " is not installed in software ", os.path.join(appname,appver))
        sys.exit(1)

def build_ruby_package_test(ruby_package):
    """ build ruby package tests. Implements option --ruby-package """


    from buildtest.tools.cmake import add_test_to_CMakeLists, setup_software_cmake

    BUILDTEST_TESTDIR = config_opts['BUILDTEST_TESTDIR']
    BUILDTEST_SHELL = config_opts['BUILDTEST_SHELL']
    BUILDTEST_ENABLE_JOB = config_opts['BUILDTEST_ENABLE_JOB']
    BUILDTEST_JOB_TEMPLATE = config_opts['BUILDTEST_JOB_TEMPLATE']

    appname = get_appname()
    appver=get_appversion()
    tcname=get_toolchain_name()
    tcver=get_toolchain_version()

    logger = logging.getLogger(logID)

    if appname.lower() != "ruby":
        print ("ERROR: software module does not appear to be Ruby module ")
        sys.exit(1)

    app_destdir = os.path.join(BUILDTEST_TESTDIR,"ebapp",appname,appver,tcname,tcver)
    cmakelist = os.path.join(app_destdir,"CMakeLists.txt")
    ruby_package_dir = os.path.join(config_opts['BUILDTEST_RUBY_TESTDIR'],ruby_package)

    if not os.path.exists(cmakelist):
        setup_software_cmake()

    check_ruby_package(ruby_package)
    count = 0
    dummy_array=[]
    for root,subdirs,files in os.walk(ruby_package_dir):

        for file in files:
            filename_strip_ext = os.path.splitext(file)[0]
            ext = os.path.splitext(file)[1]

            # skip if file is not .py extension
            if ext != ".rb":
                    continue
            # command to execute the script
            cmd = "ruby " + os.path.join(root,file)

            # getting subdirectory path to write test to correct path
            subdir = os.path.basename(root)
            subdirpath = os.path.join(app_destdir,subdir)
            create_dir(subdirpath)

            testname = filename_strip_ext + "." + BUILDTEST_SHELL
            testpath = os.path.join(subdirpath,testname)
            fd = open(testpath,'w')
            header=load_modules(BUILDTEST_SHELL)
            fd.write(header)
            fd.write(cmd)
            fd.close()

            # setting perm to 755 on testscript
            os.chmod(testpath, stat.S_IRWXU |  stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH |  stat.S_IXOTH)
            
            cmakelist = os.path.join(subdirpath,"CMakeLists.txt")
            add_test_to_CMakeLists(app_destdir,subdir,cmakelist,testname)
            msg = "Creating Test: " + testpath
            logger.info(msg)
            count = count + 1

            if BUILDTEST_ENABLE_JOB:
                generate_job(testpath,BUILDTEST_SHELL,BUILDTEST_JOB_TEMPLATE,dummy_array)

        print ("Generating ", count, " tests for ", os.path.basename(root))
