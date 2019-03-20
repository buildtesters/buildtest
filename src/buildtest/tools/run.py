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
from buildtest.test.run.system import run_system_test, run_app_test, run_suite
from buildtest.test.run.interactive import runtest_menu

from buildtest.test.job import submit_job_to_scheduler
from buildtest.tools.system import BuildTestSystem


def func_run_subcmd(args):
    """ run subcommand entry point """
    if args.interactive:
        runtest_menu()
    if args.software:
        run_app_test(args.software)
    if args.suite:
        run_suite(args.suite)
    if args.package:
        run_system_test(args.package)
    if args.job:
        submit_job_to_scheduler(args.suite)
    sys.exit(0)

def write_system_info(fd,app_name=None,pkg_name=None):
    """ write system information into run file """
    system_info = BuildTestSystem()
    system = system_info.get_system()

    fd.write(f"Date: {str(datetime.now())} \n")
    fd.write("-------------------------- SYSTEM INFO --------------------------------------\n")

    if app_name:
        fd.write("Application:" + app_name + "\n")
    if pkg_name:
        fd.write("System Package:" + pkg_name + "\n")

    for key in system:
        fd.write(f"{key} : {str(system[key])} \n")
