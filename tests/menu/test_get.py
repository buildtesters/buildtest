import pytest
import shutil
from buildtest.menu.get import clone
from buildtest.utils.file import is_dir, create_dir


def test_clone(tmp_path):
    repo = "https://github.com/HPC-buildtest/tutorials.git"

    assert is_dir(clone(repo, tmp_path))

    # cloning same repo twice will result in failure
    with pytest.raises(SystemExit) as e_info:
        clone(repo, tmp_path)

    shutil.rmtree(tmp_path)
    # will fail to clone if invalid branch is specified
    with pytest.raises(SystemExit) as e_info:
        clone(repo, tmp_path, "develop")
