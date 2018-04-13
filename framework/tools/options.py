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

"""
:author: Shahzeb Siddiqui (Pfizer)
"""


import os

from framework.env import config_opts

def override_options_env_vars():
    """ override buildtest options by environment variables """

    if os.environ.get('BUILDTEST_MODULE_NAMING_SCHEME') == "FNS" or os.environ.get('BUILDTEST_MODULE_NAMING_SCHEME') == "HMNS":
        config_opts['BUILDTEST_MODULE_NAMING_SCHEME'] = os.environ['BUILDTEST_MODULE_NAMING_SCHEME']

    if os.environ.get('BUILDTEST_LOGDIR'):
        config_opts['BUILDTEST_LOGDIR']=os.environ['BUILDTEST_LOGDIR']

    if os.environ.get('BUILDTEST_TESTDIR'):
        config_opts['BUILDTEST_TESTDIR']=os.environ['BUILDTEST_TESTDIR']

    # multiple directories can be set separated by ":" for BUILDTEST_EBROOT as envrionment variable
    if os.environ.get('BUILDTEST_EBROOT'):

        if os.environ.get('BUILDTEST_EBROOT').find(":") != -1:
            ebroot_list = os.environ.get('BUILDTEST_EBROOT').split(":")
            config_opts['BUILDTEST_EBROOT'] = []
            for ebroot in ebroot_list:
                config_opts['BUILDTEST_EBROOT'].append(ebroot)
        else:
            config_opts['BUILDTEST_EBROOT']=[]
            config_opts['BUILDTEST_EBROOT'].append(os.environ['BUILDTEST_EBROOT'])


    if os.environ.get('BUILDTEST_EASYCONFIG_REPO'):
        config_opts['BUILDTEST_EASYCONFIG_REPO']=os.environ['BUILDTEST_EASYCONFIG_REPO']

    if os.environ.get('BUILDTEST_TCL_REPO'):
        config_opts['BUILDTEST_TCL_REPO']=os.environ['BUILDTEST_TCL_REPO']

    if os.environ.get('BUILDTEST_RUBY_REPO'):
        config_opts['BUILDTEST_RUBY_REPO']=os.environ['BUILDTEST_RUBY_REPO']

    if os.environ.get('BUILDTEST_R_REPO'):
        config_opts['BUILDTEST_R_REPO']=os.environ['BUILDTEST_R_REPO']

    if os.environ.get('BUILDTEST_PYTHON_REPO'):
        config_opts['BUILDTEST_PYTHON_REPO']=os.environ['BUILDTEST_PYTHON_REPO']

    if os.environ.get('BUILDTEST_PERL_REPO'):
        config_opts['BUILDTEST_PERL_REPO']=os.environ['BUILDTEST_PERL_REPO']
