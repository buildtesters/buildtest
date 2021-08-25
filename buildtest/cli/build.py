"""
This module contains all the methods related to "buildtest build" which is used
for building test scripts from a Buildspec
"""
import json
import logging
import os
import re
import shutil
import sys
import tempfile
from datetime import datetime

from buildtest import BUILDTEST_VERSION
from buildtest.buildsystem.builders import Builder
from buildtest.buildsystem.parser import BuildspecParser
from buildtest.defaults import (
    BUILD_HISTORY_DIR,
    BUILD_REPORT,
    BUILDSPEC_CACHE_FILE,
    BUILDTEST_DEFAULT_TESTDIR,
    BUILDTEST_REPORT_SUMMARY,
)
from buildtest.exceptions import BuildspecError, BuildTestError
from buildtest.executors.poll import PollQueue
from buildtest.executors.setup import BuildExecutor
from buildtest.schemas.defaults import schema_table
from buildtest.system import system
from buildtest.utils.file import (
    create_dir,
    is_file,
    load_json,
    read_file,
    resolve_path,
    walk_tree,
)
from buildtest.utils.tools import Hasher, deep_get
from jsonschema.exceptions import ValidationError
from tabulate import tabulate
from termcolor import colored

logger = logging.getLogger(__name__)


def discover_buildspecs(
    buildspecs=None, exclude_buildspecs=None, executors=None, tags=None
):
    """This method discovers all buildspecs based on --buildspecs, --tags, --executor
    and excluding buildspecs (--exclude).

    :param buildspecs: List of input buildspecs passed by argument `buildtest build --buildspec`
    :type buildspecs: list
    :param exclude_buildspecs: List of excluded buildspecs by argument `buildtest build --exclude`
    :type exclude_buildspecs: list
    :param tags: List of input tags for discovering buildspecs by argument `buildtest build --tags`
    :type tags: list
    :param executors: List of input executors for discovering buildspecs by argument `buildtest build --executor`
    :type executors: list
    """

    # a dictionary used to keep track of included, excluded and detected buildspecs.
    buildspec_dict = {}
    buildspec_dict["included"] = []
    buildspec_dict["excluded"] = []
    buildspec_dict["detected"] = []
    buildspec_dict["tags"] = {}
    buildspec_dict["executors"] = {}

    logger.debug(
        f"Discovering buildspecs based on tags={tags}, executor={executors}, buildspec={buildspecs}, excluded buildspec={exclude_buildspecs}"
    )
    # discover buildspecs based on --tags
    if tags:
        found_buildspecs, buildspec_dict["tags"] = discover_buildspecs_by_tags(tags)

        buildspec_dict["included"] += found_buildspecs

        logger.debug(f"Discovered buildspecs based on tags: {tags}")
        logger.debug(found_buildspecs)

    # discover buildspecs based on --executor
    if executors:
        found_buildspecs, buildspec_dict["executors"] = discover_buildspecs_by_executor(
            executors
        )

        buildspec_dict["included"] += found_buildspecs
        logger.debug(f"Discovered buildspecs based on executors: {executors}")
        logger.debug(found_buildspecs)

    # discover buildspecs based on --buildspec
    if buildspecs:
        # Discover list of one or more Buildspec files based on path provided. Since --buildspec can be provided multiple
        # times we need to invoke discover_buildspecs once per argument.
        for option in buildspecs:
            bp = discover_by_buildspecs(option)

            # only add buildspecs if its not None
            if bp:
                buildspec_dict["included"] += bp

    # remove any duplicate Buildspec from list by converting list to set and then back to list
    buildspec_dict["included"] = list(set(buildspec_dict["included"]))

    # if no files discovered let's stop now
    if not buildspec_dict["included"]:
        msg = "There are no config files to process."
        sys.exit(msg)

    logger.debug(
        f"buildtest discovered the following Buildspecs: {buildspec_dict['included']}"
    )

    buildspec_dict["detected"] = buildspec_dict["included"].copy()

    # if user pass buildspecs to be excluded (buildtest build -x <buildspec>) then
    # discover all excluded buildspecs and remove from discovered list
    if exclude_buildspecs:

        # discover all excluded buildspecs, if its file add to list,
        # if its directory traverse all .yml files
        for name in exclude_buildspecs:
            bp = discover_by_buildspecs(name)
            if bp:
                buildspec_dict["excluded"] += bp

        # remove any duplicates from list
        buildspec_dict["excluded"] = list(set(buildspec_dict["excluded"]))

        logger.debug(
            f"The exclude pattern is the following: {buildspec_dict['excluded']}"
        )

        # detected buildspecs are any buildspecs in included buildspecs not in excluded buildspecs
        buildspec_dict["detected"] = [
            file
            for file in buildspec_dict["included"]
            if file not in buildspec_dict["excluded"]
        ]

        logger.debug(
            f"Buildspec list after applying exclusion: {buildspec_dict['detected']}"
        )

    # if no files remain after exclusion let's stop now.
    if not buildspec_dict["detected"]:
        msg = "There are no Buildspec files to process."
        sys.exit(msg)

    return buildspec_dict


