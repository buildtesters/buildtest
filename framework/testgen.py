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
This python module generates the binary & source test by processing all yaml 
files and create .sh scripts along with the CMakeLists configuration. There
is only 1 binary yaml file that can generate multiple binary test, while 
source test has 1 YAML file and generates only 1 test

:author: Shahzeb Siddiqui (Pfizer)
"""
from framework.env import *
from framework.tools.generic import *
from framework.tools.cmake import *
from framework.tools.file import *
from framework.tools.software import *
from framework.parser.args import *

import os.path 
import os, sys
import shutil
import yaml
import logging
from shutil import copyfile

def generate_binary_test(args_dict,verbose,pkg):
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

	software=get_arg_software(args_dict)
	system=get_arg_system(args_dict)

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
		create_dir(BUILDTEST_TESTDIR,verbose)

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
	process_binary_file(commandfile,args_dict,test_type,verbose,pkg)

	
# generate test for source
def generate_source_test(configmap,codedir,verbose,subdir):
	"""
	This function generates the tests that requires compilation for EB apps. The
	tests are written <software>/<version>/<toolchain-name>/<toolchain-version>.
	The test script is named according to "name" key tag with the extension ".sh"
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
	# app_destdir is root of test directory
	app_destdir = os.path.join(BUILDTEST_TESTDIR,"ebapp",appname,appver,tcname,tcver)

	# destdir is where test script and CMakeLists.txt will be generated. 
	# If there is a subdirectory then testscript will reside in subdir
	destdir=os.path.join(app_destdir,subdir)
	cmakelist=os.path.join(destdir,"CMakeLists.txt")
	
	# if subdirectory exists, create subdirectory in destdir so we can write test script
	if subdir != "":
		# if sub directory does not exist, then create all directories and its parents directories
		if os.path.exists(destdir) == False:
			os.makedirs(destdir)

	# testname is key value "name" with .sh extension
	testname=configmap["name"]+".sh"
	testpath=os.path.join(destdir,testname)
	sourcefilepath=os.path.join(codedir,configmap["source"])
	# name of the executable is the value of source tag with ".exe" extension
	executable=configmap["source"]+".exe"

	flags=""
	# if buildopts key exists in dictionary, then add flags to compilation step (buildcmd)
	if "buildopts" in configmap:
		flags=configmap["buildopts"]

        logger.debug("Test Name: %s", testname)
	logger.debug("Test Path: %s", testpath)
	logger.debug("Source File: %s", sourcefilepath)
        logger.debug("Executable Name: %s",  executable)
        logger.debug("Build Flags: %s",  flags)


	# write the preamble to test-script to initialize app environment using module cmds
	fd=open(testpath,'w')
	header=load_modules()
	fd.write(header)
	
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
			print msg
			logger.debug.append("%s",msg)
			logging.warning("Unable to create test from YAML config, skipping test generation")
			return

		
		fd.write(buildcmd)
	        fd.write(runcmd)

			
	# otherwise generate the buildcmd and runcmd automatically
	else:
		
		# checking if either buildcmd or runcmd specified but not both, then report an error.
		if "buildcmd" in configmap and "runcmd" not in configmap or "buildcmd" not in configmap and "runcmd" in configmap:
			print "Need to specify both key: buildcmd and runcmd"
			
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
					logger.debug("nproc: ", nproc)
				# if nproc is not specified set it to 1 when building mpi apps
				else:		
					nproc = "1"

					logger.debug("nproc key not found in YAML config file, will set nproc = 1")
				# add argument to runcmd in MPI jobs
                                if "args" in configmap:
                                        arglist = configmap["args"]
	                		runcmd = "mpirun -np " + nproc + " ./" + executable
					runcmd = add_arg_to_runcmd(runcmd,arglist)
				else:
	                		runcmd = "mpirun -np " + nproc + " ./" + executable
	                else:
				# add argument to runcmd in general jobs
				if "args" in configmap:
					arglist = configmap["args"]
					runcmd = "./" + executable 
					runcmd = add_arg_to_runcmd(runcmd,arglist)
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

    	# by default run the commands below which will add the test to CMakeLists.txt and update the logfile
        if "iter" not in configmap:
        	add_test_to_CMakeLists(app_destdir,subdir,cmakelist,testname)

	        # print "Creating Test: " + testpath

	        logger.debug("Creating Test: %s ", testpath)
	        logger.debug("[TEST START-BLOCK]")

                fd=open(testpath,'r')
                content=fd.read().splitlines()
		for line in content:
			logger.debug(line)
                fd.close()

	        logger.debug("[TEST END-BLOCK]")


	# if keyword iter is found in YAML, lets try to recreate N tests by renaming test such as
	# hello.sh to hello_1.sh and create N-1 copies with file names hello_2.sh, hello_3.sh, ...
	if  "iter" in configmap:
		filename=os.path.basename(os.path.splitext(sourcefilepath)[0])
		testname = filename + "_1.sh"  
		testpath_testname = os.path.join(destdir,testname).replace("\n",'')
		os.rename(testpath,testpath_testname)
		out = "Rename Iteration Test: " +  testpath +  " -> " +  testpath_testname
		print out
		logger.debug("%s",out)
		# writing test to CMakeLists.txt
		add_test_to_CMakeLists(app_destdir,subdir,cmakelist,testname)
		logger.debug("Content of Test file: ", testpath_testname)
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
			testname=filename+"_"+str(index+1)+".sh"
			src_testpath=testpath_testname
			dest_testpathname=os.path.join(destdir,testname).replace('\n','')
			copyfile(src_testpath,dest_testpathname)
			out = "Iteration Test: " + dest_testpathname 
			print out
			logger.debug("Adding test: %s to CMakeList", testname)
			add_test_to_CMakeLists(app_destdir,subdir,cmakelist,testname)
    
	
