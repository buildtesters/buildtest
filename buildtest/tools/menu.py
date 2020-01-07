"""
buildtest menu
"""


import argparse
import argcomplete

from buildtest.tools.build import func_build_subcmd
from buildtest.tools.config import (
    config_opts,
    check_configuration,
    func_config_edit,
    func_config_view,
    func_config_restore,
)
from buildtest.tools.modulesystem.collection import (
    func_collection_subcmd,
    get_collection_length,
)
from buildtest.tools.lsf import func_bsub
from buildtest.tools.modules import (
    func_module_subcmd,
    module_obj,
    module_load_test,
    get_all_parents,
    get_module_permutation_choices,
    list_modules
)
from buildtest.tools.modulesystem.tree import func_module_tree_subcmd

from buildtest.tools.show import func_show_subcmd
from buildtest.tools.buildsystem.status import (
    show_status_report,
    get_build_ids,
    show_status_log,
    show_status_test,
    run_tests,
)

from buildtest.tools.system import get_module_collection
from buildtest.tools.testconfigs import (
    func_testconfigs_show,
    testconfig_choices,
    func_testconfigs_view,
    func_testconfigs_edit,
    func_testconfigs_maintainer,
)
from buildtest.benchmark.benchmark import func_benchmark_osu_subcmd
from buildtest.tools.sysconfig.configuration import func_system_view, func_system_fetch

