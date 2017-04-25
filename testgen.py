from setup import *
import os.path 
import os, sys
import shutil
import yaml
def systempkg_generate_binary_test(pkg,verbose):
	toplevel_cmakelist_file=os.path.join(BUILDTEST_ROOT,"CMakeLists.txt")
	testingdir_cmakelist_file=os.path.join(BUILDTEST_TESTDIR,"CMakeLists.txt")
	commandfile=os.path.join(BUILDTEST_SOURCEDIR,"system",pkg,"command.yaml")

        # if CMakeLists.txt does not exist in top-level directory, create the header
        if os.path.isfile(toplevel_cmakelist_file) == False:
                init_CMakeList(toplevel_cmakelist_file)

        create_dir(BUILDTEST_TESTDIR,verbose)
        # if BUILDTEST_TESTDIR/CMakeLists.txt does not exist, then create it
        if os.path.isfile(testingdir_cmakelist_file) == False:
                fd=open(testingdir_cmakelist_file,'w')
                fd.close()
        # if command.yaml does not exist then report error
        if os.path.isfile(commandfile) == False:
                print "Warning: Cannot find command file:", commandfile, "Skipping binary test"
        else:
            systempkg_process_binary_file(commandfile,pkg,verbose)

def generate_binary_test(software,toolchain,verbose):
	toplevel_cmakelist_file=os.path.join(BUILDTEST_ROOT,"CMakeLists.txt")
	testingdir_cmakelist_file=os.path.join(BUILDTEST_TESTDIR,"CMakeLists.txt")
	swname = software[0]
	commandfile=os.path.join(BUILDTEST_SOURCEDIR,swname,"command.yaml")


	# if CMakeLists.txt does not exist in top-level directory, create the header
	if os.path.isfile(toplevel_cmakelist_file) == False:
		init_CMakeList(toplevel_cmakelist_file)

	create_dir(BUILDTEST_TESTDIR,verbose)
	# if BUILDTEST_TESTDIR/CMakeLists.txt does not exist, then create it
	if os.path.isfile(testingdir_cmakelist_file) == False:
		fd=open(testingdir_cmakelist_file,'w')
		fd.close()
	# if command.yaml does not exist then report error
	if os.path.isfile(commandfile) == False:
		print "Warning: Cannot find command file:", commandfile, "Skipping binary test"
	else:
	    process_binary_file(commandfile,software,toolchain,verbose)

