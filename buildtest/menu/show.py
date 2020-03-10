import json

import sys
import yaml


from buildtest.menu.config import show_configuration
from buildtest.buildsystem.singlesource import get_yaml_schema


def func_show_subcmd(args):
    """Entry point to ``buildtest show`` sub command.

    :param args: command line arguments to buildtest
    :type args: dict, required
    """
    if args.config:
        show_configuration()


def show_schema_layout(args=None):
    """Implements method ``buildtest show schema``"""
    schema = get_yaml_schema()
    yaml.dump(schema, sys.stdout, default_flow_style=False)
