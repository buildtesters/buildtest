"""
This module implements the LocalExecutor class responsible for submitting
jobs to localhost. This class is called in class BuildExecutor
when initializing the executors.
"""

import os

from buildtest.executors.base import BaseExecutor
from buildtest.utils.file import write_file


class LocalExecutor(BaseExecutor):
    """The LocalExecutor class is responsible for running tests locally for
    bash, sh, csh and python shell. The LocalExecutor runs the tests and gathers
    the output and error results and writes to file.
    """

    type = "local"

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

        run_cmd = f"{self.shell} {os.path.basename(builder.build_script)}"

        # ---------- Start of Run ---------- #
        timeout = self.timeout or self._buildtestsettings.target_config.get("timeout")
        command = builder.run(run_cmd, timeout=timeout)
        builder.stop()
        builder.record_endtime()

        if command.returncode() != 0:
            builder.failed()

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
