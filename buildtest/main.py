import os

# column width for linewrap for argparse library
os.environ["COLUMNS"] = "120"


def main():
    """Entry point to buildtest."""

    from buildtest.menu import BuildTestParser
    from buildtest.system import BuildTestSystem
    from buildtest.log import init_logfile

    logger = init_logfile("buildtest.log")
    logger.info("Starting buildtest log")

    # Create a build test system, and check requirements
    BuildTestSystem()

    parser = BuildTestParser()
    parser.parse_options()


if __name__ == "__main__":
    main()
