"""This method implements CobaltExecutor class which is defines how cobalt executor
submit job to Cobalt scheduler."""

import json
import os
import re
import shutil

from buildtest.executors.base import BaseExecutor
from buildtest.exceptions import ExecutorError
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

    def dispatch(self, builder):
        """This method is responsible for dispatching Cobalt job, get JobID
        and start record metadata in builder object. If job failed to submit
        we check returncode and exit with failure. After we submit job, we
        start timer and record when job was submitted and poll job once to get
        job details and store them in builder object.

        :param builder: builder object
        :type builder: BuilderBase, required
        """

        os.chdir(builder.stage_dir)

        batch_cmd = [self.launcher]

        if self.queue:
            batch_cmd += [f"-q {self.queue}"]

        if self.account:
            batch_cmd += [f"--project {self.account}"]

        if self.launcher_opts:
            batch_cmd += [" ".join(self.launcher_opts)]

        batch_cmd += [builder.metadata["testpath"]]
        builder.metadata["command"] = " ".join(batch_cmd)
        self.logger.debug(f"Running Test via command: {builder.metadata['command']}")

        command = BuildTestCommand(builder.metadata["command"])
        command.execute()
        self.start_time(builder)
        builder.start()

        # if qsub job submission returns non-zero exit that means we have failure, exit immediately
        if command.returncode != 0:
            err = f"[{builder.metadata['name']}] failed to submit job with returncode: {command.returncode} \n"
            err += (
                f"[{builder.metadata['name']}] running command: {' '.join(batch_cmd)}"
            )
            raise ExecutorError(err)

        parse_jobid = command.get_output()
        parse_jobid = " ".join(parse_jobid)

        # convert JobID into integer
        builder.metadata["jobid"] = int(parse_jobid)

        builder.job = CobaltJob(builder.metadata["jobid"])

        msg = f"[{builder.metadata['name']}] JobID: {builder.metadata['jobid']} dispatched to scheduler"
        print(msg)
        self.logger.debug(msg)

        # output and error file in format <JOBID>.output and <JOBID>.error we set full path to file. By
        # default Cobalt will write file into current directory where job is submitted. We assume output and error
        # file names are not set in job script
        """ DELETE THIS SECTION
        outfile = str(builder.metadata["jobid"]) + ".output"
        errfile = str(builder.metadata["jobid"]) + ".error"
        builder.metadata["outfile"] = os.path.join(builder.stage_dir, outfile)
        builder.metadata["errfile"] = os.path.join(builder.stage_dir, errfile)
        """
        builder.metadata["outfile"] = os.path.join(
            builder.stage_dir, builder.job.output_file()
        )
        builder.metadata["errfile"] = os.path.join(
            builder.stage_dir, builder.job.error_file()
        )

        self.logger.debug(
            f"Output file will be written to: {builder.metadata['outfile']}"
        )
        self.logger.debug(
            f"Error file will be written to: {builder.metadata['errfile']}"
        )
        """
        # 'qstat -lf <jobid>' will get all fields of Job.
        qstat_cmd = f"{self.poll_cmd} -lf {builder.metadata['jobid']}"
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
        builder.metadata["job"] = job_record
        """
        builder.metadata["job"] = builder.job.gather()
        self.logger.debug(json.dumps(builder.metadata["job"], indent=2))

    def poll(self, builder):
        """This method is responsible for polling Cobalt job, we check the
        job state and existence of output file. If file exists or job is in
        'exiting' stage we set job to 'done' stage and gather results. If job
        is in 'pending' stage we check if job exceeds 'max_pend_time' time limit
        by checking with builder timer attribute using ``start`` and ``stop`` method.
        If job exceeds the time limit job is cancelled.

        :param builder: builder object
        :type builder: BuilderBase, required
        """

        builder.job.poll()
        # Cobalt job can disappear if job is complete so we check if either outputfile exists
        # or job is complete to mark job finished.
        if shutil.which(builder.metadata["outfile"]) or builder.job.is_complete():
            builder.job_state = "exiting"
            self.gather(builder)
            return

        if builder.job.is_pending() or builder.job.is_suspended():
            builder.stop()
            self.logger.debug(f"Time Duration: {builder.duration}")
            self.logger.debug(f"Max Pend Time: {self.max_pend_time}")

            # if timer time is more than requested pend time then cancel job
            if int(builder.duration) > self.max_pend_time:
                builder.job.cancel()
                builder.job_state = builder.job.state()
                print(
                    "Cancelling Job because duration time: {:f} sec exceeds max pend time: {} sec".format(
                        builder.duration, self.max_pend_time
                    )
                )

            builder.start()
        """
        self.logger.debug(f"Query Job: {builder.metadata['jobid']}")

        # get Job State by running 'qstat -l --header <jobid>'
        qstat_cmd = f"{self.poll_cmd} -l --header State {builder.metadata['jobid']}"
        self.logger.debug(f"Executing command: {qstat_cmd}")
        cmd = BuildTestCommand(qstat_cmd)
        cmd.execute()
        output = cmd.get_output()

        output = " ".join(output).strip()

        # Output in format State: <state> so we need to get value of state
        job_state = output.partition(":")[2].strip()

        if job_state:
            builder.job_state = job_state

        self.logger.debug(
            "[%s]: JobID %s in %s state ",
            builder.metadata["name"],
            builder.metadata["jobid"],
            builder.job_state,
        )
        
        
        # additional check to see if job outputfile is written to file system.
        # If job is in 'exiting' state we assume job is now finished, qstat will remove
        # completed job and it can't be polled so it is likely self.job_state is undefined
        if shutil.which(builder.metadata["outfile"]) or builder.job_state == "exiting":
            builder.job_state = "done"
            self.gather(builder)
            return

        if builder.job_state == "pending":
            builder.stop()
            self.logger.debug(f"Time Duration: {builder.duration}")
            self.logger.debug(f"Max Pend Time: {self.max_pend_time}")

            # if timer time is more than requested pend time then cancel job
            if int(builder.duration) > self.max_pend_time:
                self.cancel()
                builder.job_state = "CANCELLED"
                print(
                    "Cancelling Job because duration time: {:f} sec exceeds max pend time: {} sec".format(
                        builder.duration, self.max_pend_time
                    )
                )

            builder.start()
        """

    def gather(self, builder):
        """This method is responsible for moving output and error file in the run
        directory. We need to read <JOBID>.cobaltlog file which contains
        output of exit code. Cobalt doesn't provide any method to retrieve
        exit code using account command (``qstat``) so we need to perform
        regular expression.

        :param builder: builder object
        :type builder: BuilderBase, required
        """

        builder.metadata["output"] = read_file(builder.metadata["outfile"])
        builder.metadata["error"] = read_file(builder.metadata["errfile"])
        cobaltlog = os.path.join(builder.stage_dir, builder.job.cobalt_log())

        self.end_time(builder)

        self.logger.debug(f"Cobalt Log File written to {cobaltlog}")
        if os.path.exists(cobaltlog):
            content = read_file(cobaltlog)
            pattern = r"(exit code of.)(\d+)(\;)"
            # pattern to check in cobalt log file is 'exit code of <CODE>;'
            m = re.search(pattern, content)
            if m:
                builder.metadata["result"]["returncode"] = int(m.group(2))
            else:
                self.logger.debug(
                    f"Error in regular expression: {pattern}. Unable to find returncode please check your cobalt log file"
                )

        self.check_test_state(builder)

    def cancel(self, builder):
        """Cancel Cobalt job using qdel, this operation is performed if job exceeds its ``max_pend_time``

        :param builder: builder object
        :type builder: BuilderBase, required
        """

        query = f"qdel {builder.metadata['jobid']}"

        cmd = BuildTestCommand(query)
        cmd.execute()
        msg = f"Cancelling Job: {builder.metadata['name']} running command: {query}"
        print(msg)
        self.logger.debug(msg)


