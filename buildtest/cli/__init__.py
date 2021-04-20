"""
buildtest cli: include functions to build, get test configurations, and
interact with a global configuration for buildtest.
"""
import argparse
import os

from termcolor import colored
from buildtest import BUILDTEST_VERSION, BUILDTEST_COPYRIGHT
from buildtest.defaults import BUILD_REPORT
from buildtest.schemas.defaults import schema_table


def handle_kv_string(val):
    """This method is used as type field in --filter argument in ``buildtest buildspec find``.
    This method returns a dict of key,value pair where input is in format
    key1=val1,key2=val2,key3=val3

    :param val: input value
    :type val: str
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
    if value <= 0 or value > 50:
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

    description_str = (
        "buildtest is a HPC testing framework for writing acceptance tests."
    )

    parser = argparse.ArgumentParser(
        prog="buildtest",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=description_str,
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
        "-d",
        "--debug",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Enable debugging messages.",
    )

    subparser_dict = {
        "build": "Options for building test scripts",
        "buildspec": "Options for querying buildspec cache",
        "report": "Options for querying test results",
        "schema": "Commands for viewing buildtest schemas",
        "config": "Buildtest Configuration Menu",
        "inspect": "Inspect details for test from test report",
        "docs": "Open buildtest docs in browser",
        "schemadocs": "Open buildtest schema docs in browser",
        "cdash": "Options to interact with CDASH server",
    }

    command_description = ""
    for k, v in subparser_dict.items():
        command_description += "\n {:<30} {:<30}".format(k, v)

    subparsers = parser.add_subparsers(
        title="COMMANDS", description=command_description, dest="subcommands"
    )

    subparsers.add_parser("docs")
    subparsers.add_parser("schemadocs")

    build_menu(subparsers)
    buildspec_menu(subparsers)
    config_menu(subparsers)
    report_menu(subparsers)
    inspect_menu(subparsers)
    schema_menu(subparsers)
    cdash_menu(subparsers)

    return parser


def build_menu(subparsers):
    """This method implements command line menu for ``buildtest build`` command."""

    parser_build = subparsers.add_parser("build")

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
        "-ft",
        "--filter-tags",
        action="append",
        type=str,
        help="Filter buildspecs by tags when building tests.",
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
        "-c", "--config", help="Specify path to buildtest configuration file"
    )
    parser_build.add_argument(
        "-r",
        "--report_file",
        help="Specify a report file where tests will be written.",
    )


def buildspec_menu(subparsers):
    """This method implements ``buildtest buildspec`` command"""

    parser_buildspec = subparsers.add_parser("buildspec")

    subparsers_buildspec = parser_buildspec.add_subparsers(
        description="Commands options for Buildspecs"
    )
    buildspec_find = subparsers_buildspec.add_parser("find", help="find all buildspecs")
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


def config_menu(subparsers):
    """This method adds argparse argument for ``buildtest config``"""

    parser_config = subparsers.add_parser("config")

    subparsers_config = parser_config.add_subparsers(
        description="query information from buildtest configuration file", dest="config"
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

    parser_report = subparsers.add_parser("report")
    subparsers = parser_report.add_subparsers(
        description="query information from buildtest configuration file", dest="report"
    )
    subparsers.add_parser("clear", help="delete report file")
    parser_report.add_argument(
        "--helpformat", action="store_true", help="List of available format fields"
    )
    parser_report.add_argument(
        "--format",
        help="format field for printing purposes. For more details see --helpformat for list of available fields. Fields must be separated by comma (--format <field1>,<field2>,...)",
    )
    parser_report.add_argument(
        "--filter",
        type=handle_kv_string,
        help="Filter report by filter fields. The filter fields must be set in format: --filter key1=val1,key2=val2,...",
    )
    parser_report.add_argument(
        "--helpfilter",
        action="store_true",
        help="Report a list of filter fields to be used with --filter option",
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
        "--report_file",
        help="Specify a report file to read",
        default=BUILD_REPORT,
    )


def inspect_menu(subparsers):
    """This method builds argument for `buildtest inspect` command """

    parser_inspect = subparsers.add_parser("inspect")
    parser_inspect.add_argument(
        "-r", "--report-file", help="Specify a report file to load when inspecting test"
    )
    subparser = parser_inspect.add_subparsers(
        help="subcommands", description="Inspect Test result", dest="inspect"
    )
    name = subparser.add_parser("name", help="Specify name of test")
    name.add_argument("name", nargs="*", help="Name of test")

    test_id = subparser.add_parser("id", help="Specify a Test ID")
    test_id.add_argument("id", nargs="*", help="Test ID")

    subparser.add_parser("list", help="List all test ids")


def schema_menu(subparsers):
    """This method builds menu for ``buildtest schema``"""

    parser_schema = subparsers.add_parser("schema")

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

    parser_cdash = subparsers.add_parser("cdash")
    subparser = parser_cdash.add_subparsers(
        help="subcommands", description="CDASH operations", dest="cdash"
    )
    view = subparser.add_parser("view", help="Open CDASH project in webbrowser")
    view.add_argument("--url", help="Specify a url to CDASH project")

    upload = subparser.add_parser("upload", help="Upload Test to CDASH server")
    upload.add_argument("--site", help="Specify site name reported in CDASH")
    upload.add_argument("buildname", help="Specify Build Name reported in CDASH")
    upload.add_argument(
        "--url",
        help="Specify url to CDASH server (example: https://my.cdash.org/submit.php?project=buildtest-cori)",
    )
    upload.add_argument(
        "-r", "--report-file", help="Path to report file to upload test results"
    )