def print_discovered_buildspecs(buildspec_dict):
    """This method will print the discovered buildspecs in the table format"""

    msg = """
+-------------------------------+
| Stage: Discovering Buildspecs |
+-------------------------------+ 
"""
    if os.getenv("BUILDTEST_COLOR") == "True":
        msg = colored(msg, "red", attrs=["bold"])

    print(msg)

    table = [[i] for i in buildspec_dict["included"]]
    headers = "Discovered Buildspecs"

    if os.getenv("BUILDTEST_COLOR") == "True":
        headers = colored(headers, "blue", attrs=["bold"])

    print(tabulate(table, headers=[headers], tablefmt="grid"))

    # if any buildspecs removed due to -x option we print them to screen
    if buildspec_dict["excluded"]:
        table = [[i] for i in buildspec_dict["excluded"]]
        headers = "Excluded Buildspecs"

        if os.getenv("BUILDTEST_COLOR") == "True":
            headers = colored(headers, "blue", attrs=["bold"])

        print(tabulate(table, headers=[headers], tablefmt="grid"))

    print("Discovered Buildspecs: ", len(buildspec_dict["included"]))
    print("Excluded Buildspecs: ", len(buildspec_dict["excluded"]))
    print("Detected Buildspecs after exclusion: ", len(buildspec_dict["detected"]))

    # print breakdown of buildspecs by tags
    if buildspec_dict.get("tags"):
        print("\nBREAKDOWN OF BUILDSPECS BY TAGS")
        print("----------------------------------")

        print(f"Detected Tag Names: {list(buildspec_dict['tags'].keys())}")

        for tagname in buildspec_dict["tags"].keys():
            headers = tagname
            if os.getenv("BUILDTEST_COLOR") == "True":
                headers = colored(headers, "blue", attrs=["bold"])

            # need to convert each element of list into a list type in order to print correctly
            rows = [[i] for i in buildspec_dict["tags"][tagname]]

            print(tabulate(rows, headers=[headers], tablefmt="grid"))
            print("\n")

    # print breakdown of buildspecs by executors
    if buildspec_dict.get("executors"):
        print("\nBREAKDOWN OF BUILDSPECS BY EXECUTORS")
        print("--------------------------------------")

        print(f"Detected Executor Names: {list(buildspec_dict['executors'].keys())}")

        for executorname in buildspec_dict["executors"].keys():
            headers = executorname
            if os.getenv("BUILDTEST_COLOR") == "True":
                headers = colored(headers, "blue", attrs=["bold"])

            rows = [[i] for i in buildspec_dict["executors"][executorname]]
            print(tabulate(rows, headers=[headers], tablefmt="grid"))
            print("\n")


