import os
import shutil
from buildtest.defaults import BUILDTEST_CONFIG_FILE, BUILDTEST_ROOT
from buildtest.config import (
    load_configuration,
    check_configuration,
    get_default_configuration,
    create_config_file,
    init,
)
from buildtest.utils.file import is_file, is_dir


def test_load_and_check_configuration():

    load_configuration(BUILDTEST_CONFIG_FILE)
    assert os.path.exists(BUILDTEST_CONFIG_FILE)

    check_configuration()


def test_get_default_configuration():

    config_opts = get_default_configuration()
    assert isinstance(config_opts, dict)

    assert "editor" in config_opts.keys()
    assert "executors" in config_opts.keys()


def test_create_config_file():

    os.remove(BUILDTEST_CONFIG_FILE)
    create_config_file()
    assert is_file(BUILDTEST_CONFIG_FILE)


def test_init_creation_of_buildtest_dir():

    shutil.rmtree(BUILDTEST_ROOT)
    init()
    assert is_dir(os.path.join(BUILDTEST_ROOT, "root"))
    assert is_dir(os.path.join(BUILDTEST_ROOT, "site"))
