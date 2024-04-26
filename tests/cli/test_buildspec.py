import os
import random
import string
import tempfile

import pytest
from rich.color import Color

from buildtest.cli.buildspec import (
    BuildspecCache,
    buildspec_maintainers,
    buildspec_validate_command,
    edit_buildspec_file,
    edit_buildspec_test,
    show_buildspecs,
    show_failed_buildspecs,
    summarize_buildspec_cache,
)
from buildtest.cli.report import Report
from buildtest.config import SiteConfiguration
from buildtest.defaults import BUILDTEST_ROOT
from buildtest.exceptions import BuildTestError

configuration = SiteConfiguration()
configuration.detect_system()
configuration.validate()


@pytest.mark.cli
def test_buildspec_validate():
    buildspec_validate_command(
        buildspecs=[
            os.path.join(BUILDTEST_ROOT, "tutorials", "vars.yml"),
            os.path.join(BUILDTEST_ROOT, "tutorials", "test_status"),
        ],
        excluded_buildspecs=[
            os.path.join(
                BUILDTEST_ROOT, "tutorials", "test_status", "file_exists_exception.yml"
            ),
            os.path.join(
                BUILDTEST_ROOT, "tutorials", "test_status", "file_linecount_invalid.yml"
            ),
        ],
        tags=["pass", "python"],
        executors=["generic.local.sh"],
        configuration=configuration,
    )

    with pytest.raises(SystemExit):
        buildspec_validate_command(
            buildspecs=[os.path.join(BUILDTEST_ROOT, "tutorials", "invalid_tags.yml")],
            configuration=configuration,
        )


