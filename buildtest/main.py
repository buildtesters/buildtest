"""Entry point for buildtest"""

import os
import shutil
import sys
import tempfile
from buildtest.config import (
    check_settings,
    resolve_settings_file,
    buildtest_configuration,
)
from buildtest.defaults import var_root, BUILDTEST_USER_HOME
from buildtest.menu.buildspec import buildspec_find
from buildtest.menu import BuildTestParser
from buildtest.menu.build import BuildTest
from buildtest.system import system
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
    create_dir(var_root)

    # Create a build test system, and check requirements
    # BuildTestSystem()
    system.check()

    parser = BuildTestParser()
    args = parser.parse_options()

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
        )
        cmd.build()

        logdir = buildtest_configuration.target_config.get("logdir")

        if not logdir:
            print(f"Writing Logfile to: {dest_logfile}")
            sys.exit(0)

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
        return

    settings_file = resolve_settings_file()

    logger.info(f"Processing buildtest configuration file: {settings_file}")
    check_settings(settings_file)

    # implementation for 'buildtest buildspec find'
    if args.subcommands == "buildspec":
        buildspec_find(args=args, settings_file=settings_file)
        return

    if args.subcommands and args.func:
        args.func(args)


if __name__ == "__main__":
    main()
