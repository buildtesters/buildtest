############################################################################
#
#  Copyright 2017-2019
#
#  https://github.com/HPC-buildtest/buildtest-framework
#
#  This file is part of buildtest.
#
#  buildtest is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  buildtest is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with buildtest.  If not, see <http://www.gnu.org/licenses/>.
#############################################################################
import sys
import os

sys.path.insert(0,os.path.join(os.getenv("BUILDTEST_ROOT"), 'src'))
# column width for linewrap for argparse library
os.environ['COLUMNS'] = "120"


from buildtest.tools.config import config_opts
from buildtest.tools.menu import menu, parse_options
from buildtest.tools.system import BuildTestSystem



def main():
    """Entry point to buildtest."""

    buildtest_system = BuildTestSystem()
    buildtest_system.check_system_requirements()


    parser = menu()

    parsed_opts = parse_options(parser)

    if parsed_opts.logdir:
        config_opts['BUILDTEST_LOGDIR'] = parsed_opts.logdir


if __name__ == "__main__":
    """Entry Point, invoking main() method"""
    main()
