import os
import pytest
from buildtest.exceptions import BuildTestError
from buildtest.menu.buildspec import func_buildspec_find


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
        test_by_tags = False
        test_by_executor = False
        filter = None
        format = None
        helpfilter = False
        helpformat = False

    func_buildspec_find(args)

    # rerunning buildtest buildspec find without --rebuild option this will read from cache file
    class args:
        find = True
        rebuild = False
        root = None
        buildspec_files = False
        executors = False
        tags = False
        paths = False
        test_by_tags = False
        test_by_executor = False
        filter = None
        format = None
        helpfilter = False
        helpformat = False

    func_buildspec_find(args)


@pytest.mark.cli
def test_buildspec_tags():
    class args:
        find = True
        rebuild = False
        root = None
        buildspec_files = False
        executors = False
        tags = True
        paths = False
        test_by_tags = False
        test_by_executor = False
        filter = None
        format = None
        helpfilter = False
        helpformat = False

    # testing buildtest buildspec find --tags
    func_buildspec_find(args)


@pytest.mark.cli
def test_buildspec_files():
    class args:
        find = True
        rebuild = False
        root = None
        buildspec_files = True
        executors = False
        tags = False
        paths = False
        test_by_tags = False
        test_by_executor = False
        filter = None
        format = None
        helpfilter = False
        helpformat = False

    # testing buildtest buildspec find --buildspec-files
    func_buildspec_find(args)


@pytest.mark.cli
def test_buildspec_executors():
    class args:
        find = True
        rebuild = False
        root = None
        buildspec_files = False
        executors = True
        tags = False
        paths = False
        test_by_tags = False
        test_by_executor = False
        filter = None
        format = None
        helpfilter = False
        helpformat = False

    # testing buildtest buildspec find --executors
    func_buildspec_find(args)


@pytest.mark.cli
def test_buildspec_paths():
    class args:
        find = True
        rebuild = False
        root = None
        buildspec_files = False
        executors = False
        tags = False
        paths = True
        test_by_tags = False
        test_by_executor = False
        filter = None
        format = None
        helpfilter = False
        helpformat = False

    # testing buildtest buildspec find --paths
    func_buildspec_find(args)


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
        test_by_tags = False
        test_by_executor = False
        filter = None
        format = None
        helpfilter = True
        helpformat = False

    # testing buildtest buildspec find --helpfilter
    func_buildspec_find(args)

    class args:
        find = True
        rebuild = False
        root = None
        buildspec_files = False
        executors = False
        tags = False
        paths = False
        test_by_tags = False
        test_by_executor = False
        filter = {"tags": "fail"}
        format = None
        helpfilter = False
        helpformat = False

    # testing buildtest buildspec find --filter tags=fail
    func_buildspec_find(args)

    class args:
        find = True
        rebuild = False
        root = None
        buildspec_files = False
        executors = False
        tags = False
        paths = False
        test_by_tags = False
        test_by_executor = False
        filter = {
            "type": "script",
            "executor": "local.sh",
            "tags": "fail",
        }
        format = None
        helpfilter = False
        helpformat = False

    # testing buildtest buildspec find --filter type=script,executor=local.sh,tags=fail
    func_buildspec_find(args)

    # testing buildtest buildspec find --filter key1=val1,key2=val2
    with pytest.raises(BuildTestError):

        class args:
            find = True
            rebuild = False
            root = None
            buildspec_files = False
            executors = False
            tags = False
            paths = False
            test_by_tags = False
            test_by_executor = False
            filter = {"key1": "val1", "key2": "val2"}
            format = None
            helpfilter = False
            helpformat = False

        func_buildspec_find(args)


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
        test_by_tags = False
        test_by_executor = False
        filter = None
        format = None
        helpfilter = False
        helpformat = True

    # testing buildtest buildspec find --helpformat
    func_buildspec_find(args)

    class args:
        find = True
        rebuild = False
        root = None
        buildspec_files = False
        executors = False
        tags = False
        paths = False
        test_by_tags = False
        test_by_executor = False
        filter = None
        format = "name,type,executor,description,buildspecs"
        helpfilter = False
        helpformat = False

    # testing buildtest buildspec find --helpformat
    func_buildspec_find(args)

    # testing buildtest buildspec find --format field1 should raise error. Any
    # invalid format fields will raise an exception of type BuildTestError
    with pytest.raises(BuildTestError):

        class args:
            find = True
            rebuild = False
            root = None
            buildspec_files = False
            executors = False
            tags = False
            paths = False
            test_by_tags = False
            test_by_executor = False
            filter = None
            format = "field1"
            helpfilter = False
            helpformat = False

        func_buildspec_find(args)


@pytest.mark.cli
def test_buildspec_find_roots():

    repo_root = os.path.dirname(os.path.dirname(__file__))
    root_buildspecs = [
        os.path.join(repo_root, "tests", "buildsystem"),
        os.path.join(repo_root, "tutorials"),
    ]

    class args:
        find = True
        rebuild = False
        root = root_buildspecs
        buildspec_files = False
        executors = False
        tags = False
        paths = False
        test_by_tags = False
        test_by_executor = False
        filter = None
        format = None
        helpfilter = False
        helpformat = False

    # running buildtest buildspec find --root /path/to/buildtest/tests/buildsystem --root /path/to/buildtest/tutorials/
    func_buildspec_find(args)

    class args:
        find = True
        rebuild = False
        root = [
            os.path.join(repo_root, "README.rst"),
            os.path.join(repo_root, "tutorials", "environment.yml"),
        ]
        buildspec_files = False
        executors = False
        tags = False
        paths = False
        test_by_tags = False
        test_by_executor = False
        filter = None
        format = None
        helpfilter = False
        helpformat = False

    # running buildtest buildspec find --root /path/to/buildtest/README.rst --root /path/to/buildtest/tutorials/environment.yml
    func_buildspec_find(args)
