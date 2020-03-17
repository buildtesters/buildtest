import pytest
from buildtest.utils.command import BuildTestCommand
from buildtest.exceptions import BuildTestError


class TestBuildTestError:
    @pytest.mark.xfail(
        reason="Testing to see if exception of type BuildTestError is raised",
        raises=BuildTestError,
    )
    def test_exception(self):
        """This test will check if we can raise Exception of type BuildTestError"""

        cmd = "touch /etc/passwd"
        a = BuildTestCommand(cmd)
        a.execute()
        err = a.get_error()
        ret = a.returnCode()
        raise BuildTestError(
            f"Command: {cmd} failed, Return Code: {ret} with Error: {err}"
        )
