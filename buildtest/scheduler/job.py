import time


class Job:
    """This is a base class for holding job level data and common methods for used
    for batch job submission."""

    def __init__(self, jobID):
        self.jobid = jobID
        self._state = None
        self._outfile = None
        self._errfile = None
        self._exitcode = None
        # used to store the job elapsed time
        self.elapsedtime = 0

        # used for job pending time
        self.pendtime = 0

        # time when job was submitted
        self.submittime = time.time()

        # time when job was started
        self.starttime = None

    def state(self):
        """Return job state"""
        return self._state

    def get(self):
        """Return Job ID as string type"""
        return str(self.jobid)

    def is_pending(self):
        """Check if job is in pending state"""
        raise NotImplementedError

    def is_running(self):
        """Check if job is in running state"""
        raise NotImplementedError

    def is_suspended(self):
        """Check if job is in suspended state"""
        raise NotImplementedError

    def cancel(self):
        """Cancel job"""
        raise NotImplementedError

    def poll(self):
        """Poll job and update job state."""
        raise NotImplementedError

    def get_output_and_error_files(self):
        """Get output and error of job"""
        raise NotImplementedError

    def output_file(self):
        """Return output file of job"""
        return self._outfile

    def error_file(self):
        """Return error file of job"""
        return self._errfile

    def exitcode(self):
        """Return exit code of job"""
        return self._exitcode
