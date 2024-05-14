import os
import shutil
import tempfile

import pytest
from rich.pretty import pprint

from buildtest.cli.build import BuildTest, discover_buildspecs
from buildtest.cli.buildspec import BuildspecCache
from buildtest.cli.clean import clean
from buildtest.cli.config import list_profiles
from buildtest.config import SiteConfiguration
from buildtest.defaults import BUILDTEST_RERUN_FILE, BUILDTEST_ROOT
from buildtest.exceptions import BuildTestError
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


class TestBuildTest:

    @pytest.mark.cli
    def test_build_by_tags(self):
        # ensure we rebuild cache file before running any buildspecs commands
        BuildspecCache(rebuild=True, configuration=configuration)

        #  buildtest build --tags pass
        cmd = BuildTest(configuration=configuration, tags=["pass"])
        cmd.build()

        #  buildtest build --tags fail --tags python
        cmd = BuildTest(configuration=configuration, tags=["fail", "python"])
        cmd.build()

        #   testing multiple tags as comma separated list:
        #  buildtest build --tags fail,python --tags network
        cmd = BuildTest(configuration=configuration, tags=["fail,python", "network"])
        cmd.build()

        # testing no tag names
        # buildtest build --tags ,,
        cmd = BuildTest(configuration=configuration, tags=[",,"])
        with pytest.raises(SystemExit):
            cmd.build()
        # testing with spaces between tags
        cmd = BuildTest(configuration=configuration, tags=["  ,python,  fail,   ,,"])
        cmd.build()

    @pytest.mark.cli
    def test_build_rerun(self):
        #  testing buildtest build --rerun
        cmd = BuildTest(configuration=configuration, rerun=True, dry_run=True)
        cmd.build()

        os.remove(BUILDTEST_RERUN_FILE)
        with pytest.raises(BuildTestError):
            BuildTest(configuration=configuration, rerun=True, dry_run=True)

    @pytest.mark.cli
    def test_build_executor_type(self):

        # buildtest build --tags python --executor-type local
        cmd = BuildTest(
            configuration=configuration, tags=["python"], executor_type="local"
        )
        cmd.build()

        # buildtest build --tags python --executor-type batch
        cmd = BuildTest(
            configuration=configuration, tags=["python"], executor_type="batch"
        )
        with pytest.raises(SystemExit):
            cmd.build()

    @pytest.mark.cli
    def test_build_filter_check(self):
        #  testing buildtest build --tags pass --filter tags=pass
        cmd = BuildTest(
            configuration=configuration,
            tags=["pass"],
            filter_buildspecs={"tags": ["pass"]},
        )
        cmd.build()

        #  testing buildtest build --tags tutorials --filter maintainers=@shahzebsiddiqui
        cmd = BuildTest(
            configuration=configuration,
            buildspecs=[os.path.join(BUILDTEST_ROOT, "tutorials")],
            filter_buildspecs={"maintainers": ["@shahzebsiddiqui"]},
        )
        cmd.build()

        #  testing buildtest build -b tutorials/shell_examples.yml --filter type=script
        cmd = BuildTest(
            configuration=configuration,
            buildspecs=[
                os.path.join(BUILDTEST_ROOT, "tutorials", "shell_examples.yml")
            ],
            filter_buildspecs={"type": ["script"]},
        )
        cmd.build()

    def test_invalid_build_filters(self):
        with pytest.raises(SystemExit):
            #  testing buildtest build -b tutorials/shell_examples.yml --filter type=spack this will raise an error because there would be no tests using 'type: spack'
            cmd = BuildTest(
                configuration=configuration,
                buildspecs=[
                    os.path.join(BUILDTEST_ROOT, "tutorials", "shell_examples.yml")
                ],
                filter_buildspecs={"type": ["spack"]},
            )
            cmd.build()

        # invalid filter field 'FOO' running 'buildtest build -t pass --filter FOO=BAR
        with pytest.raises(BuildTestError):
            BuildTest(
                configuration=configuration,
                tags=["pass"],
                filter_buildspecs={"FOO": "BAR"},
            )

        # invalid value for filter type running 'buildtest build -t pass --filter type=FOO
        with pytest.raises(BuildTestError):
            BuildTest(
                configuration=configuration,
                tags=["pass"],
                filter_buildspecs={"type": "FOO"},
            )

    @pytest.mark.cli
    def test_helpfilter(self):
        BuildTest(configuration=configuration, helpfilter=True)

    @pytest.mark.cli
    def test_build_buildspecs(self):
        buildspec_paths = os.path.join(test_root, "buildsystem", "valid_buildspecs")

        #  testing buildtest build --buildspec tests/buildsystem/valid_buildspecs
        cmd = BuildTest(configuration=configuration, buildspecs=[buildspec_paths])
        cmd.build()

        excluded_buildspecs = walk_tree(buildspec_paths, ".yml")
        assert len(excluded_buildspecs) > 0
        #  testing buildtest build --buildspec tests/buildsystem/valid_buildspecs and exclude the first buildspec
        cmd = BuildTest(
            configuration=configuration,
            buildspecs=[buildspec_paths],
            exclude_buildspecs=[excluded_buildspecs[0]],
        )
        cmd.build()

        #  testing buildtest build --buildspec tests/examples/buildspecs --exclude tests/examples/buildspecs
        # this results in no buildspecs built
        with pytest.raises(SystemExit):
            cmd = BuildTest(
                configuration=configuration,
                buildspecs=[buildspec_paths],
                exclude_buildspecs=[buildspec_paths],
            )
            cmd.build()

    @pytest.mark.cli
    def test_buildspec_with_module_injection(self):
        """This test run a buildspec with module injection. This will load and unload modules"""

        # buildtest build --tags python --modules gcc/9.1.0 --unload-modules gcc --module-purge
        cmd = BuildTest(
            configuration=configuration,
            tags=["python"],
            modulepurge=True,
            modules="gcc/9.1.0",
            unload_modules="gcc",
        )
        cmd.build()

    def test_run_metrics(self):
        cmd = BuildTest(
            configuration=configuration,
            buildspecs=[
                os.path.join(
                    BUILDTEST_ROOT, "tutorials", "metrics", "metrics_regex.yml"
                ),
                os.path.join(
                    BUILDTEST_ROOT,
                    "tutorials",
                    "metrics",
                    "metrics_file_regex_invalid_file.yml",
                ),
            ],
        )
        cmd.build()

    def test_run_all_perf_checks(self):

        buildspecs = walk_tree(
            root_dir=os.path.join(BUILDTEST_ROOT, "tutorials", "perf_checks"),
            ext=".yml",
        )

        #  buildtest build --buildspec $BUILDTEST_ROOT/tutorials/perf_checks
        cmd = BuildTest(configuration=configuration, buildspecs=buildspecs)
        cmd.build()

    @pytest.mark.cli
    def test_buildspec_tag_executor(self):
        # buildtest build --tags fail --executor generic.local.csh
        cmd = BuildTest(
            configuration=configuration, tags=["fail"], executors=["generic.local.csh"]
        )
        cmd.build()

    @pytest.mark.cli
    def test_exclude_tags(self):
        # testing buildtest build --tags fail --exclude-tags fail
        cmd = BuildTest(
            configuration=configuration, tags=["fail"], exclude_tags=["fail"]
        )
        cmd.build()

        # testing buildtest build --buildspec $BUILDTEST_ROOT/tutorials/python-hello.yml --exclude-tags python
        cmd = BuildTest(
            configuration=configuration,
            buildspecs=[os.path.join(BUILDTEST_ROOT, "tutorials", "python-hello.yml")],
            exclude_tags=["python"],
        )
        # no test will be run
        with pytest.raises(SystemExit):
            cmd.build()

    @pytest.mark.cli
    def test_buildspecs_by_name(self):
        # testing buildtest build --name
        cmd = BuildTest(
            configuration=configuration, name=["hello_world", "add_numbers"]
        )
        cmd.build()

        # should raise exception if `name` is not a list
        with pytest.raises(BuildTestError):
            BuildTest(configuration=configuration, name="pass_test")

    def test_build_csh_executor(self):
        if not shutil.which("csh"):
            pytest.skip("Unable to run this test since it requires 'csh'")

        # testing buildtest build --executor generic.local.csh
        cmd = BuildTest(configuration=configuration, executors=["generic.local.csh"])
        cmd.build()

    def test_skip_field(self):
        cmd = BuildTest(
            buildspecs=[os.path.join(BUILDTEST_ROOT, "tutorials", "skip_tests.yml")],
            configuration=configuration,
        )
        cmd.build()

        cmd = BuildTest(
            buildspecs=[
                os.path.join(BUILDTEST_ROOT, "tutorials", "skip_buildspec.yml")
            ],
            configuration=configuration,
        )
        with pytest.raises(SystemExit):
            cmd.build()

    @pytest.mark.cli
    def test_build_validate(self):
        # testing buildtest build --tags python --validate
        cmd = BuildTest(configuration=configuration, tags=["python"], validate=True)
        cmd.build()

    @pytest.mark.cli
    def test_build_dryrun(self):
        # testing buildtest build --tags python --dry-run
        cmd = BuildTest(configuration=configuration, tags=["python"], dry_run=True)
        cmd.build()

    @pytest.mark.cli
    def test_build_rebuild(self):
        buildspec_file = os.path.join(BUILDTEST_ROOT, "tutorials", "python-shell.yml")

        # rebuild 5 times (buildtest build -b tutorials/python-shell.yml --rebuild=5
        cmd = BuildTest(
            configuration=configuration, buildspecs=[buildspec_file], rebuild=5
        )
        cmd.build()

    @pytest.mark.cli
    def test_build_limit(self):
        # rebuild 5 times (buildtest build -t python --rebuild=5 --limit=2
        cmd = BuildTest(
            configuration=configuration, tags=["python"], rebuild=5, limit=2
        )
        cmd.build()

        # should raise error when --limit=0 testing special case
        with pytest.raises(BuildTestError):
            BuildTest(configuration=configuration, tags=["python"], rebuild=5, limit=0)

        # should raise error when --limit is a negative number
        with pytest.raises(BuildTestError):
            BuildTest(
                configuration=configuration, tags=["python"], rebuild=5, limit=-99
            )

        # should raise error when --limit is not an int
        with pytest.raises(BuildTestError):
            BuildTest(
                configuration=configuration, tags=["python"], rebuild=5, limit=1.5
            )

    def test_max_jobs(self):
        # testing buildtest build -b tutorials/hello_world.yml --max-jobs=2 --rebuild=4
        cmd = BuildTest(
            configuration=configuration,
            buildspecs=[os.path.join(BUILDTEST_ROOT, "tutorials", "hello_world.yml")],
            rebuild=4,
            max_jobs=2,
        )
        cmd.build()

    def test_verbose_mode(self):
        # buildtest --verbose build -b tutorials/perf_checks -n hello_world -t pass -e generic.local.csh -x tutorials/perf_checks/assert_ge.yml --limit=10
        cmd = BuildTest(
            configuration=configuration,
            buildspecs=[os.path.join(BUILDTEST_ROOT, "tutorials", "perf_checks")],
            exclude_buildspecs=[
                os.path.join(
                    BUILDTEST_ROOT, "tutorials", "perf_checks", "assert_ge.yml"
                )
            ],
            name=["hello_world"],
            tags=["pass"],
            executors=["generic.local.csh"],
            limit=10,
            verbose=True,
        )
        cmd.build()

    def test_invalid_buildspes(self):
        buildspec_file = [
            os.path.join(BUILDTEST_ROOT, "tutorials", "invalid_tags.yml"),
            os.path.join(BUILDTEST_ROOT, "tutorials", "invalid_executor.yml"),
        ]

        # buildtest build -b tutorials/invalid_tags.yml -b tutorials/invalid_executor.yml
        with pytest.raises(SystemExit):
            cmd = BuildTest(configuration=configuration, buildspecs=buildspec_file)
            cmd.build()

    def test_jobdeps(self):
        buildspecs = walk_tree(
            os.path.join(BUILDTEST_ROOT, "tutorials", "job_dependency")
        )

        cmd = BuildTest(configuration=configuration, buildspecs=buildspecs)
        cmd.build()

    @pytest.mark.cli
    def test_timeout(self):
        buildspecs = [os.path.join(BUILDTEST_ROOT, "tutorials", "sleep.yml")]
        cmd = BuildTest(configuration=configuration, buildspecs=buildspecs, timeout=1)
        cmd.build()

        # running same test with timeout=10 which should pass
        cmd = BuildTest(configuration=configuration, buildspecs=buildspecs, timeout=10)
        cmd.build()

    @pytest.mark.cli
    def test_remove_stagedir(self):
        buildspec_file = [os.path.join(BUILDTEST_ROOT, "tutorials", "python-shell.yml")]
        cmd = BuildTest(
            configuration=configuration, buildspecs=buildspec_file, remove_stagedir=True
        )
        cmd.build()

    @pytest.mark.cli
    def test_with_strict_mode(self):
        buildspecs = [os.path.join(BUILDTEST_ROOT, "tutorials", "strict_example.yml")]

        cmd = BuildTest(configuration=configuration, buildspecs=buildspecs, strict=True)
        cmd.build()

    @pytest.mark.cli
    def test_save_profile(self):
        tf = tempfile.NamedTemporaryFile(suffix=".yml")
        print(configuration.file)
        print(tf.name)
        shutil.copy2(configuration.file, tf.name)

        buildtest_configuration = SiteConfiguration(settings_file=tf.name)
        buildtest_configuration.detect_system()
        buildtest_configuration.validate()

        # this should raise exception when there is no profile created in configuration file
        with pytest.raises(BuildTestError):
            buildtest_configuration.get_profile(profile_name="invalid_profile")

        buildspecs = walk_tree(
            os.path.join(BUILDTEST_ROOT, "tutorials", "job_dependency")
        )

        BuildTest(
            configuration=buildtest_configuration,
            buildspecs=buildspecs,
            exclude_buildspecs=buildspecs,
            tags=["python"],
            executors=["generic.local.csh"],
            exclude_tags=["python"],
            numnodes=[1],
            numprocs=[2],
            account="dev",
            modules="gcc/9.1.0",
            unload_modules="gcc",
            modulepurge=True,
            validate=False,
            dry_run=True,
            limit=10,
            rebuild=2,
            timeout=60,
            executor_type="local",
            remove_stagedir=True,
            max_jobs=2,
            save_profile="demo",
            verbose=True,
            strict=True,
        )
        profile_configuration = buildtest_configuration.get_profile(profile_name="demo")
        pprint(profile_configuration)

        # When --module-purge is not specified (i.e False) then this key should not be in profile configuration and set to None
        BuildTest(
            buildspecs=buildspecs,
            configuration=buildtest_configuration,
            modulepurge=False,
            save_profile="module_purge_profile",
        )
        assert "module-purge" not in buildtest_configuration.get_profile(
            profile_name="module_purge_profile"
        )

        with pytest.raises(BuildTestError):
            buildtest_configuration.get_profile(profile_name="invalid_profile")

        cmd = BuildTest(
            profile="demo", configuration=buildtest_configuration, verbose=True
        )
        cmd.build()

    def test_save_profile_and_write_to_alternate_configuration_file(self):
        # generate a unique file name and close file handle so we can write to this file
        tf = tempfile.NamedTemporaryFile(suffix=".yml")
        tf.close()

        BuildTest(
            configuration=configuration,
            buildspecs=[os.path.join(BUILDTEST_ROOT, "tutorials", "hello_world.yml")],
            save_profile="demo",
            write_config_file=tf.name,
        )
        new_config_file = SiteConfiguration(settings_file=tf.name)
        new_config_file.detect_system()
        new_config_file.validate()
        list_profiles(configuration=new_config_file, print_yaml=True)

        # writing to same configuration file should raise an error since file must not exist when using --write-config-file
        with pytest.raises(BuildTestError):
            print(f"Writing to same configuration file: {tf.name} is not allowed")
            BuildTest(
                configuration=configuration,
                buildspecs=[
                    os.path.join(BUILDTEST_ROOT, "tutorials", "hello_world.yml")
                ],
                save_profile="demo",
                write_config_file=tf.name,
            )

        tf = tempfile.TemporaryDirectory()
        # writing to directory is not allowed
        with pytest.raises(BuildTestError):
            print(f"Writing to directory: {tf.name} is not allowed")
            BuildTest(
                configuration=configuration,
                buildspecs=[
                    os.path.join(BUILDTEST_ROOT, "tutorials", "hello_world.yml")
                ],
                save_profile="demo",
                write_config_file=tf.name,
            )

        tf = tempfile.NamedTemporaryFile(suffix=".yaml")
        tf.close()
        # writing to file with .yaml extension is not allowed
        with pytest.raises(BuildTestError):
            BuildTest(
                configuration=configuration,
                buildspecs=[
                    os.path.join(BUILDTEST_ROOT, "tutorials", "hello_world.yml")
                ],
                save_profile="demo",
                write_config_file=tf.name,
            )

    @pytest.mark.cli
    def test_retry(self):
        buildspecs = [
            os.path.join(
                BUILDTEST_ROOT, "tutorials", "test_status", "pass_returncode.yml"
            )
        ]
        cmd = BuildTest(configuration=configuration, buildspecs=buildspecs, retry=2)
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

    # create a temporary file and closing it which will essentially delete the file. We are testing an invalid file path
    tf = tempfile.NamedTemporaryFile()
    tf.close()
    with pytest.raises(SystemExit):
        discover_buildspecs(buildspecs=[tf.name])


