import os
import pytest
import shutil
from buildtest.defaults import TESTCONFIG_ROOT
from buildtest.menu.get import clone
from buildtest.utils.file import is_dir, create_dir

def test_clone():
    repo = "https://github.com/HPC-buildtest/tutorials.git"
    root = os.path.join(TESTCONFIG_ROOT, "github.com")

    if is_dir(root):
        shutil.rmtree(root)

    create_dir(root)

    assert is_dir(clone(repo,root))

    # cloning same repo twice will result in failure
    with pytest.raises(SystemExit) as e_info:
        clone(repo,root)

    shutil.rmtree(root)
    # will fail to clone if invalid branch is specified
    with pytest.raises(SystemExit) as e_info:
        clone(repo,root,"develop")