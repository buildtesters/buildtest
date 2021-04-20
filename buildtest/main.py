"""Entry point for buildtest"""

import os
import shutil
import tempfile
import webbrowser

from buildtest.config import (
    check_settings,
    resolve_settings_file,
    buildtest_configuration,
)
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
from buildtest.utils.file import create_dir, resolve_path

# column width for linewrap for argparse library
os.environ["COLUMNS"] = "120"


def main():
    """Entry point to buildtest."""

    if not os.getenv("BUILDTEST_COLOR"):
        os.environ["BUILDTEST_COLOR"] = "True"

    # create a temporary file to store logfile and we don't delete file by setting 'delete=False'
    # by default tempfile will delete file upon exit.
    tf = tempfile.NamedTemporaryFile(prefix="buildtest_", delete=False, suffix=".log")
    dest_logfile = tf.name

    logger = init_logfile(dest_logfile)
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
        # settings_file = resolve_settings_file(args.config)
        # check_settings(args.config)
        cmd = BuildTest(
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

        logdir = buildtest_configuration.target_config.get("logdir")

        if not logdir:
            print(f"Writing Logfile to: {dest_logfile}")

            shutil.copy2(
                dest_logfile, os.path.join(os.getenv("BUILDTEST_ROOT"), "buildtest.log")
            )
            print(
                "A copy of logfile can be found at $BUILDTEST_ROOT/buildtest.log - ",
                os.path.join(os.getenv("BUILDTEST_ROOT"), "buildtest.log"),
            )
            return

        logdir = resolve_path(logdir, exist=False)
        if logdir:
            create_dir(logdir)
            fname = os.path.basename(dest_logfile)
            logpath = os.path.join(logdir, fname)
            shutil.copy2(dest_logfile, logpath)

            print(f"Writing Logfile to: {logpath}")
        else:
            print(f"Writing Logfile to: {dest_logfile}")

        # store copy of logfile at $BUILDTEST_ROOT/buildtest.log. A convenient location for user to
        # find logfile for last build, this will be overwritten for every subsequent build.
        shutil.copy2(
            dest_logfile, os.path.join(os.getenv("BUILDTEST_ROOT"), "buildtest.log")
        )
        print(
            "A copy of logfile can be found at $BUILDTEST_ROOT/buildtest.log - ",
            os.path.join(os.getenv("BUILDTEST_ROOT"), "buildtest.log"),
        )
        return

    settings_file = resolve_settings_file()

    logger.info(f"Processing buildtest configuration file: {settings_file}")
    configuration = check_settings(settings_file)

    # implementation for 'buildtest buildspec find'
    if args.subcommands == "buildspec":
        from buildtest.cli.buildspec import buildspec_find

        buildspec_find(args=args, settings_file=settings_file)
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

        cdash_cmd(args, configuration)


if __name__ == "__main__":
    main()
