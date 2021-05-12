"""
This module implements the LocalExecutor class responsible for submitting
jobs to localhost. This class is called in class BuildExecutor
when initializing the executors.
"""

import os
import shutil
import sys

from buildtest.executors.base import BaseExecutor
from buildtest.utils.file import write_file


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

        :param builder: builder object
        :type builder: BuilderBase, required
        """

        # we only run the check at time of running the test since that's when we need
        # the binary available
        self.check()

        if self.shell_type != builder.shell_type:
            sys.exit(
                f"[{builder.name}]: we have a shell mismatch with executor: {self.name}. The executor shell: {self.shell} is not compatible with shell: {builder.shell.name} found in buildspec"
            )

        # Change to the test directory
        os.chdir(builder.stage_dir)
        self.logger.debug(f"Changing to directory {builder.stage_dir}")

        self.logger.debug(f"Running Test via command: {builder.runcmd}")
        # command = BuildTestCommand(builder.runcmd)


        command = builder.run()
        out, err = command.execute()
        builder.endtime()

        self.logger.debug(
            f"Return code: {command.returncode} for test: {builder.metadata['testpath']}"
        )
        builder.metadata["result"]["returncode"] = command.returncode

        builder.metadata["output"] = "".join(out)
        builder.metadata["error"] = "".join(err)
        self.write_testresults(builder)
        self.check_test_state(builder)

    def write_testresults(self, builder):
        """This method writes test results into output and error file.

        :param builder: builder object
        :type builder: BuilderBase, required
        """

        # Keep an output file
        run_output_file = os.path.join(
            builder.metadata.get("testroot"),
            "run",
            builder.metadata.get("name"),
        )
        outfile = run_output_file + ".out"
        errfile = run_output_file + ".err"

        self.logger.debug(f"Writing test output to file: {outfile}")
        write_file(outfile, builder.metadata["output"])

        # write error from test to .err file
        self.logger.debug(f"Writing test error to file: {errfile}")
        write_file(errfile, builder.metadata["error"])

        builder.metadata["outfile"] = outfile
        builder.metadata["errfile"] = errfile
