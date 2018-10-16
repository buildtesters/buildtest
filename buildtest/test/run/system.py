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

This module will run an entire test suite for a system package. This implements
_buildtest run --system

:author: Shahzeb Siddiqui

"""

import os
import subprocess
import sys
from buildtest.tools.config import config_opts, BUILDTEST_SHELLTYPES
def run_system_choices():
    """
    generate choice field for _buildtest run --app
    """

    system_root_testdir = os.path.join(config_opts["BUILDTEST_TESTDIR"],"system")
    # if there is no directory $BUILDTEST_TESTDIR then return an empty list
    if not os.path.exists(system_root_testdir):
        return []
    systempkg_list = [ os.path.basename(f.path) for f in os.scandir(system_root_testdir) if f.is_dir()]

    return systempkg_list

def run_system_test(systempkg, test_output="no"):
    """
    implementation for _buildtest run --systempkg to execute all tests in the test directory
    """

    system_root_testdir = os.path.join(config_opts["BUILDTEST_TESTDIR"],"system")

    output_redirect=""
    if test_output == "yes":
        output_redirect = " >/dev/stdout 2>&1"
    else:
        output_redirect = " >/dev/null 2>&1"

    tests = [ f.path + output_redirect for f in os.scandir(os.path.join(system_root_testdir,systempkg)) if os.path.splitext(f)[1] in [".sh", ".bash", ".csh"]]

    count_test = len(tests)
    passed_test = 0
    failed_test = 0
    for test in tests:
        print (f"Executing Test: {test}")
        print ("---------------------------------------------------------")
        ret = subprocess.Popen(test,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        output = ret.communicate()[0].decode("utf-8")

        ret_code = ret.returncode
        if test_output == "yes":
            print(output)
        if ret_code == 0:
            print("Test Successful")
            passed_test += 1
        else:
            print("Test Failed")
            failed_test += 1
        print ("---------------------------------------------------------")

    print
    print
    print("==============================================================")
    print("                         Test summary                         ")
    print("System Package: ", systempkg)
    print(f"Executed {count_test} tests")
    print(f"Passed Tests: {passed_test}    Percentage: {passed_test*100/count_test}%")
    print(f"Passed Tests: {failed_test}    Percentage: {failed_test*100/count_test}%")
