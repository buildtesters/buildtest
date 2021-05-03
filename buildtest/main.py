"""Entry point for buildtest"""

import os
import webbrowser
from buildtest.config import SiteConfiguration
from buildtest.defaults import (
    BUILDTEST_VAR_DIR,
    BUILDTEST_USER_HOME,
    BUILDTEST_EXECUTOR_DIR,
    BUILDTEST_BUILDSPEC_DIR,
)
from buildtest.cli import get_parser
from buildtest.cli.build import BuildTest
from buildtest.system import BuildTestSystem
from buildtest.log import init_logfile
from buildtest.utils.file import create_dir, resolve_path

# column width for linewrap for argparse library
os.environ["COLUMNS"] = "120"


def main():
    """Entry point to buildtest."""

    if not os.getenv("BUILDTEST_COLOR"):
        os.environ["BUILDTEST_COLOR"] = "True"

    parser = get_parser()
    args, extras = parser.parse_known_args()

    logger = init_logfile()

    # if no commands just print the help message and return.
    if not args.subcommands:
        print(parser.print_help())
        return

    create_dir(BUILDTEST_USER_HOME)
    create_dir(BUILDTEST_VAR_DIR)
    create_dir(BUILDTEST_EXECUTOR_DIR)
    create_dir(BUILDTEST_BUILDSPEC_DIR)

    # Create a build test system, and check requirements
    system = BuildTestSystem()
    system.check()

    config_file = resolve_path(args.config_file) or None
    configuration = SiteConfiguration(config_file)
    configuration.get_current_system()
    configuration.validate()

    logger.info(f"Processing buildtest configuration file: {configuration.file}")

    if args.subcommands == "build":

        cmd = BuildTest(
            configuration=configuration,
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
            max_pend_time=args.max_pend_time,
            poll_interval=args.poll_interval,
        )
        cmd.build()

        return

    # implementation for 'buildtest buildspec find'
    if args.subcommands == "buildspec":
        from buildtest.cli.buildspec import buildspec_find

        buildspec_find(args=args, configuration=configuration)

    elif args.subcommands == "docs":
        webbrowser.open("https://buildtest.readthedocs.io/")

    elif args.subcommands == "schemadocs":
        webbrowser.open("https://buildtesters.github.io/buildtest/")

    elif args.subcommands == "inspect":
        from buildtest.cli.inspect import inspect_cmd

        inspect_cmd(args)

    elif args.subcommands == "config" and args.config == "compilers":
        from buildtest.cli.compilers import compiler_cmd

        compiler_cmd(args, configuration)

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

        cdash_cmd(args, default_configuration=configuration)


if __name__ == "__main__":
    main()