# generate test for source
def generate_source_test(software,toolchain,configmap,codedir,verbose,subdir):
	appname=software[0]
	appver=software[1]
	tcname=toolchain[0]
	tcver=toolchain[1]
	
	# app_destdir is root of test directory
	app_destdir = os.path.join(BUILDTEST_TESTDIR,appname,appver,tcname,tcver)
	# destdir is where test script and CMakeLists.txt will be generated. If there is a subdirectory then testscript will reside
	# in subdir
	destdir=os.path.join(app_destdir,subdir)
	cmakelist=os.path.join(destdir,"CMakeLists.txt")
	
	#print "subdir:",subdir, "destdir:", destdir
	#sys.exit(1)

	# if subdirectory exists, create subdirectory in destdir so we can write test script
	if subdir != "":
		os.mkdir(destdir)

	# testname is key value "name" with .sh extension
	testname=configmap["name"]+".sh"
	testpath=os.path.join(destdir,testname)
	sourcefilepath=os.path.join(codedir,configmap["source"])
	executable=configmap["source"]+".exe"

	flags=""
	# if buildopts key exists in dictionary
	if "buildopts" in configmap:
		flags=configmap["buildopts"]

	fd=open(testpath,'w')
	header=load_modules(software,toolchain)
	fd.write(header)
	
	buildcmd=""
	runcmd=""
	compiler=""
	nproc = ""
        # if there is a buildcmd & runcmd in yaml file, put it directly in script
        if "buildcmd" in configmap and "runcmd" in configmap:
		# source BUILDTEST environments used for finding source
		fd.write("source " + BUILDTEST_ROOT + "setup.sh \n")
		for cmd in configmap["buildcmd"]:
	                buildcmd += cmd + "\n"
	
		for cmd in configmap["runcmd"]:
			runcmd += cmd + "\n"

		if verbose >=1:
			print testpath,":Invoking YAML buildcmd and runcmd fields..."
			print "-----------------------------------"
			print "BUILDCMD:"
			print buildcmd
			print "-----------------------------------"
			print "RUNCMD:"
			print runcmd
			print "-----------------------------------"
	        fd.write(buildcmd)
	        fd.write(runcmd)

			
	# otherwise generate the buildcmd and runcmd automatically
	else:
		# checking if either buildcmd or runcmd specified but not both, then report an error.
		if "buildcmd" in configmap and "runcmd" not in configmap or "buildcmd" not in configmap and "runcmd" in configmap:
			print "Need to specify both key: buildcmd and runcmd"
			sys.exit(1)

	        compiler,compiler_type=get_compiler(configmap,appname,tcname)
    		
		# set buildcmd based on testblockname. compiler is either gcc,icc,mpicc, or mpiicc based on testblockname
	        if compiler_type == "gnu" or compiler_type == "intel":
        	        buildcmd = compiler + " -o " + executable + " " + sourcefilepath + " " + flags + "\n"

	        if compiler_type == "gnu" or compiler_type == "intel" or compiler_type == "nvcc":
	                # for intel mpi test, the runcmd needs to be mpirun
	                if compiler in ["mpicc","mpic++","mpifort","mpiicc","mpiic++", "mpiifort"]:
	
		                # if nproc is defined in yaml, store value in nproc which will use it in mpirun command
        		        if configmap["nproc"]:
                		        nproc = str(configmap["nproc"])
				# if nproc is not specified set it to 1 when building mpi apps
				else:		
					nproc = "1"

                	        runcmd = "mpirun -np " + nproc + " ./" + executable + "\n"
	                else:
        	                runcmd = "./" + executable + "\n"
		elif compiler_type == "python":
			runcmd = "python " + sourcefilepath + "\n"
		elif compiler_type == "java":
			buildcmd = compiler + " " + sourcefilepath + "\n"
			java_codedir=os.path.dirname(sourcefilepath)
			filename = os.path.basename(os.path.splitext(sourcefilepath)[0])
			runcmd = "cd " + java_codedir + "\n"
			runcmd += "java " + filename + "\n"
			runcmd += "rm -v " + filename + ".class"

		if verbose >=1:
			print testpath,":Invoking automatic buildcmd and runcmd fields..."
			print "-----------------------------------"
			print "BUILDCMD:",buildcmd
			print "RUNCMD:",runcmd
			print "-----------------------------------"

		fd.write(buildcmd)
		fd.write(runcmd)
		if "runextracmd" in configmap:
			for cmd in configmap["runextracmd"]:
				fd.write(cmd + "\n")

	fd.close()

	fd=open(cmakelist,'a')
	if subdir != "":
		parent_cmakelist = os.path.join(app_destdir,"CMakeLists.txt")
		fd1=open(parent_cmakelist,'a')
		fd1.write("add_subdirectory("+subdir+") \n")
		fd1.close()

		add_test_str="add_test(NAME " + appname + "-" + appver + "-" + tcname + "-" + tcver + "-"  + subdir + "-" + testname + "\t COMMAND sh " +  testname + "\t WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}) \n"
	else:
		add_test_str="add_test(NAME " + appname + "-" + appver + "-" + tcname + "-" + tcver + "-"  + testname + "\t COMMAND sh " + testname + "\t WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}) \n"
	fd.write(add_test_str)
	fd.close()

	print "Creating Test: ",testpath	