def discover_buildspecs_by_tags(tagnames):
    """This method discovers buildspecs by tags, using ``--tags`` option
    from ``buildtest build`` command. This method will read BUILDSPEC_CACHE_FILE
    and search for ``tags`` key in buildspec recipe and match with input
    tag. Since ``tags`` field is a list, we check if input tag is in ``list``
    and if so we add the entire buildspec into a list. The return is a list
    of buildspec files to process.

    :param input_tag: List of input tags from command line argument ``buildtest build --tags <tags>``
    :type input_tag: list
    :return: a list of buildspec files that match tag name
    :rtype: list
    """

    tag_dict = {}

    if not is_file(BUILDSPEC_CACHE_FILE):
        raise BuildTestError(
            f"Cannot for buildspec cache: {BUILDSPEC_CACHE_FILE}, please run 'buildtest buildspec find' "
        )

    cache = load_json(BUILDSPEC_CACHE_FILE)

    buildspecs = []
    # query all buildspecs from BUILDSPEC_CACHE_FILE for tags keyword and
    # if it matches input_tag we add buildspec to list

    for name in tagnames:
        tag_dict[name] = set()

        for buildspecfile in cache["buildspecs"].keys():
            for test in cache["buildspecs"][buildspecfile].keys():

                # if input tag is not of type str we skip the tag name since it is not valid
                if not isinstance(name, str):
                    logger.warning(f"Tag: {name} is not of type 'str'")
                    continue

                # if tags is not declared we set to empty list
                tag = cache["buildspecs"][buildspecfile][test].get("tags") or []

                if name in tag:
                    buildspecs.append(buildspecfile)
                    tag_dict[name].add(buildspecfile)

    # remove any duplicates and return back a list
    buildspecs = list(set(buildspecs))

    return buildspecs, tag_dict


def discover_buildspecs_by_executor(executors):
    """This method discovers buildspecs by executor name, using ``buildtest build --executor``
    command. This method will read BUILDSPEC_CACHE_FILE and search for ``executor`` key
    in buildspec recipe and match with input executor name. The return is a list of matching
    buildspec with executor name to process.

    :param executors: List of input executor name from command line argument ``buildtest build --executor <name>``
    :type executors: list
    :return: a list of buildspec files that match tag name
    :rtype: list
    """

    executor_dict = {}

    if not is_file(BUILDSPEC_CACHE_FILE):
        raise BuildTestError(
            f"Cannot for buildspec cache: {BUILDSPEC_CACHE_FILE}, please run 'buildtest buildspec find' "
        )

    cache = load_json(BUILDSPEC_CACHE_FILE)

    buildspecs = []
    # query all buildspecs from BUILDSPEC_CACHE_FILE for tags keyword and
    # if it matches input_tag we add buildspec to list

    for name in executors:
        executor_dict[name] = set()

        for buildspecfile in cache["buildspecs"].keys():
            for test in cache["buildspecs"][buildspecfile].keys():

                # check if executor in buildspec matches one in argument (buildtest build --executor <EXECUTOR>)
                if name == cache["buildspecs"][buildspecfile][test].get("executor"):
                    buildspecs.append(buildspecfile)
                    executor_dict[name].add(buildspecfile)

    # remove any duplicates and return back a list
    buildspecs = list(set(buildspecs))

    return buildspecs, executor_dict


def discover_by_buildspecs(buildspec):
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


