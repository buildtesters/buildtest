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
This python module is used with the flag --testset to create test scripts that
don't require any YAML files.

:author: Shahzeb Siddiqui (Pfizer)

"""

import os
import logging
import subprocess

from buildtest.test.job import generate_job
from buildtest.test.sourcetest import recursive_gen_test
from buildtest.tools.cmake import add_test_to_CMakeLists, setup_software_cmake
from buildtest.tools.config import config_opts, PYTHON_APPS, MPI_APPS, logID, config_opts
from buildtest.tools.modules import load_modules
from buildtest.tools.utility import get_appname, get_appversion, get_toolchain_name, get_toolchain_version


def run_testset(arg_dict):
    """ checks the testset parameter to determine which set of scripts to use to create tests """

    print "--------------------------------------------"
    print "[STAGE 3]: Building Testset"
    print "--------------------------------------------"

    BUILDTEST_CONFIGS_REPO = config_opts['BUILDTEST_CONFIGS_REPO']
    BUILDTEST_PYTHON_REPO = config_opts['BUILDTEST_PYTHON_REPO']
    BUILDTEST_TCL_REPO = config_opts['BUILDTEST_TCL_REPO']
    BUILDTEST_R_REPO = config_opts['BUILDTEST_R_REPO']
    BUILDTEST_PERL_REPO = config_opts['BUILDTEST_PERL_REPO']
    BUILDTEST_RUBY_REPO = config_opts['BUILDTEST_RUBY_REPO']

    appname = get_appname()

    source_app_dir=""
    codedir=""
    logcontent = ""
    runtest = False
    if appname.lower() in PYTHON_APPS and arg_dict.testset == "Python":
        source_app_dir=os.path.join(BUILDTEST_PYTHON_REPO,"python")
        runtest=True
    if appname.lower() in ["perl"] and arg_dict.testset == "Perl":
        source_app_dir=os.path.join(BUILDTEST_PERL_REPO,"perl")
        runtest=True
    # condition to run R testset
    if appname.lower() in ["r"] and arg_dict.testset == "R":
        source_app_dir=os.path.join(BUILDTEST_R_REPO,"R")
        runtest=True

    # condition to run R testset
    if appname.lower() in ["ruby"] and arg_dict.testset == "Ruby":
        source_app_dir=os.path.join(BUILDTEST_RUBY_REPO,"ruby")
        runtest=True

    # condition to run R testset
    if appname.lower() in ["tcl"] and arg_dict.testset == "Tcl":
        source_app_dir=os.path.join(BUILDTEST_TCL_REPO,"Tcl")
        runtest=True

    # for MPI we run recursive_gen_test since it processes YAML files
    if appname in MPI_APPS and arg_dict.testset == "MPI":
        source_app_dir=os.path.join(BUILDTEST_CONFIGS_REPO,"mpi")
        configdir=os.path.join(source_app_dir,"config")
        codedir=os.path.join(source_app_dir,"code")
        recursive_gen_test(configdir,codedir)
        return
    if runtest == True:
        codedir=os.path.join(source_app_dir,"code")
        testset_generator(arg_dict,codedir)

def testset_generator(arg_dict, codedir):

    logger = logging.getLogger(logID)
    BUILDTEST_TESTDIR = config_opts['BUILDTEST_TESTDIR']
    wrapper=""
    appname=get_appname()
    appver=get_appversion()
    tcname=get_toolchain_name()
    tcver=get_toolchain_version()

    BUILDTEST_SHELL = config_opts['BUILDTEST_SHELL']
    BUILDTEST_ENABLE_JOB = config_opts['BUILDTEST_ENABLE_JOB']
    BUILDTEST_JOB_TEMPLATE = config_opts['BUILDTEST_JOB_TEMPLATE']

    app_destdir = os.path.join(BUILDTEST_TESTDIR,"ebapp",appname,appver,tcname,tcver)
    cmakelist = os.path.join(app_destdir,"CMakeLists.txt")

    # setup CMakeList in all subdirectories for the app if CMakeList.txt was not generated from
    # binary test
    if not os.path.exists(cmakelist):
        setup_software_cmake()

    emptylist = []
    testset_name = os.path.basename(os.path.dirname(codedir))

    if os.path.isdir(codedir):
        totalcount = 0
        for root,subdirs,files in os.walk(codedir):

            package_name = os.path.basename(root)

            if testset_name == "python":
                ret = verify_python_library(package_name)
                # if import package fails then skip test generation
                if ret > 0:
                    continue

            #print testset_name,package_name
            if testset_name == "R":
                ret = verify_R_library(package_name)
                # if import package fails then skip test generation
                if ret > 0:
                    continue

            #print testset_name,package_name
            if testset_name == "Ruby":
                ret = verify_Ruby_gem(package_name)
                # if import package fails then skip test generation
                if ret > 0:
                    continue

            # skip to next item in loop when a sub-directory has no files
            if len(files) == 0:
                continue

            count = 0

            for file in files:
                # get file name without extension
                fname = os.path.splitext(file)[0]
                # get file extension
                ext = os.path.splitext(file)[1]

                if testset_name == "perl":
                    #print files, file
                    #print root,files, file, fname
                    perl_module = os.path.basename(root) + "::" + fname
                    print perl_module
                    ret = verify_perl_module(perl_module)
                    # if import package fails then skip test generation
                    if ret > 0:
                        continue

                if ext == ".py":
                    wrapper = "python"
                elif ext == ".R":
                    wrapper = "Rscript"
                elif ext == ".pl":
                    wrapper = "perl"
                elif ext == ".rb":
                    wrapper = "ruby"
                elif ext == ".tcl":
                    wrapper = "tclsh"
                else:
                    continue

                # command to execute the script
                cmd = wrapper + " " + os.path.join(root,file)

                # getting subdirectory path to write test to correct path
                subdir = os.path.basename(root)
                subdirpath = os.path.join(app_destdir,subdir)
                if not os.path.exists(subdirpath):
                    os.makedirs(subdirpath)

                testname = fname + "." + BUILDTEST_SHELL
                testpath = os.path.join(subdirpath,testname)
                fd = open(testpath,'w')
                header=load_modules(BUILDTEST_SHELL)
                fd.write(header)
                fd.write(cmd)
                fd.close()

                cmakelist = os.path.join(subdirpath,"CMakeLists.txt")
                add_test_to_CMakeLists(app_destdir,subdir,cmakelist,testname)
                msg = "Creating Test: " + testpath
                logger.info(msg)
                count = count + 1

                if BUILDTEST_ENABLE_JOB:
                    generate_job(testpath,BUILDTEST_SHELL,BUILDTEST_JOB_TEMPLATE,emptylist)

            print "Generating ", count, "tests for ", os.path.basename(root)
            totalcount += count
    print "Total Tests created in stage 3:", totalcount
    print "Writing tests to ", app_destdir

def verify_python_library(python_lib):
    """ check if python package exist for request python module, if it exists create test otherwise skip test creation"""

    logger = logging.getLogger(logID)

    appname=get_appname()
    appver=get_appversion()

    BUILDTEST_MODULE_NAMING_SCHEME = config_opts['BUILDTEST_MODULE_NAMING_SCHEME']
    cmd = "module purge; module load " + os.path.join(appname,appver) + "; python -c \"import " + python_lib + "\""

    if BUILDTEST_MODULE_NAMING_SCHEME == "HMNS":
        tcname = get_toolchain_name()
        tcver = get_toolchain_version()
        if len(tcname) > 0:
            cmd = "module purge; module load " + os.path.join(tcname,tcver) + "; module load " + os.path.join(appname,appver) + "; python -c \"import " +  python_lib + "\""

    logger.debug("Check Python Package:" + python_lib)
    logger.debug("Running command -" + cmd)

    ret = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    ret.communicate()
    return ret.returncode


def verify_R_library(R_lib):
    """ check if R library exist for request R module, if it exists create test otherwise skip test creation"""

    logger = logging.getLogger(logID)

    appname=get_appname()
    appver=get_appversion()

    BUILDTEST_MODULE_NAMING_SCHEME = config_opts['BUILDTEST_MODULE_NAMING_SCHEME']
    cmd = ""


    cmd = "module purge; module load " + os.path.join(appname,appver) + "; echo \"library(" + R_lib + ")\" | R -q --no-save "

    if BUILDTEST_MODULE_NAMING_SCHEME == "HMNS":
        tcname = get_toolchain_name()
        tcver = get_toolchain_version()
        if len(tcname) > 0:
            cmd = "module purge; module load " + os.path.join(tcname,tcver) + "; module load " + os.path.join(appname,appver) + "; echo \"library(" + R_lib + ")\" | R -q --no-save "


    logger.debug("Check R Package:" + R_lib)
    logger.debug("Running command - " + cmd)

    ret = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    ret.communicate()
    return ret.returncode

def verify_perl_module(perl_module):
    """ check if perl module exist for request perl module, if it exists create test otherwise skip test creation"""

    logger = logging.getLogger(logID)
    appname=get_appname()
    appver=get_appversion()

    BUILDTEST_MODULE_NAMING_SCHEME = config_opts['BUILDTEST_MODULE_NAMING_SCHEME']
    cmd = "module purge; module load " + os.path.join(appname,appver) + "; perl -e \' use " +  perl_module + ";\'"

    if BUILDTEST_MODULE_NAMING_SCHEME == "HMNS":
        tcname = get_toolchain_name()
        tcver = get_toolchain_version()
        if len(tcname) > 0:
            cmd = "module purge; module load " + os.path.join(tcname,tcver) + "; module load " + os.path.join(appname,appver) + "; perl -e \' use " + perl_module + ";\'"

    logger.debug("Checking Perl Module " + perl_module)
    logger.debug("Running command - " + cmd)

    ret = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    ret.communicate()
    return ret.returncode

def verify_Ruby_gem(Ruby_gem):
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

    logger.debug("Check Ruby gem:" + R_lib)
    logger.debug("Running command - " + cmd)

    ret = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    ret.communicate()
    return ret.returncode
