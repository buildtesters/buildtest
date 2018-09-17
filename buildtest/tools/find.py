#!/usr/bin/env python
############################################################################
#
#  Copyright 2017-2018
#
#   https://github.com/HPC-buildtest/buildtest-framework
#
#    This file is part of buildtest.
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
find functions for flags -fc and -ft

:author: Shahzeb Siddiqui (Pfizer)
"""

import os
import sys
from buildtest.tools.config import config_opts, BUILDTEST_SHELLTYPES

def find_all_yaml_configs():
    """ find all yaml configs"""
    count = 0
    BUILDTEST_CONFIGS_REPO = config_opts['BUILDTEST_CONFIGS_REPO']

    for root, dirs, files in os.walk(BUILDTEST_CONFIGS_REPO):
        for file in files:
            if file.endswith(".yaml"):
                count+=1
                print (os.path.join(root,file))

    print
    print ("Total YAML configs: ", count)
    sys.exit(0)

def find_yaml_configs_by_arg(find_arg):
    """find yaml configs based on argument"""
    count = 0

    BUILDTEST_CONFIGS_REPO = config_opts['BUILDTEST_CONFIGS_REPO']
    for root, dirs, files in os.walk(BUILDTEST_CONFIGS_REPO):
        for file in files:
            if file.endswith(".yaml") and find_arg in os.path.basename(file):
                count+=1
                print (os.path.join(root,file))

    print
    print ("Total YAML configs: ", count)
    sys.exit(0)

def find_all_tests():
    """find all test scripts in $BUILDTEST_TESTDIR"""
    BUILDTEST_TESTDIR = config_opts['BUILDTEST_TESTDIR']
    count = 0
    for root, dirs, files in os.walk(BUILDTEST_TESTDIR):
        for file in files:
            ext = os.path.splitext(file)[1]
            # remove leading . from extension
            ext = ext[1:]
            if ext in BUILDTEST_SHELLTYPES:
                count+=1
                print (os.path.join(root,file))


    print
    print ("Total Test scripts: ", count)
    sys.exit(0)

def find_tests_by_arg(find_arg):
    """find all test scripts in $BUILDTEST_TESTDIR"""
    count = 0
    BUILDTEST_TESTDIR = config_opts['BUILDTEST_TESTDIR']
    for root, dirs, files in os.walk(BUILDTEST_TESTDIR):
        for file in files:
            ext = os.path.splitext(file)[1]
            # remove leading . from extension
            ext = ext[1:]
            if ext in BUILDTEST_SHELLTYPES and find_arg in os.path.basename(file):
                count+=1
                print (os.path.join(root,file))


    print
    print ("Total Test scripts: ", count)
    sys.exit(0)
