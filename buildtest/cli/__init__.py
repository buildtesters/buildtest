"""
buildtest cli: include functions to build, get test configurations, and
interact with a global configuration for buildtest.
"""
import argparse

from buildtest import BUILDTEST_COPYRIGHT, BUILDTEST_VERSION
from buildtest.defaults import console
from buildtest.schemas.defaults import schema_table


def handle_kv_string(val):
    """This method is used as type field in --filter argument in ``buildtest buildspec find``.
    This method returns a dict of key,value pair where input is in format
    key1=val1,key2=val2,key3=val3

    Args:
       val (str): Input string in ``key1=value1,key2=value2`` format that is processed into a dictionary type

    Returns:
        dict: A dict mapping of key=value pairs
    """

    kv_dict = {}

    if "," in val:
        args = val.split(",")
        for kv in args:
            if "=" not in kv:
                raise argparse.ArgumentTypeError("Must specify k=v")

            key, value = kv.split("=")[0], kv.split("=")[1]
            kv_dict[key] = value

        return kv_dict

    if "=" not in val:
        raise argparse.ArgumentTypeError("Must specify in key=value format")

    key, value = val.split("=")[0], val.split("=")[1]
    kv_dict[key] = value

    return kv_dict


def positive_number(value):
    """Checks if input is positive number and returns value as an int type.

    Args:
        value (str or int): Specify an input number

    Returns:
        int: Return value as int type

    Raises:
        argparse.ArgumentTypeError will be raised if input is not positive number or input is not str or int type

    >>> positive_number("1")
    1

    >>> positive_number(2)
    2
    """

    if not isinstance(value, (str, int)):
        raise argparse.ArgumentTypeError(
            f"Input must be an integer or string type, you have specified '{value}' which is of type {type(value)}"
        )

    try:
        int_val = int(value)
    except ValueError:
        console.print(f"[red]Unable to convert {value} to int ")
        console.print_exception()
        raise ValueError

    if int_val <= 0:
        raise argparse.ArgumentTypeError(
            f"Input: {value} converted to int: {int_val} must be a positive number"
        )
    return int_val