class TestBuildSpecFind:
    cache = BuildspecCache(configuration=configuration, rebuild=True)

    def test_rebuild_cache(self):
        # buildtest buildspec find --rebuild --quiet
        self.cache.print_buildspecs(quiet=True)

        # buildtest buildspec find --rebuild --terse --no-header
        self.cache = BuildspecCache(
            rebuild=True, configuration=configuration, terse=True, header=False
        )

        # buildtest buildspec find --rebuild
        self.cache = BuildspecCache(rebuild=True, configuration=configuration)

    def test_print_buildspecs(self):
        self.cache.print_buildspecs()

        # buildtest buildspec find --quiet
        self.cache.print_buildspecs(quiet=True)

        # buildtest buildspec find --row-count
        self.cache.print_buildspecs(row_count=True)

        for count in [0, 10, -1]:
            self.cache.print_buildspecs(count=count, terse=True, header=False)
            self.cache.print_buildspecs(count=count, terse=True, header=True)
            self.cache.print_buildspecs(count=count, terse=False)

    def test_print_tags(self):
        # buildtest buildspec find --tags
        self.cache.print_tags()

        # buildtest buildspec find --tags --row-count
        self.cache.print_tags(row_count=True)

        # test with --count option with different values with and without --terse and --header option
        for count in [0, 10, -1]:
            self.cache.print_tags(count=count, terse=True, header=False)
            self.cache.print_tags(count=count, terse=True, header=True)
            self.cache.print_tags(count=count, terse=False)

    def test_print_buildspecfiles(self):
        # buildtest buildspec find --buildspec
        self.cache.print_buildspecfiles()
        # buildtest buildspec find --buildspec --row-count
        self.cache.print_buildspecfiles(row_count=True)

        for count in [0, 10, -1]:
            self.cache.print_buildspecfiles(count=count, terse=True, header=False)
            self.cache.print_buildspecfiles(count=count, terse=True, header=True)
            self.cache.print_buildspecfiles(count=count, terse=False)

    def test_print_executors(self):
        # buildtest buildspec find --executors
        self.cache.print_executors()
        # buildtest buildspec find --executors --row-count
        self.cache.print_executors(row_count=True)

        for count in [0, 10, -1]:
            self.cache.print_executors(count=count, terse=True, header=False)
            self.cache.print_executors(count=count, terse=True, header=True)
            self.cache.print_executors(count=count, terse=False)

    def test_print_by_executors(self):
        # buildtest buildspec find --group-by-executors
        self.cache.print_by_executors()
        # buildtest buildspec find --group-by-executors --row-count
        self.cache.print_by_executors(row_count=True)

        for count in [0, 10, -1]:
            self.cache.print_by_executors(count=count, terse=True, header=False)
            self.cache.print_by_executors(count=count, terse=True, header=True)
            self.cache.print_by_executors(count=count, terse=False)

    def test_print_by_tags(self):
        # buildtest buildspec find --group-by-tags
        self.cache.print_by_tags()
        # buildtest buildspec find --group-by-tags --row-count
        self.cache.print_by_tags(row_count=True)

        for count in [0, 10, -1]:
            self.cache.print_by_tags(count=count, terse=True, header=False)
            self.cache.print_by_tags(count=count, terse=True, header=True)
            self.cache.print_by_tags(count=count, terse=False)

    def test_print_paths(self):
        # buildtest buildspec find --paths
        self.cache.print_paths()

    def test_print_filter_and_format_fields(self):
        # buildtest buildspec find --helpfilter
        self.cache.print_filter_fields()

        # buildtest buildspec find --helpformat
        self.cache.print_format_fields()

        # buildtest buildspec find --filterfields
        self.cache.print_raw_filter_fields()

        # buildtest buildspec find --formatfields
        self.cache.print_raw_format_fields()

    def test_pager(self):
        # buildtest buildspec find --pager
        cache = BuildspecCache(configuration=configuration, pager=True)
        cache.print_tags()
        cache.print_buildspecfiles()
        cache.print_executors()
        cache.print_by_executors()
        cache.print_by_tags()
        cache.print_maintainer()
        cache.print_maintainers_by_buildspecs()
        cache.print_buildspecs()

    def test_color(self):
        # test all commands with color 'blue'
        # buildtest --color blue buildspec find --rebuild
        cache = BuildspecCache(rebuild=True, configuration=configuration, color="blue")
        # buildtest --color blue buildspec find
        cache.print_buildspecs()
        # buildtest --color blue buildspec find -b
        cache.print_buildspecfiles()
        # buildtest --color blue buildspec find -e
        cache.print_executors()
        # buildtest --color blue buildspec find -t
        cache.print_tags()
        # buildtest --color blue buildspec find --group-by-executor
        cache.print_by_executors()
        # buildtest --color blue buildspec find --group-by-tags
        cache.print_by_tags()
        # buildtest --color blue buildspec find --helpfilter
        cache.print_filter_fields()
        # buildtest --color blue buildspec find --helpformat
        cache.print_format_fields()
        # buildtest --color blue buildspec find --filterfields
        cache.print_raw_filter_fields()
        # buildtest --color blue buildspec find --formatfields
        cache.print_raw_format_fields()

    @pytest.mark.cli
    def test_buildspec_find_filter(self):
        # buildtest buildspec find --filter tags=fail
        cache = BuildspecCache(
            filterfields={"tags": "fail"}, configuration=configuration
        )
        cache.print_buildspecs()

        # buildtest buildspec find --filter buildspec=$BUILDTEST_ROOT/tutorials/hello_world.yml
        cache = BuildspecCache(
            filterfields={
                "buildspec": os.path.join(
                    BUILDTEST_ROOT, "tutorials", "hello_world.yml"
                )
            },
            configuration=configuration,
        )
        cache.print_buildspecs()

        # buildtest buildspec find --filter type=script,executor=generic.local.sh,tags=fail
        cache = BuildspecCache(
            filterfields={
                "type": "script",
                "executor": "generic.local.bash",
                "tags": "fail",
            },
            configuration=configuration,
        )
        cache.print_buildspecs()

        with pytest.raises(BuildTestError):
            tf = tempfile.NamedTemporaryFile()
            # testing for valid filepath for buildspec file but file doesn't exist in cache
            BuildspecCache(
                filterfields={"buildspec": tf.name}, configuration=configuration
            )

        with pytest.raises(BuildTestError):
            # create temporary file and close file which will delete the file to create invalid filepath
            tf = tempfile.NamedTemporaryFile(delete=True)
            tf.close()
            # testing on invalid file path for buildspec. This should raise an exception
            BuildspecCache(
                filterfields={"buildspec": tf.name}, configuration=configuration
            )

        with pytest.raises(BuildTestError):
            tf = tempfile.TemporaryDirectory()
            # if we specify a directory path for buildspec filter this will raise an exception.
            BuildspecCache(
                filterfields={"buildspec": tf.name}, configuration=configuration
            )

        # buildtest buildspec find --filter key1=val1,key2=val2
        with pytest.raises(BuildTestError):
            cache = BuildspecCache(
                filterfields={"key1": "val1", "key2": "val2"},
                configuration=configuration,
            )
            cache.print_buildspecs()

        # testing with invalid schema type should return no entries
        cache = BuildspecCache(
            filterfields={"type": "bad_schema"}, configuration=configuration
        )
        cache.print_buildspecs()

    @pytest.mark.cli
    def test_buildspec_find_format(self):
        # buildtest buildspec find --format name,type,tags,executor,description,buildspec
        cache = BuildspecCache(
            formatfields="name,type,tags,executor,description,buildspec",
            configuration=configuration,
        )
        cache.print_buildspecs()

        # Any invalid format fields will raise an exception of type BuildTestError
        with pytest.raises(BuildTestError):
            # buildtest buildspec find --format field1
            cache = BuildspecCache(formatfields="field1", configuration=configuration)
            cache.print_buildspecs()


