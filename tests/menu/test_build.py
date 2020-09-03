import os
import pytest
import uuid
from buildtest.config import load_settings
from buildtest.defaults import BUILDTEST_SETTINGS_FILE
from buildtest.menu.build import discover_buildspecs, func_build_subcmd
from buildtest.menu.buildspec import func_buildspec_find

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

    invalid_file = str(uuid.uuid4())
    assert not discover_buildspecs(invalid_file)


def test_build_buildspecs():
    buildspec_paths = os.path.join(test_root, "examples", "buildspecs")
    buildtest_configuration = load_settings()

    class args:
        buildspec = [buildspec_paths]
        debug = False
        stage = None
        settings = None
        testdir = None
        exclude = None
        tags = None

    #  testing buildtest build --buildspec tests/examples/buildspecs
    func_build_subcmd(args, buildtest_configuration)

    class args:
        buildspec = [buildspec_paths]
        debug = False
        stage = None
        settings = BUILDTEST_SETTINGS_FILE
        testdir = "/tmp"
        exclude = [buildspec_paths]
        tags = None

    #  testing buildtest build --buildspec tests/examples/buildspecs --exclude tests/examples/buildspecs
    # this results in no buildspecs built
    with pytest.raises(SystemExit):
        func_build_subcmd(args, buildtest_configuration)


def test_build_by_tags():

    # ensure we rebuild cache file before running by tags
    # rerunning buildtest buildspec find without --clear option this will read from cache file
    class args:
        find = True
        clear = False
        tags = False
        buildspec_files = False

    func_buildspec_find(args)

    buildtest_configuration = load_settings()

    class args:
        buildspec = None
        debug = False
        stage = None
        settings = BUILDTEST_SETTINGS_FILE
        testdir = None
        exclude = None
        tags = "tutorials"

    #  testing buildtest build --tags tutorials
    func_build_subcmd(args, buildtest_configuration)


def test_build_by_stages():

    buildtest_configuration = load_settings()

    class args:
        buildspec = None
        debug = False
        stage = "parse"
        settings = BUILDTEST_SETTINGS_FILE
        testdir = None
        exclude = None
        tags = "tutorials"

    # testing buildtest build --tags tutorials --stage=parse
    func_build_subcmd(args, buildtest_configuration)

    class args:
        buildspec = None
        debug = False
        stage = "build"
        settings = BUILDTEST_SETTINGS_FILE
        testdir = None
        exclude = None
        tags = "tutorials"

    # testing buildtest build --tags tutorials --stage=build
    func_build_subcmd(args, buildtest_configuration)