def get_parser():

    epilog_str = f"""
References

GitHub:                  https://github.com/buildtesters/buildtest 
Documentation:           https://buildtest.readthedocs.io/en/latest/index.html             
Schema Documentation:    https://buildtesters.github.io/buildtest/
Slack:                   http://hpcbuildtest.slack.com/

Please report issues at https://github.com/buildtesters/buildtest/issues

{BUILDTEST_COPYRIGHT}
"""

    parser = argparse.ArgumentParser(
        prog="buildtest",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="buildtest is a HPC testing framework for building and running tests.",
        usage="%(prog)s [options] [COMMANDS]",
        epilog=epilog_str,
    )

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s version {BUILDTEST_VERSION}",
    )

    parser.add_argument(
        "-c", "--config", dest="configfile", help="Specify Path to Configuration File"
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Print debug messages to screen"
    )
    parser.add_argument(
        "--no-color", help="Disable colored output", action="store_true"
    )
    parser.add_argument("-r", "--report", help="Specify path to test report file")
    parser.add_argument(
        "--lastlog", action="store_true", help="Show content of last log"
    )
    subparsers = parser.add_subparsers(title="COMMANDS", dest="subcommands", metavar="")

    build_menu(subparsers)
    buildspec_menu(subparsers)
    config_menu(subparsers)
    report_menu(subparsers)
    inspect_menu(subparsers)
    history_menu(subparsers)
    schema_menu(subparsers)
    cdash_menu(subparsers)

    cd_parser = subparsers.add_parser(
        "cd", help="change directory to root of test given a test name"
    )
    cd_parser.add_argument(
        "test", help="Change directory to root of test for last run of test."
    )
    clean = subparsers.add_parser(
        "clean",
        help="Remove all generate files from buildtest including test directory, log files, report file, buildspec cache, history files.",
    )
    path = subparsers.add_parser("path", help="Show path attributes for a given test")
    path_group = path.add_mutually_exclusive_group()

    path_group.add_argument(
        "-t", "--testpath", action="store_true", help="Show path to test script"
    )
    path_group.add_argument(
        "-o", "--outfile", action="store_true", help="Show path to output file"
    )
    path_group.add_argument(
        "-e", "--errfile", action="store_true", help="Show path to error file"
    )
    path_group.add_argument(
        "-b", "--buildscript", action="store_true", help="Show path to build script"
    )
    path_group.add_argument(
        "-s", "--stagedir", action="store_true", help="Show path to stage directory"
    )

    path.add_argument("name", help="Name of test")

    subparsers.add_parser("docs", help="Open buildtest docs in browser")
    subparsers.add_parser("schemadocs", help="Open buildtest schema docs in browser")

    clean.add_argument(
        "-y", "--yes", action="store_true", help="Confirm yes for all prompts"
    )

    subparsers.add_parser(
        "debugreport",
        help="Display system information and additional information for debugging purposes.",
    )

    help_subparser = subparsers.add_parser(
        "help",
        aliases=["h"],
        help="buildtest command guide",
    )
    help_subparser.add_argument(
        "command",
        choices=[
            "build",
            "buildspec",
            "cdash",
            "config",
            "history",
            "inspect",
            "path",
            "report",
            "schema",
            "stylecheck",
            "unittests",
        ],
        help="Show help message for command",
    )
    unittests_parser = subparsers.add_parser(
        "unittests",
        help="Run buildtest unit tests",
    )
    unittests_parser.add_argument(
        "-c",
        "--coverage",
        action="store_true",
        help="Enable coverage when running regression test",
    )
    unittests_parser.add_argument(
        "-p", "--pytestopts", type=str, help="Specify option to pytest"
    )
    unittests_parser.add_argument(
        "-s",
        "--sourcefiles",
        type=str,
        help="Specify path to file or directory when running regression test",
        action="append",
    )

    stylecheck_parser = subparsers.add_parser(
        "stylecheck", aliases=["style"], help="Run buildtest style checks"
    )

    stylecheck_parser.add_argument(
        "--no-black", action="store_true", help="Don't run black style check"
    )
    stylecheck_parser.add_argument(
        "--no-isort", action="store_true", help="Don't run isort style check"
    )
    stylecheck_parser.add_argument(
        "--no-pyflakes", action="store_true", help="Dont' run pyflakes check"
    )
    stylecheck_parser.add_argument(
        "-a", "--apply", action="store_true", help="Apply style checks to codebase."
    )
    return parser


def history_menu(subparsers):
    """This method builds the command line menu for ``buildtest history`` command"""

    history_subcmd = subparsers.add_parser(
        "history", aliases=["hy"], help="Query build history"
    )

    history_subparser = history_subcmd.add_subparsers(
        metavar="", description="Query build history file", dest="history"
    )

    list_parser = history_subparser.add_parser(
        "list", help="List a summary of all builds"
    )
    list_parser.add_argument(
        "-n",
        "--no-header",
        action="store_true",
        help="Do not print header columns in terse output (--terse)",
    )
    list_parser.add_argument(
        "-t",
        "--terse",
        action="store_true",
        help="Print output in machine readable format",
    )
    list_parser.add_argument(
        "--pager", action="store_true", help="Enabling PAGING when viewing result"
    )

    query = history_subparser.add_parser(
        "query", help="Query information for a particular build"
    )
    query.add_argument("id", type=int, help="Select a build ID")
    query.add_argument(
        "-l",
        "--log",
        action="store_true",
        help="Display logfile for corresponding build id",
    )
    query.add_argument(
        "-o",
        "--output",
        action="store_true",
        help="view raw output from buildtest build command",
    )