def print_filters():

    headers = ["Field", "Description"]
    format_fields = [
        ["tags", "Filter tests by 'tag' field"],
        ["type", "Filter test by 'type' field"],
        ["maintainers", "Filter test by 'maintainers' field"],
    ]

    if os.getenv("BUILDTEST_COLOR") != "True":
        print(tabulate(format_fields, headers=headers, tablefmt="simple"))
        return

    table = []
    for row in format_fields:
        table.append([colored(row[0], "green", attrs=["bold"]), colored(row[1], "red")])

    print(
        tabulate(
            table,
            headers=[colored(field, "blue", attrs=["bold"]) for field in headers],
            tablefmt="simple",
        )
    )


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
        filter_buildspecs=None,
        rebuild=None,
        buildtest_system=None,
        report_file=None,
        max_pend_time=None,
        poll_interval=None,
        keep_stage_dir=None,
        retry=None,
        helpfilter=None,
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
        :param filter_buildspecs: filters buildspecs and tests based on ``--filter`` argument which is a key/value dictionary that can filter tests based on tags, type, and maintainers
        :type filter_buildspecs: dict, optional
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
        :param keep_stage_dir: Keep stage directory after job completion
        :type keep_stage_dir: bool, optional
        :param retry: number of retry for failed jobs
        :type retry: int, optional
        :param helpfilter: Display available filter fields used by ``--filter`` option.
        :type helpfilter: bool, optional
        """

        if buildspecs and not isinstance(buildspecs, list):
            raise BuildTestError(f"{buildspecs} is not of type list")

        if exclude_buildspecs and not isinstance(exclude_buildspecs, list):
            raise BuildTestError(f"{exclude_buildspecs} is not of type list")

        if tags and not isinstance(tags, list):
            raise BuildTestError(f"{tags} is not of type list")

        if executors and not isinstance(executors, list):
            raise BuildTestError(f"{executors} is not of type list")

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

        self.keep_stage_dir = keep_stage_dir
        self.configuration = configuration
        self.buildspecs = buildspecs
        self.exclude_buildspecs = exclude_buildspecs
        self.tags = tags
        self.executors = executors
        self.max_pend_time = max_pend_time
        self.poll_interval = poll_interval
        self.helpfilter = helpfilter
        self.invalid_buildspecs = None
        self.retry = retry

        if self.helpfilter:
            print_filters()
            return

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
        self.filter_buildspecs = filter_buildspecs
        self.rebuild = rebuild

        # this variable contains the detected buildspecs that will be processed by buildtest.
        self.detected_buildspecs = None

        self.builders = None

        self.buildexecutor = BuildExecutor(
            self.configuration, max_pend_time=self.max_pend_time
        )
        self.system = buildtest_system or system
        self.report_file = resolve_path(report_file, exist=False) or BUILD_REPORT

        if self.filter_buildspecs:
            self._validate_filters()

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
        print("Command:", " ".join(sys.argv))

    def _validate_filters(self):
        """Check filter fields provided by ``buildtest build --filter`` are valid types and supported. Currently
        supported filter fields are 'tags', 'type', 'maintainers'
        """

        valid_fields = ["tags", "type", "maintainers"]

        for key in self.filter_buildspecs.keys():
            if key not in valid_fields:
                raise BuildTestError(
                    f"Invalid filter field: {key} the available filter fields are: {valid_fields}"
                )

            if key == "type":
                if self.filter_buildspecs[key] not in schema_table["types"]:
                    raise BuildTestError(
                        f"Invalid value for filter 'type': '{self.filter_buildspecs[key]}', valid schema types are : {schema_table['types']}"
                    )

    def build(self):
        """This method is responsible for discovering buildspecs based on input argument. Then we parse
        the buildspecs and retrieve builder objects for each test. Each builder object will invoke `build` which
        will build the test script, and then we run the test and update report.
        """

        # if --helpfilter is specified we return from this method
        if self.helpfilter:
            return

        self.discovered_bp = discover_buildspecs(
            buildspecs=self.buildspecs,
            exclude_buildspecs=self.exclude_buildspecs,
            tags=self.tags,
            executors=self.executors,
        )

        print_discovered_buildspecs(buildspec_dict=self.discovered_bp)

        self.detected_buildspecs = self.discovered_bp["detected"]

        # Parse all buildspecs and skip any buildspecs that fail validation, return type
        # is a builder object used for building test.
        self.parse_buildspecs()

        # if no builders found or  --stage=parse set we return from method
        if not self.builders or self.stage == "parse":
            return

        self.build_phase()

        # if --stage=build is set  we return from method
        if self.stage == "build":
            return

        self.builders = self.run_phase()

        # store path to logfile in each builder object. There is a single logfile per build.
        for builder in self.builders:
            builder.metadata["logpath"] = self.logfile.name

        if not self.keep_stage_dir:
            logger.debug("Removing stage directory for all tests")
            for builder in self.builders:
                shutil.rmtree(builder.stage_dir)

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

        self._update_build_history(self.builders)

    def resolve_testdirectory(self, testdir=None):
        """This method resolves which test directory to select. For example, one
        can specify test directory via command line ``buildtest build --testdir <path>``
        or path in configuration file. The default is $HOME/.buildtest/var/tests

        :param testdir: test directory from command line ``buildtest build --testdir``
        :type testdir: str
        :return: Path to test directory to use
        :rtype: str
        """

        # variable to set test directory if prefix is set
        prefix_testdir = resolve_path(
            self.configuration.target_config.get("testdir"), exist=False
        )

        # resolve full path for test directory specified by --testdir option
        testdir = resolve_path(testdir, exist=False)

        # Order of precedence when detecting test directory
        # 1. Command line option --testdir
        # 2. Configuration option specified by 'testdir'
        # 3. Defaults to $HOME/.buildtest/tests
        test_directory = testdir or prefix_testdir or BUILDTEST_DEFAULT_TESTDIR

        create_dir(test_directory)

        return test_directory

    def parse_buildspecs(self):
        """Parse all buildspecs by passing buildspec file to ``BuildspecParser`` class. If buildspec
        fails validation we skip the buildspec and print all skipped buildspecs.
        If buildspec passes validation we get all builders by invoking ``Builder`` class that
        is responsible for creating builder objects for each test.

        :return: A list of builder objects which are instances of ``BuilderBase`` class
        :rtype: list
        """

        msg = """
