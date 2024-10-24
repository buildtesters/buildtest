"""
This module implements the LSFExecutor class responsible for submitting
jobs to LSF Scheduler. This class is called in class BuildExecutor
when initializing the executors.
"""

import logging
import os
import re

from buildtest.defaults import console
from buildtest.executors.base import BaseExecutor
from buildtest.scheduler.lsf import LSFJob
from buildtest.utils.tools import check_binaries, deep_get

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
        super().__init__(
            name,
            settings,
            site_configs,
            timeout=timeout,
            account=account,
            maxpendtime=maxpendtime,
        )

        self.queue = self._settings.get("queue")
        self.custom_dirs = deep_get(site_configs.target_config, "paths", "lsf")

    def launcher_command(self, numprocs=None, numnodes=None):
        """This command returns the launcher command and any options specified in configuration file. This
        is useful when generating the build script in the BuilderBase class
        """
        self.lsf_cmds = check_binaries(
            ["bsub", "bjobs", "bkill"], custom_dirs=self.custom_dirs
        )
        cmd = [self.lsf_cmds["bsub"]]

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

        cmd = f"{self.shell} {os.path.basename(builder.build_script)}"

        self.timeout = self.timeout or self._buildtestsettings.target_config.get(
            "timeout"
        )
        command = builder.run(cmd, self.timeout)

        if command.returncode() != 0:
            builder.failed()
            return builder

        out = command.get_output()
        out = " ".join(out)
        pattern = r"(\d+)"
        # output in the form:  'Job <58654> is submitted to queue <batch>' and applying regular expression to get job ID
        regex_match = re.search(pattern, out)
        self.logger.debug(f"Applying regular expression '{pattern}' to output: '{out}'")

        # if there is no match we raise error
        if not regex_match:
            self.logger.debug(f"Unable to find LSF Job ID in output: '{out}'")
            builder.failed()
            return builder

        try:
            job_id = int(regex_match.group(0))
        except ValueError:
            self.logger.debug(
                f"Unable to convert '{regex_match.group(0)}' to int to extract Job ID"
            )
            builder.failed()
            return builder

        builder.job = LSFJob(job_id, self.lsf_cmds)

        builder.metadata["jobid"] = job_id

        msg = f"[blue]{builder}[/]: JobID: {builder.metadata['jobid']} dispatched to scheduler"
        self.logger.debug(msg)
        console.print(msg)

        return builder
