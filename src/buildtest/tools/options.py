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
Overrides buildtest configuration via environment variable or command options
"""

import os

from buildtest.tools.config import config_opts
from distutils.util import strtobool

def override_configuration():
    """Override buildtest options by environment variables """

    if os.environ.get('BUILDTEST_LOGDIR'):
        config_opts['BUILDTEST_LOGDIR']=os.environ['BUILDTEST_LOGDIR']

    if os.environ.get('BUILDTEST_TESTDIR'):
        config_opts['BUILDTEST_TESTDIR']=os.environ['BUILDTEST_TESTDIR']

    bool_config_override("BUILDTEST_BINARY")
    bool_config_override("BUILDTEST_EASYBUILD")
    bool_config_override("BUILDTEST_CLEAN_BUILD")
    bool_config_override("BUILDTEST_OHPC")


    if os.environ.get('BUILDTEST_SHELL'):
        config_opts['BUILDTEST_SHELL']=os.environ['BUILDTEST_SHELL']


    if os.environ.get('BUILDTEST_SUCCESS_THRESHOLD'):
        threshold = float(os.environ.get('BUILDTEST_SUCCESS_THRESHOLD'))

        if threshold >= 0.0 and threshold <= 1.0:
            config_opts['BUILDTEST_SUCCESS_THRESHOLD']=threshold

    if os.environ.get('BUILDTEST_RUN_DIR'):
        run_dir = os.environ.get('BUILDTEST_RUN_DIR')
        if os.path.exists(run_dir):
            config_opts['BUILDTEST_RUN_DIR']=run_dir


def bool_config_override(key):
    """override boolean configuration via environment varaible"""
    if os.environ.get(key):
        truth_value = strtobool(os.environ[key])
        if truth_value == 1:
            config_opts[key]=True
        else:
            config_opts[key]=False