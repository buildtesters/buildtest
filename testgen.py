############################################################################ 
# 
#  Copyright 2017 
# 
#   https://github.com/shahzebsiddiqui/BuildTest 
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

from setup import *
from utilities import *
import os.path 
import os, sys
import shutil
import yaml

def systempkg_generate_binary_test(pkg,verbose,logdir):
	"""
	This function generates the binary test for system packages by processing 
	command.yaml. We make sure command.yaml exists and CMakeLists.txt is present
	in each subdirectory in BUILDTEST_TESTDIR. If CMakeLists.txt is not present, we 
	create the file and add the content "add_subdirectory(<dirname>) according to
	which directory you want ctest to process
 	
	"""
	toplevel_cmakelist_file=os.path.join(BUILDTEST_ROOT,"CMakeLists.txt")
	testingdir_cmakelist_file=os.path.join(BUILDTEST_TESTDIR,"CMakeLists.txt")
	commandfile=os.path.join(BUILDTEST_SOURCEDIR,"system",pkg,"command.yaml")

        logcontent = ""
        logcontent += "---------------------------------------------- \n "
        logcontent += "function: systempkg_generate_binary_test \n"
        logcontent += "---------------------------------------------- \n "

        # if CMakeLists.txt does not exist in top-level directory, create the header
        if os.path.isfile(toplevel_cmakelist_file) == False:
                logcontent += "File: " + toplevel_cmakelist_file + " was not found, build test will create it \n"
                init_CMakeList(toplevel_cmakelist_file)

        logcontent += "Creating Directory " + BUILDTEST_TESTDIR + "\n"
        create_dir(BUILDTEST_TESTDIR,verbose)

        # if BUILDTEST_TESTDIR/CMakeLists.txt does not exist, then create it
        if os.path.isfile(testingdir_cmakelist_file) == False:
	        logcontent += "File: " + testingdir_cmakelist + " was not found, build test will create it \n"
                fd=open(testingdir_cmakelist_file,'w')
                fd.close()
        # if command.yaml does not exist then report warning and skip to next test.
        if os.path.isfile(commandfile) == False:
                print "Warning: Cannot find command file:", commandfile, "Skipping binary test"
		logcontent += "Warning: Cannot find command file:" + commandfile + "Skipping binary test"
        else:
            logcontent += systempkg_process_binary_file(commandfile,pkg,verbose,logdir)

	return logcontent
def generate_binary_test(software,toolchain,configdir,verbose,logdir):
	"""
	This function operates similar to systempkg_generate_binary_test except this function
	is used only for ebapps that are present as modules. This is because ebapps names are 
	different then systempkg names for instance "gcc" "gcc-gfortran" "gcc-c++" are package 
	names in RHEL that test binaries for gcc, gfortran, g++. In EB there is a single app GCC
	that provides gcc, gfortran, g++. This function makes sure command.yaml exists and CMakeLists.txt
	is present in all subdirectories in BUILDTEST_TESTDIR
	"""
	toplevel_cmakelist_file=os.path.join(BUILDTEST_ROOT,"CMakeLists.txt")
	testingdir_cmakelist_file=os.path.join(BUILDTEST_TESTDIR,"CMakeLists.txt")
	swname = software[0]
	commandfile=os.path.join(configdir,"command.yaml")

	logcontent = ""
	logcontent += "--------------------------------- \n "
	logcontent += "function: generate_binary_test \n"
	logcontent += "--------------------------------- \n "
	# if CMakeLists.txt does not exist in top-level directory, create the header
	if os.path.isfile(toplevel_cmakelist_file) == False:
		logcontent += "File: " + toplevel_cmakelist_file + " was not found, build test will create it \n"
		init_CMakeList(toplevel_cmakelist_file)

	logcontent += "Creating Directory " + BUILDTEST_TESTDIR + "\n"
	create_dir(BUILDTEST_TESTDIR,verbose)

	# if BUILDTEST_TESTDIR/CMakeLists.txt does not exist, then create it
	if os.path.isfile(testingdir_cmakelist_file) == False:
		logcontent += "File: " + testingdir_cmakelist_file + " was not found, build test will create it \n"
		fd=open(testingdir_cmakelist_file,'w')
		fd.close()
	# if command.yaml does not exist then report error
	if os.path.isfile(commandfile) == False:
		print "Warning: Cannot find command file:", commandfile, "Skipping binary test"
		logcontent += "Warning: Cannot find command file:" + commandfile + "Skipping binary test"
	else:
	    logcontent += process_binary_file(commandfile,software,toolchain,verbose,logdir)

	return logcontent
