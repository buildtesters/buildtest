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
from testgen import *
from utilities import load_modules
def recursive_gen_test(software,toolchain,configdir,codedir,verbose,logdir):
        # if config directory exists then process .yaml files to build source test
	logcontent =  "\n ------------------------------------------------------------ \n"
	logcontent += " function: recursive_gen_test \n"
	logcontent += "------------------------------------------------------------ \n"
	logcontent += " Processing all YAML files in " + configdir 
        if os.path.isdir(configdir):
                for root,subdirs,files in os.walk(configdir):
    
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
                                configmap=parse_config(software,toolchain,filepath,code_destdir)    
                                # error processing config file, then parse_config will return an empty dictionary
                                if len(configmap) == 0:
                                        continue
                                logcontent+=generate_source_test(software,toolchain,configmap,code_destdir,verbose,subdir,logdir)
	return logcontent

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
				logcontent+=add_test_to_CMakeLists(appname,appver,tcname,tcver,app_destdir,subdir,cmakelist,testname)
				print "Creating Test: ", testpath
	return logcontent				
	
