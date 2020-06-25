import os
import pytest


from buildtest.menu.buildspec import func_buildspec_find
from buildtest.menu.repo import func_repo_add
from buildtest.defaults import REPO_FILE, BUILDSPEC_CACHE_FILE
from buildtest.utils.file import is_file


def test_repofile_not_found():
    """"Testing when REPO_FILE does not exist, then ``buildtest buildspec find``
        should raise SystemExit
    """

    try:
        print(f"Removing File: {REPO_FILE}")
        os.remove(REPO_FILE)
    except OSError:
        pass

    try:
        print(f"Removing File: {BUILDSPEC_CACHE_FILE}")
        os.remove(BUILDSPEC_CACHE_FILE)
    except OSError:
        pass

    assert not is_file(REPO_FILE)
    assert not is_file(BUILDSPEC_CACHE_FILE)

    class args:
        find = True
        clear = False

    with pytest.raises(SystemExit):
        func_buildspec_find(args)


def test_func_buildspec_find():
    class args:
        repo = "http://github.com/buildtesters/buildtest-cori"
        branch = "master"

    func_repo_add(args)

    # testing buildtest buildspec find --clear
    class args:
        find = True
        clear = True

    func_buildspec_find(args)
