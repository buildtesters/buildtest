############################################################################
#
#  Copyright 2017-2019
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
buildtest run --system
"""

import os
import subprocess
from datetime import datetime
from buildtest.tools.config import config_opts, BUILDTEST_TEST_EXT
from buildtest.tools.file import walk_tree_multi_ext

def run_system_choices():
    """Generate choice field for buildtest run --package"""

    system_root_testdir = os.path.join(config_opts["BUILDTEST_TESTDIR"],
                                       "system")
    # if there is no directory $BUILDTEST_TESTDIR then return an empty list
    if not os.path.exists(system_root_testdir):
        return []

    systempkg_list = [ os.path.basename(f.path)
                       for f in os.scandir(system_root_testdir) if f.is_dir()]

    return systempkg_list

def run_app_choices():
    """Generate choice field for buildtest run --software"""
    root_testdir = config_opts["BUILDTEST_TESTDIR"]
    app_root_testdir = os.path.join(root_testdir,"software")

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

def run_system_test(systempkg):
    """Implementation for buildtest run --package to execute all tests in the
    test directory."""

    from buildtest.tools.run import write_system_info

    system_root_testdir = os.path.join(config_opts["BUILDTEST_TESTDIR"],
                                       "system")

    runfile = datetime.now().strftime("buildtest_%H_%M_%d_%m_%Y.run")
    run_output_file = os.path.join(config_opts["BUILDTEST_RUN_DIR"], runfile)

    fd = open(run_output_file, "w")
    write_system_info(fd, pkg_name=systempkg)
    test_destdir = os.path.join(system_root_testdir, systempkg)

    fd.write("------------------------ START OF TEST --------------------- \n")

    tests = walk_tree_multi_ext(test_destdir, BUILDTEST_TEST_EXT)

    run_tests(fd,tests, systempkg, test_destdir, run_output_file)

def run_app_test(app_name):
    """Implementation for buildtest run --software to execute all tests in the
    test directory."""
    from buildtest.tools.run import write_system_info

    app_root_testdir = os.path.join(config_opts["BUILDTEST_TESTDIR"],
                                    "software")
    test_destdir = os.path.join(app_root_testdir,app_name)

    runfile = datetime.now().strftime("buildtest_%H_%M_%d_%m_%Y.run")
    run_output_file = os.path.join(config_opts["BUILDTEST_RUN_DIR"],runfile)

    fd = open(run_output_file,"w")
    write_system_info(fd,app_name=app_name)
    fd.write("------------------START OF TEST ------------------ \n")

    tests = walk_tree_multi_ext(test_destdir, BUILDTEST_TEST_EXT)

    run_tests(fd, tests, app_name, test_destdir, run_output_file)

def run_suite(suite):
    """Implementation for buildtest run --suite to execute all tests in the
    test directory."""

    from buildtest.tools.run import write_system_info

    app_root_testdir = os.path.join(config_opts["BUILDTEST_TESTDIR"],"suite",suite)

    runfile = datetime.now().strftime("buildtest_%H_%M_%d_%m_%Y.run")

    run_output_file = os.path.join(config_opts["BUILDTEST_RUN_DIR"],runfile)

    fd = open(run_output_file,"w")
    write_system_info(fd)
    fd.write("----------- START OF TEST ---------------- \n")



    tests = walk_tree_multi_ext(app_root_testdir,BUILDTEST_TEST_EXT)

    run_tests(fd, tests, suite, app_root_testdir, run_output_file)


def run_tests(fd, tests, name, test_destdir, run_output_file):
    """This method actually runs the test and display test summary with number
    of pass/fail test and whether it passed test threshold."""
    count_test = len(tests)
    passed_test = 0
    failed_test = 0
    for test in tests:
        ret = subprocess.Popen(test,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
        output = ret.communicate()[0].decode("utf-8")

        ret_code = ret.returncode
        fd.write("Test Name:" + test + "\n")
        fd.write("Return Code: " + str(ret_code) + "\n")
        fd.write("---------- START OF TEST OUTPUT ---------------- \n")
        fd.write(output)
        fd.write("------------ END OF TEST OUTPUT ---------------- \n")

        if ret_code == 0:
            passed_test += 1
        else:
            failed_test += 1

    print (f"Running All Tests from Test Directory: {test_destdir}")
    print
    print
    print("==============================================================")
    print("                         Test summary                         ")
    print("Package: ", name)
    print(f"Executed {count_test} tests")
    print(f"Passed Tests: {passed_test} Percentage: {passed_test*100/count_test}%")
    print(f"Failed Tests: {failed_test} Percentage: {failed_test*100/count_test}%")

    actual_ratio = passed_test/count_test
    success_threshold = float(config_opts['BUILDTEST_SUCCESS_THRESHOLD'])


    print
    print
    diff_ratio = abs(actual_ratio-success_threshold)
    if actual_ratio < success_threshold:
        print (f"WARNING: Threshold of {success_threshold*100}% was not satisfied")
        print (f"{name} has a {actual_ratio*100}% passed rate with a "
               + f"difference of {diff_ratio:.4} from the threshold" )
    else:
        print (f"SUCCESS: Threshold of {success_threshold*100}% was achieved")

    print ("Writing results to " + run_output_file)
    fd.close()
