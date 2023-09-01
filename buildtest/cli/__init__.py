"""
buildtest cli: include functions to build, get test configurations, and
interact with a global configuration for buildtest.
"""
import argparse
import datetime
import sys

from pygments.styles import STYLE_MAP
from rich.color import Color, ColorParseError

from buildtest import BUILDTEST_COPYRIGHT, BUILDTEST_VERSION
from buildtest.defaults import console
from buildtest.schemas.defaults import schema_table

# Variables needed to show all sub commands and their help mesaage
show_all_help = "-H" in sys.argv or "--help-all" in sys.argv


def build_filters_format(val):
    """This method is used as validate argument type for ``buildtest build --filter``.
    This method returns a dict of key, value pairs where input is in the format
    **key1=val1,val2;key2=val3**. The semicolon is used to separate the keys and multiple values
    can be specified via comma

    Args:
       val (str): Input string in ``key1=value1,val2;key2=value3`` format that is processed into a dictionary type

    Returns:
        dict: A dict mapping of key=value pairs
    """

    kv_dict = {}

    if ";" in val:
        entries = val.split(";")
        for entry in entries:
            if "=" not in entry:
                raise argparse.ArgumentTypeError("Must specify k=v")

            key, values = entry.split("=")[0], entry.split("=")[1]
            value_list = values.split(",")
            kv_dict[key] = value_list

        return kv_dict

    if "=" not in val:
        raise argparse.ArgumentTypeError("Must specify in key=value format")

    key, values = val.split("=")[0], val.split("=")[1]
    value_list = values.split(",")
    kv_dict[key] = value_list

    return kv_dict


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


def supported_color(input_color):
    """Checks if input is a supported color and returns value as an Color type.

    Args:
        input_color (str): Specify an input color

    Returns:
        str: Return value as rich.color.Color type

    Raises:
        argparse.ArgumentTypeError will be raised if input is not a supported color input or is not str type

    >>> supported_color("red")
    red
    """

    if not isinstance(input_color, (str)):
        raise argparse.ArgumentTypeError(
            f"Input must be a string type, you have specified '{input_color}' which is of type {type(input_color)}"
        )
    try:
        color_val = Color.parse(input_color)
    except ColorParseError:
        console.print(f"[red]Unable to convert {input_color} to a Color ")
        console.print_exception()
        return
    return color_val


def valid_time(value):
    """Checks if input is valid time and returns value as a str type.

    Args:
        value (str): Specify an input date in yyyy-mm-dd format

    Returns:
        int: Return value as str type in correct format

    Raises:
        argparse.ArgumentTypeError will be raised if input is not str or input is not in desired format

    >>> valid_time("2022-01-01")
    "2022-01-01"

    >>> valid_time("2022-01-13")
    "2022-01-13"
    """

    if not isinstance(value, str):
        raise argparse.ArgumentTypeError(
            f"Input must be string type, you have specified '{value}' which is of type {type(value)}"
        )

    fmt = "%Y-%m-%d"

    try:
        dt_object = datetime.datetime.strptime(value, fmt)
    except ValueError:
        console.print(f"[red]Unable to convert {value} to correct date format")
        console.print_exception()
        raise ValueError

    return dt_object


