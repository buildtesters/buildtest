"""
This module contains all the methods related to "buildtest build" which is used
for building test scripts from test configuration.
"""

import json
import os
import shutil
import sys

from buildtest.defaults import (
    BUILDTEST_BUILD_HISTORY,
    BUILDTEST_BUILD_LOGFILE,
    TESTCONFIG_ROOT,
)

from buildtest.buildsystem.base import BuildConfig
from buildtest.utils.file import walk_tree


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

    # If no config file provided, assume discovering across buildtest/site
    if not config_file:
        config_file = TESTCONFIG_ROOT

    # First try, the path is an absolute path to file or folder
    # Second try, the path can be relative to the TESTCONFIG_ROOT
    elif not os.path.exists(config_file):
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

    # Discover list of one or more config files based on path provided
    config_files = discover_configs(args.config)

    # Read in all config files here, loading each will validate the entire file
    # TODO: allow some level of skipping invalid files, an argument?
    for config_file in config_files:
        bc = BuildConfig(config_file)

    # Keep track of total metrics
    total_tests = 0
    failed_tests = 0
    passed_tests = 0

    # Each configuration file can have multiple tests
    for config_file in config_files:

        # Each configuration file can be loaded as a BuildConfig
        bc = BuildConfig(config_file)

        # And builders parsed through for each
        for builder in bc.get_builders():

            # Keep track of total number of tests run
            total_tests += 1
            if not args.dry:
                result = builder.run()

                # Update results
                if result["RETURN_CODE"] == 0:
                    passed_tests += 1
                else:
                    failed_tests += 1
            else:
                result = builder.dry_run()

            # Update build history
            BUILDTEST_BUILD_HISTORY[result["BUILD_ID"]] = result

    if not args.dry:
        print(f"Finished running {total_tests} total tests.")
        print
        print
        print("==============================================================")
        print("                         Test summary                         ")
        print(f"Executed {total_tests} tests")
        print(
            f"Passed Tests: {passed_tests} Percentage: {passed_tests*100/total_tests}%"
        )
        print(
            f"Failed Tests: {failed_tests} Percentage: {failed_tests*100/total_tests}%"
        )
        print
        print


def clear_builds():
    """This method clears the build history and removes all tests. This implements command ``buildtest build --clear``"""
    # TODO: refactor this so it uses modular functions shared from somewhere else
    if os.path.isfile(BUILDTEST_BUILD_LOGFILE):
        os.remove(BUILDTEST_BUILD_LOGFILE)
    if os.path.isdir(config_opts["build"]["testdir"]):
        shutil.rmtree(config_opts["build"]["testdir"])

    print("Clearing Build History")
    build_dict = {"build": {}}
    with open(BUILDTEST_BUILD_LOGFILE, "w") as outfile:
        json.dump(build_dict, outfile, indent=2)
