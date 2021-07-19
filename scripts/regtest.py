import os
import shutil
import sys

import coverage
import pytest
from buildtest.defaults import BUILDTEST_USER_HOME, VAR_DIR
from buildtest.utils.file import is_dir

if not os.getenv("BUILDTEST_ROOT"):
    sys.exit("Please check your buildtest installation by running 'source setup.sh'")

html_dir = os.path.join(os.getenv("BUILDTEST_ROOT"), "htmlcov")

if is_dir(BUILDTEST_USER_HOME):
    shutil.rmtree(BUILDTEST_USER_HOME)

if is_dir(VAR_DIR):
    shutil.rmtree(VAR_DIR)

cov = coverage.Coverage()
cov.erase()
cov.start()
pytest.main()
cov.stop()
cov.save()
cov.html_report(directory=html_dir)
cov.report()

print("\n\n")
print("Writing coverage results to: ", html_dir)
coverage_file = os.path.join(html_dir, "index.html")
assert os.path.exists(coverage_file)
print("You can view coverage report by viewing file: ", coverage_file)
