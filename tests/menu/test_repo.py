import pytest
import os
import random
import shutil
import string
import yaml
from buildtest.defaults import BUILDSPEC_DEFAULT_PATH, REPO_FILE
from buildtest.menu.repo import (
    clone,
    func_repo_add,
    func_repo_list,
    func_repo_remove,
    get_repo_paths,
    func_repo_update,
)
from buildtest.utils.file import is_dir


class none_repo:
    repo = None


class only_github_repo:
    repo = "https://gitlab.com/gitlab-org/gitlab.git"


class ssh_repo:
    repo = "git@github.com:buildtesters/buildtest-stampede2.git"
    branch = "master"


class repo_list_command:
    show = None


class repo_list_show_command:
    show = True


def test_clone(tmp_path):
    https_link = "https://github.com/buildtesters/tutorials.git"

    assert is_dir(clone(https_link, tmp_path))

    class args:
        repo = "buildtesters/tutorials"
        state = "disabled"

    func_repo_update(args)

    # cloning same repo twice will result in failure
    with pytest.raises(SystemExit):
        clone(https_link, tmp_path)

    # shutil.rmtree(tmp_path)
    # will fail to clone if invalid branch is specified
    with pytest.raises(SystemExit):
        clone(https_link, tmp_path, "develop")

    class args:
        repo = "buildtesters/tutorials"

    func_repo_remove(args)


def test_func_repo_add():

    # check if repo is None, this raises error
    with pytest.raises(SystemExit):
        func_repo_add(none_repo)

    # currently we support fetching github repos, so testing a gitlab repo
    with pytest.raises(SystemExit):
        func_repo_add(only_github_repo)

    avail_repos = func_repo_list(repo_list_command)
    # remove buildtesters/buildtest-cori before adding to list to ensure
    # directory does not exist and entry is removed from REPO_FILE
    if "buildtesters/buildtest-cori" in avail_repos:

        class args:
            repo = "buildtesters/buildtest-cori"

        func_repo_remove(args)

    class args:
        repo = "http://github.com/buildtesters/buildtest-cori"
        branch = "master"

    # test http link
    func_repo_add(args)


@pytest.mark.skipif(
    "TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
    reason="Skipping Travis Test",
)
def test_ssh_clone():
    # test ssh repo
    func_repo_add(ssh_repo)
    url = ssh_repo.repo.split(":")[1]
    username = url.split("/")[0]
    repo = ssh_repo.repo.split("/")[-1]
    repo_path = os.path.join(BUILDSPEC_DEFAULT_PATH, "github.com", username, repo)
    repo_path = os.path.basename(repo_path).replace(".git", "")
    print(f"Checking repo destination path {repo_path}")
    assert repo_path


def test_func_repo_list():

    func_repo_list(repo_list_command)
    func_repo_list(repo_list_show_command)


def test_func_repo_remove():
    class args:
        repo = None

    # checking invalid argument
    with pytest.raises(SystemExit):
        func_repo_remove(args)

    # generate random repo string
    class args:
        repo = "".join(random.choice(string.ascii_letters) for i in range(10))

    # testing invalid repo name, when it's not found in dictionary
    with pytest.raises(SystemExit):
        func_repo_remove(args)

    with open(REPO_FILE, "r") as fd:
        repo_dict = yaml.load(fd.read(), Loader=yaml.SafeLoader)

    repo_entries = list(repo_dict.keys())
    # ensure repo_entries is not an empty dict
    assert repo_entries

    class args:
        show = False

    avail_repos = func_repo_list(args)
    assert avail_repos

    for repository in avail_repos:
        # get first item in repo dictionary
        class args:
            repo = repository

        func_repo_remove(args)


def test_repofile_not_found():

    shutil.copyfile(REPO_FILE, REPO_FILE + ".bak")
    os.remove(REPO_FILE)

    class args:
        repo = "buildtesters/buildtest-cori"

    # since REPO_FILE does not exist this will raise an error
    with pytest.raises(SystemExit):
        func_repo_remove(args)

    # when REPO file not found get_repo_paths() will return empty list
    assert not get_repo_paths()

    class args:
        show = True

    with pytest.raises(SystemExit):
        func_repo_list(args)

    shutil.move(REPO_FILE + ".bak", REPO_FILE)
