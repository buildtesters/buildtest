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

import json
import yaml
import os
import sys
import subprocess
from shutil import copy


BUILDTEST_VERSION="0.6.3"
BUILDTEST_ROOT = os.getenv("BUILDTEST_ROOT")

BUILDTEST_JOB_EXTENSION = [".lsf", ".slurm"]
BUILDTEST_SHELLTYPES = ["sh", "bash", "csh"]

# test scripts that need to be run locally
BUILDTEST_TEST_LOCAL_EXT = ["."+ i for i in BUILDTEST_SHELLTYPES]
BUILDTEST_TEST_EXT = BUILDTEST_JOB_EXTENSION + \
                     ["."+ i for i in BUILDTEST_SHELLTYPES]

BUILDTEST_BUILD_LOGFILE = os.path.join(os.getenv("BUILDTEST_ROOT"),"var","build.json")
BUILDTEST_SYSTEM = os.path.join(os.getenv("BUILDTEST_ROOT"),"var","system.json")
# dictionary used for storing status of builds
BUILDTEST_BUILD_HISTORY= {}

buildtest_home_conf_dir = os.path.join(os.getenv("HOME"), ".buildtest")
BUILDTEST_CONFIG_FILE = os.path.join(buildtest_home_conf_dir, "settings.yml")
BUILDTEST_MODULE_COLLECTION_FILE = os.path.join(os.getenv("BUILDTEST_ROOT"), "var", "collection.json")
BUILDTEST_MODULE_FILE = os.path.join(os.getenv("BUILDTEST_ROOT"), "var", "modules.json")
DEFAULT_CONFIG_FILE = os.path.join(os.getenv("BUILDTEST_ROOT"),"settings.yml")

# check if $HOME/.buildtest exists, if not create directory
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

# load the configuration file
fd = open(BUILDTEST_CONFIG_FILE, 'r')
config_opts = yaml.safe_load(fd)

config_opts["BUILDTEST_CONFIGS_REPO"]= os.path.join(os.environ["BUILDTEST_ROOT"],"toolkit")
# if BUILDTEST_MODULEPATH is empty list then check if MODULEPATH is defined
# and set result to BUILDTEST_MODULEPATH
if len(config_opts["BUILDTEST_MODULEPATH"]) == 0:

    if os.getenv("MODULEPATH") == None:
        config_opts["BUILDTEST_MODULEPATH"] = []
    else:
        # otherwise set this to MODULEPATH
        tree_list = []
        # check each directory in MODULEPATH and add it to BUILDTEST_MODULEPATH
        for tree in os.getenv("MODULEPATH").split(":"):
            if os.path.isdir(tree):
                tree_list.append(tree)
            #else:
                #print (f"Skipping module tree {tree} because path does not exist")
        config_opts["BUILDTEST_MODULEPATH"] = tree_list

config_opts['BUILDTEST_VERSION'] = BUILDTEST_VERSION

logID = "buildtest"


config_directory_types = [
  "BUILDTEST_LOGDIR",
  "BUILDTEST_TESTDIR",
  "BUILDTEST_RUN_DIR",
]
config_yaml_keys = {
    'BUILDTEST_BINARY': type(True),
    'BUILDTEST_MODULE_FORCE_PURGE': type(True),
    'BUILDTEST_SHELL': type("str"),
    'BUILDTEST_SUCCESS_THRESHOLD': type(1.0),
    'BUILDTEST_MODULEPATH': type([]),
    'BUILDTEST_SPIDER_VIEW': type("str"),
    'BUILDTEST_PARENT_MODULE_SEARCH': type("str"),
    'BUILDTEST_LOGDIR': type("str"),
    'BUILDTEST_TESTDIR': type("str"),
    'BUILDTEST_RUN_DIR': type("str"),
}

def check_configuration():
    """Checks all keys in configuration file (settings.yml) are valid
    keys and ensure value of each key matches expected type . For some keys
    special logic is taken to ensure values are correct and directory path
    exists.

    Also check if module command is found.

    If any error is found buildtest will terminate immediately.
    :return: returns gracefully if all checks passes otherwise terminate immediately
    :rtype: exit code 1 if checks failed
    """


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

        if key == "BUILDTEST_MODULEPATH":
            if config_opts["BUILDTEST_MODULEPATH"] == None:
                print("Please specify a module tree to BUILDTEST_MODULEPATH"
                     + f"in configuration {BUILDTEST_CONFIG_FILE}")
            else:
                for module_root in config_opts[key]:
                    if not os.path.isdir(module_root):
                        print (f"{module_root} directory does not exist"
                               + " specified in BUILDTEST_MODULEPATH")
                        ec = 1

        if key == "BUILDTEST_SPIDER_VIEW":
            if config_opts["BUILDTEST_SPIDER_VIEW"] not in ["all","current"]:
                print (f"BUILDTEST_SPIDER_VIEW must be one of the following: all, current")
                ec = 1


        if key == "BUILDTEST_PARENT_MODULE_SEARCH":
            if config_opts["BUILDTEST_PARENT_MODULE_SEARCH"] not in ["first","all"]:
                print(
                    f"BUILDTEST_PARENT_MODULE_SEARCH must be one of the "
                    f"following: first, all")
                ec = 1


        if key in config_directory_types:

            # expand variables for directory configuration
            config_opts[key] = os.path.expandvars(config_opts[key])

            # create the directory if it doesn't exist
            if not os.path.isdir(config_opts[key]):
                os.makedirs(config_opts[key])

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



def show_configuration():
    """This method display buildtest configuration to terminal and this
    implements command buildtest show --config.
    """
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

        if key == "BUILDTEST_MODULEPATH":
            tree = ""
            for mod_tree in config_opts[key]:
                tree += mod_tree + ":"

            # remove last colon
            tree = tree[:-1]
            print ((key + "\t " + type + " =").expandtabs(50), tree)
        else:
            print ((key + "\t " + type + " =").expandtabs(50), config_opts[key])

