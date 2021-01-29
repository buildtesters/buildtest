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
from jsonschema.exceptions import ValidationError
from tabulate import tabulate
from buildtest.defaults import (
    BUILDTEST_ROOT,
    BUILDSPEC_CACHE_FILE,
)
from buildtest.buildsystem.builders import Builder
from buildtest.buildsystem.parser import BuildspecParser
from buildtest.exceptions import BuildTestError
from buildtest.executors.setup import BuildExecutor

from buildtest.menu.report import update_report
from buildtest.utils.file import walk_tree, resolve_path
from buildtest.utils.tools import Hasher

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

    for buildspecfile in cache["buildspecs"].keys():
        for test in cache["buildspecs"][buildspecfile].keys():

            # if tags is not declared we set to empty list
            tag = cache["buildspecs"][buildspecfile][test].get("tags") or []

            if input_tag in tag:
                buildspecs.append(buildspecfile)

    return buildspecs


def discover_buildspecs_by_executor_name(executor_name):
    """This method discovers buildspecs by executor name, using ``--executor-name``
    option from ``buildtest build`` command. This method will read BUILDSPEC_CACHE_FILE
    and search for ``executor`` key in buildspec recipe and match with input
    executor name. The return is a list of matching buildspec with executor name
    to process.

    :param executor_name: Input executor name from command line argument ``buildtest build --executor-name <name>``
    :type executor_name: string
    :return: a list of buildspec files that match tag name
    :rtype: list
    """

    with open(BUILDSPEC_CACHE_FILE, "r") as fd:
        cache = json.loads(fd.read())

    buildspecs = []
    # query all buildspecs from BUILDSPEC_CACHE_FILE for tags keyword and
    # if it matches input_tag we add buildspec to list

    for buildspecfile in cache["buildspecs"].keys():
        for test in cache["buildspecs"][buildspecfile].keys():

            # if tags is not declared we set to empty list
            executor = cache["buildspecs"][buildspecfile][test].get("executor") or []

            if executor_name == executor:
                buildspecs.append(buildspecfile)

    return buildspecs


def discover_by_buildspecs(buildspec):
    """ Given a buildspec file specified by the user with ``buildtest build --buildspec``,
        discover one or more files and return a list for buildtest to process.
        This method is called once per argument of ``--buildspec`` or ``--exclude``
        option. If its a directory path we recursively find all buildspecs with
        .yml extension. If filepath doesn't exist or file extension is not .yml we
        return None and capture error in log.

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


def discover_buildspecs(
    tags=None, executorname=None, buildspec=None, exclude_buildspec=None, debug=False
):
    """ This method discovers all buildspecs and returns a list of discovered
        excluded buildspecs. The input arguments ``tags``, ``buildspec``, ``exclude_buildspec``
        map to ``--tags`` ``--buildspec`` and ``--exclude`` option in buildtest build.

        :param tags: Input argument from ``buildtest build --tags``
        :type tags: list
        :param executorname: Input argument from ``buildtest build --executor-name``
        :type executorname: list
        :param buildspec: Input argument from ``buildtest build --buildspec``
        :type buildspec: str
        :param exclude_buildspec: Input argument from ``buildtest build --exclude``
        :type tags: str
        :param debug: Boolean to control print messages to stdout
        :type debug: boolean
        :return: two lists of discovered and excluded buildspecs
        :rtype: list, list
    """

    buildspecs = []
    excluded_buildspecs = []

    logger.debug(
        f"Discovering buildspecs based on tags={tags}, executor={executorname}, buildspec={buildspec}, exclude_buildspec={exclude_buildspec}"
    )
    # discover buildspecs based on --tags
    if tags:
        logger.debug(f"Checking tag argument: {tags} is of type 'list'")
        assert isinstance(tags, list)

        for tagname in tags:
            logger.debug(f"Checking {tagname} is type 'str'")
            assert isinstance(tagname, str)
            buildspecs += discover_buildspecs_by_tags(tagname)

        logger.debug(f"Discovered buildspecs based on {tags}")
        logger.debug(buildspecs)

    # discover buildspecs based on --executor
    if executorname:
        # logger.debug(f"Checking executor argument: {tags} is of type 'list'")
        # assert isinstance(executorname, list)
        for name in executorname:
            logger.debug(f"Checking {name} is type 'str'")
            assert isinstance(name, str)

            buildspecs += discover_buildspecs_by_executor_name(name)

    # discover buildspecs based on --buildspec
    if buildspec:
        # Discover list of one or more Buildspec files based on path provided. Since --buildspec can be provided multiple
        # times we need to invoke discover_buildspecs once per argument.

        logger.debug(f"Checking buildspec argument: {buildspec} is of type 'list'")
        assert isinstance(buildspec, list)

        for option in buildspec:
            bp = discover_by_buildspecs(option)

            # only add buildspecs if its not None
            if bp:
                logger.debug(f"Discovered buildspecs: {bp} based on argument: {option}")
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

    # if user pass buildspecs to be excluded (buildtest build -x <buildspec>) then
    # discover all excluded buildspecs and remove from discovered list
    if exclude_buildspec:
        assert isinstance(exclude_buildspec, list)
        excludes = []
        # discover all excluded buildspecs, if its file add to list,
        # if its directory traverse all .yml files
        for exclude_buildspec_arg in exclude_buildspec:
            bp = discover_by_buildspecs(exclude_buildspec_arg)
            if bp:
                excludes += bp

        excluded_buildspecs = list(set(excludes))

        logger.debug(f"The exclude pattern is the following: -e {exclude_buildspec}")

        # exclude files that are found in excluded_buildspecs list
        buildspecs = [file for file in buildspecs if file not in excluded_buildspecs]

        logger.debug(f"Buildspec list after applying exclusion: {buildspecs}")

    # if no files remain after exclusion let's stop now.
    if not buildspecs:
        msg = "There are no Buildspec files to process."
        sys.exit(msg)

    if debug:

        print(
            """