def build_menu(subparsers):
    """This method implements command line menu for ``buildtest build`` command."""

    parser_build = subparsers.add_parser(
        "build", aliases=["bd"], help="Build and Run test"
    )

    discover_group = parser_build.add_argument_group(
        "select", "Select buildspec file to run based on file, tag, executor"
    )
    filter_group = parser_build.add_argument_group(
        "filter", "Filter tests after selection"
    )
    module_group = parser_build.add_argument_group("module", "Module Selection option")
    batch_group = parser_build.add_argument_group("batch", "Batch Submission Options ")
    extra_group = parser_build.add_argument_group("extra", "All extra options")

    discover_group.add_argument(
        "-b",
        "--buildspec",
        help="Specify a buildspec (file or directory) to build. A buildspec must end in '.yml' extension.",
        action="append",
    )

    discover_group.add_argument(
        "-x",
        "--exclude",
        action="append",
        help="Exclude one or more buildspecs (file or directory) from processing. A buildspec must end in '.yml' extension.",
    )

    discover_group.add_argument(
        "-e",
        "--executor",
        action="append",
        type=str,
        help="Discover buildspecs by executor name found in buildspec cache",
    )
    discover_group.add_argument(
        "-t",
        "--tags",
        action="append",
        type=str,
        help="Discover buildspecs by tags found in buildspec cache",
    )

    discover_group.add_argument(
        "--rerun",
        action="store_true",
        help="Rerun last successful buildtest build command.",
    )
    filter_group.add_argument(
        "-f",
        "--filter",
        type=handle_kv_string,
        help="Filter buildspec based on tags, type, or maintainers. Usage:  --filter key1=val1,key2=val2",
    )
    filter_group.add_argument(
        "--helpfilter",
        action="store_true",
        help="Show available filter fields used with --filter option",
    )
    filter_group.add_argument(
        "-et",
        "--executor-type",
        choices=["local", "batch"],
        help="Filter tests by executor type (local, batch) ",
    )
    module_group.add_argument(
        "--module-purge",
        action="store_true",
        help="Run 'module purge' before running any test ",
    )
    module_group.add_argument(
        "-m",
        "--modules",
        type=str,
        help="Specify a list of modules to load during test execution, to specify multiple modules each one must be comma "
        "separated for instance if you want to load 'gcc' and 'python' module you can do '-m gcc,python' ",
    )
    module_group.add_argument(
        "-u",
        "--unload-modules",
        type=str,
        help="Specify a list of modules to unload during test execution",
    )

    batch_group.add_argument(
        "--account",
        type=str,
        help="Specify project account used to charge batch jobs (applicable for batch jobs only)",
    )
    extra_group.add_argument(
        "--disable-executor-check",
        action="store_false",
        help="Disable executor check during configuration check. By default these checks are enforced for Local, Slurm, PBS, LSF, and Cobalt Executor.",
    )
    extra_group.add_argument(
        "-k",
        "--keep-stage-dir",
        action="store_true",
        help="Keep stage directory after job completion.",
    )
    batch_group.add_argument(
        "--maxpendtime",
        type=positive_number,
        help="Specify Maximum Pending Time (sec) for job before cancelling job. This only applies for batch job submission.",
    )
    batch_group.add_argument(
        "--pollinterval",
        type=positive_number,
        help="Specify Poll Interval (sec) for polling batch jobs",
    )
    batch_group.add_argument(
        "--procs",
        help="Specify number of processes to run tests (only applicable with batch jobs). Multiple values can be specified comma separated.",
        nargs="+",
        type=positive_number,
    )
    batch_group.add_argument(
        "--nodes",
        help="Specify number of nodes to run tests (only applicable with batch jobs). Multiple values can be specified comma separated.",
        nargs="+",
        type=positive_number,
    )
    extra_group.add_argument(
        "--rebuild",
        type=positive_number,
        help="Rebuild test X number of times. Must be a positive number between [1-50]",
    )

    extra_group.add_argument(
        "--retry", help="Retry failed jobs", type=positive_number, default=1
    )
    extra_group.add_argument(
        "-s",
        "--stage",
        help="Control behavior of buildtest build to stop execution after 'parse' or 'build' stage",
        choices=["parse", "build"],
    )

    extra_group.add_argument(
        "--testdir",
        help="Specify a custom test directory where to write tests. This overrides configuration file and default location.",
    )