# get the appropriate compiler based on the application/toolchain. Compiler/Wrappers can be gcc,icc,mpicc,nvcc,javac,python,R,perl,etc...
def get_compiler(configmap,appname,tcname):
	# get extension for source file
	ext = os.path.splitext(configmap["source"])[1]
	compiler=""

	# if app is GCC, GCCcore, -> compiler = gcc
	# if app toolchain is GCC, GCCcore, dummy -> compiler = gcc
 	# if app is OpenMPI,MVAPICH, MPICH toolchain is GCC -> compiler = mpicc
	# if app is intel -> compiler = icc/mpiicc -> need tag: mpi=enabled
	# if app is python, tc=X -> compiler = python
	# if app is OpenMPI, tc is intel -> compiler = mpicc
	# if app is CUDA, tc=X -> compiler = nvcc
	# if app is X, tc=gcccuda, compiler = gcc/nvcc need tag: cuda=enabled
	# if cuda enabled
	cuda = ""
	mpi = ""
	if "cuda" in configmap:
		cuda=configmap["cuda"]
	if "mpi" in configmap:
		mpi=configmap["mpi"]

	# compiler_type valid may be "gnu, intel, mpi, intel-mpi, R, java, python"
	compiler_type=""

	# condition to calculate testblockname based on toolchain
	if tcname in ["GCC","GCCcore","gcccuda","dummy","gompi", "foss","goolfc"]:
		compiler_type="gnu"
	if tcname in ["intel", "iccifort","iccifortcuda","impi","iimpi","iimpic"]: 
		compiler_type="intel"
	
	
	#if appname in ["GCC","GCCcore"]:
	#	testblockname="gcc"
	if appname in ["intel"]:
		compiler_type="intel"

	# compiler can be determined automatically for apps below
	if appname in ["Anaconda2", "Anaconda3", "Python", "Python3"]:
		compiler = "python"
		return compiler,compiler
	if appname in ["R"]:
		compiler = "R"
		return compiler,compiler
	if appname in ["Java"]:
		compiler = "javac"
		return compiler,compiler
	if appname in ["CUDA"]:
		compiler = "nvcc"
		return compiler,compiler


	#testblockname=configmap["testblock"]
	
	# determine compiler based on compiler_type and its file extension
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

def systempkg_process_binary_file(filename,pkg,verbose):

	test_system_dir=os.path.join(BUILDTEST_TESTDIR,"system")
	test_destdir=os.path.join(BUILDTEST_TESTDIR,"system",pkg)

	test_cmakelist = os.path.join(BUILDTEST_TESTDIR,"CMakeLists.txt")
	test_cmakelist_pkg = os.path.join(BUILDTEST_TESTDIR,"system","CMakeLists.txt")
	test_cmakelist_destdir=os.path.join(test_destdir,"CMakeLists.txt")

        # if testdirectory exist, delete and recreate it inorder for reproducible test builds
        if os.path.isdir(test_destdir):
                shutil.rmtree(test_destdir)

	create_dir(test_system_dir,verbose)
	create_dir(test_destdir,verbose)

	create_file(test_cmakelist,verbose)
	create_file(test_cmakelist_pkg,verbose)
	create_file(test_cmakelist_destdir,verbose)


        check_CMakeLists(test_cmakelist,"system",verbose)
        check_CMakeLists(test_cmakelist_pkg,pkg,verbose)

	fd=open(filename,'r')
        content=yaml.load(fd)
        # if key binaries is not in yaml file, exit program
        if "binaries" not in content:
                print "Cant find key binaries in file: ", filename, " Exiting program"
                sys.exit(1)

        # create a binary test script for each key,value item in dictionary
        binarydict=content["binaries"]
        for key in binarydict:
                testname=key+".sh"
                testpath=os.path.join(test_destdir,testname)
                fd=open(testpath,'w')
		fd.write("module purge \n" )
                # if paramter is specified then write both executable and parameter to file otherwise only write the executable
                if binarydict[key]:
                        fd.write(key + " " + binarydict[key])
                else:
                        fd.write(key)
                fd.close()

                fd=open(test_cmakelist_destdir,'a')
                add_test_str="add_test(NAME system-" + pkg + "-" + testname + "\t COMMAND sh " + testname + "\t WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}) \n"
                fd.write(add_test_str)

                print "Creating Test:", testpath


