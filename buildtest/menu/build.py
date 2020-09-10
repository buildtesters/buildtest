"""
This module contains all the methods related to "buildtest build" which is used
for building test scripts from a Buildspec
"""

import logging
import json
import os
import re
import sys
import time
from tabulate import tabulate
from buildtest.defaults import (
    BUILDTEST_ROOT,
    BUILDSPEC_CACHE_FILE,
)


from buildtest.config import load_settings, check_settings
from buildtest.executors.setup import BuildExecutor
from buildtest.menu.buildspec import parse_buildspecs
from buildtest.menu.report import update_report
from buildtest.utils.file import walk_tree, resolve_path

logger = logging.getLogger(__name__)


def discover_buildspecs_by_tags(input_tag):
    """ This method discovers buildspecs by tags, using ``--tags`` option
        from ``buildtest build`` command. This method will read BUILDSPEC_CACHE_FILE
        and search for ``tags`` key in buildspec recipe and match with input
        tag. Since ``tags`` field is a list, we check if input tag is in ``list``
        and if so we add the entire buildspec into a list. The return is a list
        of buildspec files to process.

        :param input_tag: Input tags from command line argument ``buildtest build --tags <tags>``
        :type input_tag: string
        :return: a list of buildspec files that match tag name
        :rtype: list
    """

    with open(BUILDSPEC_CACHE_FILE, "r") as fd:
        cache = json.loads(fd.read())

    buildspecs = []
    # query all buildspecs from BUILDSPEC_CACHE_FILE for tags keyword and
    # if it matches input_tag we add buildspec to list
    for path in cache.keys():
        for buildspecfile in cache[path].keys():
            for test in cache[path][buildspecfile].keys():

                # if tags is not declared we set to empty list
                tag = cache[path][buildspecfile][test].get("tags") or []

                if input_tag in tag:
                    buildspecs.append(buildspecfile)

    return buildspecs


def discover_by_buildspecs(buildspec):
    """ Given a buildspec file specified by the user with ``buildtest build --buildspec``,
        discover one or more files and return a list for buildtest to process.
        This method is called once per argument of ``--buildspec`` or ``--exclude``
        option. If its a directory path we recursively find all buildspecs with
        .yml extension. If filepath doesn't exist or file extension is not .yml we
        return None and log as an error.

        # file path
        buildtest build --buildspec tutorials/hello.sh.yml

        # directory path
        buildtest build --buildspec tutorials

        :param buildspec: Input argument from ``buildtest build --buildspec``
        :type buildspec: str
        :return: A list of discovered buildspec with resolved path, if its invalid we return None
        :rtype: list or None
    """

    buildspecs = []
    # if buildspec doesn't exist print message and log error and return
    if not os.path.exists(os.path.abspath(buildspec)):
        msg = (
            f"Unable to find any buildspecs with name: {os.path.abspath(buildspec)} "
            + "Please provide an absolute or relative path to a directory or file relative to current directory."
        )
        print(msg)
        logger.error(msg)
        return

    # Now handle path based on being a directory or file path
    if os.path.isdir(buildspec):
        logger.debug(
            f"Buildspec File: {buildspec} is a directory so traversing directory tree to find all Buildspec files with .yml extension"
        )
        buildspecs = walk_tree(buildspec, ".yml")
    elif os.path.isfile(buildspec):
        # if buildspec doesn't end in .yml extension we print message and return None
        if not re.search(".yml$", buildspec):
            msg = f"{buildspec} does not end in file extension .yml"
            print(msg)
            logger.error(msg)
            return

        buildspecs = [buildspec]
        logger.debug(f"BuildSpec: {buildspec} is a file")

    # If we don't have any files discovered
    if not buildspecs:
        msg = "No Buildspec files found with input: %s." % buildspec
        print(msg)
        logger.error(msg)
        return

    # return all buildspec by resolving path, this gets the real canonical path and address shell expansion and user expansion
    buildspecs = [resolve_path(file) for file in buildspecs]

    logger.info(f"Found the following config files: {buildspecs}")
    return buildspecs


