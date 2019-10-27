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
        schema = SingleSource()
        print(yaml.dump(schema, default_flow_style=False, sort_keys=True))
