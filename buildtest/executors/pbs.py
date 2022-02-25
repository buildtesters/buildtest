"""This module implements PBSExecutor class that defines how executors submit
job to PBS Scheduler"""
import json
import logging
import os

from buildtest.defaults import console
from buildtest.exceptions import RuntimeFailure
from buildtest.executors.base import BaseExecutor
from buildtest.executors.job import Job
from buildtest.utils.command import BuildTestCommand
from buildtest.utils.tools import deep_get

logger = logging.getLogger(__name__)


class PBSExecutor(BaseExecutor):
    """The PBSExecutor class is responsible for submitting jobs to PBS Scheduler.
    The class implements the following methods:

    - load: load PBS executors from configuration file
    - dispatch: submit PBS job to scheduler
    - poll: poll PBS job via qstat and retrieve job state
    - gather: gather job result
    - cancel: cancel job if it exceeds max pending time
    """

    type = "pbs"
    launcher = "qsub"

    def __init__(self, name, settings, site_configs, account=None, maxpendtime=None):

        self.maxpendtime = maxpendtime
        self.account = account
        super().__init__(name, settings, site_configs)

    def load(self):
        """Load the a PBS executor configuration from buildtest settings."""

        """
        self.launcher = self._settings.get("launcher") or deep_get(
            self._buildtestsettings.target_config, "executors", "defaults", "launcher"
        )
        """
        self.launcher_opts = self._settings.get("options")

        self.queue = self._settings.get("queue")
        self.account = (
            self.account
            or self._settings.get("account")
            or deep_get(
                self._buildtestsettings.target_config,
                "executors",
                "defaults",
                "account",
            )
        )
        self.maxpendtime = (
            self.maxpendtime
            or self._settings.get("maxpendtime")
            or deep_get(
                self._buildtestsettings.target_config,
                "executors",
                "defaults",
                "maxpendtime",
            )
        )

    def launcher_command(self, numprocs=None, numnodes=None):
        batch_cmd = [self.launcher]

        if self.queue:
            batch_cmd += [f"-q {self.queue}"]

        if self.account:
            batch_cmd += [f"-P {self.account}"]

        if numprocs:
            batch_cmd += [f"-l ncpus={numprocs}"]

        if numnodes:
            batch_cmd += [f"-l nodes={numnodes}"]

        if self.launcher_opts:
            batch_cmd += [" ".join(self.launcher_opts)]

        return batch_cmd

    def run(self, builder):
        """This method is responsible for dispatching PBS job, get JobID
        and start record metadata in builder object. If job failed to submit
        we check returncode and exit with failure. After we submit job, we
        start timer and record when job was submitted and poll job once to get
        job details and store them in builder object.

        Args:
            builder (buildtest.buildsystem.base.BuilderBase): An instance object of BuilderBase type
        """

        self.load()

        os.chdir(builder.stage_dir)

        cmd = self.bash_launch_command() + [os.path.basename(builder.build_script)]
        cmd = " ".join(cmd)

        try:
            command = builder.run(cmd)
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

        msg = f"[blue]{builder}[/]: JobID: {builder.metadata['jobid']} dispatched to scheduler"
        console.print(msg)
        self.logger.debug(msg)

        return builder

    def poll(self, builder):
        """This method is responsible for polling PBS job which will update the job state. If job is complete we will
        gather job result. If job is pending we will stop timer and check if pend time exceeds max pend time for executor.
        If so we will cancel the job.

        Args:
            builder (buildtest.buildsystem.base.BuilderBase): An instance object of BuilderBase type
        """

        builder.job.poll()

        # if job is complete gather job data
        if builder.job.is_complete():
            self.gather(builder)
            return

        builder.stop()

        # if job in pending or suspended, check if it exceeds maxpendtime if so cancel job
        if builder.job.is_pending() or builder.job.is_suspended():
            self.logger.debug(f"Time Duration: {builder.timer.duration()}")
            self.logger.debug(f"Max Pend Time: {self.maxpendtime}")

            # if timer time is more than requested pend time then cancel job
            if int(builder.timer.duration()) > self.maxpendtime:
                builder.job.cancel()
                builder.failure()
                console.print(
                    f"[blue]{builder}[/]: [red]Cancelling Job {builder.job.get()} because job exceeds max pend time of {self.maxpendtime} sec with current pend time of {builder.timer.duration()} sec[/red] "
                )

        builder.start()

    def gather(self, builder):
        """This method is responsible for gather job results including output and error file and complete metadata
        for job which is stored in the builder object. We will retrieve job exitcode which corresponds to test
        returncode.

        Args:
            builder (buildtest.buildsystem.base.BuilderBase): An instance object of BuilderBase type
        """

        builder.endtime()
        builder.metadata["job"] = builder.job.gather()
        builder.metadata["result"]["returncode"] = builder.job.exitcode()

        builder.metadata["outfile"] = builder.job.output_file()
        builder.metadata["errfile"] = builder.job.error_file()

        console.print(f"[blue]{builder}[/]: Job {builder.job.get()} is complete! ")

        builder.post_run_steps()


