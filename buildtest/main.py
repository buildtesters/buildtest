import os
import sys

# column width for linewrap for argparse library
os.environ["COLUMNS"] = "120"


def main():
    """Entry point to buildtest."""

    from buildtest.tools.config import check_configuration
    from buildtest.tools.menu import BuildTestParser
    from buildtest.tools.system import BuildTestSystem

    # Create a build test system, and check requirements
    buildtest_system = BuildTestSystem()
    buildtest_system.check_system_requirements()

    check_configuration()
    parser = BuildTestParser()
    parser.parse_options()


if __name__ == "__main__":
    main()
