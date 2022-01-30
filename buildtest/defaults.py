"""
Buildtest defaults, including environment variables and paths, are defined
or derived here.
"""

import os
import pwd

from rich.console import Console

console = Console()

# Get user home based on effective uid, root of install to copy files
userhome = pwd.getpwuid(os.getuid())[5]
BUILDTEST_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SCHEMA_ROOT = os.path.join(BUILDTEST_ROOT, "buildtest", "schemas")

BUILDTEST_UNITTEST_ROOT = os.path.join(BUILDTEST_ROOT, "tests")

# root of buildtest user home, default shell
BUILDTEST_USER_HOME = os.path.join(userhome, ".buildtest")

# dictionary used for storing status of builds
USER_SETTINGS_FILE = os.path.join(BUILDTEST_USER_HOME, "config.yml")


VAR_DIR = os.path.join(BUILDTEST_ROOT, "var")

BUILDTEST_LOGFILE = os.path.join(VAR_DIR, "buildtest.log")
DEFAULT_LOGDIR = os.path.join(VAR_DIR, "logs")
BUILD_HISTORY_DIR = os.path.join(VAR_DIR, ".history")
BUILDTEST_DEFAULT_TESTDIR = os.path.join(VAR_DIR, "tests")
BUILDTEST_EXECUTOR_DIR = os.path.join(VAR_DIR, "executor")

BUILDTEST_BUILDSPEC_DIR = os.path.join(VAR_DIR, "buildspecs")

BUILDSPEC_CACHE_FILE = os.path.join(BUILDTEST_BUILDSPEC_DIR, "cache.json")

BUILD_REPORT = os.path.join(VAR_DIR, "report.json")

#  BUILDTEST_REPORTS file keeps track of all unique report files as result of 'buildtest build' commands.
#  The file contains a single line that denotes path to report file and one can specify alternate path to report file
# using 'buildtest build -r <report>' and this is used by 'buildtest inspect' and 'buildtest report' if one wants to
# read a different report file
BUILDTEST_REPORTS = os.path.join(VAR_DIR, "list-report.json")

BUILDSPEC_DEFAULT_PATH = [
    os.path.join(BUILDTEST_ROOT, "tutorials"),
    os.path.join(BUILDTEST_ROOT, "general_tests"),
]

DEFAULT_SETTINGS_FILE = os.path.join(
    BUILDTEST_ROOT, "buildtest", "settings", "config.yml"
)
TUTORIALS_SETTINGS_FILE = os.path.join(
    BUILDTEST_ROOT, "buildtest", "settings", "spack_container.yaml"
)
DEFAULT_SETTINGS_SCHEMA = os.path.join(
    BUILDTEST_ROOT, "buildtest", "schemas", "settings.schema.json"
)
