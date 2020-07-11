"""
This module contains all the methods related to "buildtest build" which is used
for building test scripts from a Buildspec
"""

import logging
import os
import re
import sys
import time
from jsonschema.exceptions import ValidationError
from buildtest.defaults import BUILDSPEC_DEFAULT_PATH

from buildtest.buildsystem.base import BuildspecParser
from buildtest.config import load_settings, check_settings
from buildtest.executors.base import BuildExecutor
from buildtest.menu.repo import get_repo_paths
from buildtest.menu.report import update_report
from buildtest.utils.file import walk_tree, resolve_path

logger = logging.getLogger(__name__)


def discover_buildspecs(buildspec):
    """Given a buildspec file specified by the user with ``buildtest build --buildspec``,
       discover one or more files and return a list for buildtest to parse.
       Examples of intended functionality are documented here. For all of
       the below, test config root refers to $HOME/.buildtest/site
 
       # A relative path to a file in the PWD (outside of test config root, returns single)
       buildtest build --buildspec relative-folder/hello.sh.yml

       # A relative path to a file in build test root (returns single)
       buildtest build --buildspec github.com/buildtesters/tutorials/hello-world/hello.sh.yml

       # relative directory path (returns multiple)
       buildtest build --buildspec hello-world

       # relative directory path in build test root (returns multiple)
       buildtest build --buildspec github.com/buildtesters/tutorials/hello-world/
    """

    buildspecs = []
    search_path = get_repo_paths() or []
    # add default path to search path
    search_path.append(BUILDSPEC_DEFAULT_PATH)

    # First try, the path is an absolute path to file or folder
    # Second try, the path can be relative to the BUILDSPEC_DEFAULT_PATH
    if not os.path.exists(buildspec):
        # find the first valid buildspec path from the list of search paths
        for path in search_path:
            if os.path.exists(os.path.join(path, buildspec)):
                buildspec = os.path.join(path, buildspec)
                break

    # Now handle path based on being a directory or file path
    if os.path.isdir(buildspec):
        logger.debug(
            f"Buildspec File: {buildspec} is a directory so traversing directory tree to find all Buildspec files with .yml extension"
        )
        buildspecs = walk_tree(buildspec, ".yml")
    elif os.path.isfile(buildspec):
        if not re.search("[.](yaml|yml)$", buildspec):
            msg = f"{buildspec} does not end in file extension .yaml or .yml"
            logger.error(msg)
            sys.exit(msg)

        buildspecs = [buildspec]
        logger.debug(f"BuildSpec: {buildspec} is a file")
    else:
        msg = (
            f"Unable to find any buildspecs in search paths: {search_path} \n"
            + "Please provide an absolute or relative path to a directory or file relative to current directory."
        )

        logger.error(msg)
        sys.exit(msg)

    # If we don't have any files discovered
    if not buildspecs:
        msg = "No Buildspec files found as %s." % buildspecs
        logger.error(msg)
        sys.exit(msg)

    # return all buildspec by resolving path, this gets the real canonical path and address shell expansion and user expansion
    buildspecs = [resolve_path(file) for file in buildspecs]

    logger.info(f"Found the following config files: {buildspecs}")
    return buildspecs


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


