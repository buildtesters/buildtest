import shutil
import sys
from buildtest.utils.command import BuildTestCommand
from buildtest.executors.base import BaseExecutor


class CobaltExecutor(BaseExecutor):
    """The CobaltExecutor class is responsible for submitting jobs to Cobalt Scheduler.

    """

    type = "cobalt"

    job_state = None
    poll_cmd = "qstat"
    
    qstat_fields = "-lf"

    def check(self):
        """Check cobalt binary is available before running tests. This will check
        the launcher (``qsub``) and ``qstat`` are available.
        """

        if not shutil.which(self.launcher):
            sys.exit(
                f"[{self.builder.metadata['name']}]: Cannot find launcher program: {self.launcher}"
            )

        if not shutil.which(self.poll_cmd):
            sys.exit(
                f"[{self.builder.metadata['name']}]: Cannot find cobalt poll command: {self.poll_cmd}"
            )

    def load(self):
        """Load the a Cobalt executor configuration from buildtest settings."""

        self.launcher = self._settings.get("launcher") or self._buildtestsettings[
            "executors"
        ].get("defaults", {}).get("launcher")
        self.launcher_opts = self._settings.get("options")

        self.queue = self._settings.get("queue")
        self.account = self._settings.get("account") or self._buildtestsettings[
            "executors"
        ].get("defaults", {}).get("account")
        self.max_pend_time = self._settings.get(
            "max_pend_time"
        ) or self._buildtestsettings["executors"].get("defaults", {}).get(
            "max_pend_time"
        )

    def dispatch(self):

        self.check()
        self.result = {}

        batch_cmd = [self.launcher]

        if self.queue:
            batch_cmd += [f"-q {self.queue}"]

        batch_cmd += [self.builder.metadata["testpath"]]
        self.builder.metadata["command"] = " ".join(batch_cmd)
        self.logger.debug(
            f"Running Test via command: {self.builder.metadata['command']}"
        )

        command = BuildTestCommand(self.builder.metadata["command"])
        command.execute()
        self.builder.start()

        # if qsub job submission returns non-zero exit that means we have failure, exit immediately
        if command.returncode != 0:
            err = f"[{self.builder.metadata['name']}] failed to submit job with returncode: {command.returncode} \n"
            err += f"[{self.builder.metadata['name']}] running command: {' '.join(batch_cmd)}"
            sys.exit(err)

        parse_jobid = command.get_output()
        parse_jobid = " ".join(parse_jobid)

        # convert JobID into integer
        self.job_id = int(parse_jobid)

        self.builder.metadata["jobid"] = self.job_id

        msg = f"[{self.builder.metadata['name']}] JobID: {self.builder.metadata['jobid']} dispatched to scheduler"
        print(msg)
        self.logger.debug(msg)

        self.result["state"] = "N/A"
        self.result["runtime"] = "0"
        self.result["returncode"] = "0"

        self.logger.debug(f"Query Job: {self.builder.metadata['jobid']}")

        qstat_cmd = (
            f"{self.poll_cmd} -l --header OutputPath:ErrorPath {self.builder.metadata['jobid']}"
        )
        cmd = BuildTestCommand(qstat_cmd)
        cmd.execute()
        content = cmd.get_output()
        for line in content:
            key, sep, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            
            if key == "OutputPath":
              self.builder.metadata["outfile"] = value

            if key == "ErrorPath":
              self.builder.metadata["errfile"] = value

        self.logger.debug(f"Output file will be written to: {self.builder.metadata['outfile']}")
        self.logger.debug(f"Error file will be written to: {self.builder.metadata['errfile']}")

        qstat_cmd = f"{self.poll_cmd} -lf {self.builder.metadata['jobid']}"
        self.logger.debug(f"Executing command: {qstat_cmd}")
        cmd = BuildTestCommand(qstat_cmd)
        cmd.execute()
        job_data = cmd.get_output()
        print(job_data)

    def poll(self):
     
        self.logger.debug(f"Query Job: {self.builder.metadata['jobid']}")

        qstat_cmd = (
            f"{self.poll_cmd} -l --header State {self.builder.metadata['jobid']}"
        )
        self.logger.debug(f"Executing command: {qstat_cmd}")
        cmd = BuildTestCommand(qstat_cmd)
        cmd.execute()
        job_state = cmd.get_output()
        job_state = " ".join(job_state).strip()
        # Output in format State: <state> so we need to get value of state
        job_state = job_state.partition(":")[2]
        job_state = job_state.strip()
 
        self.builder.job_state = job_state
         # store initial poll output in builder metadata
        # self.builder.metadata["job"] = job_data

        msg = f"[{self.builder.metadata['name']}]: JobID {self.builder.metadata['jobid']} in {self.builder.job_state} state "
        print(msg)
        self.logger.debug(msg)
      
        shutil.which(self.builder.metadata['outfile'])

	# additional check to see if job outputfile is written to file system, since 
        # qstat will remove completed job and it can't be polled. 
        if shutil.which(self.builder.metadata['outfile']):
           self.builder.job_state = 'done'
           return

        if self.builder.job_state == "pending":
            self.builder.stop()
            self.logger.debug(f"Time Duration: {self.builder.duration}")
            self.logger.debug(f"Max Pend Time: {self.max_pend_time}")

            # if timer time is more than requested pend time then cancel job
            if int(self.builder.duration) > self.max_pend_time:
                self.cancel()
                job_state = "CANCELLED"
                print(
                    "Cancelling Job because duration time: {:f} sec exceeds max pend time: {} sec".format(
                        self.builder.duration, self.max_pend_time
                    )
                )
                self.builder.job_state = self.job_state
                return self.job_state

            self.builder.start()
            self.builder.job_state = job.state

    def cancel(self):
       """Cancel Cobalt job using qdel, this operation is performed if job exceeds its max_pend_time"""

       query = f"qdel {self.builder.metadata['jobid']}"
       
       cmd = BuildTestCommand(query)
       cmd.execute()
       msg = f"Cancelling Job: {self.builder.metadata['name']} running command: {query}"
       print(msg)
       self.logger.debug(msg)
     
