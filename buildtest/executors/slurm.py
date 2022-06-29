"""
This module implements the SlurmExecutor class responsible for submitting
jobs to Slurm Scheduler. This class is called in class BuildExecutor
when initializing the executors.
"""
import logging
import os
import re

from buildtest.defaults import console
from buildtest.exceptions import RuntimeFailure
from buildtest.executors.base import BaseExecutor
from buildtest.scheduler.slurm import SlurmJob

logger = logging.getLogger(__name__)


class SlurmExecutor(BaseExecutor):
    """The SlurmExecutor class is responsible for submitting jobs to Slurm Scheduler.
    The SlurmExecutor performs the following steps:

      - **load**: load slurm configuration from buildtest configuration file
      - **dispatch**: dispatch job to scheduler and acquire job ID
      - **poll**: wait for Slurm jobs to finish, if job is pending and exceeds `maxpendtime` then cancel job
      - **gather**: Once job is complete, gather job data
    """

    type = "slurm"

    def __init__(
        self, name, settings, site_configs, account=None, maxpendtime=None, timeout=None
    ):

        self.maxpendtime = maxpendtime
        self.account = account
        super().__init__(name, settings, site_configs, timeout=timeout)

        self.cluster = self._settings.get("cluster")
        self.partition = self._settings.get("partition")
        self.qos = self._settings.get("qos")

    def launcher_command(self, numprocs=None, numnodes=None):
        """Return sbatch launcher command with options used to submit job"""
        sbatch_cmd = ["sbatch", "--parsable"]

        if self.partition:
            sbatch_cmd += [f"-p {self.partition}"]

        if self.qos:
            sbatch_cmd += [f"-q {self.qos}"]

        if self.cluster:
            sbatch_cmd += [f"--clusters={self.cluster}"]

        if self.account:
            sbatch_cmd += [f"--account={self.account}"]

        if numprocs:
            sbatch_cmd += [f"-n {numprocs}"]

        if numnodes:
            sbatch_cmd += [f"-N {numnodes}"]

        if self.launcher_opts:
            sbatch_cmd += [" ".join(self.launcher_opts)]

        return sbatch_cmd

    def run(self, builder):
        """This method is responsible for dispatching job to slurm scheduler and extracting job
        id. If job id is valid we pass the job to :class:`buildtest.executors.slurm.SlurmJob` class and store object in ``builder.job``.

        Args:
            builder (buildtest.buildsystem.base.BuilderBase): An instance object of BuilderBase type
        """

        self.result = {}

        os.chdir(builder.stage_dir)
        self.logger.debug(f"Changing to directory {builder.stage_dir}")

        cmd = f"bash {self._bashopts} {os.path.basename(builder.build_script)}"

        timeout = self.timeout or self._buildtestsettings.target_config.get("timeout")

        try:
            command = builder.run(cmd, timeout)
        except RuntimeFailure as err:
            self.logger.error(err)
            return

        # it is possible user can specify a before_script for Slurm executor which is run in build script. In order to get
        # slurm job it would be the last element in array. If before_script is not specified the last element should be the only
        # element in output
        parse_jobid = command.get_output()[-1]
        # parse_jobid = " ".join(parse_jobid)

        # output of sbatch --parsable could be in format 'JobID;cluster' if so we split by colon to extract JobID
        if re.search(";", parse_jobid):
            builder.metadata["jobid"] = int(parse_jobid.split(";")[0])
        else:
            builder.metadata["jobid"] = int(parse_jobid)

        builder.job = SlurmJob(builder.metadata["jobid"], self.cluster)

        msg = f"[blue]{builder}[/blue]: JobID {builder.metadata['jobid']} dispatched to scheduler"
        console.print(msg)
        self.logger.debug(msg)

        return builder

    def poll(self, builder):
        """This method is called during poll stage where we invoke ``builder.job.poll()`` to get updated
        job state. If job is pending or suspended we stop timer and check if job needs to be cancelled if
        time exceeds ``maxpendtime`` value.

        Args:
            builder (buildtest.buildsystem.base.BuilderBase): An instance object of BuilderBase type
        """

        builder.job.poll()

        # if job is complete gather job data
        if builder.job.complete():
            self.gather(builder)
            return

        builder.stop()

        # if job state in PENDING check if we need to cancel job by checking internal timer
        if builder.job.is_pending() or builder.job.is_suspended():

            self.logger.debug(f"Time Duration: {builder.duration}")
            self.logger.debug(f"Max Pend Time: {self.maxpendtime}")

            # if timer exceeds 'maxpendtime' then cancel job
            if int(builder.timer.duration()) > self.maxpendtime:
                builder.job.cancel()
                builder.failed()
                console.print(
                    f"[blue]{builder}[/]: [red]Cancelling Job {builder.job.get()} because job exceeds max pend time of {self.maxpendtime} sec with current pend time of {builder.timer.duration()} sec[/red] "
                )
                return

        builder.start()

    def gather(self, builder):
        """Gather Slurm job data after job completion. In this step we call ``builder.job.gather()``,
        and update builder metadata such as returncode, output and error file.

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
            builder.job.workdir(), builder.name + ".out"
        )
        builder.metadata["errfile"] = os.path.join(
            builder.job.workdir(), builder.name + ".err"
        )

        console.print(f"[blue]{builder}[/]: Job {builder.job.get()} is complete! ")
        builder.post_run_steps()
