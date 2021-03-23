"""
This module implements the LSFExecutor class responsible for submitting
jobs to LSF Scheduler. This class is called in class BuildExecutor
when initializing the executors.
"""

import datetime
import json
import os
import subprocess
import sys
import time
from buildtest.executors.base import BaseExecutor
from buildtest.utils.command import BuildTestCommand
from buildtest.utils.file import read_file
from buildtest.utils.tools import deep_get


class LSFExecutor(BaseExecutor):
    """The LSFExecutor class is responsible for submitting jobs to LSF Scheduler.
    The LSFExecutor performs the following steps

    load: load lsf configuration from buildtest configuration file
    dispatch: dispatch job to scheduler and acquire job ID
    poll: wait for LSF jobs to finish
    gather: Once job is complete, gather job data
    cancel: Cancel job if it exceeds max pending time
    """

    type = "lsf"

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

    def load(self):
        """Load the a LSF executor configuration from buildtest settings."""

        self.launcher = self._settings.get("launcher") or deep_get(
            self._buildtestsettings.target_config, "executors", "defaults", "launcher"
        )
        self.launcher_opts = self._settings.get("options")
        self.account = self._settings.get("account") or deep_get(
            self._buildtestsettings.target_config, "executors", "defaults", "account"
        )
        self.max_pend_time = self._settings.get("max_pend_time") or deep_get(
            self._buildtestsettings.target_config,
            "executors",
            "defaults",
            "max_pend_time",
        )
        self.queue = self._settings.get("queue")

    def dispatch(self):
        """This method is responsible for dispatching job to scheduler."""

        # The job_id variable is used to store the JobID retrieved by bjobs
        self.job_id = 0

        os.chdir(self.builder.stage_dir)
        self.logger.debug(f"Changing to stage directory {self.builder.stage_dir}")

        bsub_cmd = [self.launcher]

        if self.queue:
            bsub_cmd += [f"-q {self.queue}"]

        if self.account:
            bsub_cmd += [f"-P {self.account}"]

        if self.launcher_opts:
            bsub_cmd += [" ".join(self.launcher_opts)]

        bsub_cmd.append(self.builder.metadata["testpath"])

        self.builder.metadata["command"] = " ".join(bsub_cmd)
        self.logger.debug(
            f"Running Test via command: {self.builder.metadata['command']}"
        )

        command = BuildTestCommand(self.builder.metadata["command"])
        command.execute()
        self.builder.start()
        self.builder.metadata["result"]["starttime"] = datetime.datetime.now()

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

        # wait a few seconds before querying for jobID. It can take a few seconds
        # between job submission and running bjobs to get output.
        time.sleep(interval)

        # get last jobid from bjobs
        cmd = "bjobs -u $USER -o 'JobID' -noheader | tail -n 1"

        # get last job ID
        self.logger.debug(f"[Acquire Job ID]: {cmd}")
        output = subprocess.check_output(cmd, shell=True, universal_newlines=True)
        self.job_id = int(output.strip())

        self.builder.metadata["jobid"] = self.job_id

        msg = f"[{self.builder.metadata['name']}] JobID: {self.builder.metadata['jobid']} dispatched to scheduler"
        self.logger.debug(msg)
        print(msg)

    def poll(self):
        """This method will poll for job by using bjobs and return state of job.
        The command to be run is ``bjobs -noheader -o 'stat' <JOBID>`` which
        returns job state.
        """

        self.logger.debug(f"Query Job: {self.builder.metadata['jobid']}")

        query = f"{self.poll_cmd} -noheader -o 'stat' {self.builder.metadata['jobid']}"

        self.logger.debug(query)
        cmd = BuildTestCommand(query)
        cmd.execute()
        job_state = cmd.get_output()
        self.builder.job_state = "".join(job_state).rstrip()
        self.logger.debug(
            "[%s]: JobID %s in %s state ",
            self.builder.metadata["name"],
            self.builder.metadata["jobid"],
            self.builder.job_state,
        )

        # if job state in PEND check if we need to cancel job by checking internal timer
        if self.builder.job_state == "PEND":
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

            self.builder.start()

    def gather(self):
        """Gather Job detail after completion of job. This method will retrieve output
        fields defined for ``self.format_fields``. buildtest will run
        ``bjobs -o '<field1> ... <fieldN>' <JOBID> -json``.
        """

        # bjobs gather command to extract format fields and convert output to JSON
        gather_cmd = f"{self.poll_cmd} -o '{' '.join(self.format_fields)}' {self.builder.metadata['jobid']} -json"

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
            self.builder.metadata["result"]["returncode"] = 0
        else:
            self.builder.metadata["result"]["returncode"] = int(job_data["EXIT_CODE"])

        self.builder.metadata["result"]["endtime"] = datetime.datetime.now()
        runtime = self.builder.metadata["result"]["endtime"] - self.builder.metadata["result"]["starttime"]
        self.builder.metadata["result"]["runtime"] = runtime.total_seconds()

        self.builder.metadata["result"]["starttime"] = self.builder.metadata["result"]["starttime"].strftime("%Y/%m/%d %X")
        self.builder.metadata["result"]["endtime"] = self.builder.metadata["result"]["endtime"].strftime("%Y/%m/%d %X")

        self.builder.metadata["outfile"] = os.path.join(
            self.builder.stage_dir, job_data["OUTPUT_FILE"]
        )
        self.builder.metadata["errfile"] = os.path.join(
            self.builder.stage_dir, job_data["ERROR_FILE"]
        )

        self.builder.metadata["output"] = read_file(self.builder.metadata["outfile"])
        self.builder.metadata["error"] = read_file(self.builder.metadata["errfile"])

        self.logger.debug(
            f"[{self.builder.name}] returncode: {self.builder.metadata['result']['returncode']}"
        )
        self.check_test_state()

    def cancel(self):
        """Cancel LSF job, this is required if job exceeds max pending time in queue"""

        query = f"bkill {self.builder.metadata['jobid']}"

        cmd = BuildTestCommand(query)
        cmd.execute()
        msg = (
            f"Cancelling Job: {self.builder.metadata['name']} running command: {query}"
        )
        print(msg)
        self.logger.debug(msg)
