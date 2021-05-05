"""
This module implements the SlurmExecutor class responsible for submitting
jobs to Slurm Scheduler. This class is called in class BuildExecutor
when initializing the executors.
"""
import logging
import os
import re
import shutil

from buildtest.exceptions import ExecutorError
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

    poll_cmd = "sacct"
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

    def dispatch(self, builder):
        """This method is responsible for dispatching job to slurm scheduler.

        :param builder: builder object
        :type builder: BuilderBase, required
        """

        self.result = {}

        os.chdir(builder.stage_dir)
        self.logger.debug(f"Changing to directory {builder.stage_dir}")

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

        sbatch_cmd.append(builder.metadata["testpath"])

        builder.metadata["command"] = " ".join(sbatch_cmd)
        self.logger.debug(f"Running Test via command: {builder.metadata['command']}")

        command = BuildTestCommand(builder.metadata["command"])
        command.execute()

        # if sbatch job submission returns non-zero exit that means we have failure, exit immediately
        if command.returncode != 0:
            err = f"[{builder.metadata['name']}] failed to submit job with returncode: {command.returncode} \n"
            err += (
                f"[{builder.metadata['name']}] running command: {' '.join(sbatch_cmd)}"
            )
            raise ExecutorError(err)

        # record starttime of job
        self.start_time(builder)
        builder.start()

        parse_jobid = command.get_output()
        parse_jobid = " ".join(parse_jobid)

        # output of sbatch --parsable could be in format 'JobID;cluster' if so we split by colon to extract JobID
        if re.search(";", parse_jobid):
            builder.metadata["jobid"] = int(parse_jobid.split(";")[0])
        else:
            builder.metadata["jobid"] = int(parse_jobid)

        builder.job = SlurmJob(self.metata["jobid"], self.cluster)

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

        """
        self.logger.debug(f"Query Job: {builder.metadata['jobid']}")

        slurm_query = (
            f"{self.poll_cmd} -j {builder.metadata['jobid']} -o State -n -X -P"
        )

        # to query jobs from another cluster we must add -M <cluster> to sacct
        if self.cluster:
            slurm_query += f" --clusters={self.cluster}"

        self.logger.debug(slurm_query)
        cmd = BuildTestCommand(slurm_query)
        cmd.execute()

        job_state = cmd.get_output()
        builder.job_state = "".join(job_state).rstrip()

        self.logger.debug(
            "[%s]: JobID %s in %s state ",
            builder.metadata["name"],
            builder.metadata["jobid"],
            builder.job_state,
        )

        
        # if job state in PENDING check if we need to cancel job by checking internal timer
        if builder.job_state == "PENDING":
            builder.stop()
            self.logger.debug(f"Time Duration: {builder.duration}")
            self.logger.debug(f"Max Pend Time: {self.max_pend_time}")

            # if timer time is more than requested pend time then cancel job
            if int(builder.duration) > self.max_pend_time:
                self.cancel(builder)
                builder.job_state = "CANCELLED"
                print(
                    "Cancelling Job because duration time: {:f} sec exceeds max pend time: {} sec".format(
                        builder.duration, self.max_pend_time
                    )
                )

            builder.start()
        """

    def gather(self, builder):
        """Gather Slurm job data after job completion

        :param builder: instance of BuilderBase
        :type builder: BuilderBase (subclass), required
        """

        builder.metadata["job"] = builder.job.gather()
        """
        gather_cmd = f"{self.poll_cmd} -j {builder.metadata['jobid']} -X -n -P -o {','.join(self.sacct_fields)}"

        # to query jobs from another cluster we must add -M <cluster> to sacct
        if self.cluster:
            gather_cmd += f" --clusters={self.cluster}"

        self.logger.debug(f"Gather slurm job data by running: {gather_cmd}")
        cmd = BuildTestCommand(gather_cmd)
        cmd.execute()
        out = "".join(cmd.get_output())
        # split by | since
        out = out.split("|")
        job_data = {}

        self.logger.debug(f"[{builder.name}] Job Results:")
        for field, value in zip(self.sacct_fields, out):
            job_data[field] = value
            self.logger.debug(f"field: {field}   value: {value}")

        builder.metadata["job"] = job_data
        """

        builder.metadata["result"]["returncode"] = builder.job.exitcode()

        """
        # Exit Code field is in format <ExitCode>:<Signal> for now we care only
        # about first number
        builder.metadata["result"]["returncode"] = int(
            job_data["ExitCode"].split(":")[0]
        )
        """

        self.end_time(builder)

        builder.metadata["outfile"] = os.path.join(
            builder.job.workdir(), builder.metadata["name"] + ".out"
        )
        builder.metadata["errfile"] = os.path.join(
            builder.job.workdir(), builder.metadata["name"] + ".err"
        )

        builder.job.workdir()

        """
        builder.metadata["outfile"] = os.path.join(
            job_data["WorkDir"].rstrip(),
            f"{builder.metadata['name']}.out",
        )
        builder.metadata["errfile"] = os.path.join(
            job_data["WorkDir"].rstrip(),
            f"{builder.metadata['name']}.err",
        )
        """
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

    def cancel(self, builder):
        """Cancel slurm job, this operation is performed if job exceeds pending or runtime.

        :param builder: Instance of BuilderBase
        :type builder: BuilderBase (subclass), required
        """

        query = f"scancel {builder.metadata['jobid']}"
        # cancel by slurm cluster if required to cancel job from remote slurm cluster
        if self.cluster:
            query += f" --clusters={self.cluster}"

        cmd = BuildTestCommand(query)
        cmd.execute()
        msg = f"Cancelling Job: {builder.metadata['name']} running command: {query}"
        print(msg)
        self.logger.debug(msg)


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

    def cancel(self):
        query = f"scancel {self.jobid}"
        if self.cluster:
            query = f"scancel {self.jobid} --clusters={self.cluster}"

        cmd = BuildTestCommand(query)
        cmd.execute()
        logger.debug(f"Cancelling Job: {self.jobid} by running: {query}")

        self.poll()
        # output in form CANCELLED by <uid>
        if re.match("^(CANCELLED)", self.state):
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
        self._exitcode = exitcode.split(":")[0]
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

        self.logger.debug(f"Gather slurm job data by running: {query}")
        cmd = BuildTestCommand(gather_cmd)
        cmd.execute()
        out = "".join(cmd.get_output())
        # split by | since
        out = out.split("|")
        job_data = {}

        logger.debug(f"[{builder.name}] Job Results:")
        for field, value in zip(self.sacct_fields, out):
            job_data[field] = value

        return job_data

    def state(self):
        return self._state

    def workdir(self):
        return self._workdir

    def exitcode(self):
        return self._exitcode