+---------------------------+
| Stage: Parsing Buildspecs |
+---------------------------+ 
"""
        if os.getenv("BUILDTEST_COLOR") == "True":
            msg = colored(msg, "red", attrs=["bold"])

        print(msg)

        self.builders = []

        self.invalid_buildspecs = []
        # store list of valid buildspecs that pass after calling BuildspecParser and used only for printing purpose
        valid_buildspecs = []

        # stores a list of buildspecs that are filtered out
        filtered_buildspecs = []

        # build all the tests
        for buildspec in self.detected_buildspecs:
            try:
                # Read in Buildspec file here, loading each will validate the buildspec file
                bp = BuildspecParser(buildspec, self.buildexecutor)
            except (BuildTestError, BuildspecError, ValidationError) as err:
                self.invalid_buildspecs.append(buildspec)
                logger.error(err)
                continue

            valid_buildspecs.append(buildspec)

            try:
                builder = Builder(
                    bp=bp,
                    buildexecutor=self.buildexecutor,
                    filters=self.filter_buildspecs,
                    testdir=self.testdir,
                    rebuild=self.rebuild,
                    buildtest_system=self.system,
                    configuration=self.configuration,
                )
            except BuildTestError as err:
                filtered_buildspecs.append(buildspec)
                logger.error(err)
                continue

            self.builders += builder.get_builders()

        print("Valid Buildspecs: ", len(valid_buildspecs))
        print("Invalid Buildspecs: ", len(self.invalid_buildspecs))

        print("Buildspecs that passed validation")
        print("{:_<80}".format(""))
        for buildspec in valid_buildspecs:
            print(buildspec)

        # print any skipped buildspecs if they failed to validate during build stage
        if len(self.invalid_buildspecs) > 0:
            print("\n\nBuildspecs that failed validation")
            print("{:_<80}".format(""))
            for test in self.invalid_buildspecs:
                print(test)

        if len(filtered_buildspecs) > 0:
            print("\nBuildspecs that were filtered out")
            print("{:_<80}".format(""))
            for test in filtered_buildspecs:
                print(test)

        # if no builders found we return from this method
        if not self.builders:
            sys.exit("Unable to create any builder objects")

        testnames = list(map(lambda x: x.name, self.builders))
        uid = list(map(lambda x: x.metadata["id"], self.builders))
        description = list(map(lambda x: x.recipe.get("description"), self.builders))
        buildspecs = list(map(lambda x: x.buildspec, self.builders))

        print("\n\n")

        headers = ["name", "id", "description", "buildspecs"]
        if os.getenv("BUILDTEST_COLOR") == "True":
            headers = list(map(lambda x: colored(x, "blue", attrs=["bold"]), headers))

        print(
            tabulate(
                zip(testnames, uid, description, buildspecs),
                headers=headers,
                tablefmt="simple",
            )
        )

        print("\n")
        print("Total builder objects created:", len(self.builders))
        print("builders:", self.builders)

    def build_phase(self):
        """This method will build all tests by invoking class method ``build`` for
        each builder that generates testscript in the test directory.
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
            table["spack"][field] = []

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
            table[builder.type]["testpath"].append(builder.build_script)

            if builder.type == "compiler":
                table[builder.type]["compiler"].append(builder.compiler)

            # set retry limit for each builder
            builder.retry(self.retry)

        self._print_build_phase(invalid_builders, table)

        # remove builders if any invalid builders detected in build phase
        if invalid_builders:
            for test in invalid_builders:
                self.builders.remove(test)

        if not self.builders:
            raise BuildTestError(
                "Unable to create any test during build phase. Please check buildtest.log for more details"
            )

    def run_phase(self):
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

        :return: A list of valid builders
        :rtype: list
        """

        msg = """
