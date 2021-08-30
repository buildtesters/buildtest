"""Entry point for buildtest"""

import os
import webbrowser

from buildtest.cli import get_parser
from buildtest.cli.build import BuildTest
from buildtest.cli.buildspec import (
    buildspec_find,
    buildspec_validate,
    show_buildspecs,
    summarize_buildspec_cache,
)
from buildtest.cli.cd import change_directory
from buildtest.cli.cdash import cdash_cmd
from buildtest.cli.clean import clean
from buildtest.cli.compilers import compiler_cmd
from buildtest.cli.config import config_cmd
from buildtest.cli.edit import edit_buildspec
from buildtest.cli.help import buildtest_help
from buildtest.cli.history import build_history
from buildtest.cli.inspect import inspect_cmd
from buildtest.cli.path import path_cmd
from buildtest.cli.report import report_cmd
from buildtest.cli.schema import schema_cmd
from buildtest.config import SiteConfiguration
from buildtest.defaults import (
    BUILDTEST_BUILDSPEC_DIR,
    BUILDTEST_EXECUTOR_DIR,
    BUILDTEST_USER_HOME,
)
from buildtest.log import init_logfile
from buildtest.system import BuildTestSystem
from buildtest.utils.file import create_dir, is_file, remove_file, resolve_path

# column width for linewrap for argparse library
os.environ["COLUMNS"] = "120"


def main():
    """Entry point to buildtest."""

    parser = get_parser()
    args = parser.parse_args()

    color_mode = None

    if args.color == "off":
        color_mode = "False"
    else:
        color_mode = "True"

    if os.getenv("BUILDTEST_COLOR") == "False":
        color_mode = "False"

    os.environ["BUILDTEST_COLOR"] = color_mode

    # if no commands just print the help message and return.
    if not args.subcommands:
        print(parser.print_help())
        return

    buildtest_log = os.path.join(os.getenv("BUILDTEST_ROOT"), "buildtest.log")
    if is_file(buildtest_log):
        remove_file(buildtest_log)

    logger = init_logfile(debug=args.debug)

    create_dir(BUILDTEST_USER_HOME)
    create_dir(BUILDTEST_EXECUTOR_DIR)
    create_dir(BUILDTEST_BUILDSPEC_DIR)

    # Create a build test system, and check requirements
    system = BuildTestSystem()
    system.check()

    validate_executors = True
    # if buildtest build --disable-executor-check is specified store the value
    if hasattr(args, "disable_executor_check"):
        validate_executors = args.disable_executor_check

    config_file = resolve_path(args.configfile) or None
    configuration = SiteConfiguration(config_file)
    configuration.detect_system()
    configuration.validate(validate_executors)

    print("valid executors:", configuration.valid_executors)

    logger.info(f"Processing buildtest configuration file: {configuration.file}")

    # buildtest build command
    if args.subcommands in ["build", "bd"]:

        cmd = BuildTest(
            configuration=configuration,
            buildspecs=args.buildspec,
            exclude_buildspecs=args.exclude,
            executors=args.executor,
            tags=args.tags,
            filter_buildspecs=args.filter,
            rebuild=args.rebuild,
            stage=args.stage,
            testdir=args.testdir,
            buildtest_system=system,
            report_file=args.report,
            max_pend_time=args.max_pend_time,
            poll_interval=args.poll_interval,
            keep_stage_dir=args.keep_stage_dir,
            retry=args.retry,
            helpfilter=args.helpfilter,
        )
        cmd.build()

    elif args.subcommands in ["edit", "et"]:
        edit_buildspec(args.buildspec, configuration)

    # buildtest build history
    elif args.subcommands in ["history", "hy"]:
        build_history(args)

    # implementation for 'buildtest buildspec find'
    elif args.subcommands in ["buildspec", "bc"]:

        if args.buildspecs_subcommand == "find":
            buildspec_find(args=args, configuration=configuration)
        elif args.buildspecs_subcommand == "summary":
            summarize_buildspec_cache(configuration)
        elif args.buildspecs_subcommand == "show":
            show_buildspecs(name=args.name, configuration=configuration)
        elif args.buildspecs_subcommand == "validate":
            buildspec_validate(
                buildspecs=args.buildspec,
                excluded_buildspecs=args.exclude,
                tags=args.tag,
                executors=args.executor,
                configuration=configuration,
            )

    # running buildtest inspect
    elif args.subcommands in ["inspect", "it"]:
        inspect_cmd(args)

    # running buildtest config compilers
    elif args.subcommands in ["config", "cg"] and args.config == "compilers":
        compiler_cmd(args, configuration)

    # running buildtest config
    elif args.subcommands in ["config", "cg"]:
        config_cmd(args, configuration)

    # buildtest report
    elif args.subcommands in ["report", "rt"]:
        report_cmd(args)

    elif args.subcommands == "path":
        path_cmd(
            name=args.name,
            outfile=args.outfile,
            errfile=args.errfile,
            testpath=args.testpath,
            buildscript=args.buildscript,
            stagedir=args.stagedir,
        )
    # running bnuildtest schema
    elif args.subcommands == "schema":
        schema_cmd(args)

    # running buildtest cdash
    elif args.subcommands == "cdash":
        cdash_cmd(args, default_configuration=configuration)

    elif args.subcommands in ["help", "h"]:
        buildtest_help(command=args.command)

    elif args.subcommands == "clean":
        clean(configuration=configuration, yes=args.yes)

    elif args.subcommands == "cd":
        change_directory(args.test)

    elif args.subcommands == "docs":
        webbrowser.open("https://buildtest.readthedocs.io/")

    elif args.subcommands == "schemadocs":
        webbrowser.open("https://buildtesters.github.io/buildtest/")


if __name__ == "__main__":
    main()
