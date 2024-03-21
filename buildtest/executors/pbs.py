"""This module implements PBSExecutor class that defines how executors submit
job to PBS Scheduler"""

import logging
import os

from buildtest.defaults import console
from buildtest.executors.base import BaseExecutor
from buildtest.scheduler.pbs import PBSJob

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

    def __init__(
        self, name, settings, site_configs, account=None, maxpendtime=None, timeout=None
    ):
        super().__init__(
            name,
            settings,
            site_configs,
            timeout=timeout,
            account=account,
            maxpendtime=maxpendtime,
        )

        self.queue = self._settings.get("queue")

    def launcher_command(self, numprocs=None, numnodes=None):
        batch_cmd = ["qsub"]

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

        os.chdir(builder.stage_dir)

        cmd = f"{self.shell} {os.path.basename(builder.build_script)}"

        self.timeout = self.timeout or self._buildtestsettings.target_config.get(
            "timeout"
        )

        command = builder.run(cmd, timeout=self.timeout)

        if command.returncode() != 0:
            builder.failed()
            return builder

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


class TorqueExecutor(PBSExecutor):
    """This class is a sub-class of PBSExecutor class and is responsible for Torque Executor"""
