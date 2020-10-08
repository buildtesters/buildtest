import pytest
from buildtest.exceptions import BuildTestError


class TestBuildTestError:
    @pytest.mark.utility
    @pytest.mark.xfail(
        reason="Testing to see if exception of type BuildTestError is raised",
        raises=BuildTestError,
    )
    def test_exception(self,):
        """This test will check if we can raise Exception of type BuildTestError"""
        error = BuildTestError(f"Failed to run command")
        assert hasattr(error, "msg")
        assert isinstance(error.msg, str)
        raise error

    @pytest.mark.utility
    @pytest.mark.xfail(
        reason="Testing to see if exception of type BuildTestError is raised",
        raises=BuildTestError,
    )
    def test_multi_args(self):
        """This test will check if we can raise Exception of type BuildTestError"""
        error = BuildTestError(f"This is", "an", "exception")
        assert isinstance(error.msg, str)
        raise error
