import os
import shutil
import sys

import coverage
import pytest
from buildtest.defaults import BUILDTEST_ROOT, BUILDTEST_USER_HOME, VAR_DIR
from buildtest.utils.file import is_dir

# here = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, here)


def run_unit_tests():

    if not os.getenv("BUILDTEST_ROOT"):
        sys.exit(
            "Please check your buildtest installation by running 'source setup.sh'"
        )

    html_dir = os.path.join(BUILDTEST_ROOT, "htmlcov")

    if is_dir(BUILDTEST_USER_HOME):
        shutil.rmtree(BUILDTEST_USER_HOME)

    if is_dir(VAR_DIR):
        shutil.rmtree(VAR_DIR)

    cov = coverage.Coverage(config_file=os.path.join(BUILDTEST_ROOT, ".coveragerc"))
    cov.erase()
    cov.start()
    retcode = pytest.main([os.path.join(BUILDTEST_ROOT, "tests")])

    # if there is a failure in pytest raise exit 1
    if retcode == pytest.ExitCode.TESTS_FAILED:
        sys.exit(1)

    cov.stop()
    cov.save()
    cov.html_report(title="buildtest unittests coverage report", directory=html_dir)
    cov.json_report(outfile=os.path.join(BUILDTEST_ROOT, "coverage.json"))
    cov.report(ignore_errors=True, skip_empty=True, sort="cover", precision=2)

    print("\n\n")
    print("Writing coverage results to: ", html_dir)
    coverage_file = os.path.join(html_dir, "index.html")
    assert os.path.exists(coverage_file)
    print("You can view coverage report by viewing file: ", coverage_file)


if __name__ == "__main__":
    run_unit_tests()
