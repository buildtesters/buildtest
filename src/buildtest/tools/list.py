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


"""
This module implements all the list operation in buildtest which include the
following:
1. List software (buildtest list -ls)
2. List Software and associated module file (buildtest list -svr)
3. List easyconfigs in module tree (buildtest list --easyconfigs)
"""

import json
import sys
from collections import OrderedDict
from operator import itemgetter

from buildtest.tools.easybuild import find_easyconfigs
from buildtest.tools.software import get_unique_software, \
                                    software_version_relation


def func_list_subcmd(args):
    """ This method is the entry point for buildtest list subcommand."""

    if args.easyconfigs:
        find_easyconfigs()
    if args.list_unique_software:
        list_software(args)
    if args.software_version_relation:
        list_software_version_relation(args)



def list_software(args):
    """ This method implements buildtest list -ls """
    software_set=get_unique_software()

    if args.format == "json":
        json.dump(software_set, sys.stdout, indent=4, sort_keys=True)
    else:
        count = 0
        text = """
        ID  |     Software
        ----|-----------------------------  """

        print (text)
        for item in software_set:
            count = count + 1
            print ((str(count) + "\t|").expandtabs(4), item)

        print ("Total Software Packages: ", count)


def list_software_version_relation(args):
    """ This method implements  buildtest list -svr """
    software_dict = software_version_relation()

    if args.format == "json":
        json.dump(software_dict, sys.stdout, indent=4, sort_keys=True)
    else:
        text = """
         ID  |        Software            |      ModuleFile Path
        -----|----------------------------|----------------------------- """
        print (text)
        id = 0

        sorted_dict = OrderedDict(
            sorted(software_dict.items(), key=itemgetter(1)))

        keylist = sorted_dict.keys()

        modulecnt = 0

        for key in keylist:
            id = id + 1
            # for value in sset(software_dict[key]):
            print ((str(id) + "\t |").expandtabs(4),
                   "\t" + (sorted_dict[key] + "\t |").expandtabs(
                       25) + "\t" + key)
            modulecnt += 1

        print ("Total Software Modules Found: ", modulecnt)
