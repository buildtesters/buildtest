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
This module validates the user buildtest environment to ensure all everything
is setup before user can write tests

:author: Shahzeb Siddiqui (Pfizer)
"""
import subprocess
import time
import logging
import os
from framework.env import BUILDTEST_ROOT, config_opts
from framework.tools.utility import get_appname, get_appversion, get_toolchain_name, get_toolchain_version

def check_buildtest_setup():
    """
    Reports buildtest configuration and checks each BUILDTEST environment variable and check
    for module environment
    """

    BUILDTEST_MODULE_EBROOT = config_opts['BUILDTEST_EBROOT']
    BUILDTEST_MODULE_NAMING_SCHEME = config_opts['BUILDTEST_MODULE_NAMING_SCHEME']
    BUILDTEST_EASYCONFIG_REPO = config_opts['BUILDTEST_EASYCONFIG_REPO']
    BUILDTEST_TESTDIR = config_opts['BUILDTEST_TESTDIR']
    BUILDTEST_CONFIGS_REPO = config_opts['BUILDTEST_CONFIGS_REPO']
    BUILDTEST_PYTHON_REPO = config_opts['BUILDTEST_PYTHON_REPO']
    BUILDTEST_PERL_REPO = config_opts['BUILDTEST_PERL_REPO']
    BUILDTEST_R_REPO = config_opts['BUILDTEST_R_REPO']
    BUILDTEST_RUBY_REPO = config_opts['BUILDTEST_RUBY_REPO']
    BUILDTEST_TCL_REPO = config_opts['BUILDTEST_TCL_REPO']

    print "=============================================="
    print "buildtest configuration check"
    print "=============================================="

    print "Checking buildtest environment variables ..."

    ec = 0

    time.sleep(0.2)
    if not os.path.exists(BUILDTEST_ROOT):
        ec = 1
        print "STATUS: BUILDTEST_ROOT is not set ... FAILED"
    else:
        print "STATUS: BUILDTEST_ROOT ... PASSED"


    time.sleep(0.2)
    if not os.path.exists(BUILDTEST_CONFIGS_REPO):
        ec = 1
        print "STATUS: BUILDTEST_CONFIGS_REPO is not set ... FAILED"
    else:
        print "STATUS: BUILDTEST_CONFIGS_REPO ... PASSED"


    time.sleep(0.2)
    if not os.path.exists(BUILDTEST_TESTDIR):
        ec = 1
        print "STATUS: BUILDTEST_TESTDIR is not set ... FAILED"
    else:
        print "STATUS: BUILDTEST_TESTDIR ... PASSED"



    time.sleep(0.2)
    for tree in BUILDTEST_EBROOT:
        if not os.path.exists(tree):
            ec = 1
            print "STATUS: BUILDTEST_EBROOT:",tree, "does  not exists"
        else:
            print "STATUS: BUILDTEST_EBROOT:", tree, "is valid!"

    time.sleep(0.2)
    if not os.path.exists(BUILDTEST_EASYCONFIG_REPO):
        ec = 1
        print "STATUS: BUILDTEST_EASYCONFIG_REPO is not set ... FAILED"
    else:
        print "STATUS: BUILDTEST_EASYCONFIG_REPO ... PASSED"


    time.sleep(0.2)
    if BUILDTEST_MODULE_NAMING_SCHEME == "FNS" or  BUILDTEST_MODULE_NAMING_SCHEME == "HMNS":
        print "STATUS: BUILDTEST_MODULE_NAMING_SCHEME ... PASSED"
        print "BUILDTEST_MODULE_NAMING_SCHEME is set to: ", BUILDTEST_MODULE_NAMING_SCHEME
    else:
        ec = 1
        print "STATUS: BUILDTEST_MODULE_NAMING_SCHEME is set to: " + BUILDTEST_MODULE_NAMING_SCHEME
        print "Valid values for BUILDTEST_MODULE_NAMING_SCHEME are: [HMNS, FNS]"


    time.sleep(0.2)
    if not os.path.exists(BUILDTEST_R_REPO):
        ec = 1
        print "STATUS: BUILDTEST_R_REPO is not set"
    else:
        print "STATUS: BUILDTEST_R_REPO ... PASSED"


    time.sleep(0.2)
    if not os.path.exists(BUILDTEST_PERL_REPO):
        ec = 1
        print "STATUS: BUILDTEST_PERL_REPO is not set ... FAILED"
    else:
        print "STATUS: BUILDTEST_PERL_REPO ... PASSED"


    time.sleep(0.2)
    if not os.path.exists(BUILDTEST_PYTHON_REPO):
        ec = 1
        print "STATUS: BUILDTEST_PYTHON_REPO is not set ... FAILED"
    else:
        print "STATUS: BUILDTEST_PYTHON_REPO ... PASSED"

    time.sleep(0.2)
    if not os.path.exists(BUILDTEST_RUBY_REPO):
        ec = 1
        print "STATUS: BUILDTEST_RUBY_REPO is not set ... FAILED"
    else:
        print "STATUS: BUILDTEST_RUBY_REPO ... PASSED"


    time.sleep(0.2)
    if not os.path.exists(BUILDTEST_TCL_REPO):
        ec = 1
        print "STATUS: BUILDTEST_TCL_REPO is not set ... FAILED"
    else:
        print "STATUS: BUILDTEST_TCL_REPO ... PASSED"

    if ec == 0:
        print "buildtest environment variable PASSED!"

    time.sleep(0.2)

    cmd = "module --version"
    ret = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    (outputmsg,errormsg) = ret.communicate()
    ec = ret.returncode

    if ec == 0:
        print "Detecting module command .... "
        print outputmsg, errormsg

    else:
        print "module commmand not found in system"
        print outputmsg, errormsg


    # detecting whether we have Lmod or environment-modules
    # query Lmod rpm
    cmd = "rpm -q Lmod"
    ret = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    (outputmsg,errormsg) = ret.communicate()
    ec = ret.returncode
    if ec == 0:
        print "System detected Lmod found package - ", outputmsg


    cmd = "rpm -q environment-modules"
    ret = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    (outputmsg) = ret.communicate()[0]
    ec = ret.returncode

    if ec == 0:
        print "System detected environment-modules found package - ", outputmsg
