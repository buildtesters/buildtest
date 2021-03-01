import os
import pytest
import uuid
from buildtest.config import load_settings
from buildtest.defaults import BUILDTEST_ROOT
from buildtest.menu.build import (
    discover_by_buildspecs,
    discover_buildspecs,
    func_build_subcmd,
)
from buildtest.menu.buildspec import func_buildspec_find

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

    func_buildspec_find(args)

    class args:
        buildspec = None
        debug = False
        stage = None
        testdir = None
        exclude = None
        tags = ["pass"]
        executor = None
        filter_tags = None
        rebuild = None

    #  testing buildtest build --tags pass
    func_build_subcmd(args)

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

    #  testing buildtest build --tags fail --tags python
    func_build_subcmd(args)

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
    func_build_subcmd(args)


@pytest.mark.cli
def test_build_buildspecs():
    buildspec_paths = os.path.join(test_root, "buildsystem", "valid_buildspecs")

    class args:
        buildspec = [buildspec_paths]
        debug = False
        stage = None
        testdir = None
        exclude = None
        tags = None
        executor = None
        filter_tags = None
        rebuild = None

    #  testing buildtest build --buildspec tests/examples/buildspecs
    func_build_subcmd(args)

    class args:
        buildspec = [buildspec_paths]
        debug = False
        stage = None
        testdir = None
        exclude = [buildspec_paths]
        tags = None
        executor = None
        filter_tags = None
        rebuild = None

    #  testing buildtest build --buildspec tests/examples/buildspecs --exclude tests/examples/buildspecs
    # this results in no buildspecs built
    with pytest.raises(SystemExit):
        func_build_subcmd(args)


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

    # testing buildtest build --tags fail --executor local.sh
    func_build_subcmd(args)


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

    # testing buildtest build --executor local.sh --executor local.python
    func_build_subcmd(args)


@pytest.mark.cli
def test_build_by_stages():
    class args:
        buildspec = None
        debug = False
        stage = "parse"
        testdir = None
        exclude = None
        tags = ["python"]
        executor = None
        filter_tags = None
        rebuild = None

    # testing buildtest build --tags python --stage=parse
    func_build_subcmd(args)

    class args:
        buildspec = None
        debug = False
        stage = "build"
        testdir = None
        exclude = None
        tags = ["python"]
        executor = None
        filter_tags = None
        rebuild = None

    # testing buildtest build --tags tutorials --stage=build
    func_build_subcmd(args)


@pytest.mark.cli
def test_build_rebuild():

    buildspec_file = os.path.join(BUILDTEST_ROOT, "tutorials", "python-shell.yml")

    class args:
        buildspec = [buildspec_file]
        debug = False
        stage = None
        testdir = None
        exclude = None
        tags = None
        executor = None
        filter_tags = None
        rebuild = 5

    # rebuild 5 times (buildtest build -b tutorials/python-shell.yml --rebuild=5
    func_build_subcmd(args)


def test_discover_by_buildspecs(tmpdir):

    # test single buildspec file
    buildspec = os.path.join(valid_buildspecs, "environment.yml")
    # check file exists before sending to discover_buildspecs
    assert buildspec
    buildspec_files = discover_by_buildspecs(buildspec)

    assert isinstance(buildspec_files, list)
    assert buildspec in buildspec_files

    # testing with directory
    buildspec_files = discover_by_buildspecs(valid_buildspecs)

    # check if return is a list and environment.yml exists in list
    assert isinstance(buildspec_files, list)
    assert buildspec in buildspec_files

    # invalid file extension must be of type .yml
    assert not discover_by_buildspecs(os.path.join(root, "README.rst"))

    print(
        f"Searching for buildspecs in directory: {tmpdir} which should have no .yml files"
    )
    # when no Buildspec files found in a valid directory
    assert not discover_by_buildspecs(tmpdir)

    invalid_file = str(uuid.uuid4())
    assert not discover_by_buildspecs(invalid_file)


def test_discover_buildspec():
    # this should raise an error since no buildspecs are specified
    with pytest.raises(SystemExit):
        discover_buildspecs()

    bp = [os.path.join(BUILDTEST_ROOT, "README.rst")]

    with pytest.raises(SystemExit):
        discover_buildspecs(buildspec=bp)

    # this should raise AssertionError if we pass a string for buildspec argument, it expects a list
    with pytest.raises(AssertionError):
        discover_buildspecs(buildspec=bp[0])

    input_buildspec = [os.path.join(valid_buildspecs, "environment.yml")]
    # this should raise AssertionError if we pass a string for exclude_buildspec it expects a list
    with pytest.raises(AssertionError):
        discover_buildspecs(
            buildspec=input_buildspec, exclude_buildspec=input_buildspec[0]
        )

    # The test below will discover and negate all buildspecs which raises an exception of type SystemExit
    with pytest.raises(SystemExit):
        discover_buildspecs(
            buildspec=[valid_buildspecs], exclude_buildspec=[valid_buildspecs]
        )

    input_bps = [
        os.path.join(BUILDTEST_ROOT, "README.rst"),
        os.path.join(BUILDTEST_ROOT, "tutorials"),
    ]
    exclude_bps = [os.path.join(BUILDTEST_ROOT, "tutorials", "compilers")]

    discovered_bp, excluded_bp = discover_buildspecs(
        buildspec=input_bps, exclude_buildspec=exclude_bps
    )
    print("discovered:", discovered_bp)
    print("excluded:", exclude_bps)
    # assert both discovered_bp and excluded_bp are not None
    assert discovered_bp
    assert excluded_bp

    # testing by tags and input buildspecs but not excluding any buildspecs
    discovered_bp, exclude_bps = discover_buildspecs(
        tags=["tutorials"], buildspec=input_bps
    )
    # ensure that discovered buildspec is not None and exclude_bps should be empty list
    assert discovered_bp
    assert not exclude_bps

    # the tags field expect a list when searching in cache, passing a string will raise AssertionError
    with pytest.raises(AssertionError):
        discover_buildspecs(tags="tutorials")
