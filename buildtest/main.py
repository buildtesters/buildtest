import os
import sys

sys.path.insert(0, os.path.join(os.getenv("BUILDTEST_ROOT"), "buildtest"))
# column width for linewrap for argparse library
os.environ["COLUMNS"] = "120"

from buildtest.tools.menu import BuildTestParser
from buildtest.tools.system import BuildTestSystem
from buildtest.tools.config import check_configuration


def main():
    """Entry point to buildtest."""

    buildtest_system = BuildTestSystem()
    buildtest_system.check_system_requirements()

    check_configuration()

    parser = BuildTestParser()
    args = parser.parse_options()

if __name__ == "__main__":
    """Entry Point, invoking main() method"""
    main()
