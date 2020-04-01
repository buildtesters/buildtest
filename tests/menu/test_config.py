import os
import pytest
from jsonschema import validate, ValidationError
from buildtest.defaults import BUILDTEST_CONFIG_BACKUP_FILE, DEFAULT_CONFIG_SCHEMA
from buildtest.menu.config import (
    func_config_view,
    func_config_restore,
)
from buildtest.utils.file import walk_tree
from buildtest.buildsystem.schemas.utils import load_schema

pytest_root = os.path.dirname(os.path.dirname(__file__))


def test_view_configuration():
    func_config_view()


def test_config_restore():
    func_config_restore()
    # removing backup file and testing of restore works
    os.remove(BUILDTEST_CONFIG_BACKUP_FILE)
    func_config_restore()

def test_valid_config_schemas():

    valid_schema_dir = os.path.join(pytest_root,"examples","config_schemas","valid")
    schema_config = load_schema(DEFAULT_CONFIG_SCHEMA)
    for schema in walk_tree(valid_schema_dir,".yml"):        
        example = load_schema(os.path.abspath(schema))
        validate(instance=example, schema=schema_config)