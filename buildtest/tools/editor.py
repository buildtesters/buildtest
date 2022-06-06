import os
import re
import shutil
import subprocess

from buildtest.exceptions import BuildTestError
from buildtest.utils.file import resolve_path


def is_emacs(emacs_editor):

    cmd = subprocess.run(
        [emacs_editor, "--version"], capture_output=True, universal_newlines=True
    )

    match = re.match("^(GNU Emacs)", cmd.stdout)
    return match


def is_vi(vi_editor):

    cmd = subprocess.run(
        [vi_editor, "--version"], capture_output=True, universal_newlines=True
    )

    match = re.match("^(VIM -)", cmd.stdout)
    return match


def is_nano(nano_editor):
    """Check whether editor is nano by running ``nano --version`` and checking regular expression for output

    Args:
        nano_editor (str): Path to editor

    Returns:
        bool: True if editor is nano otherwise returns False
    """
    cmd = subprocess.run(
        [nano_editor, "--version"], capture_output=True, universal_newlines=True
    )
    match = re.match("( GNU nano)", cmd.stdout)
    return match


def set_editor(editor=None):
    """Set the editor used for editing files. The editor can be set based on environment ``EDITOR`` or passed as argument
    ``buildtest --editor``. The editor must be one of the following: vi, vim, emacs, nano.

    We check the path to editor before setting value to editor.

    """
    # prefer command line

    valid_editors = ["vim", "vi", "emacs", "nano"]

    for editor_name in valid_editors:
        buildtest_editor = shutil.which(editor_name)
        if buildtest_editor:
            break

    # environment variable
    if os.environ.get("EDITOR"):
        buildtest_editor = resolve_path(shutil.which(os.environ["EDITOR"]))

        if not buildtest_editor:
            raise BuildTestError(
                f"Unable to resolve path via environment EDITOR: {os.environ['EDITOR']}"
            )

    # command line option --editor is specified
    if editor:
        buildtest_editor = resolve_path(shutil.which(editor))
        if not buildtest_editor:
            raise BuildTestError(
                f"Unable to resolve path to editor specified via command line argument --editor: {editor}"
            )

    if not (
        is_emacs(buildtest_editor)
        or is_vi(buildtest_editor)
        or is_nano(buildtest_editor)
    ):
        raise BuildTestError(
            f"Invalid editor please select one of the following editors: {valid_editors}"
        )

    return buildtest_editor