# read binary file (command.txt) and create template shell script 
def process_binary_file(filename,software,toolchain,verbose):
	name,version=software
	toolchain_name,toolchain_version=toolchain
	#print "values",name,version,toolchain_name,toolchain_version
	# if top level software directory is not present, create it
	test_name_dir=os.path.join(BUILDTEST_TESTDIR,name)
	test_version_dir=os.path.join(test_name_dir,version)
	test_toolchain_name_dir=os.path.join(test_version_dir,toolchain_name)
	test_toolchain_version_dir=os.path.join(test_toolchain_name_dir,toolchain_version)

	test_cmakelist = os.path.join(BUILDTEST_TESTDIR,"CMakeLists.txt")
	test_name_cmakelist = os.path.join(test_name_dir,"CMakeLists.txt")
	test_version_cmakelist = os.path.join(test_version_dir,"CMakeLists.txt")
	test_toolchain_name_cmakelist = os.path.join(test_toolchain_name_dir,"CMakeLists.txt")
	test_toolchain_version_cmakelist = os.path.join(test_toolchain_version_dir,"CMakeLists.txt")

	test_destdir=test_toolchain_version_dir
	# if testdirectory exist, delete and recreate it inorder for reproducible test builds
	if os.path.isdir(test_destdir):
		shutil.rmtree(test_destdir)

	# create directories if they don't exist
	# Directory Format: <software>/<version>/toolchain-name>/<toolchain-version>
	create_dir(test_name_dir,verbose)
	create_dir(test_version_dir,verbose)
	create_dir(test_toolchain_name_dir,verbose)
	create_dir(test_toolchain_version_dir,verbose)
	
	# create CMakeList.txt file in each directory of <software>/<version>/<toolchain-name>/<toolchain-version> if it doesn't exist
	create_file(test_name_cmakelist,verbose)
	create_file(test_version_cmakelist,verbose)
	create_file(test_toolchain_name_cmakelist,verbose)
	create_file(test_toolchain_version_cmakelist,verbose)

	check_CMakeLists(test_cmakelist,name,verbose)
	check_CMakeLists(test_name_cmakelist,version,verbose)
	check_CMakeLists(test_version_cmakelist,toolchain_name,verbose)
	check_CMakeLists(test_toolchain_name_cmakelist,toolchain_version,verbose)

		
	header=load_modules(software,toolchain)

	fd=open(filename,'r')
	content=yaml.load(fd)
	# if key binaries is not in yaml file, exit program
	if "binaries" not in content:
		print "Cant find key binaries in file: ", filename, " Exiting program"
		sys.exit(1)

	# create a binary test script for each key,value item in dictionary
	binarydict=content["binaries"]
	for key in binarydict:
		testname=key+".sh"
		testpath=os.path.join(test_destdir,testname)
		fd=open(testpath,'w')
		fd.write(header)
		# if paramter is specified then write both executable and parameter to file otherwise only write the executable
		if binarydict[key]:
			fd.write(key + " " + binarydict[key])
		else:
			fd.write(key)
		fd.close()

		fd=open(test_toolchain_version_cmakelist,'a')
		add_test_str="add_test(NAME " + name + "-" + version + "-" + toolchain_name + "-" + toolchain_version + "-" + testname + "\t COMMAND sh " + testname + "\t WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}) \n"
		fd.write(add_test_str)

		print "Creating Test:", testpath
		
# create directory if it doesn't exist
def create_dir(dirname,verbose):
	if not os.path.isdir(dirname):
		os.mkdir(dirname)
		if verbose >= 1:
			print "Creating Directory: ",dirname

# create an empty file if it doesn't exist
def create_file(filename,verbose):
	if not os.path.isfile(filename):
		fd=open(filename,'w')
		fd.close()
		if verbose >= 1:
			print "Creating Empty File:", filename

# used for writing CMakeLists.txt with tag <software>, <version>, & toolchain
def check_CMakeLists(filename,tag, verbose):
	fd=open(filename,'r')
	content=fd.read().strip().split("\n")
	cmd="add_subdirectory("+tag+")"
	if cmd not in content:
		fd.close()
		fd=open(filename,'a')
		fd.write(cmd+"\n")
		fd.close()
		if verbose >= 1:
			print "writing:", cmd, "to file:",filename 
	else:
		fd.close()	
#def write_binary_test(filename):
def init_CMakeList(filename):
	header = """ 
cmake_minimum_required(VERSION 2.8)
include(CTest)
ENABLE_TESTING()
add_subdirectory(""" + BUILDTEST_TESTDIR + ")"
	fd=open(filename,'w')
	fd.write(header)
	fd.close()
# return a string that loads the software and toolchain module. 
def load_modules(software,toolchain):
	# for dummy toolchain you can load software directly. Ensure a clean environment by running module purge
	if toolchain[0] == "dummy":
		header="""
#!/bin/sh
module purge
module load """ + software[0] + "/" + software[1] + """
"""
	else:
		header="""
#!/bin/sh
module purge
module load """ + toolchain[0] + "/" + toolchain[1] + """
module load """ + software[0] + "/" + software[1] + """
"""
	
	return header
			
