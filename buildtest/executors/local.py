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
from buildtest.utils.timer import Timer


class LocalExecutor(BaseExecutor):
    type = "local"

    def load(self):
        self.shell = self._settings.get("shell")

        self.check()

    def check(self):

        if not shutil.which(self.shell):
            sys.exit(f"Unable to find shell: {self.shell}")

    def run(self):
        """This method is responsible for running test for LocalExecutor which
           runs test locally. We keep track of metadata in ``self.builder.metadata``
           and self.result keeps track of run result. The output and error file
           is written to filesystem. After test
        """
        # Keep a result object
        # self.result = {}

        # check shell type mismatch between buildspec shell and executor shell. We can't support python with sh/bash.
        if (
            self.builder.shell.name in ["sh", "bash", "/bin/bash", "/bin/sh"]
            and self.shell == "python"
        ) or (
            self.builder.shell.name == "python"
            and self.shell in ["sh", "bash", "/bin/bash", "/bin/sh"]
        ):
            sys.exit(
                f"[{self.name}]: shell mismatch, expecting {self.shell} while buildspec shell is {self.builder.shell.name}"
            )

        self.result["LOGFILE"] = self.builder.metadata.get("logfile", "")
        self.result["BUILD_ID"] = self.builder.metadata.get("build_id")

        # Change to the test directory
        os.chdir(self.builder.metadata["testroot"])
        self.logger.debug(f"Changing to directory {self.builder.metadata['testroot']}")

        # build the run command that includes the shell path, shell options and path to test file
        cmd = [
            self.builder.shell.path,
            self.builder.shell.opts,
            self.builder.metadata["testpath"],
        ]
        self.builder.metadata["command"] = " ".join(cmd)
        self.logger.debug(
            f"Running Test via command: {self.builder.metadata['command']}"
        )

        command = BuildTestCommand(self.builder.metadata["command"])
        self.builder.metadata["starttime"] = datetime.datetime.now()
        self.result["starttime"] = self.get_formatted_time("starttime")

        t = Timer()
        t.start()
        out, err = command.execute()
        self.result["runtime"] = t.stop()

        self.builder.metadata["endtime"] = datetime.datetime.now()
        self.result["endtime"] = self.get_formatted_time("endtime")

        self.write_testresults(out, err)

        self.logger.debug(
            f"Return code: {command.returncode} for test: {self.builder.metadata['testpath']}"
        )
        self.result["returncode"] = command.returncode

        self.write_testresults(out, err)
        self.check_test_state()
