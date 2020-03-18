from buildtest.utils.command import BuildTestCommand


class TestBuildTestCommand:
    def test_command(self):

        cmd = "hostname"
        a = BuildTestCommand(cmd)
        a.execute()

        out, err, ret = a.get_output(), a.get_error(), a.returncode

        print("Command: {cmd}")
        print(f"Output: {out}")
        print(f"Error: {err}")
        print(f"Return Code: {ret}")
        assert 0 == ret

    def test_error_command(self):

        cmd = "xyz"
        a = BuildTestCommand(cmd)
        a.execute()

        out, err, ret = a.get_output(), a.get_error(), a.returncode

        print("Command: {cmd}")
        print(f"Output: {out}")
        print(f"Error: {err}")
        print(f"Return Code: {ret}")

        assert 0 != ret
