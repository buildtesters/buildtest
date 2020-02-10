"""
This module contains all the methods related to "buildtest build" which is used
for building test scripts from test configuration.
"""

from datetime import datetime
import json
import os
import shutil
import sys


from buildtest.tools.config import (
    config_opts,
    BUILDTEST_BUILD_HISTORY,
    BUILDTEST_BUILD_LOGFILE,
    BUILDTEST_SYSTEM,
    TESTCONFIG_ROOT,
)

from buildtest.tools.buildsystem.singlesource import SingleSource
from buildtest.tools.buildsystem.dry import dry_view
from buildtest.tools.file import create_dir
from buildtest.tools.log import init_log
from buildtest.tools.buildsystem.status import get_total_build_ids
from buildtest.tools.writer import write_test


def func_build_subcmd(args):
    """Entry point for ``buildtest build`` sub-command. Depending on the command
    arguments, buildtest will set values in dictionary ``config_opts`` that is used
    to trigger the appropriate build action.

    :param args: arguments passed from command line
    :type args: dict, required

    :rtype: None
    """

    build_id = get_total_build_ids()
    BUILDTEST_BUILD_HISTORY[build_id] = {}
    BUILDTEST_BUILD_HISTORY[build_id]["TESTS"] = []

    if args.clear:
        clear_builds()
        sys.exit(0)
    fd = open(BUILDTEST_SYSTEM,"r")
    system = json.load(fd)
    fd.close()
    test_subdir = os.path.join(
        system["VENDOR"],
        system["ARCH"],
        system["PROCESSOR_FAMILY"],
        system["OS_NAME"],
        system["OS_VERSION"],
        f"build_{str(build_id)}",
    )

    config_opts["build"]["testdir"] = os.path.join(
        config_opts["build"]["testdir"], test_subdir
    )
    if not args.dry:
        create_dir(config_opts["build"]["testdir"])
        BUILDTEST_BUILD_HISTORY[build_id]["TESTDIR"] = config_opts["build"]["testdir"]

    logger, LOGFILE = init_log()
    logger.info(f"Opening File: {BUILDTEST_SYSTEM} and loading as JSON object")
    logger.info(f"Creating Directory: {config_opts['build']['testdir']}")
    logger.debug(f"Current build ID: {build_id}")

    if args.config:

        file = os.path.join(TESTCONFIG_ROOT, args.config)

        # print content of test configuration in verbose>=1
        if args.verbose >= 1:
            fd = open(file, "r")
            content = fd.read()
            print("{:_<80}".format(""))
            print(content)
            print("{:_<80}".format(""))
            fd.close()

        singlesource_test = SingleSource(file,args.collection,args.module_collection)
        content = singlesource_test.build_test_content()

        if args.dry:
            dry_view(content)
        else:
            write_test(content, args.verbose)

    if not args.dry:
        print("Writing Log file to: ", LOGFILE)

        BUILD_TIME = datetime.now().strftime("%m/%d/%Y %X")

        BUILDTEST_BUILD_HISTORY[build_id]["TESTCOUNT"] = len(
            BUILDTEST_BUILD_HISTORY[build_id]["TESTS"]
        )
        BUILDTEST_BUILD_HISTORY[build_id]["CMD"] = "buildtest " + " ".join(
            str(arg) for arg in sys.argv[1:]
        )

        BUILDTEST_BUILD_HISTORY[build_id]["BUILD_TIME"] = BUILD_TIME
        BUILDTEST_BUILD_HISTORY[build_id]["LOGFILE"] = LOGFILE

        logger.info(f"Reading Build Log File: {BUILDTEST_BUILD_LOGFILE}")

        fd = open(BUILDTEST_BUILD_LOGFILE, "r")
        build_dict = json.load(fd)
        fd.close()
        build_dict["build"][build_id] = BUILDTEST_BUILD_HISTORY[build_id]
        logger.debug("Adding latest build to dictionary")
        logger.debug(f"{BUILDTEST_BUILD_HISTORY[build_id]}")
        logger.info(f"Updating Build Log File: {BUILDTEST_BUILD_LOGFILE}")
        fd = open(BUILDTEST_BUILD_LOGFILE, "w")
        json.dump(build_dict, fd, indent=4)
        fd.close()


def clear_builds():
    """This method clears the build history and removes all tests. This implements command ``buildtest build --clear``"""
    if os.path.isfile(BUILDTEST_BUILD_LOGFILE):
        os.remove(BUILDTEST_BUILD_LOGFILE)
    if os.path.isdir(config_opts["build"]["testdir"]):
        shutil.rmtree(config_opts["build"]["testdir"])

    print("Clearing Build History")
    build_dict = {"build": {}}
    with open(BUILDTEST_BUILD_LOGFILE, "w") as outfile:
        json.dump(build_dict, outfile, indent=2)
