#!/bin/sh
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

BUILDTEST_ROOT=`pwd`
BUILDTEST_SOURCEDIR=${BUILDTEST_ROOT}"/buildtest-configs/source"
BUILDTEST_EASYCONFIGDIR=${BUILDTEST_ROOT}"/easybuild"
BUILDTEST_MODULEROOT=/nfs/grid/software/RHEL7/easybuild/modules
BUILDTEST_TESTDIR=$BUILDTEST_ROOT"/testing"

export BUILDTEST_ROOT
export BUILDTEST_SOURCEDIR
export BUILDTEST_EASYCONFIGDIR
export BUILDTEST_MODULEROOT
export BUILDTEST_TESTDIR
