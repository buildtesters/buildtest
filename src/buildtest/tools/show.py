import json

import sys
import yaml


from buildtest.tools.config import show_configuration
from buildtest.tools.buildsystem.singlesource import SingleSource


def func_show_subcmd(args):
    """Entry point to ``buildtest show`` sub command.

    :param args: command line arguments to buildtest
    :type args: dict, required
    """
    if args.config:
        show_configuration()

    if args.keys:
        schema = SingleSource().get_schema()
        yaml.dump(schema, sys.stdout, default_flow_style=False)
