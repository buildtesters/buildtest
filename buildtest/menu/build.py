"""
This module contains all the methods related to "buildtest build" which is used
for building test scripts from test configuration.
"""

import logging
import os
import re
import sys

from buildtest.defaults import TESTCONFIG_ROOT, BUILDTEST_CONFIG_FILE

from buildtest.buildsystem.base import BuildConfig
from buildtest.config import load_configuration, check_configuration
from buildtest.executors.base import BuildExecutor
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
    logger = logging.getLogger(__name__)
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
        logger.debug(
            f"Config File: {config_file} is a directory so traversing directory tree to find all .yml files."
        )
        config_files = walk_tree(config_file, ".yml")
    elif os.path.isfile(config_file):
        if not re.search("[.](yaml|yml)$", config_file):
            msg = f"{config_file} does not end in file extension .yaml or .yml"
            logger.error(msg)
            sys.exit(msg)

        config_files = [config_file]
        logger.debug(f"Config File: {config_file} is a file")
    else:
        msg = (
            "Please provide an absolute or relative path to a directory file from your present working directory or %s"
            % TESTCONFIG_ROOT
        )
        logger.error(msg)
        sys.exit(msg)

    # If we don't have any files discovered
    if not config_files:
        msg = "No test configuration files found as %s." % config_file
        logger.error(msg)
        sys.exit(msg)

    # return all configs with absolute path
    tmp = [ os.path.abspath(config) for config in config_files ]
    config_files = tmp

    logger.info(f"Found the following config files: {config_files}")
    return config_files

def exclude_configs(config_files, exclude_list):
    """This method will exclude configs from being processed after discovery and
       this implements option ``buildtest build -x``. User can pass multiple
       configs to be exclude which could be a file or a directory. This method
       will return a modified list with configs that are excluded. If an invalid
       file or directory is passed to exclude_list it will be ignored.

       Parameters:

       :param config_files: List of discovered configurations
       :type config_files: list
       :param exclude_list: List of exclude configurations
       :type exclude_list: list
       :return: a modified list after discovery with excluded configurations
       :rtype: list
    """
    # if there is nothing to exclude return original list
    if not exclude_list:
        return config_files

    # check all configs exist and return a list of configs with absolute path with shell expansion.
    tmp = [ os.path.expandvars(os.path.abspath(config)) for config in exclude_list if os.path.exists(os.path.expandvars(os.path.abspath(config))) ]
    exclude_list = tmp

    # empty list to store all exclude config files
    exclude_config_files = []
    for config in exclude_list:
        # if its a directory traverse directory and find all config files with .yml extension
        if os.path.isdir(config):
            tmp = walk_tree(config, ".yml")
            exclude_config_files += tmp
        elif os.path.isfile(config):
            exclude_config_files.append(config)

    # if exclude list is empty after attempting to find all configs then return original list since nothing to return
    if not exclude_config_files:
        return config_files

    # for every exclude config see if it exist in discovered list of configs and try to remove it
    for config in exclude_config_files:
        if config in config_files:
            config_files.remove(config)

    return config_files

def func_build_subcmd(args):
    """Entry point for ``buildtest build`` sub-command. Depending on the command
    arguments, buildtest will set values in dictionary ``config_opts`` that is used
    to trigger the appropriate build action.

    :param args: arguments passed from command line
    :type args: dict, required

    :rtype: None
    """

    # buildtest logger
    logger = logging.getLogger(__name__)

    # if buildtest settings specified on CLI, it would be in args.settings otherwise set
    # to default configuration (BUILDTEST_CONFIG_FILE)
    config_file = args.settings or BUILDTEST_CONFIG_FILE

    if args.settings:
        logger.debug(
            "Detected --settings from command line so override default settings file."
        )

    logger.debug(f"Detected the following buildtest settings file: {config_file}")

    # load the configuration file
    config_opts = load_configuration(config_file)

    check_configuration(config_file)

    # Discover list of one or more config files based on path provided
    config_files = discover_configs(args.config)

    config_files = exclude_configs(config_files, args.exclude)

    if not config_files:
        msg = "There are no config files to process."
        sys.exit(msg)


    # Keep track of total metrics
    total_tests = 0
    failed_tests = 0
    passed_tests = 0

    # Load BuildExecutors
    executor = BuildExecutor(config_opts, default=args.executor)
    print(
        "{:<30} {:<30} {:<30} {:<30}".format(
            "Config Name", "SubTest", "Status", "Config Path"
        )
    )
    print("{:_<120}".format(""))
    # Each configuration file can have multiple tests
    for config_file in config_files:

        # Read in all config files here, loading each will validate the entire file
        bc = BuildConfig(config_file)

        # And builders parsed through for each
        for builder in bc.get_builders(testdir=args.testdir):

            # Keep track of total number of tests run
            total_tests += 1
            if not args.dry:
                result = executor.run(builder)

                # Update results
                if result["RETURN_CODE"] == 0:
                    passed_tests += 1
                else:
                    failed_tests += 1
            else:
                result = executor.dry_run(builder)

    if not args.dry:
        print
        print
        print("==============================================================")
        print("                         Test summary                         ")
        print(f"Executed {total_tests} tests")
        print(
            f"Passed Tests: {passed_tests}/{total_tests} Percentage: {passed_tests*100/total_tests}%"
        )
        print(
            f"Failed Tests: {failed_tests}/{total_tests} Percentage: {failed_tests*100/total_tests}%"
        )
        print
        print