+-------------------------------+
| Stage: Discovering Buildspecs |
+-------------------------------+ 
    """
        )

        print("\nDiscovered Buildspecs:\n ")
        [print(buildspec) for buildspec in buildspecs]

        if excluded_buildspecs:
            print("\nExcluded Buildspecs:\n")
            [print(file) for file in excluded_buildspecs]

    return buildspecs, excluded_buildspecs


def resolve_testdirectory(config_opts, input_testdir=None):
    """This method resolves which test directory to select. For example, one
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


def parse_buildspecs(
    buildspecs, executor, test_directory, filters, rebuild, printTable=False
):

    """ Parse all buildspecs by invoking class ``BuildspecParser``. If buildspec
        fails validation we add it to ``skipped_tests`` list and print all skipped
        tests at end. If buildspec passes validation we get all builders by invoking
        ``get_builders`` method in BuildspecParser class which gets all tests from
        buildspec file.

        :param buildspecs: A list of input buildspecs to parse
        :type buildspecs: list, required
        :param executor: An instance of BuildExecutor class
        :type executor: BuildExecutor
        :param test_directory: Test directory where buildspecs will be written
        :type test_directory: str, required
        :param filters: A dictionary containing filters on builders based on tags and executors
        :type filters: dict, required
        :param rebuild: Input argument from command line --rebuild
        :type rebuild: int or None
        :param printTable: a boolean to control if parse table is printed
        :type printTable: bool, optional
        :return: A list of builder objects which are instances of ``BuilderBase`` class
        :rtype: list
    """

    builders = []
    table = {"schemafile": [], "validstate": [], "buildspec": []}
    invalid_buildspecs = []
    # build all the tests
    for buildspec in buildspecs:

        valid_state = True
        try:
            # Read in Buildspec file here, loading each will validate the buildspec file
            bp = BuildspecParser(buildspec, executor)
        except (BuildTestError, ValidationError) as err:
            invalid_buildspecs.append(
                f"Skipping {buildspec} since it failed to validate"
            )
            logger.error(err)
            continue

        table["schemafile"].append(bp.schema_file)
        table["validstate"].append(valid_state)
        table["buildspec"].append(buildspec)

        builder = Builder(
            bp=bp, filters=filters, testdir=test_directory, rebuild=rebuild
        )
        builders += builder.get_builders()

    # print any skipped buildspecs if they failed to validate during build stage
    if len(invalid_buildspecs) > 0:
        print("\n\n")
        print("Error Messages from Stage: Parse")
        print("{:_<80}".format(""))
        for test in invalid_buildspecs:
            print(test)

    if not builders:
        print("No buildspecs to process because there are no valid buildspecs")
        sys.exit(0)

    if printTable:
        print(
            """
+---------------------------+
| Stage: Parsing Buildspecs |
+---------------------------+ 
    """
        )
        print(tabulate(table, headers=table.keys(), tablefmt="presto"))

    return builders


