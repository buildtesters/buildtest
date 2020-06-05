"""
buildtest menu: include functions to build, get test configurations, and 
interact with a global configuration for buildtest.
"""

import argparse

from buildtest import BUILDTEST_VERSION
from buildtest.defaults import supported_schemas
from buildtest.menu.repo import func_repo_add, func_repo_list, func_repo_remove
from buildtest.menu.config import (
    func_config_edit,
    func_config_view,
    func_config_reset,
)
from buildtest.menu.show import show_schema_layout


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
        self.repo_menu()
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
            version=f"""buildtest version {BUILDTEST_VERSION}""",
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
        """This method implements argparse argument for ``buildtest build``"""

        parser_build = self.subparsers.add_parser("build")

        ##################### buildtest build     ###########################

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
            "-e",
            "--executor",
            help='specify a named executor to use (defaults to "default" key, first in list, then local (base) executor',
        )

        parser_build.add_argument(
            "-d",
            "--dry",
            help="dry-run mode, buildtest will not write the test scripts but print "
            "content of test-script that would be written",
            action="store_true",
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

    def repo_menu(self):
        """This method implements argparse argument for ``buildtest repo``"""

        parser_repo = self.subparsers.add_parser("repo")

        ##################### buildtest repo       ###########################

        subparser_repo = parser_repo.add_subparsers(
            title="commands", description="repository commands"
        )
        parser_repo_add = subparser_repo.add_parser(
            "add", help="Add repository to buildtest."
        )
        parser_repo_list = subparser_repo.add_parser(
            "list", help="List all repositories active in buildtest"
        )
        parser_repo_rm = subparser_repo.add_parser(
            "rm", help="Remove repository from buildtest"
        )

        parser_repo_add.add_argument(
            "-b",
            "--branch",
            help="Clone a particular branch (defaults to master)",
            default="master",
        )
        parser_repo_add.add_argument("repo", help="repository to clone into buildtest")
        parser_repo_list.add_argument(
            "-s", "--show", action="store_true", help="show repository details"
        )

        parser_repo_rm.add_argument("repo", help="repository to remove from buildtest")

        parser_repo_add.set_defaults(func=func_repo_add)
        parser_repo_list.set_defaults(func=func_repo_list)
        parser_repo_rm.set_defaults(func=func_repo_remove)

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
            "reset", help="Reset buildtest configuration file. "
        )

        parser_config_view.set_defaults(func=func_config_view)
        parser_config_edit.set_defaults(func=func_config_edit)
        parser_config_restore.set_defaults(func=func_config_reset)

    def show_menu(self):
        """This method adds argparse argument for ``buildtest show``"""

        # -------------------------- buildtest show options ------------------------------
        parser_show = self.subparsers.add_parser("show")

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
            "-n",
            "--name",
            help="show schema by name (e.g., script)",
            choices=supported_schemas,
        )
        parser_schema.add_argument(
            "-g",
            "--global",
            dest="_global",
            help="show global schema",
            action="store_true",
        )
        parser_schema.add_argument(
            "-s", "--settings", help="show settings schema", action="store_true",
        )
        parser_schema.set_defaults(func=show_schema_layout)
