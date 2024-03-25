import json
import logging
import re
import time
import xml.etree.ElementTree as ET

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
        return self._state == "C"

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

    def fetch_output_error_files(self):
        """Fetch output and error files right after job submission."""
        query = f"qstat -f {self.jobid}"
        cmd = BuildTestCommand(query)
        cmd.execute()
        output = " ".join(cmd.get_output())

        # Extract output and error files from the qstat output
        output_match = re.search(r"Output_Path = .+:(?P<output>.+)", output)
        error_match = re.search(r"Error_Path = .+:(?P<error>.+)", output)

        if output_match:
            self._outfile = output_match.group("output")
        if error_match:
            self._errfile = error_match.group("error")

        """
        # Regular expression pattern to match the OutPut_Path field. This will account for text spanning multiple lines
        pattern = r"Output_Path\s*=\s*(.*?)\s*Priority"
        match = re.search(pattern, output, re.DOTALL)

        if match:
            lines = match.group(1).split(":")[1].split("\n")
            # Remove leading whitespace from lines after the first line
            formatted_lines = [lines[0]] + [line.strip() for line in lines[1:]]

            self._outfile = "".join(formatted_lines)
            logger.debug(self._outfile)

        # Regular expression pattern to match the Error_Path field
        pattern = r"Error_Path\s*=\s*(.*?)\s*(?:\n\s*(?:\w+\s*=)|$)"
        match = re.search(pattern, output, re.DOTALL)
        if match:
            lines = match.group(1).split(":")[1].split("\n")
            # Remove leading whitespace from lines after the first line
            formatted_lines = [lines[0]] + [line.strip() for line in lines[1:]]

            self._errfile = "".join(formatted_lines)
        """

    def is_output_ready(self):
        """Check if the output and error file exists."""
        if not self._outfile or not self._errfile:
            self.fetch_output_error_files()
        return os.path.exists(self._outfile) and os.path.exists(self._errfile)

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

        query = f"qstat -f {self.jobid}"

        logger.debug(f"Polling job by running: {query}")
        cmd = BuildTestCommand(query)
        cmd.execute()
        output = " ".join(cmd.get_output())

        pattern = r"^Job Id:\s*(?P<jobid>\S+)"
        jobid_match = re.search(pattern, output, re.MULTILINE)
        logger.debug(
            f"Extracting Job ID from output of command: {query} by applying regular expression pattern: '{pattern}'. The return value is {jobid_match}"
        )
        if jobid_match:
            self.jobid = jobid_match.group("jobid")

        # job_data = json.loads(output)
        pattern = r"^\s*job_state = (?P<state>[A-Z])"
        state_match = re.search(pattern, output, re.MULTILINE)

        """
        if not state_match:
            self.log(f'Job state not found (job info follows):\n{output}')
            continue
        """

        self._state = state_match.group("state")

        pattern = r"^\s*exit_status = (?P<code>\d+)"
        exitcode_match = re.search(pattern, output, re.MULTILINE)

        logger.debug(
            f"Retrieving exitcode for Job: {self.jobid} by applying regular expression pattern: '{pattern}'. The return value is {exitcode_match}"
        )
        if exitcode_match:
            self._exitcode = int(exitcode_match.group("code"))
            logger.debug(f"Retrieve exitcode: {self._exitcode} for Job: {self.jobid}")

        # ---- Get output and error files ----
        self.is_output_ready()

        # if job is running and the start time is not recorded then we record the start time
        if self.is_running() and not self.starttime:
            self.starttime = time.time()

    def gather(self):
        """This method is called once job is complete. We will gather record of job by running
        ``qstat -x -f -F json <jobid>`` and return the json object as a dict.  This method is responsible
        for getting output file, error file and exit status of job.
        """

        # job_data = json.loads(output)

        # output in the form of pbs:<path>
        # self._outfile = job_data["Jobs"][self.jobid]["Output_Path"].split(":")[1]
        # self._errfile = job_data["Jobs"][self.jobid]["Error_Path"].split(":")[1]

        # self._exitcode = self._get_exitcode()
        return {}

    def _get_exitcode(self):
        cmd = BuildTestCommand(f"qstat -f {self.jobid}")
        output = " ".join(cmd.get_output())
        exitcode_match = re.search(
            r"^\s*exit_status = (?P<code>\d+)", output, re.MULTILINE
        )
        if exitcode_match:
            logger.debug(exitcode_match.group("exit_status"))
            return int(exit_status_match.group("exit_status"))

        return None

    def cancel(self):
        """Cancel PBS job by running ``qdel <jobid>``."""
        query = f"qdel {self.jobid}"
        logger.debug(f"Cancelling job {self.jobid} by running: {query}")
        cmd = BuildTestCommand(query)
        cmd.execute()


class TorqueJob(PBSJob):
    pass
