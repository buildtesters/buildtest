import logging

from buildtest.scheduler.job import Job
from buildtest.utils.command import BuildTestCommand

logger = logging.getLogger(__name__)


class CobaltJob(Job):
    """The ``CobaltJob`` class performs operation on cobalt job upon job submission such
    as polling job, gather job record, cancel job. We also retrieve job state and determine if job
    is pending, running, complete, suspended.
    """

    def __init__(self, jobID):
        super().__init__(jobID)
        self._outfile = str(jobID) + ".output"
        self._errfile = str(jobID) + ".error"
        self._cobaltlog = str(jobID) + ".cobaltlog"

    def is_pending(self):
        """Return ``True`` if job is pending otherwise returns ``False``. When cobalt recieves job it is
        in ``starting`` followed by ``queued`` state. We check if job is in either state.
        """

        return self._state in ["queued", "starting"]

    def is_running(self):
        """Return ``True`` if job is running otherwise returns ``False``. Cobalt job state for running job is
        is marked as ``running``"""

        return self._state == "running"

    def is_complete(self):
        """Return ``True`` if job is complete otherwise returns ``False``. Cobalt job state for completed job
        job is marked as ``exiting``"""

        return self._state == "exiting"

    def is_suspended(self):
        """Return ``True`` if job is suspended otherwise returns ``False``. Cobalt job state for suspended is
        marked as ``user_hold``"""

        return self._state == "user_hold"

    def is_cancelled(self):
        """Return ``True`` if job is cancelled otherwise returns ``False``. Job state is ``cancelled`` which
        is set by class ``cancel`` method
        """

        return self._state == "cancelled"

    def cobalt_log(self):
        """Return job cobalt.log file"""

        return self._cobaltlog

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
        """Poll job by running ``qstat -l --header State <jobid>`` which retrieves job state."""

        # get Job State by running 'qstat -l --header <jobid>'
        query = f"qstat -l --header State {self.jobid}"
        logger.debug(f"Getting Job State for '{self.jobid}' by running: '{query}'")
        cmd = BuildTestCommand(query)
        cmd.execute()
        output = cmd.get_output()

        output = " ".join(output).strip()

        # Output in format State: <state> so we need to get value of state
        job_state = output.partition(":")[2].strip()

        if job_state:
            self._state = job_state

        logger.debug(f"Job ID: '{self.job}' Job State: {self._state}")

    def gather(self):
        """Gather Job state by running **qstat -lf <jobid>** which retrieves all fields.
        The output is in text format which is parsed into key/value pair and stored in a dictionary. This method will
        return a dict containing the job record

        .. code-block:: console

             $ qstat -lf 347106
                JobID: 347106
                    JobName           : hold_job
                    User              : shahzebsiddiqui
                    WallTime          : 00:10:00
                    QueuedTime        : 00:13:14
                    RunTime           : N/A
                    TimeRemaining     : N/A

        """

        # 'qstat -lf <jobid>' will get all fields of Job.
        qstat_cmd = f"qstat -lf {self.jobid}"
        logger.debug(f"Executing command: {qstat_cmd}")
        cmd = BuildTestCommand(qstat_cmd)
        cmd.execute()
        output = cmd.get_output()

        job_record = {}
        # The output if in format KEY: VALUE so we store all records in a dictionary
        for line in output:
            key, sep, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            job_record[key] = value

        return job_record

    def cancel(self):
        """Cancel job by running ``qdel <jobid>``. This method is called if job timer exceeds
        ``maxpendtime`` if job is pending.
        """

        query = f"qdel {self.jobid}"
        logger.debug(f"Cancelling job {self.jobid} by running: {query}")
        cmd = BuildTestCommand(query)
        cmd.execute()

        self._state = "cancelled"
