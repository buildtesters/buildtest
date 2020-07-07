"""
buildtest menu: include functions to build, get test configurations, and 
interact with a global configuration for buildtest.
"""

import argparse

from buildtest import BUILDTEST_VERSION
from buildtest.defaults import supported_schemas
from buildtest.menu.buildspec import (
    func_buildspec_find,
    func_buildspec_view,
    func_buildspec_edit,
)
from buildtest.menu.config import (
    func_config_edit,
    func_config_view,
    func_config_reset,
    func_config_validate,
)
from buildtest.menu.repo import (
    func_repo_add,
    func_repo_list,
    func_repo_remove,
    active_repos,
    func_repo_update,
)
from buildtest.menu.report import func_report
from buildtest.menu.schema import func_schema


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
            "repo": "Options for managing buildtest repositories",
            "config": "Buildtest Configuration Menu",
        }

        self.main_menu()
        self.build_menu()
        self.buildspec_menu()
        self.report_menu()
        self.schema_menu()
        self.repo_menu()
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

           # reset buildtest settings to default file

           ``buildtest config reset``
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
        parser_config_restore = subparsers_config.add_parser(
            "reset", help="Reset buildtest configuration file. "
        )
        parser_config_validate = subparsers_config.add_parser(
            "validate", help="Validate buildtest settings file with schema."
        )

        parser_config_view.set_defaults(func=func_config_view)
        parser_config_edit.set_defaults(func=func_config_edit)
        parser_config_restore.set_defaults(func=func_config_reset)
        parser_config_validate.set_defaults(func=func_config_validate)

    def report_menu(self):
        """This method implements the ``buildtest report`` command options"""

        parser_report = self.subparsers.add_parser("report")

        ##################### buildtest report   ###########################

        parser_report.set_defaults(func=func_report)

    def repo_menu(self):
        """ This method implements ``buildtest repo``

            Command Usage

            # add test repository to buildtest, this will clone repository locally and update repository cache

           ``buildtest repo add <url>``

            # add test repository with specific branch

           ``buildtest repo add -b <branch> <url>``

           # remove a repository from buildtest repository cache. This will remove the repository from filesystem

           ``buildtest repo rm <repo>``

           # list all repository in buildtest repository cache

           ``buildtest repo list``

           # show content of repository cache

           ``buildtest repo list -s``

           # enable/disable repository state

           ``buildtest repo update --state <STATE> <repo>``

        """

        parser_repo = self.subparsers.add_parser("repo")

        ##################### buildtest repo  ###########################

        subparser_repo = parser_repo.add_subparsers(
            title="commands", description="repository commands"
        )
        parser_repo_add = subparser_repo.add_parser(
            "add", help="Add repository to buildtest."
        )
        parser_repo_list = subparser_repo.add_parser(
            "list", help="List all repositories in buildtest"
        )
        parser_repo_rm = subparser_repo.add_parser(
            "rm", help="Remove repository from buildtest"
        )

        parser_repo_update = subparser_repo.add_parser(
            "update", help="Update repository configuration"
        )
        parser_repo_update.add_argument(
            "repo", help="select repository to update", choices=active_repos()
        )
        parser_repo_update.add_argument(
            "--state",
            help="update state of repository. If you want "
            "buildtest to add repository to buildspec search path, set state "
            "to 'enabled' if you want buildtest to disable repo set state to "
            "'disabled'. buildtest will not add repository to buildspec search path.",
            choices=["enabled", "disabled"],
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
        parser_repo_update.set_defaults(func=func_repo_update)



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
            "-e", "--example", action="store_true", help="Show schema examples"
        )
        parser_schema.add_argument(
            "-j", "--json", action="store_true", help="View schema json content"
        )

        parser_schema.set_defaults(func=func_schema)

