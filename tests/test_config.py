import os
import shutil
from buildtest.defaults import BUILDTEST_SETTINGS_FILE, BUILDTEST_ROOT
from buildtest.config import (
    load_settings,
    check_settings,
    get_default_settings,
    create_settings_file,
    init,
)
from buildtest.utils.file import is_file, is_dir


def test_load_and_check_settings():

    load_settings(BUILDTEST_SETTINGS_FILE)
    assert os.path.exists(BUILDTEST_SETTINGS_FILE)

    check_settings()


def test_get_default_settings():

    loaded_settings = get_default_settings()
    assert isinstance(loaded_settings, dict)

    assert "editor" in loaded_settings.keys()
    assert "executors" in loaded_settings.keys()


def test_create_settings_file():

    os.remove(BUILDTEST_SETTINGS_FILE)
    create_settings_file()
    assert is_file(BUILDTEST_SETTINGS_FILE)


def test_init_creation_of_buildtest_dir():

    shutil.rmtree(BUILDTEST_ROOT)
    init()
    assert is_dir(os.path.join(BUILDTEST_ROOT, "root"))
    assert is_dir(os.path.join(BUILDTEST_ROOT, "site"))
