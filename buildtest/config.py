import json
import os
import shutil
from jsonschema import validate

from buildtest.utils.file import create_dir
from buildtest.defaults import (
    BUILDTEST_BUILD_LOGFILE,
    BUILDTEST_CONFIG_FILE,
    BUILDTEST_ROOT,
    DEFAULT_CONFIG_FILE,
    DEFAULT_CONFIG_SCHEMA,
)
from buildtest.buildsystem.schemas.utils import load_schema


def create_config_files():
    """If default config files don't exist, copy the default configuration provided by buildtest."""

    if not os.path.exists(BUILDTEST_CONFIG_FILE):
        shutil.copy(DEFAULT_CONFIG_FILE, BUILDTEST_CONFIG_FILE)


def create_logfile():
    """Create a logfile to keep track of messages for the user, if doesn't exist."""

    if not os.path.exists(BUILDTEST_BUILD_LOGFILE):
        build_dict = {"build": {}}
        with open(BUILDTEST_BUILD_LOGFILE, "w") as outfile:
            json.dump(build_dict, outfile, indent=2)


def init():
    """Buildtest init should check that the buildtest user root exists,
       and that dependency files are created. This is called by 
       load_configuration."""

    # check if $HOME/.buildtest exists, if not create directory
    if not os.path.exists(BUILDTEST_ROOT):
        print(
            f"Creating buildtest configuration directory: \
                 {BUILDTEST_ROOT}"
        )
        os.mkdir(BUILDTEST_ROOT)

    # Create subfolders for var and root
    create_dir(os.path.join(BUILDTEST_ROOT, "var"))
    create_dir(os.path.join(BUILDTEST_ROOT, "root"))
    create_dir(os.path.join(BUILDTEST_ROOT, "site"))

    # Create config files, module files, and log file
    create_config_files()
    create_logfile()


def check_configuration():
    """Checks all keys in configuration file (settings/default.yml) are valid
       keys and ensure value of each key matches expected type . For some keys
       special logic is taken to ensure values are correct and directory path
       exists.       

       If any error is found buildtest will terminate immediately.
       :return: returns gracefully if all checks passes otherwise terminate immediately
       :rtype: exit code 1 if checks failed
    """

    config_schema = load_schema(DEFAULT_CONFIG_SCHEMA)
    validate(instance=config_opts, schema=config_schema)


def load_configuration(config_path=None):
    """Load the default configuration file."""

    init()

    config_path = config_path or BUILDTEST_CONFIG_FILE

    # load the configuration file
    return load_schema(config_path)


# Run on init, so we only load once
config_opts = load_configuration()
