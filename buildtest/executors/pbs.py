"""This module implements PBSExecutor class that defines how executors submit
job to PBS Scheduler"""
import logging
import os

from buildtest.defaults import console
from buildtest.exceptions import RuntimeFailure
from buildtest.executors.base import BaseExecutor
from buildtest.scheduler.pbs import PBSJob
from buildtest.utils.tools import deep_get

logger = logging.getLogger(__name__)


class PBSExecutor(BaseExecutor):
    """The PBSExecutor class is responsible for submitting jobs to PBS Scheduler.
    The class implements the following methods:

    - load: load PBS executors from configuration file
    - dispatch: submit PBS job to scheduler
    - poll: poll PBS job via qstat and retrieve job state
    - gather: gather job result
    - cancel: cancel job if it exceeds max pending time
    """

    type = "pbs"
    launcher = "qsub"

    def __init__(self, name, settings, site_configs, account=None, maxpendtime=None):

        self.maxpendtime = maxpendtime
        self.account = account
        super().__init__(name, settings, site_configs)

    def load(self):
        """Load the a PBS executor configuration from buildtest settings."""

        """
        self.launcher = self._settings.get("launcher") or deep_get(
            self._buildtestsettings.target_config, "executors", "defaults", "launcher"
        )
        """
        self.launcher_opts = self._settings.get("options")

        self.queue = self._settings.get("queue")
        self.account = (
            self.account
            or self._settings.get("account")
            or deep_get(
                self._buildtestsettings.target_config,
                "executors",
                "defaults",
                "account",
            )
        )
        self.maxpendtime = (
            self.maxpendtime
            or self._settings.get("maxpendtime")
            or deep_get(
                self._buildtestsettings.target_config,
                "executors",
                "defaults",
                "maxpendtime",
            )
        )

    def launcher_command(self, numprocs=None, numnodes=None):
        batch_cmd = [self.launcher]

        if self.queue:
            batch_cmd += [f"-q {self.queue}"]

        if self.account:
            batch_cmd += [f"-P {self.account}"]

        if numprocs:
            batch_cmd += [f"-l ncpus={numprocs}"]

        if numnodes:
            batch_cmd += [f"-l nodes={numnodes}"]

        if self.launcher_opts:
            batch_cmd += [" ".join(self.launcher_opts)]

        return batch_cmd

    def run(self, builder):
        """This method is responsible for dispatching PBS job, get JobID
        and start record metadata in builder object. If job failed to submit
        we check returncode and exit with failure. After we submit job, we
        start timer and record when job was submitted and poll job once to get
        job details and store them in builder object.

        Args:
            builder (buildtest.buildsystem.base.BuilderBase): An instance object of BuilderBase type
        """

        self.load()

        os.chdir(builder.stage_dir)

        cmd = f"bash {self._bashopts} {os.path.basename(builder.build_script)}"
        try:
            command = builder.run(cmd)
        except RuntimeFailure as err:
            builder.failed()
            self.logger.error(err)
            return

        out = command.get_output()
        JobID = " ".join(out).strip()

        builder.metadata["jobid"] = JobID

        builder.job = PBSJob(JobID)

        # store job id
        builder.metadata["jobid"] = builder.job.get()

        msg = f"[blue]{builder}[/]: JobID: {builder.metadata['jobid']} dispatched to scheduler"
        console.print(msg)
        self.logger.debug(msg)

        return builder

    def poll(self, builder):
        """This method is responsible for polling PBS job which will update the job state. If job is complete we will
        gather job result. If job is pending we will stop timer and check if pend time exceeds max pend time for executor.
        If so we will cancel the job.

        Args:
            builder (buildtest.buildsystem.base.BuilderBase): An instance object of BuilderBase type
        """

        builder.job.poll()

        # if job is complete gather job data
        if builder.job.is_complete():
            self.gather(builder)
            return

        builder.stop()

        # if job in pending or suspended, check if it exceeds maxpendtime if so cancel job
        if builder.job.is_pending() or builder.job.is_suspended():
            self.logger.debug(f"Time Duration: {builder.timer.duration()}")
            self.logger.debug(f"Max Pend Time: {self.maxpendtime}")

            # if timer time is more than requested pend time then cancel job
            if int(builder.timer.duration()) > self.maxpendtime:
                builder.job.cancel()
                builder.failed()
                console.print(
                    f"[blue]{builder}[/]: [red]Cancelling Job {builder.job.get()} because job exceeds max pend time of {self.maxpendtime} sec with current pend time of {builder.timer.duration()} sec[/red] "
                )
                console.print(
                    f"{builder} in job state: {builder.job.state()} and {builder._state}"
                )
                return

        builder.start()

    def gather(self, builder):
        """This method is responsible for gather job results including output and error file and complete metadata
        for job which is stored in the builder object. We will retrieve job exitcode which corresponds to test
        returncode.

        Args:
            builder (buildtest.buildsystem.base.BuilderBase): An instance object of BuilderBase type
        """

        builder.record_endtime()
        builder.metadata["job"] = builder.job.gather()
        builder.metadata["result"]["returncode"] = builder.job.exitcode()

        builder.metadata["outfile"] = builder.job.output_file()
        builder.metadata["errfile"] = builder.job.error_file()

        console.print(f"[blue]{builder}[/]: Job {builder.job.get()} is complete! ")

        builder.post_run_steps()