def discover_buildspecs(tags=None, buildspec=None, exclude_buildspec=None, debug=False):
    """ This method discovers all buildspecs and returns a list of discovered
        excluded buildspecs. The input arguments ``tags``, ``buildspec``, ``exclude_buildspec``
        map to ``--tags`` ``--buildspec`` and ``--exclude`` option in buildtest build.

        :param tags: Input argument from ``buildtest build --tags``
        :type tags: str
        :param buildspec: Input argument from ``buildtest build --buildspec``
        :type tags: str
        :param exclude_buildspec: Input argument from ``buildtest build --exclude``
        :type tags: str
        :param debug: Boolean to control print messages to stdout
        :type debug: boolean
        :return: two lists of discovered and excluded buildspecs
        :rtype: list, list
    """

    buildspecs = []
    exclude_buildspecs = []

    if tags:
        assert isinstance(tags, str)
        buildspecs += discover_buildspecs_by_tags(tags)

    if buildspec:
        # Discover list of one or more Buildspec files based on path provided. Since --buildspec can be provided multiple
        # times we need to invoke discover_buildspecs once per argument.

        assert isinstance(buildspec, list)

        for option in buildspec:
            bp = discover_by_buildspecs(option)

            # only add buildspecs if its not None
            if bp:
                buildspecs += bp

    # remove any duplicate Buildspec from list by converting list to set and then back to list
    buildspecs = list(set(buildspecs))

    # if no files discovered let's stop now
    if not buildspecs:
        msg = "There are no config files to process."
        sys.exit(msg)

    logger.debug(
        f"Based on input argument: --buildspec {buildspec} buildtest discovered the following Buildspecs: {buildspecs}"
    )

    if exclude_buildspec:
        assert isinstance(exclude_buildspec, list)
        excludes = []
        for option in exclude_buildspec:
            bp = discover_by_buildspecs(option)
            if bp:
                excludes += bp

        exclude_buildspecs = list(set(excludes))

        logger.debug(f"The exclude pattern is the following: -e {exclude_buildspec}")

        # exclude files that are found in exclude_buildspecs list
        buildspecs = [file for file in buildspecs if file not in exclude_buildspecs]

        logger.debug(f"Buildspec list after applying exclusion: {buildspecs}")

    # if no files remain after exclusion let's stop now.
    if not buildspecs:
        msg = "There are no Buildspec files to process."
        sys.exit(msg)

    if debug:

        print(
            """
+-------------------------------+
| Stage: Discovered Buildspecs  |
+-------------------------------+ 
    """
        )

        [print(buildspec) for buildspec in buildspecs]

        if exclude_buildspecs:
            print("\nExcluded Buildspecs: ", exclude_buildspecs)

    return buildspecs, exclude_buildspecs


def resolve_testdirectory(config_opts, input_testdir=None):
    """ This method resolves which test directory to select. For example, one
        can specify test directory via command line ``buildtest build --testdir <path>``
        or path in configuration file. The default is $BUILDTEST_ROOT/var/tests


        :param config_opts: loaded buildtest configuration as a dict.
        :type config_opts: dict
        :param input_testdir: Input test directory from command line ``buildtest build --testdir``
        :type input_testdir: str
        :return: Path to test directory to use
        :rtype: str
    """

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
    # 4. Defaults to $BUILDTEST_ROOT/var/tests
    test_directory = (
        input_testdir
        or config_paths_testdir
        or prefix_testdir
        or os.path.join(BUILDTEST_ROOT, "var", "tests")
    )
    return test_directory


def build_phase(builders, printTable=False):
    """ This method will build all tests by invoking class method ``build`` for
        each builder that generates testscript in the test directory.

        :param builders: A list of builders
        :type builders: list
        :param printTable: Print builder table
        :type printTable: boolean

    """
    print(
        """
+----------------------+
| Stage: Building Test |
+----------------------+ 
"""
    )
    table = {"name": [], "schemafile": [], "testpath": [], "buildspec": []}
    for builder in builders:
        builder.build()
        table["name"].append(builder.metadata["name"])
        table["schemafile"].append(builder.metadata["schemafile"])
        table["testpath"].append(builder.metadata["testpath"])
        table["buildspec"].append(builder.buildspec)

    if printTable:
        print(
            tabulate(
                table,
                headers=["Name", "Schema File", "Test Path", "Buildspec"],
                tablefmt="presto",
            )
        )


