############################################################################ 
# 
#  Copyright 2017 
# 
#   https://github.com/shahzebsiddiqui/buildtest 
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

import os
import logging

from framework.tools.modules import load_modules
from framework.tools.cmake import add_test_to_CMakeLists, setup_software_cmake
from framework.test.sourcetest import recursive_gen_test
from framework.test.job import generate_job
from framework.tools.utility import get_appname, get_appversion, get_toolchain_name, get_toolchain_version
from framework.env import BUILDTEST_SOURCEDIR, BUILDTEST_PYTHON_DIR, BUILDTEST_R_DIR, BUILDTEST_PYTHON_DIR, BUILDTEST_RUBY_DIR, BUILDTEST_PERL_DIR, BUILDTEST_TCL_DIR,BUILDTEST_TESTDIR
from framework.env import PYTHON_APPS, MPI_APPS, logID
from framework.tools.menu import buildtest_menu

"""
This python module is used with the flag --testset to create test scripts that 
don't require any YAML files. 

:author: Shahzeb Siddiqui (Pfizer)

"""
def run_testset(arg_dict):
	""" checks the testset parameter to determine which set of scripts to use to create tests """


	appname = get_appname()

	source_app_dir=""
	codedir=""
	logcontent = ""
	runtest = False

	if appname in PYTHON_APPS and arg_dict.testset == "Python":
	        source_app_dir=os.path.join(BUILDTEST_PYTHON_DIR,"python")
                runtest=True
    
        if appname in ["Perl"] and arg_dict.testset == "Perl":
        	source_app_dir=os.path.join(BUILDTEST_PERL_DIR,"perl")
                runtest=True

        # condition to run R testset
        if appname in ["R"] and arg_dict.testset == "R":
        	source_app_dir=os.path.join(BUILDTEST_R_DIR,"R")
                runtest=True


        # condition to run R testset
        if appname in ["Ruby"] and arg_dict.testset == "Ruby":
                source_app_dir=os.path.join(BUILDTEST_RUBY_DIR,"ruby")
                runtest=True


        # condition to run R testset
        if appname in ["Tcl"] and arg_dict.testset == "Tcl":
                source_app_dir=os.path.join(BUILDTEST_TCL_DIR,"Tcl")
                runtest=True

	# for MPI we run recursive_gen_test since it processes YAML files
	if appname in MPI_APPS and arg_dict.testset == "MPI":
		source_app_dir=os.path.join(BUILDTEST_SOURCEDIR,"mpi")
		configdir=os.path.join(source_app_dir,"config")
		codedir=os.path.join(source_app_dir,"code")
		recursive_gen_test(configdir,codedir)
		return
        if runtest == True:
        	codedir=os.path.join(source_app_dir,"code")
                testset_generator(arg_dict,codedir)

def testset_generator(arg_dict, codedir):

	logger = logging.getLogger(logID)
	wrapper=""
        appname=get_appname()
        appver=get_appversion()
        tcname=get_toolchain_name()
	tcver=get_toolchain_version()

	args_dict = buildtest_menu().parse_options()
	
	app_destdir = os.path.join(BUILDTEST_TESTDIR,"ebapp",appname,appver,tcname,tcver)
	cmakelist = os.path.join(app_destdir,"CMakeLists.txt")
	
	# setup CMakeList in all subdirectories for the app if CMakeList.txt was not generated from
	# binary test 
	if not os.path.exists(cmakelist):
		setup_software_cmake()
	emptylist = []
	if os.path.isdir(codedir):
		for root,subdirs,files in os.walk(codedir):

			# skip to next item in loop when a sub-directory has no files
			if len(files) == 0:
				continue

			count = 0
			for file in files:
				# get file name without extension
				fname = os.path.splitext(file)[0]
				# get file extension
				ext = os.path.splitext(file)[1]
			
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

				testname = fname + "." + args_dict.shell
				testpath = os.path.join(subdirpath,testname)
				fd = open(testpath,'w')
				header=load_modules(args_dict.shell)
				fd.write(header)
				fd.write(cmd)
				fd.close()
			
				cmakelist = os.path.join(subdirpath,"CMakeLists.txt")
				add_test_to_CMakeLists(app_destdir,subdir,cmakelist,testname)
				msg = "Creating Test: " + testpath  
				logger.info(msg)
				count = count + 1

        			if args_dict.job_template != None:
					generate_job(testpath,args_dict.shell,args_dict.job_template,emptylist)

			print "Generating ", count, "tests for ", os.path.basename(root)

	print "Writing tests to ", app_destdir

