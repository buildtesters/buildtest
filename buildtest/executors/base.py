"""
BuildExecutor: manager for test executors
Copyright (C) 2020 Vanessa Sochat. 
"""

import os
import sys

from buildtest.config import config_opts


class BuildExecutor:
    """A BuildExector is a base class some type of executor, defined under
       the buildtest/settings/default-config.json schema. For example,
       the types "local" and "slurm" would map to `LocalExecutor` and
       `SlurmExecutor` here, each expecting a particular set of
       variables under the config options. If options are required
       and not provided, we exit on error. If they are optional and not
       provided, we use reasonable defaults.
    """

    def __init__(self, config_opts, default=None):
        """initiate executors, meaning that we provide the config_opts
           that are validated, and can instantiate each executor to be available
           
           :param config_opts: the validated config opts provided by buildtest.
           :type config_opts: dictionary
           :param default: the name of the default executor. If not set (or undefined)
           we fall back to buildtest defaults (see set_default).
           :type default: str
        """
        self.executors = {}

        # Load the executors
        for name, executor in config_opts.get("executors", {}).items():
            if executor["type"] == "local":
                self.executors[name] = LocalExecutor(name, executor)
            elif executor["type"] == "slurm":
                self.executors[name] = SlurmExecutor(name, executor)

        self.set_default(default)

    def __str__(self):
        return "[buildtest-executor]"

    def __repr__(self):
        return "[buildtest-executor]"

    def get(self, name):
        """Given the name of an executor return the executor for running 
           a buildtest build, or get the default.
        """
        return self.executors.get(name) or self.executors.get("default")

    def _choose_executor(self, builder):
        """Choose executor is called at the onset of a run or dryrun. We
           look at the builder metadata to determine if a default
           is set for the executor, and fall back to the default.

           :param builder: the builder with the loaded test configuration.
           :type builder: buildtest.buildsystem.BuilderBase (or subclass).
        """
        executor = builder.metadata.get("executor", "default")

        # The executor (or a default) must be define
        if executor not in self.executors:
            builder.logger.warning(
                "executor %s is not defined in default.yml" % executor
            )
            sys.exit(1)

        # Get the executor by name, and add the builder to it
        executor = self.executors.get(executor)
        executor.builder = builder
        return executor

    def dry_run(self, builder):
        """A dry run typically includes all of the steps up to run

           :param builder: the builder with the loaded test configuration.
           :type builder: buildtest.buildsystem.BuilderBase (or subclass).
        """
        # Choose the executor based on the builder provided
        executor = self._choose_executor(builder)

        # Run each step defined for dry run
        for step in executor.dryrun_steps:
            if getattr(executor, step, None):
                getattr(executor, step)()
        return executor.result

    def run(self, builder):
        """Given a buildtest.buildsystem.BuildConfig (subclass) go through the
           steps defined for the executor to run the build. This should
           be instantiated by the subclass. For a simple script run, we expect a 
           setup, build, and finish.

           :param builder: the builder with the loaded test configuration.
           :type builder: buildtest.buildsystem.BuilderBase (or subclass).
        """
        executor = self._choose_executor(builder)

        # Run each step defined for dry run
        for step in executor.steps:
            if getattr(executor, step, None):
                executor.builder.logger.debug(
                    "Running %s for executor %s" % (step, executor)
                )
                getattr(executor, step)()
        return executor.result

    def set_default(self, name=None):
        """Set a particular name as the default executor (defaults to default).
           In the case that no executors are defined, we return a base (local)
           executor. If executors are defined, we return the first in the list.

           :param name: the name for the key to set as default, if it exists.
           :type name: string
        """

        # If a default is not defined
        if "default" not in self.executors:

            # If no executors are defined, return a base (local)
            if not self.executors:
                self.executors["default"] = BaseExecutor("default", {})

            # Otherwise return the first in the list
            else:
                if name in self.executors:
                    self.executors["default"] = self.executors[name]
                else:
                    self.executors["default"] = list(self.executors.values())[0]


class BaseExecutor:
    """The BaseExecutor is an abstract base class for all executors. All
       executors must have a listing of steps and dryrun_steps
    """

    steps = ["setup", "run"]
    dryrun_steps = ["setup", "dry"]
    type = "base"

    def __init__(self, name, settings):
        """Initiate a base executor, meaning we provide a name (also held
           by the BuildExecutor base that holds it) and the loaded dictionary
           of config opts to parse.

           :param name: a name for the base executor and key provided in the configuration file
           :type name: string (required)
           :param settings: the original config opts to extract variables from.
           :type settings: dict (required)
           :param builder: the builder object for the executor to control.
           :type builder: buildtest.buildsystem.base.BuilderBase (or subclass).
        """

        self.name = name
        self._settings = settings
        self.load(name)
        self.builder = None
        self.result = {}

    def load(self, name=None):
        """Load a particular configuration based on the name. This method
           should set defaults for the executor, and will vary based on the
           class.
        """
        pass

    def setup(self):
        """Setup the executor, meaning we check that the builder is defined,
           the only step needed for a local (base) executor.
        """
        print(self.builder)
        if not self.builder:
            sys.exit("Builder is not defined for executor.")

    def run(self):
        """The run step basically runs the build. This is run after setup
           so we are sure that the builder is defined. This is also where
           we set the result to return.
        """
        self.result = self.builder.run()

    def dryrun(self):
        """The dry run step defines the result based on a dry run.
        """
        self.result = self.builder.dry_run()

    def __str__(self):
        return "[executor-%s-%s]" % (self.type, self.name)

    def __repr__(self):
        return self.__str__()


class LocalExecutor(BaseExecutor):
    type = "local"


class SlurmExecutor(BaseExecutor):
    """The slurm executor is optimized to setup, run, and check jobs, so it
       has subclass functions to handle these operations. This code is not
       yet written by will be done so by 

       setup: write slurm job scripts
       check: check if slurm partition is available for accepting jobs.
       dispatch: dispatch jobs to scheduler
       poll: wait for jobs to finish
       gather: gather all job data, exit codes and output
       close: clean up any generated files
    """

    type = "slurm"
    steps = ["setup", "check", "dispatch", "poll", "gather", "close"]

    def load(self, name):
        """Load the executor preferences from the provided config, which is
           added and indexed with "name." For slurm we look for the following
           in vars:

           :param launcher: defaults to sbatch
           :type launcher: string
        """

        self.launcher = self._settings.get("launcher", "sbatch")
