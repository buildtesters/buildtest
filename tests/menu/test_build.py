import os
import pytest
import uuid
from buildtest.menu.build import discover_buildspecs

test_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root = os.path.dirname(test_root)


def test_discover_buildspecs():

    # testing single file
    buildspec = os.path.join(test_root, "testdir", "slurm-hello.yml")
    buildspec_files = discover_buildspecs(buildspec)

    assert isinstance(buildspec_files, list)
    assert buildspec in buildspec_files

    # testing with directory
    buildspec_dir = os.path.join(test_root, "testdir")
    buildspec_files = discover_buildspecs(buildspec_dir)

    assert isinstance(buildspec_files, list)
    assert buildspec in buildspec_files

    # invalid file extension must be of type .yml or .yaml
    with pytest.raises(SystemExit) as e_info:
        discover_buildspecs(os.path.join(root, "README.rst"))

    # when no Buildspec files found in a valid directory
    with pytest.raises(SystemExit) as e_info:
        # searching for all Buildspecs in current directory
        discover_buildspecs(os.path.dirname(os.path.abspath(__file__)))

    # when you pass invalid file it should fail
    with pytest.raises(SystemExit) as e_info:
        invalid_file = str(uuid.uuid4())
        discover_buildspecs(invalid_file)
