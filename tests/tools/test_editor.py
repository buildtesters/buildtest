import os

import pytest
from buildtest.exceptions import BuildTestError
from buildtest.tools.editor import set_editor


def test_editor():
    set_editor("vi")
    set_editor("vim")
    set_editor("emacs")
    set_editor("nano")

    with pytest.raises(BuildTestError):
        set_editor("notepad")

    os.environ["EDITOR"] = "notepad"
    with pytest.raises(BuildTestError):
        set_editor("notepad")