# generate test for source
def generate_source_test(software,toolchain,configmap,codedir,verbose,subdir,logdir):
	"""
	This function generates the tests that requires compilation for EB apps. The
	tests are written <software>/<version>/<toolchain-name>/<toolchain-version>.
	The test script is named according to "name" key tag with the extension ".sh"
	CMakeLists.txt has an entry for each test that executes the shell-script. Most
	test requires a compilation step, while every test requires a execution stage. 
	This is done via buildcmd and runcmd tags in YAML for explicit builds. buildtest
	will try to generate this automatically if nothing is provided. 
	"""
	
	appname=software[0]
	appver=software[1]
	tcname=toolchain[0]
	tcver=toolchain[1]
	
	# app_destdir is root of test directory
	app_destdir = os.path.join(BUILDTEST_TESTDIR,"ebapp",appname,appver,tcname,tcver)

	# destdir is where test script and CMakeLists.txt will be generated. 
	# If there is a subdirectory then testscript will reside in subdir
	destdir=os.path.join(app_destdir,subdir)
	cmakelist=os.path.join(destdir,"CMakeLists.txt")
	
	logcontent = ""
	logcontent += "------------------------------------------------ \n"
	logcontent += "function: generate_source_test \n"
	logcontent += "------------------------------------------------ \n"

	# if subdirectory exists, create subdirectory in destdir so we can write test script
	if subdir != "":
		os.mkdir(destdir)

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

        logcontent += "Test Name: " +  testname + "\n"
	logcontent += "Test Path: " + testpath + "\n"
        logcontent += "Source File: " + sourcefilepath + "\n"
        logcontent += "Executable Name: " +  executable + "\n"
        logcontent += "Build Flags: " +  flags + "\n"


	# write the preamble to test-script to initialize app environment using module cmds
	fd=open(testpath,'w')
	header=load_modules(software,toolchain)
	fd.write(header)
	
	# string used for generating the compilation step
	buildcmd=""
	# string used for running the executable and used for injecting commands at pre/post test
	runcmd=""
	# string to decide the compiler wrapper to use based on application and file extension
	compiler=""
	# used for parallel processing to specify # of procs with mpirun -np 
	nproc = ""

        # if there is a buildcmd & runcmd in yaml file, place this directly in test script
        if "buildcmd" in configmap and "runcmd" in configmap:

		logcontent += "YAML file found buildcmd and runcmd. \n"
		logcontent += "buildtest will generate explicit build/run commands from buildcmd and runcmd fields \n"	

		# only process buildcmd if there is a value specified for buildcmd key
		if configmap["buildcmd"] != None:
			# for each element from dictionary configmap["buildcmd"], write
			# each instruction in buildcmd separated by newline 
			for cmd in configmap["buildcmd"]:
		                buildcmd += cmd + "\n"
		else:
			print "buildcmd is declared but value is not specified"

			logcontent+="buildcmd is declared but value is not specified \n"

		if configmap["runcmd"] != None:
			# process the runcmd tag similar same as buildcmd and store in variable
			# runcmd except if no value is specified for runcmd in YAML then throw 
			# an error
			for cmd in configmap["runcmd"]:
				runcmd += cmd + "\n"
		else:
			print "runcmd is declared but value is not specified"

			logcontent+="runcmd is declared, but value is not specified. Need to run executable \n"
			logcontent+="Program Terminating"
			update_logfile(logdir,logcontent,verbose)
			sys.exit(1)

		
		if verbose >=1:
			print testpath,":Invoking YAML buildcmd and runcmd fields..."
			print "-----------------------------------"
			print "BUILDCMD:"
			print buildcmd
			print "-----------------------------------"
			print "RUNCMD:"
			print runcmd
			print "-----------------------------------"
			
			logcontent += "Invoking YAML buildcmd and runcmd fields \n"
			logcontent += "buildcmd: \n "
			logcontent += buildcmd 
			logcontent += "runcmd: \n"
			logcontent += runcmd
	        
		fd.write(buildcmd)
	        fd.write(runcmd)

			
	# otherwise generate the buildcmd and runcmd automatically
	else:
		
		# checking if either buildcmd or runcmd specified but not both, then report an error.
		if "buildcmd" in configmap and "runcmd" not in configmap or "buildcmd" not in configmap and "runcmd" in configmap:
			print "Need to specify both key: buildcmd and runcmd"
			
			logcontent += "Need to declare both key: buildcmd and runcmd \n"
			logcontent += "Program Terminating \n"	
			update_logfile(logdir,logfile,verbose)
			sys.exit(1)

		# get the compiler tag and type based on application and toolchain
	        compiler,compiler_type=get_compiler(configmap,appname,tcname)
 
		logcontent += "buildtest will auto-generate buildcmd & runcmd \n" 
		logcontent += "Compiler: "+ compiler + "\n"
		logcontent += "Compiler Type: " + compiler_type + "\n"

		# set buildcmd based on compiler_type. compiler is either nvcc,gcc,icc,mpicc, or mpiicc for intel
	        if compiler_type == "gnu" or compiler_type == "intel" or compiler_type == "cuda":

	        	buildcmd = compiler + " -o " + executable + " " + sourcefilepath + " " + flags + "\n"

	                # set runcmd for mpi tags using mpirun otherwise just run executable 
	                if compiler in ["mpicc","mpic++","mpifort","mpiicc","mpiic++", "mpiifort"]:
	
		                # if nproc is defined in yaml, store value in nproc which will use it in mpirun command
        		        if configmap["nproc"]:
                		        nproc = str(configmap["nproc"])
					
					logcontent += "nproc key found in YAML config file \n"
					logcontent += "nproc: " + nproc + "\n" 
				# if nproc is not specified set it to 1 when building mpi apps
				else:		
					nproc = "1"

					logcontent += "nproc key not found in YAML config file, will set nproc = 1 \n"

	                	runcmd = "mpirun -np " + nproc + " ./" + executable + "\n"
	                else:
				runcmd = "./" + executable + "\n"

		# python scripts have no compilation, just run python script. So we just need to update runcmd string
		elif compiler_type == "python":
			runcmd = "python " + sourcefilepath + "\n"
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

		if verbose >=1:
			print testpath,":Invoking automatic buildcmd and runcmd fields..."
			print "-----------------------------------"
			print "BUILDCMD:",buildcmd
			print "RUNCMD:",runcmd
			print "-----------------------------------"
		
			logcontent += "Invoking Automatic buildcmd & runcmd fields \n"
			logcontent += "buildcmd: \n"
			logcontent += buildcmd
			logcontent += "runcmd: \n"
			logcontent += runcmd

		fd.write(buildcmd)
		fd.write(runcmd)
		
		# runextracmd is used when you want buildtest to generate compilation and execution step
		# automatically but need to add extra commands after execution. 
		if "runextracmd" in configmap:
			for cmd in configmap["runextracmd"]:
				fd.write(cmd + "\n")

			logcontent+= "runextracmd found in YAML config file \n"
			logcontent+= "runextracmd:" + str(configmap["runextracmd"]) + "\n"
	fd.close()

	# if YAML files are in subdirectory of config directory then update CMakeList
	# in app_destdir to add tag "add_subdirectory" for subdirectory so CMakeList
	# can find tests in subdirectory
	fd=open(cmakelist,'a')

	if subdir != "":
		parent_cmakelist = os.path.join(app_destdir,"CMakeLists.txt")
		fd1=open(parent_cmakelist,'a')
		cmake_content="add_subdirectory("+subdir+") \n"
		fd1.write(cmake_content)
		fd1.close()
			
		logcontent+="writing content: " + cmake_content + " to file " + parent_cmakelist + "\n"

		# the string add_test allows you to test script with ctest. The NAME tag is 
		# <name>-<version>-<toolchain-name>-<toolchain-version>-<subdir>-<testname>. This
		# naming scheme should allow buildtest to reuse same YAML configs for multiple version
		# built with any toolchains. Subdirectories come in handy when you have large number 
		# of tests that can cause name conflict, so this is resolved by storing YAML files and generated
		# test scripts in subdirectories
		add_test_str="add_test(NAME " + appname + "-" + appver + "-" + tcname + "-" + tcver + "-"  + subdir + "-" + testname + "\t COMMAND sh " +  testname + "\t WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}) \n"
	else:
		# for tests not present in subdirectory then subdir is removed from NAME tag in add_test CMAKE command
		add_test_str="add_test(NAME " + appname + "-" + appver + "-" + tcname + "-" + tcver + "-"  + testname + "\t COMMAND sh " + testname + "\t WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}) \n"

		logcontent+= "Updating File " + cmakelist + " with: " + add_test_str + "\n"

	fd.write(add_test_str)
	fd.close()

	print " Creating Test: " + testpath

	logcontent += " Creating Test: " + testpath + "\n"
	logcontent += "Content of Testfile: " + testpath + "\n"
	logcontent += "-------------------------------------------------- \n"
	
	fd=open(testpath,'r')
	content=fd.read()
	logcontent+=content
	fd.close()


	logcontent += "-------------------------------------------------- \n"
	return logcontent
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

	# compiler can be determined automatically for apps below
	if appname in ["Anaconda2", "Anaconda3", "Python", "Python3"]:
		compiler = "python"
		compiler_type = "python"
		return compiler,compiler_type
	if appname in ["R"]:
		compiler = "R"
		compiler_type = "R"
		return compiler,compiler_type
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

