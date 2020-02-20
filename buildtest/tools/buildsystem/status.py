"""
This module implements methods for querying status details of previous
builds by buildtest. This includes a summary of all builds, number of test and
command executed along with build ID. The build ID can be used to retrieve log files
and test scripts that were generated.
"""

import json
from buildtest.tools.config import BUILDTEST_BUILD_LOGFILE


def show_status_report(args=None):
    """
    This method displays history of builds conducted by buildtest. This method
    implements command ``buildtest build report``.

    :param args: command line arguments passed to buildtest
    :type args: dict, required
    """

    with open(BUILDTEST_BUILD_LOGFILE, "r") as fd:
        content = json.load(fd)

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


def get_total_build_ids():
    """Return a total count of build ids. This can be retrieved by getting length
    of "build:" key. Build IDs start from 0.

    :return: return a list of numbers  that represent build id
    :rtype: list
    """

    with open(BUILDTEST_BUILD_LOGFILE, "r") as fd:
        content = json.load(fd)

    total_records = len(content["build"])
    return total_records