def build_phase(builders, printTable=False):
    """This method will build all tests by invoking class method ``build`` for
    each builder that generates testscript in the test directory.

    :param builders: A list of builders
    :type builders: list
    :param printTable: Print builder table
    :type printTable: boolean
    """
    invalid_builders = []
    print(
        """
+----------------------+
| Stage: Building Test |
+----------------------+ 
"""
    )
    table = Hasher()
    for field in ["name", "id", "type", "executor", "tags", "compiler", "testpath"]:
        table["script"][field] = []
        table["compiler"][field] = []

    del table["script"]["compiler"]

    for builder in builders:
        try:
            builder.build()
        except BuildTestError as err:
            print(err)
            invalid_builders.append(builder)
            logger.error(err)
            continue

        table[builder.type]["name"].append(builder.metadata["name"])
        table[builder.type]["id"].append(builder.metadata["id"])
        table[builder.type]["type"].append(builder.recipe["type"])
        table[builder.type]["executor"].append(builder.recipe["executor"])
        table[builder.type]["tags"].append(builder.recipe.get("tags"))
        table[builder.type]["testpath"].append(builder.metadata["testpath"])

        if builder.type == "compiler":
            table[builder.type]["compiler"].append(builder.compiler)

    if printTable:
        # print any skipped buildspecs if they failed to validate during build stage
        if invalid_builders:
            print("\n\n")
            print("Error Messages from Stage: Build")
            print("{:_<80}".format(""))
            for test in invalid_builders:
                print(test)

        if len(table["script"]["name"]) > 0:
            print(
                tabulate(
                    table["script"], headers=table["script"].keys(), tablefmt="presto"
                )
            )

        print("\n")
        if len(table["compiler"]["name"]) > 0:
            print(
                tabulate(
                    table["compiler"],
                    headers=table["compiler"].keys(),
                    tablefmt="presto",
                )
            )

    # remove builders if any invalid builders detected in build phase
    if invalid_builders:
        for test in invalid_builders:
            builders.remove(test)

    return builders


