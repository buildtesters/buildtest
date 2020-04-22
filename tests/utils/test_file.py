import pytest
import os
import shutil
import uuid
from buildtest.utils.file import is_dir, is_file, create_dir, walk_tree, resolve_path, read_file, write_file
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

    file = os.path.join(tmp_path,"test.txt")

    print (f"Writing content to file: {file}")
    write_file(file, input)

    print(f"Reading content from file: {file}")
    content = read_file(file)

    # ensure return type of read_file is a list
    assert isinstance(content,list)
    # split origin input by newline to create a list
    input = input.splitlines(True)
    # perform a list equality between input content and result of read_file
    assert input == content

def test_write_file_exceptions(tmp_path):
    input = ["hi", "my", "name", "is", "Bob"]
    file = os.path.join(tmp_path,"name.txt")
    print(f"Writing content: {input} to file {file}")
    write_file(file,input)
    print("Writing to same file again, is not allowed!!!")
    # rewriting to same file is not allowed, expected return is 'None'
    assert not write_file(file,input)

    # testing invalid type for file stream, expected to return None
    assert not write_file(None,input)

    # testing if directory is passed as filepath, this is also not allowed, expected to return None
    assert not write_file(tmp_path,input)

def test_read_file(tmp_path):
    # testing invalid type for read_file, expects of type string. Expected return is 'None'
    print ("Reading file with invalid type, passing 'None'")
    assert not read_file(None)
    file = os.path.join(tmp_path,"hello.txt")
    print (f"Checking {file} is not a file." )
    # ensure file is not valid
    assert not is_file(file)

    print (f"Now reading an invalid file: {file}, expecting read_file to return 'None'")
    # checking invalid file returns None
    assert not read_file(file)
