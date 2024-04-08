"""
BuildExecutor: manager for test executors
"""

import logging
import os
import time

from buildtest.builders.base import BuilderBase
from buildtest.defaults import console
from buildtest.utils.tools import deep_get


class BaseExecutor:
    """The BaseExecutor is an abstract base class for all executors."""

    type = "base"
    default_maxpendtime = 86400

    def __init__(
        self, name, settings, site_configs, timeout=None, account=None, maxpendtime=None
    ):
        """Initiate a base executor, meaning we provide a name (also held
        by the BuildExecutor base that holds it) and the loaded dictionary
        of config opts to parse.

        Args:
            name (str): name of executor
            setting (dict): setting for a given executor defined in configuration file
            site_configs (buildtest.config.SiteConfiguration): Instance of SiteConfiguration class
            timeout (str, optional): Test timeout in number of seconds
            maxpendtime (int, optional): Maximum Pending Time until job is cancelled. The default is 1 day (86400s)
            account (str, optional): Account to use for job submission
            maxpendtime (int, optional): Maximum Pending Time until job is cancelled. The default is 1 day (86400s)
        """

        self.shell = "bash"
        self.logger = logging.getLogger(__name__)
        self.name = name
        self._settings = settings
        self._buildtestsettings = site_configs
        self.timeout = timeout
        self.builders = []
        self.account = account
        self.maxpendtime = maxpendtime

        self.load()
        # the shell type for executors will be bash by default
        # self.shell = "bash"

    def add_builder(self, builder):
        """Add builder object to ``self.builders`` only if its of type BuilderBase"""

        if isinstance(builder, BuilderBase):
            self.builders.append(builder)

    def get_builder(self):
        """Return a list of builders"""
        return self.builders

    def load(self):
        """Load a particular configuration based on the name. This method
        should set defaults for the executor, and will vary based on the
        class.
        """

        self.launcher_opts = self._settings.get("options")
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
            or self.default_maxpendtime
        )

    def run(self):
        """The run step basically runs the build. This is run after setup
        so we are sure that the builder is defined. This is also where
        we set the result to return.
        """
        raise NotImplementedError

    def poll(self, builder):
        builder.job.poll()

        # if job is complete gather job data
        if builder.job.is_complete():
            self.gather(builder)
            return

        builder.stop()

        if builder.job.is_running():
            builder.job.elapsedtime = time.time() - builder.job.starttime
            builder.job.elapsedtime = round(builder.job.elapsedtime, 2)
            if self._cancel_job_if_elapsedtime_exceeds_timeout(builder):
                return

        if builder.job.is_suspended() or builder.job.is_pending():
            if self._cancel_job_if_pendtime_exceeds_maxpendtime(builder):
                return

        builder.start()

    def gather(self, builder):
        """Gather Job detail after completion of job by invoking the builder method ``builder.job.gather()``.
        We retrieve exit code, output file, error file and update builder metadata.

        Args:
            builder (buildtest.buildsystem.base.BuilderBase): An instance object of BuilderBase type
        """

        builder.record_endtime()
        
        builder.job.retrieve_jobdata()
        builder.metadata["job"] = builder.job.jobdata()
        builder.metadata["result"]["returncode"] = builder.job.exitcode()

        self.logger.debug(
            f"[{builder.name}] returncode: {builder.metadata['result']['returncode']}"
        )

        builder.metadata["outfile"] = os.path.join(
            builder.stage_dir, builder.job.output_file()
        )
        builder.metadata["errfile"] = os.path.join(
            builder.stage_dir, builder.job.error_file()
        )
        console.print(f"[blue]{builder}[/]: Job {builder.job.get()} is complete! ")
        builder.post_run_steps()

    def _cancel_job_if_elapsedtime_exceeds_timeout(self, builder):
        if not self.timeout:
            return

        # cancel job when elapsed time exceeds the timeout value.
        if builder.job.elapsedtime > self.timeout:
            builder.job.cancel()
            builder.failed()
            console.print(
                f"[blue]{builder}[/]: [red]Cancelling Job {builder.job.get()} because job exceeds timeout of {self.timeout} sec with current elapsed time of {builder.job.elapsedtime} sec[/red] "
            )

    def _cancel_job_if_pendtime_exceeds_maxpendtime(self, builder):
        builder.job.pendtime = time.time() - builder.job.submittime
        builder.job.pendtime = round(builder.job.pendtime, 2)

        if builder.job.pendtime > self.maxpendtime:
            builder.job.cancel()
            builder.failed()
            console.print(
                f"[blue]{builder}[/]: [red]Cancelling Job {builder.job.get()} because job exceeds max pend time of {self.maxpendtime} sec with current pend time of {builder.job.pendtime} sec[/red] "
            )
            return

    def __str__(self):
        return self.name
        # return "%s.%s" % (self.type, self.name)

    def __repr__(self):
        return self.__str__()
