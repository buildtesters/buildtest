"""
This module implements the SlurmExecutor class responsible for submitting
jobs to Slurm Scheduler. This class is called in class BuildExecutor
when initializing the executors.
"""
import logging
import os
import re
import shutil

from buildtest.executors.base import BaseExecutor
from buildtest.executors.job import Job
from buildtest.utils.command import BuildTestCommand
from buildtest.utils.file import read_file
from buildtest.utils.tools import deep_get

logger = logging.getLogger(__name__)


class SlurmExecutor(BaseExecutor):
    """The SlurmExecutor class is responsible for submitting jobs to Slurm Scheduler.
    The SlurmExecutor performs the following steps

    load: load slurm configuration from buildtest configuration file
    dispatch: dispatch job to scheduler and acquire job ID
    poll: wait for Slurm jobs to finish
    gather: Once job is complete, gather job data
    cancel: Cancel job if it exceeds max pending time
    """

    type = "slurm"

    def __init__(self, name, settings, site_configs, max_pend_time=None):

        self.maxpendtime = max_pend_time
        super().__init__(name, settings, site_configs)

    def load(self):
        """Load the a slurm executor configuration from buildtest settings."""

        self.launcher = self._settings.get("launcher") or deep_get(
            self._buildtestsettings.target_config, "executors", "defaults", "launcher"
        )
        self.launcher_opts = self._settings.get("options")

        self.cluster = self._settings.get("cluster")
        self.partition = self._settings.get("partition")
        self.qos = self._settings.get("qos")
        self.account = self._settings.get("account") or deep_get(
            self._buildtestsettings.target_config, "executors", "defaults", "account"
        )
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

    def launcher_command(self):
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

        if self.launcher_opts:
            sbatch_cmd += [" ".join(self.launcher_opts)]

        return sbatch_cmd

    def dispatch(self, builder):
        """This method is responsible for dispatching job to slurm scheduler.

        :param builder: builder object
        :type builder: BuilderBase, required
        """

        self.result = {}

        os.chdir(builder.stage_dir)
        self.logger.debug(f"Changing to directory {builder.stage_dir}")

        command = builder.run()

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

        msg = f"[{builder.metadata['name']}] JobID: {builder.metadata['jobid']} dispatched to scheduler"
        print(msg)
        self.logger.debug(msg)

    def poll(self, builder):
        """This method will poll for job each interval specified by time interval
        until job finishes. We use `sacct` to poll for job id and sleep for given
        time interval until trying again. The command to be run is
        ``sacct -j <jobid> -o State -n -X -P``

        :param builder: builder object
        :type builder: BuilderBase, required
        """

        builder.job.poll()

        # if job state in PENDING check if we need to cancel job by checking internal timer
        if builder.job.is_pending() or builder.job.is_suspended():
            builder.stop()
            self.logger.debug(f"Time Duration: {builder.duration}")
            self.logger.debug(f"Max Pend Time: {self.max_pend_time}")

            # if timer time is more than requested pend time then cancel job
            if int(builder.duration) > self.max_pend_time:
                builder.job.cancel()
                print(
                    "Cancelling Job because duration time: {:f} sec exceeds max pend time: {} sec".format(
                        builder.duration, self.max_pend_time
                    )
                )

            builder.start()

    def gather(self, builder):
        """Gather Slurm job data after job completion

        :param builder: instance of BuilderBase
        :type builder: BuilderBase (subclass), required
        """
        builder.endtime()

        builder.metadata["job"] = builder.job.gather()

        builder.metadata["result"]["returncode"] = builder.job.exitcode()

        builder.metadata["outfile"] = os.path.join(
            builder.job.workdir(), builder.metadata["name"] + ".out"
        )
        builder.metadata["errfile"] = os.path.join(
            builder.job.workdir(), builder.metadata["name"] + ".err"
        )

        shutil.copy2(
            builder.metadata["outfile"],
            os.path.join(
                builder.run_dir, os.path.basename(builder.metadata["outfile"])
            ),
        )
        shutil.copy2(
            builder.metadata["errfile"],
            os.path.join(
                builder.run_dir, os.path.basename(builder.metadata["errfile"])
            ),
        )
        self.logger.debug(
            f"[{builder.name}] returncode: {builder.metadata['result']['returncode']}"
        )

        builder.metadata["output"] = read_file(self.builder.metadata["outfile"])
        builder.metadata["error"] = read_file(self.builder.metadata["errfile"])

        self.check_test_state(builder)


class SlurmJob(Job):
    def __init__(self, jobID, cluster=None):
        super().__init__(jobID)
        self.cluster = cluster

    def is_pending(self):
        return self._state == "PENDING"

    def is_running(self):
        return self._state == "RUNNING"

    def is_suspended(self):
        return self._state == "SUSPENDED"

    def is_cancelled(self):
        return self._state == "CANCELLED"

    def is_complete(self):
        return self._state == "COMPLETED"

    def is_failed(self):
        return self._state == "FAILED"

    def is_out_of_memory(self):
        return self._state == "OUT_OF_MEMORY"

    def is_timeout(self):
        return self._state == "TIMEOUT"

    def complete(self):
        """This method is used for gathering job result we assume job is complete if it's
        in any of the following state: COMPLETED, FAILED, OUT_OF_MEMORY, TIMEOUT
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
        return self._state

    def workdir(self):
        return self._workdir

    def exitcode(self):
        return self._exitcode

    def cancel(self):
        query = f"scancel {self.jobid}"
        if self.cluster:
            query = f"scancel {self.jobid} --clusters={self.cluster}"

        cmd = BuildTestCommand(query)
        cmd.execute()
        logger.debug(f"Cancelling Job: {self.jobid} by running: {query}")

        self.poll()
        self._state = "CANCELLED"

    def poll(self):

        query = f"sacct -j {self.jobid} -o State -n -X -P"
        if self.cluster:
            query += f" --clusters={self.cluster}"

        cmd = BuildTestCommand(query)
        cmd.execute()

        job_state = cmd.get_output()
        self._state = "".join(job_state).rstrip()

        query = f"sacct -j {self.jobid} -X -n -P -o ExitCode,Workdir"
        if self.cluster:
            query += f" --clusters={self.cluster}"

        cmd = BuildTestCommand(query)
        cmd.execute()
        out = "".join(cmd.get_output()).rstrip()

        exitcode, workdir = out.split("|")
        # Exit Code field is in format <ExitCode>:<Signal> for now we care only about first number
        self._exitcode = int(exitcode.split(":")[0])
        self._workdir = workdir

    def gather(self):

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
            "ReqGRES",
            "ReqMem",
            "ReqNodes",
            "ReqTRES",
            "Start",
            "State",
            "Submit",
            "UID",
            "User",
            "WorkDir",
        ]
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
