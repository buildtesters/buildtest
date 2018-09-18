
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
import sys

from buildtest.tools.config import config_opts, BUILDTEST_SHELLTYPES

def run_test_buildtest(testname):
    """ test script to run """

    try:
        open(testname,"r")
    except OSError as err_msg:
        print (err_msg)
        sys.exit(1)

    os.system(testname)
    sys.exit(0)

def test_list():
    """ return a list of test found in BUILDTEST_TESTDIR"""
    test = []

    for root, subdir, files in os.walk(config_opts['BUILDTEST_TESTDIR']):
        for file in files:
            if os.path.splitext(file)[1][1:] in BUILDTEST_SHELLTYPES:
                test.append(os.path.join(root,file))

    return test
