from buildtest.utils.command import BuildTestCommand

def test_command1():

    cmd = "hostname -f"
    a = BuildTestCommand(cmd)
    out, err = a.execute()
    ret = a.returnCode()

    print(f"Command: {cmd}")
    print(f"Output: {out}")
    print(f"Error: {err}")
    print(f"Return Code: {ret}")

    assert 0 == ret

def test_command2():

    cmd = "echo $SHELL"
    a = BuildTestCommand(cmd)
    a.execute()

    out = a.get_output()
    err = a.get_error()
    ret = a.returnCode()

    print(f"Command: {cmd}")
    print(f"Output: {out}")
    print(f"Error: {err}")
    print(f"Return Code: {ret}")


