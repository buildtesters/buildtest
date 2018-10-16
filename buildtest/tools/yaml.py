############################################################################
#
#  Copyright 2017-2018
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
buildtest yaml subcommand entry point

@author: Shahzeb Siddqiui (shahzebmsiddiqui@gmail.com)
"""
import sys
from buildtest.tools.generate_yaml import create_software_yaml, create_system_yaml, create_all_software_yaml, create_all_system_yaml

def func_yaml_subcmd(args):
    """ entry point to _buildtest yaml """
    if args.ebyaml:
        create_software_yaml(args.ebyaml)

    if args.sysyaml:
        create_system_yaml(args.sysyaml)

    if args.all_software_yaml:
        create_all_software_yaml()

    if args.all_system_yaml:
        create_all_system_yaml()

    sys.exit(0)
