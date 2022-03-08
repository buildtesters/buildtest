"""
This module implements the LocalExecutor class responsible for submitting
jobs to localhost. This class is called in class BuildExecutor
when initializing the executors.
"""

import os
import shlex

from buildtest.exceptions import RuntimeFailure
from buildtest.executors.base import BaseExecutor
from buildtest.utils.file import write_file
from buildtest.utils.shell import is_bash_shell, is_csh_shell, is_sh_shell, is_zsh_shell


class LocalExecutor(BaseExecutor):
    """The LocalExecutor class is responsible for running tests locally for
    bash, sh, csh and python shell. The LocalExecutor runs the tests and gathers
    the output and error results and writes to file.
    """

    type = "local"

    def load(self):

        self.shell = shlex.split(self._settings["shell"])[0]
        shell_options = shlex.split(self._settings["shell"])[1:]

        self.cmd = [self.shell]

        # default options for shell if no shell option specified
        if is_bash_shell(self.shell) and not shell_options:
            self.cmd.append(self._bashopts)

        elif is_sh_shell(self.shell) and not shell_options:
            self.cmd.append(self._shopts)

        elif is_csh_shell(self.shell) and not shell_options:
            self.cmd.append(self._cshopts)

        elif is_zsh_shell(self.shell) and not shell_options:
            self.cmd.append(self._zshopts)

        if shell_options:
            self.cmd.append(" ".join(shell_options))

    def run(self, builder):
        """This method is responsible for running test for LocalExecutor which
        runs test locally. We keep track of metadata in ``builder.metadata``
        that keeps track of run result. The output and error file
        are written to filesystem.

        Args:
            builder (buildtest.buildsystem.base.BuilderBase): An instance object of BuilderBase type
        """

        # Change to the test directory
        os.chdir(builder.stage_dir)
        self.logger.debug(f"Changing to directory {builder.stage_dir}")

        run_cmd = self.cmd + [os.path.basename(builder.build_script)]
        run_cmd = " ".join(run_cmd)

        # ---------- Start of Run ---------- #
        try:
            command = builder.run(run_cmd)
        except RuntimeFailure as err:
            builder.failed()
            self.logger.error(err)
            return

        builder.stop()
        builder.record_endtime()

        out = command.get_output()
        err = command.get_error()

        # ---------- End of Run ---------- #

        self.logger.debug(
            f"Return code: {command.returncode()} for test: {builder.metadata['testpath']}"
        )
        builder.metadata["result"]["returncode"] = command.returncode()

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