class PBSJob(Job):
    """The PBSJob models a PBS Job with helper methods to retrieve job state, check if job is running/pending/suspended. We have methods
    to poll job state, gather job results upon completion and cancel job.

    See https://www.altair.com/pdfs/pbsworks/PBSReferenceGuide2021.1.pdf section 8.1 for list of Job State Codes"""

    def __init__(self, jobID):
        super().__init__(jobID)

    def is_pending(self):
        """Return ``True`` if job is pending. A pending job is in state ``Q``."""
        return self._state == "Q"

    def is_running(self):
        """Return ``True`` if job is running. A completed job is in state ``R``."""
        return self._state == "R"

    def is_complete(self):
        """Return ``True`` if job is complete. A completed job is in state ``F``."""
        return self._state == "F"

    def is_suspended(self):
        """Return ``True`` if job is suspended which would be in one of these states ``H``, ``U``, ``S``."""
        return self._state in ["H", "U", "S"]

    def output_file(self):
        """Return output file of job"""
        return self._outfile

    def error_file(self):
        """Return error file of job"""
        return self._errfile

    def exitcode(self):
        """Return exit code of job"""
        return self._exitcode

    def success(self):
        """This method determines if job was completed successfully and returns ``True`` if exit code is 0.

        According to https://www.altair.com/pdfs/pbsworks/PBSAdminGuide2021.1.pdf section 14.9 Job Exit Status Codes we have the following

         - Exit Code:  X < 0         - Job could not be executed
         - Exit Code: 0 <= X < 128   -  Exit value of Shell or top-level process
         - Exit Code: X >= 128       - Job was killed by signal
         - Exit Code: X == 0         - Job executed was a successful
        """
        return self._exitcode == 0

    def fail(self):
        """Return ``True`` if their is a job failure which would be if exit code is not 0"""
        return not self.success()

    def poll(self):
        """This method will poll the PBS Job by running ``qstat -x -f -F json <jobid>`` which will report job data in JSON format that
        can be parsed to extract the job state. In PBS the active job state can be retrieved by reading property ``job_state`` property.
        Shown below is an example output

        .. code-block:: console

            [pbsuser@pbs tests]$ qstat -x -f -F json 157.pbs
            {
                "timestamp":1630683518,
                "pbs_version":"19.0.0",
                "pbs_server":"pbs",
                "Jobs":{
                    "157.pbs":{
                        "Job_Name":"pbs_hold_job",
                        "Job_Owner":"pbsuser@pbs",
                        "job_state":"H",
                        "queue":"workq",
                        "server":"pbs",
                        "Checkpoint":"u",
                        "ctime":"Fri Aug 20 23:14:08 2021",
                        "Error_Path":"pbs:/tmp/GitHubDesktop/buildtest/var/tests/generic.pbs.workq/hold/pbs_hold_job/da6d5b57/stage/pbs_hold_job.e157",
                        "Hold_Types":"u",
                        "Join_Path":"n",
                        "Keep_Files":"n",
                        "Mail_Points":"a",
                        "mtime":"Fri Aug 20 23:14:08 2021",
                        "Output_Path":"pbs:/tmp/GitHubDesktop/buildtest/var/tests/generic.pbs.workq/hold/pbs_hold_job/da6d5b57/stage/pbs_hold_job.o157",
                        "Priority":0,
                        "qtime":"Fri Aug 20 23:14:08 2021",
                        "Rerunable":"True",
                        "Resource_List":{
                            "ncpus":1,
                            "nodect":1,
                            "nodes":1,
                            "place":"scatter",
                            "select":"1:ncpus=1",
                            "walltime":"00:02:00"
                        },
                        "substate":20,
                        "Variable_List":{
                            "PBS_O_HOME":"/home/pbsuser",
                            "PBS_O_LOGNAME":"pbsuser",
                            "PBS_O_PATH":"/tmp/GitHubDesktop/buildtest/bin:/tmp/github/buildtest/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/opt/pbs/bin:/home/pbsuser/.local/bin:/home/pbsuser/bin",
                            "PBS_O_MAIL":"/var/spool/mail/pbsuser",
                            "PBS_O_SHELL":"/bin/bash",
                            "PBS_O_WORKDIR":"/tmp/GitHubDesktop/buildtest/var/tests/generic.pbs.workq/hold/pbs_hold_job/da6d5b57/stage",
                            "PBS_O_SYSTEM":"Linux",
                            "PBS_O_QUEUE":"workq",
                            "PBS_O_HOST":"pbs"
                        },
                        "Submit_arguments":"-q workq /tmp/GitHubDesktop/buildtest/var/tests/generic.pbs.workq/hold/pbs_hold_job/da6d5b57/stage/pbs_hold_job.sh",
                        "project":"_pbs_project_default"
                    }
                }
            }
        """

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
        """This method is called once job is complete. We will gather record of job by running
        ``qstat -x -f -F json <jobid>`` and return the json object as a dict.  This method is responsible
        for getting output file, error file and exit status of job.
        """

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
        """Cancel PBS job by running ``qdel <jobid>``."""
        query = f"qdel {self.jobid}"
        logger.debug(f"Cancelling job {self.jobid} by running: {query}")
        cmd = BuildTestCommand(query)
        cmd.execute()
