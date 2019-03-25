############################################################################
#
#  Copyright 2017-2019
#
#   https://github.com/HPC-buildtest/buildtest-framework
#
#  This file is part of buildtest.
#
#    buildtest is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    buildtest is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with buildtest.  If not, see <http://www.gnu.org/licenses/>.
#############################################################################

"""
buildtest menu
"""

import os
import argparse
import argcomplete

from buildtest.test.run.system import run_app_choices, run_system_choices
from buildtest.tools.build import func_build_subcmd
from buildtest.tools.config import BUILDTEST_SHELLTYPES, config_opts, \
    check_configuration
from buildtest.tools.file import create_dir, walk_tree
from buildtest.tools.find import func_find_subcmd
from buildtest.tools.list import func_list_subcmd
from buildtest.tools.modules import func_module_subcmd
from buildtest.tools.options import override_configuration
from buildtest.tools.run import func_run_subcmd
from buildtest.tools.show import func_show_subcmd
from buildtest.tools.system import systempackage_installed_list
from buildtest.tools.software import get_software_stack
from buildtest.tools.yaml import func_yaml_subcmd
from buildtest.benchmark.benchmark import func_benchmark_osu_subcmd
from buildtest.benchmark.hpl import func_benchmark_hpl_subcmd
from buildtest.benchmark.hpcg import func_benchmark_hpcg_subcmd

