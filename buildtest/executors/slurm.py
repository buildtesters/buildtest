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
from buildtest.executors.job import Job
from buildtest.utils.command import BuildTestCommand
from buildtest.utils.tools import deep_get

logger = logging.getLogger(__name__)


class SlurmExecutor(BaseExecutor):
    """The SlurmExecutor class is responsible for submitting jobs to Slurm Scheduler.
    The SlurmExecutor performs the following steps:

      - **load**: load slurm configuration from buildtest configuration file
      - **dispatch**: dispatch job to scheduler and acquire job ID
      - **poll**: wait for Slurm jobs to finish, if job is pending and exceeds `max_pend_time` then cancel job
      - **gather**: Once job is complete, gather job data
    """

    type = "slurm"
    launcher = "sbatch"

    def __init__(self, name, settings, site_configs, account=None, max_pend_time=None):

        self.maxpendtime = max_pend_time
        self.account = account
        super().__init__(name, settings, site_configs)

    def load(self):
        """Load the a slurm executor configuration from buildtest settings."""
        """
        self.launcher = self._settings.get("launcher") or deep_get(
            self._buildtestsettings.target_config, "executors", "defaults", "launcher"
        )
        """
        self.launcher_opts = self._settings.get("options")

        self.cluster = self._settings.get("cluster")
        self.partition = self._settings.get("partition")
        self.qos = self._settings.get("qos")
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

        # the max_pend_time can be defined in executors 'default' section or a named instance or passed via command line.
        # The preference is the following:
        # 1. Command line: buildtest build --max-pend-time
        # 2. 'max_pend_time' in named executor instance
        # 3. 'max_pend_time' in 'default' executor instance
        self.max_pend_time = (
            self.maxpendtime
            or self._settings.get("max_pend_time")
            or deep_get(
                self._buildtestsettings.target_config,
                "executors",
                "defaults",
                "max_pend_time",
            )
        )

    def launcher_command(self, numprocs=None):
        """Return sbatch launcher command with options used to submit job"""
        sbatch_cmd = [self.launcher, "--parsable"]

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
        if self.launcher_opts:
            sbatch_cmd += [" ".join(self.launcher_opts)]

        return sbatch_cmd

    def dispatch(self, builder):
        """This method is responsible for dispatching job to slurm scheduler and extracting job
        id. If job id is valid we pass the job to :class:`buildtest.executors.slurm.SlurmJob` class and store object in ``builder.job``.

        Args:
            builder (buildtest.buildsystem.base.BuilderBase): An instance object of BuilderBase type
        """

        self.result = {}

        os.chdir(builder.stage_dir)
        self.logger.debug(f"Changing to directory {builder.stage_dir}")

        cmd = self.bash_launch_command() + [os.path.basename(builder.build_script)]
        cmd = " ".join(cmd)

        try:
            command = builder.run(cmd)
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
        time exceeds ``max_pend_time`` value.

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
            self.logger.debug(f"Max Pend Time: {self.max_pend_time}")

            # if timer exceeds 'max_pend_time' then cancel job
            if int(builder.timer.duration()) > self.max_pend_time:
                builder.job.cancel()
                builder.failure()
                console.print(
                    f"[blue]{builder}[/]: Cancelling Job: {builder.job.get()} because job exceeds max pend time: {self.max_pend_time} sec with current pend time of {builder.timer.duration()} "
                )

        builder.start()

    def gather(self, builder):
        """Gather Slurm job data after job completion. In this step we call ``builder.job.gather()``,
        and update builder metadata such as returncode, output and error file.

        Args:
            builder (buildtest.buildsystem.base.BuilderBase): An instance object of BuilderBase type
        """
        builder.endtime()

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


