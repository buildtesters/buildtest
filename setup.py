############################################################################ 
# 
#  Copyright 2017 
# 
#   https://github.com/shahzebsiddiqui/BuildTest 
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
BUILDTEST_ROOT = os.getcwd()
BUILDTEST_SOURCEDIR = os.path.join(BUILDTEST_ROOT ,"source")
BUILDTEST_EASYCONFIGDIR = os.path.join(BUILDTEST_ROOT,"easybuild")
BUILDTEST_MODULEROOT = "/nfs/grid/software/RHEL7/easybuild/modules"
BUILDTEST_TESTDIR = os.path.join(BUILDTEST_ROOT,"testing")

