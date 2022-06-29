import os
import shutil

from buildtest.defaults import console
from buildtest.utils.file import resolve_path


def set_editor(editor=None):
    """Set the editor used for editing files. The editor can be set based on environment ``EDITOR`` or passed as argument
    ``buildtest --editor``. The editor must be one of the following: vi, vim, emacs, nano.

    We check the path to editor before setting value to editor.

    Args:
        editor (str, optional): Select choice of editor specified via ``buildtest --editor``

    Returns:
        str: Return full path to editor
    """
    # prefer command line

    default_editor = shutil.which("vi")

    valid_editors = ["vim", "vi", "emacs", "nano"]

    for editor_name in valid_editors:
        buildtest_editor = shutil.which(editor_name)
        if buildtest_editor:
            break

    # environment variable
    if os.environ.get("EDITOR"):
        buildtest_editor = resolve_path(shutil.which(os.environ["EDITOR"]))

        if not buildtest_editor:
            console.print(
                f"[red]Unable to resolve path via environment EDITOR: {os.environ['EDITOR']}"
            )

    # command line option --editor is specified
    if editor:
        buildtest_editor = resolve_path(shutil.which(editor))
        if not buildtest_editor:
            console.print(
                f"[red]Unable to resolve path to editor specified via command line argument --editor: {editor}"
            )

    # if editor is not found return the default editor which is vi
    if not buildtest_editor:
        return default_editor

    return buildtest_editor