def buildspec_menu(subparsers):
    """This method implements ``buildtest buildspec`` command"""

    parser_buildspec = subparsers.add_parser(
        "buildspec", aliases=["bc"], help="Buildspec Interface"
    )

    subparsers_buildspec = parser_buildspec.add_subparsers(
        description="Buildspec Interface subcommands",
        dest="buildspecs_subcommand",
        metavar="",
    )

    buildspec_find = subparsers_buildspec.add_parser(
        "find", help="Query information from buildspecs cache"
    )
    filter_group = buildspec_find.add_argument_group(
        "filter and format", "filter and format options"
    )
    terse_group = buildspec_find.add_argument_group("terse", "terse options")
    query_group = buildspec_find.add_argument_group(
        "query", "query options to retrieve from buildspec cache"
    )

    subparsers_invalid = buildspec_find.add_subparsers(
        metavar="", dest="buildspec_find_subcommand"
    )
    invalid_buildspecs = subparsers_invalid.add_parser(
        "invalid", help="Show invalid buildspecs"
    )

    subparsers_buildspec.add_parser("summary", help="Print summary of buildspec cache")

    show_buildspecs = subparsers_buildspec.add_parser(
        "show", help="Show content of buildspec file"
    )
    show_buildspecs.add_argument(
        "name",
        help="Show content of buildspec based on test name",
        nargs="*",
    )

    edit_buildspecs = subparsers_buildspec.add_parser(
        "edit", help="Edit buildspec file based on test name"
    )
    edit_buildspecs.add_argument(
        "name",
        help="Show content of buildspec based on test name",
        nargs="*",
    )

    edit_file = subparsers_buildspec.add_parser(
        "edit-file", help="Edit buildspec file based on filename"
    )
    edit_file.add_argument(
        "file",
        help="Edit buildspec file in editor",
        nargs="*",
    )

    buildspec_validate = subparsers_buildspec.add_parser(
        "validate", help="Validate buildspecs with JSON Schema"
    )
    # buildtest buildspec invalid options
    invalid_buildspecs.add_argument(
        "-e", "--error", action="store_true", help="Show error messages"
    )

    # buildtest buildspec validate options
    buildspec_validate.add_argument(
        "-b",
        "--buildspec",
        type=str,
        help="Specify path to buildspec (file, or directory) to validate",
        action="append",
    )

    buildspec_validate.add_argument(
        "-x",
        "--exclude",
        type=str,
        help="Specify path to buildspec to exclude (file or directory) during validation",
        action="append",
    )

    buildspec_validate.add_argument(
        "-e",
        "--executor",
        type=str,
        action="append",
        help="Specify buildspecs by executor name to validate",
    )
    buildspec_validate.add_argument(
        "-t",
        "--tag",
        type=str,
        action="append",
        help="Specify buildspecs by tag name to validate",
    )

    # buildtest buildspec find options

    query_group.add_argument(
        "-b",
        "--buildspec",
        help="Get all buildspec files from cache",
        action="store_true",
    )
    query_group.add_argument(
        "-e",
        "--executors",
        help="get all unique executors from buildspecs",
        action="store_true",
    )

    query_group.add_argument(
        "--group-by-tags", action="store_true", help="Group tests by tag name"
    )
    query_group.add_argument(
        "--group-by-executor",
        action="store_true",
        help="Group tests by executor name",
    )

    query_group.add_argument(
        "-m",
        "--maintainers",
        help="Get all maintainers for all buildspecs",
        action="store_true",
    )
    query_group.add_argument(
        "-mb",
        "--maintainers-by-buildspecs",
        help="Show maintainers breakdown by buildspecs",
        action="store_true",
    )
    query_group.add_argument(
        "-p", "--paths", help="print all root buildspec paths", action="store_true"
    )
    query_group.add_argument(
        "-t", "--tags", help="List all available tags", action="store_true"
    )

    filter_group.add_argument(
        "--filter",
        type=handle_kv_string,
        help="Filter buildspec cache with filter fields in format --filter key1=val1,key2=val2",
    )
    filter_group.add_argument(
        "--format",
        help="Format buildspec cache with format fields in format --format field1,field2,...",
    )
    filter_group.add_argument(
        "--helpfilter",
        action="store_true",
        help="Show Filter fields for --filter option for filtering buildspec cache output",
    )
    filter_group.add_argument(
        "--helpformat",
        action="store_true",
        help="Show Format fields for --format option for formatting buildspec cache output",
    )

    terse_group.add_argument(
        "-n",
        "--no-header",
        action="store_true",
        help="Print output without header in terse output",
    )
    terse_group.add_argument(
        "--terse", help="Print output in machine readable format", action="store_true"
    )
    buildspec_find.add_argument(
        "--pager", action="store_true", help="Enable PAGING when viewing result"
    )
    buildspec_find.add_argument(
        "-r",
        "--rebuild",
        help="Rebuild buildspec cache and find all buildspecs again",
        action="store_true",
    )
    buildspec_find.add_argument(
        "--root",
        help="Specify root buildspecs (directory) path to load buildspecs into buildspec cache.",
        type=str,
        action="append",
    )


