import json
import os
import pytest
from shutil import copyfile, move

from buildtest.menu.buildspec import func_buildspec_find, func_buildspec_view
from buildtest.menu.repo import func_repo_add, active_repos
from buildtest.defaults import REPO_FILE, BUILDSPEC_CACHE_FILE
from buildtest.utils.file import is_file


def test_func_buildspec_find():
    class args:
        repo = "http://github.com/buildtesters/tutorials"
        branch = "master"

    try:
        func_repo_add(args)
    except SystemExit:
        pass

    enabled_repos = active_repos()
    assert enabled_repos

    org_name = os.path.basename(os.path.dirname(args.repo))
    repo_name = os.path.basename(args.repo)
    repo = os.path.join(org_name, repo_name)
    print(repo)
    print(active_repos())
    assert repo in active_repos()

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

    with open(BUILDSPEC_CACHE_FILE, "r") as fd:
        buildspecs = json.loads(fd.read())

        # get first test name from first buildspec
        for file in buildspecs:
            test_name = buildspecs[file]["sections"][0]
            break
        print(f"Viewing buildspec test: {test_name}")

        class args:
            buildspec = test_name
            view = True
            edit = False

        func_buildspec_view(args)


def test_repofile_not_found_buildspec_find():
    """"Testing when REPO_FILE does not exist, then ``buildtest buildspec find``
        should raise SystemExit
    """
    backup_repofile = f"{REPO_FILE}.bak"
    backup_cache = f"{BUILDSPEC_CACHE_FILE}.bak"

    try:
        print(f"Creating Backup of Repo File: {REPO_FILE}")
        print(f"Creating Backup of Cache File: {BUILDSPEC_CACHE_FILE}")

        copyfile(REPO_FILE, backup_repofile)
        copyfile(BUILDSPEC_CACHE_FILE, backup_cache)

        os.remove(REPO_FILE)
        print(f"Removing File: {REPO_FILE}")

        os.remove(BUILDSPEC_CACHE_FILE)
        print(f"Removing File: {BUILDSPEC_CACHE_FILE}")
    except OSError:
        pass

    assert not is_file(REPO_FILE)
    assert not is_file(BUILDSPEC_CACHE_FILE)

    class args:
        find = True
        clear = False

    # running buildtest buildspec find when no repo file results in SystemExit. User is requested to add repo first
    with pytest.raises(SystemExit):
        func_buildspec_find(args)

    # restore from backup files
    move(backup_repofile, REPO_FILE)
    move(backup_cache, BUILDSPEC_CACHE_FILE)

