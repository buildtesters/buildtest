import os
import random
import shutil
import string
import tempfile
import unittest
import uuid

import pytest
from buildtest.exceptions import BuildTestError
from buildtest.utils.file import (
    create_dir,
    create_file,
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


def test_create_file():
    dirname = tempfile.mkdtemp()
    create_file(os.path.join(dirname, "test.txt"))

    with pytest.raises(BuildTestError):
        create_file("/xyz.txt")


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


class TestWalkTree(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory with some files for testing
        self.tempdir = tempfile.TemporaryDirectory()
        self.filepaths = [
            os.path.join(self.tempdir.name, "file1.txt"),
            os.path.join(self.tempdir.name, "file2.txt"),
            os.path.join(self.tempdir.name, "file3.doc"),
            os.path.join(self.tempdir.name, "subdir", "file4.txt"),
            os.path.join(self.tempdir.name, "subdir", "file5.txt"),
            os.path.join(self.tempdir.name, "subdir", "file6.doc"),
            os.path.join(self.tempdir.name, "subdir2", "file7.txt"),
            os.path.join(self.tempdir.name, "subdir2", "file8.doc"),
        ]
        os.makedirs(os.path.join(self.tempdir.name, "subdir"))
        os.makedirs(os.path.join(self.tempdir.name, "subdir2"))
        for filepath in self.filepaths:
            create_file(filepath)

    def test_walk_tree_no_ext(self):
        result = walk_tree(self.tempdir.name)
        assert len(result) == 8

    def test_walk_tree_single_ext(self):
        result = walk_tree(self.tempdir.name, ext=".txt")
        # check all resulting files have extension .txt
        for fname in result:
            assert fname.endswith(".txt")

    def test_walk_tree_multiple_ext(self):
        result = walk_tree(self.tempdir.name, ext=[".txt", ".doc"])
        # check all resulting files with extensions .txt and .doc
        for fname in result:
            assert fname.endswith(".txt") or fname.endswith(".doc")

    def test_walk_tree_no_files(self):
        result = walk_tree(self.tempdir.name, ext=".xyz")
        assert len(result) == 0

    def test_walk_tree_invalid_directory(self):
        result = walk_tree("/xyz")
        assert len(result) == 0

    def test_walk_tree_max_depth(self):
        result = walk_tree(self.tempdir.name, max_depth=1)
        assert len(result) == 3

    def test_walk_tree_numfiles(self):
        result = walk_tree(self.tempdir.name, numfiles=2)
        assert len(result) == 2

    def test_walk_tree_file_traverse_limit(self):
        result = walk_tree(self.tempdir.name, file_traverse_limit=6)
        assert len(result) == 6

    def test_walk_tree_by_directory(self):
        result = walk_tree(self.tempdir.name, file_type="dir")
        assert len(result) == 3

    def test_walk_tree_by_symlink(self):
        os.symlink(self.filepaths[0], os.path.join(self.tempdir.name, "file1.link"))
        result = walk_tree(self.tempdir.name, file_type="symlink")
        assert len(result) == 1

        os.symlink(self.filepaths[0], os.path.join(self.tempdir.name, "file1.rst"))
        os.symlink(self.filepaths[0], os.path.join(self.tempdir.name, "file1.md"))
        result = walk_tree(self.tempdir.name, file_type="symlink", ext=[".rst", ".md"])
        assert len(result) == 2

    def tearDown(self):
        self.tempdir.cleanup()


class TestSearchFiles(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.files = [
            "file1.txt",
            "file2.jpg",
            "file3.txt",
            "file4.jpg",
            "file5.txt",
        ]
        for f in self.files:
            create_file(os.path.join(self.temp_dir, f))

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_search_files_with_pattern(self):
        # Test searching files with regex pattern
        result = search_files(self.temp_dir, r"^file\d+\.txt$")
        assert len(result) == 3

    def test_search_files_with_numfiles(self):
        # Test searching files with numfiles parameter
        result = search_files(self.temp_dir, r".*", numfiles=3)
        assert len(result) == 3

    def test_search_files_with_max_depth(self):
        # Test searching files with max_depth parameter
        subdir_path = os.path.join(self.temp_dir, "subdir")
        os.mkdir(subdir_path)

        create_file(os.path.join(subdir_path, "subfile.txt"))

        result = search_files(subdir_path, r".*", max_depth=1)
        assert len(result) == 1

    def test_search_files_invalid_directory(self):
        result = search_files(root_dir="/xyz", regex_pattern=r".*")
        print(result)
        assert len(result) == 0

    def test_search_files_home_dir(self):
        # search for files based on variable expansion $HOME
        result = search_files(
            root_dir="$HOME", regex_pattern=r".*", file_traverse_limit=10
        )
        assert len(result) == 10

        result = search_files(root_dir="~", regex_pattern=r".*", file_traverse_limit=10)
        assert len(result) == 10

    def test_search_files_invalid_regex(self):
        # invalid regular expression will return an empty list
        files = search_files(here, regex_pattern=r"*foo[1-5]$", max_depth=1)
        assert len(files) == 0

    def test_search_files_by_symlink(self):
        # create a symlink to a file
        os.symlink(
            os.path.join(self.temp_dir, self.files[0]),
            os.path.join(self.temp_dir, f"{self.files[0]}.link"),
        )
        result = search_files(self.temp_dir, r".*", file_type="symlink")
        assert len(result) == 1

    def test_search_files_by_directory(self):
        result = search_files(self.temp_dir, r".*", file_type="dir")
        assert len(result) == 1

        for subdir in ["subdir1", "subdir2", "subdir3"]:
            os.mkdir(os.path.join(self.temp_dir, subdir))

        result = search_files(self.temp_dir, r".*", file_type="dir")
        assert len(result) == 4


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
