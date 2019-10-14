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

"""
This module contains all the methods related to "buildtest build" which is used
for building test scripts from test configuration.
"""

from datetime import datetime
import json
import os
import shutil
import subprocess
import sys
import yaml

from buildtest.tools.config import config_opts, BUILDTEST_BUILD_HISTORY, BUILDTEST_BUILD_LOGFILE,BUILDTEST_SYSTEM
from buildtest.tools.modulesystem.collection import get_buildtest_module_collection
from buildtest.tools.buildsystem.singlesource import BuildTestBuilderSingleSource
from buildtest.tools.buildsystem.binarytest import generate_binary_test
from buildtest.tools.file import create_dir, is_dir, walk_tree, is_file
from buildtest.tools.log import init_log
from buildtest.tools.modules import find_modules
from buildtest.tools.buildsystem.status import get_total_build_ids
from buildtest.tools.testconfigs import test_config_name_mapping




def func_build_subcmd(args):
    """Entry point for ``buildtest build`` sub-command. Depending on the command
    arguments, buildtest will set values in dictionary config_opts that is used
    to trigger the appropriate build action.

    :param args: arguments passed from command line
    :type args: dict, required

    :rtype: None
    """

    logger,logfile = init_log()

    build_id = get_total_build_ids()
    BUILDTEST_BUILD_HISTORY[build_id] = {}
    BUILDTEST_BUILD_HISTORY[build_id]["TESTS"] = []
    if args.clear:
        if is_file(BUILDTEST_BUILD_LOGFILE):
            os.remove(BUILDTEST_BUILD_LOGFILE)
            shutil.rmtree(config_opts["BUILDTEST_TESTDIR"])
        print ("Clearing Build History")
        sys.exit(0)
    if args.shell:
        config_opts['BUILDTEST_SHELL']=args.shell

    if args.binary:
        config_opts["BUILDTEST_BINARY"] = args.binary
    if args.parent_module_search:
        config_opts["BUILDTEST_PARENT_MODULE_SEARCH"]=args.parent_module_search

    system = json.load(open(BUILDTEST_SYSTEM, "r"))
    test_subdir = os.path.join(system["VENDOR"],
                               system["ARCH"],
                               system["PROCESSOR_FAMILY"],
                               system["OS_NAME"],
                               system["OS_VERSION"],
                               f"build_{str(build_id)}")

    config_opts['BUILDTEST_TESTDIR'] = os.path.join(config_opts['BUILDTEST_TESTDIR'],test_subdir)
    create_dir(config_opts['BUILDTEST_TESTDIR'])

    module_cmd_list = []
    # if module permutation is set
    if args.modules:
        module_cmd_list = find_modules(args.modules)


        print("Module Permutation Detected.")
        print(f"Each test will be built with {len(module_cmd_list)} "
              f"module permutations")

        print("Module Permutation List")
        print ("{:_<50}".format(""))
        [print(x) for x in module_cmd_list]

    #when -mc is specified, get module load command from internal module
    # collection
    if args.module_collection is not None:
        mod_coll= get_buildtest_module_collection(args.module_collection)
        mod_str= ' '.join(str(mod) for mod in mod_coll)
        mod_str = f"module load {mod_str}"

    if args.suite:
        test_suite_dir = os.path.join(config_opts['BUILDTEST_TESTDIR'],"suite",args.suite)
        create_dir(test_suite_dir)
        yaml_dir = os.path.join(config_opts["BUILDTEST_CONFIGS_REPO"],
                                "buildtest","suite",args.suite)

        yaml_files = walk_tree(yaml_dir,".yml")

        if args.verbose >= 1:
            print (f"Found {len(yaml_files)} yml files from directory {yaml_dir}")

        testsuite_components = os.listdir(yaml_dir)
        # pre-creates directories for each component in test suite in
        # BUILDTEST_TESTDIR
        for component in testsuite_components:
            component_dir = os.path.join(config_opts['BUILDTEST_TESTDIR'],
                                         "suite",
                                         args.suite,
                                         component)
            create_dir(component_dir)
            if args.verbose >= 2:
                print (f"Creating Directory {component_dir}")

        for file in yaml_files:
            parent_dir = os.path.basename(os.path.dirname(file))
            fd=open(file,'r')
            content = yaml.safe_load(fd)
            fd.close()
            if args.verbose >= 2:
                print (f"Loading Yaml Content from file: {file}")
            if content["testblock"] == "singlesource":
                builder = BuildTestBuilderSingleSource(file,
                                                       args,
                                                       parent_dir,
                                                       module_cmd_list,
                                                       build_id)
                if len(module_cmd_list) > 0:
                    builder.build(modules_permutation=True)
                elif args.collection:
                    builder.build(module_collection=args.collection)
                else:
                    builder.build()

    if args.config:
        test_config_table = test_config_name_mapping()
        file = test_config_table[args.config]
        #file = args.config
        parent_dir = os.path.basename(os.path.dirname(file))
        args.suite = os.path.basename(os.path.dirname(os.path.dirname(file)))
        fd = open(file,'r')
        content = yaml.safe_load(fd)
        fd.close()

        if content["testblock"] == "singlesource":
            builder = BuildTestBuilderSingleSource(file,
                                                   args,
                                                   parent_dir,
                                                   module_cmd_list,
                                                   build_id)
            # if test needs to be built with module permutation
            if len(module_cmd_list) > 0:
                builder.build(modules_permutation=True)
            elif args.collection:
                builder.build(module_collection=args.collection)
            elif args.module_collection is not None:
                builder.build(internal_module_collection=mod_str)
            else:
                builder.build()

    # if binary test is True then generate binary test for all loaded modules
    if config_opts["BUILDTEST_BINARY"]:
        cmd = "module -t list"
        out = subprocess.getoutput(cmd)
        # output of module -t list when no modules are loaded is "No modules
        #  loaded"
        if out != "No modules loaded":
            out = out.split()
            logger.info(f"Active Modules: {out}")
            # for every loaded module generate binary test
            for module_name in out:
                generate_binary_test(module_name, args.verbose, build_id, module=True)
        else:
            print("No modules loaded, please load modules and try again.")
            sys.exit(0)

    if args.package:
        generate_binary_test(args.package, args.verbose, build_id, package=True)

    print("Writing Log file to: ", logfile)

    BUILD_TIME = datetime.now().strftime("%m/%d/%Y %X")
    BUILDTEST_BUILD_HISTORY[build_id]["TESTCOUNT"] = len(os.listdir(config_opts["BUILDTEST_TESTDIR"]))
    BUILDTEST_BUILD_HISTORY[build_id]["CMD"] = "buildtest " + ' '.join(str(arg) for arg in sys.argv[1:])

    BUILDTEST_BUILD_HISTORY[build_id]["BUILD_TIME"] = BUILD_TIME
    BUILDTEST_BUILD_HISTORY[build_id]["LOGFILE"] = logfile
    fd = open(BUILDTEST_BUILD_LOGFILE,"r")
    build_dict = json.load(fd)
    fd.close()
    build_dict["build"][build_id] = BUILDTEST_BUILD_HISTORY[build_id]

    fd = open(BUILDTEST_BUILD_LOGFILE, "w")
    json.dump(build_dict, fd, indent=4)
    fd.close()
