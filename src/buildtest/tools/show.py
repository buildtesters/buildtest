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

import textwrap
import sys
from buildtest.tools.config import show_configuration
from buildtest.tools.yaml import KEY_DESCRIPTION,SLURM_KEY_DESC, LSF_KEY_DESC

def func_show_subcmd(args):
    """entry point to show sub command"""
    if args.config:
        show_configuration()

    if args.keys:
        show_yaml_keys()


def show_yaml_keys():
    """implements buildtest show -k """

    print ('{:>50}'.format("General Keys"))

    print ('{:20} | {:<30}'.format("Keys","Description"))
    print('{:-<100}'.format(""))
    for k in sorted(KEY_DESCRIPTION):
        print('{:20} | {:<30}'.format(k,textwrap.fill(KEY_DESCRIPTION[k],120)))

    print()
    print ('{:>50}'.format("LSF Keys"))
    print()
    print ('{:20} | {:<30} | {:<30}'.format("Keys","LSF Equivalents","Description"))
    print('{:-<100}'.format(""))
    for k in sorted(LSF_KEY_DESC):
        print('{:20} | {:<30} | {:<30}'.format(k,textwrap.fill(LSF_KEY_DESC[k][0],120),textwrap.fill(LSF_KEY_DESC[k][1],120)))

    print()
    print ('{:>50}'.format("SLURM Keys"))
    print()
    print ('{:20} | {:<30} | {:<30}'.format("Keys","Slurm Equivalents","Description"))
    print('{:-<100}'.format(""))
    for k in sorted(SLURM_KEY_DESC):
        print('{:20} | {:<30} | {:<30}'.format(k,textwrap.fill(SLURM_KEY_DESC[k][0],120),textwrap.fill(SLURM_KEY_DESC[k][1],120)))
    sys.exit(0)
