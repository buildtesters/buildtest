import os
import shutil
import tempfile

import pytest
from buildtest.cli.build import BuildTest, discover_buildspecs
from buildtest.cli.buildspec import BuildspecCache
from buildtest.cli.clean import clean
from buildtest.config import SiteConfiguration
from buildtest.defaults import BUILDTEST_RERUN_FILE, BUILDTEST_ROOT
from buildtest.exceptions import BuildTestError
from buildtest.system import BuildTestSystem
from buildtest.utils.file import walk_tree

test_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root = os.path.dirname(test_root)
valid_buildspecs = os.path.join(test_root, "buildsystem", "valid_buildspecs")

configuration = SiteConfiguration()
configuration.detect_system()
configuration.validate()


@pytest.mark.cli
def test_clean():
    """This test will check ``buildtest clean`` command."""
    clean(configuration, yes=True)


@pytest.mark.cli
def test_build_by_tags():

    system = BuildTestSystem()

    # ensure we rebuild cache file before running any buildspecs commands
    BuildspecCache(rebuild=True, configuration=configuration)

    #  testing buildtest build --tags pass
    cmd = BuildTest(configuration=configuration, tags=["pass"], buildtest_system=system)
    cmd.build()

    #  testing multiple tags:  buildtest build --tags fail --tags python
    cmd = BuildTest(
        configuration=configuration,
        tags=["fail", "python"],
        buildtest_system=system,
    )
    cmd.build()


@pytest.mark.cli
def test_build_rerun():

    system = BuildTestSystem()

    #  testing buildtest build --rerun
    cmd = BuildTest(configuration=configuration, rerun=True, buildtest_system=system)
    cmd.build()

    os.remove(BUILDTEST_RERUN_FILE)
    with pytest.raises(BuildTestError):
        BuildTest(configuration=configuration, rerun=True, buildtest_system=system)


@pytest.mark.cli
def test_build_executor_type():

    system = BuildTestSystem()
    #  testing buildtest build --tags python --executor-type local
    cmd = BuildTest(
        configuration=configuration,
        tags=["python"],
        executor_type="local",
        buildtest_system=system,
    )
    cmd.build()

    #  testing buildtest build --tags python --executor-type batch
    cmd = BuildTest(
        configuration=configuration,
        tags=["python"],
        executor_type="batch",
        buildtest_system=system,
    )
    with pytest.raises(SystemExit):
        cmd.build()


@pytest.mark.cli
def test_build_filter_check():

    system = BuildTestSystem()

    #  testing buildtest build --tags pass --filter tags=pass
    cmd = BuildTest(
        configuration=configuration,
        tags=["pass"],
        filter_buildspecs={"tags": "pass"},
        buildtest_system=system,
    )
    cmd.build()

    #  testing buildtest build --tags tutorials --filter maintainers=@shahzebsiddiqui
    cmd = BuildTest(
        configuration=configuration,
        buildspecs=[os.path.join(BUILDTEST_ROOT, "tutorials")],
        filter_buildspecs={"maintainers": "@shahzebsiddiqui"},
        buildtest_system=system,
    )
    cmd.build()

    #  testing buildtest build -b tutorials/shell_examples.yml --filter type=script
    cmd = BuildTest(
        configuration=configuration,
        buildspecs=[os.path.join(BUILDTEST_ROOT, "tutorials", "shell_examples.yml")],
        filter_buildspecs={"type": "script"},
        buildtest_system=system,
    )
    cmd.build()

    with pytest.raises(SystemExit):
        #  testing buildtest build -b tutorials/shell_examples.yml --filter type=spack this will raise an error because there would be no tests using 'type: spack'
        cmd = BuildTest(
            configuration=configuration,
            buildspecs=[
                os.path.join(BUILDTEST_ROOT, "tutorials", "shell_examples.yml")
            ],
            filter_buildspecs={"type": "spack"},
            buildtest_system=system,
        )
        cmd.build()

    # invalid filter field 'FOO' running 'buildtest build -t pass --filter FOO=BAR
    with pytest.raises(BuildTestError):
        BuildTest(
            configuration=configuration, tags=["pass"], filter_buildspecs={"FOO": "BAR"}
        )

    # invalid value for filter type running 'buildtest build -t pass --filter type=FOO
    with pytest.raises(BuildTestError):
        BuildTest(
            configuration=configuration,
            tags=["pass"],
            filter_buildspecs={"type": "FOO"},
        )

    BuildTest(configuration=configuration, helpfilter=True)


