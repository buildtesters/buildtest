import datetime
import json
import os
import re
import shutil
import sys

from buildtest.executors.base import BaseExecutor
from buildtest.utils.command import BuildTestCommand
from buildtest.utils.file import read_file
from buildtest.utils.tools import deep_get


class CobaltExecutor(BaseExecutor):
    """The CobaltExecutor class is responsible for submitting jobs to Cobalt Scheduler.
    The class implements the following methods:

    load: load Cobalt executors from configuration file
    dispatch: submit Cobalt job to scheduler
    poll: poll Cobalt job via qstat and retrieve job state
    gather: gather job result
    cancel: cancel job if it exceeds max pending time
    """

    type = "cobalt"
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
            self._buildtestsettings, "executors", "defaults", "max_pend_time"
        )

    def dispatch(self):
        """This method is responsible for dispatching Cobalt job, get JobID
        and start record metadata in builder object. If job failed to submit
        we check returncode and exit with failure. After we submit job, we
        start timer and record when job was submitted and poll job once to get
        job details and store them in builder object.
        """

        os.chdir(self.builder.stage_dir)

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
        parse_jobid = " ".join(parse_jobid)

        # convert JobID into integer
        self.job_id = int(parse_jobid)

        self.builder.metadata["jobid"] = self.job_id

        msg = f"[{self.builder.metadata['name']}] JobID: {self.builder.metadata['jobid']} dispatched to scheduler"
        print(msg)
        self.logger.debug(msg)

        # output and error file in format <JOBID>.output and <JOBID>.error we set full path to file. By
        # default Cobalt will write file into current directory where job is submitted. We assume output and error
        # file names are not set in job script
        outfile = str(self.builder.metadata["jobid"]) + ".output"
        errfile = str(self.builder.metadata["jobid"]) + ".error"
        self.builder.metadata["outfile"] = os.path.join(self.builder.stage_dir, outfile)
        self.builder.metadata["errfile"] = os.path.join(self.builder.stage_dir, errfile)

        self.logger.debug(
            f"Output file will be written to: {self.builder.metadata['outfile']}"
        )
        self.logger.debug(
            f"Error file will be written to: {self.builder.metadata['errfile']}"
        )
        self.builder.metadata["output"] = read_file(self.builder.metadata["outfile"])
        self.builder.metadata["error"] = read_file(self.builder.metadata["errfile"])

        # 'qstat -lf <jobid>' will get all fields of Job.
        qstat_cmd = f"{self.poll_cmd} -lf {self.builder.metadata['jobid']}"
        self.logger.debug(f"Executing command: {qstat_cmd}")
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

        self.logger.debug(json.dumps(job_record, indent=2))
        self.builder.metadata["job"] = job_record

    def poll(self):
        """This method is responsible for polling Cobalt job, we check the
        job state and existence of output file. If file exists or job is in
        'exiting' stage we set job to 'done' stage and gather results. If job
        is in 'pending' stage we check if job exceeds 'max_pend_time' time limit
        by checking with builder timer attribute using ``start`` and ``stop`` method.
        If job exceeds the time limit job is cancelled.
        """

        self.logger.debug(f"Query Job: {self.builder.metadata['jobid']}")

        # get Job State by running 'qstat -l --header <jobid>'
        qstat_cmd = (
            f"{self.poll_cmd} -l --header State {self.builder.metadata['jobid']}"
        )
        self.logger.debug(f"Executing command: {qstat_cmd}")
        cmd = BuildTestCommand(qstat_cmd)
        cmd.execute()
        output = cmd.get_output()

        output = " ".join(output).strip()

        # Output in format State: <state> so we need to get value of state
        job_state = output.partition(":")[2].strip()

        if job_state:
            self.builder.job_state = job_state

        self.logger.debug(
            "[%s]: JobID %s in %s state ",
            self.builder.metadata["name"],
            self.builder.metadata["jobid"],
            self.builder.job_state,
        )

        # additional check to see if job outputfile is written to file system.
        # If job is in 'exiting' state we assume job is now finished, qstat will remove
        # completed job and it can't be polled so it is likely self.job_state is undefined
        if (
            shutil.which(self.builder.metadata["outfile"])
            or self.builder.job_state == "exiting"
        ):
            self.builder.job_state = "done"
            self.builder.metadata["result"][
                "endtime"
            ] = datetime.datetime.now().strftime("%Y/%m/%d %X")
            self.gather()
            return

        if self.builder.job_state == "pending":
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
        """This method is responsible for moving output and error file in the run
        directory. We need to read <JOBID>.cobaltlog file which contains
        output of exit code. Cobalt doesn't provide any method to retrieve
        exit code using account command (``qstat``) so we need to perform
        regular expression.
        """

        cobaltlog = os.path.join(
            self.builder.stage_dir, str(self.builder.metadata["jobid"]) + ".cobaltlog"
        )
        self.logger.debug(f"Cobalt Log File written to {cobaltlog}")
        if os.path.exists(cobaltlog):
            content = read_file(cobaltlog)
            pattern = r"(exit code of.)(\d+)(\;)"
            # pattern to check in cobalt log file is 'exit code of <CODE>;'
            m = re.search(pattern, content)
            if m:
                self.builder.metadata["result"]["returncode"] = int(m.group(2))
                print(self.builder.metadata["result"]["returncode"])
            else:
                self.logger.debug(
                    f"Error in regular expression: {pattern}. Unable to find returncode please check your cobalt log file"
                )

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
