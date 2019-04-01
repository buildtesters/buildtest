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

    # multiple directories can be set separated by ":" for
    # BUILDTEST_MODULE_ROOT as envrionment variable
    if os.environ.get('BUILDTEST_MODULE_ROOT'):

        if os.environ.get('BUILDTEST_MODULE_ROOT').find(":") != -1:
            mod_trees = os.environ.get('BUILDTEST_MODULE_ROOT').split(":")
            config_opts['BUILDTEST_MODULE_ROOT'] = []
            for tree in mod_trees:
                config_opts['BUILDTEST_MODULE_ROOT'].append(tree)
        else:
            config_opts['BUILDTEST_MODULE_ROOT']=[]
            config_opts['BUILDTEST_MODULE_ROOT'].append(os.environ['BUILDTEST_MODULE_ROOT'])

    if os.environ.get('BUILDTEST_EASYBUILD'):
        truth_value = strtobool(os.environ['BUILDTEST_EASYBUILD'])
        if truth_value == 1:
            config_opts['BUILDTEST_EASYBUILD']=True
        else:
            config_opts['BUILDTEST_EASYBUILD']=False


    if os.environ.get('BUILDTEST_CLEAN_BUILD'):
        truth_value = strtobool(os.environ['BUILDTEST_CLEAN_BUILD'])
        if truth_value == 1:
            config_opts['BUILDTEST_CLEAN_BUILD']=True
        else:
            config_opts['BUILDTEST_CLEAN_BUILD']=False

    if os.environ.get('BUILDTEST_OHPC'):
        truth_value = strtobool(os.environ['BUILDTEST_OHPC'])
        if truth_value == 1:
            config_opts['BUILDTEST_OHPC']=True
        else:
            config_opts['BUILDTEST_OHPC']=False


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

