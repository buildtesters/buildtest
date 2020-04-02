import os

# column width for linewrap for argparse library
os.environ["COLUMNS"] = "120"


def main():
    """Entry point to buildtest."""

    from buildtest.menu import BuildTestParser
    from buildtest.system import BuildTestSystem

    # Create a build test system, and check requirements
    buildtest_system = BuildTestSystem()
    buildtest_system.check_system_requirements()

    parser = BuildTestParser()
    parser.parse_options()


if __name__ == "__main__":
    main()
