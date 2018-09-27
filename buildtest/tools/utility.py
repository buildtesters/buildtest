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
Utility methods for getting application name, version and toolchain name and version

:author: Shahzeb Siddiqui (Pfizer)
"""


from buildtest.tools.config import config_opts

class sset(set):
    def __str__(self):
        return ', '.join([str(i) for i in self])

def get_appname():
    """return application name from -s option"""
    software = config_opts["BUILDTEST_SOFTWARE"]
    software = software.split('/')
    return software[0]

def get_appversion():
    """return application version from -s option"""
    software = config_opts["BUILDTEST_SOFTWARE"]
    software = software.split('/')
    BUILDTEST_MODULE_NAMING_SCHEME = config_opts['BUILDTEST_MODULE_NAMING_SCHEME']
    if BUILDTEST_MODULE_NAMING_SCHEME == "FNS":
        tc = get_toolchain()
        tcname = get_toolchain_name()
        # when toolchain is not specified modulename is something like Python/2.7.14
        if tcname == "":
            return software[1]
        # when toolchain is part of modulename then it is something like Python/2.7.14-GCCcore-6.4.0.
        # must strip toolchain to get the version
        else:
            appversion = software[1].replace(tc,'')

            if appversion[-1] == "-":
                appversion = appversion[:-1]
                return appversion
    else:
        return software[1]

def get_application_name():
    return get_appname() + '-' + get_appversion()

def get_toolchain():
    return get_toolchain_name() + '-' + get_toolchain_version()

def get_toolchain_name():
    """return toolchain  name from -t option"""
    toolchain = config_opts["BUILDTEST_TOOLCHAIN"]


    # checking if toolchain is defined in argument
    if toolchain is  None:
            return ""
    else:
        toolchain = toolchain.split("/")
        return toolchain[0]

def get_toolchain_version():
    """return toolchain version from -t option"""
    toolchain = config_opts["BUILDTEST_TOOLCHAIN"]

    # checking if toolchain is defined in argument
    if toolchain is None:
        return ""
    else:
        toolchain = toolchain.split("/")
        return toolchain[1]
