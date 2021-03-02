import os
import pytest
import tempfile

from buildtest.defaults import BUILDTEST_ROOT, DEFAULT_SETTINGS_FILE
from buildtest.menu.build import BuildTest
from buildtest.menu.buildspec import func_buildspec_find
from buildtest.exceptions import BuildTestError

test_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root = os.path.dirname(test_root)
valid_buildspecs = os.path.join(test_root, "buildsystem", "valid_buildspecs")


@pytest.mark.cli
def test_build_by_tags():

    # ensure we rebuild cache file before running by tags
    # rerunning buildtest buildspec find without --rebuild option this will read from cache file
    class args:
        find = True
        rebuild = True
        root = None
        buildspec_files = False
        executors = False
        tags = False
        paths = False
        group_by_tags = False
        group_by_executor = False
        maintainers = False
        maintainers_by_buildspecs = False
        filter = None
        format = None
        helpfilter = False
        helpformat = False

    func_buildspec_find(args, settings_file=DEFAULT_SETTINGS_FILE)

    #  testing buildtest build --tags pass
    cmd = BuildTest(config_file=DEFAULT_SETTINGS_FILE, tags=["pass"])
    cmd.build()

    class args:
        buildspec = [os.path.join(test_root, "tutorials")]
        debug = False
        stage = None
        testdir = None
        exclude = None
        tags = ["fail", "python"]
        executor = None
        filter_tags = None
        rebuild = None

    #  testing buildtest build --tags fail --tags python --buildspec tutorials
    cmd = BuildTest(
        config_file=DEFAULT_SETTINGS_FILE,
        buildspecs=[os.path.join(test_root, "tutorials")],
        tags=["fail", "python"],
    )
    cmd.build()

    class args:
        buildspec = None
        debug = False
        stage = None
        testdir = None
        exclude = None
        tags = ["pass"]
        executor = None
        filter_tags = ["pass"]
        rebuild = None

    #  testing buildtest build --tags pass --tags pass
    cmd = BuildTest(
        config_file=DEFAULT_SETTINGS_FILE, tags=["pass"], filter_tags=["pass"]
    )
    cmd.build()


@pytest.mark.cli
def test_build_buildspecs():
    buildspec_paths = os.path.join(test_root, "buildsystem", "valid_buildspecs")

    #  testing buildtest build --buildspec tests/buildsystem/valid_buildspecs
    cmd = BuildTest(config_file=DEFAULT_SETTINGS_FILE, buildspecs=[buildspec_paths])
    cmd.build()

    #  testing buildtest build --buildspec tests/examples/buildspecs --exclude tests/examples/buildspecs
    # this results in no buildspecs built
    with pytest.raises(SystemExit):
        cmd = BuildTest(
            config_file=DEFAULT_SETTINGS_FILE,
            buildspecs=[buildspec_paths],
            exclude_buildspecs=[buildspec_paths],
        )
        cmd.build()


@pytest.mark.cli
def test_buildspec_tag_executor():
    class args:
        executor = ["generic.local.sh"]
        tags = ["fail"]
        buildspec = None
        debug = False
        stage = None
        testdir = None
        exclude = None
        filter_tags = None
        rebuild = None

    # testing buildtest build --tags fail --executor generic.local.sh
    cmd = BuildTest(
        config_file=DEFAULT_SETTINGS_FILE, tags=["fail"], executors=["generic.local.sh"]
    )
    cmd.build()


@pytest.mark.cli
def test_build_multi_executors():
    class args:
        executor = ["generic.local.sh", "generic.local.python"]
        buildspec = None
        debug = False
        stage = None
        testdir = None
        exclude = None
        tags = None
        filter_tags = None
        rebuild = None

    # testing buildtest build --executor generic.local.sh --executor generic.local.python
    cmd = BuildTest(
        config_file=DEFAULT_SETTINGS_FILE,
        executors=["generic.local.sh", "generic.local.python"],
    )
    cmd.build()


