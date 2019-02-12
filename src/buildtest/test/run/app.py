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

This module will run an entire test suite for an application. This implements
_buildtest run --software

"""

import os
import subprocess
import sys
from datetime import datetime

from buildtest.tools.config import config_opts, BUILDTEST_SHELLTYPES

def run_app_choices():
    """generate choice field for buildtest run --app"""
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
    """implementation for _buildtest run --app to execute all tests in the test directory"""
    from buildtest.tools.run import write_system_info

    app_root_testdir = os.path.join(config_opts["BUILDTEST_TESTDIR"],"ebapp")

    runfile = datetime.now().strftime("buildtest_%H_%M_%d_%m_%Y.run")
    run_output_file = os.path.join(config_opts["BUILDTEST_RUN_DIR"],runfile)

    fd = open(run_output_file,"w")
    write_system_info(fd,app_name=app_name)
    fd.write("------------------------ START OF TEST -------------------------------------- \n")


    tests = []
    # traverse test directory tree and add tests to a list object
    for root, subdir, files in os.walk(os.path.join(app_root_testdir,app_name)):
        for file in files:
            # only add test with valid shell extensions
            if os.path.splitext(file)[1] in [".sh", ".bash", ".csh"]:
                tests.append(os.path.join(root,file))


    count_test = len(tests)

    passed_test = 0
    failed_test = 0
    for test in tests:

        ret = subprocess.Popen(test,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        output = ret.communicate()[0]
        output=output.decode("utf-8")


        ret_code = ret.returncode
        fd.write("Test Name:" + test + "\n")
        fd.write("Return Code: " + str(ret_code) + "\n")
        fd.write("---------- START OF TEST OUTPUT ---------------- \n")
        fd.write(output)
        fd.write("------------ END OF TEST OUTPUT ---------------- \n")


        if ret_code == 0:
            passed_test += 1
        else:
            failed_test +=1

    print
    print
    print("==============================================================")
    print("                         Test summary                         ")
    print("Application: ", app_name)
    print("Executed " + str(count_test) + " tests")
    print("Passed Tests: " + str(passed_test) +  " Percentage: " + str(passed_test*100/count_test) + "%")
    print("Failed Tests: " + str(failed_test) + "  Percentage: " + str(failed_test*100/count_test) + "%")

    actual_ratio = passed_test/count_test
    success_threshold = float(config_opts['BUILDTEST_SUCCESS_THRESHOLD'])


    print
    print
    diff_ratio = abs(actual_ratio-success_threshold)
    if actual_ratio < success_threshold:
        print ("WARNING: Threshold of " + str(success_threshold*100) + "% was not achieved by " + app_name)
        print (app_name  + " has a " + str(actual_ratio*100) + "% passed rate with a difference of " + str(diff_ratio) + " from the threshold" )
    else:
        print ("SUCCESS: Threshold of " + str(success_threshold*100) + "% was achieved")

    print ("Writing results to " + run_output_file)
    fd.close()

def run_suite(suite):
    """implementation for buildtest run --suite to execute all tests in the test directory"""
    from buildtest.tools.run import write_system_info

    app_root_testdir = os.path.join(config_opts["BUILDTEST_TESTDIR"],"suite",suite)


    runfile = datetime.now().strftime("buildtest_%H_%M_%d_%m_%Y.run")
    run_output_file = os.path.join(config_opts["BUILDTEST_RUN_DIR"],runfile)

    fd = open(run_output_file,"w")
    write_system_info(fd)
    fd.write("------------------------ START OF TEST -------------------------------------- \n")


    tests = []
    # traverse test directory tree and add tests to a list object
    for root, subdir, files in os.walk(app_root_testdir):
        for file in files:
            # only add test with valid shell extensions
            if os.path.splitext(file)[1] in [".sh", ".bash", ".csh"]:
                tests.append(os.path.join(root,file))


    count_test = len(tests)

    passed_test = 0
    failed_test = 0

    for test in tests:

        ret = subprocess.Popen(test,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        output = ret.communicate()[0]
        output=output.decode("utf-8")


        ret_code = ret.returncode
        fd.write("Test Name:" + test + "\n")
        fd.write("Return Code: " + str(ret_code) + "\n")
        fd.write("---------- START OF TEST OUTPUT ---------------- \n")
        fd.write(output)
        fd.write("------------ END OF TEST OUTPUT ---------------- \n")


        if ret_code == 0:
            passed_test += 1
        else:
            failed_test +=1

    print
    print
    print("==============================================================")
    print("                         Test summary                         ")
    print("Executed " + str(count_test) + " tests")
    print("Passed Tests: " + str(passed_test) +  " Percentage: " + str(passed_test*100/count_test) + "%")
    print("Failed Tests: " + str(failed_test) + "  Percentage: " + str(failed_test*100/count_test) + "%")

    actual_ratio = passed_test/count_test
    success_threshold = float(config_opts['BUILDTEST_SUCCESS_THRESHOLD'])


    print
    print
    diff_ratio = abs(actual_ratio-success_threshold)
    if actual_ratio < success_threshold:
        print ("WARNING: Threshold of " + str(success_threshold*100) + "% was not achieved by " + suite)
        print (" Current Results are " + str(actual_ratio*100) + "% passed rate with a difference of " + str(diff_ratio) + " from the threshold" )
    else:
        print ("SUCCESS: Threshold of " + str(success_threshold*100) + "% was achieved")

    print ("Writing results to " + run_output_file)
    fd.close()
