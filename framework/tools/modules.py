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
This python module does the following
	 - get module listing
	 - get unique application
	 - get unique application version
	 - get easybuild toolchains
 	 - check if software exists based on argument -s
	 - check if toolchain exists based on argument -t
	 - check if easyconfig passes

:author: Shahzeb Siddiqui (Pfizer)
"""

from framework.env import BUILDTEST_MODULE_NAMING_SCHEME,BUILDTEST_MODULE_EBROOT
from framework.tools.menu import buildtest_menu
from framework.tools.utility import get_appname, get_appversion, get_toolchain_name, get_toolchain_version
import os


def get_module_list():
	"""
	returns a complete list of modules and full path in module tree
	"""
	modulefiles = []
	for root, dirs, files in os.walk(BUILDTEST_MODULE_EBROOT):
		for file in files:
			modulefiles.append(os.path.join(root,file))

	return modulefiles


def load_modules():
        """
        return a string that loads the software and toolchain module.
        """
	args = 	buildtest_menu()
	args_dict = vars(args)
	shell_type = args_dict["shell"]
	
	shell_magic = "#!/" + os.path.join("bin",shell_type)

        appname = get_appname()
        appversion = get_appversion()
        tcname = get_toolchain_name()
        tcversion = get_toolchain_version()

	header = shell_magic
        header+= """
module purge
"""
        # for dummy toolchain you can load software directly. Ensure a clean environment by running module purge
        if len(tcname) == 0:
                moduleload = "module load " + appname + "/" + appversion  + "\n"
        else:
                if BUILDTEST_MODULE_NAMING_SCHEME == "HMNS":
                        moduleload = "module load " + tcname + "/" + tcversion + "\n"
                        moduleload += "module load " + appname + "/" + appversion + "\n"
                elif BUILDTEST_MODULE_NAMING_SCHEME == "FNS":
                        moduleload = "module load " + tcname + "/" + tcversion + "\n"
                        toolchain_name = appname + "-" + tcversion
                        appversion = appversion.replace(toolchain_name,'')
                        if appversion[-1] == "-":
                                appversion = appversion[:-1]

                        moduleload += " module load " + appname + "/" + appversion + "-" + tcname + "-" + tcversion + "\n"

        header = header + moduleload
        return header