class SlurmJob(Job):
    """The SlurmJob class models a Slurm Job ID with helper methods to perform operation against an active slurm job. The SlurmJob class
    can poll job to get updated job state, gather job data upon completion of test and cancel job if necessary. We can also retrieve job
    state and determine if job is running, pending, suspended, or cancelled. Jobs are polled via `sacct <https://slurm.schedmd.com/sacct.html>`_
    command which can retrieve pending, running and complete jobs.
    """

    def __init__(self, jobID, cluster=None):
        super().__init__(jobID)
        self.cluster = cluster

    def is_pending(self):
        """If job is pending return ``True`` otherwise return ``False``. Slurm Job state for pending
        is ``PENDING``."""
        return self._state == "PENDING"

    def is_running(self):
        """If job is running return ``True`` otherwise return ``False``. Slurm will report ``RUNNING``
        for job state."""

        return self._state == "RUNNING"

    def is_suspended(self):
        """If job is suspended return ``True`` otherwise return ``False``. Slurm will report ``SUSPENDED``
        for job state."""

        return self._state == "SUSPENDED"

    def is_cancelled(self):
        """If job is cancelled return ``True`` otherwise return ``False``. Slurm will report ``CANCELLED``
        for job state."""

        return self._state == "CANCELLED"

    def is_complete(self):
        """If job is complete return ``True`` otherwise return ``False``. Slurm will report ``COMPLETED``
        for job state."""

        return self._state == "COMPLETED"

    def is_failed(self):
        """If job failed return ``True`` otherwise return ``False``. Slurm will report ``FAILED``
        for job state."""

        return self._state == "FAILED"

    def is_out_of_memory(self):
        """If job is out of memory return ``True`` otherwise return ``False``. Slurm will report ``OUT_OF_MEMORY``
        for job state."""

        return self._state == "OUT_OF_MEMORY"

    def is_timeout(self):
        """If job timed out return ``True`` otherwise return ``False``. Slurm will report ``TIMEOUT``
        for job state."""

        return self._state == "TIMEOUT"

    def complete(self):
        """This method is used for gathering job result we assume job is complete if it's
        in any of the following state: ``COMPLETED``, ``FAILED``, ``OUT_OF_MEMORY``, ``TIMEOUT``
        """

        return any(
            [
                self.is_complete(),
                self.is_failed(),
                self.is_out_of_memory(),
                self.is_timeout(),
            ]
        )

    def state(self):
        """Return job state"""

        return self._state

    def workdir(self):
        """Return job work directory"""

        return self._workdir

    def exitcode(self):
        """Return job exit code"""

        return self._exitcode

    def cancel(self):
        """Cancel job by running ``scancel <jobid>``. If job is specified to a slurm
        cluster we cancel job using ``scancel <jobid> --clusters=<cluster>``. This method
        is called if job exceeds `max_pend_time`."""

        query = f"scancel {self.jobid}"
        if self.cluster:
            query = f"scancel {self.jobid} --clusters={self.cluster}"

        cmd = BuildTestCommand(query)
        cmd.execute()
        logger.debug(f"Cancelling Job: {self.jobid} by running: {query}")

        self.poll()
        self._state = "CANCELLED"

    def poll(self):
        """This method will poll job via ``sacct`` command to get updated job state by running the
        following command: ``sacct -j <jobid> -o State -n -X -P``

        Slurm will report the job state that can be parsed. Shown below is an example job
        that is ``PENDING`` state

        .. code-block:: console

            $ sacct -j 46641229 -o State -n -X -P
            PENDING
        """

        query = f"sacct -j {self.jobid} -o State -n -X -P"
        if self.cluster:
            query += f" --clusters={self.cluster}"

        cmd = BuildTestCommand(query)
        cmd.execute()

        logger.debug(f"Querying JobID: '{self.jobid}'  Job State by running: '{query}'")
        job_state = cmd.get_output()
        self._state = "".join(job_state).rstrip()
        logger.debug(f"JobID: '{self.jobid}' job state:{self._state}")

    def gather(self):
        """Gather job record which is called after job completion. We use `sacct` to gather
        job record and return the job record as a dictionary. The command we run is
        ``sacct -j <jobid> -X -n -P -o <field1>,<field2>,...,<fieldN>``. We retrieve the following
        format fields from job record:

            - "Account"
            - "AllocNodes"
            - "AllocTRES"
            - "ConsumedEnergyRaw"
            - "CPUTimeRaw"
            - "Elapsed"
            - "End"
            - "ExitCode"
            - "JobID"
            - "JobName"
            - "NCPUS"
            - "NNodes"
            - "QOS"
            - "ReqMem"
            - "ReqNodes"
            - "Start"
            - "State"
            - "Submit"
            - "UID"
            - "User"
            - "WorkDir"

        The output of sacct is parseable using the pipe symbol (**|**) and stored into a dict

        .. code-block:: console

            $ sacct -j 42909266 -X -n -P -o Account,AllocNodes,AllocTRES,ConsumedEnergyRaw,CPUTimeRaw,Elapsed,End,ExitCode,JobID,JobName,NCPUS,NNodes,QOS,ReqMem,ReqNodes,Start,State,Submit,UID,User,WorkDir --clusters=cori
            nstaff|1|billing=272,cpu=272,energy=262,mem=87G,node=1|262|2176|00:00:08|2021-05-27T18:47:49|0:0|42909266|slurm_metadata|272|1|debug_knl|87Gn|1|2021-05-27T18:47:41|COMPLETED|2021-05-27T18:44:07|92503|siddiq90|/global/u1/s/siddiq90/.buildtest/tests/cori.slurm.knl_debug/metadata/slurm_metadata/0/stage

        We retrieve ExitCode and WorkDir via sacct command to get returncode. Slurm will write output and error file in WorkDir location. We
        run the following command below and parse the output. The ExitCode is in form ``<exitcode>:<signal>`` which is colon
        separated list. For more details on Slurm Exit code see https://slurm.schedmd.com/job_exit_code.html

        .. code-block:: console

            $ sacct -j 46294283 --clusters=cori -X -n -P -o ExitCode,Workdir
            0:0|/global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/hostname/hostname_knl/cd39a853/stage
        """

        sacct_fields = [
            "Account",
            "AllocNodes",
            "AllocTRES",
            "ConsumedEnergyRaw",
            "CPUTimeRaw",
            "Elapsed",
            "End",
            "ExitCode",
            "JobID",
            "JobName",
            "NCPUS",
            "NNodes",
            "QOS",
            "ReqMem",
            "ReqNodes",
            "Start",
            "State",
            "Submit",
            "UID",
            "User",
            "WorkDir",
        ]

        query = f"sacct -j {self.jobid} -X -n -P -o ExitCode,Workdir"
        if self.cluster:
            query += f" --clusters={self.cluster}"

        cmd = BuildTestCommand(query)
        cmd.execute()

        logger.debug(
            f"Querying JobID: '{self.jobid}' ExitCode and Workdir by running: '{query}'"
        )

        out = "".join(cmd.get_output()).rstrip()

        exitcode, workdir = out.split("|")
        # Exit Code field is in format <ExitCode>:<Signal> for now we care only about first number
        self._exitcode = int(exitcode.split(":")[0])
        self._workdir = workdir

        query = f"sacct -j {self.jobid} -X -n -P -o {','.join(sacct_fields)}"

        # to query jobs from another cluster we must add -M <cluster> to sacct
        if self.cluster:
            query += f" --clusters={self.cluster}"

        logger.debug(f"Gather slurm job data by running: {query}")
        cmd = BuildTestCommand(query)
        cmd.execute()
        out = "".join(cmd.get_output())
        # split by | since
        out = out.split("|")
        job_data = {}
        for field, value in zip(sacct_fields, out):
            job_data[field] = value

        return job_data
