import os, yaml, textwrap, subprocess, sys
from buildtest.tools.config import config_opts, TESTCONFIG_ROOT
from buildtest.tools.file import walk_tree
from buildtest.tools.system import BuildTestCommand


def testconfig_choices():
    """Return a list of test configuration used by options ``buildtest testconfigs [view | edit]`` and used for
    specifying configuration file ``buildtest build -c <config>``

    :rtype: list
    """
    all_testconfigs = walk_tree(TESTCONFIG_ROOT, ".yml")
    test = []
    for f in all_testconfigs:
        name, parent, gparent = (
            os.path.basename(f),
            os.path.basename(os.path.dirname(f)),
            os.path.basename(os.path.dirname(os.path.dirname(f))),
        )
        tname = os.path.join(gparent, parent, name)
        test.append(tname)
    return test


def func_testconfigs_show(args=None):
    """ Prints all test configuration and description of test.

    This method implements ``buildtest testconfigs list``

    :param args: command line arguments to buildtest
    :type args: dict, required
    """
    test_config_table = testconfig_choices()
    print("{:100} | {:<30}".format("Test Configuration Name", "Description"))
    print("{:-<160}".format(""))

    for testname in test_config_table:

        fd = open(os.path.join(TESTCONFIG_ROOT, testname), "r")
        config = yaml.safe_load(fd)
        fd.close()

        description = ""

        if "description" in config:
            description = config["description"]

        print("{:100} | {:<30}".format(testname, textwrap.fill(description, 120)))


def func_testconfigs_view(args=None):
    """Print content of test configuration. This method implements
    ``buildtest testconfigs view <config>`` command.

    :param args: command line arguments to buildtest
    :type args: dict, required
    """
    testconfig = os.path.join(TESTCONFIG_ROOT, args.name)
    query = f"cat {testconfig}"
    cmd = BuildTestCommand()
    cmd.execute(query)
    out = cmd.get_output()
    print(out)


def func_testconfigs_edit(args=None):
    """Open test configuration in editor. This method implements
    ``buildtest testconfigs edit <config>`` command

    :param args: command line arguments to buildtest
    :type args: dict, required
    """
    testconfig = os.path.join(TESTCONFIG_ROOT, args.name)
    query = f"{config_opts['EDITOR']} {testconfig}"
    os.system(query)
