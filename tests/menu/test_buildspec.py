import os
import pytest
from buildtest.config import resolve_settings_file
from buildtest.exceptions import BuildTestError
from buildtest.menu.buildspec import BuildspecCache

settings_file = resolve_settings_file()


@pytest.mark.cli
def test_func_buildspec_find():

    # testing buildtest buildspec find --rebuild
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

    """
    cache = BuildspecCache(
        rebuild=args.rebuild,
        filterfields=args.filter,
        formatfields=args.format,
        roots=args.root,
        settings_file=settings_file,
    )
    """
    # buildtest buildspec find --rebuild
    cache = BuildspecCache(rebuild=True, settings_file=settings_file)

    cache.print_buildspecs()

    # buildtest buildspec find
    cache = BuildspecCache(settings_file=settings_file)
    cache.print_buildspecs()

    # implements buildtest buildspec find --tags
    cache.get_tags()

    # implements buildtest buildspec find --buildspec-files
    cache.get_buildspecfiles()

    # implements buildtest buildspec find --paths
    cache.print_paths()

    # implements buildtest buildspec find --executors
    cache.get_executors()

    # implements buildtest buildspec find --group-by-executors
    cache.print_by_executors()

    # implements buildtest buildspec find --group-by-tags
    cache.print_by_tags()

    # implements buildtest buildspec find --maintainers
    cache.print_maintainer()

    # implements buildtest buildspec find --maintainers-by-buildspecs
    cache.print_maintainers_by_buildspecs()

    # implements buildtest buildspec find --helpfilter
    cache.print_filter_fields()

    # implements buildtest buildspec find --helpformat
    cache.print_format_fields()


@pytest.mark.cli
def test_buildspec_find_filter():
    class args:
        find = True
        rebuild = False
        root = None
        buildspec_files = False
        executors = False
        tags = False
        paths = False
        group_by_tags = False
        group_by_executor = False
        maintainers = False
        maintainers_by_buildspecs = False
        filter = {"tags": "fail"}
        format = None
        helpfilter = False
        helpformat = False

    # testing buildtest buildspec find --filter tags=fail
    cache = BuildspecCache(filterfields={"tags": "fail"}, settings_file=settings_file)
    cache.print_buildspecs()

    # testing buildtest buildspec find --filter type=script,executor=generic.local.sh,tags=fail
    cache = BuildspecCache(
        filterfields={"type": "script", "executor": "generic.local.sh", "tags": "fail"},
        settings_file=settings_file,
    )
    cache.print_buildspecs()

    # testing buildtest buildspec find --filter key1=val1,key2=val2
    with pytest.raises(BuildTestError):
        cache = BuildspecCache(
            filterfields={"key1": "val1", "key2": "val2"}, settings_file=settings_file
        )
        cache.print_buildspecs()


@pytest.mark.cli
def test_buildspec_find_format():
    class args:
        find = True
        rebuild = False
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
        format = "name,type,executor,description,file"
        helpfilter = False
        helpformat = False

    # testing buildtest buildspec find --filter type=script,executor=generic.local.sh,tags=fail
    cache = BuildspecCache(
        formatfields="name,type,executor,description,file", settings_file=settings_file
    )
    cache.print_buildspecs()

    # testing buildtest buildspec find --format field1 should raise error. Any
    # invalid format fields will raise an exception of type BuildTestError
    with pytest.raises(BuildTestError):

        # testing buildtest buildspec find --filter type=script,executor=generic.local.sh,tags=fail
        cache = BuildspecCache(formatfields="field1", settings_file=settings_file)
        cache.print_buildspecs()


@pytest.mark.cli
def test_buildspec_find_roots():

    repo_root = os.path.dirname(os.path.dirname(__file__))
    root_buildspecs = [
        os.path.join(repo_root, "tests", "buildsystem"),
        os.path.join(repo_root, "tutorials"),
    ]

    BuildspecCache(roots=root_buildspecs, settings_file=settings_file)

    # running buildtest buildspec find --root /path/to/buildtest/README.rst --root /path/to/buildtest/tutorials/environment.yml
    BuildspecCache(
        roots=[
            os.path.join(repo_root, "README.rst"),
            os.path.join(repo_root, "tutorials", "environment.yml"),
        ],
        settings_file=settings_file,
    )
