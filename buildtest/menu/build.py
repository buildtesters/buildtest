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
from buildtest.utils.file import walk_tree, resolve_path

logger = logging.getLogger(__name__)


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

    # return all configs by resolving path, this gets the real canonical path and address shell expansion and user expansion
    config_files = [resolve_path(config) for config in config_files]

    logger.info(f"Found the following config files: {config_files}")
    return config_files


def include_file(file_path, white_list_patterns):
    """Check if file is included based on OR regular expression. If no white_list_patterns
       provided method will return ``True``. Otherwise it will return the list of files that don't
       match the regular expression

       Parameters:

       :param file_path: file path to run regular expression upon
       :type file_path: str, required
       :param white_list_patterns: the exclude list provided on command line option
       :type white_list_patterns: list, required
       :return: Returns True or a list of files that don't match regular expression
       :rtype: bool or str
    """

    if not white_list_patterns:
        logger.debug("No white list patterns provided, returning True")
        return True

    logger.debug(f"white list pattern before resolving paths: {white_list_patterns}")

    white_list_patterns = [resolve_path(path) for path in white_list_patterns]

    logger.debug(f"white list pattern after resolving paths: {white_list_patterns}")

    regexp = "(%s)" % "|".join(white_list_patterns)
    logger.debug(f"Applying Regular Expression Search: {regexp} to file: {file_path}")

    return not re.search(regexp, file_path)


def func_build_subcmd(args):
    """Entry point for ``buildtest build`` sub-command. Depending on the command
       arguments, buildtest will set values in dictionary ``config_opts`` that is used
       to trigger the appropriate build action.

       Parameters:

       :param args: arguments passed from command line
       :type args: dict, required

       :rtype: None
    """

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

    # if no files discovered let's stop now
    if not config_files:
        msg = "There are no config files to process."
        sys.exit(msg)

    print("\n {:^45} \n".format("Discovered Files"))
    [print(config) for config in config_files]
    print("\n\n")

    logger.debug(
        f"Based on input argument: -c {args.config} buildtest discovered the following configuration {config_files}"
    )

    if args.exclude:
        logger.debug(f"The exclude config pattern are the following: -e {args.exclude}")
        config_files = [
            config for config in config_files if include_file(config, args.exclude)
        ]
        logger.debug(f"Configuration List after applying exclusion: {config_files}")

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
        print("\n\n{:=<60}".format(""))
        print("{:^60}".format("Test summary"))
        print("{:=<60}".format(""))
        print(f"Executed {total_tests} tests")

        pass_rate = passed_tests * 100 / total_tests
        fail_rate = failed_tests * 100 / total_tests

        print(
            f"Passed Tests: {passed_tests}/{total_tests} Percentage: {pass_rate:.3f}%"
        )

        print(
            f"Failed Tests: {failed_tests}/{total_tests} Percentage: {fail_rate:.3f}%"
        )
        print
        print
