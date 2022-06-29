import json
import logging

from buildtest.scheduler.job import Job
from buildtest.utils.command import BuildTestCommand

logger = logging.getLogger(__name__)


class PBSJob(Job):
    """The PBSJob models a PBS Job with helper methods to retrieve job state, check if job is running/pending/suspended. We have methods
    to poll job state, gather job results upon completion and cancel job.
    """

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

        According to https://help.altair.com/2021.1.3/PBS%20Professional/PBSAdminGuide2021.1.3.pdf section 14.9 Job Exit Status Codes we have the following

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
