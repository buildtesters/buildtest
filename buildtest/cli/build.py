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
    console,
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
from buildtest.utils.tools import deep_get
from jsonschema.exceptions import ValidationError
from rich import box
from rich.panel import Panel
from rich.table import Table

logger = logging.getLogger(__name__)


def resolve_testdirectory(configuration, testdir=None):
    """This method resolves which test directory to select. For example, one
    can specify test directory via command line ``buildtest build --testdir <path>``
    or path in configuration file. The default is $HOME/.buildtest/var/tests

    Args:
        configuration (buildtest.config.SiteConfiguration): An instance of SiteConfiguration class which contains content of buildtest configuration file
        testdir (str, optional): Path to test directory specified via command line ``buildtest build --testdir``

    Returns:
        str: Path to test directory
    """

    # variable to set test directory if prefix is set
    config_testdir = resolve_path(
        configuration.target_config.get("testdir"), exist=False
    )

    # resolve full path for test directory specified by --testdir option
    testdir = resolve_path(testdir, exist=False)

    # Order of precedence when detecting test directory
    # 1. Command line option --testdir
    # 2. Configuration option specified by 'testdir'
    # 3. Defaults to $BUILDTEST_ROOT/.var/tests
    test_directory = testdir or config_testdir or BUILDTEST_DEFAULT_TESTDIR

    return test_directory


def discover_buildspecs(
    buildspecs=None, exclude_buildspecs=None, executors=None, tags=None
):
    """This method discovers all buildspecs based on --buildspecs, --tags, --executor
    and excluding buildspecs (--exclude).

    Args:
        buildspecs (list, optional): List of input buildspecs passed by argument ``buildtest build --buildspec``
        exclude_buildspecs (list, optional): List of excluded buildspecs by argument ``buildtest build --exclude``
        tags (list, optional): List of input tags for discovering buildspecs by argument ``buildtest build --tags``
        executors (list, optional): List of input executors for discovering buildspecs by argument ``buildtest build --executor``

    Returns:
        dict: A dictionary containing a list of included, excluded, detected buildspecs and buildspecs detected based on tags and executors
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
    """This method will print the discovered buildspecs in table format

    Args:
        buildspec_dict (dict): A dictionary containing a list of included and excluded buildspecs and breakdown of buildspecs by tags and executors
    """

    console.rule("[bold red] Discovering Buildspecs")

    print("Discovered Buildspecs: ", len(buildspec_dict["included"]))
    print("Excluded Buildspecs: ", len(buildspec_dict["excluded"]))
    print("Detected Buildspecs after exclusion: ", len(buildspec_dict["detected"]))

    table = Table(
        "[blue]Buildspecs", title="Discovered buildspecs", box=box.DOUBLE_EDGE
    )

    for i in buildspec_dict["included"]:
        table.add_row(f"[red]{i}")
    console.print(table)

    # if any buildspecs removed due to -x option we print them to screen
    if buildspec_dict["excluded"]:

        table = Table(
            "[blue]Buildspecs", title="Excluded buildspecs", box=box.DOUBLE_EDGE
        )
        for i in buildspec_dict["excluded"]:
            table.add_row(f"[red]{i}")
        console.print(table)

    # print breakdown of buildspecs by tags
    if buildspec_dict.get("tags"):

        for tagname in buildspec_dict["tags"].keys():
            table = Table(
                "[blue]Buildspecs",
                title=f"Buildspecs By Tag={tagname}",
                box=box.DOUBLE_EDGE,
            )
            for row in buildspec_dict["tags"][tagname]:
                table.add_row(f"[red] {row}")
            console.print(table)

    # print breakdown of buildspecs by executors
    if buildspec_dict.get("executors"):

        for executorname in buildspec_dict["executors"].keys():
            table = Table(
                "[blue]Buildspecs",
                title=f"Buildspecs by Executor={executorname}",
                box=box.DOUBLE_EDGE,
            )

            for row in buildspec_dict["executors"][executorname]:
                table.add_row(f"[red]{row}")
            console.print(table)


def discover_buildspecs_by_tags(tagnames):
    """This method discovers buildspecs by tags, using ``buildtest build --tags`` option.
    This method will read BUILDSPEC_CACHE_FILE and search for ``tags`` key in buildspec recipe and
    match with input tag. The input ``tags`` are a list of tagnames to search in buildspec with the
    ``tags`` property in buildspec. The return is a list of buildspec files to process.

    Args:
        tagnames (list): List of input tags from command line argument ``buildtest build --tags <tags>``

    Returns:
        list, dict: first argument is a list of buildspecs discovered for all tag names. The second argument is
        dictionary breakdown of buildspecs by each tag name
    """

    tag_dict = {}

    """
    if not is_file(BUILDSPEC_CACHE_FILE):
        raise BuildTestError(
            f"Cannot for buildspec cache: {BUILDSPEC_CACHE_FILE}, please run 'buildtest buildspec find' "
        )
    """

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
    command. This method will read BUILDSPEC_CACHE_FILE and search for ``executor`` property
    in buildspec and match with input executor name. The return is a list of matching
    buildspec with executor name to process.

    Args:
        executors (list): List of input executor name from command line argument ``buildtest build --executor <name>``

    Returns:
         list, dict: first argument is a list of buildspecs discovered for all executors. The second argument is
         dictionary breakdown of buildspecs by each executor name
    """

    executor_dict = {}

    """
    if not is_file(BUILDSPEC_CACHE_FILE):
        raise BuildTestError(
            f"Cannot for buildspec cache: {BUILDSPEC_CACHE_FILE}, please run 'buildtest buildspec find' "
        )
    """

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
    with **.yml** extension. If filepath doesn't exist or file extension is not **.yml** we
    return None and capture error in log.

    .. code-block:: console

        # file path
        buildtest build --buildspec tutorials/hello.sh.yml

        # directory path
        buildtest build --buildspec tutorials

        # invalid file path returns None
        buildtest build -b /xyz.yml

        # invalid file extension
        buildtest build -b README.md


    Args:
        buildspec (str): Full path to buildspec based on argument ``buildtest build --buildspec``

    Returns:
        list: List of resolved buildspecs.
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
    """This method will print list of filters fields used by ``buildtest build --filter``. This method is invoked by
    running ``buildtest build --helpfilter``.
    """

    table = Table("[blue]Field", "[blue]Description", title="Buildtest Filters")
    table.add_row("[green]tags", "[red]Filter tests by 'tag' field")
    table.add_row("[green]type", "[red]Filter test by 'type' field")
    table.add_row("[green]maintainers", "[red]Filter test by 'maintainers' field")
    console.print(table)