def run_phase(builders, executor, config_dict, printTable=False):
    """ This method will run all builders with the appropriate executor.
        The executor argument is an instance of ``BuildExecutor`` that is responsible
        for orchestrating builder execution to the appropriate executor class. The
        executor contains a list of executors picked up from buildtest configuration.
        For tests running locally, we get the test metadata and count PASS/FAIL test
        state to tally number of pass and fail test which is printed at end in
        Test Summary. For tests that need to run via scheduler (Slurm, LSF) the first
        stage of run will dispatch job, and state will be `N/A`. We first dispatch all
        jobs and later poll jobs until they are complete. The poll section is skipped
        if all tests are run locally. In poll section we regenerate table with all
        valid_builders and updated test state and returncode and calculate total
        pass/fail tests. Finally we return a list of valid_builders which are tests
        that ran through one of the executors. Any test that failed to run or be
        dispatched will be skipped during run stage and not added in `valid_builders`.
        The `valid_builders` contains the test meta-data that is used for updating
        test report in next stage.

        :param builders:  A list of builders that need to be run. These correspond to test names
        :type: builders: list of objects of type `BuilderBase`
        :param executor: The master executor class responsible for invoking appropriate executor class corresponding to builder.
        :type executor: BuildExecutor
        :param config_dict: loaded buildtest configuration
        :type config_dict: dict
        :param printTable: boolean to control print statement for run phase
        :type printTable: bool
        :return: A list of valid builders
        :rtype: list
    """

    valid_builders = []
    # run all the tests
    passed_tests = 0
    failed_tests = 0
    total_tests = 0
    errmsg = []

    poll = False

    if printTable:
        print(
            """
+----------------------+
| Stage: Running Test  |
+----------------------+ 
    """
        )

    table = {"name": [], "executor": [], "status": [], "returncode": [], "testpath": []}

    poll_queue = []

    for builder in builders:
        try:
            result = executor.run(builder)
        except SystemExit as err:
            print("[%s]: Failed to Run Test" % builder.metadata["name"])
            errmsg.append(err)
            logger.error(err)
            continue

        valid_builders.append(builder)

        table["name"].append(builder.name)
        table["executor"].append(builder.executor)
        table["status"].append(result["state"])
        table["returncode"].append(result["returncode"])
        table["testpath"].append(builder.metadata["testpath"])

        if result["state"] == "N/A":
            poll_queue.append(builder)
            poll = True
            continue

        if result["state"] == "PASS":
            passed_tests += 1
        else:
            failed_tests += 1

        total_tests += 1

    if printTable:
        print(tabulate(table, headers=table.keys(), tablefmt="presto"))

    if errmsg:
        print("\n\n")
        print("Error Messages from Stage: Run")
        print("{:_<80}".format(""))
        for error in errmsg:
            print(error)
        print("\n")

    ########## END RUN STAGE ####################
    # poll will be True if one of the result State is N/A which is buildtest way to inform job is dispatched to scheduler which requires polling
    if poll:
        ########## BEGIN POLL STAGE ####################
        interval = (
            config_dict.get("executors", {}).get("defaults", {}).get("pollinterval")
        )
        # if no items in poll_queue terminate, this will happen as jobs complete polling
        # and they are removed from queue.
        while poll_queue:

            print("\n")
            print(f"Polling Jobs in {interval} seconds")
            print("{:_<40}".format(""))

            logger.debug(f"Sleeping for {interval} seconds")
            time.sleep(interval)
            logger.debug(f"Polling Jobs: {poll_queue}")

            for builder in poll_queue:
                state = executor.poll(builder)
                # remove builder from poll_queue when state is True
                if state:
                    logger.debug(
                        f"{builder} poll complete, removing test from poll queue"
                    )
                    poll_queue.remove(builder)

        table = {
            "name": [],
            "executor": [],
            "status": [],
            "returncode": [],
            "testpath": [],
        }

        if printTable:

            print(
                """
+---------------------------------------------+
| Stage: Final Results after Polling all Jobs |
+---------------------------------------------+ 
    """
            )

        # regenerate test results after poll
        passed_tests = 0
        failed_tests = 0
        total_tests = 0
        for builder in valid_builders:
            result = builder.metadata["result"]
            if result["state"] == "PASS":
                passed_tests += 1
            else:
                failed_tests += 1

            table["name"].append(builder.name)
            table["executor"].append(builder.executor)
            table["status"].append(result["state"])
            table["returncode"].append(result["returncode"])
            table["testpath"].append(builder.metadata["testpath"])

            total_tests += 1

        if printTable:
            print(tabulate(table, headers=table.keys(), tablefmt="presto"))

    ########## END POLL STAGE ####################

    ########## TEST SUMMARY ####################
    if total_tests == 0:
        print("No tests were executed")
        return

    if printTable:
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

        print(
            f"Passed Tests: {passed_tests}/{total_tests} Percentage: {pass_rate:.3f}%"
        )

        print(
            f"Failed Tests: {failed_tests}/{total_tests} Percentage: {fail_rate:.3f}%"
        )
        print("\n\n")

    return valid_builders


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

    test_directory = resolve_testdirectory(config_opts, args.testdir)

    ########## BEGIN BUILDSPEC DISCOVER STAGE ####################

    # discover all buildspecs by tags, buildspecs, and exclude buildspecs. The return
    # is a list of buildspecs and excluded buildspecs
    buildspecs, exclude_buildspecs = discover_buildspecs(
        args.tags, args.buildspec, args.exclude, debug=True
    )

    ########## END BUILDSPEC DISCOVER STAGE ####################
    stage = args.stage

    # Parse all buildspecs and skip any buildspecs that fail validation, return type
    # is a builder object used for building test.
    builders = parse_buildspecs(buildspecs, test_directory, printTable=True)

    # if --stage=parse we stop here
    if stage == "parse":
        return

    executor = BuildExecutor(config_opts)

    build_phase(builders, printTable=True)

    if stage == "build":
        return

    valid_builders = run_phase(builders, executor, config_opts, printTable=True)

    update_report(valid_builders)
