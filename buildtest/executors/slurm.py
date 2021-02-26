"""
This module implements the SlurmExecutor class responsible for submitting
jobs to Slurm Scheduler. This class is called in class BuildExecutor
when initializing the executors.
"""

import os
import re
import shutil

from buildtest.exceptions import BuildTestError
from buildtest.executors.base import BaseExecutor
from buildtest.utils.command import BuildTestCommand
from buildtest.utils.file import read_file


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

    def load(self):
        """Load the a slurm executor configuration from buildtest settings."""

        self.launcher = self._settings.get("launcher") or self._buildtestsettings[
            "executors"
        ].get("defaults", {}).get("launcher")
        self.launcher_opts = self._settings.get("options")

        self.cluster = self._settings.get("cluster")
        self.partition = self._settings.get("partition")
        self.qos = self._settings.get("qos")
        self.account = self._settings.get("account") or self._buildtestsettings[
            "executors"
        ].get("defaults", {}).get("account")
        self.max_pend_time = self._settings.get(
            "max_pend_time"
        ) or self._buildtestsettings["executors"].get("defaults", {}).get(
            "max_pend_time"
        )

    def dispatch(self):
        """This method is responsible for dispatching job to slurm scheduler."""

        self.result = {}

        os.chdir(self.builder.stage_dir)
        self.logger.debug(f"Changing to directory {self.builder.stage_dir}")

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

        sbatch_cmd.append(self.builder.metadata["testpath"])

        self.builder.metadata["command"] = " ".join(sbatch_cmd)
        self.logger.debug(
            f"Running Test via command: {self.builder.metadata['command']}"
        )

        command = BuildTestCommand(self.builder.metadata["command"])
        command.execute()
        self.builder.start()

        # if sbatch job submission returns non-zero exit that means we have failure, exit immediately
        if command.returncode != 0:
            err = f"[{self.builder.metadata['name']}] failed to submit job with returncode: {command.returncode} \n"
            err += f"[{self.builder.metadata['name']}] running command: {' '.join(sbatch_cmd)}"
            raise BuildtestError(err)

        parse_jobid = command.get_output()
        parse_jobid = " ".join(parse_jobid)

        # output of sbatch --parsable could be in format 'JobID;cluster' if so we split by colon to extract JobID
        if re.search(";", parse_jobid):
            self.builder.metadata["jobid"] = int(parse_jobid.split(";")[0])
        else:
            self.builder.metadata["jobid"] = int(parse_jobid)

        msg = f"[{self.builder.metadata['name']}] JobID: {self.builder.metadata['jobid']} dispatched to scheduler"
        print(msg)
        self.logger.debug(msg)

    def poll(self):
        """This method will poll for job each interval specified by time interval
        until job finishes. We use `sacct` to poll for job id and sleep for given
        time interval until trying again. The command to be run is
        ``sacct -j <jobid> -o State -n -X -P``
        """

        self.logger.debug(f"Query Job: {self.builder.metadata['jobid']}")

        slurm_query = (
            f"{self.poll_cmd} -j {self.builder.metadata['jobid']} -o State -n -X -P"
        )

        # to query jobs from another cluster we must add -M <cluster> to sacct
        if self.cluster:
            slurm_query += f" --clusters={self.cluster}"

        self.logger.debug(slurm_query)
        cmd = BuildTestCommand(slurm_query)
        cmd.execute()

        job_state = cmd.get_output()
        self.builder.job_state = "".join(job_state).rstrip()

        self.logger.debug(
            "[%s]: JobID %s in %s state ",
            self.builder.metadata["name"],
            self.builder.metadata["jobid"],
            self.builder.job_state,
        )

        # if job state in PENDING check if we need to cancel job by checking internal timer
        if self.builder.job_state == "PENDING":
            self.builder.stop()
            self.logger.debug(f"Time Duration: {self.builder.duration}")
            self.logger.debug(f"Max Pend Time: {self.max_pend_time}")

            # if timer time is more than requested pend time then cancel job
            if int(self.builder.duration) > self.max_pend_time:
                self.cancel()
                self.builder.job_state = "CANCELLED"
                print(
                    "Cancelling Job because duration time: {:f} sec exceeds max pend time: {} sec".format(
                        self.builder.duration, self.max_pend_time
                    )
                )

                # return self.builder.job_state

            self.builder.start()

        # return self.builder.job_state

    def gather(self):
        """Gather Slurm detail after job completion"""

        gather_cmd = f"{self.poll_cmd} -j {self.builder.metadata['jobid']} -X -n -P -o {','.join(self.sacct_fields)}"

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

        self.logger.debug(f"[{self.builder.name}] Job Results:")
        for field, value in zip(self.sacct_fields, out):
            job_data[field] = value
            self.logger.debug(f"field: {field}   value: {value}")

        self.builder.metadata["job"] = job_data

        # Exit Code field is in format <ExitCode>:<Signal> for now we care only
        # about first number
        self.builder.metadata["result"]["returncode"] = int(
            job_data["ExitCode"].split(":")[0]
        )

        self.builder.metadata["result"]["starttime"] = job_data["Start"]
        self.builder.metadata["result"]["endtime"] = job_data["End"]
        self.builder.metadata["result"]["runtime"] = job_data["Elapsed"]

        if self.builder.job_state == "CANCELLED":
            return

        self.builder.metadata["outfile"] = os.path.join(
            job_data["WorkDir"].rstrip(),
            f"{self.builder.metadata['name']}.out",
        )
        self.builder.metadata["errfile"] = os.path.join(
            job_data["WorkDir"].rstrip(),
            f"{self.builder.metadata['name']}.err",
        )

        shutil.copy2(
            self.builder.metadata["outfile"],
            os.path.join(
                self.builder.run_dir, os.path.basename(self.builder.metadata["outfile"])
            ),
        )
        shutil.copy2(
            self.builder.metadata["errfile"],
            os.path.join(
                self.builder.run_dir, os.path.basename(self.builder.metadata["errfile"])
            ),
        )
        self.logger.debug(
            f"[{self.builder.name}] returncode: {self.builder.metadata['result']['returncode']}"
        )

        slurm_cmd = f"scontrol show job {self.builder.metadata['jobid']}"
        if self.cluster:
            slurm_cmd += f" --clusters={self.cluster}"

        cmd = BuildTestCommand(slurm_cmd)
        cmd.execute()
        self.builder.metadata["job"]["scontrol"] = {}
        self.builder.metadata["job"]["scontrol"]["command"] = slurm_cmd
        self.builder.metadata["job"]["scontrol"]["output"] = "".join(cmd.get_output())
        self.builder.metadata["output"] = read_file(self.builder.metadata["outfile"])
        self.builder.metadata["error"] = read_file(self.builder.metadata["errfile"])

        self.logger.debug(f"Executing slurm command: {slurm_cmd}")
        self.check_test_state()

    def cancel(self):
        """Cancel slurm job, this operation is performed if job exceeds pending or runtime."""

        query = f"scancel {self.builder.metadata['jobid']}"
        # cancel by slurm cluster if required to cancel job from remote slurm cluster
        if self.cluster:
            query += f" --clusters={self.cluster}"

        cmd = BuildTestCommand(query)
        cmd.execute()
        msg = (
            f"Cancelling Job: {self.builder.metadata['name']} running command: {query}"
        )
        print(msg)
        self.logger.debug(msg)