class BuildTestParser:
    """This class implements the buildtest command line interface. This class
    implements the following methods:

    - :func:`get_parser`: This method builds the command line interface for buildtest
    - :func:`parse`: This method parses arguments passed to buildtest command line interface
    """

    _github = "https://github.com/buildtesters/buildtest"
    _docs = "https://buildtest.readthedocs.io/en/latest/index.html"
    _schemadocs = "https://buildtesters.github.io/buildtest/"
    _slack = "http://hpcbuildtest.slack.com/"
    _issues = "https://github.com/buildtesters/buildtest/issues"
    _progname = "buildtest"
    _description = (
        "buildtest is a HPC testing framework for building and running tests."
    )
    epilog_str = f"""
    References

    GitHub:                  {_github}
    Documentation:           {_docs}
    Schema Documentation:    {_schemadocs}
    Slack:                   {_slack}

    Please report issues at {_issues}

    {BUILDTEST_COPYRIGHT}
    """

    def __init__(self):
        self.subcommands = {
            "build": {"help": "Build and Run test", "aliases": ["bd"]},
            "buildspec": {"help": "Buildspec Interface", "aliases": ["bc"]},
            "config": {"help": "Query buildtest configuration", "aliases": ["cg"]},
            "report": {"help": "Query test report", "aliases": ["rt"]},
            "inspect": {"help": "Inspect a test", "aliases": ["it"]},
            "path": {"help": "Show path attributes for a given test", "aliases": ["p"]},
            "history": {"help": "Query build history", "aliases": ["hy"]},
            "schema": {"help": "List schema contents and examples"},
            "cdash": {"help": "Upload test to CDASH server"},
            "cd": {"help": "Change directory to root of test given a test name"},
            "clean": {
                "help": "Remove all generate files from buildtest including test directory, log files, report file, buildspec cache, history files"
            },
            "debugreport": {
                "help": "Display system information and additional information for debugging purposes.",
                "aliases": ["debug"],
            },
            "stats": {"help": "Show test statistics for given test"},
            "info": {"help": " Show details regarding current buildtest setup"},
            "show": {"help": "buildtest command guide"},
            "commands": {"help": "List all buildtest commands", "aliases": ["cmds"]},
            "tutorial-examples": {"help": ""},
            "schemadocs": {"help": ""},
            "unittests": {"help": "", "aliases": ["test"]},
            "stylecheck": {"help": "", "aliases": ["style"]},
        }

        self.build_parser()

    def parse(self, args=None):
        """This method parses arguments passed to buildtest command line interface

        Args:
            args (list, optional): List of arguments passed to buildtest command line interface. Defaults to None.

        Returns:
            argparse.Namespace: Return parsed arguments
        """

        return self.parser.parse_args(args)

    def get_subparsers(self):
        return self.subparsers

    def build_parser(self):
        self.parser = argparse.ArgumentParser(
            prog=self._progname,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=self._description,
            usage="%(prog)s [options] [COMMANDS]",
            epilog=self.epilog_str,
        )

        self.main_options()

        self.subparsers = self.parser.add_subparsers(
            title="COMMANDS", dest="subcommands", metavar=""
        )

        def get_parent_parser():
            parent_parser = {}

            parent_parser["pager"] = argparse.ArgumentParser(add_help=False)
            parent_parser["pager"].add_argument(
                "--pager", action="store_true", help="Enable PAGING when viewing result"
            )

            parent_parser["file"] = argparse.ArgumentParser(add_help=False)
            parent_parser["file"].add_argument(
                "--file", help="Write configuration file to a new file"
            )

            parent_parser["row-count"] = argparse.ArgumentParser(add_help=False)
            parent_parser["row-count"].add_argument(
                "--row-count",
                action="store_true",
                help="Display number of rows from query shown in table",
            )
            parent_parser["terse"] = argparse.ArgumentParser(add_help=False)
            parent_parser["terse"].add_argument(
                # "-t",
                "--terse",
                action="store_true",
                help="Print output in machine readable format",
            )
            parent_parser["no-header"] = argparse.ArgumentParser(add_help=False)
            parent_parser["no-header"].add_argument(
                "-n",
                "--no-header",
                action="store_true",
                help="Do not print header columns in terse output (--terse)",
            )
            parent_parser["count"] = argparse.ArgumentParser(add_help=False)
            parent_parser["count"].add_argument(
                "-c",
                "--count",
                type=int,
                help="Retrieve limited number of rows that get printed",
            )
            parent_parser["theme"] = argparse.ArgumentParser(add_help=False)
            parent_parser["theme"].add_argument(
                "--theme",
                metavar="Color Themes",
                help="Specify a color theme, Pygments style to use when displaying output. See https://pygments.org/docs/styles/#getting-a-list-of-available-styles for available themese",
                choices=list(STYLE_MAP.keys()),
            )
            return parent_parser

        self.parent_parser = get_parent_parser()
        self._build_subparsers()

        self.build_menu()
        self.buildspec_menu()
        self.config_menu()
        self.report_menu()
        self.inspect_menu()
        self.path_menu()
        self.history_menu()
        self.schema_menu()
        self.cdash_menu()
        self.unittest_menu()
        self.stylecheck_menu()
        self.misc_menu()

        # Displays all hidden commands
        if show_all_help:
            self.help_all()

    def _build_subparsers(self):
        """This method builds subparsers for buildtest command line interface."""
        for name, subcommand in self.subcommands.items():
            self.subparsers.add_parser(
                name, help=subcommand["help"], aliases=subcommand.get("aliases", [])
            )

    def main_options(self):
        """This method builds the main options for buildtest command line interface."""

        arguments = [
            (
                ["-V", "--version"],
                {
                    "action": "version",
                    "version": f"%(prog)s version {BUILDTEST_VERSION}",
                },
            ),
            (["-c", "--configfile"], {"help": "Specify Path to Configuration File"}),
            (
                ["-d", "--debug"],
                {"action": "store_true", "help": "Stream log messages to stdout"},
            ),
            (
                ["-l", "--loglevel"],
                {
                    "help": "Filter log messages based on logging level",
                    "choices": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                    "default": "DEBUG",
                },
            ),
            (
                ["--editor"],
                {
                    "help": "Select your preferred editor when opening files.",
                    "choices": ["vi", "vim", "emacs", "nano"],
                },
            ),
            (
                ["--view-log"],
                {"action": "store_true", "help": "Show content of last log"},
            ),
            (
                ["--logpath"],
                {"action": "store_true", "help": "Print full path to last log file"},
            ),
            (
                ["--print-log"],
                {
                    "action": "store_true",
                    "help": "Print content of last log without pagination",
                },
            ),
            (
                ["--color"],
                {
                    "type": supported_color,
                    "metavar": "COLOR",
                    "help": "Print output of table with the selected color.",
                },
            ),
            (
                ["--no-color"],
                {"help": "Disable colored output", "action": "store_true"},
            ),
            (
                ["--helpcolor"],
                {
                    "action": "store_true",
                    "help": "Print available color options in a table format.",
                },
            ),
            (["-r", "--report"], {"help": "Specify path to test report file"}),
            (
                ["-H", "--help-all"],
                {"help": "List all commands and options", "action": "help"},
            ),
        ]

        for args, kwargs in arguments:
            self.parser.add_argument(*args, **kwargs)
        return

    def misc_menu(self):
        """Build the command line menu for some miscellaneous commands"""

        cd_parser = self.subparsers.choices["cd"]
        cd_parser.add_argument(
            "test", help="Change directory to root of test for last run of test."
        )
        clean = self.subparsers.add_parser(
            "clean",
            help="Remove all generate files from buildtest including test directory, log files, report file, buildspec cache, history files.",
        )

        clean.add_argument(
            "-y", "--yes", action="store_true", help="Confirm yes for all prompts"
        )

        parser_stats = self.subparsers.choices["stats"]
        parser_stats.add_argument("name", help="Name of test")

        show_subparser = self.subparsers.choices["show"]
        show_subparser.add_argument(
            "command",
            choices=[
                "bd",
                "build",
                "bc",
                "buildspec",
                "cdash",
                "cg",
                "config",
                "hy",
                "history",
                "it",
                "inspect",
                "path",
                "rt",
                "report",
                "schema",
                "style",
                "stylecheck",
                "test",
                "unittests",
            ],
            help="Show help message for command",
        )

    def stylecheck_menu(self):
        """This method will create command options for ``buildtest stylecheck``"""

        # Subcommands that do not need to be shown in ``--help``
        stylecheck_parser = self.subparsers.choices["stylecheck"]

        # stylecheck_parser = self.subparsers.add_parser("stylecheck", aliases=["style"])

        stylecheck_args = [
            (
                ["--no-black"],
                {"action": "store_true", "help": "Don't run black style check"},
            ),
            (
                ["--no-isort"],
                {"action": "store_true", "help": "Don't run isort style check"},
            ),
            (
                ["--no-pyflakes"],
                {"action": "store_true", "help": "Don't run pyflakes check"},
            ),
            (
                ["-a", "--apply"],
                {"action": "store_true", "help": "Apply style checks to codebase."},
            ),
        ]

        for args, kwargs in stylecheck_args:
            stylecheck_parser.add_argument(*args, **kwargs)

    def unittest_menu(self):
        """This method builds the command line menu for ``buildtest unittests`` command"""
        unittests_parser = self.subparsers.choices["unittests"]

        unittests_args = [
            (
                ["-c", "--coverage"],
                {
                    "action": "store_true",
                    "help": "Enable coverage when running regression test",
                },
            ),
            (["-p", "--pytestopts"], {"type": str, "help": "Specify option to pytest"}),
            (
                ["-s", "--sourcefiles"],
                {
                    "type": str,
                    "help": "Specify path to file or directory when running regression test",
                    "action": "append",
                },
            ),
        ]

        for args, kwargs in unittests_args:
            unittests_parser.add_argument(*args, **kwargs)

    def path_menu(self):
        """This method builds the command line menu for ``buildtest path`` command"""

        path = self.subparsers.choices["path"]

        path_options = [
            (
                ["-be", "--buildenv"],
                {"action": "store_true", "help": "Show path to build environment"},
            ),
            (
                ["-t", "--testpath"],
                {"action": "store_true", "help": "Show path to test script"},
            ),
            (
                ["-o", "--outfile"],
                {"action": "store_true", "help": "Show path to output file"},
            ),
            (
                ["-e", "--errfile"],
                {"action": "store_true", "help": "Show path to error file"},
            ),
            (
                ["-b", "--buildscript"],
                {"action": "store_true", "help": "Show path to build script"},
            ),
            (
                ["-s", "--stagedir"],
                {"action": "store_true", "help": "Show path to stage directory"},
            ),
        ]

        path_group = path.add_mutually_exclusive_group()
        for args, kwargs in path_options:
            path_group.add_argument(*args, **kwargs)

        path.add_argument("name", help="Name of test")

    def history_menu(self):
        """This method builds the command line menu for ``buildtest history`` command"""

        history_subcmd = self.subparsers.choices["history"]

        history_subparser = history_subcmd.add_subparsers(
            metavar="", description="Query build history file", dest="history"
        )

        subparser_info = [
            {
                "name": "list",
                "help": "List a summary of all builds",
                "parents": [
                    self.parent_parser["pager"],
                    self.parent_parser["row-count"],
                    self.parent_parser["terse"],
                    self.parent_parser["no-header"],
                ],
                "args": [],
            },
            {
                "name": "query",
                "help": "Query information for a particular build",
                "parents": [self.parent_parser["pager"]],
                "args": [
                    (["id"], {"type": int, "help": "Select a build ID"}),
                    (
                        ["-l", "--log"],
                        {
                            "action": "store_true",
                            "help": "Display logfile for corresponding build id",
                        },
                    ),
                    (
                        ["-o", "--output"],
                        {
                            "action": "store_true",
                            "help": "View raw output from buildtest build command",
                        },
                    ),
                ],
            },
        ]

        for subparser_info in subparser_info:
            subparser = history_subparser.add_parser(
                subparser_info["name"],
                help=subparser_info["help"],
                parents=subparser_info["parents"],
            )
            for arg_args, arg_kwargs in subparser_info["args"]:
                subparser.add_argument(*arg_args, **arg_kwargs)

    def build_menu(self):
        """This method implements command line menu for ``buildtest build`` command."""

        parser_build = self.subparsers.choices["build"]

        groups = [
            (
                "discover",
                "discover",
                "Select buildspec file to run based on file, tag, executor",
            ),
            ("filter", "filter", "Filter tests after selection"),
            ("module", "module", "Module Selection option"),
            ("batch", "batch", "Batch Submission options"),
            ("extra", "extra", "All extra options"),
        ]
        arguments = {
            "discover": [
                (
                    ["-b", "--buildspec"],
                    {
                        "help": "Specify a buildspec (file or directory) to build. A buildspec must end in '.yml' extension.",
                        "action": "append",
                    },
                ),
                (
                    ["-x", "--exclude"],
                    {
                        "action": "append",
                        "help": "Exclude one or more buildspecs (file or directory) from processing. A buildspec must end in '.yml' extension.",
                    },
                ),
                (
                    ["-e", "--executor"],
                    {
                        "action": "append",
                        "type": str,
                        "help": "Discover buildspecs by executor name found in buildspec cache",
                    },
                ),
                (
                    ["-xt", "--exclude-tags"],
                    {
                        "action": "append",
                        "type": str,
                        "help": "Exclude tests by one or more tagnames found in buildspec cache",
                    },
                ),
                (
                    ["-t", "--tags"],
                    {
                        "action": "append",
                        "type": str,
                        "help": "Discover buildspecs by tags found in buildspec cache",
                    },
                ),
                (
                    ["--rerun"],
                    {
                        "action": "store_true",
                        "help": "Rerun last successful buildtest build command.",
                    },
                ),
            ],
            "filter": [
                (
                    ["-f", "--filter"],
                    {
                        "type": build_filters_format,
                        "help": "Filter buildspec based on tags, type, or maintainers. Usage:  --filter key1=val1,val2;key2=val3;key3=val4,val5",
                    },
                ),
                (
                    ["--helpfilter"],
                    {
                        "action": "store_true",
                        "help": "Show available filter fields used with --filter option",
                    },
                ),
                (
                    ["-et", "--executor-type"],
                    {
                        "choices": ["local", "batch"],
                        "help": "Filter tests by executor type (local, batch)",
                    },
                ),
            ],
            "module": [
                (
                    ["--module-purge"],
                    {
                        "action": "store_true",
                        "help": "Run 'module purge' before running any test",
                    },
                ),
                (
                    ["-m", "--modules"],
                    {
                        "type": str,
                        "help": "Specify a list of modules to load during test execution, to specify multiple modules each one must be comma separated for instance if you want to load 'gcc' and 'python' module you can do '-m gcc,python'",
                    },
                ),
                (
                    ["-u", "--unload-modules"],
                    {
                        "type": str,
                        "help": "Specify a list of modules to unload during test execution",
                    },
                ),
            ],
            "batch": [
                (
                    ["--account"],
                    {
                        "type": str,
                        "help": "Specify project account used to charge batch jobs (applicable for batch jobs only)",
                    },
                ),
                (
                    ["--maxpendtime"],
                    {
                        "type": positive_number,
                        "help": "Specify Maximum Pending Time (sec) for job before cancelling job. This only applies for batch job submission.",
                    },
                ),
                (
                    ["--pollinterval"],
                    {
                        "type": positive_number,
                        "help": "Specify Poll Interval (sec) for polling batch jobs",
                    },
                ),
                (
                    ["--procs"],
                    {
                        "nargs": "+",
                        "type": positive_number,
                        "help": "Specify number of processes to run tests (only applicable with batch jobs). Multiple values can be specified comma separated.",
                    },
                ),
                (
                    ["--nodes"],
                    {
                        "nargs": "+",
                        "type": positive_number,
                        "help": "Specify number of nodes to run tests (only applicable with batch jobs). Multiple values can be specified comma separated.",
                    },
                ),
            ],
            "extra": [
                (
                    ["--limit"],
                    {
                        "type": positive_number,
                        "help": "Limit number of tests that can be run.",
                    },
                ),
                (
                    ["--remove-stagedir"],
                    {
                        "action": "store_true",
                        "help": "Remove stage directory after job completion.",
                    },
                ),
                (
                    ["--rebuild"],
                    {
                        "type": positive_number,
                        "help": "Rebuild test X number of times. Must be a positive number between [1-50]",
                    },
                ),
                (
                    ["--retry"],
                    {
                        "type": positive_number,
                        "default": 1,
                        "help": "Retry failed jobs",
                    },
                ),
                (
                    ["-s", "--stage"],
                    {
                        "choices": ["parse", "build"],
                        "help": "Control behavior of buildtest build to stop execution after 'parse' or 'build' stage",
                    },
                ),
                (
                    ["--testdir"],
                    {
                        "help": "Specify a custom test directory where to write tests. This overrides configuration file and default location."
                    },
                ),
                (
                    ["--timeout"],
                    {
                        "type": positive_number,
                        "help": "Specify test timeout in number of seconds",
                    },
                ),
                (
                    ["--save-profile"],
                    {
                        "help": "Save buildtest command options into a profile and update configuration file"
                    },
                ),
                (
                    ["--profile"],
                    {"help": "Specify a profile to load from configuration file"},
                ),
            ],
        }

        for group_name, dest_name, desc in groups:
            group = parser_build.add_argument_group(group_name, description=desc)

            self.argument_group(arguments=arguments, group=group, dest_name=dest_name)

    def argument_group(self, arguments, group, dest_name):
        """This method adds arguments to a given group and destination name

        Args:
            arguments (dict): A dictionary of arguments to add to group
            group (argparse._ArgumentGroup): Argument group to add arguments
            dest_name (str): Destination name to add arguments to group

        Returns:

        """

        for arg_args, arg_kwargs in arguments[dest_name]:
            group.add_argument(*arg_args, **arg_kwargs)

    def buildspec_menu(self):
        """This method implements ``buildtest buildspec`` command"""

        parser_buildspec = self.subparsers.choices["buildspec"]

        subparsers_buildspec = parser_buildspec.add_subparsers(
            description="Buildspec Interface subcommands",
            dest="buildspecs_subcommand",
            metavar="",
        )

        buildspec_subcommands = [
            {
                "name": "edit-file",
                "help": "Edit buildspec file based on filename",
                "parents": [],
                "aliases": ["ef"],
                "args": [
                    (["file"], {"help": "Edit buildspec file in editor", "nargs": "*"})
                ],
            },
            {
                "name": "edit-test",
                "help": "Edit buildspec file based on test name",
                "parents": [],
                "aliases": ["et"],
                "args": [
                    (
                        ["name"],
                        {
                            "help": "Show content of buildspec based on test name",
                            "nargs": "*",
                        },
                    )
                ],
            },
            {
                "name": "find",
                "help": "Query information from buildspecs cache",
                "aliases": ["f"],
                "parents": [
                    self.parent_parser["pager"],
                    self.parent_parser["row-count"],
                    self.parent_parser["terse"],
                    self.parent_parser["no-header"],
                    self.parent_parser["count"],
                ],
                " args": [],
            },
            {
                "name": "maintainers",
                "help": "Query maintainers from buildspecs cache",
                "aliases": ["m"],
                "parents": [
                    self.parent_parser["row-count"],
                    self.parent_parser["terse"],
                    self.parent_parser["no-header"],
                ],
                "args": [
                    (
                        ["-b", "--breakdown"],
                        {
                            "action": "store_true",
                            "help": "Breakdown of buildspecs by maintainers",
                        },
                    )
                ],
            },
            {
                "name": "show",
                "help": "Show content of buildspec file",
                "parents": [self.parent_parser["theme"]],
                "aliases": ["s"],
                "args": [
                    (
                        ["name"],
                        {
                            "help": "Show content of buildspec based on test name",
                            "nargs": "*",
                        },
                    )
                ],
            },
            {
                "name": "show-fail",
                "help": "Show content of buildspec file for all failed tests",
                "parents": [self.parent_parser["theme"]],
                "aliases": ["sf"],
                "args": [
                    (
                        ["name"],
                        {
                            "help": "Show content of buildspec based on failed test name",
                            "nargs": "*",
                        },
                    )
                ],
            },
            {
                "name": "summary",
                "help": "Print summary of buildspec cache",
                "parents": [self.parent_parser["theme"], self.parent_parser["pager"]],
                "args": [],
                "aliases": ["sm"],
            },
            {
                "name": "validate",
                "help": "Validate buildspecs with JSON Schema",
                "parents": [],
                "aliases": ["val"],
                "args": [
                    (
                        ["-b", "--buildspec"],
                        {
                            "type": str,
                            "action": "append",
                            "help": "Specify path to buildspec (file, or directory) to validate",
                        },
                    ),
                    (
                        ["-x", "--exclude"],
                        {
                            "type": str,
                            "action": "append",
                            "help": "Specify path to buildspec to exclude (file or directory) during validation",
                        },
                    ),
                    (
                        ["-e", "--executor"],
                        {
                            "type": str,
                            "action": "append",
                            "help": "Specify buildspecs by executor name to validate",
                        },
                    ),
                    (
                        ["-t", "--tag"],
                        {
                            "type": str,
                            "action": "append",
                            "help": "Specify buildspecs by tag name to validate",
                        },
                    ),
                ],
            },
        ]

        subcommand = {}
        # Loop through the list of dictionaries and create subcommands with their parent parsers and arguments
        for cmd_info in buildspec_subcommands:
            name = cmd_info["name"]
            subcommand[name] = subparsers_buildspec.add_parser(
                cmd_info["name"],
                help=cmd_info["help"],
                parents=cmd_info["parents"],
                aliases=cmd_info.get("aliases", []),
            )
            for arg_info in cmd_info.get("args", []):
                subcommand[name].add_argument(*arg_info[0], **arg_info[1])

        # build menu for 'buildtest buildspec maintainers' command

        subparsers_maintainers = subcommand["maintainers"].add_subparsers()
        maintainers_find = subparsers_maintainers.add_parser(
            "find", help="Find buildspecs based on maintainer name"
        )
        maintainers_find.add_argument(
            "name", help="Find buildspec based on maintainer name"
        )

        # build menu for 'buildtest buildspec find' command
        self.buildspec_find_menu(subcommand["find"])

    def buildspec_find_menu(self, buildspec_find_parser):
        groups = [
            ("query", "query", "query options to retrieve from buildspec cache"),
            ("filter", "filter", "filter and format options"),
            ("extra", "extra", "All extra options"),
        ]
        arguments = {
            "query": [
                (
                    ["-b", "--buildspec"],
                    {
                        "help": "Get all buildspec files from cache",
                        "action": "store_true",
                    },
                ),
                (
                    ["-e", "--executors"],
                    {
                        "help": "Get all unique executors from buildspecs",
                        "action": "store_true",
                    },
                ),
                (
                    ["--group-by-tags"],
                    {"action": "store_true", "help": "Group tests by tag name"},
                ),
                (
                    ["--group-by-executor"],
                    {"action": "store_true", "help": "Group tests by executor name"},
                ),
                (
                    ["-p", "--paths"],
                    {"action": "store_true", "help": "Print all root buildspec paths"},
                ),
                (
                    ["-t", "--tags"],
                    {"action": "store_true", "help": "List all available tags"},
                ),
            ],
            "filter": [
                (
                    ["--filter"],
                    {
                        "type": handle_kv_string,
                        "help": "Filter buildspec cache with filter fields in format --filter key1=val1,key2=val2",
                    },
                ),
                (
                    ["--format"],
                    {
                        "help": "Format buildspec cache with format fields in format --format field1,field2,..."
                    },
                ),
                (
                    ["--helpfilter"],
                    {
                        "action": "store_true",
                        "help": "Show Filter fields for --filter option for filtering buildspec cache output",
                    },
                ),
                (
                    ["--helpformat"],
                    {
                        "action": "store_true",
                        "help": "Show Format fields for --format option for formatting buildspec cache output",
                    },
                ),
                (
                    ["--filterfields"],
                    {
                        "action": "store_true",
                        "help": "Print raw Filter fields for --filter option for filtering buildspec cache output",
                    },
                ),
                (
                    ["--formatfields"],
                    {
                        "action": "store_true",
                        "help": "Print raw Format fields for --format option for formatting buildspec cache output",
                    },
                ),
            ],
            "extra": [
                (
                    ["-r", "--rebuild"],
                    {
                        "action": "store_true",
                        "help": "Rebuild buildspec cache and find all buildspecs again",
                    },
                ),
                (
                    ["--root"],
                    {
                        "type": str,
                        "action": "append",
                        "help": "Specify root buildspecs (directory) path to load buildspecs into buildspec cache.",
                    },
                ),
                (
                    ["-q", "--quiet"],
                    {
                        "action": "store_true",
                        "help": "Don't print output of buildspec cache when rebuilding cache",
                    },
                ),
            ],
        }

        for group_name, dest_name, desc in groups:
            group = buildspec_find_parser.add_argument_group(
                group_name, description=desc
            )

            self.argument_group(arguments=arguments, group=group, dest_name=dest_name)

        buildtest_find_commands = [
            {
                "name": "invalid",
                "help": "Show invalid buildspecs",
                "parents": [self.parent_parser["row-count"]],
                "args": [
                    (
                        ["-e", "--error"],
                        {"action": "store_true", "help": "Show error messages"},
                    )
                ],
            }
        ]
        subcommand = {}
        subparsers_invalid = buildspec_find_parser.add_subparsers(
            metavar="", dest="buildspec_find_subcommand"
        )
        for cmd_info in buildtest_find_commands:
            name = cmd_info["name"]
            subcommand[name] = subparsers_invalid.add_parser(
                cmd_info["name"],
                help=cmd_info["help"],
                parents=cmd_info["parents"],
                aliases=cmd_info.get("aliases", []),
            )
            for arg_info in cmd_info.get("args", []):
                subcommand[name].add_argument(*arg_info[0], **arg_info[1])

    def config_menu(self):
        """This method adds argparse argument for ``buildtest config``"""

        parser_config = self.subparsers.choices["config"]

        subparsers_config = parser_config.add_subparsers(
            description="Query information from buildtest configuration file",
            dest="config",
            metavar="",
        )

        compilers = subparsers_config.add_parser(
            "compilers", aliases=["co"], help="Search compilers"
        )
        # buildtest config profile
        profile = subparsers_config.add_parser(
            "profiles", help="Query profile from buildtest configuration"
        )
        subparsers_profile = profile.add_subparsers(
            description="Query information about buildtest profiles",
            dest="profiles",
            metavar="",
        )

        subparsers_profile_list = subparsers_profile.add_parser(
            "list", help="List all profiles", parents=[self.parent_parser["theme"]]
        )
        # buildtest config profiles remove
        subparsers_profile_remove = subparsers_profile.add_parser(
            "remove", aliases=["rm"], help="Remove a profile from configuration"
        )
        subparsers_profile_remove.add_argument(
            "profile_name", nargs="*", help="Specify profile name to remove"
        )
        # buildtest config profile list options
        subparsers_profile_list.add_argument(
            "-y",
            "--yaml",
            action="store_true",
            help="List Profile details in YAML Format",
        )

        subparsers_config.add_parser(
            "edit", aliases=["e"], help="Open configuration file in editor"
        )

        executors = subparsers_config.add_parser(
            "executors",
            aliases=["ex"],
            help="Query executors from buildtest configuration",
        )
        subparsers_executors = executors.add_subparsers(
            description="Query executors from buildtest configuration",
            dest="executors",
            metavar="",
        )

        subparsers_config.add_parser(
            "path", aliases=["p"], help="Show path to configuration file"
        )

        subparsers_config.add_parser("systems", help="List all available systems")

        # buildtest config validate
        subparsers_config.add_parser(
            "validate",
            aliases=["val"],
            help="Validate buildtest settings file with schema.",
        )
        # buildtest config view
        subparsers_config.add_parser(
            "view",
            aliases=["v"],
            help="View configuration file",
            parents=[self.parent_parser["pager"], self.parent_parser["theme"]],
        )

        executors_list = subparsers_executors.add_parser(
            "list", help="List all executors"
        )
        executor_group = executors_list.add_mutually_exclusive_group()

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

        subparsers_compiler = compilers.add_subparsers(
            description="Find new compilers and add them to detected compiler section",
            dest="compilers",
            metavar="",
        )
        compiler_list = subparsers_compiler.add_parser("list", help="List compilers")
        compiler_remove = subparsers_compiler.add_parser(
            "remove", aliases=["rm"], help="Remove compilers"
        )
        compiler_remove.add_argument(
            "compiler_names", nargs="*", help="Specify compiler name to remove"
        )
        # buildtest config compilers
        compiler_list.add_argument(
            "-j",
            "--json",
            action="store_true",
            help="List compiler details in JSON format",
        )
        compiler_list.add_argument(
            "-y",
            "--yaml",
            action="store_true",
            help="List compiler details in YAML format",
        )

        compiler_find = subparsers_compiler.add_parser(
            "find", help="Find compilers", parents=[self.parent_parser["file"]]
        )
        compiler_find.add_argument(
            "-d",
            "--detailed",
            help="Display detailed output when finding compilers",
            action="store_true",
        )
        compiler_find.add_argument(
            "-u",
            "--update",
            action="store_true",
            help="Update configuration file with new compilers",
        )
        compiler_find.add_argument(
            "-m",
            "--modulepath",
            type=str,
            nargs="+",
            help="Specify a list of directories to search for modules via MODULEPATH to detect compilers",
        )

        compiler_test = subparsers_compiler.add_parser(
            "test", help="Test each compiler instance by performing module load test"
        )
        compiler_test.add_argument(
            "compiler_names", nargs="*", help="Specify compiler name to test"
        )

    def report_menu(self):
        """This method implements the ``buildtest report`` command options"""

        parser_report = self.subparsers.add_parser(
            "report",
            aliases=["rt"],
            help="Query test report",
            parents=[
                self.parent_parser["pager"],
                self.parent_parser["row-count"],
                self.parent_parser["terse"],
                self.parent_parser["no-header"],
                self.parent_parser["count"],
            ],
        )
        subparsers = parser_report.add_subparsers(
            description="Fetch test results from report file and print them in table format",
            metavar="",
            dest="report_subcommand",
        )
        subparsers.add_parser("clear", aliases=["c"], help="Remove all report file")
        subparsers.add_parser("list", aliases=["l"], help="List all report files")
        subparsers.add_parser(
            "path", aliases=["p"], help="Print full path to the report file being used"
        )
        parser_report_summary = subparsers.add_parser(
            "summary",
            aliases=["sm"],
            help="Summarize test report",
            parents=[self.parent_parser["pager"]],
        )
        filter_group = parser_report.add_argument_group("filter", "Filter options")

        # buildtest report
        filter_group.add_argument(
            "--filter",
            type=handle_kv_string,
            help="Filter report by filter fields. The filter fields must be a key=value pair and multiple fields can be comma separated in the following format: --filter key1=val1,key2=val2 . For list of filter fields run: --helpfilter.",
        )

        filter_group.add_argument(
            "--helpfilter",
            action="store_true",
            help="List available filter fields to be used with --filter option",
        )

        filter_group.add_argument(
            "--filterfields",
            action="store_true",
            help="Print raw filter fields for --filter option to filter the report",
        )

        format_group = parser_report.add_argument_group("format", "Format options")

        format_group.add_argument(
            "--helpformat", action="store_true", help="List of available format fields"
        )

        format_group.add_argument(
            "--formatfields",
            action="store_true",
            help="Print raw format fields for --format option to format the report",
        )

        format_detailed_group = parser_report.add_mutually_exclusive_group()
        format_detailed_group.add_argument(
            "--format",
            help="format field for printing purposes. For more details see --helpformat for list of available fields. Fields must be separated by comma (usage: --format <field1>,<field2>,...)",
        )

        format_detailed_group.add_argument(
            "-d",
            "--detailed",
            help="Print a detailed summary of the test results",
            action="store_true",
        )

        pass_fail = parser_report.add_mutually_exclusive_group()

        pass_fail.add_argument(
            "-f", "--fail", help="Retrieve all FAIL tests", action="store_true"
        )
        pass_fail.add_argument(
            "-p",
            "--pass",
            dest="passed",
            help="Retrieve all PASS tests",
            action="store_true",
        )

        parser_report.add_argument(
            "-s", "--start", type=valid_time, help="Retrieve tests by starttime"
        )
        parser_report.add_argument(
            "-e", "--end", type=valid_time, help="Retrieve tests by endtime"
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
        parser_report_summary.add_argument(
            "--detailed",
            "-d",
            action="store_true",
            help="Enable a more detailed report",
        )

    def inspect_menu(self):
        """This method builds argument for ``buildtest inspect`` command"""

        parser_inspect = self.subparsers.choices["inspect"]

        subparser = parser_inspect.add_subparsers(
            description="Inspect Test result based on Test ID or Test Name",
            dest="inspect",
            metavar="",
        )

        menu = {
            "buildspec": {
                "aliases": ["b"],
                "help": "Inspect a test based on buildspec",
                "parents": [self.parent_parser["pager"]],
                "args": [
                    (
                        ["buildspec"],
                        {"nargs": "*", "help": "List of buildspecs to query"},
                    ),
                    (
                        ["-a", "--all"],
                        {
                            "action": "store_true",
                            "help": "Fetch all records for a given test",
                        },
                    ),
                ],
            },
            "name": {
                "aliases": ["n"],
                "help": "Specify name of test",
                "parents": [self.parent_parser["pager"]],
                "args": [(["name"], {"nargs": "*", "help": "Name of test"})],
            },
            "query": {
                "aliases": ["q"],
                "help": "Query fields from record",
                "parents": [self.parent_parser["pager"], self.parent_parser["theme"]],
                "args": [
                    (
                        ["-b", "--buildscript"],
                        {"action": "store_true", "help": "Print build script"},
                    ),
                    (
                        ["-be", "--buildenv"],
                        {"action": "store_true", "help": "Print content of build env"},
                    ),
                    (
                        ["-e", "--error"],
                        {"action": "store_true", "help": "Print error file"},
                    ),
                    (
                        ["-o", "--output"],
                        {"action": "store_true", "help": "Print output file"},
                    ),
                    (
                        ["-t", "--testpath"],
                        {"action": "store_true", "help": "Print content of testpath"},
                    ),
                    (
                        ["name"],
                        {
                            "nargs": "*",
                            "help": "Name of builder to query in report file",
                        },
                    ),
                ],
            },
            "list": {
                "aliases": ["l"],
                "help": "List all test names, ids, and corresponding buildspecs",
                "parents": [
                    self.parent_parser["pager"],
                    self.parent_parser["row-count"],
                    self.parent_parser["terse"],
                    self.parent_parser["no-header"],
                ],
                "args": [
                    (
                        ["-b", "--builder"],
                        {"action": "store_true", "help": "List test in builder format"},
                    )
                ],
            },
        }

        # Create parsers and arguments using the menu dictionary
        for command, options in menu.items():
            parser = subparser.add_parser(
                command,
                aliases=options["aliases"],
                help=options["help"],
                parents=options["parents"],
            )
            for arg_info in options["args"]:
                parser.add_argument(*arg_info[0], **arg_info[1])

        return

    def schema_menu(self):
        """This method builds menu for ``buildtest schema``"""

        parser_schema = self.subparsers.choices["schema"]

        schema_args = [
            (
                ["-e", "--example"],
                {"action": "store_true", "help": "Show schema examples"},
            ),
            (
                ["-j", "--json"],
                {"action": "store_true", "help": "Display json schema file"},
            ),
            (
                ["-n", "--name"],
                {
                    "help": "show schema by name (e.g., script)",
                    "metavar": "Schema Name",
                    "choices": schema_table["names"],
                },
            ),
        ]

        for arg_info in schema_args:
            parser_schema.add_argument(*arg_info[0], **arg_info[1])

    def cdash_menu(self):
        """This method builds arguments for ``buildtest cdash`` command."""

        cdash_commands = {
            "view": {"help": "Open CDASH project in web browser"},
            "upload": {"help": "Upload test results to CDASH server"},
        }

        cdash_arguments = {
            "view": [],
            "upload": [
                (["--site"], {"help": "Specify site name reported in CDASH"}),
                (["buildname"], {"help": "Specify Build Name reported in CDASH"}),
                (
                    ["-o", "--open"],
                    {"action": "store_true", "help": "Open CDASH report in browser"},
                ),
            ],
        }

        parser_cdash = self.subparsers.choices["cdash"]
        subparser = parser_cdash.add_subparsers(
            description="buildtest CDASH integration", dest="cdash", metavar=""
        )

        for command, command_info in cdash_commands.items():
            cdash_parser = subparser.add_parser(command, **command_info)
            for args, args_info in cdash_arguments[command]:
                cdash_parser.add_argument(*args, **args_info)

        return
        parser_cdash = self.subparsers.choices["cdash"]

        subparser = parser_cdash.add_subparsers(
            description="buildtest CDASH integeration", dest="cdash", metavar=""
        )
        subparser.add_parser("view", help="Open CDASH project in webbrowser")

        upload = subparser.add_parser("upload", help="Upload Test to CDASH server")

        upload.add_argument("--site", help="Specify site name reported in CDASH")
        upload.add_argument("buildname", help="Specify Build Name reported in CDASH")
        upload.add_argument(
            "-o", "--open", action="store_true", help="Open CDASH report in browser"
        )

    def help_all(self):
        """This method will add parser for hidden command that can be shown when using ``--help-all/-H``"""
        hidden_parser = {
            "tutorial-examples": "Generate documentation examples for Buildtest Tutorial",
            "docs": "Open buildtest docs in browser",
            "schemadocs": "Open buildtest schema docs in browser",
            "unittests": {"help": "Run buildtest unit tests", "aliases": ["test"]},
            "stylecheck": {"help": "Run buildtest style checks", "aliases": ["style"]},
        }

        for command, val in hidden_parser.items():
            if type(val) is dict:
                self.subparsers.add_parser(
                    command, help=val.get("help"), aliases=val.get("aliases")
                )
            else:
                self.subparsers.add_parser(command, help=val)
