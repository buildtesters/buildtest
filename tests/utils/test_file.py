import os
import random
import shutil
import string
import tempfile
import uuid

import pytest
from buildtest.defaults import BUILDTEST_ROOT
from buildtest.exceptions import BuildTestError
from buildtest.utils.file import (
    create_dir,
    is_dir,
    is_file,
    is_symlink,
    load_json,
    read_file,
    remove_file,
    resolve_path,
    search_files,
    walk_tree,
    write_file,
)

here = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.utility
def test_checking_directory():
    dirname = str(uuid.uuid4())
    assert not is_dir(dirname)


@pytest.mark.utility
def test_checking_file():
    file_name = str(uuid.uuid4())
    assert not is_file(file_name)
    assert is_file("/bin/bash")


@pytest.mark.utility
def test_is_symlink():
    # Target path of the symbolic link
    link_target = tempfile.NamedTemporaryFile(dir=os.path.expanduser("~"))

    # Symbolic link path
    link_path = tempfile.NamedTemporaryFile(dir=os.path.expanduser("~"))

    link_path.close()

    # Create symbolic link
    os.symlink(link_target.name, link_path.name)

    # get filename from the path
    filename = os.path.basename(link_path.name)

    # test for shell expansion
    assert is_symlink(os.path.join("$HOME", filename))

    # test for user expansion
    assert is_symlink(os.path.join("~", filename))

    # test when link is not a symbolic link
    assert not is_symlink(link_target.name)

    # delete the target file path
    link_target.close()

    # test for broken symbolic link
    assert not is_symlink(link_path.name)

    # remove the symbolic link
    os.remove(link_path.name)


@pytest.mark.utility
def test_directory_expansion():
    dir1 = "$HOME"
    dir2 = "~"

    assert is_dir(dir1)
    assert is_dir(dir2)


@pytest.mark.utility
def test_create_dir(tmp_path):
    # since tmp_path creates a directory we will create a subdirectory "test" in tmp_path using create_dir
    assert is_dir(str(tmp_path))
    dirname = os.path.join(str(tmp_path), "test")
    # check we dont have a directory before creation
    assert not is_dir(dirname)
    # creating directory
    create_dir(dirname)
    # check if directory is created  after invoking create_dir
    assert is_dir(dirname)

    with pytest.raises(BuildTestError):
        create_dir("/xyz")


@pytest.mark.utility
def test_walk_tree():
    files = walk_tree(here)
    assert files

    list_of_files = walk_tree(here, ext=".py")
    print(f"Detected {len(list_of_files)} .py files found in directory: {here}")
    assert len(list_of_files) > 0

    # traverse by depth
    files = walk_tree(root_dir=BUILDTEST_ROOT, ext=".rst", max_depth=1)
    print(
        f"Detected {len(files)} .rst files found in directory: {BUILDTEST_ROOT} with max depth of 2"
    )
    assert len(files) > 0

    # traverse by directory using variable expansion
    files = walk_tree(root_dir="~", max_depth=1)
    print(
        f"Detected {len(files)} files found in directory: {os.path.expanduser('~')} with max depth of 1"
    )


def test_search_files():
    # search for all files ending in .py extension
    files = search_files(here, regex_pattern=r".py$")
    print(f"Detected {len(files)} .py files found in directory: {here}")
    assert files
    print(files)

    # search for all files ending in .rst or .sh extension
    files = search_files(BUILDTEST_ROOT, regex_pattern=r"(.rst|.sh)$")
    print(
        f"Detected {len(files)} .rst or .sh files found in directory: {BUILDTEST_ROOT}"
    )
    assert files
    print(files)

    # search for files with conf.py and main.py
    files = search_files("$BUILDTEST_ROOT", regex_pattern=r"(conf|main).py$")
    print(
        f"Detected {len(files)} conf.py or main.py files found in directory: {BUILDTEST_ROOT}"
    )
    assert files
    print(files)

    # search for file starting with 'buildtest' in directory $BUILDTEST_ROOT/bin
    files = search_files(
        "$BUILDTEST_ROOT/bin", regex_pattern=r"^buildtest$", max_depth=1
    )
    print(
        f"Detected file {files} found in directory: {os.path.join(BUILDTEST_ROOT,'bin')} with max depth of 1"
    )
    assert len(files) == 1
    print(files)

    # invalid regular expression will raise exception since re.compile will raise exception of type re.error. We also raise BuildTestError
    with pytest.raises(BuildTestError):
        search_files(here, regex_pattern=r"*foo[1-5]$", max_depth=1)


@pytest.mark.utility
def test_walk_tree_no_files(tmp_path):
    # need to convert tmp_path to str since its of type PosixPath
    list_of_files = walk_tree(str(tmp_path), ".py")
    print(
        f"Detected {len(list_of_files)} .py files found in directory: {str(tmp_path)}"
    )
    assert 0 == len(list_of_files)


