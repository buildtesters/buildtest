import os
import subprocess
import sys

from buildtest.buildsystem.parser import BuildspecParser
from buildtest.executors.setup import BuildExecutor
from buildtest.utils.file import is_dir, resolve_path


def edit_buildspec(buildspec, configuration):
    """Open buildspec in editor and validate buildspec with parser"""
    buildspec = resolve_path(buildspec, exist=False)
    if is_dir(buildspec):
        sys.exit(f"buildspec: {buildspec} is a directory, please specify a file type")

    EDITOR = os.environ.get("EDITOR", "vim")

    subprocess.call([EDITOR, buildspec])

    print(f"Writing file: {buildspec}")

    be = BuildExecutor(configuration)
    BuildspecParser(buildspec, be)
