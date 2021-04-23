"""Entry point for buildtest"""

import os
import webbrowser

from buildtest.config import check_settings
from buildtest.defaults import (
    BUILDTEST_VAR_DIR,
    BUILDTEST_USER_HOME,
    BUILDTEST_EXECUTOR_DIR,
    BUILDTEST_BUILDSPEC_DIR,
)
from buildtest.cli import get_parser
from buildtest.cli.build import BuildTest
from buildtest.system import BuildTestSystem
from buildtest.log import init_logfile, streamlog
from buildtest.utils.file import create_dir

# column width for linewrap for argparse library
os.environ["COLUMNS"] = "120"


def main():
    """Entry point to buildtest."""

    if not os.getenv("BUILDTEST_COLOR"):
        os.environ["BUILDTEST_COLOR"] = "True"

    # the logfile is written to $BUILDTEST_ROOT/buildtest.log
    logger = init_logfile(os.path.join(os.getenv("BUILDTEST_ROOT"), "buildtest.log"))
    logger.info("Starting buildtest log")

    create_dir(BUILDTEST_USER_HOME)
    create_dir(BUILDTEST_VAR_DIR)
    create_dir(BUILDTEST_EXECUTOR_DIR)
    create_dir(BUILDTEST_BUILDSPEC_DIR)

    # Create a build test system, and check requirements
    system = BuildTestSystem()
    system.check()

    parser = get_parser()
    args, extras = parser.parse_known_args()

    # if no commands specified we raise an error
    if not args.subcommands:
        raise SystemExit("Invalid input argument")

    if args.debug:
        streamlog(args.debug)

    if args.subcommands == "build":

        configuration = check_settings(args.config)
        logger.info(f"Processing buildtest configuration file: {configuration.file}")

        cmd = BuildTest(
            configuration=configuration,
            config_file=args.config,
            buildspecs=args.buildspec,
            exclude_buildspecs=args.exclude,
            executors=args.executor,
            tags=args.tags,
            filter_tags=args.filter_tags,
            rebuild=args.rebuild,
            stage=args.stage,
            testdir=args.testdir,
            buildtest_system=system,
            report_file=args.report_file,
        )
        cmd.build()

        return

    configuration = check_settings()
    logger.info(f"Processing buildtest configuration file: {configuration.file}")

    # implementation for 'buildtest buildspec find'
    if args.subcommands == "buildspec":
        from buildtest.cli.buildspec import buildspec_find

        buildspec_find(args=args, settings_file=configuration.file)
    elif args.subcommands == "docs":
        webbrowser.open("https://buildtest.readthedocs.io/")
    elif args.subcommands == "schemadocs":

        webbrowser.open("https://buildtesters.github.io/buildtest/")
    elif args.subcommands == "inspect":
        from buildtest.cli.inspect import inspect_cmd

        inspect_cmd(args)

    elif args.subcommands == "config" and args.config == "compilers":
        from buildtest.cli.compilers import compiler_cmd

        compiler_cmd(args)

    elif args.subcommands == "config":
        from buildtest.cli.config import config_cmd

        config_cmd(args, configuration)

    elif args.subcommands == "report":
        from buildtest.cli.report import report_cmd

        report_cmd(args)

    elif args.subcommands == "schema":
        from buildtest.cli.schema import schema_cmd

        schema_cmd(args)

    elif args.subcommands == "cdash":
        from buildtest.cli.cdash import cdash_cmd

        # Check for configuration since 'buildtest cdash -c /path/to/config' can specify alternate location
        configuration = check_settings(args.config)
        logger.info(f"Processing buildtest configuration file: {configuration.file}")

        cdash_cmd(args, default_configuration=configuration)


if __name__ == "__main__":
    main()
