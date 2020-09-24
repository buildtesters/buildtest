import pytest
from buildtest.menu.buildspec import func_buildspec_find, func_buildspec_view
from buildtest.defaults import BUILDSPEC_CACHE_FILE


@pytest.mark.cli
def test_func_buildspec_find():

    # testing buildtest buildspec find --clear
    class args:
        find = True
        clear = True
        buildspec_files = False
        list_executors = False
        tags = False
        filter = None
        helpfilter = False

    func_buildspec_find(args)

    # rerunning buildtest buildspec find without --clear option this will read from cache file
    class args:
        find = True
        clear = False
        buildspec_files = False
        list_executors = False
        tags = False
        filter = None
        helpfilter = False

    func_buildspec_find(args)


@pytest.mark.cli
def test_buildspec_view():

    assert BUILDSPEC_CACHE_FILE

    test_name = "cc_example"
    print(f"Viewing buildspec test: {test_name}")

    class args:
        buildspec = test_name
        view = True
        edit = False

    func_buildspec_view(args)


@pytest.mark.cli
def test_buildspec_tags():
    class args:
        find = True
        tags = True
        clear = False
        buildspec_files = False
        list_executors = False
        filter = None
        helpfilter = False

    # testing buildtest buildspec find --tags
    func_buildspec_find(args)


@pytest.mark.cli
def test_buildspec_files():
    class args:
        find = True
        buildspec_files = True
        clear = False
        list_executors = False
        tags = False
        filter = None
        helpfilter = False

    # testing buildtest buildspec find --buildspec-files
    func_buildspec_find(args)


@pytest.mark.cli
def test_buildspec_executors():
    class args:
        find = True
        list_executors = True
        clear = False
        tags = False
        buildspec_files = False
        filter = None
        helpfilter = False

    # testing buildtest buildspec find --list-executors
    func_buildspec_find(args)


@pytest.mark.cli
def test_buildspec_find_filter():
    class args:
        find = True
        helpfilter = True
        list_executors = False
        clear = False
        tags = False
        buildspec_files = False
        filter = None

    # testing buildtest buildspec find --helpfilter
    func_buildspec_find(args)

    class args:
        find = True
        filter = {"tags": "fail"}
        helpfilter = False
        list_executors = False
        clear = False
        tags = False
        buildspec_files = False

    # testing buildtest buildspec find --filter tags=fail
    func_buildspec_find(args)

    class args:
        find = True
        filter = {"type": "script", "executor": "local.sh", "tags": "tutorials"}
        helpfilter = False
        list_executors = False
        clear = False
        tags = False
        buildspec_files = False

    # testing buildtest buildspec find --filter type=script,executor=local.sh,tags=fail
    func_buildspec_find(args)
