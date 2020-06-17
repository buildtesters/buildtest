"""
Buildtest defaults, including environment variables and paths, are defined
or derived here.
"""

import pwd
import os

logID = "buildtest"

# each has a subfolder in buildtest/buildsystem/schemas/ with *.schema.json
supported_schemas = [
    "script-v1.0.schema.json",
    "compiler-v1.0.schema.json",
    "global.schema.json",
    "settings.schema.json",
]

# Get user home based on effective uid, root of install to copy files
userhome = pwd.getpwuid(os.getuid())[5]
root = os.path.dirname(os.path.abspath(__file__))

# root of buildtest user home, default shell
BUILDTEST_ROOT = os.path.join(userhome, ".buildtest")

# dictionary used for storing status of builds
BUILDTEST_SETTINGS_FILE = os.path.join(BUILDTEST_ROOT, "settings.yml")

REPO_FILE = os.path.join(BUILDTEST_ROOT, "repo.yaml")

BUILDSPEC_CACHE_FILE = os.path.join(BUILDTEST_ROOT, "buildspec.cache")

BUILD_REPORT = os.path.join(os.path.dirname(root), "var", "report.json")

# BUILDSPEC_DEFAULT_PATH is the root directory where Buildspec are found
# when using buildtest get to clone a buildtest test repo
BUILDSPEC_DEFAULT_PATH = os.path.join(BUILDTEST_ROOT, "site")
DEFAULT_SETTINGS_FILE = os.path.join(root, "settings", "settings.yml")
DEFAULT_SETTINGS_SCHEMA = os.path.join(root, "settings", "settings.schema.json")