def get_compiler(configmap,appname,tcname):
	"""
	 This function gets the appropriate compiler tag and compiler type based on the 
	 application/toolchain + file extension. Compiler/Wrappers can be 
	 gcc,icc,mpicc,nvcc,javac,python,R,perl,etc...
	 """

	# if app is GCC, GCCcore, -> compiler = gcc
	# if app toolchain is GCC, GCCcore, dummy -> compiler = gcc
	# if app is intel -> compiler = icc/mpiicc -> need tag: mpi=enabled
	# if app is python, tc=X -> compiler = python
	# if app is OpenMPI,MPICH,MVAPICH, tc=X -> compiler = mpicc
	# if app is CUDA, tc=X -> compiler = nvcc
	# if app is X, tc=gcccuda, compiler = gcc/nvcc need tag: cuda=enabled

	# if cuda enabled in YAML
	cuda = ""
	# if mpi is enabled in YAML
	mpi = ""
	if "cuda" in configmap:
		cuda=configmap["cuda"]
	if "mpi" in configmap:
		mpi=configmap["mpi"]

        # get extension for source file 
        ext = os.path.splitext(configmap["source"])[1] 
        compiler="" 

	# compiler_type valid may be "gnu, intel, mpi, intel-mpi, R, java, python"
	compiler_type=""

	# condition to calculate compiler_type based on toolchain
	if tcname in ["GCC","GCCcore","gcccuda","dummy","gompi", "foss","goolfc"]:
		compiler_type="gnu"
	if tcname in ["intel", "iccifort","iccifortcuda","impi","iimpi","iimpic"]: 
		compiler_type="intel"
	
	# if application is intel then compiler_type will be intel
	if appname in ["intel"]:
		compiler_type="intel"

	if appname in ["Java"]:
		compiler = "javac"
		compiler_type = "java"
		return compiler,compiler_type
	if appname in ["CUDA"]:
		compiler = "nvcc"
		compiler_type = "cuda"
		return compiler,compiler_type

	# MPI apps built with any toolchain (intel, gcc, pgi) will default to gnu. This is because all of these apps provide
 	# mpicc, mpifort, mpic++. While intel mpi provides mpiicc, mpiifort, mpiic++
	if appname in ["MPICH","OpenMPI","MVAPICH"]:
		compiler_type="gnu"
	
	
	# determine compiler based on compiler_type and its file extension
	
	# perl extension
	if ext == ".py":
		compiler_type = "python"
		compiler = "python "
		return compiler,compiler_type
	if ext == ".pl":
		compiler_type = "perl"
		compiler = "perl"
		return compiler,compiler_type
	if ext == ".R":
		compiler_type = "R"
		compiler = "Rscript "
		return compiler,compiler_type
	# C extension
	if ext == ".c":
		if compiler_type == "gnu":
			# set compiler to nvcc when cuda is enabled
			if cuda == "enabled":
				compiler="nvcc"
			# set compiler to mpicc when mpi is enabled
			elif mpi == "enabled":
				compiler="mpicc"
			else:
				compiler="gcc"
		elif compiler_type == "intel":
			# mpi test in intel test needs a check for mpi=enabled field to determine which wrapper to use 
			if mpi=="enabled":
				compiler="mpiicc"
			else:
				compiler="icc"
	# C++ extension
	elif ext == ".cpp":
		if compiler_type == "gnu":
			# set compiler to nvcc when cuda is enabled
			if cuda == "enabled": 
                                compiler="nvcc"
                        # set compiler to mpicc when mpi is enabled
                        elif mpi == "enabled":
                                compiler="mpic++"
			else:
				compiler="g++"
		elif compiler_type == "intel":
			if mpi=="enabled":
				compiler="mpiic++"
			else:
				compiler="icpc"
	# Fortran extension
	elif ext == ".f90" or ext == ".f" or ext == ".f77":
		if compiler_type == "gnu":
			# set compiler to nvcc when cuda is enabled
                        if cuda == "enabled":
                                compiler="nvcc"
                        # set compiler to mpicc when mpi is enabled
                        elif mpi == "enabled":
                                compiler="mpifort"
			else:
				compiler="gfortran"
		elif compiler_type == "intel":
			if mpi=="enabled":
				compiler="mpiifort"
			else:
				compiler="ifort"

	return compiler,compiler_type

