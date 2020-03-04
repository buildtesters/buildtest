"""

Buildtest defaults, including environment variables and paths, are defined
or derived here.

"""

import pwd
import os

logID = "buildtest"

# Get user home based on effective uid, root of install to copy files
userhome = pwd.getpwuid(os.getuid())[5]
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# root of buildtest-framework user home
BUILDTEST_ROOT = os.path.join(userhome, ".buildtest")

# json file used by buildtest to write build meta-data
BUILDTEST_BUILD_LOGFILE = os.path.join(BUILDTEST_ROOT, "var", "build.json")

# dictionary used for storing status of builds
BUILDTEST_BUILD_HISTORY = {}
BUILDTEST_CONFIG_FILE = os.path.join(BUILDTEST_ROOT, "settings.yml")
BUILDTEST_CONFIG_BACKUP_FILE = os.path.join(BUILDTEST_ROOT, "settings.yml.bak")

# TESTCONFIG_ROOT is the root directory where test configurations are found
# configs can be specified as full paths or relative to this path
TESTCONFIG_ROOT = os.path.join(BUILDTEST_ROOT, "site")
DEFAULT_CONFIG_FILE = os.path.join(root, "settings.yml")
EDITOR_LIST = ["vim", "emacs", "nano"]
