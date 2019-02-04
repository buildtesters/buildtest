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

from buildtest.test.run.app import run_app_choices
from buildtest.test.run.system import run_system_choices
from buildtest.test.python import python_pkg_choices
from buildtest.test.r import r_pkg_choices
from buildtest.test.ruby import ruby_pkg_choices
from buildtest.test.perl import perl_pkg_choices
from buildtest.test.run.testname import test_list
from buildtest.benchmark.benchmark import func_benchmark_osu_subcmd
from buildtest.benchmark.hpl import func_benchmark_hpl_subcmd
from buildtest.benchmark.hpcg import func_benchmark_hpcg_subcmd
from buildtest.tools.build import func_build_subcmd
from buildtest.tools.config import BUILDTEST_SHELLTYPES, config_opts, check_configuration
from buildtest.tools.find import func_find_subcmd
from buildtest.tools.list import func_list_subcmd
from buildtest.tools.modules import func_module_subcmd
from buildtest.tools.options import override_configuration
from buildtest.tools.run import func_run_subcmd
from buildtest.tools.system import systempackage_installed_list
from buildtest.tools.software import get_software_stack, get_toolchain_stack
from buildtest.tools.yaml import func_yaml_subcmd


def menu():
    """ buildtest menu"""
    parser = {}
    override_configuration()
    check_configuration()

    #test_category = ["mpi"]
    pkglist = systempackage_installed_list()
    python_choices = python_pkg_choices()
    r_choices = r_pkg_choices()
    ruby_choices = ruby_pkg_choices()
    perl_choices = perl_pkg_choices()
    software_list = get_software_stack()
    toolchain_list = get_toolchain_stack()
    test_choices = test_list()
    app_choices = run_app_choices()
    systempkg_choices = run_system_choices()

    parser = argparse.ArgumentParser(prog='buildtest', usage='%(prog)s [options]')
    parser.add_argument("-V", "--version", help="show program version number and exit",action="store_true")
    parser.add_argument("--logdir", help="Path to write buildtest logs. Override configuration BUILDTEST_LOGDIR")
    parser.add_argument("--show", help="show buildtest environment configuration", action="store_true")
    parser.add_argument("--show-keys", help="display yaml key description", action="store_true")
    parser.add_argument("--scantest", help=""" Report all application that buildtest can be build.""", action="store_true")
    parser.add_argument("--clean-logs", help="delete buildtest log directory ($BUILDTEST_LOGDIR)",action="store_true")
    parser.add_argument("--submitjob", help = "specify a directory or job script to submit to resource scheduler")
    #parser.add_argument("-C", "--category", help="select test category for building tests", choices=self.test_category, metavar="TEST-CATEGORY")
    subparsers = parser.add_subparsers(help='subcommand help', dest="subcommand")
    # -------------------------------- list menu --------------------------
    parser_list = subparsers.add_parser('list', help='list help')
    parser_list.add_argument('-lt', "--list-toolchain", help="retrieve a list of easybuild toolchain used for --toolchain option", action="store_true")
    parser_list.add_argument("-ls", "--list-unique-software",help="retrieve all unique software found in your module tree specified by BUILDTEST_MODULE_ROOT", action="store_true")
    parser_list.add_argument("-svr", "--software-version-relation", help="retrieve a relationship between software and version found in module files", action="store_true")
    parser_list.add_argument("-ec","--easyconfigs", help="Return a list of easyconfigs from a easybuild module tree",action="store_true")
    parser_list.add_argument("--format", help="Output format type", choices=["json"])
    parser_list.set_defaults(func=func_list_subcmd)

    # -------------------------------- find menu ---------------------------
    parser_find = subparsers.add_parser('find', help='find configuration files and test')
    parser_find.add_argument("-fc","--findconfig", help= """ Find buildtest YAML config files found in BUILDTEST_CONFIGS_REPO.
                                         To find all yaml config files use -fc all """)
    parser_find.add_argument("-ft", "--findtest", help="""Find test scripts generated by buildtest defined by BUILDTEST_TESTDIR.
                                 To find all test scripts use -ft all """)
    parser_find.set_defaults(func=func_find_subcmd)

    # -------------------------------- yaml  menu --------------------------
    parser_yaml = subparsers.add_parser('yaml', help='Options for building YAML configuration')
    parser_yaml.add_argument("--ohpc", help="Indicate to buildtest this is a OpenHPC package. YAML files will be written in $BUILDTEST_CONFIGS_REPO/ohpc", action="store_true")
    parser_yaml.set_defaults(func=func_yaml_subcmd)

    # -------------------------------- build menu --------------------------
    parser_build = subparsers.add_parser('build', help='options for building tests')
    parser_build.add_argument("-s", "--software", help=" Specify software package to test", choices=software_list, metavar='INSTALLED-SOFTWARE')
    parser_build.add_argument("-t", "--toolchain",help=" Specify toolchain for the software package", choices=toolchain_list, metavar='INSTALLED-SOFTWARE-TOOLCHAINS')
    parser_build.add_argument("-p", "--package", help=" Build test for system packages", choices=pkglist, metavar='SYSTEM-PACKAGE')
    parser_build.add_argument("--prepend-modules", help= "Prepend modules in test script prior to loading application module. Use this option with Hierarchical Module Naming Scheme", choices=software_list,  metavar='INSTALLED-SOFTWARE',action="append", default=[])
    parser_build.add_argument("--all-package", help="build tests for all system packages from buildtest repository ", action="store_true")
    parser_build.add_argument("--all-software", help="build tests for all software from buildtest repository ", action="store_true")
    parser_build.add_argument("--shell", help=""" Select the type of shell when running test""", choices=BUILDTEST_SHELLTYPES)
    parser_build.add_argument("-b", "--binary", help="Conduct binary test for a package", action="store_true")
    parser_build.add_argument("--python-package", help="build test for Python packages", choices=python_choices,metavar='PYTHON-PACKAGES')
    parser_build.add_argument("--r-package", help="build test for R packages", choices=r_choices,metavar='R-PACKAGES')
    parser_build.add_argument("--ruby-package", help="build test for Ruby packages", choices=ruby_choices,metavar='RUBY-PACKAGES')
    parser_build.add_argument("--perl-package", help="build test for Perl packages", choices=perl_choices,metavar='PERL-PACKAGES')
    parser_build.add_argument("--clean-tests",help="delete testing directory ($BUILDTEST_TESTDIR)",action="store_true")
    parser_build.add_argument("--testdir", help="Path to write buildtest tests. Overrides configuration BUILDTEST_TESTDIR")
    parser_build.add_argument("--clean-build", help="delete software test directory before writing test scripts", action="store_true")
    parser_build.add_argument("-eb","--easybuild", help="check if application is built by easybuild",action="store_true")
    parser_build.add_argument("--enable-job", help="enable job script generation with buildtest", action="store_true")
    parser_build.add_argument("--job-template", help = "specify  job template file to create job submission script for the test to run with resource scheduler")
    parser_build.add_argument("-mns", "--module-naming-scheme", help="Specify module naming scheme for easybuild apps", choices=["HMNS","FNS"])
    parser_build.add_argument("--ohpc", help="Indicate to buildtest this is a OpenHPC package. YAML files will be processed from $BUILDTEST_CONFIGS_REPO/ohpc", action="store_true")
    parser_build.set_defaults(func=func_build_subcmd)

    # -------------------------------- run menu ----------------------------
    parser_run = subparsers.add_parser('run', help='options for running test')
    parser_run.add_argument("-i", "--interactive", help="Run the test interactively", action="store_true")
    parser_run.add_argument("-t", "--testname", help="Run a single testscript via buildtest", choices=test_choices, metavar='TEST-CHOICES')
    parser_run.add_argument("-s", "--software", help="Run test suite for application via buildtest", choices=app_choices, metavar='SOFTWARE-TEST-SUITE')
    parser_run.add_argument("-p", "--package", help="Run test suite for system package via buildtest", choices=systempkg_choices, metavar='PACKAGE-TEST-SUITE')
    parser_run.add_argument("--all-software", help="Run test suite for all software packages", action="store_true")
    parser_run.add_argument("--all-package", help="Run test suite for all system packages", action="store_true")
    parser_run.set_defaults(func=func_run_subcmd)

    # -------------------------------- module menu --------------------------
    parser_module = subparsers.add_parser('module', help='module load testing and difference between module trees')
    parser_module.add_argument("--module-load-test", help="conduct module load test for all modules defined in BUILDTEST_MODULE_ROOT", action="store_true")
    parser_module.add_argument("--diff-trees", help="Show difference between two module trees")
    parser_module.set_defaults(func=func_module_subcmd)

    # -------------------------------- benchmark menu ----------------------
    parser_benchmark = subparsers.add_parser('benchmark', help="Benchmark Menu")
    subparsers_benchmark = parser_benchmark.add_subparsers(help='subcommand help', dest="benchmark_subcommand")

    # -------------------------------- osu  menu ---------------------------
    osu_parser = subparsers_benchmark.add_parser('osu', help = "OSU MicroBenchmark sub menu")
    osu_parser.add_argument("-r", "--run", help ="Run Benchmark", action="store_true")
    osu_parser.add_argument("-i", "--info", help="show yaml key description", action="store_true")
    osu_parser.add_argument("-l", "--list", help="List of tests available for OSU Benchmark", action="store_true")
    osu_parser.add_argument("-c", "--config", help="OSU Yaml Configuration File")
    osu_parser.set_defaults(func=func_benchmark_osu_subcmd)

    # -------------------------------- HPL  menu ---------------------------
    hpl_parser = subparsers_benchmark.add_parser('hpl', help ="High Performance Linpack sub menu")
    hpl_parser.set_defaults(func=func_benchmark_hpl_subcmd)

    # -------------------------------- HPCG  menu ---------------------------
    hpcg_parser = subparsers_benchmark.add_parser('hpcg', help="High Performance Conjugate Gradient sub menu")
    hpcg_parser.set_defaults(func=func_benchmark_hpcg_subcmd)

    return parser

def parse_options(parser):
    """return parser as a dictionary and apply argument completion on parser object"""
    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    if args.subcommand:
        args.func(args)
    return args