class BuildTest:
    """This class is an interface to building tests via ``buildtest build`` command."""

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
        account=None,
        helpfilter=None,
    ):
        """The initializer method is responsible for checking input arguments for type
        check, if any argument fails type check we raise an error. If all arguments pass
        we assign the values and proceed with building the test.

        Args:
            configuration (buildtest.config.SiteConfiguration, optional): Loaded configuration content which is an instance of SiteConfiguration
            buildspecs (list, optional): list of buildspecs from command line ``buildtest build --buildspec``
            exclude_buildspecs (list, optional): list of excluded buildspecs from command line ``buildtest build --exclude``
            tags (list, optional): list if tags passed from command line ``buildtest build --tags``
            executors (list, optional): list of executors passed from command line ``buildtest build --executors``
            testdir (str): Path to test directory where tests are written. This argument can be passed from command line ``buildtest build --testdir``
            stage (str, optional): Stop build after parse or build stage which can be configured via ``buildtest build --stage`` option
            filter_buildspecs (dict, optional): filters buildspecs and tests based on ``buildtest build --filter`` argument which is a key/value dictionary that can filter tests based on **tags**, **type**, and **maintainers**
            rebuild (int, optional): Rebuild tests X times based on ``buildtest build --rebuild`` option.
            buildtest_system (buildtest.system.BuildTestSystem, optional): Instance of BuildTestSystem class
            report_file (str, optional): Location to report file where test data will be written upon completion. This can be specified via ``buildtest build --report`` command
            max_pend_time (int, optional): Specify maximum pending time in seconds for batch job until job is cancelled
            poll_interval (int, optional): Specify poll interval in seconds for polling batch jobs.
            keep_stage_dir (bool, optional): Keep stage directory after job completion
            retry (int, optional): Number of retry for failed jobs
            account (str, optional): Project account to charge jobs. This takes input argument ``buildtest build --account``
            helpfilter (bool, optional): Display available filter fields for ``buildtest build --filter`` command. This argument is set to ``True`` if one specifies ``buildtest build --helpfilter``
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
        self.account = account
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

        self.testdir = resolve_testdirectory(self.configuration, testdir)

        create_dir(self.testdir)

        self.stage = stage
        self.filter_buildspecs = filter_buildspecs
        self.rebuild = rebuild

        # this variable contains the detected buildspecs that will be processed by buildtest.
        self.detected_buildspecs = None

        self.builders = None

        self.buildexecutor = BuildExecutor(
            self.configuration, max_pend_time=self.max_pend_time, account=self.account
        )
        self.system = buildtest_system or system
        self.report_file = resolve_path(report_file, exist=False) or BUILD_REPORT

        if self.filter_buildspecs:
            self._validate_filters()

        msg = f"""
