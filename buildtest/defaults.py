"""
Buildtest defaults, including environment variables and paths, are defined
or derived here.
"""

import pwd
import os

logID = "buildtest"


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

var_root = os.path.join(BUILDTEST_ROOT, "var")
executor_root = os.path.join(var_root, "executors")

BUILDSPEC_CACHE_FILE = os.path.join(var_root, "buildspec-cache.json")

BUILD_REPORT = os.path.join(var_root, "report.json")

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
