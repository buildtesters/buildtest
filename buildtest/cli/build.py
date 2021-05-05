"""
This module contains all the methods related to "buildtest build" which is used
for building test scripts from a Buildspec
"""

import logging
import os
import re
import shutil
import sys
import time
import tempfile
from datetime import datetime
from jsonschema.exceptions import ValidationError
from tabulate import tabulate
from termcolor import colored

from buildtest import BUILDTEST_VERSION
from buildtest.buildsystem.builders import Builder
from buildtest.buildsystem.parser import BuildspecParser
from buildtest.cli.report import update_report
from buildtest.defaults import BUILDSPEC_CACHE_FILE, BUILDTEST_USER_HOME, BUILD_REPORT
from buildtest.exceptions import (
    BuildTestError,
    BuildspecError,
    ExecutorError,
)
from buildtest.executors.setup import BuildExecutor
from buildtest.system import system
from buildtest.utils.file import walk_tree, resolve_path, is_file, create_dir, load_json
from buildtest.utils.tools import Hasher, deep_get

logger = logging.getLogger(__name__)


class BuildTest:
    """This class is an interface to building tests via "buildtest build" command."""

    def __init__(
        self,
        configuration=None,
        buildspecs=None,
        exclude_buildspecs=None,
        tags=None,
        executors=None,
        testdir=None,
        stage=None,
        filter_tags=None,
        rebuild=None,
        buildtest_system=None,
        report_file=None,
        max_pend_time=None,
        poll_interval=None,
    ):
        """The initializer method is responsible for checking input arguments for type
        check, if any argument fails type check we raise an error. If all arguments pass
        we assign the values and proceed with building the test.

        :param configuration: Loaded configuration content which is an instance of SiteConfiguration
        :type configuration: SiteConfiguration
        :param buildspecs: list of buildspecs from command line (--buildspec)
        :type buildspecs: list, optional
        :param exclude_buildspecs: list of excluded buildspecs from command line (--exclude)
        :type exclude_buildspecs: list, optional
        :param tags: list of tags passed from command line (--tags)
        :type tags: list, optional
        :param executors: list of executors passed from command line (--executors)
        :type executors: list, optional
        :param testdir: specify path to test directory where tests are written. This argument is passed from command line (--testdir)
        :type testdir: str, optional
        :param stage: contains value of command line argument (--stage)
        :type stage: str, optional
        :param filter_tags: contains value of command line argument (--filter-tags)
        :type filter_tags: list, optional
        :param rebuild: contains value of command line argument (--rebuild)
        :type rebuild: list, optional
        :param buildtest_system: Instance of BuildTestSystem class
        :type  buildtest_system: BuildTestSystem
        :param report_file: Specify location where report file is written
        :type report_file: str, optional
        :param max_pend_time: Maximum Pend Time (sec) for batch job submission
        :type max_pend_time: int, optional
        :param poll_interval: Poll Interval (sec) for polling batch jobs
        :type poll_interval: int, optional

        """

        if buildspecs and not isinstance(buildspecs, list):
            raise BuildTestError(f"{buildspecs} is not of type list")

        if exclude_buildspecs and not isinstance(exclude_buildspecs, list):
            raise BuildTestError(f"{exclude_buildspecs} is not of type list")

        if tags and not isinstance(tags, list):
            raise BuildTestError(f"{tags} is not of type list")

        if executors and not isinstance(executors, list):
            raise BuildTestError(f"{executors} is not of type list")

        if filter_tags and not isinstance(filter_tags, list):
            raise BuildTestError(f"{filter_tags} is not of type list")

        if testdir and not isinstance(testdir, str):
            raise BuildTestError(f"{testdir} is not of type str")

        if stage and not isinstance(stage, str):
            raise BuildTestError(f"{stage} is not of type str")

        if rebuild:
            if not isinstance(rebuild, int):
                raise BuildTestError(f"{rebuild} is not of type int")

            if rebuild > 50:
                raise BuildTestError(
                    f"--rebuild {rebuild} exceeds maximum rebuild limit of 50"
                )

        self.configuration = configuration
        self.buildspecs = buildspecs
        self.exclude_buildspecs = exclude_buildspecs
        self.tags = tags
        self.executors = executors
        self.max_pend_time = max_pend_time
        self.poll_interval = poll_interval

        # get real path to log directory which accounts for variable expansion, user expansion, and symlinks
        self.logdir = resolve_path(
            self.configuration.target_config.get("logdir"), exist=False
        )

        # create a temporary file to store logfile and we don't delete file by setting 'delete=False'
        # by default tempfile will delete file upon exit.
        self.logfile = tempfile.NamedTemporaryFile(
            prefix="buildtest_", delete=False, suffix=".log"
        )

        if self.logdir:

            create_dir(self.logdir)
            self.logfile.name = os.path.join(
                self.logdir, os.path.basename(self.logfile.name)
            )

        self.testdir = self.resolve_testdirectory(testdir)
        self.stage = stage
        self.filtertags = filter_tags
        self.rebuild = rebuild

        # contains a list of buildspecs found from tags, executors, buildspecs argument
        self.bp_found = None
        # contains a list of buildspecs removed after discovery
        self.bp_removed = None
        # this variable contains the detected buildspecs that will be processed by buildtest.
        self.detected_buildspecs = None

        self.builders = None
        self.buildexecutor = BuildExecutor(self.configuration, self.max_pend_time)
        self.system = buildtest_system or system
        self.report_file = resolve_path(report_file, exist=False) or BUILD_REPORT

        print("\n")
        print("User: ", self.system.system["user"])
        print("Hostname: ", self.system.system["host"])
        print("Platform: ", self.system.system["platform"])
        print("Current Time: ", datetime.now().strftime("%Y/%m/%d %X"))
        print("buildtest path:", shutil.which("buildtest"))
        print("buildtest version: ", BUILDTEST_VERSION)
        print("python path:", self.system.system["python"])
        print("python version: ", self.system.system["pyver"])
        print("Test Directory: ", self.testdir)
        print("Configuration File: ", self.configuration.file)

    def build(self):
        """This method is responsible for implementating stages: parse, build, run, update. """

        self.discover_buildspecs(printTable=True)

        # Parse all buildspecs and skip any buildspecs that fail validation, return type
        # is a builder object used for building test.

        self.parse_buildspecs(printTable=True)

        # if no builders found or  --stage=parse set we return from method
        if not self.builders or self.stage == "parse":
            return

        self.build_phase(printTable=True)

        # if --stage=build is set  we return from method
        if self.stage == "build":
            return

        self.builders = self.run_phase(printTable=True)

        # store path to logfile in each builder object. There is a single logfile per build.
        for builder in self.builders:
            builder.metadata["logpath"] = self.logfile.name

        # only update report if we have a list of valid builders returned from run_phase
        if self.builders:
            update_report(self.builders, self.report_file)

        shutil.copy2(
            os.path.join(os.getenv("BUILDTEST_ROOT"), "buildtest.log"),
            self.logfile.name,
        )

        print(f"Writing Logfile to: {self.logfile.name}")
        print(
            "A copy of logfile can be found at $BUILDTEST_ROOT/buildtest.log - ",
            os.path.join(os.getenv("BUILDTEST_ROOT"), "buildtest.log"),
        )

    def resolve_testdirectory(self, cli_testdir=None):
        """This method resolves which test directory to select. For example, one
        can specify test directory via command line ``buildtest build --testdir <path>``
        or path in configuration file. The default is $HOME/.buildtest/var/tests


        :param cli_testdir: test directory from command line ``buildtest build --testdir``
        :type cli_testdir: str
        :return: Path to test directory to use
        :rtype: str
        """

        # variable to set test directory if prefix is set
        prefix_testdir = resolve_path(
            self.configuration.target_config.get("testdir"), exist=False
        )

        # resolve full path for test directory specified by --testdir option
        cli_testdir = resolve_path(cli_testdir, exist=False)

        # Order of precedence when detecting test directory
        # 1. Command line option --testdir
        # 2. Configuration option specified by 'testdir'
        # 3. Defaults to $HOME/.buildtest/var/tests
        test_directory = (
            cli_testdir
            or prefix_testdir
            or os.path.join(BUILDTEST_USER_HOME, "var", "tests")
        )

        create_dir(test_directory)

        return test_directory

    def discover_buildspecs(self, printTable=False):
        """This method discovers all buildspecs based on --buildspecs, --tags, --executor
        and excluding buildspecs (--exclude).

        :param printTable: Boolean to control print messages to stdout
        :type printTable: boolean, optional
        """

        self.bp_found = []
        self.bp_removed = []

        tag_dict = {}
        executor_dict = {}

        logger.debug(
            f"Discovering buildspecs based on tags={self.tags}, executor={self.executors}, buildspec={self.buildspecs}, excluded buildspec={self.exclude_buildspecs}"
        )
        # discover buildspecs based on --tags
        if self.tags:

            buildspecs = []
            for name in self.tags:
                logger.debug(f"Checking {name} is type 'str'")
                assert isinstance(name, str)
                tag_dict[name] = self.discover_buildspecs_by_tags(name)
                buildspecs += tag_dict[name]

            self.bp_found += buildspecs

            logger.debug(f"Discovered buildspecs based on tags: {self.tags}")
            logger.debug(self.buildspecs)

        # discover buildspecs based on --executor
        if self.executors:
            buildspecs = []
            for name in self.executors:
                logger.debug(f"Checking {name} is type 'str'")
                assert isinstance(name, str)

                executor_dict[name] = self.discover_buildspecs_by_executor_name(name)
                buildspecs += executor_dict[name]

            self.bp_found += buildspecs

            logger.debug(f"Discovered buildspecs based on executors: {self.executors}")
            logger.debug(buildspecs)

        # discover buildspecs based on --buildspec
        if self.buildspecs:
            # Discover list of one or more Buildspec files based on path provided. Since --buildspec can be provided multiple
            # times we need to invoke discover_buildspecs once per argument.
            buildspecs = []
            for option in self.buildspecs:
                bp = self.discover_by_buildspecs(option)

                # only add buildspecs if its not None
                if bp:
                    buildspecs += bp

            self.bp_found += buildspecs

        # remove any None objects from list since there is possibility they got added if 'tags', 'executors', 'buildspecs' is None
        self.bp_found = list(filter(None, self.bp_found))

        # remove any duplicate Buildspec from list by converting list to set and then back to list
        self.bp_found = list(set(self.bp_found))

        # if no files discovered let's stop now
        if not self.bp_found:
            msg = "There are no config files to process."
            sys.exit(msg)

        logger.debug(f"buildtest discovered the following Buildspecs: {self.bp_found}")

        self.detected_buildspecs = self.bp_found.copy()

        # if user pass buildspecs to be excluded (buildtest build -x <buildspec>) then
        # discover all excluded buildspecs and remove from discovered list
        if self.exclude_buildspecs:

            excludes = []
            # discover all excluded buildspecs, if its file add to list,
            # if its directory traverse all .yml files
            for name in self.exclude_buildspecs:
                bp = self.discover_by_buildspecs(name)
                if bp:
                    excludes += bp

            self.bp_removed = list(set(excludes))

            logger.debug(f"The exclude pattern is the following: {self.bp_removed}")

            # exclude files that are found in excluded_buildspecs list
            self.detected_buildspecs = [
                file for file in self.bp_found if file not in self.bp_removed
            ]

            logger.debug(
                f"Buildspec list after applying exclusion: {self.detected_buildspecs}"
            )

        # if no files remain after exclusion let's stop now.
        if not self.detected_buildspecs:
            msg = "There are no Buildspec files to process."
            sys.exit(msg)

        if printTable:
            msg = """
+-------------------------------+
| Stage: Discovering Buildspecs |
+-------------------------------+ 
"""
            if os.getenv("BUILDTEST_COLOR") == "True":
                msg = colored(msg, "red", attrs=["bold"])

            print(msg)

            print("Discovered Buildspecs:")
            for buildspec in self.detected_buildspecs:
                print(buildspec)

            if self.bp_removed:
                print("\nExcluded Buildspecs:")
                for file in self.bp_removed:
                    print(file)

            # print breakdown of buildspecs by tags
            if tag_dict:
                print("\nBREAKDOWN OF BUILDSPECS BY TAGS\n")

                headers = tag_dict.keys()
                if os.getenv("BUILDTEST_COLOR") == "True":
                    headers = list(
                        map(
                            lambda x: colored(x, "blue", attrs=["bold"]),
                            tag_dict.keys(),
                        )
                    )
                print(tabulate(tag_dict, headers=headers, tablefmt="simple"))

            # print breakdown of buildspecs by executors
            if executor_dict:
                print("\nBREAKDOWN OF BUILDSPECS BY EXECUTORS\n")

                headers = executor_dict.keys()
                if os.getenv("BUILDTEST_COLOR") == "True":
                    headers = list(
                        map(
                            lambda x: colored(x, "blue", attrs=["bold"]),
                            executor_dict.keys(),
                        )
                    )

                print(tabulate(executor_dict, headers=headers, tablefmt="simple"))

    def discover_buildspecs_by_tags(self, input_tag):
        """This method discovers buildspecs by tags, using ``--tags`` option
        from ``buildtest build`` command. This method will read BUILDSPEC_CACHE_FILE
        and search for ``tags`` key in buildspec recipe and match with input
        tag. Since ``tags`` field is a list, we check if input tag is in ``list``
        and if so we add the entire buildspec into a list. The return is a list
        of buildspec files to process.

        :param input_tag: Input tags from command line argument ``buildtest build --tags <tags>``
        :type input_tag: str
        :return: a list of buildspec files that match tag name
        :rtype: list
        """
        if not is_file(BUILDSPEC_CACHE_FILE):
            raise BuildTestError(
                f"Cannot for buildspec cache: {BUILDSPEC_CACHE_FILE}, please run 'buildtest buildspec find' "
            )

        cache = load_json(BUILDSPEC_CACHE_FILE)

        buildspecs = []
        # query all buildspecs from BUILDSPEC_CACHE_FILE for tags keyword and
        # if it matches input_tag we add buildspec to list

        for buildspecfile in cache["buildspecs"].keys():
            for test in cache["buildspecs"][buildspecfile].keys():

                # if tags is not declared we set to empty list
                tag = cache["buildspecs"][buildspecfile][test].get("tags") or []

                if input_tag in tag:
                    buildspecs.append(buildspecfile)

        # remove any duplicates and return back a list
        buildspecs = list(set(buildspecs))

        return buildspecs

    def discover_buildspecs_by_executor_name(self, executor_name):
        """This method discovers buildspecs by executor name, using ``buildtest build --executor``
        command. This method will read BUILDSPEC_CACHE_FILE and search for ``executor`` key
        in buildspec recipe and match with input executor name. The return is a list of matching
        buildspec with executor name to process.

        :param executor_name: Input executor name from command line argument ``buildtest build --executor <name>``
        :type executor_name: string
        :return: a list of buildspec files that match tag name
        :rtype: list
        """

        if not is_file(BUILDSPEC_CACHE_FILE):
            raise BuildTestError(
                f"Cannot for buildspec cache: {BUILDSPEC_CACHE_FILE}, please run 'buildtest buildspec find' "
            )

        cache = load_json(BUILDSPEC_CACHE_FILE)

        buildspecs = []
        # query all buildspecs from BUILDSPEC_CACHE_FILE for tags keyword and
        # if it matches input_tag we add buildspec to list

        for buildspecfile in cache["buildspecs"].keys():
            for test in cache["buildspecs"][buildspecfile].keys():

                # check if executor in buildspec matches one in argument (buildtest build --executor <EXECUTOR>)
                if executor_name == cache["buildspecs"][buildspecfile][test].get(
                    "executor"
                ):
                    buildspecs.append(buildspecfile)

        # remove any duplicates and return back a list
        buildspecs = list(set(buildspecs))

        return buildspecs

    def discover_by_buildspecs(self, buildspec):
        """Given a buildspec file specified by the user with ``buildtest build --buildspec``,
        discover one or more files and return a list for buildtest to process.
        This method is called once per argument of ``--buildspec`` or ``--exclude``
        option. If its a directory path we recursively find all buildspecs with
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
            logger.debug(f"Buildspec: {buildspec} is a file")

        # If we don't have any files discovered
        if not buildspecs:
            msg = "No Buildspec files found with input: %s." % buildspec
            print(msg)
            logger.error(msg)
            return

        # return all buildspec by resolving path, this gets the real canonical path and address shell expansion and user expansion
        buildspecs = [resolve_path(file) for file in buildspecs]

        logger.info(
            f"Based on input argument we discovered the following buildspecs: {buildspecs}"
        )
        return buildspecs

    def parse_buildspecs(self, printTable=False):
        """Parse all buildspecs by invoking class ``BuildspecParser``. If buildspec
        fails validation we add it to ``skipped_tests`` list and print all skipped
        tests at end. If buildspec passes validation we get all builders by invoking
        ``get_builders`` method in BuildspecParser class which gets all tests from
        buildspec file.

        :param printTable: a boolean to control if parse table is printed
        :type printTable: bool, optional
        :return: A list of builder objects which are instances of ``BuilderBase`` class
        :rtype: list
        """

        self.builders = []
        table = {"schemafile": [], "validstate": [], "buildspec": []}
        invalid_buildspecs = []
        # build all the tests
        for buildspec in self.detected_buildspecs:

            valid_state = True
            try:
                # Read in Buildspec file here, loading each will validate the buildspec file
                bp = BuildspecParser(buildspec, self.buildexecutor)
            except (BuildTestError, BuildspecError, ValidationError) as err:
                invalid_buildspecs.append(
                    f"Skipping {buildspec} since it failed to validate"
                )
                logger.error(err)
                continue

            table["schemafile"].append(bp.schema_file)
            table["validstate"].append(valid_state)
            table["buildspec"].append(buildspec)

            builder = Builder(
                bp=bp,
                buildexecutor=self.buildexecutor,
                filters=self.filtertags,
                testdir=self.testdir,
                rebuild=self.rebuild,
                buildtest_system=self.system,
                configuration=self.configuration,
            )
            self.builders += builder.get_builders()

        # print any skipped buildspecs if they failed to validate during build stage
        if len(invalid_buildspecs) > 0:
            print("\n\nError Messages from Stage: Parse")
            print("{:_<80}".format(""))
            for test in invalid_buildspecs:
                print(test)

        # if no builders found we return from this method
        if not self.builders:
            print("No buildspecs to process because there are no valid buildspecs")
            return

        if printTable:
            msg = """
