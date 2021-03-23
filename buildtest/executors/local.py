"""
This module implements the LocalExecutor class responsible for submitting
jobs to localhost. This class is called in class BuildExecutor
when initializing the executors.
"""

import datetime
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

    def run(self):
        """This method is responsible for running test for LocalExecutor which
        runs test locally. We keep track of metadata in ``self.builder.metadata``
        that keeps track of run result. The output and error file
        are written to filesystem.
        """

        if self.shell_type != self.builder.shell_type:
            sys.exit(
                f"[{self.builder.name}]: we have a shell mismatch with executor: {self.name}. The executor shell: {self.shell} is not compatible with shell: {self.builder.shell.name} found in buildspec"
            )

        # Change to the test directory
        os.chdir(self.builder.stage_dir)
        self.logger.debug(f"Changing to directory {self.builder.stage_dir}")

        cmd = [self.builder.metadata["testpath"]]

        self.builder.metadata["command"] = " ".join(cmd)
        self.logger.debug(
            f"Running Test via command: {self.builder.metadata['command']}"
        )

        command = BuildTestCommand(self.builder.metadata["command"])

        self.start_time()
        out, err = command.execute()
        self.end_time()
        self.runtime()

        self.logger.debug(
            f"Return code: {command.returncode} for test: {self.builder.metadata['testpath']}"
        )
        self.builder.metadata["result"]["returncode"] = command.returncode

        self.builder.metadata["output"] = out
        self.builder.metadata["error"] = err
        print(self.builder.metadata["result"])
        self.write_testresults(out, err)
        self.check_test_state()
