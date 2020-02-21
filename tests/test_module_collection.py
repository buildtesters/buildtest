import os
import pytest
from buildtest.tools.config import BUILDTEST_MODULE_COLLECTION_FILE
from buildtest.tools.modulesystem.collection import (
    add_collection,
    list_collection,
    clear_module_collection,
    remove_collection,
    update_collection,
    get_collection_length,
    check_module_collection,
    get_buildtest_module_collection,
)
from buildtest.tools.log import BuildTestError


def test_module_collection_add():
    add_collection()
    list_collection()


def test_remove_module_collection():
    add_collection()
    list_collection()
    remove_collection(0)


def test_clear_module_collection():
    clear_module_collection()


def test_collection_length_when_empty():
    clear_module_collection()
    assert 0 == get_collection_length()

    # listing module collection after clearing collection
    list_collection()
    # check all module collection when empty list
    check_module_collection()


def test_get_module_collection():
    clear_module_collection()
    add_collection()
    module_list = get_buildtest_module_collection(0)
    assert len(module_list) > 0


def test_check_collection():
    add_collection()
    check_module_collection()
    clear_module_collection()


def test_update_collection():
    """Test to see if we can update a module collection. This test will add the active modules and overwrite with same module
    collection in index 0"""
    add_collection()
    update_collection(0)
    clear_module_collection()


def test_collection_check_when_file_not_found():
    os.remove(BUILDTEST_MODULE_COLLECTION_FILE)
    check_module_collection()


@pytest.mark.xfail(
    reason="When collection file is not found, we can't remove a module collection ",
    raises=BuildTestError,
)
def test_collection_remove_when_file_not_found():
    os.remove(BUILDTEST_MODULE_COLLECTION_FILE)
    remove_collection(0)


@pytest.mark.xfail(
    reason="When collection file is not found, we can't update a module collection ",
    raises=BuildTestError,
)
def test_collection_update_when_file_not_found():
    os.remove(BUILDTEST_MODULE_COLLECTION_FILE)
    update_collection(0)


@pytest.mark.xfail(
    reason="When collection file is not found, we can't list a module collection ",
    raises=BuildTestError,
)
def test_collection_list_when_file_not_found():
    os.remove(BUILDTEST_MODULE_COLLECTION_FILE)
    list_collection()


def test_collection_list_when_file_not_found():
    os.remove(BUILDTEST_MODULE_COLLECTION_FILE)
    assert 0 == get_collection_length()
