"""
This module contains all the methods related to "buildtest build" which is used
for building test scripts from test configuration.
"""


import json
import os
import shutil
import sys
import subprocess
from datetime import datetime

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

        # First try, the user can provide a full path
        config_file = args.config

        # Second try, the path can be relative to the TESTCONFIG_ROOT
        if not os.path.exists(config_file):
            config_file = os.path.join(TESTCONFIG_ROOT, config_file)

        if not os.path.exists(config_file):
            sys.exit(
                "Please provide an absolute path, or path relative to %s"
                % TESTCONFIG_ROOT
            )

        config_file = os.path.abspath(config_file)
        singlesource_test = SingleSource(
            config_file, args.collection, args.module_collection
        )
        content = singlesource_test.build_test_content()

        if args.dry:
            dry_view(content)
        else:
            write_test(content)

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

        with open(BUILDTEST_BUILD_LOGFILE, "r") as fd:
            build_dict = json.load(fd)

        build_dict["build"][build_id] = BUILDTEST_BUILD_HISTORY[build_id]
        logger.debug("Adding latest build to dictionary")
        logger.debug(f"{BUILDTEST_BUILD_HISTORY[build_id]}")
        logger.info(f"Updating Build Log File: {BUILDTEST_BUILD_LOGFILE}")

        with open(BUILDTEST_BUILD_LOGFILE, "w") as fd:
            json.dump(build_dict, fd, indent=4)

        run_tests(build_id)


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


def run_tests(build_id):
    """This method actually runs the test and display test summary"""

    with open(BUILDTEST_BUILD_LOGFILE, "r") as fd:
        content = json.load(fd)

    tests = content["build"][str(build_id)]["TESTS"]

    # all tests are in same directory, retrieving parent directory of test
    test_dir = content["build"][str(build_id)]["TESTDIR"]

    runfile = datetime.now().strftime("buildtest_%H_%M_%d_%m_%Y.run")
    run_output_file = os.path.join(test_dir, "run", runfile)
    create_dir(os.path.join(test_dir, "run"))

    count_test = len(tests)
    passed_test = 0
    failed_test = 0

    with open(run_output_file, "w") as fd:
        for test in tests:
            ret = subprocess.Popen(
                test, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
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

    print(f"Running All Tests from Test Directory: {test_dir}")
    print
    print
    print("==============================================================")
    print("                         Test summary                         ")
    print(f"Executed {count_test} tests")
    print(f"Passed Tests: {passed_test} Percentage: {passed_test*100/count_test}%")
    print(f"Failed Tests: {failed_test} Percentage: {failed_test*100/count_test}%")
    print
    print
    print("Writing results to " + run_output_file)
