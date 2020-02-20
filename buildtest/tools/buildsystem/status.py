"""
This module implements methods for querying status details of previous
builds by buildtest. This includes a summary of all builds, number of test and
command executed along with build ID. The build ID can be used to retrieve log files
and test scripts that were generated.
"""

import json
import os
import subprocess
from datetime import datetime
from buildtest.tools.config import config_opts, BUILDTEST_BUILD_LOGFILE
from buildtest.tools.file import create_dir


def show_status_report(args=None):
    """
    This method displays history of builds conducted by buildtest. This method
    implements command ``buildtest build report``.

    :param args: command line arguments passed to buildtest
    :type args: dict, required
    """

    fd = open(BUILDTEST_BUILD_LOGFILE, "r")
    content = json.load(fd)
    fd.close()

    print(
        "{:3} | {:<20} | {:<15} | {:<60} ".format(
            "ID", "Build Time", "Number of Tests", "Command"
        )
    )

    print("{:-<120}".format(""))
    count = 0

    for build_id in content["build"].keys():

        print(
            "{:3} | {:<20} | {:<15} | {:<60} ".format(
                count,
                content["build"][build_id]["BUILD_TIME"],
                content["build"][build_id]["TESTCOUNT"],
                content["build"][build_id]["CMD"],
                content["build"][build_id]["LOGFILE"],
            )
        )
        count += 1

def get_build_ids():
    """Return a list of build ids. This can be retrieved by getting length
    of "build:" key and pass it to range() method to return a list. Build IDs
    start from 0. This method is used as choice field in add_argument() method

    :return: return a list of numbers  that represent build id
    :rtype: list
    """
    if not os.path.exists(BUILDTEST_BUILD_LOGFILE):
        return []

    fd = open(BUILDTEST_BUILD_LOGFILE, "r")
    content = json.load(fd)
    fd.close()
    total_records = len(content["build"])
    return range(total_records)


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
    return total_records
