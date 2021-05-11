"""
This module is responsible for setup of executors defined in buildtest
configuration. The BuildExecutor class initializes the executors and chooses the
executor class (LocalExecutor, LSFExecutor, SlurmExecutor, CobaltExecutor) to call depending
on executor name.
"""

import logging
import os

from buildtest.defaults import BUILDTEST_EXECUTOR_DIR
from buildtest.executors.base import BaseExecutor
from buildtest.executors.cobalt import CobaltExecutor
from buildtest.executors.local import LocalExecutor
from buildtest.executors.lsf import LSFExecutor
from buildtest.executors.slurm import SlurmExecutor
from buildtest.executors.pbs import PBSExecutor
from buildtest.exceptions import ExecutorError
from buildtest.utils.file import create_dir, write_file


class BuildExecutor:
    """A BuildExecutor is responsible for initialing executors from buildtest configuration
    file which provides a list of executors. This class keeps track of all executors and provides
    the following methods:

    **setup**: This method will  write executor's ``before_script.sh`` and ``after_script.sh`` file that is sourced in each test upon calling executor.
    **run**: Responsible for invoking executor's **run** method based on builder object which is of type BuilderBase.
    **poll**: This is responsible for invoking ``poll`` method for corresponding executor from the builder object by checking job state
    """

    def __init__(self, site_config, max_pend_time=None):
        """Initialize executors, meaning that we provide the buildtest
        configuration that are validated, and can instantiate
        each executor to be available.

        :param site_config: the site configuration for buildtest.
        :type site_config: SiteConfiguration class, required
        """

        self.executors = {}
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Getting Executors from buildtest settings")

        if site_config.localexecutors:
            for name in site_config.localexecutors:
                self.executors[f"{site_config.name}.local.{name}"] = LocalExecutor(
                    f"{site_config.name}.local.{name}",
                    site_config.target_config["executors"]["local"][name],
                    site_config,
                )

        if site_config.slurmexecutors:
            for name in site_config.slurmexecutors:
                self.executors[f"{site_config.name}.slurm.{name}"] = SlurmExecutor(
                    f"{site_config.name}.slurm.{name}",
                    site_config.target_config["executors"]["slurm"][name],
                    site_config,
                    max_pend_time,
                )

        if site_config.lsfexecutors:
            for name in site_config.lsfexecutors:
                self.executors[f"{site_config.name}.lsf.{name}"] = LSFExecutor(
                    f"{site_config.name}.lsf.{name}",
                    site_config.target_config["executors"]["lsf"][name],
                    site_config,
                    max_pend_time,
                )

        if site_config.cobaltexecutors:
            for name in site_config.cobaltexecutors:
                self.executors[f"{site_config.name}.cobalt.{name}"] = CobaltExecutor(
                    f"{site_config.name}.cobalt.{name}",
                    site_config.target_config["executors"]["cobalt"][name],
                    site_config,
                    max_pend_time,
                )

        if site_config.pbsexecutors:
            for name in site_config.pbsexecutors:
                self.executors[f"{site_config.name}.pbs.{name}"] = PBSExecutor(
                    f"{site_config.name}.pbs.{name}",
                    site_config.target_config["executors"]["pbs"][name],
                    site_config,
                    max_pend_time,
                )
        self.setup()

    def __str__(self):
        return "[buildtest-executor]"

    def __repr__(self):
        return "[buildtest-executor]"

    def list_executors(self):
        return list(self.executors.keys())

    def get(self, name):
        """Given the name of an executor return the executor for running
        a buildtest build, or get the default.
        """
        return self.executors.get(name)

    def _choose_executor(self, builder):
        """Choose executor is called at the onset of a run or poll stage. We
        look at the builder metadata to determine if a default
        is set for the executor, and fall back to the default.

        :param builder: the builder with the loaded Buildspec.
        :type builder: BuilderBase (subclass), required.
        """

        # Get the executor by name, and add the builder to it
        executor = self.executors.get(builder.executor)
        if not isinstance(executor, BaseExecutor):
            raise ExecutorError(
                f"{executor} is not a valid executor because it is not of type BaseExecutor class."
            )

        executor.builder = builder
        return executor

    def setup(self):
        """This method creates directory ``var/executors/<executor-name>``
        for every executor defined in buildtest configuration and write scripts
        before_script.sh and after_script.sh if the fields ``before_script``
        and ``after_script`` are specified in executor section. This method
        is called after executors are initialized in the class **__init__**
        method.
        """

        for executor_name in self.executors.keys():
            create_dir(os.path.join(BUILDTEST_EXECUTOR_DIR, executor_name))
            executor_settings = self.executors[executor_name]._settings

            # if before_script field defined in executor section write content to var/executors/<executor>/before_script.sh
            file = os.path.join(
                BUILDTEST_EXECUTOR_DIR, executor_name, "before_script.sh"
            )
            content = executor_settings.get("before_script") or ""
            write_file(file, content)

            # after_script field defined in executor section write content to var/executors/<executor>/after_script.sh
            file = os.path.join(
                BUILDTEST_EXECUTOR_DIR, executor_name, "after_script.sh"
            )
            content = executor_settings.get("after_script") or ""
            write_file(file, content)

    def run(self, builder):
        """Given a BuilderBase (subclass) go through the
        steps defined for the executor to run the build. This should
        be instantiated by the subclass. For a simple script run, we expect a
        setup, build, and finish.

        :param builder: the builder with the loaded test configuration.
        :type builder: BuilderBase (subclass), required.
        """
        executor = self._choose_executor(builder)
        # The run stage for LocalExecutor is to invoke run method
        if executor.type == "local":
            executor.run(builder)
        # The run stage for batch executor (Slurm, LSF, Cobalt, PBS) executor is to invoke dispatch method
        elif executor.type in ["slurm", "lsf", "cobalt", "pbs"]:
            executor.dispatch(builder)
        else:
            raise ExecutorError(
                f"Invalid executor type: {executor.type} for executor: {executor.name}. Please check your configuration file"
            )

    def poll(self, builder):
        """Poll all jobs for batch executors (LSF, Slurm, Cobalt, PBS). For slurm we poll
        until job is in ``PENDING`` or ``RUNNING`` state. If Slurm job is in
        ``FAILED`` or ``COMPLETED`` state we assume job is finished and we gather
        results. If its in any other state we ignore job and return out of method.

        For LSF jobs we poll job if it's in ``PEND`` or ``RUN`` state, if its in
        ``DONE`` state we gather results, otherwise we assume job is incomplete
        and return with ``ignore_job`` set to ``True``. This informs buildtest
        to ignore job when showing report.

        For Cobalt jobs, we poll if its in ``starting``, ``queued``, or ``running``
        state. For Cobalt jobs we cannot query job after its complete since JobID
        is no longer present in queuing system. Therefore, for when job is complete
        which is ``done`` or ``exiting`` state, we mark job is complete.

        For PBS jobs we poll job if its in queued or running stage which corresponds
        to ``Q`` and ``R`` in job stage. If job is finished (``F``) we gather results. If job
        is in ``H`` stage we automatically cancel job otherwise we ignore job and mark job complete.

        :param builder: an instance of BuilderBase (subclass)
        :type builder: BuilderBase (subclass), required
        :return: Return a dictionary containing poll information
        :rtype: dict
        """

        poll_info = {
            "job_complete": False,  # indicate job is not complete and requires polling
            "ignore_job": False,  # indicate job should be ignored
        }
        executor = self._choose_executor(builder)
        # if builder is local executor we shouldn't be polling so we set job to
        # complete and return
        if executor.type == "local":
            poll_info["job_complete"] = True
            return poll_info

        # poll Slurm job
        if executor.type == "slurm":
            if (
                builder.job.is_pending()
                or builder.job.is_suspended()
                or builder.job.is_running()
                or not builder.job.state()
            ):
                executor.poll(builder)
            elif builder.job.complete():
                executor.gather(builder)
                poll_info["job_complete"] = True
            else:
                poll_info["job_complete"] = True
                poll_info["ignore_job"] = True

        # poll LSF job
        elif executor.type == "lsf":
            if (
                builder.job.is_pending()
                or builder.job.is_running()
                or builder.job.is_suspended()
                or not builder.job.state()
            ):
                executor.poll(builder)
            elif builder.job.is_complete():
                executor.gather(builder)
                poll_info["job_complete"] = True
            else:
                poll_info["job_complete"] = True
                poll_info["ignore_job"] = True

        elif executor.type == "cobalt":
            if (
                builder.job.is_pending()
                or builder.job.is_running()
                or builder.job.is_suspended()
                or not builder.job.state()
            ):
                executor.poll(builder)
            elif builder.job.is_complete():
                poll_info["job_complete"] = True
            elif builder.job.is_cancelled():
                poll_info["job_complete"] = True
                poll_info["ignore_job"] = True

        elif executor.type == "pbs":
            if (
                builder.job.is_pending()
                or builder.job.is_running()
                or builder.job.is_suspended()
                or not builder.job.state()
            ):
                executor.poll(builder)
            elif builder.job.is_complete():
                executor.gather(builder)
                poll_info["job_complete"] = True
            else:
                poll_info["job_complete"] = True
                poll_info["ignore_job"] = True

        return poll_info
