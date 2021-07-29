"""
Buildtest defaults, including environment variables and paths, are defined
or derived here.
"""

import os
import pwd

supported_type_schemas = ["script-v1.0.schema.json", "compiler-v1.0.schema.json"]

# each has a subfolder in buildtest/buildsystem/schemas/ with *.schema.json
supported_schemas = supported_type_schemas + [
    "global.schema.json",
    "settings.schema.json",
]

# Get user home based on effective uid, root of install to copy files
userhome = pwd.getpwuid(os.getuid())[5]
BUILDTEST_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SCHEMA_ROOT = os.path.join(BUILDTEST_ROOT, "buildtest", "schemas")

# root of buildtest user home, default shell
BUILDTEST_USER_HOME = os.path.join(userhome, ".buildtest")

# dictionary used for storing status of builds
USER_SETTINGS_FILE = os.path.join(BUILDTEST_USER_HOME, "config.yml")


VAR_DIR = os.path.join(BUILDTEST_ROOT, "var")

BUILD_HISTORY_DIR = os.path.join(VAR_DIR, ".history")
BUILDTEST_DEFAULT_TESTDIR = os.path.join(VAR_DIR, "tests")
BUILDTEST_EXECUTOR_DIR = os.path.join(VAR_DIR, "executor")

BUILDTEST_BUILDSPEC_DIR = os.path.join(VAR_DIR, "buildspecs")

BUILDSPEC_CACHE_FILE = os.path.join(BUILDTEST_BUILDSPEC_DIR, "cache.json")

BUILD_REPORT = os.path.join(VAR_DIR, "report.json")

#  BUILDTEST_REPORT_SUMMARY file keeps track of all unique report files as result of 'buildtest build' commands.
#  The file contains a single line that denotes path to report file and one can specify alternate path to report file
# using 'buildtest build -r <report>' and this is used by 'buildtest inspect' and 'buildtest report' if one wants to
# read a different report file
BUILDTEST_REPORT_SUMMARY = os.path.join(VAR_DIR, "report-summary.txt")

BUILDSPEC_DEFAULT_PATH = [
    os.path.join(BUILDTEST_ROOT, "tutorials"),
    os.path.join(BUILDTEST_ROOT, "general_tests"),
]

DEFAULT_SETTINGS_FILE = os.path.join(
    BUILDTEST_ROOT, "buildtest", "settings", "config.yml"
)
DEFAULT_SETTINGS_SCHEMA = os.path.join(
    BUILDTEST_ROOT, "buildtest", "schemas", "settings.schema.json"
)
