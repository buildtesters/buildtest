import os
import pytest
import uuid
from buildtest.menu.build import discover_configs, exclude_configs

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

def test_exclude_configs():

    config = os.path.join(root,"examples","script")
    detected_config_files = discover_configs(config)


    exclude_list = None
    # nothing to exclude so normalized_config_files should be same as detected_config_files
    normalized_config_files = exclude_configs(detected_config_files, exclude_list)
    assert detected_config_files == normalized_config_files

    remove_config = os.path.join(config,"zlib.yml")
    remove_list = [remove_config]

    # check if examples/script/zlib.yml is detected
    assert remove_config in detected_config_files
    # now attempting to exclude examples/script/zlib.yml and checking if it is removed after exclusion
    normalized_config_files = exclude_configs(detected_config_files, remove_list)
    assert remove_config not in normalized_config_files

    remove_config = config
    remove_list = [remove_config]
    # this will do a directory exclusion in examples/script and since we are searching for same directory
    # this should return an empty list
    normalized_config_files = exclude_configs(detected_config_files, remove_list)

    assert not normalized_config_files