+---------------------+
| Stage: Running Test |
+---------------------+ 
"""
        if os.getenv("BUILDTEST_COLOR") == "True":
            msg = colored(msg, "red", attrs=["bold"])

        print(msg)

        self.buildexecutor.load_builders(self.builders)
        builders = self.buildexecutor.run()

        if not builders:
            sys.exit("Unable to run any tests")

        poll = False
        for builder in builders:
            if builder.is_batch_job():
                poll = True
                break

        # if any builders to poll we poll the jobs
        if poll:
            builders = self.poll_phase(builders)

        valid_builders = []
        for builder in builders:
            if builder.is_complete():
                valid_builders.append(builder)

        ########## TEST SUMMARY ####################
        if not valid_builders:
            sys.exit("Unable to run any tests")

        self._print_test_summary(valid_builders)

        return valid_builders

    def poll_phase(self, builders):
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

        poll_jobs = PollQueue(
            builders=builders, interval=interval, buildexecutor=self.buildexecutor
        )
        poll_jobs.poll()
        poll_jobs.print_polled_jobs()

        cancelled_jobs = poll_jobs.cancelled()
        completed_jobs = poll_jobs.completed()

        if completed_jobs:
            for builder in completed_jobs:
                builders.remove(builder)
                builders.append(builder)

        if cancelled_jobs:
            print("\nCancelled Jobs:", list(cancelled_jobs))

            for builder in cancelled_jobs:
                builders.remove(builder)
                builders.append(builder)

        return builders

    def _print_build_phase(self, invalid_builders, table):
        """print build phase table"""

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

        # if we have any tests using 'script' schema we print all tests together since table columns are different
        if len(table["spack"]["name"]) > 0:

            headers = table["spack"].keys()
            if os.getenv("BUILDTEST_COLOR") == "True":
                headers = list(
                    map(
                        lambda x: colored(x, "blue", attrs=["bold"]),
                        table["spack"].keys(),
                    )
                )

            print(
                tabulate(
                    table["spack"],
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

    def _print_run_phase(self, builders):
        """print run phase table"""

        table = {
            "name": [],
            "id": [],
            "executor": [],
            "status": [],
            "returncode": [],
            "runtime": [],
        }

        for builder in builders:
            # valid_builders.append(builder)
            table["name"].append(builder.name)
            table["id"].append(builder.metadata["id"])
            table["executor"].append(builder.executor)
            table["status"].append(builder.metadata["result"]["state"])
            table["returncode"].append(builder.metadata["result"]["returncode"])
            table["runtime"].append(builder.metadata["result"]["runtime"])

        headers = table.keys()
        if os.getenv("BUILDTEST_COLOR") == "True":
            headers = list(map(lambda x: colored(x, "blue", attrs=["bold"]), headers))

        print("\n")
        print(tabulate(table, headers=headers, tablefmt="presto"))

    def _print_test_summary(self, builders):
        """Print a summary of total pass and fail test with percentage breakdown."""

        msg = """
