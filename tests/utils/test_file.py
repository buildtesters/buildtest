import pytest
import os
import shutil
import uuid
from buildtest.utils.file import is_dir, is_file, create_dir, walk_tree, resolve_path
from buildtest.exceptions import BuildTestError

here = os.path.dirname(os.path.abspath(__file__))


def test_checking_directory():
    dirname = str(uuid.uuid4())
    assert not is_dir(dirname)


@pytest.mark.xfail(
    reason="Test expected to fail when checking an obscure file", raises=BuildTestError
)
def test_checking_file():
    file_name = str(uuid.uuid4())
    assert not is_file(file_name)

    file1 = "~/.profile"
    file2 = "$HOME/.profile"

    assert is_file(file1)
    assert is_file(file2)


def test_directory_expansion():
    dir1 = "$HOME"
    dir2 = "~"

    assert is_dir(dir1)
    assert is_dir(dir2)


def test_create_dir(tmp_path):
    # since tmp_path creates a directory we will create a subdirectory "test" in tmp_path using create_dir
    assert is_dir(tmp_path)
    dirname = os.path.join(tmp_path, "test")
    # check we dont have a directory before creation
    assert not is_dir(dirname)
    # creating directory
    create_dir(dirname)
    # check if directory is created  after invoking create_dir
    assert is_dir(dirname)


@pytest.mark.xfail(
    reason="This test is expected to fail due to insufficient privileges",
    raises=OSError,
)
def test_fail_create_dir():
    create_dir("/xyz")


def test_walk_tree():
    list_of_files = walk_tree(here, ".py")
    assert len(list_of_files) > 0


@pytest.mark.xfail(
    reason="This test is expected to fail since we passed invalid path for directory traversal",
    raises=BuildTestError,
)
def test_walk_tree_invalid_dir():
    walk_tree("/xyz", ".py")