class TestBuildTest_TypeCheck:
    def test_buildspec(self):
        # buildspec must be a list not a string
        buildspec = os.path.join(valid_buildspecs, "environment.yml")
        with pytest.raises(BuildTestError):
            BuildTest(configuration=configuration, buildspecs=buildspec)

    def test_exclude_buildspecs(self):
        # buildspec must be a list not a string
        buildspec = os.path.join(valid_buildspecs, "environment.yml")

        # invalid value for exclude buildspecs must be a list
        with pytest.raises(BuildTestError):
            BuildTest(
                configuration=configuration,
                buildspecs=[buildspec],
                exclude_buildspecs=buildspec,
            )

    def test_invalid_tag(self):
        # tags must be a list not a string
        with pytest.raises(BuildTestError):
            BuildTest(configuration=configuration, tags="pass")

    def test_invalid_executors(self):
        # executors must be a list not a string
        with pytest.raises(BuildTestError):
            BuildTest(configuration=configuration, executors="generic.local.bash")

    def test_invalid_type_for_testdir(self):
        # invalid value for testdir argument, must be a str
        with pytest.raises(BuildTestError):
            BuildTest(
                configuration=configuration, tags=["pass"], testdir=list(BUILDTEST_ROOT)
            )

    def test_invalid_type_rebuild(self):
        # invalid type for rebuild argument, must be an int not string
        with pytest.raises(BuildTestError):
            BuildTest(configuration=configuration, tags=["pass"], rebuild="1")

    def test_rebuild_limit(self):
        # test rebuild limit
        with pytest.raises(BuildTestError):
            BuildTest(configuration=configuration, tags=["pass"], rebuild=51)

    def test_invalid_timeout_type(self):
        # timeout must be an integer
        with pytest.raises(BuildTestError):
            BuildTest(configuration=configuration, tags=["pass"], timeout=1.5)

        # timeout must be a positive integer
        with pytest.raises(BuildTestError):
            BuildTest(configuration=configuration, tags=["pass"], timeout=-1)

    def test_invalid_max_jobs(self):
        with pytest.raises(BuildTestError):
            BuildTest(configuration=configuration, tags=["pass"], max_jobs=0)

        # must be an integer
        with pytest.raises(BuildTestError):
            BuildTest(configuration=configuration, tags=["pass"], max_jobs=0.1)

    def test_invalid_exclude_tags_type(self):
        # exclude_tags must be a list
        with pytest.raises(BuildTestError):
            BuildTest(configuration=configuration, tags=["pass"], exclude_tags=True)

    def test_report_value_as_directory(self):
        tempdir = tempfile.TemporaryDirectory()
        # report must be a file not a directory
        with pytest.raises(BuildTestError):
            BuildTest(
                configuration=configuration, tags=["pass"], report_file=tempdir.name
            )
