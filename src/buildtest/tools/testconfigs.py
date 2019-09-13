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

import os, yaml, textwrap
from buildtest.tools.config import config_opts
from buildtest.tools.file import walk_tree
from buildtest.tools.system import BuildTestCommand


def testconfig_choices():
    """Return a list of test configuration used by options
    ``buildtest testconfigs view`` and ``buildtest testconfigs edit``

    :rtype: list
    """
    return test_config_name_mapping().keys()

def func_testconfigs_show(args):
    """ Prints all test configuration and description of test.

    This method implements ``buildtest testconfigs list``

    :param args: command line arguments to buildtest
    :type args: dict, required
    """
    test_config_table = test_config_name_mapping()
    print ('{:60} | {:<30}'.format("Test Configuration Name", "Description"))
    print('{:-<100}'.format(""))


    for config in test_config_table.items():
        tname = config[0]
        fname = config[1]

        fd = open(fname,"r")
        config = yaml.safe_load(fd)
        fd.close()

        description = ""

        if "description" in config:
            description = config["description"]

        print('{:60} | {:<30}'.format(tname, textwrap.fill(description, 120)))

def test_config_name_mapping():
    """This method returns test configuration name in the format
    ``{parent_parent}.{parent}.{os.path.basename(f)``
    It maps the name to full path of test configuration so it can be read the
    configuration file.

    :rtype: dict
    """
    yml_files = walk_tree(config_opts['BUILDTEST_CONFIGS_REPO'], ".yml")
    test_config_table = {}
    for f in yml_files:
        parent_parent = os.path.basename(os.path.dirname(os.path.dirname(f)))
        parent = os.path.basename(os.path.dirname(f))
        testconfig_name = f"{parent_parent}.{parent}.{os.path.basename(f)}"

        test_config_table[testconfig_name] = f
    return test_config_table

def func_testconfigs_view(args):
    """Print content of test configuration. This method implements
    ``buildtest testconfigs view <config>`` command.

    :param args: command line arguments to buildtest
    :type args: dict, required
    """
    test_config_table = test_config_name_mapping()
    query = f"cat {test_config_table[args.name]}"
    cmd = BuildTestCommand()
    cmd.execute(query)
    out = cmd.get_output()
    print (out)

def func_testconfigs_edit(args):
    """Open test configuration in editor. This method implements
    ``buildtest testconfigs edit <config>`` command

    :param args: command line arguments to buildtest
    :type args: dict, required
    """
    test_config_table = test_config_name_mapping()
    query = f"vim {test_config_table[args.name]}"
    os.system(query)