def systempkg_process_binary_file(filename,pkg,verbose,logdir):
	"""
	This function does the work in writing the test scripts from command.yaml
	for system package tests. CMakeLists.txt is updated for each sub directory
	"""

	logcontent = ""
	logcontent += "--------------------------------------- \n"
	logcontent += " function: systempkg_process_binary_file \n"
	logcontent += "--------------------------------------- \n"

	# top level system directory and system package directory
	test_system_dir=os.path.join(BUILDTEST_TESTDIR,"system")
	test_destdir=os.path.join(BUILDTEST_TESTDIR,"system",pkg)

	# top level CMakeLists.txt in testing directory
	test_cmakelist = os.path.join(BUILDTEST_TESTDIR,"CMakeLists.txt")

	# CMakeLists.txt that contains all system package directories to process
	test_cmakelist_pkg = os.path.join(BUILDTEST_TESTDIR,"system","CMakeLists.txt")

	# CMakeLists.txt that contais the actual tests (add_test)
	test_cmakelist_destdir=os.path.join(test_destdir,"CMakeLists.txt")

	logcontent += " Variables Assignments \n"
	logcontent += "test_system_dir = " + test_system_dir + "\n"
	logcontent += "test_destdir = " + test_destdir + "\n"
	logcontent += "test_cmakelist = " + test_cmakelist + "\n"
	logcontent += "test_cmakelist_pkg = " + test_cmakelist_pkg + "\n"
	logcontent += "test_cmakelist_destdir = " + test_cmakelist_destdir + "\n"
	logcontent += "\n"

        # if testdirectory exist, delete and recreate it inorder for reproducible test builds
        if os.path.isdir(test_destdir):
                shutil.rmtree(test_destdir)
		logcontent += "removing directory " + test_destdir + "\n"

	# create the directories if they don't exist
	logcontent += "Creating directory: " + test_system_dir + "\n"
	create_dir(test_system_dir,verbose)
	logcontent += "Creating directory: " + test_destdir + "\n"
	create_dir(test_destdir,verbose)



	logcontent += "Creating CMakeLists.txt File: " + test_cmakelist + "\n"
	# create CMakeLists.txt files if they are not present
	create_file(test_cmakelist,verbose)

	logcontent += "Creating CMakeLists.txt File: " + test_cmakelist_pkg + "\n"
	create_file(test_cmakelist_pkg,verbose)

	logcontent += "Creating CMakeLists.txt File: " + test_cmakelist_destdir + "\n"
	create_file(test_cmakelist_destdir,verbose)

	# update the CMakeLists.txt with the tag add_subdirectory(system) 
	logcontent += "Updating " + test_cmakelist + " with add_subdirectory(system) \n"
        update_CMakeLists(test_cmakelist,"system",verbose)

	logcontent += "Updating " + test_cmakelist_pkg + " with add_subdirectory("+pkg+") \n"
	# update CMakeLists.txt with the tag add_subdirectory(pkg) where pkg is the application name
        update_CMakeLists(test_cmakelist_pkg,pkg,verbose)

	logcontent += "\n"
	logcontent += "Reading File: " + filename + "\n"

	# open command.yaml and load the YAML content in variable content 
	fd=open(filename,'r')
        content=yaml.load(fd)
	logcontent += "Loading YAML content \n"

        # if key binaries is not in yaml file, exit program
        if "binaries" not in content:
                print "Cant find key binaries in file: ", filename, " Exiting program"
                logcontent += "Cant find key binaries in file: " + filename  + "\n"
		logcontent += "Exiting program \n"
		update_logfile(logdir,logcontent,verbose)
                sys.exit(1)

        # create a binary test script for each key,value item in dictionary
        binarydict=content["binaries"]
        for key in binarydict:
                testname=key+".sh"
                testpath=os.path.join(test_destdir,testname)
		logcontent += "Creating test file: " +  testpath + "\n"
                fd=open(testpath,'w')
		fd.write("#!/bin/sh \n")
		fd.write("module purge \n" )
                # if paramter is specified then write both executable and parameter to file otherwise only write the executable
                if binarydict[key]:
                        fd.write(key + " " + binarydict[key])
                else:
                        fd.write(key)
                fd.close()

		# reading test script for writing content of test in logcontent 
		fd=open(testpath,'r')
		content=fd.read()
		fd.close()
		logcontent += "Content of test file: " + testpath + "\n"
		logcontent += "----------------------------------------------------- \n"
		logcontent += content +"\n"
		logcontent += "----------------------------------------------------- \n"
		
		# append the test in CMakeLists.txt
                fd=open(test_cmakelist_destdir,'a')
                add_test_str="add_test(NAME system-" + pkg + "-" + testname + "\t COMMAND sh " + testname + "\t WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}) \n"
                fd.write(add_test_str)

		logcontent += "Updating CMakeLists: " + test_cmakelist_destdir + " with content: "+ add_test_str 

                print "Creating Test:", testpath
		logcontent += "Creating Test:" + testpath + "\n"

	return logcontent
