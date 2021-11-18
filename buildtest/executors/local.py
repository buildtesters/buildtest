"""
This module implements the LocalExecutor class responsible for submitting
jobs to localhost. This class is called in class BuildExecutor
when initializing the executors.
"""

import os
import shlex
import shutil
import sys

from buildtest.defaults import console
from buildtest.exceptions import RuntimeFailure
from buildtest.executors.base import BaseExecutor
from buildtest.utils.file import write_file


class LocalExecutor(BaseExecutor):
    """The LocalExecutor class is responsible for running tests locally for
    bash, sh, csh and python shell. The LocalExecutor runs the tests and gathers
    the output and error results and writes to file.
    """

    type = "local"

    def load(self):

        # shell_settings = shlex.split(self._settings["shell"])

        self.shell = shlex.split(self._settings["shell"])[0]
        self.shell_opts = shlex.split(self._settings["shell"])[1:]

        if self.shell.endswith("python") or self.shell.endswith("python3"):
            self.shell = "bash"

        # default shell option for bash is 'bash --norc --noprofile -eo pipefail' if no options are specified
        if self.shell == "bash" and not self.shell_opts:
            self.shell_opts = ["--norc", "--noprofile", "-eo pipefail"]

        if self.shell == "sh" and not self.shell_opts:
            self.shell_opts = ["--norc", "--noprofile", "-eo pipefail"]

        if self.shell == "csh" and not self.shell_opts:
            self.shell_opts = ["-e"]

        # self.shell_opts = ' '.join(shell_settings[1:])

    def run(self, builder):
        """This method is responsible for running test for LocalExecutor which
        runs test locally. We keep track of metadata in ``builder.metadata``
        that keeps track of run result. The output and error file
        are written to filesystem.

        Args:
            builder (buildtest.buildsystem.base.BuilderBase): An instance object of BuilderBase type
        """

        # we only run the check at time of running the test since that's when we need
        # the binary available
        # self.check()

        # Change to the test directory
        os.chdir(builder.stage_dir)
        self.logger.debug(f"Changing to directory {builder.stage_dir}")

        run_cmd = (
            [self.shell] + self.shell_opts + [os.path.basename(builder.build_script)]
        )
        run_cmd = " ".join(run_cmd)

        # ---------- Start of Run ---------- #
        try:
            command = builder.run(run_cmd)
        except RuntimeFailure as err:
            builder.failure()
            self.logger.error(err)
            return

        builder.stop()
        builder.endtime()

        out = command.get_output()
        err = command.get_error()

        # ---------- End of Run ---------- #

        # self.logger.debug(f"Running Test via command: {builder.runcmd}")

        self.logger.debug(
            f"Return code: {command.returncode()} for test: {builder.metadata['testpath']}"
        )
        builder.metadata["result"]["returncode"] = command.returncode()
        console.print(
            f"[blue]{builder}[/]: Test completed with returncode: {command.returncode()}"
        )

        out = "".join(out)
        err = "".join(err)

        # --------- write output and error file ------------- #

        outfile = os.path.join(builder.stage_dir, builder.name) + ".out"
        errfile = os.path.join(builder.stage_dir, builder.name) + ".err"

        self.logger.debug(f"Writing test output to file: {outfile}")
        write_file(outfile, out)

        # write error from test to .err file
        self.logger.debug(f"Writing test error to file: {errfile}")
        write_file(errfile, err)

        builder.metadata["outfile"] = outfile
        builder.metadata["errfile"] = errfile

        builder.post_run_steps()

        return builder
