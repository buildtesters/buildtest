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
buildtest build subcommand methods

:author: Shahzeb Siddqiui
"""
import os
import sys


from buildtest.tools.config import config_opts
from buildtest.tools.file import create_dir
from buildtest.tools.log import init_log
from buildtest.tools.software import get_software_stack
from buildtest.test.function import clean_tests
from buildtest.test.binarytest import generate_binary_test
from buildtest.test.job import update_job_template
from buildtest.test.perl import build_perl_package_test
from buildtest.test.python import build_python_test
from buildtest.test.r import build_r_package_test
from buildtest.test.ruby import build_ruby_package_test
from buildtest.test.sourcetest import recursive_gen_test
from buildtest.tools.cmake import setup_software_cmake
from buildtest.tools.easybuild import is_easybuild_app
from buildtest.tools.utility import get_appname, get_appversion, get_toolchain_name, get_toolchain_version

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
    if args.ignore_easybuild:
        config_opts["BUILDTEST_IGNORE_EASYBUILD"]=True
    if args.enable_job:
        config_opts['BUILDTEST_ENABLE_JOB']=True
    if args.module_naming_scheme:
        config_opts['BUILDTEST_MODULE_NAMING_SCHEME'] = args.module_naming_scheme
    if args.job_template:
        update_job_template(args.job_template)


    logdir = config_opts['BUILDTEST_LOGDIR']
    testdir = config_opts['BUILDTEST_TESTDIR']

    create_dir(logdir)
    create_dir(testdir)

    if args.all_package:
        packages = os.listdir(os.path.join(config_opts['BUILDTEST_CONFIGS_REPO'],"buildtest","system"))
        for pkg in packages:
            generate_binary_test(pkg,"systempackage")

    if args.all_software:
        app_list = get_software_stack()
        for app in app_list:
            config_opts["BUILDTEST_SOFTWARE"] = app
            config_opts["BUILDTEST_TOOLCHAIN"] = None
            generate_binary_test(app,"software")

    if args.package:
        func_build_system(args.package, logger, logdir, logpath, logfile)
    elif args.software:
        func_build_software(args, logger, logdir, logpath, logfile)

    sys.exit(0)

def func_build_system(systempkg, logger, logdir, logpath, logfile):
    """ method implementation for "_buildtest build --system" """

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
    """ implementation for "buildtest build -s " """

    config_opts["BUILDTEST_SOFTWARE"] = args.software
    config_opts["BUILDTEST_TOOLCHAIN"] = args.toolchain

    appname=get_appname()
    appversion=get_appversion()
    tcname = get_toolchain_name()
    tcversion = get_toolchain_version()

    print("Detecting Software: ", os.path.join(appname,appversion))

    logger.debug("Generating Test from EB Application")

    logger.debug("Software: %s", appname)
    logger.debug("Software Version: %s", appversion)
    logger.debug("Toolchain: %s", tcname)
    logger.debug("Toolchain Version: %s", tcversion)

    logger.debug("Checking if software: %s/%s exists",appname,appversion)


    # check if software is an easybuild applicationa
    if config_opts["BUILDTEST_IGNORE_EASYBUILD"] == False:
        is_easybuild_app()

    logdir=os.path.join(logdir,appname,appversion,tcname,tcversion)

    # if directory tree for software log is not present, create the directory
    create_dir(logdir)

    setup_software_cmake()

    generate_binary_test(args.software,"software")

    source_app_dir=os.path.join(config_opts['BUILDTEST_CONFIGS_REPO'],"buildtest/source",appname.lower())
    configdir=os.path.join(source_app_dir,"config")
    codedir=os.path.join(source_app_dir,"code")

    logger.debug("Source App Directory: %s",  source_app_dir)
    logger.debug("Config Directory: %s ", configdir)
    logger.debug("Code Directory: %s", codedir)


    # this generates all the compilation tests found in application directory ($BUILDTEST_CONFIGS_REPO/ebapps/<software>)
    recursive_gen_test(configdir,codedir)

    if args.python_package:
        build_python_test(args.python_package)

    if args.r_package:
        build_r_package_test(args.r_package)

    if args.ruby_package:
        build_ruby_package_test(args.ruby_package)

    if args.perl_package:
        build_perl_package_test(args.perl_package)

    # moving log file from $BUILDTEST_LOGDIR/buildtest_%H_%M_%d_%m_%Y.log to $BUILDTEST_LOGDIR/app/appver/tcname/tcver/buildtest_%H_%M_%d_%m_%Y.log
    os.rename(logpath, os.path.join(logdir,logfile))
    logger.debug("Writing Log file to %s", os.path.join(logdir,logfile))

    print ("Writing Log file: ", os.path.join(logdir,logfile))
