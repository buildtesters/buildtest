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
This module implements methods for querying status details of previous
builds by buildtest. This includes a summary of all builds, number of test and
command executed along with build ID. The build ID can be used to retrieve log files
and test scripts that were generated.
"""

import json
import os
from buildtest.tools.config import BUILDTEST_BUILD_LOGFILE

def show_status_report(args):
    """
    This method displays history of builds conducted by buildtest. This method
    implements command ``buildtest status report``.

    :param args: command line arguments passed to buildtest
    :type args: dict, required
    """
    fd = open(BUILDTEST_BUILD_LOGFILE,"r")
    content = json.load(fd)
    fd.close()

    print ('{:3} | {:<20} | {:<15} | {:<60} '.format("ID","Build Time","Number of Tests","Command"))

    print('{:-<160}'.format(""))
    count = 0

    for build_id in content["build"].keys():

        print ('{:3} | {:<20} | {:<15} | {:<60} '.format(count,
                                                         content["build"][build_id]["BUILD_TIME"],
                                                         content["build"][build_id]["TESTCOUNT"],
                                                         content["build"][build_id]["CMD"],
                                                         content["build"][build_id]["LOGFILE"]))
        count += 1

def get_build_ids():
    """Return a list of build ids. This can be retrieved by getting length
    of "build:" key and pass it to range() method to return a list. Build IDs
    start from 0. This method is used as choice field in add_argument() method

    :return: return a list of numbers  that represent build id
    :rtype: list
    """

    fd = open(BUILDTEST_BUILD_LOGFILE, "r")
    content = json.load(fd)
    fd.close()
    total_records = len(content["build"])
    return (range(total_records))


def get_total_build_ids():
    """Return a total count of build ids. This can be retrieved by getting length
    of "build:" key. Build IDs start from 0.

    :return: return a list of numbers  that represent build id
    :rtype: list
    """

    fd = open(BUILDTEST_BUILD_LOGFILE, "r")
    content = json.load(fd)
    fd.close()
    total_records = len(content["build"])
    return (total_records)

def show_status_log(args):
    """This method opens log file using "less" by reading build.json
    and fetching log file based on build id. This method implements
    ``buildtest status log``.

    :param args: command arguments passed to buildtest
    :type args: dict, required
    """
    fd = open(BUILDTEST_BUILD_LOGFILE, "r")
    content = json.load(fd)
    fd.close()

    logfile = content["build"][str(args.id)]["LOGFILE"]
    query = f"less {logfile}"
    os.system(query)


def show_status_test(args):
    """ This method list tests generated from a build ID. This method
    implements ``buildtest status test``

    :param args: command line argument passed to buildtest
    :type args: dict, required
    """

    fd = open(BUILDTEST_BUILD_LOGFILE, "r")
    content = json.load(fd)
    fd.close()

    tests = content["build"][str(args.id)]["TESTS"]
    [print (test) for test in tests]
