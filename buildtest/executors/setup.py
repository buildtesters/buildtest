"""
This module is responsible for setup of executors defined in buildtest
configuration. The BuildExecutor class initializes the executors and chooses the
executor class (LocalExecutor, LSFExecutor, SlurmExecutor) to call depending
on executor name.
"""

import logging
import os
import sys

from buildtest.defaults import BUILDTEST_SETTINGS_FILE, executor_root
from buildtest.executors.base import SSHExecutor
from buildtest.executors.local import LocalExecutor
from buildtest.executors.lsf import LSFExecutor
from buildtest.executors.slurm import SlurmExecutor
from buildtest.utils.file import create_dir, write_file


class BuildExecutor:
    """A BuildExecutor is a base class some type of executor, defined under
       the buildtest/settings/default-config.json schema. For example,
       the types "local" and "slurm" would map to `LocalExecutor` and
       `SlurmExecutor` here, each expecting a particular set of
       variables under the config options. If options are required
       and not provided, we exit on error. If they are optional and not
       provided, we use reasonable defaults.
    """

    def __init__(self, config_opts):
        """initiate executors, meaning that we provide the config_opts
           that are validated, and can instantiate each executor to be available

           Parameters:

           :param config_opts: the validated config opts provided by buildtest.
           :type config_opts: dictionary, required
        """

        self.executors = {}
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Getting Executors from buildtest settings")

        for name in config_opts["executors"].get("local", {}).keys():
            self.executors[f"local.{name}"] = LocalExecutor(
                name, config_opts["executors"]["local"][name], config_opts
            )

        for name in config_opts["executors"].get("ssh", {}).keys():
            self.executors[f"ssh.{name}"] = SSHExecutor(
                name, config_opts["executors"]["ssh"][name], config_opts
            )

        for name in config_opts["executors"].get("slurm", {}).keys():
            self.executors[f"slurm.{name}"] = SlurmExecutor(
                name, config_opts["executors"]["slurm"][name], config_opts
            )

        for name in config_opts["executors"].get("lsf", {}).keys():
            self.executors[f"lsf.{name}"] = LSFExecutor(
                name, config_opts["executors"]["lsf"][name], config_opts
            )

        self.setup()

    def __str__(self):
        return "[buildtest-executor]"

    def __repr__(self):
        return "[buildtest-executor]"

    def get(self, name):
        """Given the name of an executor return the executor for running
           a buildtest build, or get the default.
        """
        return self.executors.get(name)

    def _choose_executor(self, builder):
        """Choose executor is called at the onset of a run or dryrun. We
           look at the builder metadata to determine if a default
           is set for the executor, and fall back to the default.

           Parameters:

           :param builder: the builder with the loaded Buildspec.
           :type builder: buildtest.buildsystem.BuilderBase (or subclass).
        """

        executor = builder.metadata.get("recipe").get("executor")
        # if executor not defined in buildspec we raise an error
        if not executor:
            msg = "[%s]: 'executor' key not defined in buildspec: %s" % (
                builder.metadata["name"],
                builder.metadata["buildspec"],
            )
            builder.logger.error(msg)
            builder.logger.debug("test: %s", builder.metadata["recipe"])
            sys.exit(msg)

        # The executor (or a default) must be define
        if executor not in self.executors:
            msg = "[%s]: executor %s is not defined in %s" % (
                builder.metadata["name"],
                executor,
                BUILDTEST_SETTINGS_FILE,
            )
            builder.logger.error(msg)
            sys.exit(msg)

        # Get the executor by name, and add the builder to it
        executor = self.executors.get(executor)
        executor.builder = builder
        return executor

    def setup(self):
        """
        This method creates directory ``var/executors/<executor-name>`` for every
        executor defined in buildtest configuration and write scripts before_script.sh
        and after_script.sh if the fields ``before_script`` and ``after_script``
        defined in executor. This method is called after executors are initialized
        in the class __init__ method
        """

        for executor_name in self.executors.keys():
            create_dir(os.path.join(executor_root, executor_name))
            executor_settings = self.executors[executor_name]._settings
            # if before_script field defined in executor section write content to var/executors/<executor>/before_script.sh

            file = os.path.join(executor_root, executor_name, "before_script.sh")
            content = executor_settings.get("before_script") or ""
            write_file(file, content)

            # after_script field defined in executor section write content to var/executors/<executor>/after_script.sh
            file = os.path.join(executor_root, executor_name, "after_script.sh")
            content = executor_settings.get("after_script") or ""
            write_file(file, content)

    def run(self, builder):
        """Given a buildtest.buildsystem.BuildspecParser (subclass) go through the
           steps defined for the executor to run the build. This should
           be instantiated by the subclass. For a simple script run, we expect a
           setup, build, and finish.

           :param builder: the builder with the loaded test configuration.
           :type builder: buildtest.buildsystem.BuilderBase (or subclass).
        """
        executor = self._choose_executor(builder)

        if executor.type == "local":
            executor.run()
        elif executor.type in ["slurm", "lsf"]:
            executor.dispatch()

        return executor.result

    def poll(self, builder):

        executor = self._choose_executor(builder)
        if executor.type == "type":
            return True

        # poll slurm job
        if executor.type == "slurm":
            # only poll job if its in PENDING or RUNNING state
            if executor.job_state in ["PENDING", "RUNNING"] or not executor.job_state:
                executor.poll()
            else:
                executor.gather()
                return True

        elif executor.type == "lsf":
            # only poll job if its in PENDING or RUNNING state
            if executor.job_state in ["PEND", "RUN"] or not executor.job_state:
                executor.poll()
            else:
                executor.gather()
                return True

        return False
