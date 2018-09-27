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
This python module generates the binary & source test by processing all yaml
files and create .sh scripts along with the CMakeLists configuration. There
is only 1 binary yaml file that can generate multiple binary test, while
source test has 1 YAML file and generates only 1 test

:author: Shahzeb Siddiqui (Pfizer)
"""

import re
import sys
import os
import logging
import stat
from shutil import copyfile


from buildtest.test.compiler import get_compiler
from buildtest.test.function import add_arg_to_runcmd
from buildtest.test.job import generate_job, generate_job_by_config
from buildtest.tools.cmake import  add_test_to_CMakeLists
from buildtest.tools.config import  config_opts, logID
from buildtest.tools.file import create_dir
from buildtest.tools.modules import load_modules
from buildtest.tools.parser.yaml_config import parse_config
from buildtest.tools.utility import get_appname, get_appversion, get_toolchain_name, get_toolchain_version


def recursive_gen_test(configdir,codedir):
    """ if config directory exists then process all .yaml files to build source test """

    # only process yaml files if configdir directory is found
    if os.path.isdir(configdir):

        logger = logging.getLogger(logID)

        logger.debug("Processing all YAML files in %s", configdir)

        print ("--------------------------------------------")
        print ("[STAGE 2]: Building Source Tests")
        print ("--------------------------------------------")

        print ("Processing all YAML files in directory: ", configdir)
        count = 0
        for root,subdirs,files in os.walk(configdir):

            # skip to next element if subdirectory has no files
            if len(files) == 0:
                continue

            #filepath=configdir+filename
            for file in files:
                filepath=os.path.join(root,file)
                subdir=os.path.basename(root)

                # if there is no subdirectory in configdir that means subdir would be set to "config" so it can
                # be set to empty string in order to concat codedir and subdir. This way both subdirectory and
                # and no subdirectory structure for yaml will work
                if subdir == "config":
                    subdir = ""

                code_destdir=os.path.join(codedir,subdir)
                logger.debug("Parsing YAML file: %s", filepath)
                configmap=parse_config(filepath,code_destdir)
                # error processing config file, then parse_config will return an empty dictionary

                if configmap is None:
                    continue
                if len(configmap) == 0:
                    continue

                count = count + 1

                generate_source_test(configmap,code_destdir,subdir)

        appname=get_appname()
        appver=get_appversion()
        tcname=get_toolchain_name()
        tcver=get_toolchain_version()
        BUILDTEST_TESTDIR = config_opts['BUILDTEST_TESTDIR']
        destdir = os.path.join(BUILDTEST_TESTDIR,"ebapp",appname,appver,tcname,tcver)

        print ("Generating", count, " Source Tests and writing at ",destdir)
    else:
        return

# generate test for source
def generate_source_test(configmap,codedir,subdir):
    """
    This function generates the tests that requires compilation for EB apps. The
    tests are written <software>/<version>/<toolchain-name>/<toolchain-version>.
    The test script is named according to "name" key tag with the shell extension
    CMakeLists.txt has an entry for each test that executes the shell-script. Most
    test requires a compilation step, while every test requires a execution stage.
    This is done via buildcmd and runcmd tags in YAML for explicit builds. buildtest
    will try to generate this automatically if nothing is provided.
    """

    appname=get_appname()
    appver=get_appversion()
    tcname=get_toolchain_name()
    tcver=get_toolchain_version()

    logger = logging.getLogger(logID)
    BUILDTEST_TESTDIR = config_opts['BUILDTEST_TESTDIR']

    testname = ""
    testpath = ""
    sourcefilepath = ""
    executable = ""
    buildopts = ""
    environment = ""
    env_msg = []
    # app_destdir is root of test directory
    app_destdir = os.path.join(BUILDTEST_TESTDIR,"ebapp",appname,appver,tcname,tcver)

    # destdir is where test script and CMakeLists.txt will be generated.
    # If there is a subdirectory then testscript will reside in subdir
    destdir=os.path.join(app_destdir,subdir)
    cmakelist=os.path.join(destdir,"CMakeLists.txt")

    # if subdirectory exists, create subdirectory in destdir so we can write test script
    #if subdir != "":
        # if sub directory does not exist, then create all directories and its parents directories
    create_dir(destdir)


    shell_type = config_opts['BUILDTEST_SHELL']
    BUILDTEST_JOB_TEMPLATE = config_opts['BUILDTEST_JOB_TEMPLATE']
    BUILDTEST_ENABLE_JOB = config_opts['BUILDTEST_ENABLE_JOB']

    # testname is key value "name" with .sh extension
    testname=configmap["name"]+"."+shell_type
    testpath=os.path.join(destdir,testname)
    sourcefilepath=os.path.join(codedir,configmap["source"])
    # name of the executable is the value of source tag with ".exe" extension
    executable=configmap["source"]+".exe"

    if "procrange" in configmap:
        procrange = configmap["procrange"]
        startproc =  int(procrange.split(",")[0])
        endproc = int(procrange.split(",")[1])
        procinterval = int(procrange.split(",")[2])
        testname=configmap["name"]+"_nproc_"+str(startproc)+"."+shell_type
        testpath = os.path.join(destdir,testname)
        mpi_proc_list = range(startproc,endproc+1,procinterval)

    if "threadrange" in configmap:
        threadrange = configmap["threadrange"]
        startthread =  int(threadrange.split(",")[0])
        endthread = int(threadrange.split(",")[1])
        threadinterval = int(threadrange.split(",")[2])
        testname=configmap["name"]+"_nthread_"+str(startthread)+"."+shell_type
        testpath = os.path.join(destdir,testname)
        thread_list = range(startthread,endthread+1,threadinterval)
        openmp_env_str = get_environment_variable(shell_type,"OMP_NUM_THREADS",startthread)

    # write the preamble to test-script to initialize app environment using module cmds
    fd=open(testpath,'w')
    header=load_modules(shell_type)
    fd.write(header)

    # setting perm to 755 on testscript
    os.chmod(testpath, stat.S_IRWXU |  stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH |  stat.S_IXOTH)
    flags=""
    # if buildopts key exists in dictionary, then add flags to compilation step (buildcmd)
    if "buildopts" in configmap:
        flags=configmap["buildopts"]

    logger.debug("Test Name: %s", testname)
    logger.debug("Test Path: %s", testpath)
    logger.debug("Source File: %s", sourcefilepath)
    logger.debug("Executable Name: %s",  executable)
    logger.debug("Build Flags: %s",  flags)

    if "environment" in configmap:
        environment = configmap["environment"]

        # loop over a list of tuples that content environment name and value
        for variable in environment:
            # extract value from list of tuple, since variables.keys() will only return one tuple we just index the first element
            env_key = list(variable.keys())[0]
            env_value = list(variable.values())[0]

            env_msg.append(get_environment_variable(shell_type,env_key,env_value))
        for variable in env_msg:
            fd.write(variable)

    # string used for generating the compilation step
    buildcmd=""
    # string used for running the executable and used for injecting commands at pre/post test
    runcmd=""
    # string to decide the compiler wrapper to use based on application and file extension
    compiler=""
    # used for parallel processing to specify # of procs with mpirun -np
    nproc = ""


    logger.debug("""Checking for YAML key "buildcmd" and "runcmd" """)

    # if there is a buildcmd & runcmd in yaml file, place this directly in test script
    if "buildcmd" in configmap and "runcmd" in configmap:

        logger.debug("YAML file found buildcmd and runcmd.")
        logger.debug("buildtest will generate explicit build/run commands from buildcmd and runcmd field")

        # only process buildcmd if there is a value specified for buildcmd key
        if configmap["buildcmd"] != None:
            # for each element from dictionary configmap["buildcmd"], write
            # each instruction in buildcmd separated by newline
            for cmd in configmap["buildcmd"]:
                buildcmd += cmd + "\n"
        else:
            msg = "buildcmd is declared but value is not specified \n"
            logger.debug("%s",msg)

        if configmap["runcmd"] != None:
            # process the runcmd tag similar same as buildcmd and store in variable
            # runcmd except if no value is specified for runcmd in YAML then throw
            # an error
            for cmd in configmap["runcmd"]:
            	runcmd += cmd + "\n"
        else:
            msg = "runcmd is declared but value is not specified. Need runcmd to run executable \n"
            print (msg)
            logger.debug.append("%s",msg)
            logging.warning("Unable to create test from YAML config, skipping test generation")
            return

        fd.write(buildcmd)
        fd.write(runcmd)
    # otherwise generate the buildcmd and runcmd automatically
    else:

        # checking if either buildcmd or runcmd specified but not both, then report an error.
        if "buildcmd" in configmap and "runcmd" not in configmap or "buildcmd" not in configmap and "runcmd" in configmap:
            print ("Need to specify both key: buildcmd and runcmd")

            logger.warning("Need to declare both key: buildcmd and runcmd. Skipping to next YAML config \n")
            return

        # get the compiler tag and type based on application and toolchain
        compiler,compiler_type=get_compiler(configmap,appname,tcname)


        logger.debug("buildtest will auto-generate buildcmd & runcmd")
        logger.debug("Compiler: %s", compiler)
        logger.debug("Compiler Type: %s", compiler_type)

        # set buildcmd based on compiler_type. compiler is either nvcc,gcc,icc,mpicc, or mpiicc for intel
        if compiler_type == "gnu" or compiler_type == "intel" or compiler_type == "cuda":

            buildcmd = compiler + " -o " + executable + " " + sourcefilepath + " " + flags + "\n"


            # set runcmd for mpi tags using mpirun otherwise just run executable
            if compiler in ["mpicc","mpic++","mpifort","mpiicc","mpiic++", "mpiifort"]:

                # if nproc is defined in yaml, store value in nproc which will use it in mpirun command
                if "nproc" in configmap:
                    nproc = str(configmap["nproc"])
                    logger.debug("nproc key found in YAML config file")
                    logger.debug("nproc: %s", nproc)

                # check for procrange in case nproc is not defined
                elif "procrange" in configmap:
                    nproc = str(startproc)

                # if nproc is not specified set it to 1 when building mpi apps
                else:
                    nproc = "1"

                    logger.debug("nproc key not found in YAML config file, will set nproc = 1")
                    # add argument to runcmd in MPI jobs
                    if "args" in configmap:
                        args = configmap["args"]
                        runcmd = "mpirun -np " + nproc + " ./" + executable
                        runcmd += " " + args
                    else:
                        runcmd = "mpirun -np " + nproc + " ./" + executable
            else:
                # add argument to runcmd in general jobs
                if "args" in configmap:
                    args = configmap["args"]
                    runcmd = "./" + executable
                    runcmd += " " + args
                else:
                    runcmd = "./" + executable

        # Scripting languages like Python, R, Perl no compilation stage, just run script. So we just need to update runcmd string
        elif compiler_type == "python" or compiler_type == "perl" or compiler_type == "R":
            if "args" in configmap:
                arglist = configmap["args"]
                runcmd = compiler + " " + sourcefilepath
                runcmd = add_arg_to_runcmd(runcmd,arglist)

            else:
                runcmd = compiler + " " + sourcefilepath

        # java programs need "javac" to compile and "java" to run program. This works best if you are
        # in current directory where source file exists.
        elif compiler_type == "java":
            buildcmd = compiler + " " + sourcefilepath + "\n"
            java_codedir=os.path.dirname(sourcefilepath)
            filename = os.path.basename(os.path.splitext(sourcefilepath)[0])
            # need to be directory where java files reside
            runcmd = "cd " + java_codedir + "\n"
            runcmd += "java " + filename + "\n"
            # would like to remove .class files that are generated due to javac
            runcmd += "rm -v " + filename + ".class"

        # if inputfile key is found, add this as part of runcmd
        if "inputfile" in configmap:
            runcmd += " < " + os.path.join(codedir,configmap["inputfile"])
        # if output of program needs to be written to file instead of STDOUT
        if "outputfile" in configmap:
            runcmd +=  " > " + configmap["outputfile"]

        if "threadrange" in configmap:
            fd.write(openmp_env_str)


        fd.write(buildcmd)
        fd.write(runcmd)

        # runextracmd is used when you want buildtest to generate compilation and execution step
        # automatically but need to add extra commands after execution.
        if "runextracmd" in configmap:
            for cmd in configmap["runextracmd"]:
                fd.write(cmd + "\n")

            logger.debug("runextracmd found in YAML config file")
            logger.debug("runextracmd: %s", str(configmap["runextracmd"]))

        fd.close()

    if BUILDTEST_ENABLE_JOB:
        if "scheduler" in configmap:
            generate_job_by_config(testpath,shell_type, configmap)
        else:
            # generate job script based on template, if "scheduler" found in
            # then module below will do nothing and taken care off by
            # generate_job_by_config
            generate_job(testpath,shell_type,BUILDTEST_JOB_TEMPLATE,configmap)


    # by default run the commands below which will add the test to CMakeLists.txt and update the logfile
    if "iter" not in configmap:
        add_test_to_CMakeLists(app_destdir,subdir,cmakelist,testname)

        logger.debug("Creating Test: %s ", testpath)
        logger.debug("[TEST START-BLOCK]")

        fd=open(testpath,'r')
        content=fd.read().splitlines()
        for line in content:
            logger.debug(line)

        fd.close()

        logger.debug("[TEST END-BLOCK]")


    if "procrange" in configmap:
        create_procrange_test(testpath,startproc,mpi_proc_list,subdir)
    if "threadrange" in configmap:
        create_threadrange_test(testpath,startthread,thread_list,subdir)

    # if keyword iter is found in YAML, lets try to recreate N tests by renaming test such as
    # hello.sh to hello_1.sh and create N-1 copies with file names hello_2.sh, hello_3.sh, ...
    if  "iter" in configmap:
        filename=os.path.basename(os.path.splitext(sourcefilepath)[0])
        testname = filename + "_1." + shell_type
        testpath_testname = os.path.join(destdir,testname).replace("\n",'')
        os.rename(testpath,testpath_testname)
        out = "Rename Iteration Test: " +  testpath +  " -> " +  testpath_testname
        logger.debug("%s",out)
        # writing test to CMakeLists.txt
        add_test_to_CMakeLists(app_destdir,subdir,cmakelist,testname)
        logger.debug("Content of Test file: %s", testpath_testname)
        logger.debug("[START TEST-BLOCK]")

        fd=open(testpath_testname,'r')
        content=fd.read()
        logger.debug("%s",content)
        fd.close()
        logger.debug("[END TEST-BLOCK]")

        numiter = int(configmap["iter"])
        logger.debug("Making %s copy of test: %s", numiter, testpath_testname)
        # creating N-1 copies of tests
        for index in range(1,numiter):
            testname=filename+"_"+str(index+1)+"." + shell_type
            src_testpath=testpath_testname
            dest_testpathname=os.path.join(destdir,testname).replace('\n','')
            copyfile(src_testpath,dest_testpathname)
            # setting perm to 755 on testscript
            os.chmod(dest_testpathname, stat.S_IRWXU |  stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH |  stat.S_IXOTH)
            out = "Iteration Test: " + dest_testpathname
            logger.info("%s",out)
            logger.debug("Adding test: %s to CMakeList", testname)
            add_test_to_CMakeLists(app_destdir,subdir,cmakelist,testname)

def create_procrange_test(testpath, startproc, proc_list,subdir):
    """ create same mpi tests with varying parameter for -np """
    destdir = os.path.dirname(testpath)
    cmakelist = os.path.join(destdir,"CMakeLists.txt")
    ext = os.path.splitext(testpath)[1]
    fd=open(testpath,'r')
    content = fd.read()
    fd.close()
    os.chdir(destdir)

    for proc in proc_list:
        newtestname = os.path.basename(testpath).rsplit("_",1)[0]
        if proc == startproc:
            continue

        newtestname += "_" + str(proc) + ext
        # replace mpirun -np with value of proc
        ret = re.sub("mpirun -np " + str(startproc), "mpirun -np " + str(proc) + " " ,content)
        fd = open(newtestname,'w')
        fd.write(ret)
        fd.close()
        # setting perm to 755 on testscript
        os.chmod(newtestname, stat.S_IRWXU |  stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH |  stat.S_IXOTH)
        add_test_to_CMakeLists(destdir,subdir,cmakelist,newtestname)

def create_threadrange_test(testpath,startthread,thread_list,subdir):
    """ create a range of OpenMP thread test """
    """ create same mpi tests with varying parameter for -np """
    destdir = os.path.dirname(testpath)
    cmakelist = os.path.join(destdir,"CMakeLists.txt")
    ext = os.path.splitext(testpath)[1]
    fd=open(testpath,'r')
    content = fd.read()
    fd.close()
    os.chdir(destdir)

    for thread in thread_list:
        ret = ""
        # replace threadcnt for each testname <testname>_nthread_<threadcnt>.<shell_ext>
        newtestname = os.path.basename(testpath).rsplit("_",1)[0]
        if thread == startthread:
            continue

        newtestname += "_" + str(thread) + ext
        # change value of OMP_NUM_THREAD in loop depending on type of shell
        if ext == ".bash" or ext == ".sh":
            ret = re.sub("export OMP_NUM_THREADS=" + str(startthread), "export OMP_NUM_THREADS=" + str(thread)  ,content)
        else:
            ret = re.sub("setenv OMP_NUM_THREADS " + str(startthread), "setenv OMP_NUM_THREADS " + str(thread)  ,content)

        fd = open(newtestname,'w')
        fd.write(ret)
        fd.close()
        # setting perm to 755 on testscript
        os.chmod(newtestname, stat.S_IRWXU |  stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH |  stat.S_IXOTH)
        add_test_to_CMakeLists(destdir,subdir,cmakelist,newtestname)

def get_environment_variable(shell,key, value):
    """ return environment variable for setting OpenMP threads as a string based on shell type """
    if shell == "sh" or shell == "bash":
        return "export " + key + "=" +  str(value) + "\n"
    elif shell == "csh":
        return "setenv " + key + " " +  str(value) + "\n"