class BuildTestParser():
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
            "benchmark": "Run Benchmark",
            "system": "System Configuration"
        }

        self.main_menu()
        self.build_menu()
        self.module_menu()
        self.config_menu()
        self.show_menu()
        self.testconfigs_menu()
        self.system_menu()
        self.benchmark_menu()

    def main_menu(self):
        command_description = ""
        for k,v in self.subparser_dict.items():
            command_description += f"""\n      {k}           {v}"""


        self.subparsers = self.parser.add_subparsers(title="COMMANDS",description=command_description, dest="subcommands")

        self.parser.add_argument(
            "-V",
            "--version",
            action="version",
            version=f"""buildtest version {config_opts["BUILDTEST_VERSION"]}""",
        )

    def get_parser(self):
        return self.parser
    def parse_options(self):
        argcomplete.autocomplete(self.parser)
        args = self.parser.parse_args()

        if args.subcommands:
            args.func(args)

        return args
    def build_menu(self):
        """

        :return:
        """

        test_config_choice = testconfig_choices()
        module_collection = get_module_collection()
        module_permutation_choices = get_module_permutation_choices()
        collection_len = get_collection_length()
        collection_len = list(range(collection_len))
        build_ids = get_build_ids()

        parser_build = self.subparsers.add_parser("build")
        subparsers_build = parser_build.add_subparsers(
            description="Report status on builds performed by buildtest."
        )
        ##################### buildtest build report ###########################
        parser_build_report = subparsers_build.add_parser(
            "report", help="Report status details of all builds "
        )
        ##################### buildtest build log ###########################
        parser_build_log = subparsers_build.add_parser(
            "log", help="Report build log for a particular build"
        )
        parser_build_log.add_argument(
            "id",
            help="Display Log File for a build ID",
            type=int,
            choices=build_ids,
            metavar="BUILD ID",
        )
        ##################### buildtest build test ###########################
        parser_build_test = subparsers_build.add_parser(
            "test", help="Report test scripts based on build ID"
        )
        parser_build_test.add_argument(
            "id",
            help="Display test scripts based on build ID",
            type=int,
            choices=build_ids,
            metavar="BUILD ID",
        )
        ##################### buildtest build run ###########################
        parser_build_run = subparsers_build.add_parser(
            "run", help="Run test scripts based on build ID"
        )
        parser_build_run.add_argument(
            "id",
            help="Run test scripts based on build ID",
            type=int,
            choices=build_ids,
            metavar="BUILD ID",
        )
        ##################### buildtest build bsub ###########################
        parser_build_bsub = subparsers_build.add_parser(
            "bsub", help="LSF Batch Job Launcher (bsub)"
        )
        parser_build_bsub.add_argument(
            "id",
            help="Dispatch test based on build ID",
            type=int,
            choices=build_ids,
            metavar="BUILD ID",
        )
        parser_build_bsub.add_argument(
            "-q", "--queue", help="select queue (bsub -q)", type=str
        )
        parser_build_bsub.add_argument(
            "-R", "--resource", help="Resource Selection (bsub -R)", type=str
        )
        parser_build_bsub.add_argument(
            "-n",
            "--ntasks",
            help="Submits a parallel job and specifies number of tasks in job (bsub -n)",
            type=str,
        )
        parser_build_bsub.add_argument(
            "-m", "--machine", help="Submit job to specific hosts (bsub -m)", type=str
        )
        parser_build_bsub.add_argument(
            "-W", "--walltime", help="Wall Time of Job (bsub -W)", type=str
        )
        parser_build_bsub.add_argument(
            "-M",
            "--memory",
            help="Sets per-process (soft) memory for all process in job (bsub -M)",
            type=str,
        )
        parser_build_bsub.add_argument(
            "-J", "--jobname", help="Assign a Job Name (bsub -J)", type=str
        )

        parser_build_bsub.add_argument(
            "--dry-run",
            help="Preview bsub command and not submit job to scheduler",
            action="store_true",
        )

        ##################### buildtest build     ###########################
        parser_build.add_argument(
            "--clear", help="Clear build history and remove all tests", action="store_true"
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
        parser_build.add_argument(
            "-v",
            "--verbose",
            help="verbosity level (default: %(default)s)",
            action="count",
            default=0,
        )

        parser_build_mutex_modules = parser_build.add_mutually_exclusive_group()
        parser_build_mutex_modules.add_argument(
            "-m",
            "--modules",
            help="Select a module name and " "build for every module " "version",
            choices=module_permutation_choices,
            metavar="Module Permutation Options",
        )
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
            choices=collection_len,
            metavar="COLLECTION-ID",
        )


        parser_build_bsub.set_defaults(func=func_bsub)
        parser_build_run.set_defaults(func=run_tests)
        parser_build_test.set_defaults(func=show_status_test)
        parser_build_report.set_defaults(func=show_status_report)
        parser_build_log.set_defaults(func=show_status_log)
        parser_build.set_defaults(func=func_build_subcmd)
    def module_menu(self):

        parent_choices = get_all_parents()
        collection_len = get_collection_length()
        collection_len = list(range(collection_len))

        parser_module = self.subparsers.add_parser("module")
        subparsers_module = parser_module.add_subparsers(
            description="Module utilties for managing module collections,"
                        " module trees, module load testing, reporting eb/spack modules,"
                        "and report difference between trees."
        )
        parser_module_list = subparsers_module.add_parser(
            "list", help="module list operation"
        )
        parser_moduleload = subparsers_module.add_parser(
            "loadtest", help="module load test"
        )
        parser_module_tree = subparsers_module.add_parser(
            "tree", help="module tree " "operation"
        )
        parser_collection = subparsers_module.add_parser(
            "collection", help="module collection " "operation"
        )

        # ------------------------- buildtest module loadtest options -------------------------------
        parser_moduleload.add_argument("--login", help="Run test in a login shell", action="store_true")
        parser_moduleload.add_argument("--numtest", help="Number of tests to run before exiting", type=int)
        parser_moduleload.add_argument("--purge-modules", help="purge modules before loading modules.",
                                       action="store_true")

        # ------------------------- buildtest module list options ----------------------------------
        parser_module_list.add_argument("--exclude-version-files",
                                        help="Exclude version files from search when reporting module list",
                                        action="store_true")
        parser_module_list.add_argument("--filter-include",
                                        help="Filter output by including only modules of interest.", type=str,
                                        nargs='+', default=None)
        parser_module_list.add_argument("--querylimit",
                                        help="Limit query of modules during module list", type=int)

        # ------------------------- buildtest module collection options -----------------------------
        parser_collection.add_argument(
            "-l", "--list", action="store_true", help="List all Module Collection"
        )
        parser_collection.add_argument(
            "-a", "--add", action="store_true", help="Add a Module Collection"
        )
        parser_collection.add_argument(
            "-u",
            "--update",
            type=int,
            choices=collection_len,
            metavar="Update a Module Collection Index",
            help="Update a Module Collection Index",
        )
        parser_collection.add_argument(
            "-r",
            "--remove",
            type=int,
            choices=collection_len,
            metavar="Module Collection Index",
            help="Remove a Module Collection",
        )
        parser_collection.add_argument(
            "-c", "--clear", help="remove all module collections", action="store_true"
        )
        parser_collection.add_argument(
            "--check",
            help="Check all module collection by performing module load test.",
            action="store_true",
        )

        # ------------------------- buildtest module tree  options --------------------------------
        parser_module_tree.add_argument(
            "-a",
            help="add a module tree",
            dest="add",
            action="append",
            metavar="Module Tree",
        )

        parser_module_tree.add_argument(
            "-l", help="list module trees", action="store_true", dest="list"
        )

        parser_module_tree.add_argument(
            "-r",
            help="remove a module tree",
            choices=config_opts["BUILDTEST_MODULEPATH"],
            action="append",
            dest="rm",
            metavar="Module Tree",
        )
        parser_module_tree.add_argument(
            "-s", help="Assign a module tree to BUILDTEST_MODULEPATH", dest="set"
        )

        # -------------------------------- buildtest module  options --------------------------------

        parser_module.add_argument(
            "--diff-trees", help="Show difference between two module trees"
        )

        parser_module.add_argument(
            "-eb",
            "--easybuild",
            help="reports modules that are built by easybuild",
            action="store_true",
        )
        parser_module.add_argument(
            "--spack", help="reports modules that are built by spack", action="store_true"
        )
        parser_module.add_argument(
            "-d",
            "--module-deps",
            help="retrieve all modules that module is " "depended on",
            choices=parent_choices,
            metavar="AVAILABLE-MODULES",
        )

        parser_module.add_argument(
            "-s",
            "--software",
            help="get unique software from Lmod spider command",
            action="store_true",
        )

        parser_moduleload.set_defaults(func=module_load_test)
        parser_module_list.set_defaults(func=list_modules)
        parser_module_tree.set_defaults(func=func_module_tree_subcmd)
        parser_collection.set_defaults(func=func_collection_subcmd)
        parser_module.set_defaults(func=func_module_subcmd)
    def config_menu(self):

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
        parser_show = self.subparsers.add_parser("show")
        # -------------------------- buildtest show options ------------------------------
        parser_show.add_argument(
            "-c",
            "--config",
            help="show buildtest environment configuration",
            action="store_true",
        )
        parser_show.add_argument(
            "-k", "--keys", help="show yaml keys", choices=["singlesource"]
        )

        parser_show.set_defaults(func=func_show_subcmd)
    def testconfigs_menu(self):

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
        parser_testconfigs_maintainer = subparsers_testconfigs.add_parser(
            "maintainer", help="Add/Remove maintainer from test configuration"
        )
        parser_testconfigs_maintainer.add_argument(
            "name",
            help="Select name of test configuration",
            choices=test_config_choice,
            metavar="Test Configuration",
        )
        parser_testconfigs_maintainer.add_argument(
            "-m",
            "--maintainer",
            help="Add/Remove yourself as maintainer from test configuration",
            choices=["yes", "no"],
        )

        parser_testconfigs_list.set_defaults(func=func_testconfigs_show)
        parser_testconfigs_view.set_defaults(func=func_testconfigs_view)
        parser_testconfigs_edit.set_defaults(func=func_testconfigs_edit)
        parser_testconfigs_maintainer.set_defaults(func=func_testconfigs_maintainer)
    def system_menu(self):

        parser_system = self.subparsers.add_parser("system")
        # -------------------------------- buildtest system options --------------------------
        subparsers_system = parser_system.add_subparsers(description="system configuration")
        parser_system_view = subparsers_system.add_parser(
            "view", help="View System Configuration"
        )
        parser_system_fetch = subparsers_system.add_parser(
            "fetch", help="Fetch System Information"
        )

        parser_system_view.set_defaults(func=func_system_view)
        parser_system_fetch.set_defaults(func=func_system_fetch)
    def benchmark_menu(self):

        parser_benchmark = self.subparsers.add_parser("benchmark")
        subparsers_benchmark = parser_benchmark.add_subparsers(dest="Run HPC Benchmark")

        # -------------------------------- buildtest benchmark osu options --------------------------
        osu_parser = subparsers_benchmark.add_parser("osu", help="Run OSU MicroBenchmark ")
        osu_parser.add_argument("-r", "--run", help="Run Benchmark", action="store_true")
        osu_parser.add_argument(
            "-i", "--info", help="show yaml key description", action="store_true"
        )
        osu_parser.add_argument(
            "-l",
            "--list",
            help="List of tests available for OSU Benchmark",
            action="store_true",
        )
        osu_parser.add_argument("-c", "--config", help="OSU Yaml Configuration File")
        osu_parser.set_defaults(func=func_benchmark_osu_subcmd)
