import logging
import os
import shutil
from jsonschema import validate

from buildtest.utils.file import create_dir
from buildtest.defaults import (
    BUILDTEST_SETTINGS_FILE,
    BUILDTEST_ROOT,
    DEFAULT_SETTINGS_FILE,
    DEFAULT_SETTINGS_SCHEMA,
)
from buildtest.buildsystem.schemas.utils import load_schema


def create_settings_file():
    """If default settings file don't exist, copy the default settings provided by buildtest."""

    if not os.path.exists(BUILDTEST_SETTINGS_FILE):
        shutil.copy(DEFAULT_SETTINGS_FILE, BUILDTEST_SETTINGS_FILE)


def init():
    """Buildtest init should check that the buildtest user root exists,
       and that dependency files are created. This is called by 
       ``load_settings``."""

    # check if $HOME/.buildtest exists, if not create directory
    if not os.path.exists(BUILDTEST_ROOT):
        print(
            f"Creating buildtest configuration directory: \
                 {BUILDTEST_ROOT}"
        )
        os.mkdir(BUILDTEST_ROOT)

    # Create subfolders for root, site
    create_dir(os.path.join(BUILDTEST_ROOT, "root"))
    create_dir(os.path.join(BUILDTEST_ROOT, "site"))

    # Create settings files
    create_settings_file()


def check_settings(settings_path=None):
    """Checks all keys in configuration file (settings/settings.yml) are valid
       keys and ensure value of each key matches expected type . For some keys
       special logic is taken to ensure values are correct and directory path
       exists.       

       If any error is found buildtest will terminate immediately.
       :return: returns gracefully if all checks passes otherwise terminate immediately
       :rtype: exit code 1 if checks failed
    """

    logger = logging.getLogger(__name__)

    user_schema = load_settings(settings_path)

    config_schema = load_schema(DEFAULT_SETTINGS_SCHEMA)
    logger.debug(f"Loading default configuration schema: {DEFAULT_SETTINGS_SCHEMA}")

    logger.debug(f"Validating user schema: {user_schema} with schema: {config_schema}")
    validate(instance=user_schema, schema=config_schema)
    logger.debug("Validation was successful")


def load_settings(settings_path=None):
    """Load the default settings file if no argument is specified.

       Parameters:

       :param settings_path: Path to buildtest settings file
       :type settings_path: str, optional
    """

    init()

    settings_path = settings_path or BUILDTEST_SETTINGS_FILE

    # load the configuration file
    return load_schema(settings_path)


def get_default_settings():
    """Load and return the default buildtest settings file. """

    return load_settings()
