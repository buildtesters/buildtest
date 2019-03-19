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
for building test scripts from yaml configuration.
"""


import os
import shutil
import sys
import stat
import subprocess
import yaml

from buildtest.tools.config import config_opts
from buildtest.tools.file import create_dir, is_dir, walk_tree
from buildtest.tools.log import init_log
from buildtest.test.binarytest import generate_binary_test
from buildtest.tools.cmake import setup_software_cmake
from buildtest.tools.easybuild import is_easybuild_app
from buildtest.tools.ohpc import check_ohpc
from buildtest.tools.utility import get_appname, get_appversion
from buildtest.tools.yaml import BuildTestYamlSingleSource
from buildtest.tools.system import BuildTestCommand


def func_build_subcmd(args):
    """ Entry point for build sub-command. The args variable is a list of
        options passed through command line. Each option is checked and
        appropriate action is taken in this method or calls another method. """

    logger,logpath,logfile = init_log()


    if args.shell:
        config_opts['BUILDTEST_SHELL']=args.shell
    if args.clean_tests:
        clean_tests()

    if args.clean_build:
        config_opts['BUILDTEST_CLEAN_BUILD']=True
    if args.testdir:
        config_opts['BUILDTEST_TESTDIR'] = args.testdir
    if args.easybuild:
        config_opts["BUILDTEST_EASYBUILD"]=True
    if args.prepend_modules:
        config_opts["BUILDTEST_PREPEND_MODULES"] = args.prepend_modules
    if args.binary:
        config_opts["BUILDTEST_BINARY"] = args.binary


    if args.ohpc:
        check_ohpc()
        config_opts["BUILDTEST_OHPC"] = True

    logdir = config_opts['BUILDTEST_LOGDIR']
    testdir = config_opts['BUILDTEST_TESTDIR']

    create_dir(logdir)
    create_dir(testdir)

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
            content = yaml.load(fd)

            if args.verbose >= 2:
                print (f"Loading Yaml Content from file: {file}")
            if content["testblock"] == "singlesource":
                builder = BuildTestBuilderSingleSource(file,
                                                       args,
                                                       parent_dir)

                builder.build()

    if args.package:
        func_build_system(args.package, logger, logdir, logpath, logfile)
    elif args.software:
        func_build_software(args, logger, logdir, logpath, logfile)

    sys.exit(0)

class BuildTestBuilderSingleSource():
    """ Class responsible for building a single source test."""
    yaml_dict = {}
    test_dict = {}
    def __init__(self,yaml,args,parent_dir):
        """ Entry point to class. This method will set all class variables.

            :param yaml: The yaml file to be processed
            :param test_suite: Name of the test suite (buildtest build -S <suite>)
            :param parent_dir: parent directory where test script will be written
            :param software_module: Name of software module to write in test script.
        """
        self.shell = config_opts["BUILDTEST_SHELL"]
        self.yaml = yaml
        self.testname = '%s.%s' % (os.path.basename(self.yaml),self.shell)
        self.test_suite = args.suite
        self.parent_dir = parent_dir
        yaml_parser = BuildTestYamlSingleSource(self.yaml,args,self.shell)
        self.yaml_dict, self.test_dict = yaml_parser.parse()
        self.verbose = args.verbose
    def build(self):
        """ Logic to build the test script.

            This class will invoke class BuildTestYamlSingleSource to return a
            dictionary that will contain all the information required to write
            the test script.

            This method will write the test script with one of the shell
            extensions (.bash, .csh, .sh) depending on what shell was requested.

            For a job script the shell extension .lsf or .slurm will be inserted.
            The test script will be set with 755 permission upon completion.

        """

        # if this is a LSF job script then create .lsf extension for testname
        if "lsf" in self.test_dict:
            self.testname = '%s.%s' % (os.path.basename(self.yaml),"lsf")
        # if this is a slurm job script then create .lsf extension for testname
        if "slurm" in self.test_dict:
            self.testname = '%s.%s' % (os.path.basename(self.yaml),"slurm")

        test_dir  = os.path.join(config_opts["BUILDTEST_TESTDIR"],"suite",self.test_suite,self.parent_dir)


        abs_test_path = os.path.join(test_dir,self.testname)
        print(f'Writing Test: {abs_test_path}')
        fd = open(abs_test_path, "w")

        # return the shell path i.e #!/bin/bash, #!/bin/sh
        shell_path = BuildTestCommand().which(self.shell)[0]

        fd.write(f'#!{shell_path}')

        if "lsf" in self.test_dict:
            fd.write(self.test_dict["lsf"])
        if "slurm" in self.test_dict:
            fd.write(self.test_dict["slurm"])

        fd.write(self.test_dict["module"])

        if "vars" in self.test_dict:
            fd.write(self.test_dict["vars"])

        fd.write(self.test_dict["workdir"])
        [ fd.write(k + " ") for k in self.test_dict["command"] ]
        fd.write("\n")

        if "run" in self.test_dict:
            fd.write(self.test_dict["run"])
            fd.write(self.test_dict["post_run"])

        fd.close()
        # setting perm to 755 on testscript
        os.chmod(abs_test_path, stat.S_IRWXU |  stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH |  stat.S_IXOTH)

        if self.verbose >= 1:
            print (f"Changing permission to 755 for test: {abs_test_path}")

        if self.verbose >= 2:
            test_output = subprocess.getoutput(f"cat {abs_test_path}").splitlines()
            print ("{:_<80}".format(""))
            for line in test_output:
                print (line)
            print ("{:_<80}".format(""))

def func_build_system(systempkg, logger, logdir, logpath, logfile):
    """ This method implements details for "buildtest build --package" and
        invokes method "generate_binary_test" to get all the binary tests and
        write them in the appropriate location.


       :param systempkg: Name of the system package
       :param logger:
       :param logdir:
       :param logpath:
       :param logfile:

    """

    system_logdir = os.path.join(logdir,"system",systempkg)
    #setup_system_cmake()
    generate_binary_test(systempkg,"systempackage")

    create_dir(system_logdir)
    logger.warning("Creating directory %s , to write log file", system_logdir)

    destpath = os.path.join(system_logdir,logfile)
    os.rename(logpath, destpath)
    logger.info("Moving log file from %s to %s", logpath, destpath)

    print("Writing Log file to: ", destpath)


def func_build_software(args, logger, logdir, logpath, logfile):
    """ This method implements option "buildtest build -s" which is
        used for building binary test for software modules.

        :param args:
        :param logger:
        :param logdir:
        :param logpath:
        :param logfile:

    """

    config_opts["BUILDTEST_SOFTWARE"] = args.software


    appname=get_appname()
    appversion=get_appversion()

    print("Detecting Software: ", os.path.join(appname,appversion))

    logger.debug("Generating Test from Application")

    logger.debug("Software: %s", appname)
    logger.debug("Software Version: %s", appversion)


    # check if software is an easybuild applicationa
    if config_opts["BUILDTEST_EASYBUILD"] == True:
        is_easybuild_app()

    logdir=os.path.join(logdir,appname,appversion)

    # if directory tree for software log is not present, create the directory
    create_dir(logdir)

    setup_software_cmake()
    if config_opts["BUILDTEST_BINARY"]:
        generate_binary_test(args.software,"software")

    # moving log file from $BUILDTEST_LOGDIR/buildtest_%H_%M_%d_%m_%Y.log to $BUILDTEST_LOGDIR/app/appver/tcname/tcver/buildtest_%H_%M_%d_%m_%Y.log
    os.rename(logpath, os.path.join(logdir,logfile))
    logger.debug("Writing Log file to %s", os.path.join(logdir,logfile))

    print ("Writing Log file: ", os.path.join(logdir,logfile))

def clean_tests():
    """ cleans all the tests in BUILDTEST_TESTDIR.
        This implements "buildtest build --clean-tests" """
    try:
        shutil.rmtree(config_opts['BUILDTEST_TESTDIR'])
        print (f"Removing test directory {config_opts['BUILDTEST_TESTDIR']}")
    except OSError as err_msg:
        print(err_msg)