class CobaltJob(Job):
    def __init__(self, jobID):
        super().__init__(jobID)
        self._outfile = str(jobID) + ".output"
        self._errfile = str(jobID) + ".error"
        self._cobaltlog = str(jobID) + ".cobaltlog"

    def is_pending(self):
        return self._state == "queued"

    def is_running(self):
        return self._state == "running"

    def is_complete(self):
        return self._state == "exiting"

    def is_suspended(self):
        return self._state == "user_hold"

    def is_cancelled(self):
        return self._state == "cancelled"

    def poll(self):

        # get Job State by running 'qstat -l --header <jobid>'
        query = f"{self.poll_cmd} -l --header State {builder.metadata['jobid']}"
        logger.debug(f"Executing command: {query}")
        cmd = BuildTestCommand(qstat_cmd)
        cmd.execute()
        output = cmd.get_output()

        output = " ".join(output).strip()

        # Output in format State: <state> so we need to get value of state
        job_state = output.partition(":")[2].strip()

        if job_state:
            builder.job_state = job_state

    def gather(self):
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
        """Cancel Cobalt job. Upon cancelling job, we can't retrieve job record via `qstat` to get its state therefore, we
        make up an arbitrary state name ``cancelled`` and assign this to `self._state`.
        """

        query = f"qdel {self.jobid}"
        logger.debug(f"Cancelling job {self.jobid} by running: {query}")
        cmd = BuildTestCommand(query)
        cmd.execute()

        self._state = "cancelled"

    def cobalt_log(self):
        return self._cobaltlog

    def output_file(self):
        return self._outfile

    def error_file(self):
        return self._errfile

    def exitcode(self):
        return self._exitcode
