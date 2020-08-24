"""
This module implements the LSFExecutor class responsible for submitting
jobs to LSF Scheduler. This class is called in class BuildExecutor
when initializing the executors.
"""

import json
import os
import shutil
import subprocess
import sys
import time
from buildtest.executors.base import BaseExecutor
from buildtest.utils.command import BuildTestCommand


class LSFExecutor(BaseExecutor):
    """The LSFExecutor class is responsible for submitting jobs to LSF Scheduler.
       The LSFExecutor performs the following steps

       check: check if lsf queue is available for accepting jobs.
       load: load lsf configuration from buildtest configuration file
       dispatch: dispatch job to scheduler and acquire job ID
       poll: wait for LSF jobs to finish
       gather: Once job is complete, gather job data
    """

    type = "lsf"
    steps = ["check", "dispatch", "poll", "gather", "close"]
    job_state = None
    poll_cmd = "bjobs"
    # format fields we retrieve in gather step
    format_fields = [
        "job_name",
        "stat",
        "user",
        "user_group",
        "queue",
        "proj_name",
        "pids",
        "exit_code",
        "from_host",
        "exec_host",
        "submit_time",
        "start_time",
        "finish_time",
        "nthreads",
        "exec_home",
        "exec_cwd",
        "output_file",
        "error_file",
    ]

    def check(self):
        """Checking binary for lsf launcher and poll command. If not found we raise error"""
        if not shutil.which(self.launcher):
            sys.exit(
                f"[{self.builder.metadata['name']}]: Cannot find launcher program: {self.launcher}"
            )

        if not shutil.which(self.poll_cmd):
            sys.exit(
                f"[{self.builder.metadata['name']}]: Cannot find poll command: {self.poll_cmd}"
            )

    def load(self):
        """Load the a LSF executor configuration from buildtest settings."""

        self.launcher = self._settings.get("launcher") or self._buildtestsettings[
            "executors"
        ].get("defaults", {}).get("launcher")
        self.launcher_opts = self._settings.get("options")

        self.queue = self._settings.get("queue")

    def dispatch(self):
        """This method is responsible for dispatching job to slurm scheduler."""

        self.check()

        self.result["BUILD_ID"] = self.builder.metadata.get("build_id")

        os.chdir(self.builder.metadata["testroot"])
        self.logger.debug(f"Changing to directory {self.builder.metadata['testroot']}")

        bsub_cmd = [self.launcher]

        if self.queue:
            bsub_cmd += [f"-q {self.queue}"]

        if self.launcher_opts:
            bsub_cmd += [" ".join(self.launcher_opts)]

        bsub_cmd.append(self.builder.metadata["testpath"])

        self.builder.metadata["command"] = " ".join(bsub_cmd)
        self.logger.debug(
            f"Running Test via command: {self.builder.metadata['command']}"
        )

        command = BuildTestCommand(self.builder.metadata["command"])
        command.execute()

        # if job submission returns non-zero exit that means we have failure, exit immediately
        if command.returncode != 0:
            err = f"[{self.builder.metadata['name']}] failed to submit job with returncode: {command.returncode} \n"
            err += f"[{self.builder.metadata['name']}] running command: {bsub_cmd}"
            sys.exit(err)

        interval = 5

        print(f"[{self.builder.metadata['name']}] job dispatched to scheduler")
        print(
            f"[{self.builder.metadata['name']}] acquiring job id in {interval} seconds"
        )

        # wait 10 seconds before querying slurm for jobID. It can take some time for output
        # of job to show up from time of submission and running squeue.
        time.sleep(interval)

        cmd = ["bjobs"]

        cmd += ["-u $USER -o 'JobID' -noheader | tail -n 1"]
        cmd = " ".join(cmd)

        # get last job ID
        self.logger.debug(f"[Acquire Job ID]: {cmd}")
        output = subprocess.check_output(cmd, shell=True, universal_newlines=True)
        self.job_id = int(output.strip())
        self.logger.debug(
            f"[{self.builder.metadata['name']}] JobID: {self.job_id} dispatched to scheduler"
        )
        self.result["state"] = "N/A"
        self.result["runtime"] = "0"
        self.result["returncode"] = "0"
        # self.write_testresults(out, err)

    def poll(self):
        """ This method will poll for job by using bjobs and return state of job.
            The command to be run is ``bjobs -noheader -o 'stat' <JOBID>``
             which returns job state.
        """

        self.logger.debug(f"Query Job: {self.job_id}")

        query = f"{self.poll_cmd} -noheader -o 'stat' {self.job_id}"

        self.logger.debug(query)
        cmd = BuildTestCommand(query)
        cmd.execute()
        self.job_state = cmd.get_output()
        self.job_state = "".join(self.job_state).rstrip()
        msg = f"[{self.builder.metadata['name']}]: JobID {self.job_id} in {self.job_state} state "
        print(msg)
        self.logger.debug(msg)
        return self.job_state

    def gather(self):
        """Gather Job detail after completion of job. This method will retrieve output
           fields defined for ``self.format_fields``. buildtest will run
           ``bjobs -o '<field1> ... <fieldN>' <JOBID> -json``.
        """
        # command
        gather_cmd = (
            f"{self.poll_cmd} -o '{' '.join(self.format_fields)}' {self.job_id} -json"
        )

        self.logger.debug(f"Gather LSF job data by running: {gather_cmd}")
        cmd = BuildTestCommand(gather_cmd)
        cmd.execute()
        out = cmd.get_output()
        out = "".join(out).rstrip()

        out = json.loads(out)

        job_data = {}

        self.logger.debug(f"[{self.builder.name}] Job Results:")
        records = out["RECORDS"][0]
        for field, value in records.items():
            job_data[field] = value
            self.logger.debug(f"field: {field}   value: {value}")

        self.builder.metadata["job"] = job_data

        # Exit Code field is in format <ExitCode>:<Signal> for now we care only
        # about first number
        if job_data["EXIT_CODE"] == "":
            self.result["returncode"] = 0
        else:
            self.result["returncode"] = int(job_data["EXIT_CODE"])

        self.result["starttime"] = job_data["START_TIME"]
        self.result["endtime"] = job_data["FINISH_TIME"]
        self.builder.metadata["outfile"] = job_data["OUTPUT_FILE"]
        self.builder.metadata["errfile"] = job_data["ERROR_FILE"]

        self.logger.debug(f"[{self.builder.name}] result: {self.result}")
        self.logger.debug(
            f"[{self.builder.name}] returncode: {self.result['returncode']}"
        )
        self.check_test_state()
