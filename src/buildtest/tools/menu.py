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
)
from buildtest.tools.modulesystem.tree import func_module_tree_subcmd

from buildtest.tools.options import override_configuration
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


def menu():
    """The method implements the buildtest menu using argparse library.
    """

    override_configuration()
    check_configuration()

    test_config_choice = testconfig_choices()

    parent_choices = get_all_parents()

    module_collection = get_module_collection()
    module_permutation_choices = get_module_permutation_choices()
    collection_len = get_collection_length()
    collection_len = list(range(collection_len))
    build_ids = get_build_ids()
    epilog_str = (
        "Documentation: " + "https://buildtest.readthedocs.io/en/latest/index.html"
    )
    description_str = (
        "buildtest is a software testing framework designed "
        + "for HPC facilities to verify their Software Stack. buildtest "
        + "abstracts test complexity into YAML files that is interpreted"
        + "by buildtest into shell script"
    )

    parser = argparse.ArgumentParser(
        prog="buildtest",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=description_str,
        usage="%(prog)s [options] [COMMANDS]",
        epilog=epilog_str,
    )

    show_title = "Options for displaying buildtest configuration"
    testconfig_title = "Options for list, view, and edit test configuration"
    build_title = "Options for building test scripts"
    benchmark_title = "Run Benchmark"
    module_title = "Module Operations including module load testing, module collections, module tree, easybuild/spack modules, parent-modules. "
    system_title = "System Configuration"
    config_title = "Buildtest Configuration"
    command_description = f"""
  
  show        {show_title}  
  testconfigs {testconfig_title}         
  build       {build_title}  
  benchmark   {benchmark_title}
  module      {module_title}
  system      {system_title}
  config      {config_title}
"""
    subparsers = parser.add_subparsers(
        title="COMMANDS", description=command_description, dest="subcommands"
    )

    # ---------------------------------- sub parsers -----------------------
    parser_list = subparsers.add_parser("list")
    parser_build = subparsers.add_parser("build")
    parser_show = subparsers.add_parser("show")
    parser_benchmark = subparsers.add_parser("benchmark")
    parser_testconfigs = subparsers.add_parser("testconfigs")
    parser_module = subparsers.add_parser("module")
    parser_system = subparsers.add_parser("system")
    parser_config = subparsers.add_parser("config")

    subparsers_module = parser_module.add_subparsers(
        description="Module utilties for managing module collections,"
        " module trees, module load testing, reporting eb/spack modules,"
        "and report difference between trees."
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

    # -------------------------------- build menu --------------------------
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

    subparsers_build = parser_build.add_subparsers(
        description="Report status on builds performed by buildtest."
    )
    parser_build_report = subparsers_build.add_parser(
        "report", help="Report status details of all builds "
    )

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
    parser_build_bsub.set_defaults(func=func_bsub)
    parser_build_run.set_defaults(func=run_tests)
    parser_build_test.set_defaults(func=show_status_test)
    parser_build_report.set_defaults(func=show_status_report)
    parser_build_log.set_defaults(func=show_status_log)

    parser_build.set_defaults(func=func_build_subcmd)

    # -------------------------------- system menu --------------------------
    subparsers_system = parser_system.add_subparsers(description="system configuration")
    parser_system_view = subparsers_system.add_parser(
        "view", help="View System Configuration"
    )
    parser_system_fetch = subparsers_system.add_parser(
        "fetch", help="Fetch System Information"
    )

    parser_system_view.set_defaults(func=func_system_view)
    parser_system_fetch.set_defaults(func=func_system_fetch)

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
    # -------------------------------- module menu --------------------------

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

    parser_module.add_argument(
        "-l",
        "--list",
        help="get full module name and path to module files",
        action="store_true",
    )
    parser_module.add_argument(
        "-ec",
        "--easyconfigs",
        help="Return a list of easyconfigs from a module tree",
        action="store_true",
    )


    # ------------------------- module tree  options ------------
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

    # ------------------------- module collection options ------------
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
    parser_moduleload.set_defaults(func=module_load_test)
    parser_module_tree.set_defaults(func=func_module_tree_subcmd)
    parser_collection.set_defaults(func=func_collection_subcmd)
    parser_module.set_defaults(func=func_module_subcmd)

    # -------------------------------- show menu --------------------------

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

    # -------------------------------- testconfigs menu ----------------------
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
    # -------------------------------- benchmark menu ----------------------

    subparsers_benchmark = parser_benchmark.add_subparsers(dest="Run HPC Benchmark")

    # -------------------------------- osu  menu ---------------------------
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

    # ------------------------------ Miscellaneous Options -----------------------
    misc_group = parser.add_argument_group("Miscellaneous Options ")

    misc_group.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"""buildtest version {config_opts["BUILDTEST_VERSION"]}""",
    )

    return parser


def parse_options(parser):
    """Return parsed arguments and apply argument completion to make use of
    argcomplete library.

    :param parser: parser object is an instance of argparse.ArgumentParser()
    :type parser: dict, required
    """
    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    if args.subcommands:
        args.func(args)
