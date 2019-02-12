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
buildtest build subcommand methods
"""
import os
import sys
import stat

from buildtest.tools.config import config_opts
from buildtest.tools.file import create_dir
from buildtest.tools.log import init_log
from buildtest.tools.software import get_software_stack
from buildtest.test.function import clean_tests
from buildtest.test.binarytest import generate_binary_test
from buildtest.test.job import update_job_template
from buildtest.test.sourcetest import recursive_gen_test
from buildtest.tools.cmake import setup_software_cmake
from buildtest.tools.easybuild import is_easybuild_app
from buildtest.tools.ohpc import check_ohpc
from buildtest.tools.utility import get_appname, get_appversion, get_toolchain_name, get_toolchain_version
from buildtest.tools.yaml import BuildTestYaml, get_all_yaml_files
from buildtest.tools.system import BuildTestCommand

def func_build_subcmd(args):
    """ entry point for build subcommand """
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
    if args.enable_job:
        config_opts['BUILDTEST_ENABLE_JOB']=True
    if args.module_naming_scheme:
        config_opts['BUILDTEST_MODULE_NAMING_SCHEME'] = args.module_naming_scheme
    if args.job_template:
        update_job_template(args.job_template)
    if args.prepend_modules:
        config_opts["BUILDTEST_PREPEND_MODULES"]   = args.prepend_modules
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
        create_dir(os.path.join(testdir,"suite",args.suite))
        yaml_dir = os.path.join(config_opts["BUILDTEST_CONFIGS_REPO"], "buildtest","suite",args.suite)
        yaml_files = get_all_yaml_files(yaml_dir)

        testsuite_components = os.listdir(yaml_dir)
        # precreate direcorties for each component for test suite in BUILDTEST_TESTDIR
        for component in testsuite_components:
            create_dir(os.path.join(testdir,"suite",args.suite,component))

        for file in yaml_files:
            parent_dir = os.path.basename(os.path.dirname(file))
            #print (parent_dir, file)
            builder = BuildTestBuilder(file,args.suite, parent_dir)
            builder.build()

    if args.conf:
        pass
        #builder = BuildTestBuilder(args.conf,args.suite)
        #builder.build()

    if args.package:
        func_build_system(args.package, logger, logdir, logpath, logfile)
    elif args.software:
        func_build_software(args, logger, logdir, logpath, logfile)

    sys.exit(0)

def func_build_system(systempkg, logger, logdir, logpath, logfile):
    """ method implementation for "buildtest build --package" """

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
    """implementation for "buildtest build -s " """

    config_opts["BUILDTEST_SOFTWARE"] = args.software
    config_opts["BUILDTEST_TOOLCHAIN"] = args.toolchain

    appname=get_appname()
    appversion=get_appversion()
    tcname = get_toolchain_name()
    tcversion = get_toolchain_version()

    print("Detecting Software: ", os.path.join(appname,appversion))

    logger.debug("Generating Test from Application")

    logger.debug("Software: %s", appname)
    logger.debug("Software Version: %s", appversion)
    logger.debug("Toolchain: %s", tcname)
    logger.debug("Toolchain Version: %s", tcversion)

    logger.debug("Checking if software: %s/%s exists",appname,appversion)


    # check if software is an easybuild applicationa
    if config_opts["BUILDTEST_EASYBUILD"] == True:
        is_easybuild_app()

    logdir=os.path.join(logdir,appname,appversion,tcname,tcversion)

    # if directory tree for software log is not present, create the directory
    create_dir(logdir)

    setup_software_cmake()
    if config_opts["BUILDTEST_BINARY"]:
        generate_binary_test(args.software,"software")

    source_app_dir=os.path.join(config_opts['BUILDTEST_CONFIGS_REPO'],"buildtest/source",appname.lower())
    configdir=os.path.join(source_app_dir,"config")
    codedir=os.path.join(source_app_dir,"code")

    logger.debug("Source App Directory: %s",  source_app_dir)
    logger.debug("Config Directory: %s ", configdir)
    logger.debug("Code Directory: %s", codedir)


    # this generates all the compilation tests found in application directory ($BUILDTEST_CONFIGS_REPO/ebapps/<software>)
    recursive_gen_test(configdir,codedir)

    # moving log file from $BUILDTEST_LOGDIR/buildtest_%H_%M_%d_%m_%Y.log to $BUILDTEST_LOGDIR/app/appver/tcname/tcver/buildtest_%H_%M_%d_%m_%Y.log
    os.rename(logpath, os.path.join(logdir,logfile))
    logger.debug("Writing Log file to %s", os.path.join(logdir,logfile))

    print ("Writing Log file: ", os.path.join(logdir,logfile))

class BuildTestBuilder():
    """ class responsible for building a test"""
    yaml_dict = {}
    test_dict = {}
    def __init__(self,yaml,test_suite,parent_dir):
        self.testdir = config_opts["BUILDTEST_TESTDIR"]
        self.shell = config_opts["BUILDTEST_SHELL"]
        yaml_dict = BuildTestYaml(yaml,test_suite,self.shell)
        self.yaml_dict, self.test_dict = yaml_dict.parse()
        self.testname = '%s.%s' % (os.path.basename(yaml),self.shell)
        #self.testname = self.yaml_dict["name"] + "." + self.shell
        self.test_suite = test_suite
        self.parent_dir = parent_dir
    def build(self):
        """ logic to build the test script"""

        test_dir  = os.path.join(config_opts["BUILDTEST_TESTDIR"],"suite",self.test_suite,self.parent_dir)


        abs_test_path = os.path.join(test_dir,self.testname)
        print("Writing Test: " + abs_test_path)
        fd = open(abs_test_path, "w")

        shell_path = BuildTestCommand().which(self.shell)[0]

        fd.write("#!" + shell_path)

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
        fd.write(self.test_dict["run"])
        fd.write(self.test_dict["post_run"])

        # setting perm to 755 on testscript
        os.chmod(abs_test_path, stat.S_IRWXU |  stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH |  stat.S_IXOTH)
