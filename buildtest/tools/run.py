#
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

# @author: Shahzeb Siddiqui (Pfizer)

import sys
from buildtest.test.run.app import run_app_test
from buildtest.test.run.testname import run_test_buildtest
from buildtest.test.run.system import run_system_test
from buildtest.test.run.interactive import runtest_menu

def func_run_subcmd(args):
    """ run subcommand entry point """
    if args.interactive:
        runtest_menu()
    if args.testname:
        run_test_buildtest(args.testname)
    if args.app:
        run_app_test(args.app,args.output)
    if args.systempkg:
        run_system_test(args.systempkg)
    sys.exit(0)
