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
import json

sys.path.insert(0,os.path.abspath('.'))
os.environ["BUILDTEST_ROOT"]=os.path.dirname(os.path.dirname(__file__))
os.environ["BUILDTEST_JOB_TEMPLATE"]=os.path.join(os.getenv("BUILDTEST_ROOT"),"template/job.slurm")
# column width for linewrap for argparse library
os.environ['COLUMNS'] = "120"

from buildtest.tools.menu import buildtest_menu


from buildtest.test.job import submit_job_to_scheduler, update_job_template
from buildtest.test.run import run_test_buildtest
from buildtest.tools.config import show_configuration, config_opts
from buildtest.tools.find import find_all_yaml_configs, find_yaml_configs_by_arg
from buildtest.tools.find import find_all_tests, find_tests_by_arg
from buildtest.tools.easybuild import find_easyconfigs, is_easybuild_app
from buildtest.tools.generate_yaml import create_system_yaml, create_software_yaml
from buildtest.tools.log import clean_logs

from buildtest.tools.modules import diff_trees, module_load_test
from buildtest.tools.parser.yaml_config import show_yaml_keys
from buildtest.tools.scan import scantest
from buildtest.tools.system import get_system_info
from buildtest.tools.version import buildtest_version
from buildtest.runtest import runtest_menu

def main():
    """ entry point to buildtest """


    config_opts["BUILDTEST_IGNORE_EASYBUILD"]=False

    BUILDTEST_CONFIGS_REPO = config_opts['BUILDTEST_CONFIGS_REPO']
    parser = buildtest_menu()

    bt_opts = parser.parse_options()

    if config_opts.get('BUILDTEST_IGNORE_EASYBUILD'):
        BUILDTEST_IGNORE_EASYBUILD=config_opts['BUILDTEST_IGNORE_EASYBUILD']

    if bt_opts.version:
        buildtest_version()

    if bt_opts.show:
        show_configuration()

    if bt_opts.show_keys:
        show_yaml_keys()

    if bt_opts.logdir:
        config_opts['BUILDTEST_LOGDIR'] = bt_opts.logdir

    if bt_opts.ignore_easybuild:
        config["BUILDTEST_IGNORE_EASYBUILD"]=True

    if bt_opts.enable_job:
        config_opts['BUILDTEST_ENABLE_JOB']=True

    if bt_opts.clean_logs:
        clean_logs()

    if bt_opts.module_naming_scheme:
        config_opts['BUILDTEST_MODULE_NAMING_SCHEME'] = bt_opts.module_naming_scheme

    if bt_opts.runtest:
        runtest_menu()

    if bt_opts.scantest:
        scantest()

    if bt_opts.easyconfigs:
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

    if bt_opts.run:
        run_test_buildtest(bt_opts.run)

    if bt_opts.job_template is not None:
        update_job_template(bt_opts.job_template)

    if bt_opts.submitjob is not None:
        submit_job_to_scheduler(bt_opts.submitjob)
        sys.exit(0)

    if bt_opts.sysyaml is not None:
        create_system_yaml(bt_opts.sysyaml)

    if bt_opts.ebyaml != None:
        create_software_yaml(bt_opts.ebyaml)


    get_system_info()


if __name__ == "__main__":
        main()
