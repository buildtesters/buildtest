import json
import sys

from buildtest.tools.config import BUILDTEST_SYSTEM
from buildtest.tools.system import BuildTestSystem


def func_system_view(args=None):
    """Display system configuration from system.json. This implements `buildtest system view`"""
    fd = open(BUILDTEST_SYSTEM, "r")
    system_detail = json.load(fd)
    json.dump(system_detail, sys.stdout, indent=2)


def func_system_fetch(args=None):
    system = BuildTestSystem().get_system()

    with open(BUILDTEST_SYSTEM, "w") as outfile:
        json.dump(system, outfile, indent=4)

    print("Updating system configuration.")
