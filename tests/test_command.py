from buildtest.utils.command import BuildTestCommand

class TestBuildTestCommand:

    def test_command(self):

        a = BuildTestCommand()
        cmd = "hostname"
        a.execute(cmd)

        out, ret = a.get_output(), a.get_error(), a.returnCode()

        print ("Command: {cmd}")
        print (f"Output: {out}")
        print (f"Error: {err}")
        print (f"Return Code: {ret}")
        assert 0 == ret

    def test_error_command(self):

        a = BuildTestCommand()
        cmd = "xyz"
        a.execute(cmd)

        out, err, ret = a.get_output(), a.get_error(), a.returnCode()

        print ("Command: {cmd}")
        print (f"Output: {out}")
        print (f"Error: {err}")
        print (f"Return Code: {ret}")

        assert 0 != ret

