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


import yaml
import os
import sys
import subprocess
from shutil import copy


BUILDTEST_VERSION="0.6.3"
BUILDTEST_ROOT = os.getenv("BUILDTEST_ROOT")

BUILDTEST_JOB_EXTENSION = [".lsf", ".slurm"]
BUILDTEST_SHELLTYPES = ["sh", "bash", "csh"]

BUILDTEST_TEST_EXT = BUILDTEST_JOB_EXTENSION + ["."+ i for i in BUILDTEST_SHELLTYPES]

PYTHON_APPS = ["python","anaconda2", "anaconda3"]
MPI_APPS = ["openmpi", "mpich","mvapich2", "intel", "impi"]

MPI_C_LIST = ["mpicc", "mpiicc"]
MPI_F_LIST = ["mpifort", "mpifc", "mpif90", "mpif77"]
MPI_CPP_LIST = ["mpic++", "mpicxx", "mpiicpc"]
MPI_LIST = MPI_C_LIST + MPI_F_LIST + MPI_CPP_LIST


buildtest_home_conf_dir = os.path.join(os.getenv("HOME"), ".buildtest")
BUILDTEST_CONFIG_FILE = os.path.join(buildtest_home_conf_dir, "settings.yml")

DEFAULT_CONFIG_FILE = os.path.join(os.getenv("BUILDTEST_ROOT"),"settings.yml")

if not os.path.isdir(buildtest_home_conf_dir):
    print(f"Creating buildtest configuration directory: \
            {buildtest_home_conf_dir}")
    os.makedirs(buildtest_home_conf_dir)

# if the file $HOME/.buildtest/settings.yml does not exist copy the default file
# into the appropriate location
if not os.path.exists(BUILDTEST_CONFIG_FILE):
    copy(DEFAULT_CONFIG_FILE,BUILDTEST_CONFIG_FILE)
    print(f"Copying Default Configuration {DEFAULT_CONFIG_FILE} to \
          {BUILDTEST_CONFIG_FILE}")


fd = open(BUILDTEST_CONFIG_FILE, 'r')
config_opts = yaml.load(fd)

# if MODULEPATH is not declared set BUILDTEST_MODULE_ROOT to None. In this event
#  user should fix their environment
if os.getenv("MODULEPATH") == None:
    config_opts["BUILDTEST_MODULE_ROOT"] = None
else:
    # otherwise set this to MODULEPATH
    config_opts["BUILDTEST_MODULE_ROOT"] = os.getenv("MODULEPATH").split(":")


# The section below causes import error, trying to clone buildtest-configs and
# write yaml content back to file.
"""
# get parent directory where buildtest-framework is cloned
parent_BUILDTEST_ROOT = os.path.dirname(os.getenv("BUILDTEST_ROOT"))
os.chdir(parent_BUILDTEST_ROOT)
# if buildtest-configs does not exist in parent directory then clone it
if not os.path.exists("buildtest-configs"):
    print("Cloning repo buildtest-configs")
    git_clone = "git clone git@github.com:HPC-buildtest/buildtest-configs.git"
    os.system(git_clone)

config_opts["BUILDTEST_CONFIGS_REPO"] = os.path.abspath("buildtest-configs")

with open(BUILDTEST_CONFIG_FILE,'w') as outfile:
    yaml.dump(config_opts,outfile,default_flow_style=False)
"""


config_opts['BUILDTEST_VERSION'] = BUILDTEST_VERSION

#global logID
logID = "buildtest"


DIR_config = [ "BUILDTEST_CONFIGS_REPO",
              "BUILDTEST_LOGDIR",
              "BUILDTEST_TESTDIR",
              "BUILDTEST_RUN_DIR" ]
config_yaml_keys = {
    'BUILDTEST_MODULE_NAMING_SCHEME': type("str"),
    'BUILDTEST_EASYBUILD': type(True),
    'BUILDTEST_CLEAN_BUILD': type(True),
    'BUILDTEST_OHPC': type(True),
    'BUILDTEST_BINARY': type(True),
    'BUILDTEST_SHELL': type("str"),
    'BUILDTEST_SUCCESS_THRESHOLD': type(1.0),
    'BUILDTEST_MODULE_ROOT': type([]),
    'BUILDTEST_CONFIGS_REPO': type("str"),
    'BUILDTEST_LOGDIR': type("str"),
    'BUILDTEST_TESTDIR': type("str"),
    'BUILDTEST_RUN_DIR': type("str"),
}
values_BUILDTEST_MODULE_NAMING_SCHEME = ["HMNS", "FNS"]


