import os
import pytest
import tempfile

from buildtest.defaults import BUILDTEST_ROOT
from buildtest.exceptions import BuildTestError
from buildtest.config import SiteConfiguration
from buildtest.cli.build import BuildTest, discover_buildspecs
from buildtest.cli.buildspec import BuildspecCache
from buildtest.utils.file import walk_tree
from buildtest.system import BuildTestSystem

test_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root = os.path.dirname(test_root)
valid_buildspecs = os.path.join(test_root, "buildsystem", "valid_buildspecs")

configuration = SiteConfiguration()
configuration.detect_system()
configuration.validate()


@pytest.mark.cli
def test_build_by_tags():

    system = BuildTestSystem()
    system.check()

    # ensure we rebuild cache file before running any buildspecs commands
    BuildspecCache(rebuild=True, configuration=configuration)

    #  testing buildtest build --tags pass
    cmd = BuildTest(configuration=configuration, tags=["pass"], buildtest_system=system)
    cmd.build()

    #  testing buildtest build --tags fail --tags python --buildspec tutorials
    cmd = BuildTest(
        configuration=configuration,
        buildspecs=[os.path.join(test_root, "tutorials")],
        tags=["fail", "python"],
        buildtest_system=system,
    )
    cmd.build()

    #  testing buildtest build --tags pass --tags pass
    cmd = BuildTest(
        configuration=configuration,
        tags=["pass"],
        filter_tags=["pass"],
        buildtest_system=system,
    )
    cmd.build()


@pytest.mark.cli
def test_build_buildspecs():

    system = BuildTestSystem()
    system.check()

    buildspec_paths = os.path.join(test_root, "buildsystem", "valid_buildspecs")

    #  testing buildtest build --buildspec tests/buildsystem/valid_buildspecs
    cmd = BuildTest(
        configuration=configuration,
        buildspecs=[buildspec_paths],
        buildtest_system=system,
    )
    cmd.build()

    excluded_buildspecs = walk_tree(buildspec_paths, ".yml")
    assert len(excluded_buildspecs) > 0
    #  testing buildtest build --buildspec tests/buildsystem/valid_buildspecs and exclude the first buildspec
    cmd = BuildTest(
        configuration=configuration,
        buildspecs=[buildspec_paths],
        exclude_buildspecs=[excluded_buildspecs[0]],
        buildtest_system=system,
    )
    cmd.build()

    #  testing buildtest build --buildspec tests/examples/buildspecs --exclude tests/examples/buildspecs
    # this results in no buildspecs built
    with pytest.raises(SystemExit):
        cmd = BuildTest(
            configuration=configuration,
            buildspecs=[buildspec_paths],
            exclude_buildspecs=[buildspec_paths],
            buildtest_system=system,
        )
        cmd.build()


@pytest.mark.cli
def test_buildspec_tag_executor():

    system = BuildTestSystem()
    system.check()

    # testing buildtest build --tags fail --executor generic.local.csh
    cmd = BuildTest(
        configuration=configuration,
        tags=["fail"],
        executors=["generic.local.csh"],
        buildtest_system=system,
    )
    cmd.build()


@pytest.mark.cli
def test_build_multi_executors():

    system = BuildTestSystem()
    system.check()

    # testing buildtest build --executor generic.local.csh --executor generic.local.python
    cmd = BuildTest(
        configuration=configuration,
        executors=["generic.local.csh", "generic.local.python"],
        buildtest_system=system,
    )
    cmd.build()


@pytest.mark.cli
def test_run_only():

    system = BuildTestSystem()
    system.check()

    # Testing run_only fields by running:  buildtest build -b tutorials/root_user.yml -b tutorials/run_only_distro.yml -b tutorials/run_only_platform.yml
    cmd = BuildTest(
        buildspecs=[
            os.path.join(BUILDTEST_ROOT, "tutorials", "root_user.yml"),
            os.path.join(BUILDTEST_ROOT, "tutorials", "run_only_distro.yml"),
            os.path.join(BUILDTEST_ROOT, "tutorials", "run_only_platform.yml"),
        ],
        configuration=configuration,
        buildtest_system=system,
    )
    cmd.build()


@pytest.mark.cli
def test_skip_field():

    system = BuildTestSystem()
    system.check()

    # Testing run_only fields by running:  buildtest build -b tutorials/skip.yml
    cmd = BuildTest(
        buildspecs=[os.path.join(BUILDTEST_ROOT, "tutorials", "skip_tests.yml")],
        configuration=configuration,
        buildtest_system=system,
    )
    cmd.build()


@pytest.mark.cli
def test_build_by_stages():

    system = BuildTestSystem()
    system.check()

    # testing buildtest build --tags python --stage=parse
    cmd = BuildTest(
        configuration=configuration,
        tags=["python"],
        stage="parse",
        buildtest_system=system,
    )
    cmd.build()

    # testing buildtest build --tags tutorials --stage=build
    cmd = BuildTest(
        configuration=configuration,
        tags=["python"],
        stage="build",
        buildtest_system=system,
    )
    cmd.build()


