############################################################################ 
# 
#  Copyright 2017 
# 
#   https://github.com/shahzebsiddiqui/buildtest-framework
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

def get_arg_version(config):
	return config["version"]

def get_arg_findconfig(config):
        return config["findconfig"]

def get_arg_findtest(config):
        return config["findtest"]

def get_arg_software(config):
        return config["software"]

def get_arg_toolchain(config):
	return config["toolchain"]

def get_arg_list_toolchain(config):
        return config["list_toolchain"]

def get_arg_list_unique_software(config):
	return config["list_unique_software"]

def get_arg_software_version_relation(config):
	return config["software_version_relation"]

def get_arg_system(config):
	return config["system"]

def get_arg_testset(config):
	return config["testset"]

def get_arg_verbose(config):
        return config["verbose"]


