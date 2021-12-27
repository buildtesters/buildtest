"""Entry point for buildtest"""

import os
import shutil
import webbrowser

from buildtest.cli import get_parser
from buildtest.cli.build import BuildTest, Tee
from buildtest.cli.buildspec import (
    BuildspecCache,
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
from buildtest.cli.debugreport import print_debug_report
from buildtest.cli.edit import edit_buildspec
from buildtest.cli.help import buildtest_help
from buildtest.cli.history import build_history
from buildtest.cli.inspect import inspect_cmd
from buildtest.cli.path import path_cmd
from buildtest.cli.report import report_cmd
from buildtest.cli.schema import schema_cmd
from buildtest.config import SiteConfiguration
from buildtest.defaults import (
    BUILDSPEC_CACHE_FILE,
    BUILDTEST_BUILDSPEC_DIR,
    BUILDTEST_EXECUTOR_DIR,
    BUILDTEST_LOGFILE,
    BUILDTEST_USER_HOME,
    VAR_DIR,
    console,
)
from buildtest.log import init_logfile
from buildtest.system import BuildTestSystem
from buildtest.tools.stylecheck import run_style_checks
from buildtest.tools.unittests import run_unit_tests
from buildtest.utils.file import create_dir, is_file, remove_file, resolve_path
from rich.traceback import install


def main():
    """Entry point to buildtest."""

    parser = get_parser()
    args = parser.parse_args()

    install(show_locals=True)
    no_color = False

    # disable color if buildtest --no-color or BUILDTEST_COLOR=False is set
    if args.no_color or os.getenv("BUILDTEST_COLOR") == "False":
        no_color = True

    console.no_color = no_color

    # if no commands just print the help message and return.
    if not args.subcommands:
        print(parser.print_help())
        return

    if is_file(BUILDTEST_LOGFILE):
        remove_file(BUILDTEST_LOGFILE)

    logger = init_logfile(debug=args.debug)

    create_dir(BUILDTEST_USER_HOME)
    create_dir(BUILDTEST_EXECUTOR_DIR)
    create_dir(BUILDTEST_BUILDSPEC_DIR)

    # Create a build test system, and check requirements
    system = BuildTestSystem()

    validate_executors = True
    # if buildtest build --disable-executor-check is specified store the value
    if hasattr(args, "disable_executor_check"):
        validate_executors = args.disable_executor_check

    config_file = (
        resolve_path(args.configfile) or os.getenv("BUILDTEST_CONFIGFILE") or None
    )
    configuration = SiteConfiguration(config_file)
    configuration.detect_system()
    configuration.validate(validate_executors)

    logger.info(f"Processing buildtest configuration file: {configuration.file}")

    # build buildspec cache file automatically if it doesn't exist
    if not is_file(BUILDSPEC_CACHE_FILE):
        root_buildspecs = []
        if hasattr(args, "root"):
            root_buildspecs = args.root

        BuildspecCache(roots=root_buildspecs, configuration=configuration)

    # buildtest build command
    if args.subcommands in ["build", "bd"]:
        fname = os.path.join(VAR_DIR, "output.txt")

        with Tee(fname):
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
                max_pend_time=args.maxpendtime,
                poll_interval=args.pollinterval,
                keep_stage_dir=args.keep_stage_dir,
                retry=args.retry,
                account=args.account,
                helpfilter=args.helpfilter,
                numprocs=args.procs,
            )
            cmd.build()

        if cmd.build_success():
            build_history_dir = cmd.get_build_history_dir()
            shutil.move(fname, os.path.join(build_history_dir, "output.txt"))

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
            show_buildspecs(test_names=args.name, configuration=configuration)
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

    # running buildtest config
    elif args.subcommands in ["config", "cg"]:
        #  running buildtest config compilers
        if args.config == "compilers":
            compiler_cmd(args, configuration)
        else:
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

    elif args.subcommands == "debugreport":
        print_debug_report(system, configuration)

    elif args.subcommands == "unittests":
        run_unit_tests()

    elif args.subcommands in ["stylecheck", "style"]:
        run_style_checks(
            no_black=args.no_black,
            no_isort=args.no_isort,
            no_pyflakes=args.no_pyflakes,
            apply_stylechecks=args.apply,
        )


if __name__ == "__main__":
    main()
