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

This module will run an entire test suite for an application. This implements
_buildtest run --app

:author: Shahzeb Siddiqui

"""

import os
import sys
from buildtest.tools.config import config_opts, BUILDTEST_SHELLTYPES
def run_app_choices():
    """
    generate choice field for _buildtest run --app
    """
    root_testdir = config_opts["BUILDTEST_TESTDIR"]
    app_root_testdir = os.path.join(root_testdir,"ebapp")

    # if there is no directory $BUILDTEST_TESTDIR then return an empty list
    if not os.path.exists(app_root_testdir):
        return []
    app_name_list = [ f.path for f in os.scandir(app_root_testdir) if f.is_dir()]

    app_choices_fullpath = []
    for app in app_name_list:
        app_ver_list = [ f.path for f in os.scandir(app) if f.is_dir()]
        if len(app_ver_list) > 0:
            app_choices_fullpath += app_ver_list

    app_choices = []
    for path in app_choices_fullpath:
        name = os.path.basename(os.path.dirname(path))
        ver = os.path.basename(path)

        app_choices.append(os.path.join(name,ver))

    return app_choices

def run_app_test(app_name):
    """
    implementation for _buildtest run --app to execute all tests in the test directory
    """

    app_root_testdir = os.path.join(config_opts["BUILDTEST_TESTDIR"],"ebapp")

    tests = [ f.path for f in os.scandir(os.path.join(app_root_testdir,app_name)) if os.path.splitext(f)[1] in [".sh", ".bash", ".csh"]]

    count_test = len(tests)

    for test in tests:
        print (f"Executing Test: {test}")
        print ("---------------------------------------------------------")
        os.system(test)
        print ("---------------------------------------------------------")

    print (f"Executed {count_test} tests for software: {app_name}")
