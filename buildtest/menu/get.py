"""
This module contains all the methods related to "buildtest get" which is used
for retrieving test repository that can be used for building tests with buildtest.
"""

import logging
import os
import re
import sys

from buildtest.config import get_default_settings
from buildtest.defaults import BUILDSPEC_DEFAULT_PATH
from buildtest.utils.file import create_dir

logger = logging.getLogger(__name__)


def func_get_subcmd(args):
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
        sys.exit("Currently only GitHub is supported for buildtest get.")

    config_opts = get_default_settings()
    repo_path = None
    if config_opts.get("config").get("paths").get("get_repo_path"):
        repo_path = os.path.realpath(
            config_opts.get("config").get("paths").get("get_repo_path")
        )
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

    # Ensure https prefix is provided
    if not re.search("^(http|git@)", url):
        url = "https://%s" % url

    # Fail early if path exists
    if os.path.exists(dest):
        sys.exit("%s already exists. Remove and try again." % dest)

    return_code = os.system("git clone -b %s %s %s" % (branch, url, dest))
    if return_code == 0:
        return dest
    sys.exit("Error cloning repo %s" % url)
