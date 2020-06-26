import pytest
import os
import random
import shutil
import string
import uuid
from buildtest.utils.file import (
    is_dir,
    is_file,
    create_dir,
    walk_tree,
    read_file,
    write_file,
    resolve_path,
)
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
    print(f"Detected {len(list_of_files)} .py files found in directory: {here}")
    assert len(list_of_files) > 0


def test_walk_tree_no_files(tmp_path):
    list_of_files = walk_tree(tmp_path, ".py")
    print(f"Detected {len(list_of_files)} .py files found in directory: {tmp_path}")
    assert 0 == len(list_of_files)


def test_walk_tree_invalid_dir(tmp_path):
    # we want to test an invalid directory so we remove temporary directory created by tmp_path
    shutil.rmtree(tmp_path)
    print(
        f"Removing directory: {tmp_path} first before doing directory traversal on invalid directory"
    )
    list_of_files = walk_tree(tmp_path, ".py")
    print(
        f"Returned following files: {list_of_files} with .py extension for path: {tmp_path}"
    )
    assert not list_of_files


def test_write_file(tmp_path):
    input = """This is a 
    multi-line
    string"""

    file = os.path.join(tmp_path, "test_write.txt")

    print(f"Writing content to file: {file}")
    write_file(file, input)

    print(f"Reading content from file: {file}")
    content = read_file(file)

    # ensure return type of read_file is a list
    assert isinstance(content, str)
    # split origin input by newline to create a list

    # perform a string equality between input content and result of read_file
    assert input == content


def test_write_file_exceptions(tmp_path):
    input = "hi my name is Bob"
    file = os.path.join(tmp_path, "name.txt")
    print(f"Writing content: {input} to file {file}")
    write_file(file, input)

    # testing invalid type for file stream
    with pytest.raises(SystemExit):
        print("Passing 'None' as input filestream to write_file")
        write_file(None, input)

    assert is_dir(tmp_path)
    # testing if directory is passed as filepath, this is also not allowed and expected to raise error
    with pytest.raises(SystemExit):
        print(f"Passing directory: {tmp_path} as input filestream to method write_file")
        write_file(tmp_path, input)

    filename = "".join(random.choice(string.ascii_letters) for i in range(10))
    path = os.path.join("/", filename)
    print(f"Can't write to path: {path} due to permissions")

    with pytest.raises(BuildTestError):
        write_file(path, input)

    # input content must be a string, will return None upon
    assert not write_file(os.path.join(tmp_path, "null.txt"), ["hi"])


def test_read_file(tmp_path):
    # testing invalid type for read_file, expects of type string. Expected return is 'None'
    print("Reading file with invalid type, passing 'None'")
    with pytest.raises(SystemExit):
        read_file(None)

    file = os.path.join(tmp_path, "hello.txt")
    print(f"Checking {file} is not a file.")
    # ensure file is not valid
    assert not is_file(file)

    print(f"Now reading an invalid file: {file}, expecting read_file to return 'None'")
    # checking invalid file should report an error
    with pytest.raises(SystemExit):
        read_file(file)

    print("Reading '/etc/shadow' will raise an exception BuildTestError")
    # reading /etc/shadow will raise a Permission error so we catch this exception BuildTestError
    with pytest.raises(BuildTestError):
        read_file("/etc/shadow")


def test_resolve_path():
    assert resolve_path("$HOME")
    assert resolve_path("~")

    random_name = "".join(random.choice(string.ascii_letters) for i in range(10))
    # test a directory path that doesn't exist in $HOME with random key, but setting exist=False will return
    # path but doesn't mean file exists
    path = resolve_path(os.path.join("$HOME", random_name), exist=False)

    # checking if path is not file, or directory and not None. This is only valid when exist=False is set
    assert not is_file(path)
    assert not is_dir(path)
    assert path is not None
