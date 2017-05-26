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
from parser import *
from tools.generic import *
from tools.cmake import *
from master import *
import os
def run_testset(software,toolchain,testset,verbose):
	""" checks the testset parameter to determine which set of scripts to use to create tests """

	appname,appversion=software

	source_app_dir=""
	codedir=""
	logcontent = ""
	runtest = False

	if appname in PYTHON_APPS and testset == "python":
	        source_app_dir=os.path.join(os.environ['BUILDTEST_PYTHON_DIR'],"python")
                runtest=True
    
        if appname in PERL_APPS and testset == "perl":
        	source_app_dir=os.path.join(os.environ['BUILDTEST_PERL_DIR'],"perl")
                runtest=True

        # condition to run R testset
        if appname in ["R"] and testset == "R":
        	source_app_dir=os.path.join(os.environ['BUILDTEST_R_DIR'],"R")
                runtest=True

	# for MPI we run recursive_gen_test since it processes YAML files
	if appname in MPI_APPS and testset == "mpi":
		source_app_dir=os.path.join(BUILDTEST_SOURCEDIR,"python")
		configdir=os.path.join(source_app_dir,"config")
		codedir=os.path.join(source_app_dir,"code")
		recursive_gen_test(software,toolchain,configdir,codedir,verbose)
		return
        if runtest == True:
        	codedir=os.path.join(source_app_dir,"code")
                testset_generator(software,toolchain,codedir,verbose)

def testset_generator(software,toolchain,codedir,verbose):
	logcontent = "--------------------------------------\n"
	logcontent = "function: testset_generator \n"
	logcontent = "--------------------------------------\n"

	wrapper=""
        appname=software[0]
        appver=software[1]
        tcname=toolchain[0]
        tcver=toolchain[1]

	app_destdir = os.path.join(BUILDTEST_TESTDIR,"ebapp",appname,appver,tcname,tcver)
	cmakelist = os.path.join(app_destdir,"CMakeLists.txt")
	if os.path.isdir(codedir):
		for root,subdirs,files in os.walk(codedir):
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
				else:
					continue

				cmd = wrapper + " " + os.path.join(root,file)
				subdir = os.path.basename(root)
				subdirpath = os.path.join(app_destdir,subdir)
				if not os.path.exists(subdirpath):
					os.mkdir(subdirpath)
				testname = fname + ".sh"
				testpath = os.path.join(subdirpath,testname)
				fd = open(testpath,'w')
				header=load_modules(software,toolchain)
				fd.write(header)
				fd.write(cmd)
				fd.close()
			
				logcontent+="TestPath: " + testpath
				logcontent+="\n--------------------------------------------\n"
				logcontent+=open(testpath,'r').read()
				logcontent+="\n--------------------------------------------\n"
				
				cmakelist = os.path.join(subdirpath,"CMakeLists.txt")
				add_test_to_CMakeLists(appname,appver,tcname,tcver,app_destdir,subdir,cmakelist,testname)
				msg = "Creating Test: " + testpath  
				print msg
				BUILDTEST_LOGCONTENT.append(msg + "\n")
