import os
import pytest
import uuid
from buildtest.menu.build import discover_configs

test_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root = os.path.dirname(test_root)


def test_discover_configs():

    # testing single file
    config = os.path.join(test_root, "testdir", "slurm-hello.yml")
    config_files = discover_configs(config)

    assert isinstance(config_files, list)
    assert config in config_files

    # testing with directory
    config_dir = os.path.join(test_root, "testdir")
    config_files = discover_configs(config_dir)

    assert isinstance(config_files, list)
    assert config in config_files

    # invalid file extension must be of type .yml or .yaml
    with pytest.raises(SystemExit) as e_info:
        discover_configs(os.path.join(root, "README.rst"))

    # when no config files found in a valid directory
    with pytest.raises(SystemExit) as e_info:
        # searching for all configs in current directory
        discover_configs(os.path.dirname(os.path.abspath(__file__)))

    # when you pass invalid file it should fail
    with pytest.raises(SystemExit) as e_info:
        invalid_file = str(uuid.uuid4())
        discover_configs(invalid_file)