@pytest.mark.utility
def test_walk_tree_invalid_dir(tmp_path):
    # we want to test an invalid directory so we remove temporary directory created by tmp_path
    shutil.rmtree(str(tmp_path))
    print(
        f"Removing directory: {tmp_path} first before doing directory traversal on invalid directory"
    )
    list_of_files = walk_tree(str(tmp_path), ".py")
    print(
        f"Returned following files: {list_of_files} with .py extension for path: {tmp_path}"
    )
    assert not list_of_files


@pytest.mark.utility
def test_write_file(tmp_path):
    msg = """This is a
    multi-line
    string"""

    file = os.path.join(tmp_path, "test_write.txt")

    print(f"Writing content to file: {file}")
    write_file(file, msg)

    print(f"Reading content from file: {file}")
    content = read_file(file)

    # ensure return type of read_file is a list
    assert isinstance(content, str)
    # split origin input by newline to create a list

    # perform a string equality between input content and result of read_file
    assert msg == content


@pytest.mark.utility
def test_write_file_exceptions(tmp_path):
    temporary_directory = str(tmp_path)
    msg = "hi my name is Bob"
    file = os.path.join(temporary_directory, "name.txt")
    print(f"Writing content: {msg} to file {file}")
    write_file(file, msg)

    # testing invalid type for file stream
    with pytest.raises(BuildTestError):
        print("Passing 'None' as input filestream to write_file")
        write_file(None, msg)

    assert is_dir(temporary_directory)
    # testing if directory is passed as filepath, this is also not allowed and expected to raise error
    with pytest.raises(BuildTestError):
        print(
            f"Passing directory: {temporary_directory} as input filestream to method write_file"
        )
        write_file(tmp_path, msg)

    filename = "".join(random.choices(string.ascii_letters, k=10))
    path = os.path.join("/", filename)
    print(f"Can't write to path: {path} due to permissions")

    with pytest.raises(BuildTestError):
        write_file(path, msg)

    # input content must be a string, will return None upon
    with pytest.raises(BuildTestError):
        write_file(os.path.join(tmp_path, "null.txt"), ["hi"])

    with tempfile.TemporaryDirectory() as tmpdir:
        print("Creating temporary directory: ", tmpdir)
        with pytest.raises(BuildTestError):
            write_file(tmpdir, "hello world")


@pytest.mark.utility
def test_read_file(tmp_path):
    # testing invalid type for read_file, expects of type string. Expected return is 'None'
    print("Reading file with invalid type, passing 'None'")
    with pytest.raises(BuildTestError):
        read_file(None)

    file = os.path.join(tmp_path, "hello.txt")
    print(f"Checking {file} is not a file.")
    # ensure file is not valid
    assert not is_file(file)

    print(f"Now reading an invalid file: {file}, expecting read_file to return 'None'")
    # checking invalid file should report an error
    with pytest.raises(BuildTestError):
        read_file(file)

    with tempfile.TemporaryDirectory() as tmpdir:
        fname = os.path.join(tmpdir, "permission-denied.txt")
        msg = "hello world"
        write_file(fname, msg)
        # make permission 000 so its unreadable
        os.chmod(fname, 000)
        with pytest.raises(BuildTestError):
            read_file(fname)

    print("Reading '/etc/shadow' will raise an exception BuildTestError")
    # reading /etc/shadow will raise a Permission error so we catch this exception BuildTestError
    with pytest.raises(BuildTestError):
        read_file("/etc/shadow")


@pytest.mark.utility
def test_resolve_path():
    assert resolve_path("$HOME")
    assert resolve_path("~")

    assert not resolve_path(None)

    random_name = "".join(random.choices(string.ascii_letters, k=10))
    # test a directory path that doesn't exist in $HOME with random key, but setting exist=False will return
    # path but doesn't mean file exists
    path = resolve_path(os.path.join("$HOME", random_name), exist=False)

    # checking if path is not file, or directory and not None. This is only valid when exist=False is set
    assert not is_file(path)
    assert not is_dir(path)
    assert path is not None

    with pytest.raises(BuildTestError):
        resolve_path(["/bin/bash"])


@pytest.mark.utility
def test_load_json():
    # passing None will raise an error
    with pytest.raises(BuildTestError):
        load_json(None)

    with pytest.raises(BuildTestError):
        random_name = "".join(random.choices(string.ascii_letters, k=10))
        load_json(random_name)


@pytest.mark.utility
def test_remove_file():
    assert not remove_file(None)

    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(BuildTestError):
            remove_file(tmpdir)

    tf = tempfile.NamedTemporaryFile(delete=False)
    remove_file(tf.name)
    print(f"Removing file: {tf.name}")
    assert not is_file(tf.name)

    # must be a string not a list
    with pytest.raises(BuildTestError):
        remove_file(["/bin/bash"])

    # removing a file like /bin/bash will raise an exception OSError and BuildTestError
    with pytest.raises(BuildTestError):
        remove_file("/bin/bash")
