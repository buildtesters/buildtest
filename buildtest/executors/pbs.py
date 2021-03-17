import datetime
import json
import os
import sys

from buildtest.executors.base import BaseExecutor
from buildtest.utils.command import BuildTestCommand
from buildtest.utils.file import read_file
from buildtest.utils.tools import deep_get


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

        self.max_pend_time = self._settings.get("max_pend_time") or deep_get(
            self._buildtestsettings.target_config, "executors", "defaults", "max_pend_time"
        )

    def dispatch(self):
        """This method is responsible for dispatching PBS job, get JobID
        and start record metadata in builder object. If job failed to submit
        we check returncode and exit with failure. After we submit job, we
        start timer and record when job was submitted and poll job once to get
        job details and store them in builder object.
        """

        self.load()

        os.chdir(self.builder.stage_dir)

        batch_cmd = [self.launcher]

        if self.queue:
            batch_cmd += [f"-q {self.queue}"]

        if self.account:
            batch_cmd += [f"-P {self.account}"]

        if self.launcher_opts:
            batch_cmd += [" ".join(self.launcher_opts)]

        batch_cmd += [self.builder.metadata["testpath"]]
        self.builder.metadata["command"] = " ".join(batch_cmd)
        self.logger.debug(
            f"Running Test via command: {self.builder.metadata['command']}"
        )
        self.builder.metadata["result"]["starttime"] = datetime.datetime.now().strftime(
            "%Y/%m/%d %X"
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
        self.job_id = " ".join(parse_jobid).strip()

        self.builder.metadata["jobid"] = self.job_id

        msg = f"[{self.builder.metadata['name']}] JobID: {self.builder.metadata['jobid']} dispatched to scheduler"
        print(msg)
        self.logger.debug(msg)

        qstat_cmd = f"{self.poll_cmd} -f -F json {self.builder.metadata['jobid']}"
        cmd = BuildTestCommand(qstat_cmd)
        cmd.execute()
        output = cmd.get_output()
        output = " ".join(output)
        job_data = json.loads(output)

        # output in the form of <server>:<file>
        self.builder.metadata['outfile'] = job_data["Jobs"][self.job_id]["Output_Path"].split(":")[1]
        self.builder.metadata['errfile'] = job_data["Jobs"][self.job_id]["Error_Path"].split(":")[1]

    def poll(self):
        """This method is responsible for polling Cobalt job, we check the
        job state and existence of output file. If file exists or job is in
        'exiting' stage we set job to 'done' stage and gather results. If job
        is in 'pending' stage we check if job exceeds 'max_pend_time' time limit
        by checking with builder timer attribute using ``start`` and ``stop`` method.
        If job exceeds the time limit job is cancelled.
        """

        self.logger.debug(f"Query Job: {self.builder.metadata['jobid']}")
        # run qstat -f -F json <jobid>
        qstat_cmd = (
            f"{self.poll_cmd} -x -f -F json {self.builder.metadata['jobid']}"
        )
        self.logger.debug(f"Executing command: {qstat_cmd}")
        cmd = BuildTestCommand(qstat_cmd)
        cmd.execute()
        output = cmd.get_output()
        output = " ".join(output)

        job_data = json.loads(output)

        self.logger.debug("Job record")
        self.logger.debug(json.dumps(job_data,indent=2))

        job_state = job_data["Jobs"][self.builder.metadata['jobid']]["job_state"]

        if job_state:
            self.builder.job_state = job_state

        self.logger.debug(
            "[%s]: JobID %s in %s state ",
            self.builder.metadata["name"],
            self.builder.metadata["jobid"],
            self.builder.job_state,
        )

        # if job in pending state (Q) check if it exceeds max_pend_time if so cancel job
        if self.builder.job_state == "Q":
            self.builder.stop()
            self.logger.debug(f"Time Duration: {self.builder.duration}")
            self.logger.debug(f"Max Pend Time: {self.max_pend_time}")

            # if timer time is more than requested pend time then cancel job
            if int(self.builder.duration) > self.max_pend_time:
                self.cancel()
                self.builder.job_state = "CANCELLED"
                print(
                    "Cancelling Job because duration time: {:f} sec exceeds max pend time: {} sec".format(
                        self.builder.duration, self.max_pend_time
                    )
                )

            self.builder.start()

    def gather(self):
        """This method is responsible for getting output of job using `qstat -x -f -F json <jobID>`
        and storing the result in builder object. We retrieve specific fields such as exit status,
        start time, end time, runtime and store them in builder object. We read output and error file
        and store the content in builder object.
        """

        qstat_cmd = f"{self.poll_cmd} -x -f -F json {self.builder.metadata['jobid']}"

        self.logger.debug(f"Executing command: {qstat_cmd}")
        cmd = BuildTestCommand(qstat_cmd)
        cmd.execute()
        output = cmd.get_output()
        output = " ".join(output)

        job_data = json.loads(output)

        self.builder.metadata["result"]["returncode"] = job_data["Jobs"][self.builder.metadata['jobid']]["Exit_status"]
        self.builder.metadata["result"]["starttime"] = job_data["Jobs"][self.builder.metadata['jobid']]["stime"]
        self.builder.metadata["result"]["endtime"] = job_data["Jobs"][self.builder.metadata['jobid']]["etime"]
        self.builder.metadata["result"]["runtime"] = job_data["Jobs"][self.builder.metadata['jobid']]["resources_used"]["walltime"]
        self.builder.metadata["job"] = job_data

        self.builder.metadata["output"] = read_file(self.builder.metadata["outfile"])
        self.builder.metadata["error"] = read_file(self.builder.metadata["errfile"])

        self.check_test_state()

    def cancel(self):
        """Cancel Cobalt job using qdel, this operation is performed if job exceeds its max_pend_time"""

        query = f"qdel {self.builder.metadata['jobid']}"

        cmd = BuildTestCommand(query)
        cmd.execute()
        msg = (
            f"Cancelling Job: {self.builder.metadata['name']} running command: {query}"
        )
        print(msg)
        self.logger.debug(msg)
