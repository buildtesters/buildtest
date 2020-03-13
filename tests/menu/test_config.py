import os
from buildtest.defaults import BUILDTEST_CONFIG_BACKUP_FILE
from buildtest.menu.config import show_configuration, func_config_view, func_config_restore
from buildtest.menu.show import show_schema_layout

def test_show_config():
    show_configuration()

def test_view_configuration():
    func_config_view()

def test_config_restore():
    func_config_restore()
    # removing backup file and testing of restore works
    os.remove(BUILDTEST_CONFIG_BACKUP_FILE)
    func_config_restore()


def test_show_schema():
    show_schema_layout()
