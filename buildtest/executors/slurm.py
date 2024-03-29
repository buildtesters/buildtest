"""
This module implements the SlurmExecutor class responsible for submitting
jobs to Slurm Scheduler. This class is called in class BuildExecutor
when initializing the executors.
"""

import logging
import os
import re

from buildtest.defaults import console
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
        super().__init__(
            name,
            settings,
            site_configs,
            timeout=timeout,
            account=account,
            maxpendtime=maxpendtime,
        )

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

        os.chdir(builder.stage_dir)
        self.logger.debug(f"Changing to directory {builder.stage_dir}")

        cmd = f"{self.shell} {os.path.basename(builder.build_script)}"

        self.timeout = self.timeout or self._buildtestsettings.target_config.get(
            "timeout"
        )
        command = builder.run(cmd, self.timeout)

        if command.returncode() != 0:
            builder.failed()
            return builder

        # it is possible user can specify a before_script for Slurm executor which is run in build script. In order to get
        # slurm job it would be the last element in array. If before_script is not specified the last element should be the only
        # element in output
        parse_jobid = command.get_output()[-1]

        # output of sbatch --parsable could be in format 'JobID;cluster' if so we split by colon to extract JobID
        if re.search(";", parse_jobid):
            builder.metadata["jobid"] = int(parse_jobid.split(";")[0])
        else:
            builder.metadata["jobid"] = int(parse_jobid)

        builder.job = SlurmJob(builder.metadata["jobid"], self.cluster)

        msg = f"[blue]{builder}[/blue]: JobID {builder.metadata['jobid']} dispatched to scheduler"
        console.print(msg)

        builder.job.get_output_and_error_files()
        self.logger.debug(msg)

        return builder

    def gather(self, builder):
        """Gather Slurm job data after job completion. In this step we call ``builder.job.gather()``,
        and update builder metadata such as returncode, output and error file.

        Args:
            builder (buildtest.buildsystem.base.BuilderBase): An instance object of BuilderBase type
        """
        builder.record_endtime()

        builder.metadata["job"] = builder.job.jobdata()

        builder.metadata["result"]["returncode"] = builder.job.exitcode()

        self.logger.debug(
            f"[{builder.name}] returncode: {builder.metadata['result']['returncode']}"
        )

        builder.metadata["outfile"] = builder.job.output_file()
        builder.metadata["errfile"] = builder.job.error_file()

        console.print(f"[blue]{builder}[/]: Job {builder.job.get()} is complete! ")
        builder.post_run_steps()
