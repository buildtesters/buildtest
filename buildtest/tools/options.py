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
Overrides buildtest configuration via environment variable or command options

:author: Shahzeb Siddiqui (Pfizer)
"""


import os

from buildtest.tools.config import config_opts


def override_configuration():
    """ override buildtest options by environment variables """

    if os.environ.get('BUILDTEST_MODULE_NAMING_SCHEME'):
        config_opts['BUILDTEST_MODULE_NAMING_SCHEME'] = os.environ['BUILDTEST_MODULE_NAMING_SCHEME']

    if os.environ.get('BUILDTEST_LOGDIR'):
        config_opts['BUILDTEST_LOGDIR']=os.environ['BUILDTEST_LOGDIR']

    if os.environ.get('BUILDTEST_TESTDIR'):
        config_opts['BUILDTEST_TESTDIR']=os.environ['BUILDTEST_TESTDIR']

    # multiple directories can be set separated by ":" for BUILDTEST_MODULE_ROOT as envrionment variable
    if os.environ.get('BUILDTEST_MODULE_ROOT'):

        if os.environ.get('BUILDTEST_MODULE_ROOT').find(":") != -1:
            ebroot_list = os.environ.get('BUILDTEST_MODULE_ROOT').split(":")
            config_opts['BUILDTEST_MODULE_ROOT'] = []
            for ebroot in ebroot_list:
                config_opts['BUILDTEST_MODULE_ROOT'].append(ebroot)
        else:
            config_opts['BUILDTEST_MODULE_ROOT']=[]
            config_opts['BUILDTEST_MODULE_ROOT'].append(os.environ['BUILDTEST_MODULE_ROOT'])

    if os.environ.get('BUILDTEST_IGNORE_EASYBUILD'):
        config_opts['BUILDTEST_IGNORE_EASYBUILD']=os.environ['BUILDTEST_IGNORE_EASYBUILD']

    if os.environ.get('BUILDTEST_CLEAN_BUILD'):
        config_opts['BUILDTEST_CLEAN_BUILD']=os.environ['BUILDTEST_CLEAN_BUILD']

    if os.environ.get('BUILDTEST_ENABLE_JOB'):
        config_opts['BUILDTEST_ENABLE_JOB']=os.environ['BUILDTEST_ENABLE_JOB']

    if os.environ.get('BUILDTEST_CONFIGS_REPO'):

        config_opts['BUILDTEST_CONFIGS_REPO']=os.environ['BUILDTEST_CONFIGS_REPO']

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

    if os.environ.get('BUILDTEST_SHELL'):
        config_opts['BUILDTEST_SHELL']=os.environ['BUILDTEST_SHELL']

    if os.environ.get('BUILDTEST_JOB_TEMPLATE'):
        config_opts['BUILDTEST_JOB_TEMPLATE']=os.environ['BUILDTEST_JOB_TEMPLATE']

    config_opts['BUILDTEST_CONFIGS_REPO_SYSTEM'] = os.path.join(config_opts['BUILDTEST_CONFIGS_REPO'],"buildtest/system")
    config_opts['BUILDTEST_CONFIGS_REPO_SOFTWARE'] = os.path.join(config_opts['BUILDTEST_CONFIGS_REPO'],"buildtest/ebapps")
    config_opts['BUILDTEST_R_TESTDIR'] = os.path.join(config_opts['BUILDTEST_R_REPO'],"buildtest/R/code")
    config_opts['BUILDTEST_PERL_TESTDIR'] = os.path.join(config_opts['BUILDTEST_PERL_REPO'],"buildtest/perl/code")
    config_opts['BUILDTEST_PYTHON_TESTDIR'] = os.path.join(config_opts['BUILDTEST_PYTHON_REPO'],"buildtest/python/code")
    config_opts['BUILDTEST_RUBY_TESTDIR'] = os.path.join(config_opts['BUILDTEST_RUBY_REPO'],"buildtest/ruby/code")
