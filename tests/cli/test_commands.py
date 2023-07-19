import pytest
from buildtest.cli.commands import commands_cmd


def test_commands_cmd():
    with pytest.raises(SystemExit):
        commands_cmd()