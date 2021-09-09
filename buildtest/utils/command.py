# import locale
import os
import shlex
import shutil
import subprocess
import tempfile

from buildtest.utils.file import read_file


class Capturing:
    """capture output from stdout and stderr into capture object.
    This is based off of github.com/vsoch/gridtest but modified
    to write files. The stderr and stdout are set to temporary files at
    the init of the capture, and then they are closed when we exit. This
    means expected usage looks like:

    .. code-block:: python

        with Capturing() as capture:
            process = subprocess.Popen(...)


    And then the output and error are retrieved from reading the files:
    and exposed as properties to the client: capture.out, capture.err

    And cleanup means deleting these files, if they exist.
    """

    def __enter__(self):
        self.set_stdout()
        self.set_stderr()
        return self

    def set_stdout(self):
        self.stdout = open(tempfile.mkstemp()[1], "w")

    def set_stderr(self):
        self.stderr = open(tempfile.mkstemp()[1], "w")

    def __exit__(self, *args):
        self.stderr.close()
        self.stdout.close()

    @property
    def out(self):
        """Return content of output stream if file exists otherwise returns empty string"""
        if os.path.exists(self.stdout.name):
            return read_file(self.stdout.name)
        return ""

    @property
    def err(self):
        """Return content of error stream if file exists otherwise returns empty string."""
        if os.path.exists(self.stderr.name):
            return read_file(self.stderr.name)
        return ""

    def cleanup(self):
        """This method will remove stdout and stderr file upon reading both streams"""
        for filename in [self.stdout.name, self.stderr.name]:
            if os.path.exists(filename):
                os.remove(filename)


class BuildTestCommand:
    """Class method to invoke shell commands and retrieve output and error.
    This class is inspired and derived from utils functions in
    https://github.com/vsoch/scif
    """

    def __init__(self, cmd=None):
        """The initializer method will initialize class variables and check input argument `cmd` and make sure
        command is in a list format.

        Args:
            cmd (str, optional): Input shell command
        """
        cmd = cmd or []
        self._returncode = None
        self.out = []
        self.err = []

        # If a list isn't provided, split it
        if cmd:
            self.set_command(cmd)

    def set_command(self, cmd):
        """parse is called when a new command is provided to ensure we have
        a list. We don't check that the executable is on the path,
        as the initialization might not occur in the runtime environment.
        """
        if not isinstance(cmd, list):
            cmd = shlex.split(cmd)
        self.cmd = cmd

    def execute(self):
        """Execute a system command and return output and error."""
        # Reset the output and error records
        self.out = []
        self.err = []

        # The executable must be found, return code 1 if not
        executable = shutil.which(self.cmd[0])
        if not executable:
            self.err = ["%s not found." % self.cmd[0]]
            self._returncode = 1
            return (self.out, self.err)

        # remove the original executable
        args = self.cmd[1:]

        # Use updated command with executable and remainder (list)
        cmd = [executable] + args

        # Capturing provides temporary output and error files
        with Capturing() as capture:
            process = subprocess.Popen(
                cmd,
                stdout=capture.stdout,
                stderr=capture.stderr,
                universal_newlines=True,
            )
            returncode = process.poll()

            # Iterate through the output
            while returncode is None:
                returncode = process.poll()

        # Get the remainder of lines, add return code. The self.decode avoids UTF-8 decode error
        self.out += ["%s\n" % x for x in self.decode(capture.out).split("\n") if x]
        self.err += ["%s\n" % x for x in self.decode(capture.err).split("\n") if x]

        # self.out += ["%s\n" % x for x in capture.out.split("\n") if x]
        # self.err += ["%s\n" % x for x in capture.err.split("\n") if x]
        # Cleanup capture files and save final return code
        capture.cleanup()
        self._returncode = returncode

        return (self.out, self.err)

    def returncode(self):
        """Returns the return code from shell command

        Returns:
            int: returncode of shell command
        """

        return self._returncode

    def decode(self, line):
        """Given a line of output (error or regular) decode using the
        system default, if appropriate
        """

        # loc = locale.getdefaultlocale()[1]

        try:
            line = line.decode("utf-8")
        except Exception:
            pass
        return line

    def get_output(self):
        """Returns the output content from shell command"""
        return self.out

    def get_error(self):
        """Returns the error content from shell command"""

        return self.err

    def get_command(self):
        """Returns the executed command"""

        return " ".join(self.cmd)