+----------------------+
| Stage: Test Summary  |
+----------------------+ 
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
            "runtime": [],
        }
        passed_tests = 0
        failed_tests = 0
        total_tests = 0
        for builder in builders:
            if builder.metadata["result"]["state"] == "PASS":
                passed_tests += 1
            else:
                failed_tests += 1

            table["name"].append(builder.name)
            table["id"].append(builder.metadata["id"])
            table["executor"].append(builder.executor)
            table["status"].append(builder.metadata["result"]["state"])
            table["returncode"].append(builder.metadata["result"]["returncode"])
            table["runtime"].append(builder.metadata["result"]["runtime"])

            total_tests += 1

        headers = table.keys()
        if os.getenv("BUILDTEST_COLOR") == "True":
            headers = list(map(lambda x: colored(x, "blue", attrs=["bold"]), headers))

        print(tabulate(table, headers=headers, tablefmt="presto"))
        print("\n\n")

        pass_rate = passed_tests * 100 / total_tests
        pass_rate = format(pass_rate, ".3f")
        fail_rate = failed_tests * 100 / total_tests
        fail_rate = format(fail_rate, ".3f")

        msg1 = f"Passed Tests: {passed_tests}/{total_tests} Percentage: {pass_rate}%"
        msg2 = f"Failed Tests: {failed_tests}/{total_tests} Percentage: {fail_rate}%"
        if os.getenv("BUILDTEST_COLOR") == "True":
            msg1 = colored(msg1, "green")
            msg2 = colored(msg2, "red")

        print(msg1)
        print(msg2)
        print("\n")

        self.test_summary = {
            "total": str(total_tests),
            "pass": str(passed_tests),
            "fail": str(failed_tests),
            "pass_rate": pass_rate,
            "fail_rate": fail_rate,
        }

    def _update_build_history(self, builders):
        """Write a build history file that is stored in **$BUILDTEST_ROOT/var/.history** directory summarizing output of build. The history
        file is a json file named `build.json` which contains a copy of the build log for troubleshooting. buildtest will create a sub-directory
        that is incremented such as 0, 1, 2 in **$BUILDTEST_ROOT/var/.history** which is used to differentiate builds.
        """

        create_dir(BUILD_HISTORY_DIR)
        num_files = len(os.listdir(BUILD_HISTORY_DIR))
        # create a sub-directory in $BUILDTEST_ROOT/var/.history/ that is incremented for every build starting with 0, 1, 2, ...
        build_history_dir = os.path.join(BUILD_HISTORY_DIR, str(num_files))
        create_dir(build_history_dir)
        build_history_file = os.path.join(build_history_dir, "build.json")

        # copy the logfile into the history directory
        shutil.copy2(
            self.logfile.name,
            os.path.join(build_history_dir, os.path.basename(self.logfile.name)),
        )

        history_data = {
            "command": " ".join(sys.argv),
            "user": self.system.system["user"],
            "hostname": self.system.system["host"],
            "platform": self.system.system["platform"],
            "date": datetime.now().strftime("%Y/%m/%d %X"),
            "buildtest": shutil.which("buildtest"),
            "python": self.system.system["python"],
            "python_version": self.system.system["pyver"],
            "testdir": self.testdir,
            "configuration": self.configuration.file,
            "system": self.configuration.name(),
            "logpath": os.path.join(
                build_history_dir, os.path.basename(self.logfile.name)
            ),
            "invalid_buildspecs": self.invalid_buildspecs,
            "buildspecs": {
                "detected": self.discovered_bp["detected"],
                "included": self.discovered_bp["included"],
                "excluded": self.discovered_bp["excluded"],
            },
            "test_summary": {
                "pass": self.test_summary["pass"],
                "fail": self.test_summary["fail"],
                "total": self.test_summary["total"],
                "pass_rate": self.test_summary["pass_rate"],
                "fail_rate": self.test_summary["fail_rate"],
            },
        }

        history_data["builders"] = {}
        for builder in builders:
            uid = str(builder.metadata["full_id"])
            history_data["builders"][uid] = {}
            history_data["builders"][uid]["name"] = builder.name
            history_data["builders"][uid]["buildspec"] = builder.buildspec
            history_data["builders"][uid]["tags"] = builder.metadata["tags"]
            history_data["builders"][uid]["executors"] = builder.metadata["executor"]
            history_data["builders"][uid]["state"] = builder.metadata["result"]["state"]
            history_data["builders"][uid]["returncode"] = builder.metadata["result"][
                "returncode"
            ]
            history_data["builders"][uid]["runtime"] = builder.metadata["result"][
                "runtime"
            ]
            history_data["builders"][uid]["testpath"] = builder.metadata["testpath"]
            history_data["builders"][uid]["errfile"] = builder.build_script
            history_data["builders"][uid]["outfile"] = builder.metadata["outfile"]
            history_data["builders"][uid]["errfile"] = builder.metadata["errfile"]

        with open(build_history_file, "w") as fd:
            fd.write(json.dumps(history_data, indent=2))