def process_binary_file(filename,software,toolchain,verbose,logdir):
	"""
	does the same operation as systempkg_process_binary_file but for ebapps. There are extra 
	subdirectories that are created that implies multiple CMakeLists.txt files for each sub directory
	"""
	name,version=software
	toolchain_name,toolchain_version=toolchain
	
	logcontent = ""
	logcontent += "--------------------------------------- \n"
	logcontent += " function: process_binary_file \n"
	logcontent += "--------------------------------------- \n"

	# if top level software directory is not present, create it
	test_ebapp_dir=os.path.join(BUILDTEST_TESTDIR,"ebapp")

	# variables to reference each subdirectory in <software>/<version>/<toolchain-name>/<toolchain-version>
	test_name_dir=os.path.join(test_ebapp_dir,name)
	test_version_dir=os.path.join(test_name_dir,version)
	test_toolchain_name_dir=os.path.join(test_version_dir,toolchain_name)
	test_toolchain_version_dir=os.path.join(test_toolchain_name_dir,toolchain_version)

	# BUILDTEST_TESTDIR/CMakeLists.txt
	test_cmakelist = os.path.join(BUILDTEST_TESTDIR,"CMakeLists.txt")

	# BUILDTEST_TESTDIR/ebapps/CMakeLists.txt
	test_ebapp_cmakelist = os.path.join(test_ebapp_dir,"CMakeLists.txt")
	
	# CMakeLists.txt files in <software>/<version>/<toolchain-name>/<toolchain-version>
	test_name_cmakelist = os.path.join(test_name_dir,"CMakeLists.txt")
	test_version_cmakelist = os.path.join(test_version_dir,"CMakeLists.txt")
	test_toolchain_name_cmakelist = os.path.join(test_toolchain_name_dir,"CMakeLists.txt")
	test_toolchain_version_cmakelist = os.path.join(test_toolchain_version_dir,"CMakeLists.txt")

	test_destdir=test_toolchain_version_dir

	logcontent += " Variables Assignments \n"
	logcontent += "test_ebapp_dir = " + test_ebapp_dir + "\n"
	logcontent += "test_name_dir = " + test_name_dir + "\n"
	logcontent += "test_version_dir = " + test_version_dir + "\n"
	logcontent += "test_toolchain_name_dir = " + test_toolchain_name_dir + "\n"
	logcontent += "test_toolchain_version_dir = " + test_toolchain_version_dir + "\n"
	logcontent += "test_cmakelist = " + test_cmakelist + "\n"
	logcontent += "test_name_cmakelist = " +test_name_cmakelist + "\n"
	logcontent += "test_version_cmakelist = " +test_version_cmakelist + "\n"
	logcontent += "test_toolchain_name_cmakelist = " +test_toolchain_name_cmakelist + "\n"
	logcontent += "test_toolchain_version_cmakelist = " +test_toolchain_version_cmakelist + "\n"
	logcontent += "test_destdir = " + test_destdir + "\n"
	logcontent += "\n"
	# if test directory exist, delete and recreate it inorder for reproducible test builds
	if os.path.isdir(test_destdir):
		shutil.rmtree(test_destdir)
		logcontent += "removing directory " + test_destdir + "\n"

	# create directories if they don't exist
	# Directory Format: <software>/<version>/toolchain-name>/<toolchain-version>
	logcontent += "Creating directory: " + test_ebapp_dir + "\n"
	create_dir(test_ebapp_dir,verbose)

	logcontent += "Creating directory: " + test_name_dir + "\n"
	create_dir(test_name_dir,verbose)

	logcontent += "Creating directory: " + test_version_dir + "\n"
	create_dir(test_version_dir,verbose)

	logcontent += "Creating directory: " + test_toolchain_name_dir + "\n"
	create_dir(test_toolchain_name_dir,verbose)

	logcontent += "Creating directory: " + test_toolchain_version_dir + "\n"
	create_dir(test_toolchain_version_dir,verbose)
	
	# create CMakeList.txt file in each directory of <software>/<version>/<toolchain-name>/<toolchain-version> if it doesn't exist
	logcontent += "Creating CMakeLists.txt file: " + test_ebapp_cmakelist + "\n"
	create_file(test_ebapp_cmakelist,verbose)

	logcontent += "Creating CMakeLists.txt file: " + test_name_cmakelist + "\n"
	create_file(test_name_cmakelist,verbose)

	logcontent += "Creating CMakeLists.txt file: " + test_version_cmakelist + "\n"
	create_file(test_version_cmakelist,verbose)

	logcontent += "Creating CMakeLists.txt file: " + test_toolchain_name_cmakelist + "\n"
	create_file(test_toolchain_name_cmakelist,verbose)

	logcontent += "Creating CMakeLists.txt file: " + test_toolchain_version_cmakelist + "\n"
	create_file(test_toolchain_version_cmakelist,verbose)

	logcontent += "Updating " + test_cmakelist + " with add_subdirectory(ebapp) \n"
	# update CMakeLists.txt with tags add_subdirectory(ebapp)
	update_CMakeLists(test_cmakelist,"ebapp",verbose)

	# update CMakeLists.txt with tags add_subdirectory(X) where X=name|version|toolchain-name|toolchain-version
	logcontent += "Updating " + test_ebapp_cmakelist + " with add_subdirectory("+name+")\n"
	update_CMakeLists(test_ebapp_cmakelist,name,verbose)

	logcontent += "Updating " + test_name_cmakelist + " with add_subdirectory("+version+")\n"
	update_CMakeLists(test_name_cmakelist,version,verbose)

	logcontent += "Updating " + test_version_cmakelist + " with add_subdirectory("+toolchain_name+")\n"
	update_CMakeLists(test_version_cmakelist,toolchain_name,verbose)

	logcontent += "Updating " + test_toolchain_name_cmakelist + " with add_subdirectory("+toolchain_version+")\n"
	update_CMakeLists(test_toolchain_name_cmakelist,toolchain_version,verbose)

	# load preamble for test-script that initializes environment.
	header=load_modules(software,toolchain)

	logcontent += "\n"
	logcontent += "Reading File: " + filename + "\n"
	fd=open(filename,'r')
	content=yaml.load(fd)
	logcontent += "Loading YAML content \n"
	# if key binaries is not in yaml file, exit program
	if "binaries" not in content:
		print "Cant find key binaries in file: ", filename, " Exiting program"
		update_logfile(logdir,logcontent,verbose)
		sys.exit(1)

	# create a binary test script for each key,value item in dictionary
	binarydict=content["binaries"]
	for key in binarydict:
		testname=key+".sh"
		testpath=os.path.join(test_destdir,testname)
		logcontent += "Creating test file: " +  testpath + "\n"
		fd=open(testpath,'w')
		fd.write(header)
		# if paramter is specified then write both executable and parameter to file otherwise only write the executable
		if binarydict[key]:
			fd.write(key + " " + binarydict[key])
		else:
			fd.write(key)
		fd.close()

		# reading test script for writing content of test in logcontent 
		fd=open(testpath,'r')
		content=fd.read()
		fd.close()
		logcontent+= "Content of test file: " + testpath + "\n"
		logcontent += "----------------------------------------------------- \n"
		logcontent+=content +"\n"
		logcontent += "----------------------------------------------------- \n"
		
		fd=open(test_toolchain_version_cmakelist,'a')
		add_test_str="add_test(NAME " + name + "-" + version + "-" + toolchain_name + "-" + toolchain_version + "-" + testname + "\t COMMAND sh " + testname + "\t WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}) \n"
	
		logcontent += "Updating CMakeLists: " + test_toolchain_version_cmakelist + " with content: "+ add_test_str 
		fd.write(add_test_str)

		print "Creating Test:", testpath
		logcontent += "Creating Test:" + testpath + "\n"
	return logcontent
	
			
