"""
This module implements the LocalExecutor class responsible for submitting
jobs to localhost. This class is called in class BuildExecutor
when initializing the executors.
"""

import os
import shutil
import sys

from buildtest.executors.base import BaseExecutor
from buildtest.utils.command import BuildTestCommand


class LocalExecutor(BaseExecutor):
    """The LocalExecutor class is responsible for running tests locally for
    bash, sh and python shell. The LocalExecutor runs the tests and gathers
    the output and error results and writes to file. This class implements
    ``load``, ``check`` and ``run`` method.
    """

    type = "local"

    def load(self):
        self.shell = self._settings.get("shell")
        self.shell = self.shell.split()[0]
        self.check()

    def check(self):
        """Check if shell binary is available"""
        if not shutil.which(self.shell):
            sys.exit(f"Unable to find shell: {self.shell}")

        if self.shell in ["sh", "bash", "zsh", "/bin/sh", "/bin/bash", "/bin/zsh"]:
            self.shell_type = "bash"
        elif self.shell in ["csh", "tcsh", "/bin/csh", "/bin/tcsh"]:
            self.shell_type = "csh"
        elif self.shell in ["python"]:
            self.shell_type = "python"

    def run(self, builder):
        """This method is responsible for running test for LocalExecutor which
        runs test locally. We keep track of metadata in ``builder.metadata``
        that keeps track of run result. The output and error file
        are written to filesystem.
        """

        if self.shell_type != builder.shell_type:
            sys.exit(
                f"[{builder.name}]: we have a shell mismatch with executor: {self.name}. The executor shell: {self.shell} is not compatible with shell: {builder.shell.name} found in buildspec"
            )

        # Change to the test directory
        os.chdir(builder.stage_dir)
        self.logger.debug(f"Changing to directory {builder.stage_dir}")

        cmd = [builder.metadata["testpath"]]

        builder.metadata["command"] = " ".join(cmd)
        self.logger.debug(f"Running Test via command: {builder.metadata['command']}")

        command = BuildTestCommand(builder.metadata["command"])

        self.start_time(builder)
        out, err = command.execute()
        self.end_time(builder)

        self.logger.debug(
            f"Return code: {command.returncode} for test: {builder.metadata['testpath']}"
        )
        builder.metadata["result"]["returncode"] = command.returncode

        builder.metadata["output"] = out
        builder.metadata["error"] = err
        self.write_testresults(out, err)
        self.check_test_state()
