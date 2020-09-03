"""
This module implements the SlurmExecutor class responsible for submitting
jobs to Slurm Scheduler. This class is called in class BuildExecutor
when initializing the executors.
"""

import os
import shutil
import sys
import re
from buildtest.executors.base import BaseExecutor
from buildtest.utils.command import BuildTestCommand


class SlurmExecutor(BaseExecutor):
    """The SlurmExecutor class is responsible for submitting jobs to Slurm Scheduler.
       The SlurmExecutor performs the following steps

       check: check if slurm partition is available for accepting jobs.
       load: load slurm configuration from buildtest configuration file
       dispatch: dispatch job to scheduler and acquire job ID
       poll: wait for Slurm jobs to finish
       gather: Once job is complete, gather job data
    """

    type = "slurm"
    steps = ["dispatch", "poll", "gather", "close"]
    job_state = None
    poll_cmd = "sacct"
    sacct_fields = [
        "Account",
        "AllocNodes",
        "AllocTRES",
        "ConsumedEnergyRaw",
        "CPUTimeRaw",
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

    def check(self):
        """Check slurm binary is available before running tests. This will check
           the launcher (sbatch) and sacct are available. If qos, partition, and
           cluster key defined we check if its a valid entity in slurm configuration.
           For partition, we also check if its in the ``up`` state before dispatching
           jobs. This method will raise an exception of type SystemExit if any
           checks fail.
        """

        if not shutil.which(self.launcher):
            sys.exit(
                f"[{self.builder.metadata['name']}]: Cannot find launcher program: {self.launcher}"
            )

        if not shutil.which(self.poll_cmd):
            sys.exit(
                f"[{self.builder.metadata['name']}]: Cannot find slurm poll command: {self.poll_cmd}"
            )

    def load(self):
        """Load the a slurm executor configuration from buildtest settings."""

        self.launcher = self._settings.get("launcher") or self._buildtestsettings[
            "executors"
        ].get("defaults", {}).get("launcher")
        self.launcher_opts = self._settings.get("options")

        self.cluster = self._settings.get("cluster")
        self.partition = self._settings.get("partition")
        self.qos = self._settings.get("qos")

    def dispatch(self):
        """This method is responsible for dispatching job to slurm scheduler."""

        self.check()
        self.result = {}
        # The job_id variable is used to store the JobID retrieved by sacct
        self.job_id = 0
        self.result["id"] = self.builder.metadata.get("id")

        os.chdir(self.builder.metadata["testroot"])
        self.logger.debug(f"Changing to directory {self.builder.metadata['testroot']}")

        sbatch_cmd = [self.launcher, "--parsable"]

        if self.partition:
            sbatch_cmd += [f"-p {self.partition}"]

        if self.qos:
            sbatch_cmd += [f"-q {self.qos}"]

        if self.cluster:
            sbatch_cmd += [f"-M {self.cluster}"]

        if self.launcher_opts:
            sbatch_cmd += [" ".join(self.launcher_opts)]

        sbatch_cmd.append(self.builder.metadata["testpath"])

        self.builder.metadata["command"] = " ".join(sbatch_cmd)
        self.logger.debug(
            f"Running Test via command: {self.builder.metadata['command']}"
        )

        command = BuildTestCommand(self.builder.metadata["command"])
        command.execute()

        # if sbatch job submission returns non-zero exit that means we have failure, exit immediately
        if command.returncode != 0:
            err = f"[{self.builder.metadata['name']}] failed to submit job with returncode: {command.returncode} \n"
            err += f"[{self.builder.metadata['name']}] running command: {' '.join(sbatch_cmd)}"
            sys.exit(err)

        parse_jobid = command.get_output()
        parse_jobid = " ".join(parse_jobid)

        # output of sbatch --parsable could be in format 'JobID;cluster' if so we split by colon to extract JobID
        if re.search(";", parse_jobid):
            self.job_id = int(parse_jobid.split(";")[0])
        else:
            self.job_id = int(parse_jobid)

        self.builder.metadata["jobid"] = self.job_id

        msg = f"[{self.builder.metadata['name']}] JobID: {self.builder.metadata['jobid']} dispatched to scheduler"
        print(msg)
        self.logger.debug(msg)

        self.result["state"] = "N/A"
        self.result["runtime"] = "0"
        self.result["returncode"] = "0"

    def poll(self):
        """ This method will poll for job each interval specified by time interval
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
            slurm_query += f" -M {self.cluster}"

        self.logger.debug(slurm_query)
        cmd = BuildTestCommand(slurm_query)
        cmd.execute()
        self.job_state = cmd.get_output()
        self.job_state = "".join(self.job_state).rstrip()

        msg = f"[{self.builder.metadata['name']}]: JobID {self.builder.metadata['jobid']} in {self.job_state} state "
        print(msg)
        self.logger.debug(msg)
        return self.job_state

    def gather(self):
        """Gather Slurm detail after job completion"""

        gather_cmd = f"{self.poll_cmd} -j {self.builder.metadata['jobid']} -X -n -P -o {','.join(self.sacct_fields)}"

        # to query jobs from another cluster we must add -M <cluster> to sacct
        if self.cluster:
            gather_cmd += f" -M {self.cluster}"

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
        self.result["returncode"] = int(job_data["ExitCode"].split(":")[0])

        self.result["starttime"] = job_data["Start"]
        self.result["endtime"] = job_data["End"]

        self.builder.metadata["outfile"] = os.path.join(
            job_data["WorkDir"].rstrip(),
            f"{job_data['JobName']}-{job_data['JobID']}.out",
        )
        self.builder.metadata["errfile"] = os.path.join(
            job_data["WorkDir"].rstrip(),
            f"{job_data['JobName']}-{job_data['JobID']}.err",
        )
        self.logger.debug(f"[{self.builder.name}] result: {self.result}")
        self.logger.debug(
            f"[{self.builder.name}] returncode: {self.result['returncode']}"
        )
        self.check_test_state()
        self.builder.metadata["result"] = self.result
