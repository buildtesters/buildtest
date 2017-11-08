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
This python module gets the parameters from YAML file and returns them to be 
used as python variables

:author: Shahzeb Siddiqui (Pfizer)
"""
def get_name(config):
	return config["name"]

def get_source(config):
	return config["source"]

def get_args(config):
	return config["args"]

def get_buildopts(config):
	return config["buildopts"]

def get_inputfile(config):
	return config["inputfile"]

def get_outputfile(config):
	return config["outputfile"]

def get_iter(config):
	return config["iter"]

def get_runcmd(config):
	return config["runcmd"]

def get_runextracmd(config):
	return config["runextracmd"]

def get_mpi(config):
	return config["mpi"]

def get_cuda(config):
	return config["cuda"]

def get_nproc(config):
	return config["nproc"]