def check_configuration():
    """ Checks if each key in configuration file (settings.yml) is valid
        key and check type validation of each key and its value. For some keys
        special logic is taken to ensure values are correct and directory path
        exists.

        Also check if module command is found.

        If any error is found buildtest will terminate immediately. """


    ec = 0

    keylist = config_yaml_keys.keys()
    valuelist = config_yaml_keys.values()

    # check if any key is not found in settings.yml
    for key in keylist:
        if key not in config_opts:
            print (f"Unable to find key: {key} in {BUILDTEST_CONFIG_FILE}")
            ec = 1


    for key,value in zip(keylist,valuelist):
        if value is not type(config_opts[key]):
            print(f"Invalid Type for key: {key}")
            print(f"Expecting type: {str(value)}")
            print(f"Current type: {str(type(config_opts[key]))}")
            ec = 1

        # check if BUILDTEST_MODULE_NAMING_SCHEME is either "FNS" or "HMNS"
        if (key == "BUILDTEST_MODULE_NAMING_SCHEME" and
            config_opts[key] not in values_BUILDTEST_MODULE_NAMING_SCHEME):
            print (f"{key} expects value "
                   + f"{str(values_BUILDTEST_MODULE_NAMING_SCHEME)} current "
                   + f"value is {str(config_opts[key])}" )
            ec = 1

        if (key == "BUILDTEST_SHELL" and
            config_opts[key] not in BUILDTEST_SHELLTYPES):
            print (f"{key} expects value {str(BUILDTEST_SHELLTYPES)} current "
                   + f"value is {str(config_opts[key])}")
            ec = 1

        # check if BUILDTEST_SUCCESS_THRESHOLD is between 0.0 and 1.0
        if (key == "BUILDTEST_SUCCESS_THRESHOLD" and
            (config_opts[key] < 0.0 or  config_opts[key] > 1.0)):
            print (f"{key} must be between [0.0-1.0]")
            print(f"Current value is {str(config_opts[key])}")
            ec = 1

        if key == "BUILDTEST_MODULE_ROOT":
            if config_opts["BUILDTEST_MODULE_ROOT"] == None:
                print("Please specify a module tree to BUILDTEST_MODULE_ROOT"
                     + f"in configuration {BUILDTEST_CONFIG_FILE}")
            else:
                for module_root in config_opts[key]:
                    if not os.path.isdir(module_root):
                        print (f"{module_root} directory does not exist"
                               + " specified in BUILDTEST_MODULE_ROOT")
                        ec = 1

        # if yaml key is of type FILE, check if file exists
        if value in DIR_config:
            if not os.path.isdir(config_opts[key]):
                print (f"{config_opts[key]} has an invalid directory path "
                       + " lease check your configuration")
                ec = 1
    if (ec):
        sys.exit(0)

    cmd = "module --version"
    ret = subprocess.Popen(cmd,shell=True,
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    (outputmsg,errormsg) = ret.communicate()
    ec = ret.returncode

    if ec != 0:
        print ("module commmand not found in system")
        print (outputmsg)
        print (errormsg)
        sys.exit(1)


    # if BUILDTEST_PREPEND_MODULES not defined then declare as empty list
    if "BUILDTEST_PREPEND_MODULES" not in  list(config_opts.keys()):
        config_opts["BUILDTEST_PREPEND_MODULES"] = []



def show_configuration():
    """ This method display buildtest configuration to terminal and this
        implements command buildtest show --config """
    exclude_list = ["BUILDTEST_VERSION"]
    print
    print ("\t buildtest configuration summary")
    print ("\t (C): Configuration File,  (E): Environment Variable")
    print


    for key in sorted(config_opts):
        if key in exclude_list:
            continue
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
