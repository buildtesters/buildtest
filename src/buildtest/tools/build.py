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

import os
import shutil
import subprocess
import yaml

from buildtest.tools.config import config_opts
from buildtest.tools.modulesystem.collection import get_buildtest_module_collection
from buildtest.tools.buildsystem.singlesource import \
    BuildTestBuilderSingleSource
from buildtest.tools.file import create_dir, is_dir, walk_tree
from buildtest.tools.log import init_log
from buildtest.tools.modules import find_modules
from buildtest.tools.testconfigs import test_config_name_mapping
from buildtest.test.binarytest import generate_binary_test



def func_build_subcmd(args):
    """Entry point for buildtest build sub-command. Depending on the command
    arguments, buildtest will set values in dictionary config_opts that is used
    to trigger the appropriate build action.

    :param args: arguments passed from command line
    :type args: dictionary, required

    :rtype: None
    """

    logger,logpath,logfile = init_log()


    if args.shell:
        config_opts['BUILDTEST_SHELL']=args.shell
    if args.clean_build:
        config_opts['BUILDTEST_CLEAN_BUILD']=True
    if args.testdir:
        config_opts['BUILDTEST_TESTDIR'] = args.testdir
    if args.binary:
        config_opts["BUILDTEST_BINARY"] = args.binary
    if args.parent_module_search:
        config_opts["BUILDTEST_PARENT_MODULE_SEARCH"]=args.parent_module_search

    logdir = config_opts['BUILDTEST_LOGDIR']
    testdir = config_opts['BUILDTEST_TESTDIR']

    create_dir(logdir)
    create_dir(testdir)

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
        test_suite_dir = os.path.join(testdir,"suite",args.suite)
        create_dir(test_suite_dir)
        yaml_dir = os.path.join(config_opts["BUILDTEST_CONFIGS_REPO"],
                                "buildtest","suite",args.suite)

        yaml_files = walk_tree(yaml_dir,".yml")

        if args.verbose >= 1:
            print (f"Found {len(yaml_files)} yml files from directory {yaml_dir}")

        if config_opts["BUILDTEST_CLEAN_BUILD"]:
            if is_dir(test_suite_dir):
                shutil.rmtree(test_suite_dir)
                if args.verbose >= 1:
                    print (f"Removing test directory: {test_suite_dir}")

        testsuite_components = os.listdir(yaml_dir)
        # pre-creates directories for each component in test suite in
        # BUILDTEST_TESTDIR
        for component in testsuite_components:
            component_dir = os.path.join(testdir,"suite",args.suite,component)
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
                                                       module_cmd_list)
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
                                                   module_cmd_list)
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
            # for every loaded module generate binary test
            for package in out:
                generate_binary_test(package, args.verbose, "software")

    if args.package:
        func_build_system(args, logger, logpath, logfile)



def func_build_system(args, logger, logpath, logfile):
    """ This method implements details for "buildtest build --package" and
        invokes method "generate_binary_test" to get all the binaries and
        write the test scripts in BUILDTEST_TESTDIR.

        :param args: dictionary of command line arguments
        :type args: dictionary, required
        :param logger:  instance of logger class for writing logs to logfile
        :type logpath: class object, required
        :param logpath: full path to logfile
        :type logpath: string, required
        :param logfile: log file name
        :type logfile: string, required

        :rtype: None
    """

    system_logdir = os.path.join(config_opts["BUILDTEST_LOGDIR"],"system",args.package)

    generate_binary_test(args.package,args.verbose,"systempackage")

    create_dir(system_logdir)
    logger.warning("Creating directory %s , to write log file", system_logdir)

    destpath = os.path.join(system_logdir,logfile)
    os.rename(logpath, destpath)

    if args.verbose >= 1:
        print (f"Creating Log Directory: {system_logdir}")
        print (f"Renaming Log file {logpath} --> {destpath}")

    logger.info("Moving log file from %s to %s", logpath, destpath)

    print("Writing Log file to: ", destpath)