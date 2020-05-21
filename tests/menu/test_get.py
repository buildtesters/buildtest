import pytest
import os
import shutil

from buildtest.defaults import BUILDSPEC_DEFAULT_PATH
from buildtest.menu.get import clone, func_get_subcmd
from buildtest.utils.file import is_dir


class none_repo:
    repo = None


class only_github_repo:
    repo = "https://gitlab.com/gitlab-org/gitlab.git"


class ssh_repo:
    repo = "git@github.com:buildtesters/buildtest-stampede2.git"
    branch = "master"


def test_clone(tmp_path):
    repo = "https://github.com/buildtesters/tutorials.git"
    http_link = "http://github.com/buildtesters/buildtest-cori"

    assert is_dir(clone(repo, tmp_path))

    # cloning same repo twice will result in failure
    with pytest.raises(SystemExit) as e_info:
        clone(repo, tmp_path)

    shutil.rmtree(tmp_path)
    # will fail to clone if invalid branch is specified
    with pytest.raises(SystemExit) as e_info:
        clone(repo, tmp_path, "develop")

    # check if repo is None, this raises error
    with pytest.raises(SystemExit) as e_info:
        func_get_subcmd(none_repo)

    # currently we support fetching github repos, so testing a gitlab repo
    with pytest.raises(SystemExit) as e_info:
        func_get_subcmd(only_github_repo)

    # test http link
    clone(http_link, tmp_path, "master")


@pytest.mark.skipif(
    "TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
    reason="Skipping Travis Test",
)
def test_ssh_clone():
    # test ssh repo
    func_get_subcmd(ssh_repo)
    url = ssh_repo.repo.split(":")[1]
    username = url.split("/")[0]
    repo = ssh_repo.repo.split("/")[-1]
    repo_path = os.path.join(BUILDSPEC_DEFAULT_PATH, "github.com", username, repo)
    repo_path = os.path.basename(repo_path).replace(".git", "")
    print(f"Checking repo destination path {repo_path}")
    assert repo_path
