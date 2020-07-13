import os
import pytest
import uuid
from buildtest.config import load_settings
from buildtest.defaults import BUILDTEST_SETTINGS_FILE
from buildtest.menu.build import discover_buildspecs, func_build_subcmd
from buildtest.menu.repo import active_repos, func_repo_add, get_repo_paths

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
    class args:
        buildspec = ["examples"]
        debug = False
        settings = None
        testdir = None
        exclude = None

    buildtest_configuration = load_settings()

    tutorials = "buildtesters/tutorials"
    if tutorials not in active_repos():

        class repocmd:
            repo = "https://github.com/buildtesters/tutorials.git"
            branch = "master"

        func_repo_add(repocmd)

        assert tutorials in active_repos()

    func_build_subcmd(args, buildtest_configuration)

    repo_paths = get_repo_paths()
    prefix = repo_paths[0]

    class args:
        buildspec = [os.path.join(prefix, "examples")]
        debug = False
        settings = BUILDTEST_SETTINGS_FILE
        testdir = "/tmp"
        exclude = [os.path.join(prefix, "examples")]

    # this results in no buildspecs built
    with pytest.raises(SystemExit):
        func_build_subcmd(args, buildtest_configuration)
