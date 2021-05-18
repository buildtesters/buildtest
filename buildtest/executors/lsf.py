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

    def launcher_command(self):
        """This command returns the launcher command and any options specified in configuration file. This
        is useful when generating the build script in the BuilderBase class
        """
        cmd = [self.launcher]

        if self.queue:
            cmd += [f"-q {self.queue}"]

        if self.account:
            cmd += [f"-P {self.account}"]

        if self.launcher_opts:
            cmd += [" ".join(self.launcher_opts)]

        return cmd

    def dispatch(self, builder):
        """This method is responsible for dispatching job to scheduler.

        :param builder: builder object
        :type builder: BuilderBase, required
        """

        os.chdir(builder.stage_dir)
        self.logger.debug(f"Changing to stage directory {builder.stage_dir}")

        builder.run()

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

        builder.endtime()

        builder.metadata["job"] = builder.job.gather()
        builder.metadata["result"]["returncode"] = builder.job.exitcode()

        # self.end_time(builder)

        builder.metadata["outfile"] = os.path.join(
            builder.stage_dir, builder.job.output_file()
        )
        builder.metadata["errfile"] = os.path.join(
            builder.stage_dir, builder.job.error_file()
        )

        builder.metadata["output"] = read_file(builder.metadata["outfile"])
        builder.metadata["error"] = read_file(builder.metadata["errfile"])

        self.logger.debug(
            f"[{builder.name}] returncode: {builder.metadata['result']['returncode']}"
        )
        self.check_test_state(builder)


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

    def output_file(self):
        return self._outfile

    def error_file(self):
        return self._errfile

    def exitcode(self):
        return self._exitcode

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
            self._exitcode = int(output)
        except ValueError:
            self._exitcode = 0

    def gather(self):
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
        query = f"bjobs -o '{' '.join(format_fields)}' {self.jobid} -json"

        logger.debug(f"Gather LSF job data by running: {query}")
        cmd = BuildTestCommand(query)
        cmd.execute()
        out = cmd.get_output()
        out = "".join(out).rstrip()

        out = json.loads(out)

        job_data = {}

        records = out["RECORDS"][0]
        for field, value in records.items():
            job_data[field] = value

        return job_data

    def cancel(self):
        query = f"bkill {self.jobid}"
        logger.debug(f"Cancelling job {self.jobid} by running: {query}")
        cmd = BuildTestCommand(query)
        cmd.execute()
