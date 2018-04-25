############################################################################
#
#  Copyright 2017
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

import os
import sys
from framework.env import config_opts

def show_configuration():
    """ show buildtest configuration """
    print
    print "\t buildtest configuration summary"
    print "\t (C): Configuration File,  (E): Environment Variable"
    print
    print ("BUILDTEST_ROOT" + "\t (E):").expandtabs(50), os.environ['BUILDTEST_ROOT']
    for key in sorted(config_opts):
        if os.environ.get(key):
            type = "(E)"
        else:
            type = "(C)"

        if key == "BUILDTEST_MODULE_ROOT":
            tree = ""
            for mod_tree in config_opts[key]:
                tree += mod_tree + ":"

            # remove last colon
            tree = tree[:-1]
            print (key + "\t " + type + " =").expandtabs(50), tree
        else:
            print (key + "\t " + type + " =").expandtabs(50), config_opts[key]

    sys.exit(0)
