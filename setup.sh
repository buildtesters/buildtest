#!/bin/sh
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

# @author: Shahzeb Siddiqui (Pfizer)

BUILDTEST_ROOT=`pwd`

# module naming scheme valid options: HMNS, FNS
BUILDTEST_MODULE_NAMING_SCHEME="HMNS"

BUILDTEST_SOURCEDIR=${BUILDTEST_ROOT}"/buildtest-configs"
BUILDTEST_TESTDIR=$BUILDTEST_ROOT"/testing"
BUILDTEST_PYTHON_DIR=$BUILDTEST_ROOT"/Python-buildtest-config"
BUILDTEST_PERL_DIR=$BUILDTEST_ROOT"/Perl-buildtest-config"
BUILDTEST_R_DIR=$BUILDTEST_ROOT"/R-buildtest-config"
BUILDTEST_RUBY_DIR=$BUILDTEST_ROOT"/Ruby-buildtest-config"
BUILDTEST_TCL_DIR=$BUILDTEST_ROOT"/Tcl-buildtest-config"

# BUILDTEST_EASYCONFIGDIR path to easybuild easyconfig directory
# BUILDTEST_EASYCONFIG=${BUILDTEST_ROOT}/path/to/easybuild/

# BUILDTEST_MODULE_EBROOT specify the root of the EB module tree
# BUILDTEST_MODULE_EBROOT=/path/to/moduletree:/path/to/moduletree/

export BUILDTEST_ROOT
export BUILDTEST_SOURCEDIR
export BUILDTEST_EASYCONFIGDIR
export BUILDTEST_MODULE_EBROOT
export BUILDTEST_MODULE_NAMING_SCHEME
export BUILDTEST_TESTDIR
export BUILDTEST_PYTHON_DIR
export BUILDTEST_PERL_DIR
export BUILDTEST_R_DIR
export BUILDTEST_RUBY_DIR
export BUILDTEST_TCL_DIR

export PATH=$PWD:${PATH}
