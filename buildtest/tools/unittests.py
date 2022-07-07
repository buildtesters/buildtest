import argparse
import os
import shutil
import sys

here = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(here)
print(sys.path)

import coverage
import pytest
from buildtest.defaults import (
    BUILDTEST_ROOT,
    BUILDTEST_UNITTEST_ROOT,
    BUILDTEST_USER_HOME,
    VAR_DIR,
    console,
)
from buildtest.utils.file import is_dir, resolve_path


def run_unit_tests(pytestopts=None, sourcefiles=None, enable_coverage=False):
    """Entry point for running buildtest unit tests. This method can be invoked via ``buildtest unittests`` or run
    via command line as standalone program. The unit tests are run via `pytest <https://docs.pytest.org/>`_ and `coverage <https://coverage.readthedocs.io/en/6.2/>`_
    for measuring coverage report. This method will report coverage results that can be viewable in html or json.

    Args:
        pytestopts (str): Specify options to pytest command.
        sourcefiles (list): List of source files to run with pytest
        enable_coverage (bool): Enable coverage when running regression test
    """

    if not os.getenv("BUILDTEST_ROOT"):
        sys.exit(
            "Please check your buildtest installation by running 'source setup.sh'"
        )

    pytestopts = pytestopts.split() if pytestopts else []
    sources = []

    # if --sourcefiles specified we resolve path to each argument otherwise default to BUILDTEST_UNITTEST_ROOT which is root of test directory
    sourcefiles = sourcefiles or [BUILDTEST_UNITTEST_ROOT]
    for fpath in sourcefiles:
        sources.append(resolve_path(fpath))

    # need to remove any None types from list since resolve_path method can return None if path is invalid
    sources = list(filter(None, sources))

    pytest_cmd = pytestopts + sources

    html_dir = os.path.join(BUILDTEST_ROOT, "htmlcov")

    if is_dir(BUILDTEST_USER_HOME):
        shutil.rmtree(BUILDTEST_USER_HOME)

    if is_dir(VAR_DIR):
        shutil.rmtree(VAR_DIR)

    cov = coverage.Coverage(branch=True)

    # run regression test with coverage if --coverage is specified
    if enable_coverage:
        cov.erase()
        cov.start()

    # run regression test
    retcode = pytest.main(pytest_cmd)

    # if there is a failure in pytest raise exit 1
    if retcode == pytest.ExitCode.TESTS_FAILED:
        sys.exit(1)

    if enable_coverage:
        cov.stop()
        cov.html_report(title="buildtest unittests coverage report", directory=html_dir)
        cov.json_report(outfile=os.path.join(BUILDTEST_ROOT, "coverage.json"))
        cov.report(ignore_errors=True, skip_empty=True, sort="-cover", precision=2)

        print("\n\n")
        console.print("Writing coverage results to: ", html_dir)
        coverage_file = os.path.join(html_dir, "index.html")
        assert os.path.exists(coverage_file)
        console.print("You can view coverage report by viewing file: ", coverage_file)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        prog="unittest",
        description="Run buildtest unit tests",
    )
    parser.add_argument(
        "-c",
        "--coverage",
        action="store_true",
        help="Enable coverage when running regression test",
    )
    parser.add_argument("-p", "--pytestopts", type=str, help="Specify option to pytest")
    parser.add_argument(
        "-s",
        "--sourcefiles",
        type=str,
        help="Specify path to file or directory when running regression test",
        action="append",
    )
    args = parser.parse_args()

    run_unit_tests(
        pytestopts=args.pytestopts,
        sourcefiles=args.sourcefiles,
        enable_coverage=args.coverage,
    )
