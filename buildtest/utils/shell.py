import shutil

from buildtest.exceptions import BuildTestError
from buildtest.utils.command import BuildTestCommand
from buildtest.utils.file import is_file


def get_shells():
    """Return a list of shell returned from /etc/shells file. If file exist we return a list
    The command we run is the following which will omit any lines that start with ``#`` which
    is for comments. If file doesn't exist we return an empty list

    .. code-block:: console

        $ grep '^[^#]' /etc/shells
        /bin/bash
        /bin/csh
        /bin/dash
        /bin/ksh
        /bin/sh
        /bin/tcsh
        /bin/zsh

    Returns:
        list: Return a list of shells
    """

    etc_shell = "/etc/shells"
    if not is_file(etc_shell):
        return []

    cmd = BuildTestCommand(f"grep '^[^#]' {etc_shell}")
    cmd.execute()
    out = cmd.get_output()
    out = [item.strip() for item in out]

    return out


def get_python_shells():
    """Return a list of all python shells by running ``which -a python3 python`` which
    will report full path to all python and python3 wrapper in current $PATH.

    Shown below is an expected output.

    .. code-block:: console

        $ which -a python3 python
        /Users/siddiq90/.local/share/virtualenvs/buildtest-KLOcDrW0/bin/python3
        /usr/local/bin/python3
        /usr/bin/python3
        /Users/siddiq90/.local/share/virtualenvs/buildtest-KLOcDrW0/bin/python
        /usr/bin/python

    Returns:
        list: A list of full path to python shells
    """

    python_shells = []

    cmd = BuildTestCommand(f"which -a python python3")
    cmd.execute()
    out = cmd.get_output()
    python_shells += [item.strip() for item in out]

    return python_shells


python_shells = get_python_shells()
system_shells = get_shells()


class Shell:
    def __init__(self, shell="bash"):
        """The Shell initializer takes an input shell and shell options and split
        string by shell name and options.

        Args:
            shell (str): Specify shell program and any options passed to shell. Defaults to ``bash``
        """

        # enforce input argument 'shell' to be a string
        if not isinstance(shell, str):
            raise BuildTestError(
                f"Invalid type for input: {shell} must be of type 'str'"
            )

        self.name = shell.split()[0]

        self.valid_shells = (
            system_shells
            + python_shells
            + ["bash", "csh", "tcsh", "sh", "zsh", "python", "python3"]
        )

        # if input shell is not in list of valid shells we raise error.
        if self.name not in self.valid_shells:
            raise BuildTestError(
                f"Invalid shell: {self.name} select from one of the following shells: {self.valid_shells}"
            )

        self._opts = " ".join(shell.split()[1:])
        self.path = self.name

    @property
    def opts(self):
        """retrieve the shell opts that are set on init, and updated with setter"""
        return self._opts

    @opts.setter
    def opts(self, shell_opts):
        """Override the shell options in class attribute, this would be useful
        when shell options need to change due to change in shell program.
        """
        self._opts = shell_opts
        return self._opts

    @property
    def path(self):
        """This method returns the full path to shell program using ``shutil.which()``
        If shell program is not found we raise an exception. The shebang is
        is updated assuming path is valid which is just adding character '#!'
        in front of path. The return is full path to shell program. This method
        automatically updates the shell path when there is a change in attribute
        self.name

        >>> shell = Shell("bash")
        >>> shell.path
        '/usr/bin/bash'
        >>> shell.name="sh"
        >>> shell.path
        '/usr/bin/sh'

        """
        return self._path

    # Identity functions
    def __str__(self):
        return "[buildtest.shell][%s]" % self.name

    def __repr__(self):
        return self.__str__()

    @path.setter
    def path(self, name):
        """If the user provides a new path with a name, do same checks to
        ensure that it's found.
        """
        path = shutil.which(name)

        # raise an exception if shell program is not found
        if not path:
            raise BuildTestError(f"Can't find program: {name}")

        # Update the name not that we are sure path is found
        self.name = name

        # if input shell is not in list of valid shells we raise error.
        if self.name not in self.valid_shells:
            raise BuildTestError(
                f"Please select one of the following shells: {self.valid_shells}"
            )

        self._path = path

        # shebang is formed by adding the char '#!' with path to program
        self.shebang = f"#!{path}"

    def get(self):
        """Return shell attributes as a dictionary"""
        return {
            "name": self.name,
            "opts": self._opts,
            "path": self._path,
            "shebang": self.shebang,
        }