@pytest.mark.cli
def test_build_rebuild():

    system = BuildTestSystem()
    system.check()

    buildspec_file = os.path.join(BUILDTEST_ROOT, "tutorials", "python-shell.yml")

    # rebuild 5 times (buildtest build -b tutorials/python-shell.yml --rebuild=5
    cmd = BuildTest(
        configuration=configuration,
        buildspecs=[buildspec_file],
        rebuild=5,
        buildtest_system=system,
    )
    cmd.build()


@pytest.mark.cli
def test_invalid_buildspes():

    system = BuildTestSystem()
    system.check()

    buildspec_file = [
        os.path.join(BUILDTEST_ROOT, "tutorials", "invalid_tags.yml"),
        os.path.join(BUILDTEST_ROOT, "tutorials", "invalid_executor.yml"),
    ]

    # rebuild 5 times (buildtest build -b tutorials/python-shell.yml --rebuild=5
    cmd = BuildTest(
        configuration=configuration,
        buildspecs=buildspec_file,
        rebuild=5,
        buildtest_system=system,
    )
    cmd.build()


@pytest.mark.cli
def test_build_with_without_color():

    system = BuildTestSystem()
    system.check()

    buildspec_file = [os.path.join(BUILDTEST_ROOT, "tutorials", "python-shell.yml")]
    os.environ["BUILDTEST_COLOR"] = "False"

    # BUILDTEST_COLOR=False buildtest build -b tutorials/python-shell.yml
    cmd = BuildTest(
        configuration=configuration,
        buildspecs=buildspec_file,
        buildtest_system=system,
    )
    cmd.build()

    os.environ["BUILDTEST_COLOR"] = "True"

    # BUILDTEST_COLOR=True buildtest build -b tutorials/python-shell.yml
    cmd = BuildTest(
        configuration=configuration,
        buildspecs=buildspec_file,
        buildtest_system=system,
    )
    cmd.build()


@pytest.mark.cli
def test_keep_stage():

    system = BuildTestSystem()
    system.check()
    buildspec_file = [os.path.join(BUILDTEST_ROOT, "tutorials", "python-shell.yml")]
    cmd = BuildTest(
        configuration=configuration,
        buildspecs=buildspec_file,
        buildtest_system=system,
        keep_stage_dir=True,
    )
    cmd.build()


def test_discover():

    system = BuildTestSystem()
    system.check()

    # test single buildspec file
    buildspec = [os.path.join(valid_buildspecs, "environment.yml")]

    detected_buildspecs = discover_buildspecs(buildspecs=buildspec)

    assert buildspec == detected_buildspecs["detected"]

    detected_buildspecs = discover_buildspecs(buildspecs=[valid_buildspecs])
    assert detected_buildspecs["detected"]

    buildspec = [os.path.join(root, "README.rst")]
    # testing invalid extension this will raise an error

    with pytest.raises(SystemExit):
        discover_buildspecs(buildspecs=buildspec)

    tempdir = tempfile.TemporaryDirectory()
    # passing an empty directory will raise an error because no .yml extensions found
    with pytest.raises(SystemExit):
        discover_buildspecs(buildspecs=[tempdir.name])

    buildspec = []
    # passing no buildspecs will result in error
    with pytest.raises(SystemExit):
        discover_buildspecs(buildspecs=[])


def test_BuildTest_type():

    # buildspec must be a list not a string
    buildspec = os.path.join(valid_buildspecs, "environment.yml")
    with pytest.raises(BuildTestError):
        BuildTest(configuration=configuration, buildspecs=buildspec)

    # invalid value for exclude buildspecs must be a list
    with pytest.raises(BuildTestError):
        BuildTest(
            configuration=configuration,
            buildspecs=[buildspec],
            exclude_buildspecs=buildspec,
        )

    # tags must be a list not a string
    with pytest.raises(BuildTestError):
        BuildTest(configuration=configuration, tags="pass")

    # tags must be a list not a string
    with pytest.raises(BuildTestError):
        BuildTest(configuration=configuration, executors="generic.local.bash")

    # filter_tags must be a list not a string
    with pytest.raises(BuildTestError):
        BuildTest(configuration=configuration, tags=["pass"], filter_tags="pass")

    # invalid type for stage argument, must be a string not list
    with pytest.raises(BuildTestError):
        BuildTest(configuration=configuration, tags=["pass"], stage=["parse"])

    # invalid value for testdir argument, must be a str
    with pytest.raises(BuildTestError):
        BuildTest(
            configuration=configuration,
            tags=["pass"],
            testdir=list(BUILDTEST_ROOT),
        )

    # invalid type for rebuild argument, must be an int not string
    with pytest.raises(BuildTestError):
        BuildTest(configuration=configuration, tags=["pass"], rebuild="1")