def func_build_subcmd(args, config_opts):
    """Entry point for ``buildtest build`` sub-command. This method will discover
       Buildspecs in method ``discover_buildspecs``. If there is an exclusion list
       this will be checked, once buildtest knows all Buildspecs to process it will
       begin validation by calling ``BuildspecParser`` and followed by an executor
       instance by invoking BuildExecutor that is responsible for executing the
       test based on the executor type. A report of all builds, along with test summary
       will be displayed to screen.

       Parameters:

       :param args: arguments passed from command line
       :type args: dict, required

       :rtype: None
    """

    # if buildtest settings specified on CLI, it would be in args.settings otherwise set
    # to default configuration (BUILDTEST_SETTINGS_FILE)

    if args.settings:
        logger.debug(
            "Detected --settings from command line so override default settings file."
        )

        # load the user's buildtest settings file
        config_opts = load_settings(args.settings)

        # check user's buildtest setting for any errors by validating against settings schema
        check_settings(args.settings)

    prefix = config_opts.get("config", {}).get("paths", {}).get("prefix")
    # variable to set test directory if prefix is set
    prefix_testdir = None
    if prefix:
        prefix = resolve_path(prefix)
        if prefix:
            prefix_testdir = os.path.join(prefix, "tests")

    config_paths_testdir = config_opts.get("config", {}).get("paths", {}).get("testdir")

    # if testdir defined in configuration file get realpath
    if config_paths_testdir:
        config_paths_testdir = resolve_path(config_paths_testdir)

    # Order of precedence when detecting test directory
    # 1. Command line option --testdir
    # 2. Configuration option specified by 'testdir'
    # 3. Configuration option specified by 'prefix'
    # 4. Defaults to current working directory in .buildtest subdirectory
    test_directory = args.testdir or config_paths_testdir or prefix_testdir

    # returns a list of destination directories where repositories are cloned, if
    # REPO_FILE is not found get_repo_paths will return None, in that case we
    # set buildspec_searchpath to empty list
    buildspec_searchpath = get_repo_paths() or []

    # add default path to search path
    buildspec_searchpath.append(BUILDSPEC_DEFAULT_PATH)

    print("Paths:")
    print("{:_<10}".format(""))
    print(f"Prefix: {prefix}")
    print(f"Buildspec Search Path: {buildspec_searchpath}")
    print(f"Test Directory: {test_directory}")

    # list to store all Buildspecs that are found using discover_buildspecs
    # followed by exclusion check
    buildspecs = []

    # Discover list of one or more Buildspec files based on path provided. Since --buildspec can be provided multiple
    # times we need to invoke discover_buildspecs once per argument.
    for buildtest_argument in args.buildspec:
        buildspecs += discover_buildspecs(buildtest_argument)

    # remove any duplicate Buildspec from list by converting list to set and then back to list
    buildspecs = list(set(buildspecs))
    all_buildspecs = buildspecs

    # if no files discovered let's stop now
    if not buildspecs:
        msg = "There are no config files to process."
        sys.exit(msg)

    logger.debug(
        f"Based on input argument: --buildspec {args.buildspec} buildtest discovered the following Buildspecs: {buildspecs}"
    )

    if args.exclude:
        logger.debug(f"The exclude pattern is the following: -e {args.exclude}")

        buildspecs = [file for file in buildspecs if include_file(file, args.exclude)]
        logger.debug(f"Buildspec list after applying exclusion: {buildspecs}")

        # if no files remain after exclusion let's stop now.
        if not buildspecs:
            msg = "There are no Buildspec files to process."
            sys.exit(msg)

    print("\nStage: Discovered Buildspecs \n")
    print(
        """
+-------------------------------+
| Stage: Discovered Buildspecs  |
+-------------------------------+ 
"""
    )

    [print(buildspec) for buildspec in buildspecs]

    exclude_buildspecs = list(set(all_buildspecs) - set(buildspecs))
    print("\nExcluded Buildspecs: ", exclude_buildspecs)
    print(
        """
+----------------------+
| Stage: Building Test |
+----------------------+ 
"""
    )

    print(
        "{:<25} {:<25} {:<40} {:<40}".format(
            "Name", "Schema Validation File ", "TestPath", "Buildspec"
        )
    )
    print("{:_<160}".format(""))
    # Process each Buildspec iteratively by parsing using BuildspecParser followed by
    # getting the appropriate builder and invoking the executor instance of type BuildExecutor
    # to run the test
    builders = []
    skipped_tests = []
    valid_builders = []
    # build all the tests
    for buildspec in buildspecs:

        try:
            # Read in Buildspec file here, loading each will validate the buildspec file
            bp = BuildspecParser(buildspec)
        except (SystemExit, ValidationError) as err:
            skipped_tests.append(f"Skipping {buildspec} since it failed to validate")
            logger.error(err)
            continue

        # And builders parsed through for each
        for builder in bp.get_builders(testdir=test_directory):

            builder.build()
            print(
                "{:<25} {:<25} {:<40} {:<40}".format(
                    builder.metadata["name"],
                    builder.schemafile,
                    builder.metadata["testpath"],
                    builder.buildspec,
                )
            )
            builders.append(builder)

    # print any skipped buildspecs if they failed to validate during build stage
    if len(skipped_tests) > 0:
        print("\n\n")
        print("Error Messages from Stage: Build")
        print("{:_<80}".format(""))
        for test in skipped_tests:
            print(test)

    executor = BuildExecutor(config_opts)

    # run all the tests
    passed_tests = 0
    failed_tests = 0
    total_tests = 0
    errmsg = []
    results = []
    poll = False
    print(
        """
+----------------------+
| Stage: Running Test  |
+----------------------+ 
"""
    )
    print(
        "{:<20} {:<20} {:<20} {:<20} {:<20}".format(
            "Name", "Executor", "Status", "Return Code", "Buildspec Path"
        )
    )
    print("{:_<120}".format(""))
    for builder in builders:
        try:
            result = executor.run(builder)
        except SystemExit as err:
            print("[%s]: Failed to Run Test" % builder.metadata["name"])
            errmsg.append(err)
            logger.error(err)
            continue

        valid_builders.append(builder)
        results.append(result)
        if result["state"] == "PASS":
            passed_tests += 1
        else:
            failed_tests += 1

        if result["state"] == "N/A":
            poll = True

        print(
            "{:<20} {:<20} {:<20} {:<20} {:<20}".format(
                builder.name,
                builder.executor,
                result["state"],
                result["returncode"],
                builder.buildspec,
            )
        )

        total_tests += 1

    if errmsg:
        print("\n\n")
        print("Error Messages from Stage: Run")
        print("{:_<80}".format(""))
        for error in errmsg:
            print(error)
        print("\n")

    # poll will be True if one of the result State is N/A which is buildtest way
    # to inform job is dispatched to scheduler which requires polling
    if poll:
        interval = 10
        while True:
            statelist = []
            print("\n")
            print(f"Polling Jobs in {interval} seconds")
            print("{:_<80}".format(""))

            time.sleep(interval)

            for builder in builders:
                state = executor.poll(builder)
                statelist.append(state)

            # break when all poll states are True
            if all(statelist):
                break

    if total_tests == 0:
        print("No tests were executed")
        return
    print(
        """
+----------------------+
| Stage: Test Summary  |
+----------------------+ 
"""
    )

    print(f"Executed {total_tests} tests")

    pass_rate = passed_tests * 100 / total_tests
    fail_rate = failed_tests * 100 / total_tests

    print(f"Passed Tests: {passed_tests}/{total_tests} Percentage: {pass_rate:.3f}%")

    print(f"Failed Tests: {failed_tests}/{total_tests} Percentage: {fail_rate:.3f}%")
    print("\n\n")

    update_report(valid_builders)