@pytest.mark.cli
def test_buildspec_maintainers():
    buildspec_maintainers(configuration=configuration)

    # buildtest buildspec maintainers --terse --no-header
    buildspec_maintainers(configuration=configuration, terse=True, header=True)

    # buildtest buildspec maintainers --terse
    buildspec_maintainers(configuration=configuration, terse=True, header=False)

    # buildtest buildspec maintainers --breakdown
    buildspec_maintainers(configuration=configuration, breakdown=True)

    # buildtest buildspec maintainers --terse --no-header --breakdown
    buildspec_maintainers(
        configuration=configuration, breakdown=True, terse=True, header=True
    )

    # buildtest buildspec maintainers --terse --breakdown
    buildspec_maintainers(
        configuration=configuration, breakdown=True, terse=True, header=False
    )

    # buildtest buildspec maintainers --row-count
    buildspec_maintainers(configuration=configuration, row_count=True)
    # buildtest buildspec maintainers find @shahzebsiddiqui
    buildspec_maintainers(configuration=configuration, name="@shahzebsiddiqui")


@pytest.mark.cli
def test_buildspec_find_invalid():
    cache = BuildspecCache(configuration=configuration)

    # testing buildtest buildspec find invalid. This will assert SystemExit exception raised by sys.exit
    with pytest.raises(SystemExit):
        cache.print_invalid_buildspecs(error=True)

    # print default table of invalid buildspecs
    with pytest.raises(SystemExit):
        cache.print_invalid_buildspecs()

    # show count of invalid buildspecs via --row-count
    with pytest.raises(SystemExit):
        cache.print_invalid_buildspecs(row_count=True)

    # the --error and --terse option can't be specified together since they will impact how printing is done
    with pytest.raises(SystemExit):
        cache.print_invalid_buildspecs(error=True, terse=True)

    # print in terse format
    with pytest.raises(SystemExit):
        cache.print_invalid_buildspecs(terse=True)

@pytest.mark.cli
def test_edit_test():
    edit_buildspec_test(
        test_names=["hello_world"], configuration=configuration, editor=None
    )


@pytest.mark.cli
def test_edit_file():
    edit_buildspec_file(
        buildspecs=[os.path.join(BUILDTEST_ROOT, "tutorials", "vars.yml")],
        configuration=configuration,
        editor=None,
    )


@pytest.mark.cli
def test_buildspec_find_roots():
    root_buildspecs = [
        os.path.join(BUILDTEST_ROOT, "tests", "buildsystem"),
        os.path.join(BUILDTEST_ROOT, "tutorials"),
    ]
    # buildtest buildspec find --root $BUILDTEST_ROOT/tests/buildsystem --root $BUILDTEST_ROOT/tutorials
    BuildspecCache(roots=root_buildspecs, configuration=configuration, rebuild=False)

    with pytest.raises(BuildTestError):
        # buildtest buildspec find --root $BUILDTEST_ROOT/README.rst --root $BUILDTEST_ROOT/environment.yml
        BuildspecCache(
            roots=[
                os.path.join(BUILDTEST_ROOT, "README.rst"),
                os.path.join(BUILDTEST_ROOT, "tutorials", "environment.yml"),
            ],
            configuration=configuration,
        )


@pytest.mark.cli
def test_buildspec_summary():
    # buildtest buildspec summary
    summarize_buildspec_cache(
        configuration=configuration, pager=False, color=Color.default().name
    )
    # buildtest buildspec summary --pager
    summarize_buildspec_cache(configuration=configuration, pager=True)


@pytest.mark.cli
def test_buildspec_show():
    cache = BuildspecCache(configuration=configuration)

    test_name = cache.get_random_tests(num_items=1)

    # buildtest buildspec show <test>
    show_buildspecs(test_name, configuration)

    # buildtest buildspec <test> show --theme monokai
    show_buildspecs(test_name, configuration, theme="monokai")

    # testing invalid buildspec name, it should not raise exception
    random_testname = "".join(random.choices(string.ascii_letters, k=10))
    show_buildspecs(test_names=[random_testname], configuration=configuration)


@pytest.mark.cli
def test_buildspec_show_fail():
    # Query some random test name that doesn't exist

    # show all failed buildspecs
    show_failed_buildspecs(configuration=configuration)

    random_testname = "".join(random.choices(string.ascii_letters, k=10))
    show_failed_buildspecs(configuration=configuration, test_names=[random_testname])

    # Query a test that is NOT in state=FAIL

    results = Report(configuration=configuration)
    pass_test = random.sample(results.get_test_by_state(state="PASS"), 1)
    show_failed_buildspecs(configuration=configuration, test_names=[pass_test])

    report = Report(configuration=configuration)
    # get a random failed test from report file to be used for showing content of buildspec file
    fail_tests = random.sample(report.get_test_by_state(state="FAIL"), 1)
    # buildtest buildspec show-fail <test> --theme monokai
    show_failed_buildspecs(
        configuration=configuration, test_names=fail_tests, theme="monokai"
    )
