import os
import sys

sys.path.insert(0, os.path.join(os.getenv("BUILDTEST_ROOT"), "src"))
# column width for linewrap for argparse library
os.environ["COLUMNS"] = "120"

from buildtest.tools.menu import menu, parse_options, BuildTestParser
from buildtest.tools.system import BuildTestSystem


def main():
    """Entry point to buildtest."""

    buildtest_system = BuildTestSystem()
    buildtest_system.check_system_requirements()
    parser = BuildTestParser()
    args = parser.parse_options()

    #parser.parse_options(("subcommands": "show","config": True) )


if __name__ == "__main__":
    """Entry Point, invoking main() method"""
    main()
