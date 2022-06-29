"""
This module implements the LSFExecutor class responsible for submitting
jobs to LSF Scheduler. This class is called in class BuildExecutor
when initializing the executors.
"""
import logging
import os
import re

from buildtest.defaults import console
from buildtest.exceptions import RuntimeFailure
from buildtest.executors.base import BaseExecutor
from buildtest.scheduler.lsf import LSFJob

logger = logging.getLogger(__name__)


class LSFExecutor(BaseExecutor):
    """The LSFExecutor class is responsible for submitting jobs to LSF Scheduler.
    The LSFExecutor performs the following steps

    - **load**: load lsf configuration from buildtest configuration file
    - **dispatch**: dispatch job to scheduler and acquire job ID
    - **poll**: wait for LSF jobs to finish
    - **gather**: Once job is complete, gather job data
    """

    type = "lsf"

    def __init__(
        self, name, settings, site_configs, account=None, maxpendtime=None, timeout=None
    ):
        self.account = account
        self.maxpendtime = maxpendtime
        super().__init__(name, settings, site_configs, timeout=None)

        self.queue = self._settings.get("queue")

    def launcher_command(self, numprocs=None, numnodes=None):
        """This command returns the launcher command and any options specified in configuration file. This
        is useful when generating the build script in the BuilderBase class
        """
        cmd = ["bsub"]

        if self.queue:
            cmd += [f"-q {self.queue}"]

        if self.account:
            cmd += [f"-P {self.account}"]

        if numprocs:
            cmd += [f"-n {numprocs}"]

        if numnodes:
            cmd += [f"-nnodes {numnodes}"]

        if self.launcher_opts:
            cmd += [" ".join(self.launcher_opts)]

        return cmd

    def run(self, builder):
        """This method is responsible for dispatching job to scheduler and extracting job ID by applying a ``re.search`` against
        output at onset of job submission. If job id is not retrieved due to job failure or unable to match regular expression we
        mark job incomplete by invoking :func:`buildtest.buildsystem.base.BuilderBase.incomplete`` method and return from method.

        If we have a valid job ID we invoke :class:`buildtest.executors.lsf.LSFJob` class given the job id to poll job and store this
        into ``builder.job`` attribute.

        Args:
            builder (buildtest.buildsystem.base.BuilderBase): An instance object of BuilderBase type
        """

        os.chdir(builder.stage_dir)
        self.logger.debug(f"Changing to stage directory {builder.stage_dir}")

        cmd = f"bash {self._bashopts} {os.path.basename(builder.build_script)}"

        timeout = self.timeout or self._buildtestsettings.target_config.get("timeout")

        try:
            command = builder.run(cmd, timeout)
        except RuntimeFailure as err:
            self.logger.error(err)
            return

        out = command.get_output()
        out = " ".join(out)
        pattern = r"(\d+)"
        # output in the form:  'Job <58654> is submitted to queue <batch>' and applying regular expression to get job ID
        m = re.search(pattern, out)
        self.logger.debug(f"Applying regular expression '{pattern}' to output: '{out}'")

        # if there is no match we raise error
        if not m:
            self.logger.debug(f"Unable to find LSF Job ID in output: '{out}'")
            builder.failed()
            return

        try:
            job_id = int(m.group(0))
        except ValueError:
            self.logger.debug(
                f"Unable to convert '{m.group(0)}' to int to extract Job ID"
            )
            builder.failed()
            return

        builder.job = LSFJob(job_id)

        builder.metadata["jobid"] = job_id

        msg = f"[blue]{builder}[/]: JobID: {builder.metadata['jobid']} dispatched to scheduler"
        self.logger.debug(msg)
        console.print(msg)

        return builder

    def poll(self, builder):
        """Given a builder object we poll the job by invoking builder method ``builder.job.poll()`` return state of job. If
        job is suspended or pending we stop timer and check if timer exceeds maxpendtime value which could be defined in configuration
        file or passed via command line ``--max-pend-time``

        Args:
            builder (buildtest.buildsystem.base.BuilderBase): An instance object of BuilderBase type
        """

        builder.job.poll()

        # if job is complete gather job data
        if builder.job.is_complete():
            self.gather(builder)
            return

        builder.stop()
        if builder.job.is_suspended() or builder.job.is_pending():

            self.logger.debug(f"Time Duration: {builder.duration}")
            self.logger.debug(f"Max Pend Time: {self.maxpendtime}")

            # if timer time is more than requested pend time then cancel job
            if int(builder.timer.duration()) > self.maxpendtime:
                builder.job.cancel()
                builder.failed()
                console.print(
                    f"[blue]{builder}[/]: [red]Cancelling Job {builder.job.get()} because job exceeds max pend time of {self.maxpendtime} sec with current pend time of {builder.timer.duration()} sec[/red] "
                )
                return

        builder.start()

    def gather(self, builder):
        """Gather Job detail after completion of job by invoking the builder method ``builder.job.gather()``.
        We retrieve exit code, output file, error file and update builder metadata.

        Args:
            builder (buildtest.buildsystem.base.BuilderBase): An instance object of BuilderBase type
        """

        builder.record_endtime()

        builder.metadata["job"] = builder.job.gather()
        builder.metadata["result"]["returncode"] = builder.job.exitcode()

        self.logger.debug(
            f"[{builder.name}] returncode: {builder.metadata['result']['returncode']}"
        )

        builder.metadata["outfile"] = os.path.join(
            builder.stage_dir, builder.job.output_file()
        )
        builder.metadata["errfile"] = os.path.join(
            builder.stage_dir, builder.job.error_file()
        )
        console.print(f"[blue]{builder}[/]: Job {builder.job.get()} is complete! ")
        builder.post_run_steps()
