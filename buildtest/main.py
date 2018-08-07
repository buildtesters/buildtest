#!/usr/bin/env python
############################################################################
#
#  Copyright 2017-2018
#
#   https://github.com/HPC-buildtest/buildtest-framework
#
#    This file is part of buildtest.
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
The entry point to buildtest

:author: Shahzeb Siddiqui (Pfizer)
"""

import sys
import os
import subprocess
import argparse
import glob
#sys.path.insert(0,os.path.abspath('.'))

sys.path.insert(0,os.path.abspath('.'))


os.environ["BUILDTEST_ROOT"]=os.path.dirname(os.path.dirname(__file__))
os.environ["BUILDTEST_JOB_TEMPLATE"]=os.path.join(os.environ.get("BUILDTEST_ROOT"),"template/job.slurm")

from buildtest.test.binarytest import generate_binary_test
from buildtest.test.function import clean_tests
from buildtest.test.job import submit_job_to_scheduler, update_job_template
from buildtest.test.python import build_python_test
from buildtest.test.r import build_r_package_test
from buildtest.test.ruby import build_ruby_package_test
from buildtest.test.perl import build_perl_package_test
from buildtest.test.sourcetest import recursive_gen_test
from buildtest.tools.cmake import setup_software_cmake
from buildtest.tools.config import show_configuration, config_opts
from buildtest.tools.file import create_dir
from buildtest.tools.find import find_all_yaml_configs, find_yaml_configs_by_arg
from buildtest.tools.find import find_all_tests, find_tests_by_arg
from buildtest.tools.easybuild import list_toolchain, find_easyconfigs, is_easybuild_app
from buildtest.tools.generate_yaml import create_system_yaml, create_software_yaml
from buildtest.tools.log import init_log, clean_logs
from buildtest.tools.menu import buildtest_menu
from buildtest.tools.modules import diff_trees, module_load_test
from buildtest.tools.parser.yaml_config import show_yaml_keys
from buildtest.tools.print_functions import print_software_version_relation, print_software, print_toolchain
from buildtest.tools.scan import scantest
from buildtest.tools.software import get_unique_software, software_version_relation
from buildtest.tools.system import get_system_info
from buildtest.tools.utility import get_appname, get_appversion, get_toolchain_name, get_toolchain_version
from buildtest.tools.version import buildtest_version
from buildtest.runtest import runtest_menu

# column width for linewrap for argparse library
os.environ['COLUMNS'] = "120"

def main():
    """ entry point to buildtest """

    BUILDTEST_IGNORE_EASYBUILD=False

    BUILDTEST_CONFIGS_REPO = config_opts['BUILDTEST_CONFIGS_REPO']
    parser = buildtest_menu()
    bt_opts = parser.parse_options()

    if config_opts.get('BUILDTEST_IGNORE_EASYBUILD'):
        BUILDTEST_IGNORE_EASYBUILD=config_opts['BUILDTEST_IGNORE_EASYBUILD']

    if bt_opts.version:
        buildtest_version()
        sys.exit(0)

    if bt_opts.show:
        show_configuration()

    if bt_opts.show_keys:
        show_yaml_keys()

    if bt_opts.logdir:
        config_opts['BUILDTEST_LOGDIR'] = bt_opts.logdir

    if bt_opts.testdir:
         config_opts['BUILDTEST_TESTDIR'] = bt_opts.testdir

    if bt_opts.ignore_easybuild:
        BUILDTEST_IGNORE_EASYBUILD=True

    if bt_opts.clean_build:
        config_opts['BUILDTEST_CLEAN_BUILD']=True

    if bt_opts.enable_job:
        config_opts['BUILDTEST_ENABLE_JOB']=True

    if bt_opts.clean_logs:
        clean_logs()

    if bt_opts.clean_tests:
        clean_tests()

    if bt_opts.module_naming_scheme:
        config_opts['BUILDTEST_MODULE_NAMING_SCHEME'] = bt_opts.module_naming_scheme

    if bt_opts.runtest:
        runtest_menu()

    if bt_opts.scantest:
        scantest()



    if bt_opts.list_toolchain is True:
        toolchain_set=list_toolchain()
        print_toolchain(toolchain_set)
        sys.exit(0)

    if bt_opts.list_unique_software:
        software_set=get_unique_software()
        print_software(software_set)
        sys.exit(0)

    if bt_opts.software_version_relation:
        software_dict = software_version_relation()
        print_software_version_relation(software_dict)
        sys.exit(0)

    if bt_opts.easyconfigs_in_moduletrees:
        find_easyconfigs()
        sys.exit(0)

    if bt_opts.diff_trees:
        args_trees = bt_opts.diff_trees
        diff_trees(args_trees)
        sys.exit(0)

    # when no argument is specified to -fc then output all yaml files
    if bt_opts.findconfig == "all":
        find_all_yaml_configs()

    # find yaml configs by argument instead of reporting all yaml files
    elif bt_opts.findconfig is not None:
        find_yaml_configs_by_arg(bt_opts.findconfig)

	# report all buildtest generated test scripts
    if bt_opts.findtest == "all":
        find_all_tests()

    # find test by argument instead of all tests
    elif bt_opts.findtest is not None:
        find_tests_by_arg(bt_opts.findtest)


    if bt_opts.module_load_test:
        module_load_test()

    if bt_opts.shell:
         config_opts['BUILDTEST_SHELL']=bt_opts.shell

    if bt_opts.job_template is not None:
        update_job_template(bt_opts.job_template)

    if bt_opts.submitjob is not None:
        submit_job_to_scheduler(bt_opts.submitjob)
        sys.exit(0)

    if bt_opts.sysyaml is not None:
        create_system_yaml(bt_opts.sysyaml)

    if bt_opts.ebyaml != None:
        create_software_yaml(bt_opts.ebyaml)


    logger,logpath,logfile = init_log()
    BUILDTEST_LOGDIR = config_opts['BUILDTEST_LOGDIR']
    BUILDTEST_TESTDIR = config_opts['BUILDTEST_TESTDIR']

    create_dir(BUILDTEST_LOGDIR)
    create_dir(BUILDTEST_TESTDIR)

    cmd = "env | grep BUILDTEST"
    ret = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ret.communicate()[0]
    output = output.split("\n")

    for line in output:
        logger.debug(line)

    get_system_info()

    # generate system pkg test
    if bt_opts.system is not None:
        if bt_opts.system == "all":
            systempkg = bt_opts.system
            logger.info("Generating all system package tests from YAML files in %s", config_opts['BUILDTEST_CONFIGS_REPO_SYSTEM'])

            BUILDTEST_LOGDIR = os.path.join(BUILDTEST_LOGDIR,"system","all")
            systempkg_list = os.listdir(config_opts['BUILDTEST_CONFIGS_REPO_SYSTEM'])

            logger.info("List of system packages to test: %s ", systempkg_list)

            for pkg in systempkg_list:
                generate_binary_test(bt_opts,pkg)
        else:

            systempkg = bt_opts.system
            BUILDTEST_LOGDIR = os.path.join(BUILDTEST_LOGDIR,"system",systempkg)
            generate_binary_test(bt_opts,systempkg)

        create_dir(BUILDTEST_LOGDIR)
        logger.warning("Creating directory %s, to write log file", BUILDTEST_LOGDIR)

        destpath = os.path.join(BUILDTEST_LOGDIR,logfile)
        os.rename(logpath, destpath)
        logger.info("Moving log file from %s to %s", logpath, destpath)

        print "Writing Log file to:", destpath
        sys.exit(0)

	# when -s is specified
    if bt_opts.software is not None:
        software=bt_opts.software.split("/")

        if bt_opts.toolchain is None:
            toolchain="dummy/dummy".split("/")
        else:
            toolchain=bt_opts.toolchain.split("/")

        appname=get_appname()
        appversion=get_appversion()
        tcname = get_toolchain_name()
        tcversion = get_toolchain_version()

        print "Detecting Software: ", os.path.join(appname,appversion)

        logger.debug("Generating Test from EB Application")

        logger.debug("Software: %s", appname)
        logger.debug("Software Version: %s", appversion)
        logger.debug("Toolchain: %s", tcname)
        logger.debug("Toolchain Version: %s", tcversion)

        logger.debug("Checking if software: %s/%s exists",appname,appversion)


        # check if software is an easybuild applicationa
        if BUILDTEST_IGNORE_EASYBUILD == False:
            is_easybuild_app()

        source_app_dir=os.path.join(config_opts['BUILDTEST_CONFIGS_REPO_SOFTWARE'],appname.lower())
        configdir=os.path.join(source_app_dir,"config")
        codedir=os.path.join(source_app_dir,"code")
        BUILDTEST_LOGDIR=os.path.join(BUILDTEST_LOGDIR,appname,appversion,tcname,tcversion)

        # if directory tree for software log is not present, create the directory
        create_dir(BUILDTEST_LOGDIR)

        logger.debug("Source App Directory: %s",  source_app_dir)
        logger.debug("Config Directory: %s ", configdir)
        logger.debug("Code Directory: %s", codedir)

        setup_software_cmake()

        generate_binary_test(bt_opts,None)

        # this generates all the compilation tests found in application directory ($BUILDTEST_CONFIGS_REPO/ebapps/<software>)
        recursive_gen_test(configdir,codedir)

        if bt_opts.python_package:
            build_python_test(bt_opts.python_package)

        if bt_opts.r_package:
            build_r_package_test(bt_opts.r_package)

        if bt_opts.ruby_package:
            build_ruby_package_test(bt_opts.ruby_package)

        if bt_opts.perl_package:
            build_perl_package_test(bt_opts.perl_package)

        # moving log file from $BUILDTEST_LOGDIR/buildtest_%H_%M_%d_%m_%Y.log to $BUILDTEST_LOGDIR/app/appver/tcname/tcver/buildtest_%H_%M_%d_%m_%Y.log
        os.rename(logpath, os.path.join(BUILDTEST_LOGDIR,logfile))
        logger.debug("Writing Log file to %s", os.path.join(BUILDTEST_LOGDIR,logfile))

        print "Writing Log file: ", os.path.join(BUILDTEST_LOGDIR,logfile)

if __name__ == "__main__":
        main()