def config_menu(subparsers):
    """This method adds argparse argument for ``buildtest config``"""

    parser_config = subparsers.add_parser(
        "config", aliases=["cg"], help="Query buildtest configuration"
    )

    subparsers_config = parser_config.add_subparsers(
        description="Query information from buildtest configuration file",
        dest="config",
        metavar="",
    )

    compilers = subparsers_config.add_parser("compilers", help="Search compilers")

    subparsers_config.add_parser("edit", help="Open configuration file in editor")

    executors = subparsers_config.add_parser(
        "executors", help="Query executors from buildtest configuration"
    )

    subparsers_config.add_parser("systems", help="List all available systems")

    subparsers_config.add_parser(
        "validate", help="Validate buildtest settings file with schema."
    )
    subparsers_config.add_parser("view", help="View configuration file")

    executor_group = executors.add_mutually_exclusive_group()

    # buildtest config executors
    executor_group.add_argument(
        "-j", "--json", action="store_true", help="View executor in JSON format"
    )
    executor_group.add_argument(
        "-y", "--yaml", action="store_true", help="View executors in YAML format"
    )
    executor_group.add_argument(
        "-d", "--disabled", action="store_true", help="Show disabled executors"
    )
    executor_group.add_argument(
        "-i", "--invalid", action="store_true", help="Show invalid executors"
    )

    # buildtest config compilers
    compilers.add_argument(
        "-j",
        "--json",
        action="store_true",
        help="List compiler details in JSON format",
    )
    compilers.add_argument(
        "-y",
        "--yaml",
        action="store_true",
        help="List compiler details in YAML format",
    )

    subparsers_compiler_find = compilers.add_subparsers(
        description="Find new compilers and add them to detected compiler section",
        dest="compilers",
        metavar="",
    )

    compiler_find = subparsers_compiler_find.add_parser(
        "find",
        help="Find compilers",
    )
    compiler_find.add_argument(
        "-d",
        "--debug",
        help="Display Debugging output when finding compilers",
        action="store_true",
    )
    compiler_find.add_argument(
        "-u",
        "--update",
        action="store_true",
        help="Update configuration file with new compilers",
    )


def report_menu(subparsers):
    """This method implements the ``buildtest report`` command options"""

    parser_report = subparsers.add_parser(
        "report", aliases=["rt"], help="Query test report"
    )
    subparsers = parser_report.add_subparsers(
        description="Fetch test results from report file and print them in table format",
        metavar="",
        dest="report_subcommand",
    )
    subparsers.add_parser("clear", help="Remove all report file")
    subparsers.add_parser("list", help="List all report files")
    parser_report_summary = subparsers.add_parser(
        "summary", help="Summarize test report"
    )

    # buildtest report
    parser_report.add_argument(
        "--filter",
        type=handle_kv_string,
        help="Filter report by filter fields. The filter fields must be a key=value pair and multiple fields can be comma separated in the following format: --filter key1=val1,key2=val2 . For list of filter fields run: --helpfilter.",
    )

    parser_report.add_argument(
        "--format",
        help="format field for printing purposes. For more details see --helpformat for list of available fields. Fields must be separated by comma (usage: --format <field1>,<field2>,...)",
    )
    parser_report.add_argument(
        "--helpfilter",
        action="store_true",
        help="List available filter fields to be used with --filter option",
    )
    parser_report.add_argument(
        "--helpformat", action="store_true", help="List of available format fields"
    )
    parser_report.add_argument(
        "--latest",
        help="Retrieve latest record of particular test",
        action="store_true",
    )
    parser_report.add_argument(
        "--oldest",
        help="Retrieve oldest record of particular test",
        action="store_true",
    )
    parser_report.add_argument(
        "-n",
        "--no-header",
        action="store_true",
        help="Don't print headers column used with terse option (--terse).",
    )

    parser_report.add_argument(
        "-t",
        "--terse",
        action="store_true",
        help="Print output in machine readable format",
    )
    parser_report.add_argument(
        "--pager", action="store_true", help="Enable PAGING when viewing result"
    )

    parser_report_summary.add_argument(
        "--pager", action="store_true", help="Enable PAGING when viewing result"
    )


