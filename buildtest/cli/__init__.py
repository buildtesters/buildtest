"""
buildtest cli: include functions to build, get test configurations, and
interact with a global configuration for buildtest.
"""
import argparse
import os

from buildtest import BUILDTEST_COPYRIGHT, BUILDTEST_VERSION
from buildtest.defaults import BUILD_REPORT
from buildtest.schemas.defaults import schema_table
from termcolor import colored


def single_kv_string(val):
    """This method is used for filter field in ``buildtest build --filter``.
    This method returns a dict of key/value pair where input must be a single key/value pair

    :param val: input value
    :type val: str
    :return: dictionary of key/value pairs
    :rtype: dict
    """

    kv_dict = {}

    if "=" not in val:
        raise argparse.ArgumentTypeError("Filter field must be in format key=value")

    key, value = val.split("=")[0], val.split("=")[1]
    kv_dict[key] = value

    return kv_dict


def handle_kv_string(val):
    """This method is used as type field in --filter argument in ``buildtest buildspec find``.
    This method returns a dict of key,value pair where input is in format
    key1=val1,key2=val2,key3=val3

    :param val: input value
    :type val: str
    :param multiple_keys: multiple_keys is a boolean to determine if key/value pair accepts multiple key/value arguments
    :type val: bool
    :return: dictionary of key/value pairs
    :rtype: dict
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
    """Checks if input value is positive value and within range of 1-50. This method
    is used for --rebuild option
    """

    value = int(value)
    if value <= 0:
        raise argparse.ArgumentTypeError(
            f"{value} must be a positive number between [1-50]"
        )
    return value


def get_parser():

    epilog_str = f"""
References
_______________________________________________________________________________________
GitHub:                  https://github.com/buildtesters/buildtest 
Documentation:           https://buildtest.readthedocs.io/en/latest/index.html             
Schema Documentation:    https://buildtesters.github.io/buildtest/
Slack:                   http://hpcbuildtest.slack.com/

Please report issues at https://github.com/buildtesters/buildtest/issues

