"""
buildtest menu: include functions to build, get test configurations, and 
interact with a global configuration for buildtest.
"""

import argparse

from buildtest.config import config_opts
from buildtest.menu.build import func_build_subcmd
from buildtest.menu.get import func_get_subcmd
from buildtest.menu.config import (
    func_config_edit,
    func_config_view,
    func_config_restore,
)

from buildtest.menu.show import func_show_subcmd, show_schema_layout
from buildtest.menu.status import show_status_report


class BuildTestParser:
    def __init__(self):
        epilog_str = (
            "Documentation: " + "https://buildtest.readthedocs.io/en/latest/index.html"
        )
        description_str = (
            "buildtest is a software testing framework designed "
            + "for HPC facilities to verify their Software Stack. buildtest "
            + "abstracts test complexity into YAML files that is interpreted"
            + "by buildtest into shell script"
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
            "show": "Options for displaying buildtest configuration",
            "config": "Buildtest Configuration Menu",
        }

        self.main_menu()
        self.build_menu()
        self.get_menu()
        self.config_menu()
        self.show_menu()

    def main_menu(self):
        """This method adds argument to ArgumentParser to main menu of buildtest"""
        command_description = ""
        for k, v in self.subparser_dict.items():
            command_description += f"""\n      {k}           {v}"""

        self.subparsers = self.parser.add_subparsers(
            title="COMMANDS", description=command_description, dest="subcommands"
        )

        self.parser.add_argument(
            "-V",
            "--version",
            action="version",
            version=f"""buildtest version {config_opts["BUILDTEST_VERSION"]}""",
        )

    def parse_options(self):
        """This method parses the argument from ArgumentParser class and returns as a dictionary. Also it
        redirects sub-commands to appropriate methods.

        :return: return a parsed dictionary returned by ArgumentParser
        :rtype: dict
        """
        args = self.parser.parse_args()

        if args.subcommands:
            args.func(args)

        return args

    def build_menu(self):
        """This method implements argparse argument for ``buildtest build``"""

        parser_build = self.subparsers.add_parser("build")

        ##################### buildtest build     ###########################
        parser_build.add_argument(
            "--clear",
            help="Clear build history and remove all tests",
            action="store_true",
        )

        parser_build.add_argument(
            "-c",
            "--config",
            help="Specify test configuration file.",
            metavar="TEST CONFIGURATION",
        )

        parser_build.add_argument(
            "-d",
            "--dry",
            help="dry-run mode, buildtest will not write the test scripts but print "
            "content of test that would be written",
            action="store_true",
        )

        # parser_build.set_defaults(func=func_build_subcmd)

        # -------------------------- buildtest build report ------------------------------
        subparsers_build = parser_build.add_subparsers(
            description="Report status on builds performed by buildtest."
        )

        parser_report = subparsers_build.add_parser(
            "report", help="Report status details of all builds "
        )
        parser_report.set_defaults(func=show_status_report)

    def get_menu(self):
        """This method implements argparse argument for ``buildtest get``"""

        parser_get = self.subparsers.add_parser("get")

        ##################### buildtest get       ###########################
        parser_get.add_argument(
            "repo", help="specify github.com or other repository to clone."
        )

        parser_get.add_argument(
            "-b",
            "--branch",
            help="Clone a particular branch (defaults to master)",
            default="master",
        )

        parser_get.set_defaults(func=func_get_subcmd)

    def config_menu(self):
        """This method adds argparse argument for ``buildtest config``"""
        parser_config = self.subparsers.add_parser("config")
        # -------------------------------- config  menu --------------------------
        subparsers_config = parser_config.add_subparsers(
            description="buildtest configuration"
        )
        parser_config_view = subparsers_config.add_parser(
            "view", help="View Buildtest Configuration File"
        )
        parser_config_edit = subparsers_config.add_parser(
            "edit", help="Edit Buildtest Configuration File"
        )
        parser_config_restore = subparsers_config.add_parser(
            "restore", help="Restore Buildtest Configuration File from backup"
        )

        parser_config_view.set_defaults(func=func_config_view)
        parser_config_edit.set_defaults(func=func_config_edit)
        parser_config_restore.set_defaults(func=func_config_restore)

    def show_menu(self):
        """This method adds argparse argument for ``buildtest show``"""

        # -------------------------- buildtest show options ------------------------------
        parser_show = self.subparsers.add_parser("show")
        parser_show.add_argument(
            "-c",
            "--config",
            help="show buildtest global configuration",
            action="store_true",
        )
        parser_show.set_defaults(func=func_show_subcmd)

        # -------------------------- buildtest show schemas ------------------------------
        subparsers_show = parser_show.add_subparsers(
            description="buildtest configuration"
        )
        parser_schema = subparsers_show.add_parser(
            "schema", help="Display test config schema"
        )
        parser_schema.add_argument(
            "-v", "--version", help="choose a specific version of schema to show.",
        )
        parser_schema.add_argument(
            "-n", "--name", help="show schema by name (e.g., script)",
        )
        parser_schema.set_defaults(func=show_schema_layout)