@pytest.mark.cli
def test_build_by_stages():

    # testing buildtest build --tags python --stage=parse
    cmd = BuildTest(config_file=DEFAULT_SETTINGS_FILE, tags=["python"], stage="parse")
    cmd.build()

    # testing buildtest build --tags tutorials --stage=build
    cmd = BuildTest(config_file=DEFAULT_SETTINGS_FILE, tags=["python"], stage="build")
    cmd.build()


@pytest.mark.cli
def test_build_rebuild():

    buildspec_file = os.path.join(BUILDTEST_ROOT, "tutorials", "python-shell.yml")

    # rebuild 5 times (buildtest build -b tutorials/python-shell.yml --rebuild=5
    cmd = BuildTest(
        config_file=DEFAULT_SETTINGS_FILE, buildspecs=[buildspec_file], rebuild=5
    )
    cmd.build()


def test_discover():

    # test single buildspec file
    buildspec = [os.path.join(valid_buildspecs, "environment.yml")]

    cmd = BuildTest(config_file=DEFAULT_SETTINGS_FILE, buildspecs=buildspec)
    cmd.discover_buildspecs()
    assert buildspec == cmd.detected_buildspecs

    # testing buildspecs in directory
    cmd = BuildTest(config_file=DEFAULT_SETTINGS_FILE, buildspecs=[valid_buildspecs])
    cmd.discover_buildspecs()
    assert cmd.detected_buildspecs

    buildspec = [os.path.join(root, "README.rst")]
    # testing invalid extension this will raise an error
    cmd = BuildTest(config_file=DEFAULT_SETTINGS_FILE, buildspecs=buildspec)
    with pytest.raises(SystemExit):
        cmd.discover_buildspecs()

    tempdir = tempfile.TemporaryDirectory()
    # passing an empty directory will raise an error because no .yml extensions found
    cmd = BuildTest(config_file=DEFAULT_SETTINGS_FILE, buildspecs=[tempdir.name])
    with pytest.raises(SystemExit):
        cmd.discover_buildspecs()

    buildspec = []
    # passing no buildspecs will result in error
    cmd = BuildTest(config_file=DEFAULT_SETTINGS_FILE, buildspecs=buildspec)
    with pytest.raises(SystemExit):
        cmd.discover_buildspecs()


def test_BuildTest_type():

    # buildspec must be a list not a string
    buildspec = os.path.join(valid_buildspecs, "environment.yml")
    with pytest.raises(BuildTestError):
        BuildTest(config_file=DEFAULT_SETTINGS_FILE, buildspecs=buildspec)

    # invalid value for exclude buildspecs must be a list
    with pytest.raises(BuildTestError):
        BuildTest(
            config_file=DEFAULT_SETTINGS_FILE,
            buildspecs=[buildspec],
            exclude_buildspecs=buildspec,
        )

    # tags must be a list not a string
    with pytest.raises(BuildTestError):
        BuildTest(config_file=DEFAULT_SETTINGS_FILE, tags="pass")

    # tags must be a list not a string
    with pytest.raises(BuildTestError):
        BuildTest(config_file=DEFAULT_SETTINGS_FILE, executors="generic.local.bash")

    # filter_Tags must be a list not a string
    with pytest.raises(BuildTestError):
        BuildTest(config_file=DEFAULT_SETTINGS_FILE, tags=["pass"], filter_tags="pass")

    # invalid type for stage argument, must be a string not list
    with pytest.raises(BuildTestError):
        BuildTest(config_file=DEFAULT_SETTINGS_FILE, tags=["pass"], stage=["parse"])

    # invalid value for stage argument, must be 'parse' or 'build'
    with pytest.raises(BuildTestError):
        BuildTest(config_file=DEFAULT_SETTINGS_FILE, tags=["pass"], stage="unknown")

    # invalid value for testdir argument, must be a str
    with pytest.raises(BuildTestError):
        BuildTest(
            config_file=DEFAULT_SETTINGS_FILE,
            tags=["pass"],
            testdir=list(BUILDTEST_ROOT),
        )

    # invalid type for rebuild argument, must be an int not string
    with pytest.raises(BuildTestError):
        BuildTest(config_file=DEFAULT_SETTINGS_FILE, tags=["pass"], rebuild="1")
