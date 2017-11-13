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


from framework.env import BUILDTEST_MODULE_NAMING_SCHEME, logID
from framework.tools.menu import buildtest_menu
"""
:author: Shahzeb Siddiqui (Pfizer) 
"""
def print_set(setcollection):
        """
        prints the content of set 
        """
        for item in setcollection:
                print item
class sset(set):
    def __str__(self):
        return ', '.join([str(i) for i in self])

def get_appname():
        args = buildtest_menu()
        args_dict = vars(args)
        software = args_dict["software"]
        software = software.split('/')
        return software[0]

def get_appversion():
        args = buildtest_menu()
        args_dict = vars(args)
        software = args_dict["software"]
        software = software.split('/')
        if BUILDTEST_MODULE_NAMING_SCHEME == "FNS":
                tc = get_toolchain()
                appversion = software[1].replace(tc,'')
                if appversion[-1] == "-":
                        appversion = appversion[:-1]
                        return appversion
        else:
                return software[1]

def get_application_name():
        return get_appname() + '-' + get_appversion()

def get_toolchain():
        return get_toolchain_name() + '-' + get_toolchain_version()

def get_toolchain_name():
        args = buildtest_menu()
        args_dict = vars(args)
        toolchain = args_dict["toolchain"]

        # checking if toolchain is defined in argument
        if toolchain is  None:
                return ""
        else:
                toolchain = toolchain.split("/")
                return toolchain[0]

def get_toolchain_version():
        args = buildtest_menu()
        args_dict = vars(args)
        toolchain = args_dict["toolchain"]

        # checking if toolchain is defined in argument
        if toolchain is None:
                return ""
        else:
                toolchain = toolchain.split("/")
                return toolchain[1]


