"""

Buildtest defaults, including environment variables and paths, are defined
or derived here.

"""

import pwd
import os

from buildtest import BUILDTEST_VERSION

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
BUILDTEST_MODULE_COLLECTION_FILE = os.path.join(
    BUILDTEST_ROOT, "var", "collection.json"
)
BUILDTEST_MODULE_FILE = os.path.join(BUILDTEST_ROOT, "var", "modules.json")

# BUILDTEST_SPIDER_FILE is used to keep a cache of Lmod spider locally to avoid rerunning spider every time
BUILDTEST_SPIDER_FILE = os.path.join(BUILDTEST_ROOT, "root", "spider.json")

# TESTCONFIG_ROOT is the root directory where test configurations are found
TESTCONFIG_ROOT = os.path.join(BUILDTEST_ROOT, "site")
DEFAULT_CONFIG_FILE = os.path.join(root, "settings.yml")
EDITOR_LIST = ["vim", "emacs", "nano"]
