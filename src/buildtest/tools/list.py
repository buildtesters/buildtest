"""
This module implements all the list operation in buildtest which include the
following:
1. List Software (buildtest list --software)
2. List Full Module Name and associated module file (buildtest list --modules)
3. List easyconfigs from module tree (buildtest list --easyconfigs)
"""

from buildtest.tools.modules import module_obj
from buildtest.tools.easybuild import find_easyconfigs


def func_list_subcmd(args):
    """This method is the entry point for ``buildtest list`` subcommand.

    :param args: dict of command line arguments passed
    :type args: dict, required
    """

    if args.easyconfigs:
        find_easyconfigs()
    if args.software:
        list_software()
    if args.modules:
        list_modules()


def list_software():
    """This method gets unique software from spider and prints the software
    with total count. This method invokes ``get_unique_modules()`` which is part
    of ``BuildTestModule`` and module_obj is an instance object.

    This method implements ``buildtest list --software``.
    """

    module_stack = module_obj.get_unique_modules()

    for item in module_stack:
        print(item)

    print("\n")
    print("Total Software Packages: ", len(module_stack))


def list_modules():

    """This is a method to invoke BuildTestModule.list_modules()"""
    module_obj.list_modules()


