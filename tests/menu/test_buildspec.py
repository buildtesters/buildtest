from buildtest.menu.buildspec import func_buildspec_find, func_buildspec_view
from buildtest.defaults import BUILDSPEC_CACHE_FILE


def test_func_buildspec_find():

    # testing buildtest buildspec find --clear
    class args:
        find = True
        clear = True

    func_buildspec_find(args)

    # rerunning buildtest buildspec find without --clear option this will read from cache file
    class args:
        find = True
        clear = False

    func_buildspec_find(args)


def test_buildspec_view():

    assert BUILDSPEC_CACHE_FILE

    test_name = "cc_example"
    print(f"Viewing buildspec test: {test_name}")

    class args:
        buildspec = test_name
        view = True
        edit = False

    func_buildspec_view(args)
