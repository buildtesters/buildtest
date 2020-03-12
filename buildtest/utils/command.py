import subprocess


class BuildTestCommand:
    """Class method to invoke shell commands and retrieve output and error. This class
    makes use of **subprocess.Popen()** to run the shell command. This class has no
    **__init__()** method
    """

    ret = []
    out = ""
    err = ""

    def execute(self, cmd):
        """Execute a system command and return output and error

        :param cmd: shell command to execute
        :type cmd: str, required
        :return: Output and Error from shell command
        :rtype: two str objects
        """

        self.ret = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        (self.out, self.err) = self.ret.communicate()
        self.out = self.out.decode("utf-8")
        self.err = self.err.decode("utf-8")
        return (self.out, self.err)

    def returnCode(self):
        """Returns the return code from shell command

        :rtype: int
        """

        return self.ret.returncode

    def get_output(self):
        """Returns the output from shell command

        :rtype: str
        """

        return self.out

    def get_error(self):
        """Returns the error from shell command

        :rtype: str
        """

        return self.err
