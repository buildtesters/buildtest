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
from tools.generic import *


def recursive_gen_test(software,toolchain,configdir,codedir,verbose,logdir):
        """ if config directory exists then process .yaml files to build source test """
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