def inspect_menu(subparsers):
    """This method builds argument for ``buildtest inspect`` command"""

    parser_inspect = subparsers.add_parser(
        "inspect", aliases=["it"], help="Inspect a test based on NAME or ID "
    )

    subparser = parser_inspect.add_subparsers(
        description="Inspect Test result based on Test ID or Test Name",
        dest="inspect",
        metavar="",
    )
    inspect_buildspec = subparser.add_parser(
        "buildspec", help="Inspect a test based on buildspec"
    )
    name = subparser.add_parser("name", help="Specify name of test")
    query_list = subparser.add_parser("query", help="Query fields from record")

    # buildtest inspect buildspec
    inspect_buildspec.add_argument(
        "buildspec", nargs="*", help="List of buildspecs to query"
    )
    inspect_buildspec.add_argument(
        "-a", "--all", action="store_true", help="Fetch all records for a given test"
    )

    name.add_argument("name", nargs="*", help="Name of test")

    # buildtest inspect list
    inspect_list = subparser.add_parser(
        "list", help="List all test names, ids, and corresponding buildspecs"
    )
    inspect_list.add_argument(
        "-n",
        "--no-header",
        action="store_true",
        help="Print output without header in terse format (--terse)",
    )
    inspect_list.add_argument(
        "-t", "--terse", action="store_true", help="Print output in terse format"
    )

    inspect_list.add_argument(
        "-b", "--builder", action="store_true", help="List test in builder format"
    )

    # buildtest inspect query
    query_list.add_argument(
        "-b", "--buildscript", action="store_true", help="Print build script"
    )

    query_list.add_argument(
        "-e", "--error", action="store_true", help="Print error file"
    )
    query_list.add_argument(
        "-o", "--output", action="store_true", help="Print output file"
    )
    query_list.add_argument(
        "-t", "--testpath", action="store_true", help="Print content of testpath"
    )
    query_list.add_argument(
        "name", nargs="*", help="Name of builder to query in report file"
    )


def schema_menu(subparsers):
    """This method builds menu for ``buildtest schema``"""

    parser_schema = subparsers.add_parser(
        "schema", help="List schema contents and examples"
    )
    parser_schema.add_argument(
        "-e",
        "--example",
        action="store_true",
        help="Show schema examples",
    )
    parser_schema.add_argument(
        "-j", "--json", action="store_true", help="Display json schema file"
    )
    parser_schema.add_argument(
        "-n",
        "--name",
        help="show schema by name (e.g., script)",
        metavar="Schema Name",
        choices=schema_table["names"],
    )


def cdash_menu(subparsers):
    """This method builds arguments for ``buildtest cdash`` command."""

    parser_cdash = subparsers.add_parser("cdash", help="Upload test to CDASH server")

    subparser = parser_cdash.add_subparsers(
        description="buildtest CDASH integeration", dest="cdash", metavar=""
    )
    subparser.add_parser("view", help="Open CDASH project in webbrowser")

    upload = subparser.add_parser("upload", help="Upload Test to CDASH server")

    upload.add_argument("--site", help="Specify site name reported in CDASH")
    upload.add_argument("buildname", help="Specify Build Name reported in CDASH")
