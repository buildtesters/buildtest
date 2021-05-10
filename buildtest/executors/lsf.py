"""
This module implements the LSFExecutor class responsible for submitting
jobs to LSF Scheduler. This class is called in class BuildExecutor
when initializing the executors.
"""

import logging
import json
import os
import subprocess
import time
from buildtest.executors.base import BaseExecutor
from buildtest.executors.job import Job
from buildtest.exceptions import ExecutorError
from buildtest.utils.command import BuildTestCommand
from buildtest.utils.file import read_file
from buildtest.utils.tools import deep_get

logger = logging.getLogger(__name__)


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

    def __init__(self, name, settings, site_configs, max_pend_time=None):

        self.maxpendtime = max_pend_time
        super().__init__(name, settings, site_configs)

    def load(self):
        """Load the a LSF executor configuration from buildtest settings."""

        self.launcher = self._settings.get("launcher") or deep_get(
            self._buildtestsettings.target_config, "executors", "defaults", "launcher"
        )
        self.launcher_opts = self._settings.get("options")
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
        self.queue = self._settings.get("queue")

    def dispatch(self, builder):
        """This method is responsible for dispatching job to scheduler.

        :param builder: builder object
        :type builder: BuilderBase, required
        """

        os.chdir(builder.stage_dir)
        self.logger.debug(f"Changing to stage directory {builder.stage_dir}")

        bsub_cmd = [self.launcher]

        if self.queue:
            bsub_cmd += [f"-q {self.queue}"]

        if self.account:
            bsub_cmd += [f"-P {self.account}"]

        if self.launcher_opts:
            bsub_cmd += [" ".join(self.launcher_opts)]

        bsub_cmd.append(builder.metadata["testpath"])

        builder.metadata["command"] = " ".join(bsub_cmd)
        self.logger.debug(f"Running Test via command: {builder.metadata['command']}")

        command = BuildTestCommand(builder.metadata["command"])
        command.execute()
        self.start_time(builder)
        builder.start()
        # if job submission returns non-zero exit that means we have failure, exit immediately
        if command.returncode != 0:
            err = f"[{builder.metadata['name']}] failed to submit job with returncode: {command.returncode} \n"
            err += f"[{builder.metadata['name']}] running command: {bsub_cmd}"
            raise ExecutorError(err)

        interval = 5

        # wait a few seconds before querying for jobID. It can take a few seconds
        # between job submission and running bjobs to get output.
        time.sleep(interval)

        # get last jobid from bjobs
        cmd = "bjobs -u $USER -o 'JobID' -noheader | tail -n 1"

        # get last job ID
        self.logger.debug(f"[Acquire Job ID]: {cmd}")
        output = subprocess.check_output(cmd, shell=True, universal_newlines=True)
        job_id = int(output.strip())

        builder.job = LSFJob(job_id)

        builder.metadata["jobid"] = job_id

        msg = f"[{builder.metadata['name']}] JobID: {builder.metadata['jobid']} dispatched to scheduler"
        self.logger.debug(msg)
        print(msg)

    def poll(self, builder):
        """This method will poll for job by using bjobs and return state of job.
        The command to be run is ``bjobs -noheader -o 'stat' <JOBID>`` which
        returns job state.

        :param builder: builder object
        :type builder: BuilderBase, required
        """

        builder.job.poll()

        if builder.job.is_suspended() or builder.job.is_pending():
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
        """Gather Job detail after completion of job. This method will retrieve output
        fields defined for ``self.format_fields``. buildtest will run
        ``bjobs -o '<field1> ... <fieldN>' <JOBID> -json``.

        :param builder: builder object
        :type builder: BuilderBase, required
        """

        # bjobs gather command to extract format fields and convert output to JSON
        gather_cmd = f"{self.poll_cmd} -o '{' '.join(self.format_fields)}' {builder.metadata['jobid']} -json"

        self.logger.debug(f"Gather LSF job data by running: {gather_cmd}")
        cmd = BuildTestCommand(gather_cmd)
        cmd.execute()
        out = cmd.get_output()
        out = "".join(out).rstrip()

        out = json.loads(out)

        job_data = {}

        self.logger.debug(f"[{builder.name}] Job Results:")
        records = out["RECORDS"][0]
        for field, value in records.items():
            job_data[field] = value
            self.logger.debug(f"field: {field}   value: {value}")

        builder.metadata["job"] = job_data

        # Exit Code field is in format <ExitCode>:<Signal> for now we care only
        # about first number
        if job_data["EXIT_CODE"] == "":
            builder.metadata["result"]["returncode"] = 0
        else:
            builder.metadata["result"]["returncode"] = int(job_data["EXIT_CODE"])

        self.end_time(builder)

        builder.metadata["outfile"] = os.path.join(
            builder.stage_dir, job_data["OUTPUT_FILE"]
        )
        builder.metadata["errfile"] = os.path.join(
            builder.stage_dir, job_data["ERROR_FILE"]
        )

        builder.metadata["output"] = read_file(builder.metadata["outfile"])
        builder.metadata["error"] = read_file(builder.metadata["errfile"])

        self.logger.debug(
            f"[{builder.name}] returncode: {builder.metadata['result']['returncode']}"
        )
        self.check_test_state(builder)

    def cancel(self, builder):
        """Cancel LSF job, this is required if job exceeds max pending time in queue.

        :param builder: builder object
        :type builder: BuilderBase, required
        """

        query = f"bkill {builder.metadata['jobid']}"

        cmd = BuildTestCommand(query)
        cmd.execute()
        msg = f"Cancelling Job: {builder.metadata['name']} running command: {query}"
        print(msg)
        self.logger.debug(msg)


class LSFJob(Job):
    def __init__(self, jobID):
        super().__init__(jobID)

    def is_pending(self):
        return self._state == "PEND"

    def is_running(self):
        return self._state == "RUN"

    def is_complete(self):
        return self._state == "DONE"

    def is_suspended(self):
        return self._state in ["PSUSP", "USUSP", "SSUSP"]

    def is_failed(self):
        return self._state == "EXIT"

    def poll(self):
        query = f"bjobs -noheader -o 'stat' {self.jobid}"

        logger.debug(query)
        cmd = BuildTestCommand(query)
        cmd.execute()
        job_state = cmd.get_output()
        self._state = "".join(job_state).rstrip()

        query = f"bjobs -noheader -o 'output_file' {self.jobid} "
        cmd = BuildTestCommand(query)
        cmd.execute()
        self._outfile = "".join(cmd.get_output()).rstrip()

        query = f"bjobs -noheader -o 'error_file' {self.jobid} "
        cmd = BuildTestCommand(query)
        cmd.execute()
        self._errfile = "".join(cmd.get_output()).rstrip()

        query = f"bjobs -noheader -o 'EXIT_CODE' {self.jobid} "
        cmd = BuildTestCommand(query)
        cmd.execute()
        output = "".join(cmd.get_output()).rstrip()

        # for 0 or negative exit code output is in form "-" otherwise set value retrieved by bjobs
        try:
            self.exitcode = int(output)
        except ValueError:
            self.exitcode = 0

    def cancel(self):
        query = f"bkill {self.jobid}"
        logger.debug(f"Cancelling job {self.jobid} by running: {query}")
        cmd = BuildTestCommand(query)
        cmd.execute()

    def output_file(self):
        return self._outfile

    def error_file(self):
        return self._errfile

    def exitcode(self):
        return self._exitcode
