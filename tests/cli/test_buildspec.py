import os

import pytest
from buildtest.cli.buildspec import BuildspecCache, buildspec_validate
from buildtest.config import SiteConfiguration
from buildtest.defaults import BUILDTEST_ROOT
from buildtest.exceptions import BuildTestError

configuration = SiteConfiguration()
configuration.detect_system()
configuration.validate()


@pytest.mark.cli
def test_buildspec_validate():

    buildspecs = [
        os.path.join(BUILDTEST_ROOT, "tutorials", "vars.yml"),
        os.path.join(BUILDTEST_ROOT, "tutorials", "compilers"),
    ]
    exclude_buildspecs = [
        os.path.join(BUILDTEST_ROOT, "tutorials", "compilers", "gnu_hello_c.yml")
    ]
    tags = ["pass", "python"]
    executors = ["generic.local.sh"]

    buildspec_validate(
        buildspecs=buildspecs,
        excluded_buildspecs=exclude_buildspecs,
        tags=tags,
        executors=executors,
        configuration=configuration,
    )

    buildspec = [os.path.join(BUILDTEST_ROOT, "tutorials", "invalid_executor.yml")]

    buildspec_validate(buildspecs=buildspec, configuration=configuration)


@pytest.mark.cli
def test_func_buildspec_find():

    # buildtest buildspec find --rebuild
    cache = BuildspecCache(rebuild=True, configuration=configuration)

    cache.print_buildspecs()

    # buildtest buildspec find
    cache = BuildspecCache(configuration=configuration)
    cache.print_buildspecs()

    # buildtest buildspec find --tags
    cache.get_tags()

    #  buildtest buildspec find --tags --terse
    cache.get_tags(terse=True)

    # buildtest buildspec find --buildspec
    cache.get_buildspecfiles()

    #  buildtest buildspec find --buildspec
    cache.get_buildspecfiles(terse=True)

    # buildtest buildspec find --paths
    cache.print_paths()

    # buildtest buildspec find --executors
    cache.get_executors()

    # buildtest buildspec find --executors --terse
    cache.get_executors(terse=True)

    # buildtest buildspec find --group-by-executors
    cache.print_by_executors()

    # buildtest buildspec find --group-by-tags
    cache.print_by_tags()

    # buildtest buildspec find --maintainers
    cache.print_maintainer()

    # buildtest buildspec find --maintainers --terse
    cache.print_maintainer(terse=True)

    # implements buildtest buildspec find --maintainers-by-buildspecs
    cache.print_maintainers_by_buildspecs()

    # implements buildtest buildspec find --helpfilter
    cache.print_filter_fields()

    # implements buildtest buildspec find --helpformat
    cache.print_format_fields()


@pytest.mark.cli
def test_buildspec_find_filter():

    # testing buildtest buildspec find --filter tags=fail
    cache = BuildspecCache(filterfields={"tags": "fail"}, configuration=configuration)
    cache.print_buildspecs()

    # testing buildtest buildspec find --filter type=script,executor=generic.local.sh,tags=fail
    cache = BuildspecCache(
        filterfields={"type": "script", "executor": "generic.local.sh", "tags": "fail"},
        configuration=configuration,
    )
    cache.print_buildspecs()

    # testing buildtest buildspec find --filter key1=val1,key2=val2
    with pytest.raises(BuildTestError):
        cache = BuildspecCache(
            filterfields={"key1": "val1", "key2": "val2"}, configuration=configuration
        )
        cache.print_buildspecs()


@pytest.mark.cli
def test_buildspec_find_format():

    # testing buildtest buildspec find --format name,type,executor,description,file
    cache = BuildspecCache(
        formatfields="name,type,executor,description,file", configuration=configuration
    )
    cache.print_buildspecs()

    # Any invalid format fields will raise an exception of type BuildTestError
    with pytest.raises(BuildTestError):

        # testing buildtest buildspec find --format field1
        cache = BuildspecCache(formatfields="field1", configuration=configuration)
        cache.print_buildspecs()


@pytest.mark.cli
def test_buildspec_find_roots():

    root_buildspecs = [
        os.path.join(BUILDTEST_ROOT, "tests", "buildsystem"),
        os.path.join(BUILDTEST_ROOT, "tutorials"),
    ]
    # testing buildtest buildspec find --root $BUILDTEST_ROOT/tests/buildsystem --root $BUILDTEST_ROOT/tutorials
    BuildspecCache(roots=root_buildspecs, configuration=configuration)

    # running buildtest buildspec find --root $BUILDTEST_ROOT/README.rst --root $BUILDTEST_ROOT/environment.yml
    BuildspecCache(
        roots=[
            os.path.join(BUILDTEST_ROOT, "README.rst"),
            os.path.join(BUILDTEST_ROOT, "tutorials", "environment.yml"),
        ],
        configuration=configuration,
    )