@pytest.mark.cli
def test_build_buildspecs():

    system = BuildTestSystem()

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

    # testing buildtest build --tags fail --executor generic.local.csh
    cmd = BuildTest(
        configuration=configuration,
        tags=["fail"],
        executors=["generic.local.csh"],
        buildtest_system=system,
    )
    cmd.build()


@pytest.mark.cli
def test_build_csh_executor():

    if not shutil.which("csh"):
        pytest.skip("Unable to run this test since it requires 'csh'")

    system = BuildTestSystem()

    # testing buildtest build --executor generic.local.csh
    cmd = BuildTest(
        configuration=configuration,
        executors=["generic.local.csh"],
        buildtest_system=system,
    )
    cmd.build()


@pytest.mark.cli
def test_skip_field():

    system = BuildTestSystem()

    cmd = BuildTest(
        buildspecs=[os.path.join(BUILDTEST_ROOT, "tutorials", "skip_tests.yml")],
        configuration=configuration,
        buildtest_system=system,
    )
    cmd.build()

    cmd = BuildTest(
        buildspecs=[os.path.join(BUILDTEST_ROOT, "tutorials", "skip_buildspec.yml")],
        configuration=configuration,
        buildtest_system=system,
    )
    with pytest.raises(SystemExit):
        cmd.build()


@pytest.mark.cli
def test_build_by_stages():

    system = BuildTestSystem()

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
def test_build_limit():

    system = BuildTestSystem()

    # rebuild 5 times (buildtest build -t python --rebuild=5 --limit=2
    cmd = BuildTest(
        configuration=configuration,
        tags=["python"],
        rebuild=5,
        buildtest_system=system,
        limit=2,
    )
    cmd.build()

    # should raise error when --limit=0 testing special case
    with pytest.raises(BuildTestError):
        BuildTest(
            configuration=configuration,
            tags=["python"],
            rebuild=5,
            buildtest_system=system,
            limit=0,
        )

    # should raise error when --limit is a negative number
    with pytest.raises(BuildTestError):
        BuildTest(
            configuration=configuration,
            tags=["python"],
            rebuild=5,
            buildtest_system=system,
            limit=-99,
        )

    # should raise error when --limit is not an int
    with pytest.raises(BuildTestError):
        BuildTest(
            configuration=configuration,
            tags=["python"],
            rebuild=5,
            buildtest_system=system,
            limit=1.5,
        )


@pytest.mark.cli
def test_invalid_buildspes():

    system = BuildTestSystem()

    buildspec_file = [
        os.path.join(BUILDTEST_ROOT, "tutorials", "invalid_tags.yml"),
        os.path.join(BUILDTEST_ROOT, "tutorials", "invalid_executor.yml"),
    ]

    # buildtest build -b tutorials/invalid_tags.yml -b tutorials/invalid_executor.yml
    with pytest.raises(SystemExit):
        cmd = BuildTest(
            configuration=configuration,
            buildspecs=buildspec_file,
            buildtest_system=system,
        )
        cmd.build()


def test_jobdeps():
    system = BuildTestSystem()

    buildspecs = walk_tree(os.path.join(BUILDTEST_ROOT, "tutorials", "job_dependency"))

    cmd = BuildTest(
        configuration=configuration,
        buildspecs=buildspecs,
        buildtest_system=system,
    )
    cmd.build()


@pytest.mark.cli
def test_timeout():

    system = BuildTestSystem()

    buildspecs = [os.path.join(BUILDTEST_ROOT, "tutorials", "sleep.yml")]
    cmd = BuildTest(
        configuration=configuration,
        buildspecs=buildspecs,
        buildtest_system=system,
        timeout=1,
    )
    cmd.build()

    # running same test with timeout=10 which should pass
    cmd = BuildTest(
        configuration=configuration,
        buildspecs=buildspecs,
        buildtest_system=system,
        timeout=10,
    )
    cmd.build()


@pytest.mark.cli
def test_remove_stagedir():

    system = BuildTestSystem()

    buildspec_file = [os.path.join(BUILDTEST_ROOT, "tutorials", "python-shell.yml")]
    cmd = BuildTest(
        configuration=configuration,
        buildspecs=buildspec_file,
        buildtest_system=system,
        remove_stagedir=True,
    )
    cmd.build()


def test_discover():

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

    # timeout must be an integer
    with pytest.raises(BuildTestError):
        BuildTest(configuration=configuration, tags=["pass"], timeout=1.5)

    # timeout must be a positive integer
    with pytest.raises(BuildTestError):
        BuildTest(configuration=configuration, tags=["pass"], timeout=-1)