{BUILDTEST_COPYRIGHT}
    """
    if os.getenv("BUILDTEST_COLOR") == "True":
        epilog_str = colored(epilog_str, "blue", attrs=["bold"])

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

    subparsers = parser.add_subparsers(title="COMMANDS", dest="subcommands", metavar="")

    build_menu(subparsers)
    history_menu(subparsers)
    buildspec_menu(subparsers)
    config_menu(subparsers)
    report_menu(subparsers)
    inspect_menu(subparsers)
    schema_menu(subparsers)
    cdash_menu(subparsers)

    subparsers.add_parser("docs", help="Open buildtest docs in browser")
    subparsers.add_parser("schemadocs", help="Open buildtest schema docs in browser")

    subparsers.add_parser("help", help="buildtest command guide")

    return parser


def history_menu(subparsers):
    """This method builds the command line menu for ``buildtest history`` command"""

    history_subcmd = subparsers.add_parser("history", help="Query build history")

    history_subparser = history_subcmd.add_subparsers(
        metavar="", description="Query build history file", dest="history"
    )

    list_parser = history_subparser.add_parser(
        "list", help="List a summary of all builds"
    )
    list_parser.add_argument(
        "-t",
        "--terse",
        action="store_true",
        help="Print output in machine readable format",
    )

    list_parser.add_argument(
        "-n",
        "--no-header",
        action="store_true",
        help="Do not print header columns in terse output (--terse)",
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


def build_menu(subparsers):
    """This method implements command line menu for ``buildtest build`` command."""

    parser_build = subparsers.add_parser("build", help="Build and Run test")

    parser_build.add_argument(
        "-b",
        "--buildspec",
        help="Specify a buildspec (file or directory) to build. A buildspec must end in '.yml' extension.",
        action="append",
    )

    parser_build.add_argument(
        "-x",
        "--exclude",
        action="append",
        help="Exclude one or more buildspecs (file or directory) from processing. A buildspec must end in '.yml' extension.",
    )

    parser_build.add_argument(
        "-t",
        "--tags",
        action="append",
        type=str,
        help="Discover buildspecs by tags found in buildspec cache",
    )

    parser_build.add_argument(
        "--filter",
        type=single_kv_string,
        help="Filter buildspec based on tags, type, or maintainers. Usage:  --filter key1=val1,key2=val2",
    )

    parser_build.add_argument(
        "-e",
        "--executor",
        action="append",
        type=str,
        help="Discover buildspecs by executor name found in buildspec cache",
    )
    parser_build.add_argument(
        "-s",
        "--stage",
        help="control behavior of buildtest build",
        choices=["parse", "build"],
    )

    parser_build.add_argument(
        "--testdir",
        help="Specify a custom test directory where to write tests. This overrides configuration file and default location.",
    )
    parser_build.add_argument(
        "--rebuild",
        type=positive_number,
        help="Rebuild test X number of times. Must be a positive number between [1-50]",
    )

    parser_build.add_argument(
        "-r",
        "--report",
        help="Specify a report file where tests will be written.",
    )
    parser_build.add_argument(
        "--max-pend-time",
        type=positive_number,
        help="Specify Maximum Pending Time (sec) for job before cancelling job. This only applies for batch job submission.",
    )
    parser_build.add_argument(
        "--poll-interval",
        type=positive_number,
        help="Specify Poll Interval (sec) for polling batch jobs",
    )
    parser_build.add_argument(
        "-k",
        "--keep-stage-dir",
        action="store_true",
        help="Keep stage directory after job completion.",
    )


def buildspec_menu(subparsers):
    """This method implements ``buildtest buildspec`` command"""

    parser_buildspec = subparsers.add_parser(
        "buildspec", help="Options for querying buildspec cache"
    )

    subparsers_buildspec = parser_buildspec.add_subparsers(
        description="Find buildspec from cache file",
        dest="buildspecs_subcommand",
        metavar="",
    )
    buildspec_find = subparsers_buildspec.add_parser("find", help="find all buildspecs")
    buildspec_validate = subparsers_buildspec.add_parser(
        "validate", help="Validate buildspecs"
    )

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
        "-t",
        "--tag",
        type=str,
        action="append",
        help="Specify buildspecs by tag name to validate",
    )

    buildspec_validate.add_argument(
        "-e",
        "--executor",
        type=str,
        action="append",
        help="Specify buildspecs by executor name to validate",
    )

    buildspec_find.add_argument(
        "--root",
        help="Specify root buildspecs (directory) path to load buildspecs into buildspec cache.",
        type=str,
        action="append",
    )

    buildspec_find.add_argument(
        "-r",
        "--rebuild",
        help="Rebuild buildspec cache and find all buildspecs again",
        action="store_true",
    )
    buildspec_find.add_argument(
        "-t", "--tags", help="List all available tags", action="store_true"
    )
    buildspec_find.add_argument(
        "-b",
        "--buildspec",
        help="Get all buildspec files from cache",
        action="store_true",
    )
    buildspec_find.add_argument(
        "-e",
        "--executors",
        help="get all unique executors from buildspecs",
        action="store_true",
    )
    buildspec_find.add_argument(
        "-p", "--paths", help="print all root buildspec paths", action="store_true"
    )
    buildspec_find.add_argument(
        "--group-by-tags", action="store_true", help="Group tests by tag name"
    )
    buildspec_find.add_argument(
        "--group-by-executor",
        action="store_true",
        help="Group tests by executor name",
    )
    buildspec_find.add_argument(
        "-m",
        "--maintainers",
        help="Get all maintainers for all buildspecs",
        action="store_true",
    )
    buildspec_find.add_argument(
        "-mb",
        "--maintainers-by-buildspecs",
        help="Show maintainers breakdown by buildspecs",
        action="store_true",
    )
    buildspec_find.add_argument(
        "--filter",
        type=handle_kv_string,
        help="Filter buildspec cache with filter fields in format --filter key1=val1,key2=val2",
    )
    buildspec_find.add_argument(
        "--format",
        help="Format buildspec cache with format fields in format --format field1,field2,...",
    )
    buildspec_find.add_argument(
        "--helpfilter",
        action="store_true",
        help="Show Filter fields for --filter option for filtering buildspec cache output",
    )
    buildspec_find.add_argument(
        "--helpformat",
        action="store_true",
        help="Show Format fields for --format option for formatting buildspec cache output",
    )
    buildspec_find.add_argument(
        "--terse", help="Print output in machine readable format", action="store_true"
    )

    buildspec_find.add_argument(
        "-n",
        "--no-header",
        action="store_true",
        help="Print output without header in terse output",
    )


def config_menu(subparsers):
    """This method adds argparse argument for ``buildtest config``"""

    parser_config = subparsers.add_parser(
        "config", help="Query buildtest configuration"
    )

    subparsers_config = parser_config.add_subparsers(
        description="Query information from buildtest configuration file",
        dest="config",
        metavar="",
    )

    executors = subparsers_config.add_parser(
        "executors", help="Query executors from buildtest configuration"
    )

    executors.add_argument(
        "-j", "--json", action="store_true", help="View executor in JSON format"
    )
    executors.add_argument(
        "-y", "--yaml", action="store_true", help="View executors in YAML format"
    )

    subparsers_config.add_parser("view", help="View Buildtest Configuration File")
    subparsers_config.add_parser(
        "validate", help="Validate buildtest settings file with schema."
    )

    subparsers_config.add_parser(
        "summary", help="Provide summary of buildtest settings."
    )
    subparsers_config.add_parser("systems", help="List all available systems")

    compilers = subparsers_config.add_parser(
        "compilers",
        help="search or find compilers",
    )

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


def report_menu(subparsers):
    """This method implements the ``buildtest report`` command options"""

    parser_report = subparsers.add_parser("report", help="Query test report")
    subparsers = parser_report.add_subparsers(
        description="Fetch test results from report file and print them in table format",
        metavar="",
        dest="report_subcommand",
    )
    subparsers.add_parser("clear", help="delete report file")
    subparsers.add_parser("list", help="List all report files")

    parser_report.add_argument(
        "--helpformat", action="store_true", help="List of available format fields"
    )
    parser_report.add_argument(
        "--helpfilter",
        action="store_true",
        help="List available filter fields to be used with --filter option",
    )
    parser_report.add_argument(
        "--format",
        help="format field for printing purposes. For more details see --helpformat for list of available fields. Fields must be separated by comma (usage: --format <field1>,<field2>,...)",
    )
    parser_report.add_argument(
        "--filter",
        type=handle_kv_string,
        help="Filter report by filter fields. The filter fields must be a key=value pair and multiple fields can be comma separated in the following format: --filter key1=val1,key2=val2 . For list of filter fields run: --helpfilter.",
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
        "-r",
        "--report",
        help="Specify a report file to read",
        default=BUILD_REPORT,
    )
    parser_report.add_argument(
        "-t",
        "--terse",
        action="store_true",
        help="Print output in machine readable format",
    )


def inspect_menu(subparsers):
    """This method builds argument for `buildtest inspect` command"""

    parser_inspect = subparsers.add_parser(
        "inspect", help="Inspect a test based on NAME or ID "
    )
    parser_inspect.add_argument(
        "-r", "--report", help="Specify a report file to load when inspecting test"
    )
    subparser = parser_inspect.add_subparsers(
        description="Inspect Test result based on Test ID or Test Name",
        dest="inspect",
        metavar="",
    )
    name = subparser.add_parser("name", help="Specify name of test")
    name.add_argument("name", nargs="*", help="Name of test")

    test_id = subparser.add_parser("id", help="Specify a Test ID")
    test_id.add_argument("id", nargs="*", help="Test ID")

    inspect_list = subparser.add_parser("list", help="List all test ids")
    inspect_list.add_argument(
        "-t", "--terse", action="store_true", help="Print output in terse format"
    )
    inspect_list.add_argument(
        "-n",
        "--no-header",
        action="store_true",
        help="Print output without header in terse format (--terse)",
    )

    query_list = subparser.add_parser("query", help="Query fields from record")
    query_list.add_argument(
        "-t", "--testpath", action="store_true", help="Print content of testpath"
    )
    query_list.add_argument(
        "-o", "--output", action="store_true", help="Print output file"
    )
    query_list.add_argument(
        "-e", "--error", action="store_true", help="Print error file"
    )
    query_list.add_argument(
        "-b", "--buildscript", action="store_true", help="Print build script"
    )
    query_list.add_argument(
        "-d",
        "--display",
        help="Determine how records are fetched, by default it will report the last record of the test.",
        choices=["first", "last", "all"],
        default="last",
    )
    query_list.add_argument("name", nargs="*", help="Name of test")


def schema_menu(subparsers):
    """This method builds menu for ``buildtest schema``"""

    parser_schema = subparsers.add_parser(
        "schema", help="List schema contents and examples"
    )

    parser_schema.add_argument(
        "-n",
        "--name",
        help="show schema by name (e.g., script)",
        metavar="Schema Name",
        choices=schema_table["names"],
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


def cdash_menu(subparsers):
    """This method builds arguments for `buildtest cdash` command."""

    parser_cdash = subparsers.add_parser("cdash", help="Upload test to CDASH server")

    subparser = parser_cdash.add_subparsers(
        description="buildtest CDASH integeration", dest="cdash", metavar=""
    )
    view = subparser.add_parser("view", help="Open CDASH project in webbrowser")
    view.add_argument("--url", help="Specify a url to CDASH project")

    upload = subparser.add_parser("upload", help="Upload Test to CDASH server")
    upload.add_argument("--site", help="Specify site name reported in CDASH")
    upload.add_argument("buildname", help="Specify Build Name reported in CDASH")
    upload.add_argument(
        "-r", "--report", help="Path to report file to upload test results"
    )
