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
Checks buildtest configuration and reports any errors. Also display buildtest
configuration using buildtest --show

:author: Shahzeb Siddiqui (Pfizer)
"""
import os
import sys
import time
import logging
import subprocess
import yaml

# read the BUILDTEST env vars from the shell environment that is sourced by setup.sh
BUILDTEST_VERSION="0.6.1"
BUILDTEST_ROOT = os.getenv("BUILDTEST_ROOT")

BUILDTEST_JOB_EXTENSION = [".lsf", ".slurm", ".pbs"]
BUILDTEST_SHELLTYPES = ["sh", "bash", "csh"]

PYTHON_APPS = ["python","anaconda2", "anaconda3"]
MPI_APPS = ["openmpi", "mpich","mvapich2", "intel", "impi"]

#BUILDTEST_DEFAULT_CONFIG=os.path.join(BUILDTEST_ROOT,"config.yaml")
#print BUILDTEST_DEFAULT_CONFIG
#fd = open(BUILDTEST_DEFAULT_CONFIG,'r')
BUILDTEST_CONFIG_FILE = os.path.join(os.getenv("HOME"),".local","buildtest","config.yaml")
#if not os.path.exists(BUILDTEST_CONFIG_FILE):
#    print (f"FILE: {BUILDTEST_CONFIG_FILE} not found")
try:
    fd = open(BUILDTEST_CONFIG_FILE,'r')
    config_opts = yaml.load(fd)
    config_opts['BUILDTEST_CONFIGS_REPO_SYSTEM']=""
    config_opts['BUILDTEST_CONFIGS_REPO_SOFTWARE']=""

except FileNotFoundError as err_msg:
    print(f"{err_msg}")
    raise

#global logID
logID = "buildtest"


def check_configuration():
    """
    Reports buildtest configuration and checks each BUILDTEST environment variable and check
    for module environment
    """

    BUILDTEST_MODULE_ROOT = config_opts['BUILDTEST_MODULE_ROOT']
    BUILDTEST_MODULE_NAMING_SCHEME = config_opts['BUILDTEST_MODULE_NAMING_SCHEME']
    BUILDTEST_TESTDIR = config_opts['BUILDTEST_TESTDIR']
    BUILDTEST_CONFIGS_REPO = config_opts['BUILDTEST_CONFIGS_REPO']
    BUILDTEST_PYTHON_REPO = config_opts['BUILDTEST_PYTHON_REPO']
    BUILDTEST_PERL_REPO = config_opts['BUILDTEST_PERL_REPO']
    BUILDTEST_R_REPO = config_opts['BUILDTEST_R_REPO']
    BUILDTEST_RUBY_REPO = config_opts['BUILDTEST_RUBY_REPO']
    BUILDTEST_IGNORE_EASYBUILD = config_opts['BUILDTEST_IGNORE_EASYBUILD']
    BUILDTEST_SHELL = config_opts['BUILDTEST_SHELL']
    BUILDTEST_JOB_TEMPLATE = config_opts['BUILDTEST_JOB_TEMPLATE']

    #print "Checking buildtest environment variables ..."

    ec = 0

    time.sleep(0.1)

    if not os.path.exists(BUILDTEST_ROOT):
        ec = 1
        print ("ERROR:  \t BUILDTEST_ROOT: %s does not exist", BUILDTEST_ROOT)



    time.sleep(0.1)
    if not os.path.exists(BUILDTEST_CONFIGS_REPO):
        ec = 1
        print ("ERROR:  \t BUILDTEST_CONFIGS_REPO: %s does not exist",BUILDTEST_CONFIGS_REPO)


    time.sleep(0.1)
    for tree in BUILDTEST_MODULE_ROOT:
        if not os.path.exists(tree):
            ec = 1
            print ("ERROR:  \t BUILDTEST_MODULE_ROOT: %s does  not exists ", tree)



    time.sleep(0.1)
    if BUILDTEST_MODULE_NAMING_SCHEME not in ["FNS", "HMNS"]:
        ec = 1
        print ("ERROR:  \t BUILDTEST_MODULE_NAMING_SCHEME: %s valid values are {HMNS, FNS}", BUILDTEST_MODULE_NAMING_SCHEME)

    time.sleep(0.1)

    if BUILDTEST_IGNORE_EASYBUILD not in ["True", "False"]:
        ec = 1
        print ("ERROR:  \t BUILDTEST_IGNORE_EASYBUILD: %s valid values are {True, False} ",BUILDTEST_IGNORE_EASYBUILD)

    time.sleep(0.1)
    if not os.path.exists(BUILDTEST_R_REPO):
        ec = 1
        print ("ERROR:  \t BUILDTEST_R_REPO: %s does not exist", BUILDTEST_R_REPO)

    time.sleep(0.1)
    if not os.path.exists(config_opts['BUILDTEST_R_TESTDIR']):
        ec = 1
        print ("ERROR: \t BUILDTEST_R_TESTDIR: %s  does not exist", config_opts['BUILDTEST_R_TESTDIR'])

    time.sleep(0.1)
    if not os.path.exists(BUILDTEST_PERL_REPO):
        ec = 1
        print ("ERROR:  \t BUILDTEST_PERL_REPO: %s does not exist", BUILDTEST_PERL_REPO)

    time.sleep(0.1)
    if not os.path.exists(config_opts['BUILDTEST_PERL_TESTDIR']):
        ec = 1
        print ("ERROR: \t BUILDTEST_PERL_TESTDIR: %s does not exist",config_opts['BUILDTEST_PERL_TESTDIR'])

    time.sleep(0.1)
    if not os.path.exists(BUILDTEST_PYTHON_REPO):
        ec = 1
        print ("ERROR:  \t BUILDTEST_PYTHON_REPO: %s does not exist",BUILDTEST_PYTHON_REPO)

    time.sleep(0.1)
    if not os.path.exists(config_opts['BUILDTEST_PYTHON_TESTDIR']):
        ec = 1
        print ("ERROR: \t BUILDTEST_PYTHON_TESTDIR: %s does not exist", config_opts['BUILDTEST_PYTHON_TESTDIR'])


    time.sleep(0.1)
    if not os.path.exists(BUILDTEST_RUBY_REPO):
        ec = 1
        print ("ERROR:  \t BUILDTEST_RUBY_REPO: %s does not exist",BUILDTEST_RUBY_REPO)

    time.sleep(0.1)
    if not os.path.exists(config_opts['BUILDTEST_RUBY_TESTDIR']):
        ec = 1
        print ("ERROR: \t BUILDTEST_RUBY_TESTDIR: %s does not exist",config_opts['BUILDTEST_RUBY_TESTDIR'])

    time.sleep(0.1)
    if BUILDTEST_SHELL not in BUILDTEST_SHELLTYPES:
        ec = 1
        print ("ERROR: \t BUILDTEST_SHELL: %s not a valid value, must be one of the following: %s", BUILDTEST_SHELL, BUILDTEST_SHELLTYPES)

    time.sleep(0.1)


    if not os.path.exists(BUILDTEST_JOB_TEMPLATE):
        ec = 1
        print ("ERROR:\t BUILDTEST_JOB_TEMPLATE: %s does not exist",BUILDTEST_JOB_TEMPLATE)

    time.sleep(0.1)

    if os.path.splitext(BUILDTEST_JOB_TEMPLATE)[1]  not in BUILDTEST_JOB_EXTENSION:
        ec = 1
        print ("Invalid file extension: %s must be one of the following extension %s", BUILDTEST_JOB_EXTENSION, BUILDTEST_JOB_EXTENSION)

    time.sleep(0.1)

    if ec != 0:
        print ("Please fix your BUILDTEST configuration")
        sys.exit(1)

    cmd = "module --version"
    ret = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    (outputmsg,errormsg) = ret.communicate()
    ec = ret.returncode

    if ec != 0:
        print ("module commmand not found in system")
        print (outputmsg)
        print (errormsg)
        sys.exit(1)

def show_configuration():
    """ show buildtest configuration """
    print
    print ("\t buildtest configuration summary")
    print ("\t (C): Configuration File,  (E): Environment Variable")
    print
    print (("BUILDTEST_ROOT" + "\t (E) =").expandtabs(50), os.getenv("BUILDTEST_ROOT"))
    for key in sorted(config_opts):
        if os.getenv(key):
            type = "(E)"
        else:
            type = "(C)"

        if key == "BUILDTEST_MODULE_ROOT":
            tree = ""
            for mod_tree in config_opts[key]:
                tree += mod_tree + ":"

            # remove last colon
            tree = tree[:-1]
            print ((key + "\t " + type + " =").expandtabs(50), tree)
        else:
            print ((key + "\t " + type + " =").expandtabs(50), config_opts[key])

    sys.exit(0)
