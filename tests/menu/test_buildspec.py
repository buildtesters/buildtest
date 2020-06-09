import os
import pytest


from buildtest.menu.buildspec import func_buildspec_find
from buildtest.menu.repo import func_repo_add
from buildtest.defaults import REPO_FILE
from buildtest.utils.file import is_file


def test_repofile_not_found():
    """"Testing when REPO_FILE does not exist, then ``buildtest buildspec find``
        should raise SystemExit
    """

    if is_file(REPO_FILE):
        os.remove(REPO_FILE)

    class args:
        find = True

    with pytest.raises(SystemExit):
        func_buildspec_find(args)


def test_func_buildspec_find():
    class args:
        repo = "http://github.com/buildtesters/buildtest-cori"
        branch = "master"

    func_repo_add(args)

    class args:
        find = True

    func_buildspec_find(args)