+---------------------------+
| Stage: Parsing Buildspecs |
+---------------------------+ 
"""
            headers = table.keys()

            if os.getenv("BUILDTEST_COLOR") == "True":
                msg = colored(msg, "red", attrs=["bold"])
                headers = list(
                    map(lambda x: colored(x, "blue", attrs=["bold"]), headers)
                )

            print(msg)
            print(tabulate(table, headers=headers, tablefmt="presto"))

            testnames = list(map(lambda x: x.name, self.builders))
            description = list(
                map(lambda x: x.recipe.get("description"), self.builders)
            )

            print("\n\n")

            headers = ["name", "description"]
            if os.getenv("BUILDTEST_COLOR") == "True":
                headers = list(
                    map(lambda x: colored(x, "blue", attrs=["bold"]), headers)
                )

            print(
                tabulate(
                    zip(testnames, description), headers=headers, tablefmt="simple"
                )
            )

    def build_phase(self, printTable=False):
        """This method will build all tests by invoking class method ``build`` for
        each builder that generates testscript in the test directory.

        :param printTable: Print builder table
        :type printTable: boolean
        """

        invalid_builders = []
        msg = """
+----------------------+
| Stage: Building Test |
+----------------------+ 
"""
        if os.getenv("BUILDTEST_COLOR") == "True":
            msg = colored(msg, "red", attrs=["bold"])

        print(msg)

        table = Hasher()

        for field in ["name", "id", "type", "executor", "tags", "testpath"]:
            table["script"][field] = []
        for field in ["name", "id", "type", "executor", "tags", "compiler", "testpath"]:
            table["compiler"][field] = []

        for builder in self.builders:
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
            table[builder.type]["executor"].append(builder.executor)
            table[builder.type]["tags"].append(builder.recipe.get("tags"))
            table[builder.type]["testpath"].append(builder.metadata["testpath"])

            if builder.type == "compiler":
                table[builder.type]["compiler"].append(builder.compiler)

        if printTable:
            # print any skipped buildspecs if they failed to validate during build stage
            if invalid_builders:
                print("\n\nError Messages from Stage: Build")
                print("{:_<80}".format(""))
                for test in invalid_builders:
                    print(test)

            # if we have any tests using 'script' schema we print all tests together since table columns are different
            if len(table["script"]["name"]) > 0:

                headers = table["script"].keys()
                if os.getenv("BUILDTEST_COLOR") == "True":
                    headers = list(
                        map(
                            lambda x: colored(x, "blue", attrs=["bold"]),
                            table["script"].keys(),
                        )
                    )

                print(
                    tabulate(
                        table["script"],
                        headers=headers,
                        tablefmt="presto",
                    )
                )

            print("\n")

            # if we have any tests using 'compiler' schema we print all tests together since table columns are different
            if len(table["compiler"]["name"]) > 0:

                headers = table["compiler"].keys()
                if os.getenv("BUILDTEST_COLOR") == "True":
                    headers = list(
                        map(
                            lambda x: colored(x, "blue", attrs=["bold"]),
                            table["compiler"].keys(),
                        )
                    )

                print(
                    tabulate(
                        table["compiler"],
                        headers=headers,
                        tablefmt="presto",
                    )
                )

        # remove builders if any invalid builders detected in build phase
        if invalid_builders:
            for test in invalid_builders:
                self.builders.remove(test)

        if not self.builders:
            raise BuildTestError(
                "Unable to create any test during build phase. Please check buildtest.log for more details"
            )

    def run_phase(self, printTable=False):
        """This method will run all builders with the appropriate executor.
        The executor argument is an instance of ``BuildExecutor`` that is responsible
        for orchestrating builder execution to the appropriate executor class. The
        executor contains a list of executors picked up from buildtest configuration.
        For tests running locally, we get the test metadata and count PASS/FAIL test
        state which is printed at end in Test Summary. For tests that need to run
        via scheduler, the first stage of run will dispatch job, and state will be
        `N/A`. We first dispatch all jobs and later poll jobs until they are complete.
        The poll section is skipped if all tests are run locally. In poll section we
        regenerate table with all valid_builders and updated test state and returncode
        and recalculate total pass/fail tests. Finally we return a list of valid_builders
        which are tests that ran through one of the executors. Any test that failed to run or be
        dispatched will be skipped during run stage and not added in `valid_builders`.
        The `valid_builders` contains the test meta-data that is used for updating
        test report in next stage.

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
            msg = """
+---------------------+
| Stage: Running Test |
+---------------------+ 
"""
            if os.getenv("BUILDTEST_COLOR") == "True":
                msg = colored(msg, "red", attrs=["bold"])

            print(msg)

        table = {
            "name": [],
            "id": [],
            "executor": [],
            "status": [],
            "returncode": [],
        }

        poll_queue = []

        for builder in self.builders:
            try:
                self.buildexecutor.run(builder)
            except ExecutorError as err:
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

            # for jobs with N/A state we append to poll queue which means job is dispatched to scheduler
            # and we poll job later
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
            headers = table.keys()
            if os.getenv("BUILDTEST_COLOR") == "True":
                headers = list(
                    map(lambda x: colored(x, "blue", attrs=["bold"]), headers)
                )

            print(tabulate(table, headers=headers, tablefmt="presto"))

        if errmsg:
            print("\n\n")
            print("Error Messages from Stage: Run")
            print("{:_<80}".format(""))
            for error in errmsg:
                print(error)
            print("\n")

        # poll will be True if one of the result State is N/A which is buildtest way to inform job is dispatched to scheduler which requires polling
        if poll:
            valid_builders = self.poll_jobs(poll_queue, valid_builders)

            table = {
                "name": [],
                "id": [],
                "executor": [],
                "status": [],
                "returncode": [],
            }

            if printTable:
                msg = """
+---------------------------------------------+
| Stage: Final Results after Polling all Jobs |
+---------------------------------------------+ 
"""
                if os.getenv("BUILDTEST_COLOR") == "True":
                    msg = colored(msg, "red", attrs=["bold"])

                print(msg)

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

                total_tests += 1

            if printTable:
                headers = table.keys()
                if os.getenv("BUILDTEST_COLOR") == "True":
                    headers = list(
                        map(lambda x: colored(x, "blue", attrs=["bold"]), headers)
                    )

                print(tabulate(table, headers=headers, tablefmt="presto"))

        ########## TEST SUMMARY ####################
        if total_tests == 0:
            print("No tests were executed")
            return

        if printTable:
            msg = """
+----------------------+
| Stage: Test Summary  |
+----------------------+ 
"""
            if os.getenv("BUILDTEST_COLOR") == "True":
                msg = colored(msg, "red", attrs=["bold"])

            print(msg)

            pass_rate = passed_tests * 100 / total_tests
            fail_rate = failed_tests * 100 / total_tests

            msg1 = f"Passed Tests: {passed_tests}/{total_tests} Percentage: {pass_rate:.3f}%"
            msg2 = f"Failed Tests: {failed_tests}/{total_tests} Percentage: {fail_rate:.3f}%"
            if os.getenv("BUILDTEST_COLOR") == "True":
                msg1 = colored(msg1, "green")
                msg2 = colored(msg2, "red")

            print(msg1)
            print(msg2)
            print("\n")

        return valid_builders

    def poll_jobs(self, poll_queue, valid_builders):
        """This method will poll jobs by processing all jobs in ``poll_queue``. If
        job is cancelled by scheduler, we remove this from valid_builders list.
        This method will return a list of valid_builders after polling. If there
        are no valid_builders after polling, the method will return None

        :param poll_queue: a list of jobs that need to be polled. The jobs will poll using poll method from executor
        :type poll_queue: list, required
        :param valid_builders: list of valid builders
        :type valid_builders: list, required
        """
        # default interval is 30sec for polling jobs if poll interval not set in configuration file or command line
        default_interval = 30

        interval = self.poll_interval or deep_get(
            self.configuration.target_config, "executors", "defaults", "pollinterval"
        )

        if not interval:
            interval = default_interval

        # keep track of ignored jobs by job scheduler these include jobs that failed abnormally or cancelled by scheduler
        ignore_jobs = set()
        completed_jobs = set()

        # loop until poll_queue is empty which means all jobs have finished
        while poll_queue:

            print("\n")
            print(f"Polling Jobs in {interval} seconds")
            print("{:_<40}".format(""))

            logger.debug(f"Sleeping for {interval} seconds")
            time.sleep(interval)
            logger.debug(f"Polling Jobs: {poll_queue}")

            for builder in poll_queue:
                poll_info = self.buildexecutor.poll(builder)

                # remove builder from poll_queue when state is True
                if poll_info["job_complete"]:
                    logger.debug(
                        f"{builder} poll complete, removing test from poll queue"
                    )
                    poll_queue.remove(builder)
                    completed_jobs.add(builder)

                # add invalid jobs to ignore_jobs list which are ignored from output
                # and not updated in report
                if poll_info["ignore_job"]:
                    ignore_jobs.add(builder)
                    completed_jobs.add(builder)

            jobIDs = []

            for job in poll_queue:
                jobIDs.append(job.metadata["jobid"])
            print("Job Queue:", jobIDs)

            completed_jobs_table = {
                "name": [],
                "executor": [],
                "jobID": [],
                "jobstate": [],
            }
            pending_jobs_table = {
                "name": [],
                "executor": [],
                "jobID": [],
                "jobstate": [],
            }
            for job in completed_jobs:
                completed_jobs_table["name"].append(job.name)
                completed_jobs_table["executor"].append(job.executor)
                completed_jobs_table["jobID"].append(job.metadata["jobid"])
                # completed_jobs_table["jobstate"].append(job.job_state)
                completed_jobs_table["jobstate"].append(job.job.state())

            for job in poll_queue:
                pending_jobs_table["name"].append(job.name)
                pending_jobs_table["executor"].append(job.executor)
                pending_jobs_table["jobID"].append(job.metadata["jobid"])
                # pending_jobs_table["jobstate"].append(job.job_state)
                pending_jobs_table["jobstate"].append(job.job.state())

            print("\n")
            print("Completed Jobs")
            print("{:_<40}".format(""))
            print("\n")
            print(
                tabulate(
                    completed_jobs_table,
                    headers=completed_jobs_table.keys(),
                    tablefmt="fancy_grid",
                )
            )

            print("\n")
            print("Pending Jobs")
            print("{:_<40}".format(""))
            print("\n")
            print(
                tabulate(
                    pending_jobs_table,
                    headers=pending_jobs_table.keys(),
                    tablefmt="fancy_grid",
                )
            )

        # remove any builders where for jobs that need to be ignored
        if ignore_jobs:
            # convert set to list
            ignore_jobs = list(ignore_jobs)
            for builder in ignore_jobs:
                valid_builders.remove(builder)

            print("Cancelled Tests:")
            for builder in ignore_jobs:
                print(builder.metadata["name"])

        # after removing jobs from valid_builders list there is chance we have no jobs to report
        # in that case we return from method
        if not valid_builders:
            sys.exit("After polling all jobs we found no valid builders to process")

        return valid_builders
