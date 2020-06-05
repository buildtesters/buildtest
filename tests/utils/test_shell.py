import pytest
import shutil
from buildtest.exceptions import BuildTestError
from buildtest.utils.shell import Shell


def test_default_shell():
    # creating a Shell object with no argument will result in bash shell

    shell = Shell()
    # checking if shell.name is bash
    assert shell.name == "bash"
    # check shell.path and shebang is full path to bash reported by shutil.which
    assert shell.path == shutil.which("bash")
    assert shell.shebang == f"#!{shutil.which('bash')}"


def test_sh_shell():
    # create a sh shell
    shell = Shell("sh")
    assert shell.name == "sh"

    # pass shell options to shell
    shell = Shell("sh -x")
    assert shell.name == "sh"
    assert shell.opts == "-x"


def test_update_instance():

    # create a sh shell
    shell = Shell("sh")
    assert shell.name == "sh"
    # check shell.path and shebang is full path to bash reported by shutil.which
    assert shell.path == shutil.which("sh")
    assert shell.shebang == f"#!{shutil.which('sh')}"

    # update attributes 'name' and 'path' in instance object
    shell.name = "python"
    shell.path = shutil.which("python")

    # check instance attribute match from ones reported from get method
    assert shell.get()["name"] == shell.name
    assert shell.get()["path"] == shell.path

    # update shell opts and check value reported by get method
    shell.opts = ["-v"]
    assert shell.get()["opts"] == shell.opts


def test_shell_exceptions(tmp_path):
    # Shell will raise an error if program is not found
    with pytest.raises(BuildTestError):
        Shell("xyz")

    # input argument to Shell must be a string, any other value will raise an exception
    with pytest.raises(BuildTestError):
        Shell(["sh"])

    shell = Shell()
    # update shell.path to invalid program will raise an error. In this case we use tmp_path to set a random filepath
    # to shell.path and we expect Shell to raise an exception of type BuildTestError
    with pytest.raises(BuildTestError):
        shell.path = tmp_path
