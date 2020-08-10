import os
import pytest
import uuid
from buildtest.config import load_settings
from buildtest.defaults import BUILDTEST_SETTINGS_FILE
from buildtest.menu.build import discover_buildspecs, func_build_subcmd


test_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root = os.path.dirname(test_root)


def test_discover_buildspecs():

    # testing single file
    buildspec_dir = os.path.join(test_root, "examples", "buildspecs")

    # test single buildspec file
    buildspec = os.path.join(buildspec_dir, "environment.yml")
    # check file exists before sending to discover_buildspecs
    assert buildspec
    buildspec_files = discover_buildspecs(buildspec)

    assert isinstance(buildspec_files, list)
    assert buildspec in buildspec_files

    # testing with directory
    buildspec_files = discover_buildspecs(buildspec_dir)

    assert isinstance(buildspec_files, list)
    assert buildspec in buildspec_files

    # invalid file extension must be of type .yml or .yaml
    with pytest.raises(SystemExit):
        discover_buildspecs(os.path.join(root, "README.rst"))

    # when no Buildspec files found in a valid directory
    with pytest.raises(SystemExit):
        # searching for all Buildspecs in current directory
        discover_buildspecs(os.path.dirname(os.path.abspath(__file__)))

    # when you pass invalid file it should fail
    with pytest.raises(SystemExit):
        invalid_file = str(uuid.uuid4())
        discover_buildspecs(invalid_file)


def test_func_build_subcmd():
    buildspec_paths = os.path.join(test_root, "examples", "buildspecs")

    class args:
        buildspec = [buildspec_paths]
        debug = False
        settings = None
        testdir = None
        exclude = None
        tags = None

    buildtest_configuration = load_settings()

    func_build_subcmd(args, buildtest_configuration)

    class args:
        buildspec = [buildspec_paths]
        debug = False
        settings = BUILDTEST_SETTINGS_FILE
        testdir = "/tmp"
        exclude = [buildspec_paths]
        tags = None

    # this results in no buildspecs built
    with pytest.raises(SystemExit):
        func_build_subcmd(args, buildtest_configuration)
