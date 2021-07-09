"""
This module implements the LSFExecutor class responsible for submitting
jobs to LSF Scheduler. This class is called in class BuildExecutor
when initializing the executors.
"""

import json
import logging
import os
import re

from buildtest.executors.base import BaseExecutor
from buildtest.executors.job import Job
from buildtest.utils.command import BuildTestCommand
from buildtest.utils.file import read_file
from buildtest.utils.tools import deep_get

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
        """This method is responsible for dispatching job to scheduler and extracting job ID by applying a ``re.search`` against
        output at onset of job submission. If job id is not retrieved due to job failure or unable to match regular expression we
        mark job incomplete by invoking ``builder.incomplete()`` method and return from method.

        If we have a valid job ID we invoke ``LSFJob`` class given the job id to poll job and store this into ``builder.job`` attribute.

        :param builder: builder object
        :type builder: BuilderBase, required
        """

        os.chdir(builder.stage_dir)
        self.logger.debug(f"Changing to stage directory {builder.stage_dir}")

        command = builder.run()
        out = command.get_output()
        out = " ".join(out)
        pattern = r"(\d+)"
        # output in the form:  'Job <58654> is submitted to queue <batch>' and applying regular expression to get job ID
        m = re.search(pattern, out)
        self.logger.debug(f"Applying regular expression '{pattern}' to output: '{out}'")

        # if there is no match we raise error
        if not m:
            self.logger.debug(f"Unable to find LSF Job ID in output: '{out}'")
            builder.incomplete()
            return

        try:
            job_id = int(m.group(0))
        except ValueError:
            self.logger.debug(
                f"Unable to convert '{m.group(0)}' to int to extract Job ID"
            )
            builder.incomplete()
            return

        builder.job = LSFJob(job_id)

        builder.metadata["jobid"] = job_id

        msg = f"[{builder.metadata['name']}] JobID: {builder.metadata['jobid']} dispatched to scheduler"
        self.logger.debug(msg)
        print(msg)

    def poll(self, builder):
        """Given a builder object we poll the job by invoking builder method ``builder.job.poll()`` return state of job. If
        job is suspended or pending we stop timer and check if timer exceeds max_pend_time value which could be defined in configuration
        file or passed via command line ``--max-pend-time``

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
        """Gather Job detail after completion of job by invoking the builder method ``builder.job.gather()``.
        We retrieve exit code, output file, error file and update builder metadata.

        :param builder: builder object
        :type builder: BuilderBase, required
        """

        builder.endtime()

        builder.metadata["job"] = builder.job.gather()
        builder.metadata["result"]["returncode"] = builder.job.exitcode()

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
        builder.copy_stage_files()

        self.check_test_state(builder)


class LSFJob(Job):
    def __init__(self, jobID):
        super().__init__(jobID)

    def is_pending(self):
        """Check if Job is pending which is reported by LSF as ``PEND``. Return ``True`` if there is a match otherwise returns ``False``"""

        return self._state == "PEND"

    def is_running(self):
        """Check if Job is running which is reported by LSF as ``RUN``. Return ``True`` if there is a match otherwise returns ``False``"""

        return self._state == "RUN"

    def is_complete(self):
        """Check if Job is complete which is in ``DONE`` state. Return ``True`` if there is a match otherwise return ``False``"""

        return self._state == "DONE"

    def is_suspended(self):
        """Check if Job is in suspended state which could be in any of the following states: [``PSUSP``, ``USUSP``, ``SSUSP``].
        We return ``True`` if job is in one of the states otherwise return ``False``
        """

        return self._state in ["PSUSP", "USUSP", "SSUSP"]

    def is_failed(self):
        """Check if Job failed. We return ``True`` if job is in ``EXIT`` state otherwise return ``False``"""

        return self._state == "EXIT"

    def output_file(self):
        """Return job output file"""

        return self._outfile

    def error_file(self):
        """Return job error file"""

        return self._errfile

    def exitcode(self):
        """Return job exit code"""

        return self._exitcode

    def poll(self):
        """Given a job id we poll the LSF Job by retrieving its job state, output file, error file and exit code.
        We run the following commands to retrieve following states

        - Job State: ``bjobs -noheader -o 'stat' <JOBID>``
        - Output File: ``bjobs -noheader -o 'output_file' <JOBID>'``
        - Error File: ``bjobs -noheader -o 'error_file' <JOBID>'``
        - Exit Code  File: ``bjobs -noheader -o 'EXIT_CODE' <JOBID>'``
        """

        # get job state
        query = f"bjobs -noheader -o 'stat' {self.jobid}"
        logger.debug(query)
        logger.debug(
            f"Extracting Job State for job: {self.jobid} by running  '{query}'"
        )
        cmd = BuildTestCommand(query)
        cmd.execute()
        job_state = cmd.get_output()
        self._state = "".join(job_state).rstrip()
        logger.debug(f"Job State: {self._state}")

        # get path to output file
        query = f"bjobs -noheader -o 'output_file' {self.jobid} "
        logger.debug(
            f"Extracting OUTPUT FILE for job: {self.jobid} by running  '{query}'"
        )
        cmd = BuildTestCommand(query)
        cmd.execute()
        self._outfile = "".join(cmd.get_output()).rstrip()
        logger.debug(f"Output File: {self._outfile}")

        # get path to error file
        query = f"bjobs -noheader -o 'error_file' {self.jobid} "
        logger.debug(
            f"Extracting ERROR FILE for job: {self.jobid} by running  '{query}'"
        )
        cmd = BuildTestCommand(query)
        cmd.execute()
        self._errfile = "".join(cmd.get_output()).rstrip()
        logger.debug(f"Error File: {self._errfile}")

        query = f"bjobs -noheader -o 'EXIT_CODE' {self.jobid} "
        logger.debug(
            f"Extracting EXIT CODE for job: {self.jobid} by running  '{query}'"
        )
        cmd = BuildTestCommand(query)
        cmd.execute()
        output = "".join(cmd.get_output()).rstrip()

        # for 0 or negative exit code output is in form "-" otherwise set value retrieved by bjobs
        try:
            self._exitcode = int(output)
        except ValueError:
            self._exitcode = 0

        logger.debug(f"Exit Code: {self._exitcode}")

    def gather(self):
        """Gather Job record at onset of job completion by running ``bjobs -o '<format1> <format2>' <jobid> -json``. The format
        fields extracted from job are the following:

           - "job_name"
           - "stat"
           - "user"
           - "user_group"
           - "queue"
           - "proj_name"
           - "pids"
           - "exit_code"
           - "from_host"
           - "exec_host"
           - "submit_time"
           - "start_time"
           - "finish_time"
           - "nthreads"
           - "exec_home"
           - "exec_cwd"
           - "output_file"
           - "error_file"

        Shown below is the output format and we retrieve the job records defined in **RECORDS** property

        .. code-block:: console

            $ bjobs -o 'job_name stat user user_group queue proj_name pids exit_code from_host exec_host submit_time start_time finish_time nthreads exec_home exec_cwd output_file error_file' 58652 -json
            {
              "COMMAND":"bjobs",
              "JOBS":1,
              "RECORDS":[
                {
                  "JOB_NAME":"hold_job",
                  "STAT":"PSUSP",
                  "USER":"shahzebsiddiqui",
                  "USER_GROUP":"GEN014ECPCI",
                  "QUEUE":"batch",
                  "PROJ_NAME":"GEN014ECPCI",
                  "PIDS":"",
                  "EXIT_CODE":"",
                  "FROM_HOST":"login1",
                  "EXEC_HOST":"",
                  "SUBMIT_TIME":"May 28 12:45",
                  "START_TIME":"",
                  "FINISH_TIME":"",
                  "NTHREADS":"",
                  "EXEC_HOME":"",
                  "EXEC_CWD":"",
                  "OUTPUT_FILE":"hold_job.out",
                  "ERROR_FILE":"hold_job.err"
                }
              ]
            }
        """

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
        """Cancel LSF Job by running ``bkill <jobid>``. This is called if job has exceeded
        `max_pend_time` limit during poll stage."""

        query = f"bkill {self.jobid}"
        logger.debug(f"Cancelling job {self.jobid} by running: {query}")
        cmd = BuildTestCommand(query)
        cmd.execute()
