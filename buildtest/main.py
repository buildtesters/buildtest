import os

# column width for linewrap for argparse library
os.environ["COLUMNS"] = "120"

from buildtest.tools.menu import BuildTestParser
from buildtest.tools.system import BuildTestSystem
from buildtest.tools.config import check_configuration


def main():
    """Entry point to buildtest."""

    # Create a build test system, and check requirements
    buildtest_system = BuildTestSystem()
    buildtest_system.check_system_requirements()

    check_configuration()
    parser = BuildTestParser()
    parser.parse_options()


if __name__ == "__main__":
    main()
