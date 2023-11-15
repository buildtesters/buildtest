import os
import shutil

from buildtest.tools.editor import set_editor


def test_editor():
    set_editor("vi")
    set_editor("vim")
    set_editor("emacs")
    set_editor("nano")

    # an invalid editor will force this method to return full path to default editor which is 'vi'
    assert set_editor("notepad") == shutil.which("vi")

    os.environ["EDITOR"] = "notepad"
    assert set_editor("notepad") == shutil.which("vi")
