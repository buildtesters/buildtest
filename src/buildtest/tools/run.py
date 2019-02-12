############################################################################
#
#  Copyright 2017-2019
#   https://github.com/HPC-buildtest/buildtest-framework
#    This file is part of buildtest.
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
buildtest run subcommand entry point
"""

import sys
from datetime import datetime
from buildtest.test.run.app import run_app_test
from buildtest.test.run.testname import run_testname
from buildtest.test.run.system import run_system_test
from buildtest.test.run.interactive import runtest_menu
from buildtest.test.run.app import run_app_choices, run_suite
from buildtest.test.run.system import run_system_choices
from buildtest.tools.config import config_opts
from buildtest.tools.system import BuildTestSystem


def func_run_subcmd(args):
    """ run subcommand entry point """
    if args.interactive:
        runtest_menu()
    if args.testname:
        run_testname(args.testname)
    if args.software:
        run_app_test(args.software)
    if args.suite:
        run_suite(args.suite)
    if args.package:
        run_system_test(args.package)
    if args.all_software:
        stack = run_app_choices()
        for software in stack:
            run_app_test(software,args.output)
    if args.all_package:
        stack = run_system_choices()
        for package in stack:
            run_system_test(package,args.output)
    sys.exit(0)

def write_system_info(fd,app_name=None,pkg_name=None):
    """ write system information into run file """
    system = BuildTestSystem().system
    fd.write("-------------------------- SYSTEM INFO --------------------------------------\n")
    fd.write("Date:" + str(datetime.now()) + "\n")
    fd.write("buildtest version: " + config_opts["BUILDTEST_VERSION"] + "\n")
    if app_name:
        fd.write("Application:" + app_name + "\n")
    if pkg_name:
        fd.write("System Package:" + pkg_name + "\n")

    for key in system:
        fd.write(key + ":" + str(system[key]) + "\n")
