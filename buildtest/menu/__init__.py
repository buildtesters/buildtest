"""
buildtest menu: include functions to build, get test configurations, and 
interact with a global configuration for buildtest.
"""

import argparse

from buildtest import BUILDTEST_VERSION
from buildtest.defaults import supported_schemas
from buildtest.menu.buildspec import (
    func_buildspec_find,
    func_buildspec_edit,
    func_buildspec_view,
)
from buildtest.menu.config import (
    func_config_edit,
    func_config_summary,
    func_config_validate,
    func_config_view,
)

from buildtest.menu.report import func_report
from buildtest.menu.schema import func_schema


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
            if "=" in kv:
                key, value = kv.split("=")[0], kv.split("=")[1]
                kv_dict[key] = value
            else:
                raise argparse.ArgumentTypeError("Must specify k=v")

    else:
        if "=" in val:
            key, value = val.split("=")[0], val.split("=")[1]
            kv_dict[key] = value

    return kv_dict
    # if '=' in split_args
    # if '=' in val:
    #    return val.split('=')
    # else:
    #    raise argparse.ArgumentTypeError('Must specify k=v')


class BuildTestParser:
    def __init__(self):
        epilog_str = (
            "Documentation: " + "https://buildtest.readthedocs.io/en/latest/index.html"
        )
        description_str = (
            "buildtest is a HPC testing framework for building and executing"
            + "tests. Buildtest comes with a set of json-schemas used to write "
            + "test configuration (Buildspecs) in YAML to generate test scripts."
        )

        self.parser = argparse.ArgumentParser(
            prog="buildtest",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=description_str,
            usage="%(prog)s [options] [COMMANDS]",
            epilog=epilog_str,
        )
        self.subparser_dict = {
            "build": "Options for building test scripts",
            "buildspec": "Command options for buildspecs",
            "report": "Show report for test results",
            "schema": "Commands for viewing buildtest schemas",
            "config": "Buildtest Configuration Menu",
        }

        self.main_menu()
        self.build_menu()
        self.buildspec_menu()
        self.report_menu()
        self.schema_menu()
        self.config_menu()

    def main_menu(self):
        """This method adds argument to ArgumentParser to main menu of buildtest"""

        command_description = ""
        for k, v in self.subparser_dict.items():
            command_description += "\n {:<30} {:<30}".format(k, v)

        self.subparsers = self.parser.add_subparsers(
            title="COMMANDS", description=command_description, dest="subcommands"
        )

        self.parser.add_argument(
            "-V",
            "--version",
            action="version",
            version=f"""buildtest version {BUILDTEST_VERSION}""",
        )
        self.parser.add_argument(
            "-d",
            "--debug",
            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            help="Enable debugging messages.",
        )
        self.parser.add_argument(
            "--docs", action="store_true", help="Open buildtest docs in browser"
        )
        self.parser.add_argument(
            "--schemadocs",
            action="store_true",
            help="Open buildtest  schema docs in browser",
        )

    def parse_options(self):
        """This method parses the argument from ArgumentParser class and returns
        the arguments. We store extra (non parsed arguments) with the class if
        they are needed.

        :return: return a parsed dictionary returned by ArgumentParser
        :rtype: dict
        """
        args, extra = self.parser.parse_known_args()
        self.extra = extra

        return args

    def build_menu(self):
        """This method implements the ``buildtest build`` command

            # single buildspec file

            ``buildtest build -b <file>``

            # single buildspec directory (builds all buildspec in directory)

            ``buildtest build -b <dir>``

            # build a buildspec and exclude some buildspecs. The exclude (-x) accepts both file and directory

            ``buildtest build -b <file> -x <file>``

           # multiple buildspecs build and exclude

           ``buildtest build -b <file> -b <dir> -x <file> -x <file>``

        """

        parser_build = self.subparsers.add_parser("build")

        ##################### buildtest build  ###########################

        parser_build.add_argument(
            "-b",
            "--buildspec",
            help="Specify a Buildspec (YAML) file to build and run the test.",
            action="append",
        )

        parser_build.add_argument(
            "-t",
            "--testdir",
            help="specify a custom test directory. By default, use .buildtest in $PWD.",
        )

        parser_build.add_argument(
            "--settings", help="Specify an alternate buildtest settings file to use",
        )

        parser_build.add_argument(
            "-x",
            "--exclude",
            action="append",
            help="Exclude one or more configs from processing. Configs can be files or directories.",
        )

        parser_build.add_argument(
            "--tags", help="Specify buildspecs by tags",
        )
        parser_build.add_argument(
            "-s",
            "--stage",
            help="control behavior of buildtest build",
            choices=["parse", "build"],
        )

    def buildspec_menu(self):
        """This method implements ``buildtest buildspec`` command

            Command Usage

            # find all buildspecs

            ``buildtest buildspec find``

            # view a buildspec file

            ``buildtest buildspec view <name>``

            # edit and validate a buildspec file

            ``buildtest buildspec edit <name>``

        """
        # ####################### buildtest buildspec  ########################
        parser_buildspec = self.subparsers.add_parser("buildspec")

        subparsers_buildspec = parser_buildspec.add_subparsers(
            description="Commands options for Buildspecs"
        )
        buildspec_find = subparsers_buildspec.add_parser(
            "find", help="find all buildspecs"
        )
        buildspec_find.add_argument(
            "-c",
            "--clear",
            help="Clear buildspec cache and find all buildspecs again",
            action="store_true",
        )
        buildspec_find.add_argument(
            "-t", "--tags", help="List all available tags", action="store_true"
        )
        buildspec_find.add_argument(
            "-bf",
            "--buildspec-files",
            help="Get all buildspec files from cache",
            action="store_true",
        )
        buildspec_find.add_argument(
            "-le",
            "--list-executors",
            help="get all unique executors from buildspecs",
            action="store_true",
        )

        buildspec_view = subparsers_buildspec.add_parser(
            "view", help="view a buildspec"
        )
        buildspec_view.add_argument("buildspec", help="name of buildspec")
        buildspec_edit = subparsers_buildspec.add_parser(
            "edit", help="edit a buildspec"
        )
        buildspec_edit.add_argument("buildspec", help="name of buildspec")

        buildspec_find.set_defaults(func=func_buildspec_find)
        buildspec_view.set_defaults(func=func_buildspec_view)
        buildspec_edit.set_defaults(func=func_buildspec_edit)

    def config_menu(self):
        """This method adds argparse argument for ``buildtest config``

           Command Usage

            # view buildtest settings file

            ``buildtest config view``

           # open buildtest settings in editor and validate upon saving

           ``buildtest config edit``

           # validate buildtest settings

           ``buildtest config validate``

           # summary of buildtest

           ``buildtest config summary``
        """

        parser_config = self.subparsers.add_parser("config")
        # #################### buildtest config   ###############################
        subparsers_config = parser_config.add_subparsers(
            description="buildtest configuration"
        )
        parser_config_view = subparsers_config.add_parser(
            "view", help="View Buildtest Configuration File"
        )
        parser_config_edit = subparsers_config.add_parser(
            "edit", help="Edit Buildtest Configuration File"
        )
        parser_config_validate = subparsers_config.add_parser(
            "validate", help="Validate buildtest settings file with schema."
        )
        parser_config_summary = subparsers_config.add_parser(
            "summary", help="Provide summary of buildtest settings."
        )

        parser_config_view.set_defaults(func=func_config_view)
        parser_config_edit.set_defaults(func=func_config_edit)
        parser_config_validate.set_defaults(func=func_config_validate)
        parser_config_summary.set_defaults(func=func_config_summary)

    def report_menu(self):
        """This method implements the ``buildtest report`` command options"""

        parser_report = self.subparsers.add_parser("report")
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
        ##################### buildtest report   ###########################

        parser_report.set_defaults(func=func_report)

    def schema_menu(self):
        """This method adds argparse argument for ``buildtest show``

            Command Usage

            # list all schema names

            -``buildtest schema``

            # list all schema in json

            -``buildtest schema -j``

            # list schema global.schema.json in json

            -``buildtest schema -n global.schema.json -j``

            # list schema examples for global.schema.json

            -``buildtest schema  -n global.schema.json -e``

        """

        # ################### buildtest schema  ########################
        parser_schema = self.subparsers.add_parser("schema")

        parser_schema.add_argument(
            "-n",
            "--name",
            help="show schema by name (e.g., script)",
            metavar="Schema Name",
            choices=supported_schemas,
        )
        parser_schema.add_argument(
            "-e",
            "--example",
            action="store_true",
            help="Show schema examples that are validated by corresponding schemafile",
        )
        parser_schema.add_argument(
            "-j", "--json", action="store_true", help="Display json schema file"
        )

        parser_schema.set_defaults(func=func_schema)
