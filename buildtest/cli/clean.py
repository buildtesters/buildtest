import os
import shutil

from buildtest.cli.build import resolve_testdirectory
from buildtest.defaults import (
    BUILD_HISTORY_DIR,
    BUILD_REPORT,
    BUILDSPEC_CACHE_FILE,
    BUILDTEST_REPORT_SUMMARY,
)
from buildtest.utils.file import is_dir, is_file


def clean(configuration, yes):
    """"""
    remove_report = "y"
    remove_history = "y"
    remove_buildspec_cache = "y"
    remove_testdir = "y"

    resolved_testdir = resolve_testdirectory(configuration)

    # request user prompt when 'buildtest clean' is specified without '-y' option. Default selection is 'y' for confirmation
    if not yes:

        remove_testdir = (
            input(f"Remove Test Directory {resolved_testdir} (y/n) [default: y] ")
            or "y"
        )
        remove_report = (
            input(f"Remove Report File {BUILD_REPORT} (y/n) [default: y] ") or "y"
        )
        remove_history = (
            input(f"Remove History Directory {BUILD_HISTORY_DIR} (y/n) [default: y] ")
            or "y"
        )
        remove_buildspec_cache = (
            input(f"Remove Buildspec Cache {BUILDSPEC_CACHE_FILE} (y/n) [default: y] ")
            or "y"
        )

    if remove_testdir == "y":
        print("======> Remove Test Directory")
        if is_dir(resolved_testdir):
            shutil.rmtree(resolved_testdir)

    if remove_report == "y":
        print("======> Removing Report File")
        if is_file(BUILD_REPORT):
            os.remove(BUILD_REPORT)
        if is_file(BUILDTEST_REPORT_SUMMARY):
            os.remove(BUILDTEST_REPORT_SUMMARY)

    if remove_history == "y":
        print("======> Removing History Directory")
        if is_dir(BUILD_HISTORY_DIR):
            shutil.rmtree(BUILD_HISTORY_DIR)

    if remove_buildspec_cache == "y":
        print("======> Removing buildspec cache")
        if is_file(BUILDSPEC_CACHE_FILE):
            os.remove(BUILDSPEC_CACHE_FILE)
