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
Function that process the YAML config and verify key/value.
Also declares the valid YAML keys that can be used when writing YAML configs


:author: Shahzeb Siddiqui (Pfizer)
"""

import os
import sys
import yaml 


field={
	'name':'',
	'source':'',
	'args':'',
	'scheduler':['slurm','lsf','pbs'],
	'buildopts':'',
	'buildcmd':'',
	'inputfile':'',
	'iter':'',
	'outputfile':'',
	'runcmd':'',
	'runextracmd':'',
	'mpi':'enabled',
	'cuda':'enabled',
	'nproc': ''
}

def parse_config(filename,codedir):
	"""
	read config file and verify the key-value content with dictionary field
	"""
        fd=open(filename,'r')
	content=yaml.load(fd)
	# iterate over dictionary to seek any invalid keys 
	for key in content:
		if key not in field:
			print "ERROR: invalid key", key 
			sys.exit(1)
		# key-value name must match the yaml file name, but strip out .yaml extension for comparison
		if key == "name":
			strip_ext=os.path.splitext(filename)[0]
        	        # get name of file only for comparison with key value "name"
                	filename=os.path.basename(strip_ext)
                	if content[key] != filename:   
                        	print "Invalid value for key: ",key,":",content[key],". Value should be:", filename
				sys.exit(1)
		# source must match a valid file name
		elif key == "source" or key == "inputfile":
	                codefile=os.path.join(codedir,content[key])
        	        if not os.path.exists(codefile):
                	        print "Can't find source file: ",codefile, ". Verify source file in directory:", codedir
				sys.exit(1)
		# checking for invalid scheduler option
		elif key == "scheduler":
			if content[key] not in field["scheduler"]:
				print "Invalid scheduler option: ", key, " Please select on of the following:" , field["scheduler"]
				sys.exit(1)
		elif key == "nproc" or key == "iter":
			# checking whether value of nproc and iter is integer
			if not str(content[key]).isdigit(): 
				print key + " key must be an integer value"
				sys.exit(1)
			# checking whether key is negative or zero
			else:
				if int(content[key]) <= 0: 
					print key + " must be greater than 0"
					sys.exit(1)
		
			
	fd.close()
	return content

