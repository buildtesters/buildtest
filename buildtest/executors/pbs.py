"""This module implements PBSExecutor class that defines how executors submit
job to PBS Scheduler"""
import json
import logging
import os

from buildtest.exceptions import RuntimeFailure
from buildtest.executors.base import BaseExecutor
from buildtest.executors.job import Job
from buildtest.utils.command import BuildTestCommand
from buildtest.utils.tools import deep_get

logger = logging.getLogger(__name__)


class PBSExecutor(BaseExecutor):
    """The PBSExecutor class is responsible for submitting jobs to PBS Scheduler.
    The class implements the following methods:

    load: load PBS executors from configuration file
    dispatch: submit PBS job to scheduler
    poll: poll PBS job via qstat and retrieve job state
    gather: gather job result
    cancel: cancel job if it exceeds max pending time
    """

    type = "pbs"
    poll_cmd = "qstat"

    def __init__(self, name, settings, site_configs, max_pend_time=None):

        self.maxpendtime = max_pend_time
        super().__init__(name, settings, site_configs)

    def load(self):
        """Load the a Cobalt executor configuration from buildtest settings."""

        self.launcher = self._settings.get("launcher") or deep_get(
            self._buildtestsettings.target_config, "executors", "defaults", "launcher"
        )
        self.launcher_opts = self._settings.get("options")

        self.queue = self._settings.get("queue")
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
        batch_cmd = [self.launcher]

        if self.queue:
            batch_cmd += [f"-q {self.queue}"]

        if self.account:
            batch_cmd += [f"-P {self.account}"]

        if self.launcher_opts:
            batch_cmd += [" ".join(self.launcher_opts)]

        return batch_cmd

    def dispatch(self, builder):
        """This method is responsible for dispatching PBS job, get JobID
        and start record metadata in builder object. If job failed to submit
        we check returncode and exit with failure. After we submit job, we
        start timer and record when job was submitted and poll job once to get
        job details and store them in builder object.

        :param builder: builder object
        :type builder: BuilderBase, required
        """

        self.load()

        os.chdir(builder.stage_dir)

        try:
            command = builder.run()
        except RuntimeFailure as err:
            builder.failure()
            self.logger.error(err)
            return

        out = command.get_output()
        JobID = " ".join(out).strip()

        builder.metadata["jobid"] = JobID

        builder.job = PBSJob(JobID)

        # store job id
        builder.metadata["jobid"] = builder.job.get()

        msg = f"[{builder.metadata['name']}] JobID: {builder.metadata['jobid']} dispatched to scheduler"
        print(msg)
        self.logger.debug(msg)

        return builder

    def poll(self, builder):
        """This method is responsible for polling PBS job.

        :param builder: builder object
        :type builder: BuilderBase, required
        """

        builder.job.poll()

        # if job is complete gather job data
        if builder.job.is_complete():
            self.gather(builder)
            return

        builder.stop()

        # if job in pending or suspended, check if it exceeds max_pend_time if so cancel job
        if builder.job.is_pending() or builder.job.is_suspended():
            self.logger.debug(f"Time Duration: {builder.timer.duration()}")
            self.logger.debug(f"Max Pend Time: {self.max_pend_time}")

            # if timer time is more than requested pend time then cancel job
            if int(builder.timer.duration()) > self.max_pend_time:
                builder.job.cancel()
                builder.failure()
                print(
                    "{}: Cancelling Job: {} because job exceeds max pend time: {} sec with current pend time of {} ".format(
                        builder,
                        builder.job.get(),
                        self.max_pend_time,
                        builder.timer.duration(),
                    )
                )

        builder.start()

    def gather(self, builder):
        """This method is responsible for getting output of job using `qstat -x -f -F json <jobID>`
        and storing the result in builder object. We retrieve specific fields such as exit status,
        start time, end time, runtime and store them in builder object. We read output and error file
        and store the content in builder object.

        :param builder: builder object
        :type builder: BuilderBase, required
        """

        builder.endtime()
        builder.metadata["job"] = builder.job.gather()
        builder.metadata["result"]["returncode"] = builder.job.exitcode()

        builder.metadata["outfile"] = builder.job.output_file()
        builder.metadata["errfile"] = builder.job.error_file()

        print(f"{builder}: Job {builder.job.get()} is complete! ")

        builder.post_run_steps()


class PBSJob(Job):
    """See https://www.altair.com/pdfs/pbsworks/PBSReferenceGuide2021.1.pdf section 8.1 for Job State Codes"""

    def __init__(self, jobID):
        super().__init__(jobID)

    def is_pending(self):
        return self._state == "Q"

    def is_running(self):
        return self._state == "R"

    def is_complete(self):
        return self._state == "F"

    def is_suspended(self):
        return self._state in ["H", "U", "S"]

    def output_file(self):
        return self._outfile

    def error_file(self):
        return self._errfile

    def exitcode(self):
        return self._exitcode

    def success(self):
        """This method determines if job was completed successfully. According to https://www.altair.com/pdfs/pbsworks/PBSAdminGuide2021.1.pdf
        section 14.9 Job Exit Status Codes we have the following:
            Exit Code:  X < 0         - Job could not be executed
            Exit Code: 0 <= X < 128   -  Exit value of Shell or top-level process
            Exit Code: X >= 128       - Job was killed by signal

            Exit Code 0 is a success
        """
        return self._exitcode == 0

    def fail(self):
        return not self.success()

    def poll(self):
        """This method will poll the PBS Job by running ``qstat -x -f -F json <jobid>``"""
        query = f"qstat -x -f -F json {self.jobid}"

        logger.debug(query)
        cmd = BuildTestCommand(query)
        cmd.execute()
        output = " ".join(cmd.get_output())
        job_data = json.loads(output)

        self._state = job_data["Jobs"][self.jobid]["job_state"]

        # The Exit_status property will be available when job is finished
        self._exitcode = job_data["Jobs"][self.jobid].get("Exit_status")

    def gather(self):
        query = f"qstat -x -f -F json {self.jobid}"

        logger.debug(f"Executing command: {query}")
        cmd = BuildTestCommand(query)
        cmd.execute()
        output = cmd.get_output()
        output = " ".join(output)

        job_data = json.loads(output)

        # output in the form of pbs:<path>
        self._outfile = job_data["Jobs"][self.jobid]["Output_Path"].split(":")[1]
        self._errfile = job_data["Jobs"][self.jobid]["Error_Path"].split(":")[1]

        # if job is complete but terminated or deleted we won't have exit status in that case we ignore this file
        try:
            self._exitcode = job_data["Jobs"][self.jobid]["Exit_status"]
        except KeyError:
            self._exitcode = -1
        return job_data

    def cancel(self):
        query = f"qdel {self.jobid}"
        logger.debug(f"Cancelling job {self.jobid} by running: {query}")
        cmd = BuildTestCommand(query)
        cmd.execute()
