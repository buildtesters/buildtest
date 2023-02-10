import shutil

import pytest
from buildtest.exceptions import BuildTestError
from buildtest.utils.shell import Shell


class TestShell:
    @pytest.mark.utility
    def test_default_shell(self):
        # creating a Shell object with no argument will result in bash shell

        shell = Shell()
        # checking if shell.name is bash
        assert shell.name == "bash"
        # check shell.path and shebang is full path to bash reported by shutil.which
        assert shell.path == shutil.which("bash")
        assert shell.shebang == f"#!{shutil.which('bash')}"

    @pytest.mark.utility
    def test_sh_shell(self):
        # create a sh shell
        shell = Shell("sh")
        assert shell.name == "sh"
        assert shell.path == shutil.which("sh")
        assert shell.shebang == f"#!{shutil.which('sh')}"

        # pass shell options to shell
        shell = Shell("sh -x")
        assert shell.name == "sh"
        assert shell.opts == "-x"
        assert shell.path == shutil.which("sh")

        # create a sh shell
        shell = Shell("/bin/sh")
        assert shell.name == "/bin/sh"
        assert shell.path == shutil.which("/bin/sh")
        assert shell.shebang == f"#!{shutil.which('/bin/sh')}"

    @pytest.mark.utility()
    def test_bash_shell(self):
        shell = Shell("/bin/bash")
        assert shell.name == "/bin/bash"
        assert shell.path == shutil.which("/bin/bash")
        assert shell.shebang == f"#!{shutil.which('/bin/bash')}"

        shell = Shell("bash")
        assert shell.name == "bash"
        assert shell.path == shutil.which("bash")
        assert shell.shebang == f"#!{shutil.which('bash')}"

    @pytest.mark.utility()
    def test_zsh_shell(self):
        if not shutil.which("bin/zsh"):
            pytest.skip("Skipping test for zsh shell")

        shell = Shell("/bin/zsh")
        assert shell.name == "/bin/zsh"
        assert shell.path == shutil.which("/bin/zsh")
        assert shell.shebang == f"#!{shutil.which('/bin/zsh')}"

        shell = Shell("zsh")
        assert shell.name == "zsh"
        assert shell.path == shutil.which("zsh")
        assert shell.shebang == f"#!{shutil.which('zsh')}"

    @pytest.mark.utility()
    def test_csh_shell(self):
        if not shutil.which("bin/csh"):
            pytest.skip("Skipping test for csh shell")

        shell = Shell("/bin/csh")
        assert shell.name == "/bin/csh"
        assert shell.path == shutil.which("/bin/csh")
        assert shell.shebang == f"#!{shutil.which('/bin/csh')}"

        shell = Shell("csh")
        assert shell.name == "csh"
        assert shell.path == shutil.which("csh")
        assert shell.shebang == f"#!{shutil.which('csh')}"

    @pytest.mark.utility()
    def test_tcsh_shell(self):
        if not shutil.which("bin/tcsh"):
            pytest.skip("Skipping test for tcsh shell")

        shell = Shell("/bin/tcsh")
        assert shell.name == "/bin/tcsh"
        assert shell.path == shutil.which("/bin/tcsh")
        assert shell.shebang == f"#!{shutil.which('/bin/tcsh')}"

        shell = Shell("tcsh")
        assert shell.name == "tcsh"
        assert shell.path == shutil.which("tcsh")
        assert shell.shebang == f"#!{shutil.which('tcsh')}"

    @pytest.mark.utility
    def test_update_instance(self):
        # create a sh shell
        shell = Shell("sh")
        assert shell.name == "sh"
        # check shell.path and shebang is full path to bash reported by shutil.which
        assert shell.path == shutil.which("sh")
        assert shell.shebang == f"#!{shutil.which('sh')}"

        # if system doesn't have /bin/csh then we should expect this to raise exception
        try:
            shell.path = "/bin/csh"
        except BuildTestError:
            return

        # check instance attribute match from ones reported from get method
        assert shell.get()["name"] == shell.name
        assert shell.get()["path"] == shell.path

        # update shell opts and check value reported by get method
        shell.opts = ["-v"]
        assert shell.get()["opts"] == shell.opts

    @pytest.mark.utility
    def test_shell_exceptions(self, tmp_path):
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

        # input must be valid shell we can't set shell to arbitrary linux command
        with pytest.raises(BuildTestError):
            Shell("pwd")

        # test invalid shell with shell options
        with pytest.raises(BuildTestError):
            Shell("ls -l ")

        # invoking a valid shell but later changing shell path to an invalid shell will result in error
        with pytest.raises(BuildTestError):
            shell = Shell()
            shell.path = "/bin/ls"
