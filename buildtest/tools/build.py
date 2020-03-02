"""
This module contains all the methods related to "buildtest build" which is used
for building test scripts from test configuration.
"""

from copy import deepcopy
from datetime import datetime
import json
import os
import shutil
import sys
import subprocess

from buildtest.tools.config import config_opts
from buildtest.tools.defaults import (
    BUILDTEST_BUILD_HISTORY,
    BUILDTEST_BUILD_LOGFILE,
    TESTCONFIG_ROOT,
)

from buildtest.tools.buildsystem.singlesource import SingleSource
from buildtest.tools.buildsystem.dry import dry_view
from buildtest.tools.file import create_dir, walk_tree
from buildtest.tools.log import init_log
from buildtest.tools.buildsystem.status import get_total_build_ids
from buildtest.tools.writer import write_test


def discover_configs(config_file):
    """Given a config file specified by the user with buildtest build -c,
       discover one or more files and return a list for buildtest to parse.
       Examples of intended functionality are documented here. For all of
       the below, test config root refers to $HOME/.buildtest/site
 
       # A relative path to a file in the PWD (outside of test config root, returns single)
       buildtest build -c relative-folder/hello.sh.yml

       # A relative path to a file in build test root (returns single)
       buildtest build -c buildtest build -c github.com/HPC-buildtest/tutorials/hello-world/hello.sh.ym

       # relative directory path (returns multiple)
       buildtest build -c hello-world

       # relative directory path in build test root (returns multiple)
       buildtest build -c github.com/HPC-buildtest/tutorials/hello-world/
    """
    config_files = []

    # First try, the path is an absolute path to file or folder
    # Second try, the path can be relative to the TESTCONFIG_ROOT
    if not os.path.exists(config_file):
        config_file = os.path.join(TESTCONFIG_ROOT, config_file)

    # Now handle path based on being a directory or file path
    if os.path.isdir(config_file):
        config_files = walk_tree(config_file, ".yml")
    elif os.path.isfile(config_file):
        config_files = [config_file]
    else:
        sys.exit(
            "Please provide an absolute or relative path to a directory file ",
            "from your present working directory or %s" % TESTCONFIG_ROOT,
        )

    # If we don't have any files discovered
    if not config_files:
        sys.exit("No test configuration files found as %s." % config_file)

    return config_files


def func_build_subcmd(args):
    """Entry point for ``buildtest build`` sub-command. Depending on the command
    arguments, buildtest will set values in dictionary ``config_opts`` that is used
    to trigger the appropriate build action.

    :param args: arguments passed from command line
    :type args: dict, required

    :rtype: None
    """
    if args.clear:
        clear_builds()
        sys.exit(0)

    if args.config:

        # Discover list of one or more config files based on path provided
        config_files = discover_configs(args.config)

    # TODO: read in all config files here, validate
    # There could be a yaml file that isn't a recipe, so they should be removed

    # Keep track of total metrics
    total_tests = 0

    for config_file in config_files:

        build_id = get_total_build_ids()
        BUILDTEST_BUILD_HISTORY[build_id] = {}
        BUILDTEST_BUILD_HISTORY[build_id]["TESTS"] = []
        cmd_executed = "buildtest " + " ".join(str(arg) for arg in sys.argv[1:])

        # Create a deep copy of config_opts for the build file
        options = deepcopy(config_opts)
        config_file = os.path.abspath(config_file)

        # TODO: derive type based on config type
        singlesource_test = SingleSource(config_file)
        content = singlesource_test.build_test_content()

        if args.dry:
            dry_view(content)
        else:
            write_test(content)

        BUILD_TIME = datetime.now().strftime("%m/%d/%Y %X")

        options["build"]["testdir"] = os.path.join(
            options["build"]["testdir"], f"build_{str(build_id)}"
        )
        if not args.dry:
            create_dir(options["build"]["testdir"])
            BUILDTEST_BUILD_HISTORY[build_id]["TESTDIR"] = options["build"]["testdir"]

        logger, LOGFILE = init_log(options)
        logger.info(f"Creating Directory: {options['build']['testdir']}")
        logger.debug(f"Current build ID: {build_id}")

        print("{:_<80}".format(""))
        print("{:>40} {}".format("build time:", BUILD_TIME))
        print("{:>40} {}".format("command:", cmd_executed))
        print("{:>40} {}".format("test configuration root:", TESTCONFIG_ROOT))
        print("{:>40} {}".format("configuration file:", args.config))
        print("{:>40} {}".format("buildpath:", options["build"]["testdir"]))
        print("{:>40} {}".format("logpath:", LOGFILE))
        print("{:_<80}".format(""))

        print("\n\n")
        print("{:<40} {}".format("STAGE", "VALUE"))
        print("{:_<80}".format(""))

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
            total_tests += BUILDTEST_BUILD_HISTORY[build_id]["TESTCOUNT"]

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
