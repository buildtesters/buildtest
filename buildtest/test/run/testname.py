############################################################################
#
#  Copyright 2017-2018
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

This module will run test scripts via buildtest and capture output and additional
metrics that will be stored in json format

:author: Shahzeb Siddiqui

"""
import os
import subprocess
import sys

from buildtest.tools.config import config_opts, BUILDTEST_SHELLTYPES

def run_testname(testname,test_output="no"):
    """ test script to run """

    try:
        open(testname,"r")
    except OSError as err_msg:
        print (err_msg)
        sys.exit(1)

    output_redirect=""
    if test_output == "yes":
        output_redirect = " >/dev/stdout 2>&1"
    else:
        output_redirect = " >/dev/null 2>&1"

    testname += output_redirect
    print (f"Executing Test: {testname}")
    print ("---------------------------------------------------------")
    ret = subprocess.Popen(testname,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ret.communicate()[0].decode("utf-8")

    ret_code = ret.returncode
    if test_output == "yes":
        print(output)
    if ret_code == 0:
        print("Test Successful")
    else:
        print("Test Failed")
    print ("---------------------------------------------------------")
    sys.exit(0)

def test_list():
    """ return a list of test found in BUILDTEST_TESTDIR"""
    test = []

    for root, subdir, files in os.walk(config_opts['BUILDTEST_TESTDIR']):
        for file in files:
            if os.path.splitext(file)[1][1:] in BUILDTEST_SHELLTYPES:
                test.append(os.path.join(root,file))

    return test
