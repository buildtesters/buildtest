"""
This module contains all the methods related to "buildtest get" which is used
for retrieving test repository that can be used for building tests with buildtest.
"""

import logging
import os
import re
import shutil
import sys
import yaml

from buildtest.config import load_settings
from buildtest.defaults import BUILDSPEC_DEFAULT_PATH, REPO_FILE
from buildtest.utils.file import create_dir, is_file, resolve_path, is_dir

logger = logging.getLogger(__name__)


def func_repo_add(args):
    """Entry point for ``buildtest get`` sub-command. The expected
    single argument provided should be a valid repository address to clone.

    :param args: arguments passed from command line
    :type args: dict, required

    :rtype: None
    """
    if not args.repo:
        sys.exit("A repository address is required.")

    # Currently just support for GitHub
    if not re.search("github.com", args.repo):
        sys.exit("Currently only GitHub is supported by buildtest.")

    config_opts = load_settings()
    repo_path = None

    # if clonepath key is defined than override value generated from 'prefix'

    clonepath = config_opts.get("config", {}).get("paths", {}).get("clonepath")
    prefix = config_opts.get("config", {}).get("paths", {}).get("prefix")

    clone_prefix = clonepath or prefix

    if clone_prefix:
        # resolve clone prefix, this accounts for shell expansion, directory expansion and gets realpath. We don't care if path exists to ensure we don't return None
        repo_path = resolve_path(clone_prefix, exist=False)

    # it is possible prefix and clonepath are not defined, in that case we used default value
    repo_search_path = repo_path or BUILDSPEC_DEFAULT_PATH
    root = os.path.join(repo_search_path, "github.com")
    create_dir(root)

    # Parse the repository name assumes it is using HTTPS in format https://github.com/<username>/<repo>.git
    username = args.repo.split("/")[-2]

    # resolve url when its using SSH in format git@github.com:<username>/<repo>
    if re.search("^(git@github.com)", args.repo):
        url = args.repo.split(":")[1]
        username = url.split("/")[0]

    clone_path = os.path.join(root, username)
    create_dir(clone_path)

    # Clone to install
    dest = clone(args.repo, clone_path, args.branch)
    logger.info("%s cloned to %s" % (args.repo, dest))


def clone(url, dest, branch="master"):
    """Clone a repository from Github

       Parameters:

       :param url: URL to Github repository to clone
       :type url: str, required
       :param dest: location where to clone repo
       :type dest: str, required
       :param branch: select which branch to clone, defaults to 'master' branch
       :type branch: str, optional
    """

    name = os.path.basename(url).replace(".git", "")
    dest = os.path.join(dest, name)

    # If http prefix is provided, change this to https
    if re.search("^(http://)", url):
        url = "https://" + url.split("http://")[1]

    # get repository entry for example https://github.com/buildtesters/buildtest-cori
    # this will extract buildtesters/buildtest-cori
    if re.search("^(https)", url):
        username = url.split("/")[-2]
        reponame = url.split("/")[-1]
    # otherwise entry will be SSH so for example git@github.com:buildtesters/buildtest-stampede2.git
    # this will retrieve buildtesters/buildtest-stampede2
    else:
        username = url.split(":")[1].split("/")[0]
        reponame = url.split(":")[1].split("/")[1]

    reponame = reponame.replace(".git", "")

    # Fail early if path exists
    if os.path.exists(dest):
        sys.exit("%s already exists. Remove and try again." % dest)

    return_code = os.system("git clone -b %s %s %s" % (branch, url, dest))

    if return_code != 0:
        sys.exit("Error cloning repo %s" % url)

    repo_entry = os.path.join(username, reponame)
    repo_dict = {}

    # if file exists, then read file and load YAML into repo_dict
    if is_file(REPO_FILE):
        with open(REPO_FILE, "r") as fd:
            repo_dict = yaml.load(fd.read(), Loader=yaml.SafeLoader)

    # if its new entry add to file otherwise file won't be updated
    if repo_entry not in repo_dict.keys():
        repo_dict[repo_entry] = {}
        repo_dict[repo_entry]["url"] = url
        repo_dict[repo_entry]["dest"] = dest
        repo_dict[repo_entry]["branch"] = branch
        repo_dict[repo_entry]["state"] = "enabled"
        with open(REPO_FILE, "w") as fd:
            yaml.dump(repo_dict, fd, default_flow_style=False)

    return dest


