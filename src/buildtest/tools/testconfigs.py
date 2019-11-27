import os, yaml, textwrap, subprocess
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
    print("{:60} | {:<30}".format("Test Configuration Name", "Description"))
    print("{:-<100}".format(""))

    for config in test_config_table.items():
        tname = config[0]
        fname = config[1]

        fd = open(fname, "r")
        config = yaml.safe_load(fd)
        fd.close()

        description = ""

        if "description" in config:
            description = config["description"]

        print("{:60} | {:<30}".format(tname, textwrap.fill(description, 120)))


def test_config_name_mapping():
    """This method returns test configuration name in the format
    ``{parent_parent}.{parent}.{os.path.basename(f)``
    It maps the name to full path of test configuration so it can be read the
    configuration file.

    :rtype: dict
    """
    yml_files = walk_tree(config_opts["BUILDTEST_CONFIGS_REPO"], ".yml")
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
    print(out)


def func_testconfigs_edit(args):
    """Open test configuration in editor. This method implements
    ``buildtest testconfigs edit <config>`` command

    :param args: command line arguments to buildtest
    :type args: dict, required
    """
    test_config_table = test_config_name_mapping()
    query = f"vim {test_config_table[args.name]}"
    os.system(query)


def func_testconfigs_maintainer(args):
    """Update maintainer key in test configuration."""

    git_user_name = subprocess.getoutput("git config --get user.name").rstrip().lower()
    git_user_email = (
        subprocess.getoutput("git config --get user.email").rstrip().lower()
    )

    entry = f"{git_user_name} {git_user_email}"

    testconfig_mapping = test_config_name_mapping()
    testconfig_file = testconfig_mapping[args.name]

    fd = open(testconfig_file, "r")
    content = yaml.safe_load(fd)
    fd.close()

    # if user wants to be maintainer of file
    if args.maintainer == "yes":
        # if user the first maintainer to file
        if "maintainer" not in content:
            content["maintainer"] = []
            content["maintainer"].append(entry)
        else:
            if entry not in content["maintainer"]:
                content["maintainer"].append(entry)
                print(f"Adding Maintainer: {entry} to file {testconfig_file}")
            else:
                print(f"{entry} is already a maintainer")
                return

        write_fd = open(testconfig_file, "w")
        yaml.dump(content, write_fd, default_flow_style=False)
        write_fd.close()

    # if user wants to be removed from maintainer
    else:
        # if maintainer key found then only check if user exist in list,
        # otherwise no action is needed
        if "maintainer" in content:
            if entry in content["maintainer"]:
                write_fd = open(testconfig_file, "w")
                content["maintainer"].remove(entry)
                # if no maintainers are left after removal, then delete the
                # key. It may be worth changing this behavior to ensure one
                # maintainer is always present
                if len(content["maintainer"]) == 0:
                    del content["maintainer"]

                yaml.dump(content, write_fd, default_flow_style=False)
                write_fd.close()

                print(f"Removing Maintainer: {entry} from file {testconfig_file}")
            else:
                print(f"{entry} is not a maintainer of file {testconfig_file}")
                return

    print(f"----------------- FILE:{testconfig_file} ----------------------")
    print(yaml.dump(content, default_flow_style=False))