def run_phase(builders, executor, buildtest_config, printTable=False):
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
        :param buildtest_config: loaded buildtest configuration
        :type buildtest_config: dict
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

    table = {
        "name": [],
        "id": [],
        "executor": [],
        "status": [],
        "returncode": [],
        "testpath": [],
    }

    poll_queue = []

    for builder in builders:
        try:
            executor.run(builder)
        except SystemExit as err:
            print("[%s]: Failed to Run Test" % builder.metadata["name"])
            errmsg.append(err)
            logger.error(err)
            continue

        valid_builders.append(builder)
        table["name"].append(builder.name)
        table["id"].append(builder.metadata["id"])
        table["executor"].append(builder.executor)
        table["status"].append(builder.metadata["result"]["state"])
        table["returncode"].append(builder.metadata["result"]["returncode"])
        table["testpath"].append(builder.metadata["testpath"])

        if builder.metadata["result"]["state"] == "N/A":
            poll_queue.append(builder)
            poll = True
            continue

        if builder.metadata["result"]["state"] == "PASS":
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
        valid_builders = poll_jobs(
            buildtest_config, poll_queue, executor, valid_builders
        )

        table = {
            "name": [],
            "id": [],
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
            if builder.metadata["result"]["state"] == "PASS":
                passed_tests += 1
            else:
                failed_tests += 1

            table["name"].append(builder.name)
            table["id"].append(builder.metadata["id"])
            table["executor"].append(builder.executor)
            table["status"].append(builder.metadata["result"]["state"])
            table["returncode"].append(builder.metadata["result"]["returncode"])
            table["testpath"].append(builder.metadata["testpath"])

            total_tests += 1

        if printTable:
            print(tabulate(table, headers=table.keys(), tablefmt="presto"))

    ########## TEST SUMMARY ####################
    if total_tests == 0:
        print("No tests were executed")
        return

    if printTable:
        print_test_summary(total_tests, passed_tests, failed_tests)

    return valid_builders


def poll_jobs(config_dict, poll_queue, executor, valid_builders):
    """ This method will poll jobs by processing all jobs in ``poll_queue``. If
        job is cancelled by scheduler, we remove this from valid_builders list.
        This method will return a list of valid_builders after polling. If there
        are no valid_builders after polling, the method will return None

        :param config_dict: loaded buildtest configuration
        :type config_dict: dict, required
        :param poll_queue: a list of jobs that need to be polled. The jobs will poll using poll method from executor
        :type poll_queue: list, required
        :param executor: an instance of BuildExecutor class
        :type executor: BuildExecutor, required
        :param valid_builders: list of valid builders
        :type valid_builders: list, required
    """

    interval = config_dict.get("executors", {}).get("defaults", {}).get("pollinterval")
    # if no items in poll_queue terminate, this will happen as jobs complete polling
    # and they are removed from queue.

    # keep track of ignored jobs by job scheduler these include jobs that failed abnormally or cancelled by scheduler
    ignore_jobs = set()
    while poll_queue:

        print("\n")
        print(f"Polling Jobs in {interval} seconds")
        print("{:_<40}".format(""))

        logger.debug(f"Sleeping for {interval} seconds")
        time.sleep(interval)
        logger.debug(f"Polling Jobs: {poll_queue}")

        for builder in poll_queue:
            poll_info = executor.poll(builder)

            # remove builder from poll_queue when state is True
            if poll_info["job_complete"]:
                logger.debug(f"{builder} poll complete, removing test from poll queue")
                poll_queue.remove(builder)

            # add invalid jobs to ignore_jobs list which are ignored from output
            # and not updated in report
            if poll_info["ignore_job"]:
                ignore_jobs.add(builder)

    # remove any builders where for jobs that need to be ignored
    if ignore_jobs:
        # convert set to list
        ignore_jobs = list(ignore_jobs)
        for builder in ignore_jobs:
            valid_builders.remove(builder)

        print("Cancelled Tests:")
        [print(builder.metadata["name"]) for builder in ignore_jobs]

    # after removing jobs from valid_builders list there is chance we have no jobs to report
    # in that case we return from method
    if not valid_builders:
        sys.exit("After polling all jobs we found no valid builders to process")

    return valid_builders


def print_test_summary(total_tests, passed_tests, failed_tests):
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


def func_build_subcmd(args, buildtest_config):
    """ Entry point for ``buildtest build`` sub-command. This method will discover
        Buildspecs in method ``discover_buildspecs``. If there is an exclusion list
        this will be checked, once buildtest knows all Buildspecs to process it will
        begin validation by calling ``BuildspecParser`` and followed by an executor
        instance by invoking BuildExecutor that is responsible for executing the
        test based on the executor type. A report of all builds, along with test summary
        will be displayed to screen.

        :param args: arguments passed from command line
        :type args: dict, required
        :param buildtest_config: loaded buildtest settings
        :type buildtest_config: dict, required
        :rtype: None
    """

    test_directory = resolve_testdirectory(buildtest_config, args.testdir)

    # discover all buildspecs by tags, buildspecs, and exclude buildspecs. The return
    # is a list of buildspecs and excluded buildspecs
    buildspecs, exclude_buildspecs = discover_buildspecs(
        args.tags, args.executor, args.buildspec, args.exclude, debug=True
    )

    stage = args.stage
    executor = BuildExecutor(buildtest_config)

    buildspec_filters = {"tags": args.filter_tags}

    # Parse all buildspecs and skip any buildspecs that fail validation, return type
    # is a builder object used for building test.
    builders = parse_buildspecs(
        buildspecs=buildspecs,
        filters=buildspec_filters,
        executor=executor,
        test_directory=test_directory,
        rebuild=args.rebuild,
        printTable=True,
    )

    # if --stage=parse we stop here
    if stage == "parse":
        return

    buildphase_builders = build_phase(builders, printTable=True)
    if not buildphase_builders:
        raise BuildTestError(
            "Unable to create any test during build phase. Please check buildtest.log for more details"
        )

    if stage == "build":
        return

    runphase_builders = run_phase(
        buildphase_builders, executor, buildtest_config, printTable=True
    )

    # only update report if we have a list of valid builders returned from run_phase
    if runphase_builders:
        update_report(runphase_builders)