def update_report(valid_builders, report_file=BUILD_REPORT):
    """This method will update BUILD_REPORT after every test run performed
    by ``buildtest build``. If BUILD_REPORT is not created, we will create
    file and update json file by extracting contents from builder.metadata

    :param valid_builders: builder object that were successful during build and able to execute test
    :type valid_builders: instance of BuilderBase (subclass)
    :param report_file: specify location to report file
    :type report_file: str
    """

    if not is_file(os.path.dirname(report_file)):
        create_dir(os.path.dirname(report_file))

    report = {}

    # if file exists, read json file
    if is_file(report_file):
        report = load_json(report_file)

    for builder in valid_builders:
        buildspec = builder.buildspec
        name = builder.name
        entry = {}

        report[buildspec] = report.get(buildspec) or {}
        report[buildspec][name] = report.get(buildspec, {}).get(name) or []

        # query over attributes found in builder.metadata, we only assign
        # keys that we care about for reporting
        for item in [
            "id",
            "full_id",
            "description",
            "schemafile",
            "executor",
            "compiler",
            "hostname",
            "user",
            "testroot",
            "testpath",
            "stagedir",
            "command",
            "outfile",
            "errfile",
            "buildspec_content",
            "test_content",
            "buildscript_content",
            "logpath",
            "metrics",
        ]:
            entry[item] = builder.metadata[item]

        entry["tags"] = ""
        # convert tags to string if defined in buildspec
        if builder.metadata["tags"]:
            if isinstance(builder.metadata["tags"], list):
                entry["tags"] = " ".join(builder.metadata["tags"])
            else:
                entry["tags"] = builder.metadata["tags"]

        # query over result attributes, we only assign some keys of interest
        for item in ["starttime", "endtime", "runtime", "state", "returncode"]:
            entry[item] = str(builder.metadata["result"][item])

        entry["output"] = builder.metadata["output"]
        entry["error"] = builder.metadata["error"]

        entry["job"] = builder.metadata["job"]
        entry["build_script"] = builder.build_script
        report[buildspec][name].append(entry)

    with open(report_file, "w") as fd:
        json.dump(report, fd, indent=2)

    #  BUILDTEST_REPORT_SUMMARY file keeps track of all report files which
    #  contains a single line that denotes path to report file. This file only contains unique report files

    content = []
    if is_file(BUILDTEST_REPORT_SUMMARY):
        content = read_file(BUILDTEST_REPORT_SUMMARY)
        content = content.split("\n")

    if report_file not in content:
        content.append(report_file)

    with open(BUILDTEST_REPORT_SUMMARY, "w") as fd:
        fd.write("\n".join(content))
