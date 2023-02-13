import pytest
from buildtest.exceptions import BuildTestError
from buildtest.utils.command import BuildTestCommand


@pytest.mark.utility
class TestBuildTestCommand:
    def test_command(self):
        cmd = "hostname"
        a = BuildTestCommand(cmd)
        a.execute()

        out, err, ret = a.get_output(), a.get_error(), a.returncode()

        print(f"Command: {cmd}")
        print(f"Output: {out}")
        print(f"Error: {err}")
        print(f"Return Code: {ret}")
        assert 0 == ret

    def test_error_command(self):
        cmd = "xyz"
        a = BuildTestCommand(cmd)
        a.execute()

        out, err, ret = a.get_output(), a.get_error(), a.returncode()

        print(f"Command: {cmd}")
        print(f"Output: {out}")
        print(f"Error: {err}")
        print(f"Return Code: {ret}")

        assert 0 != ret

    def test_invalid_type(self):
        query = ["hostname"]
        # input type must be a string otherwise it will raise an exception
        with pytest.raises(BuildTestError):
            BuildTestCommand(query)
