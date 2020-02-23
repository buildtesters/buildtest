"""
This module contains all the methods related to "buildtest build" which is used
for building test scripts from test configuration.
"""


import os
import re
import sys

from buildtest.tools.config import config_opts
from buildtest.tools.defaults import TESTCONFIG_ROOT

from buildtest.tools.file import create_dir
from buildtest.tools.log import init_log


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

    logger, LOGFILE = init_log(config_opts)
    root = os.path.join(TESTCONFIG_ROOT, "github.com")
    create_dir(root)

    # Parse the repository name
    username = args.repo.split("/")[-2]
    repo = args.repo.split("/")[-1]
    clone_path = os.path.join(root, username)
    create_dir(clone_path)

    # Clone to install
    dest = clone(args.repo, clone_path)
    logger.info("%s cloned to %s" % (args.repo, dest))


def clone(url, dest):
    """clone a repository from Github"""
    name = os.path.basename(url).replace(".git", "")
    dest = os.path.join(dest, name)

    # Ensure https prefix is provided
    if not re.search("^(http|git@)", url):
        url = "https://%s" % url

    return_code = os.system("git clone %s %s" % (url, dest))
    if return_code == 0:
        return dest
    sys.exit("Error cloning repo %s" % url)