[magenta]User:[/]               [cyan]{self.system.system['user']}
[magenta]Hostname:[/]           [cyan]{self.system.system['host']}
[magenta]Platform:[/]           [cyan]{self.system.system['platform']}
[magenta]Current Time:[/]       [cyan]{datetime.now().strftime('%Y/%m/%d %X')}
[magenta]buildtest path:[/]     [cyan]{shutil.which('buildtest')}
[magenta]buildtest version:[/]  [cyan]{BUILDTEST_VERSION}    
[magenta]python path:[/]        [cyan]{self.system.system['python']}
[magenta]python version:[/]     [cyan]{self.system.system['pyver']}[/]
[magenta]Configuration File:[/] [cyan]{self.configuration.file}[/]
[magenta]Test Directory:[/]     [cyan]{self.testdir}[/]
[magenta]Command:[/]            [cyan]{' '.join(sys.argv)}[/]
"""
        console.print(Panel.fit(msg, title="buildtest summary"), justify="left")

    def _validate_filters(self):
        """Check filter fields provided by ``buildtest build --filter`` are valid types and supported. Currently
        supported filter fields are ``tags``, ``type``, ``maintainers``

        Raises:
            BuildTestError: if input filter field is not valid we raise exception. For ``type`` filter we check for value and make sure the schema type is supported
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
        the buildspecs and retrieve builder objects for each test. Each builder object will invoke :func:`buildtest.buildsystem.base.BuilderBase.build`
        which will build the test script, and then we run the test and update report.
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

    def parse_buildspecs(self):
        """Parse all buildspecs by passing buildspec file to :class:`buildtest.buildsystem.parser.BuildspecParser` class.
        If buildspec fails validation we skip the buildspec and print all skipped buildspecs.
        If buildspec passes validation we get all builders by invoking ``Builder`` class that
        is responsible for creating builder objects for each test.

        Raises:
            SystemExit: If no builders are created after parsing buildspecs
        """

        console.rule("[bold red]Parsing Buildspecs")
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

        console.print(f"Valid Buildspecs: [green]{len(valid_buildspecs)}")
        console.print(f"Invalid Buildspecs: [red]{len(self.invalid_buildspecs)}")

        for buildspec in valid_buildspecs:

            msg = f"[green]{buildspec}: VALID"
            console.print(msg)

        # print any skipped buildspecs if they failed to validate during build stage
        if len(self.invalid_buildspecs) > 0:
            for buildspec in self.invalid_buildspecs:

                msg = f"[red]{buildspec}: INVALID"
                console.print(msg)

        if len(filtered_buildspecs) > 0:
            table = Table("[blue]Buildspecs", title="Buildspecs Filtered out")

            for test in filtered_buildspecs:
                table.add_row(f"[red]{test}")
            console.print(table)

        # if no builders found we return from this method
        if not self.builders:
            sys.exit("Unable to create any builder objects")

        print("\n")
        print("Total builder objects created:", len(self.builders))
        print("\n")

        table = Table(title="Builder Details", show_lines=True)
        table.add_column("[blue]Builder", overflow="fold")
        table.add_column("[blue]Executor", overflow="fold")
        table.add_column("[blue]description", overflow="fold")
        table.add_column("[blue]buildspecs", overflow="fold")

        for builder in self.builders:
            description = builder.recipe.get("description") or ""

            table.add_row(
                f"[blue]{builder}",
                f"[green]{builder.executor}",
                f"[magenta]{description}",
                f"[yellow]{builder.buildspec}",
            )

        console.print(table)

    def build_phase(self):
        """This method will build all tests by invoking class method ``build`` for
        each builder that generates testscript in the test directory. If no builders are
        present upon building test we raise exception and terminate immediately

        Raises:
            BuildTestError: If no builders are present in build phase
        """

        invalid_builders = []
        console.rule("Building Test")

        valid_builders = []
        for builder in self.builders:
            try:
                builder.build()
            except BuildTestError as err:
                console.print(f"[red]{err}")
                invalid_builders.append(builder)
                logger.error(err)
                continue

            valid_builders.append(builder)

            # set retry limit for each builder
            builder.retry(self.retry)

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
        The :class:`buildtest.executors.setup.BuildExecutor` class is responsible for orchestrating builder execution to the
        appropriate executor class. The BuildExecutor contains a list of executors picked up from buildtest configuration.
        For tests running locally, we get the test metadata and count PASS/FAIL test
        state which is printed at end in Test Summary. For tests that need batch submission
        via scheduler, the first stage of run will dispatch job, and state will be
        unknown. After dispatching all jobs, we will poll jobs until they are complete.
        The poll section is skipped if all tests are run locally. In poll section we
        regenerate table with all valid builders and updated test state and returncode
        and recalculate total pass/fail tests. Any test that failed to run or be
        dispatched will be skipped during run stage and they will not be recorded in the test report

        Returns:
            A list of valid builders after running tests
        """

        console.rule("Running Tests")

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
        """This method will poll jobs by processing all builders. The :class:`buildtest.executors.poll.PollQueue`
        is responsible for polling builders at set interval until all jobs are complete. The ``PollQueue``
        will cancel job if it exceeds `max_pend_time` to ensure jobs are not stuck indefinitely. If
        job is cancelled by scheduler, we remove this from list of builders that will be returned from this method.
        This method will return a list of valid builders after polling. If there
        are no vali _builders after polling, the method will return **None**

        Args:
            builders (list): List of builder objects that require polling

        Returns:
            List of builder objects that ran to completion without any failure.
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

    def _print_test_summary(self, builders):
        """Print a summary of total pass and fail test with percentage breakdown.

        Args:
            builders (list): List of builders that ran to completion
        """

        table = Table(title="Test Summary", show_lines=True)
        table.add_column("[blue]Builder", overflow="fold")
        table.add_column("[blue]executor")
        table.add_column("[blue]status")
        table.add_column("[blue]Checks (ReturnCode, Regex, Runtime)", overflow="fold")
        table.add_column("[blue]ReturnCode")
        table.add_column("[blue]Runtime")

        passed_tests = 0
        failed_tests = 0
        total_tests = 0
        for builder in builders:
            if builder.metadata["result"]["state"] == "PASS":
                passed_tests += 1
                color_row = "green"
            else:
                failed_tests += 1
                color_row = "red"

            table.add_row(
                f"[{color_row}]{builder}",
                f"[{color_row}]{builder.executor}",
                f"[{color_row}]{builder.metadata['result']['state']}",
                f"[{color_row}]{builder.metadata['check']['returncode']} [{color_row}]{builder.metadata['check']['regex']} [{color_row}]{builder.metadata['check']['runtime']}",
                f"[{color_row}]{builder.metadata['result']['returncode']}",
                f"[{color_row}]{builder.metadata['result']['runtime']}",
            )

            total_tests += 1

        console.print(table)
        print("\n\n")

        pass_rate = passed_tests * 100 / total_tests
        pass_rate = format(pass_rate, ".3f")
        fail_rate = failed_tests * 100 / total_tests
        fail_rate = format(fail_rate, ".3f")

        msg1 = f"[green]Passed Tests: {passed_tests}/{total_tests} Percentage: {pass_rate}%"
        msg2 = (
            f"[red]Failed Tests: {failed_tests}/{total_tests} Percentage: {fail_rate}%"
        )

        console.print(msg1)
        console.print(msg2)
        print("\n")

        self.test_summary = {
            "total": str(total_tests),
            "pass": str(passed_tests),
            "fail": str(failed_tests),
            "pass_rate": pass_rate,
            "fail_rate": fail_rate,
        }

    def _update_build_history(self, builders):
        """Write a build history file that is stored in ``$BUILDTEST_ROOT/var/.history`` directory summarizing output of build. The history
        file is a json file named `build.json` which contains a copy of the build log for troubleshooting. buildtest will create a sub-directory
        that is incremented such as 0, 1, 2 in **$BUILDTEST_ROOT/var/.history** which is used to differentiate builds.

        Shown below is content of the top-level directory for the history directory. There is one subdirectory for each build ID starting with 0

        .. code-block:: console

            bash-3.2$ ls -l $BUILDTEST_ROOT/var/.history
            total 0
            drwxr-xr-x  4 siddiq90  92503  128 Sep  8 13:50 0
            drwxr-xr-x  4 siddiq90  92503  128 Sep  8 13:50 1

        For every build ID we have a ``build.json`` and log file for each build.

        .. code-block:: console

            bash-3.2$ ls $BUILDTEST_ROOT/var/.history/{0,1}
            /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/.history/0:
            build.json             buildtest_y3gh46j_.log

            /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/.history/1:
            build.json             buildtest_a1rjdy59.log
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
    file and update json file by extracting contents from builder metadata

    Args:
        valid_builders (list): List of valid builders that ran to completion
        report_file (str): Specify location to report file.
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
            "check",
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