def process_binary_file(filename,args_dict,test_type,verbose,pkg):
	"""
	Module responsible for actually creating the test scripts for binary tests along
	with CMakeLists.txt in subdirectories under $BUILDTEST_TESTDIR. This module
	is used for generating binary tests for both system and ebapps tests.
	"""

	logger = logging.getLogger(logID)

	if test_type == "software":

 		name = get_appname()
		version = get_appversion()
	        toolchain_name = get_toolchain_name()
        	toolchain_version = get_toolchain_version()

		test_destdir,test_destdir_cmakelist = setup_software_cmake(args_dict)	

 	       # load preamble for test-script that initializes environment.
        	header=load_modules()

	else:
		system=get_arg_system(args_dict)
		
		test_destdir,test_destdir_cmakelist = setup_system_cmake(args_dict,pkg)	


	
	logger.info("Reading File: %s", filename)
	fd=open(filename,'r')
	content=yaml.load(fd)
	logger.debug("Loading YAML content")
	# if key binaries is not in yaml file, exit program
	if "binaries" not in content:
		logger.error("Can't find key: binaries in file %s", filename)
		sys.exit(1)

	# create a binary test script for each key,value item in dictionary
	binarydict=content["binaries"]
	# keep track of number of binary test
	count = 0

	for key in binarydict:
		count = count + 1
		name_str=key.replace(" ","_")
		testname=name_str+".sh"
		testpath=os.path.join(test_destdir,testname)

		logger.debug("Creating and Opening  test file: %s for writing ",  testpath)
		fd=open(testpath,'w')
		
		if test_type == "software":
			fd.write(header)
		else:
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
				add_test_str="add_test(NAME " + name + "-" + version + "-" + testname + "\t COMMAND sh " + testname + "\t WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}) \n"
			else:
				add_test_str="add_test(NAME " + name + "-" + version + "-" + toolchain_name + "-" + toolchain_version + "-" + testname + "\t COMMAND sh " + testname + "\t WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}) \n"
		else:
			add_test_str="add_test(NAME system-" + pkg + "-" + testname + "\t COMMAND sh " + testname + "\t WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}) \n"

		
		logger.debug("Adding content: %s ",  add_test_str)
		fd.write(add_test_str)

		# print "Creating Test:", testpath

	print
	if test_type == "system":
		print "Generating " + str(count) + " binary tests for package: " + pkg
	else:
		print "Generating " + str(count) + " binary tests for Application: " + name + "/" + version

	print "Binary Tests are written in " + test_destdir
	
			
