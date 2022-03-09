"""This method implements CobaltExecutor class which is defines how cobalt executor
submit job to Cobalt scheduler."""
import json
import logging
import os
import re
import shutil
import time

from buildtest.defaults import console
from buildtest.exceptions import RuntimeFailure
from buildtest.executors.base import BaseExecutor
from buildtest.scheduler.cobalt import CobaltJob
from buildtest.utils.file import is_file, read_file
from buildtest.utils.tools import deep_get

logger = logging.getLogger(__name__)


class CobaltExecutor(BaseExecutor):
    """The CobaltExecutor class is responsible for submitting jobs to Cobalt Scheduler.
    The class implements the following methods:

    - **load**: load Cobalt executors from configuration file
    - **dispatch**: submit Cobalt job to scheduler
    - **poll**: poll Cobalt job via qstat and retrieve job state
    - **gather**: gather job record including output, error, exit code
    """

    type = "cobalt"
    launcher = "qsub"

    def __init__(self, name, settings, site_configs, account=None, maxpendtime=None):

        self.account = account
        self.maxpendtime = maxpendtime
        super().__init__(name, settings, site_configs)

    def load(self):
        """Load the a Cobalt executor configuration from buildtest settings."""

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

    def launcher_command(self, numprocs, numnodes):

        batch_cmd = [self.launcher]

        if self.queue:
            batch_cmd += [f"-q {self.queue}"]

        if self.account:
            batch_cmd += [f"--project {self.account}"]

        if numprocs:
            batch_cmd += [f"--proccount={self.numprocs}"]

        if numnodes:
            batch_cmd += [f"--nodecount={self.numnodes}"]

        if self.launcher_opts:
            batch_cmd += [" ".join(self.launcher_opts)]

        return batch_cmd

    def run(self, builder):
        """This method is responsible for dispatching job to Cobalt Scheduler by invoking ``builder.run()``
        which runs the build script. If job is submitted to scheduler, we get the JobID and pass this to
        ``CobaltJob`` class. At job submission, cobalt will report the output and error file which can be retrieved
        using **qstat**. We retrieve the cobalt job record using ``builder.job.gather()``.

        Args:
            builder (buildtest.buildsystem.base.BuilderBase): An instance object of BuilderBase type
        """

        os.chdir(builder.stage_dir)

        cmd = f"bash {self._bashopts} {os.path.basename(builder.build_script)}"

        try:
            command = builder.run(cmd)
        except RuntimeFailure as err:
            self.logger.error(err)
            return

        out = command.get_output()
        out = " ".join(out)

        # convert JobID into integer
        job_id = int(out)
        builder.metadata["jobid"] = job_id

        builder.job = CobaltJob(job_id)

        msg = f"[blue]{builder}[/]: JobID: {builder.metadata['jobid']} dispatched to scheduler"
        console.print(msg)
        logger.debug(msg)

        # output and error file in format <JOBID>.output and <JOBID>.error we set full path to file. By
        # default Cobalt will write file into current directory where job is submitted. We assume output and error
        # file names are not set in job script

        builder.metadata["outfile"] = os.path.join(
            builder.stage_dir, builder.job.output_file()
        )
        builder.metadata["errfile"] = os.path.join(
            builder.stage_dir, builder.job.error_file()
        )

        logger.debug(f"Output file will be written to: {builder.metadata['outfile']}")
        logger.debug(f"Error file will be written to: {builder.metadata['errfile']}")

        builder.metadata["job"] = builder.job.gather()
        logger.debug(json.dumps(builder.metadata["job"], indent=2))

        return builder

    def poll(self, builder):
        """This method is responsible for polling Cobalt job by invoking the builder method
        ``builder.job.poll()``.  We check the job state and existence of output file. If file
        exists or job is complete, we gather the results and return from function. If job
        is pending we check if job time exceeds ``maxpendtime`` time limit and cancel job.

        Args:
            builder (buildtest.buildsystem.base.BuilderBase): An instance object of BuilderBase type
        """

        builder.job.poll()
        # Cobalt job can disappear if job is complete so we check when outputfile exists as an indicator when job is finished
        if is_file(builder.metadata["outfile"]) or builder.job.is_complete():
            # builder.job_state = "exiting"
            self.gather(builder)
            return

        builder.stop()
        # if job is pending or suspended check if builder timer duration exceeds maxpendtime if so cancel job
        if builder.job.is_pending() or builder.job.is_suspended():
            logger.debug(f"Time Duration: {builder.duration}")
            logger.debug(f"Max Pend Time: {self.maxpendtime}")

            # if timer time is more than requested pend time then cancel job
            if int(builder.timer.duration()) > self.maxpendtime:
                builder.job.cancel()
                builder.failed()
                console.print(
                    f"[blue]{builder}[/]: [red]Cancelling Job {builder.job.get()} because job exceeds max pend time of {self.maxpendtime} sec with current pend time of {builder.timer.duration()} sec[/red] "
                )
            return

        builder.start()

    def gather(self, builder):
        """This method is responsible for moving output and error file in the run
        directory. We need to read ``<JOBID>.cobaltlog`` file which contains
        output of exit code by performing a regular expression ``(exit code of.)(\d+)(\;)``.
        The cobalt log file will contain a line: **task completed normally with an exit code of 0; initiating job cleanup and removal**

        Args:
            builder (buildtest.buildsystem.base.BuilderBase): An instance object of BuilderBase type
        """

        builder.record_endtime()
        # The cobalt job will write output and error file after job completes, there is a few second delay before file comes. Hence
        # stay in while loop and sleep for every 5 second until we find both files in filesystem
        while True:
            interval = 5
            if is_file(builder.metadata["outfile"]) and is_file(
                builder.metadata["errfile"]
            ):
                break
            logger.debug(
                f"Sleeping {interval} seconds and waiting for Cobalt Scheduler to write output and error file"
            )
            time.sleep(interval)

        # builder.metadata["output"] = read_file(builder.metadata["outfile"])
        # builder.metadata["error"] = read_file(builder.metadata["errfile"])

        cobaltlog = os.path.join(builder.stage_dir, builder.job.cobalt_log())

        logger.debug(f"Cobalt Log File written to {cobaltlog}")

        # if os.path.exists(cobaltlog):
        content = read_file(cobaltlog)
        pattern = r"(exit code of.)(\d+)(\;)"
        # pattern to check in cobalt log file is 'exit code of <CODE>;'
        m = re.search(pattern, content)
        if m:
            rc = int(m.group(2))
            builder.metadata["result"]["returncode"] = rc
            logger.debug(
                f"Test: {builder.name} got returncode: {rc} from JobID: {builder.job.jobid}"
            )
        else:
            logger.debug(
                f"Error in regular expression: '{pattern}'. Unable to find returncode please check your cobalt log file"
            )

        shutil.copy2(
            cobaltlog, os.path.join(builder.test_root, os.path.basename(cobaltlog))
        )
        logger.debug(
            f"Copying cobalt log file: {cobaltlog} to {os.path.join(builder.test_root,os.path.basename(cobaltlog))}"
        )

        console.print(f"[blue]{builder}[/]: Job {builder.job.get()} is complete! ")

        builder.post_run_steps()
