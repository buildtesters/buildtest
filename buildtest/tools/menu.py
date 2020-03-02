"""
buildtest menu
"""

import argparse
import argcomplete

from buildtest.tools.config import config_opts
from buildtest.tools.build import func_build_subcmd
from buildtest.tools.get import func_get_subcmd
from buildtest.tools.configuration.config import (
    func_config_edit,
    func_config_view,
    func_config_restore,
)

from buildtest.tools.show import func_show_subcmd, show_schema_layout
from buildtest.tools.buildsystem.status import show_status_report

from buildtest.tools.system import get_module_collection
from buildtest.tools.testconfigs import (
    func_testconfigs_show,
    testconfig_choices,
    func_testconfigs_view,
    func_testconfigs_edit,
)

test_config_choice = testconfig_choices()
module_collection = get_module_collection()

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
            "module": "Buildtest Module Utilities",
            "show": "Options for displaying buildtest configuration",
            "testconfigs": "Options for list, view, and edit test configuration",
            "config": "Buildtest Configuration Menu",
        }

        self.main_menu()
        self.build_menu()
        self.get_menu()
        self.config_menu()
        self.show_menu()
        self.testconfigs_menu()

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

        argcomplete.autocomplete(self.parser)
        args = self.parser.parse_args()

        if args.subcommands:
            args.func(args)

        return args

    def build_menu(self):
        """This method implements argparse argument for ``buildtest build``"""

        parser_build = self.subparsers.add_parser("build")
        subparsers_build = parser_build.add_subparsers(
            description="Report status on builds performed by buildtest."
        )
        ##################### buildtest build report ###########################
        parser_build_report = subparsers_build.add_parser(
            "report", help="Report status details of all builds "
        )

        ##################### buildtest build     ###########################
        parser_build.add_argument(
            "--clear",
            help="Clear build history and remove all tests",
            action="store_true",
        )

        parser_build.add_argument(
            "-c",
            "--config",
            help="Specify test configuration",
            choices=test_config_choice,
            metavar="TEST CONFIGURATION",
        )

        parser_build.add_argument(
            "-d",
            "--dry",
            help="dry-run mode, buildtest will not write the test scripts but print "
            "content of test that would be written",
            action="store_true",
        )

        parser_build_mutex_modules = parser_build.add_mutually_exclusive_group()
        parser_build_mutex_modules.add_argument(
            "-co",
            "--collection",
            help="Use user Lmod module " "collection when building " "test",
            choices=module_collection,
            metavar="Lmod Collection Name",
        )
        parser_build_mutex_modules.add_argument(
            "-mc",
            "--module-collection",
            help="Use internal buildtest " "module collection when " "building test.",
            type=int,
            metavar="COLLECTION-ID",
        )

        parser_build_report.set_defaults(func=show_status_report)
        parser_build.set_defaults(func=func_build_subcmd)

    def get_menu(self):
        """This method implements argparse argument for ``buildtest get``"""

        parser_get = self.subparsers.add_parser("get")

        ##################### buildtest get       ###########################
        parser_get.add_argument(
            "repo", help="specify github.com or other repository to clone."
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

        parser_show = self.subparsers.add_parser("show")
        # -------------------------- buildtest show options ------------------------------
        parser_show.add_argument(
            "-c",
            "--config",
            help="show buildtest environment configuration",
            action="store_true",
        )
        subparsers_show = parser_show.add_subparsers(
            description="buildtest configuration"
        )
        parser_schema = subparsers_show.add_parser("schema", help="Display YAML schema")
        parser_schema.set_defaults(func=show_schema_layout)
        parser_show.set_defaults(func=func_show_subcmd)

    def testconfigs_menu(self):
        """This method adds argparse argument for ``buildtest testconfigs``"""

        test_config_choice = testconfig_choices()

        parser_testconfigs = self.subparsers.add_parser("testconfigs")

        # -------------------------------- buildtest testconfigs options ----------------------
        subparsers_testconfigs = parser_testconfigs.add_subparsers(
            description="Test configuration options"
        )
        parser_testconfigs_list = subparsers_testconfigs.add_parser(
            "list", help="List all test configuration"
        )
        parser_testconfigs_view = subparsers_testconfigs.add_parser(
            "view", help="View a test configuration"
        )
        parser_testconfigs_view.add_argument(
            "name",
            help="Select name of test configuration",
            choices=test_config_choice,
            metavar="Test Configuration",
        )
        parser_testconfigs_edit = subparsers_testconfigs.add_parser(
            "edit", help="Edit a test configuration "
        )
        parser_testconfigs_edit.add_argument(
            "name",
            help="Select name of test configuration",
            choices=test_config_choice,
            metavar="Test Configuration",
        )

        parser_testconfigs_list.set_defaults(func=func_testconfigs_show)
        parser_testconfigs_view.set_defaults(func=func_testconfigs_view)
        parser_testconfigs_edit.set_defaults(func=func_testconfigs_edit)