def func_repo_list(args):
    """This method implements ``buildtest repo list`` which shows content of all
       repositories from REPO_FILE. If no repositories are found we print a message
       and return otherwise we show the list of repository entries when
       ``buildtest repo list`` is issued, if ``buildtest repo list -s`` is
       issued we show content of REPO_FILE.
    """

    if not is_file(REPO_FILE):
        raise SystemExit(
            "No repositories found, please consider adding a repository via 'buildtest repo add'"
        )

    with open(REPO_FILE, "r") as fd:
        repo_dict = yaml.load(fd.read(), Loader=yaml.SafeLoader)

    # if no repos found we return with message
    if not repo_dict:
        print("No repositories found")
        return

    # show content of yaml file if buildtest repo list --show is issued otherwise
    # report a list of all repositories.
    if args.show:
        print(yaml.dump(repo_dict, default_flow_style=False))
    else:
        for repo in repo_dict.keys():
            print(repo)


def active_repos():
    """ Return list of active repository names from REPO_FILE

        :return: list of repository names as string type
        :rtype: list
    """
    repo_dict = {}

    if not is_file(REPO_FILE):
        return []

    with open(REPO_FILE, "r") as fd:
        repo_dict = yaml.load(fd.read(), Loader=yaml.SafeLoader)

    return list(repo_dict.keys())


def validate_repos():
    """Remove any invalid repos from repo file when destination path is removed
       manually but repo entry exists.
    """

    if not is_file(REPO_FILE):
        return

    with open(REPO_FILE, "r") as fd:
        repo_dict = yaml.load(fd.read(), Loader=yaml.SafeLoader)

    invalid_repos = []
    # remove any repos that don't have dest directory defined
    for repo in repo_dict.keys():
        if not is_dir(repo_dict[repo]["dest"]):
            invalid_repos.append(repo)

    if invalid_repos:
        print("Removing invalid repos:", invalid_repos)
        for repo in invalid_repos:
            del repo_dict[repo]

        with open(REPO_FILE, "w") as fd:
            yaml.dump(repo_dict, fd, default_flow_style=False)


def get_repo_paths(repo_name=None):
    """ Return list of destination path where repositories are cloned. This
        is used to build the buildspec search path.

        :return: A list of directory path where repos are cloned
        :rtype: list
    """

    dest_paths = []

    if not is_file(REPO_FILE):
        return

    validate_repos()

    with open(REPO_FILE, "r") as fd:
        repo_dict = yaml.load(fd.read(), Loader=yaml.SafeLoader)

    if repo_name and repo_name in active_repos():
        return repo_dict[repo_name]["dest"]

    for repo in repo_dict.keys():
        if repo_dict[repo]["state"] == "enabled":
            dest_paths.append(repo_dict[repo]["dest"])

    return dest_paths


def func_repo_remove(args):
    """This method implements command ``buildtest repo rm`` which removes repository
       entries from REPO_FILE and updates file. """

    if not is_file(REPO_FILE):
        raise SystemExit(f"Unable to find repository file: {REPO_FILE}")

    with open(REPO_FILE, "r") as fd:
        repo_dict = yaml.load(fd.read(), Loader=yaml.SafeLoader)

    if not args.repo in repo_dict.keys():
        raise SystemExit(f"Unable to delete repository {args.repo}")

    destdir = repo_dict[args.repo]["dest"]
    shutil.rmtree(destdir)
    print(f"Removing Repository: {args.repo} and deleting files from {destdir}")

    del repo_dict[args.repo]
    with open(REPO_FILE, "w") as fd:
        yaml.dump(repo_dict, fd, default_flow_style=False)


def func_repo_update(args):
    """This method implements command ``buildtest repo update`` which
       allows user to enable/disable repository state.
    """

    if not is_file(REPO_FILE):
        raise SystemExit(f"Unable to find repository file: {REPO_FILE}")

    with open(REPO_FILE, "r") as fd:
        repo_dict = yaml.load(fd.read(), Loader=yaml.SafeLoader)

    repo_dict[args.repo]["state"] = args.state
    with open(REPO_FILE, "w") as fd:
        yaml.dump(repo_dict, fd, default_flow_style=False)

    print(f"Update repo: {args.repo} to state: {args.state}")