def menu():
    """ buildtest menu"""

    override_configuration()
    check_configuration()

    test_suite_dir = os.path.join(config_opts["BUILDTEST_TESTDIR"], "suite")
    create_dir(test_suite_dir)

    test_class = os.listdir(os.path.join(config_opts["BUILDTEST_CONFIGS_REPO"],
                                         "buildtest",
                                         "suite"))
    yaml_choices = walk_tree(os.path.join(config_opts["BUILDTEST_CONFIGS_REPO"],
                                          "buildtest",
                                          "suite"),".yml")


    run_test_class = os.listdir(test_suite_dir)
    pkglist = systempackage_installed_list()
    software_list = get_software_stack()

    app_choices = run_app_choices()

    systempkg_choices = run_system_choices()
    epilog_str = "Documentation: " + \
                 "https://buildtest.readthedocs.io/en/latest/index.html"
    description_str = "buildtest is a software testing framework designed " + \
        "for HPC facilities to verify their Software Stack. buildtest " + \
        "abstracts test complexity into YAML files that is interpreted" + \
        "by buildtest into shell script"


    parser = argparse.ArgumentParser(prog='buildtest',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=description_str,
                                     epilog=epilog_str)


    list_title = "Options for listing software, module files, and  easyconfigs"
    show_title = "Options for displaying buildtest configuration"
    find_title = "Find configuration files and test scripts"
    build_title = "Options for building test scripts"
    run_title = "Run Tests"
    benchmark_title = "Run Benchmark"
    yaml_title = "Yaml commands for buildtest"
    module_title = "Options for module load testing and report diff between module trees"
    command_description = f"""
Info:
    list        {list_title}
    show        {show_title}
    find        {find_title}
           
    
Build:
    build       {build_title}
    run         {run_title}
    benchmark   {benchmark_title}

Misc:
    yaml        {yaml_title}
    module      {module_title}
    """
    subparsers = parser.add_subparsers(title='commands', description=command_description,dest="subcommand")

    # ---------------------------------- sub parsers -----------------------
    parser_list = subparsers.add_parser('list')
    parser_find = subparsers.add_parser('find')
    parser_yaml = subparsers.add_parser('yaml')
    parser_build = subparsers.add_parser('build')
    parser_run = subparsers.add_parser('run')
    parser_module = subparsers.add_parser('module')
    parser_show = subparsers.add_parser('show')
    parser_benchmark = subparsers.add_parser('benchmark')


    # -------------------------------- list menu --------------------------


    parser_list.add_argument("-ls",
                             "--list-unique-software",
                             help="retrieve all unique software found in your "
                                  + "module tree specified by "
                                  + "BUILDTEST_MODULE_ROOT",
                             action="store_true")

    parser_list.add_argument("-svr",
                             "--software-version-relation",
                             help="retrieve software and path to module files "
                                  + "grouped by software alphabetically",
                             action="store_true")
    parser_list.add_argument("-ec",
                             "--easyconfigs",
                             help="Return a list of easyconfigs from a "
                                  + "module tree",
                             action="store_true")
    parser_list.add_argument("--format",
                             help="Output format type",
                             choices=["json"])
    parser_list.set_defaults(func=func_list_subcmd)

    # -------------------------------- find menu ---------------------------

    parser_find.add_argument("-fc",
                             "--findconfig",
                             help="Find buildtest YAML "
                                  + "config files. To find all yaml files use"
                                    " -fc all")

    parser_find.add_argument("-ft",
                             "--findtest",
                             help="Find generated test scripts. To find all "
                                  + "testscripts use -ft all")
    parser_find.set_defaults(func=func_find_subcmd)


    # -------------------------------- yaml  menu --------------------------

    parser_yaml.add_argument("--ohpc",
                             help="Build YAML configuration for OpenHPC "
                                  + "package. YAML files will be written in "
                                  + "$BUILDTEST_CONFIGS_REPO/ohpc",
                             action="store_true")
    parser_yaml.add_argument("-m", "--maintainer",
                             help="Add as maintainer to test",
                             choices=["yes", "no"]),
    parser_yaml.add_argument("config",
                             help="Select the Yaml Configuration",
                             choices=yaml_choices,
                             metavar="YAML CONFIGURATION LIST")

    parser_yaml_use_subparser = parser_yaml.add_subparsers(
        help='Load a Test Scope')


    parser_yaml_use = parser_yaml_use_subparser.add_parser('load',
                                                 help="Load a Test Scope")
    parser_yaml_use.add_argument("config",
                                 choices=yaml_choices,
                                 metavar="YAML")


    parser_yaml.set_defaults(func=func_yaml_subcmd)

    # -------------------------------- build menu --------------------------

    parser_build.add_argument("-s",
                              "--software",
                              help=" Specify software package to test",
                              choices=software_list,
                              metavar='INSTALLED-SOFTWARE')
    parser_build.add_argument("-p",
                              "--package",
                              help="Build test for system packages",
                              choices=pkglist,
                              metavar='SYSTEM-PACKAGE')
    parser_build.add_argument("--prepend-modules",
                              help="Prepend modules in test script prior to "
                                   +"loading application module.",
                              choices=software_list,
                              metavar='INSTALLED-SOFTWARE',
                              action="append",
                              default=[])
    parser_build.add_argument("--shell",
                              help=" Select the type of shell for testscript",
                              choices=BUILDTEST_SHELLTYPES)
    parser_build.add_argument("-b", "--binary",
                              help="Conduct binary test for a package",
                              action="store_true")
    parser_build.add_argument("-S",
                              "--suite",
                              help="specify test suite",
                              choices=test_class)
    parser_build.add_argument("--clean-tests",
                              help="delete test directory $BUILDTEST_TESTDIR",
                              action="store_true")
    parser_build.add_argument("--testdir",
                              help="Specify alternate test directory to write "
                                   + "test. This overrides configuration "
                                   + "BUILDTEST_TESTDIR")
    parser_build.add_argument("--clean-build",
                              help="delete software test directory before "
                                   + "writing test scripts",
                              action="store_true")
    parser_build.add_argument("-eb",
                              "--easybuild",
                              help="check if application is built by easybuild",
                              action="store_true")
    parser_build.add_argument("--ohpc",
                              help="Indicate to buildtest this is a OpenHPC "
                                   + "package. YAML files will be processed "
                                   + "from $BUILDTEST_CONFIGS_REPO/ohpc",
                              action="store_true")
    parser_build.add_argument("-v", "--verbose",
                              help="verbosity level",
                              action="count",
                              default=0)


    parser_build.set_defaults(func=func_build_subcmd)

    # -------------------------------- run menu ----------------------------

    parser_run.add_argument("-i",
                            "--interactive",
                            help="Run the test interactively",
                            action="store_true")
    parser_run.add_argument("-s",
                            "--software",
                            help="Run test suite for application",
                            choices=app_choices,
                            metavar='SOFTWARE-TEST-SUITE')
    parser_run.add_argument("-p",
                            "--package",
                            help="Run test suite for system package",
                            choices=systempkg_choices,
                            metavar='PACKAGE-TEST-SUITE')
    parser_run.add_argument("-S",
                            "--suite",
                            help="Run the test suite",
                            choices=run_test_class)
    parser_run.add_argument("-j",
                            "--job",
                            help = "Submit jobs to resource scheduler",
                            action="store_true")
    parser_run.set_defaults(func=func_run_subcmd)

    # -------------------------------- module menu --------------------------

    parser_module.add_argument("--module-load-test",
                               help="conduct module load test for all modules "
                                    + "defined in BUILDTEST_MODULE_ROOT",
                               action="store_true")
    parser_module.add_argument("--diff-trees",
                               help="Show difference between two module trees")
    parser_module.set_defaults(func=func_module_subcmd)

    # -------------------------------- show menu --------------------------


    parser_show.add_argument("-c","--config",
                             help="show buildtest environment configuration",
                             action="store_true")
    parser_show.add_argument("-k","--keys",
                             help="show yaml keys",
                             choices = ["singlesource"])
    parser_show.set_defaults(func=func_show_subcmd)

    # -------------------------------- benchmark menu ----------------------

    subparsers_benchmark = parser_benchmark.add_subparsers(help='subcommand help',
                                                           dest="benchmark_subcommand")

    # -------------------------------- osu  menu ---------------------------
    osu_parser = subparsers_benchmark.add_parser('osu',
                                                 help = "OSU MicroBenchmark sub menu")
    osu_parser.add_argument("-r",
                            "--run",
                            help ="Run Benchmark",
                            action="store_true")
    osu_parser.add_argument("-i",
                            "--info",
                            help="show yaml key description",
                            action="store_true")
    osu_parser.add_argument("-l",
                            "--list",
                            help="List of tests available for OSU Benchmark",
                            action="store_true")
    osu_parser.add_argument("-c",
                            "--config",
                            help="OSU Yaml Configuration File")
    osu_parser.set_defaults(func=func_benchmark_osu_subcmd)

    # -------------------------------- HPL  menu ---------------------------
    hpl_parser = subparsers_benchmark.add_parser('hpl',
                                                 help="High Performance "
                                                      + "Linpack sub menu")
    hpl_parser.set_defaults(func=func_benchmark_hpl_subcmd)

    # -------------------------------- HPCG  menu ---------------------------
    hpcg_parser = subparsers_benchmark.add_parser('hpcg',
                                                  help="High Performance "
                                                       + "Conjugate Gradient "
                                                       + "sub menu")
    hpcg_parser.set_defaults(func=func_benchmark_hpcg_subcmd)

    # ------------------------------ Miscellaneous Options -----------------------
    misc_group = parser.add_argument_group("Miscellaneous Options ")
    misc_group.add_argument("-V",
                            "--version",
                            help="show program version number and exit",
                            action="store_true")
    misc_group.add_argument("--logdir",
                            help="Path to write buildtest logs. Override "
                                 + "configuration BUILDTEST_LOGDIR")
    misc_group.add_argument("--clean-logs",
                            help="delete buildtest log directory $BUILDTEST_LOGDIR",
                            action="store_true")

    return parser

def parse_options(parser):
    """Return parsed arguments and apply argument completion to make use of
    argcomplete library."""
    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    if args.subcommand:
        args.func(args)
    return args
