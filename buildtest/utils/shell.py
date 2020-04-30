import shutil
from buildtest.exceptions import BuildTestError


class Shell:
    def __init__(self, shell):
        """ The Shell initializer takes an input shell and shell options and split
            string by shell name and options.

            Parameters:

            :param shell: specify shell program and any options passed to shell
            :type shell: str
        """

        # enforce input argument 'shell' to be a string
        if not isinstance(shell, str):
            raise BuildTestError(
                f"Invalid type for input: {shell} must be of type 'str'"
            )

        self.name = shell.split()[0]
        self.opts = " ".join(shell.split()[1:])

    def opts(self, shell_opts):
        """Override the shell options in class attribute, this would be useful
           when shell options need to change due to change in shell program."""

        self.opts = shell_opts

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

        path = shutil.which(self.name)

        # raise an exception if shell program is not found
        if not path:
            raise BuildTestError(f"Can't find program: {self.name}")

        # shebang is formed by adding the char '#!' with path to program
        self.shebang = f"#!{path}"
        return path

    def get(self):
        """Return shell attributes as a dictionary"""

        self.shell = {}
        self.shell["name"] = self.name
        self.shell["opts"] = self.opts
        self.shell["path"] = self.path
        self.shell["shebang"] = self.shebang
        return self.shell
