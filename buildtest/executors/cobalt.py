import os
import re
import shutil
import sys
from buildtest.utils.command import BuildTestCommand
from buildtest.utils.file import read_file
from buildtest.executors.base import BaseExecutor


class CobaltExecutor(BaseExecutor):
    """The CobaltExecutor class is responsible for submitting jobs to Cobalt Scheduler.

    """

    type = "cobalt"

    job_state = None
    poll_cmd = "qstat"
    

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

        batch_cmd = [self.launcher]

        if self.queue:
            batch_cmd += [f"-q {self.queue}"]

        if self.account:
            batch_cmd += [f"--project {self.account}"]
        
        if self.launcher_opts:
           batch_cmd += [" ".join(self.launcher_opts)]

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
        ##### NEED TO FIGURE OUT THIS SECTION FOR CAPTURING DATA
        qstat_cmd = f"{self.poll_cmd} -lf {self.builder.metadata['jobid']}"
        self.logger.debug(f"Executing command: {qstat_cmd}")         
        cmd = BuildTestCommand(qstat_cmd)
        cmd.execute()
        job_data = cmd.get_output()

    def poll(self):
     
        self.logger.debug(f"Query Job: {self.builder.metadata['jobid']}")

        qstat_cmd = (
            f"{self.poll_cmd} -l --header State {self.builder.metadata['jobid']}"
        )
        self.logger.debug(f"Executing command: {qstat_cmd}")
        cmd = BuildTestCommand(qstat_cmd)
        cmd.execute()
        output = cmd.get_output()

        output = " ".join(output).strip()
        # Output in format State: <state> so we need to get value of state
        job_state = output.partition(":")[2]
        self.job_state = job_state.strip()
        print(f"job state: {job_state}")
        if self.job_state:
            self.builder.job_state = self.job_state

        # store initial poll output in builder metadata
        # self.builder.metadata["job"] = job_data

        msg = f"[{self.builder.metadata['name']}]: JobID {self.builder.metadata['jobid']} in {self.builder.job_state} state "
        print(msg)
        self.logger.debug(msg)
        print(self.builder.metadata['outfile'])
        print("running shutil.which - ", shutil.which(self.builder.metadata['outfile']))
        
	# additional check to see if job outputfile is written to file system.
        # If job is in 'exiting' state we assume job is now finished, qstat will remove 
        # completed job and it can't be polled so it is likely self.job_state is undefined
        if shutil.which(self.builder.metadata['outfile']) or self.job_state == "exiting":
           self.builder.job_state = 'done'
           print("builder state - ", self.builder.job_state)
           self.gather()
           return

        print("builder state - ", self.builder.job_state)

        if self.builder.job_state == "pending":
            self.builder.stop()
            self.logger.debug(f"Time Duration: {self.builder.duration}")
            self.logger.debug(f"Max Pend Time: {self.max_pend_time}")

            # if timer time is more than requested pend time then cancel job
            if int(self.builder.duration) > self.max_pend_time:
                self.cancel()
                self.job_state = "CANCELLED"
                print(
                    "Cancelling Job because duration time: {:f} sec exceeds max pend time: {} sec".format(
                        self.builder.duration, self.max_pend_time
                    )
                )

            self.builder.start()
            self.builder.job_state = self.job_state
  
    def gather(self):
        self.builder.metadata["result"] = {}

        cobaltlog = str(self.builder.metadata['jobid']) + ".cobaltlog"
        if shutil.which(cobaltlog):
          content = read_file(cobaltlog)
          print (content)
          exit_code_message = "task completed normally with an exit code of 0"
          if re.search(exit_code_message,content):
             self.builder.metadata["result"]["returncode"] = 0
          else:
             self.builder.metadata["result"]["returncode"] = 1

        self.check_test_state()
    def cancel(self):
       """Cancel Cobalt job using qdel, this operation is performed if job exceeds its max_pend_time"""

       query = f"qdel {self.builder.metadata['jobid']}"
       
       cmd = BuildTestCommand(query)
       cmd.execute()
       msg = f"Cancelling Job: {self.builder.metadata['name']} running command: {query}"
       print(msg)
       self.logger.debug(msg)
       
