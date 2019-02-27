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
Utility methods for getting application name, version and toolchain name and version
"""

from buildtest.tools.config import config_opts

class sset(set):
    def __str__(self):
        return ', '.join([str(i) for i in self])

def get_appname():
    """return application name from buildtest build -s option"""
    software = config_opts["BUILDTEST_SOFTWARE"]
    software = software.split('/')
    return software[0]

def get_appversion():
    """return application version from buildtest build -s option"""
    software = config_opts["BUILDTEST_SOFTWARE"]
    software = software.split('/')
    BUILDTEST_MODULE_NAMING_SCHEME = config_opts['BUILDTEST_MODULE_NAMING_SCHEME']
    if BUILDTEST_MODULE_NAMING_SCHEME == "FNS":
       return software[1]
    else:
        return software[1]

def get_application_name():
    """ get application name including the application version separated by "-" """
    return get_appname() + '-' + get_appversion()
