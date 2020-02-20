"""
This module contains all the methods related to "buildtest build" which is used
for building test scripts from test configuration.
"""

from datetime import datetime
import json
import os
import shutil
import sys


from buildtest.tools.config import config_opts
from buildtest.tools.defaults import (
    BUILDTEST_BUILD_HISTORY,
    BUILDTEST_BUILD_LOGFILE,
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
    cmd_executed = "buildtest " + " ".join(str(arg) for arg in sys.argv[1:])

    if args.clear:
        clear_builds()
        sys.exit(0)

    BUILD_TIME = datetime.now().strftime("%m/%d/%Y %X")

    config_opts["build"]["testdir"] = os.path.join(
        config_opts["build"]["testdir"], f"build_{str(build_id)}"
    )
    if not args.dry:
        create_dir(config_opts["build"]["testdir"])
        BUILDTEST_BUILD_HISTORY[build_id]["TESTDIR"] = config_opts["build"]["testdir"]

    logger, LOGFILE = init_log(config_opts)
    logger.info(f"Creating Directory: {config_opts['build']['testdir']}")
    logger.debug(f"Current build ID: {build_id}")

    print("{:_<80}".format(""))
    print("{:>40} {}".format("build time:", BUILD_TIME))
    print("{:>40} {}".format("command:", cmd_executed))
    print("{:>40} {}".format("test configuration root:", TESTCONFIG_ROOT))
    print("{:>40} {}".format("configuration file:", args.config))
    print("{:>40} {}".format("buildpath:", config_opts["build"]["testdir"]))
    print("{:>40} {}".format("logpath:", LOGFILE))
    print("{:_<80}".format(""))

    print("\n\n")
    print("{:<40} {}".format("STAGE", "VALUE"))
    print("{:_<80}".format(""))
    if args.config:

        file = os.path.join(TESTCONFIG_ROOT, args.config)

        singlesource_test = SingleSource(
            file, args.collection, args.module_collection, args.verbose
        )
        content = singlesource_test.build_test_content()

        if args.dry:
            dry_view(content)
        else:
            write_test(content, args.verbose)

    print("{:<40} {}".format("[WRITING TEST]", "PASSED"))
    if not args.dry:

        BUILDTEST_BUILD_HISTORY[build_id]["TESTCOUNT"] = len(
            BUILDTEST_BUILD_HISTORY[build_id]["TESTS"]
        )
        print(
            "{:<40} {}".format(
                "[NUMBER OF TEST]", BUILDTEST_BUILD_HISTORY[build_id]["TESTCOUNT"]
            )
        )
        BUILDTEST_BUILD_HISTORY[build_id]["CMD"] = cmd_executed

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
