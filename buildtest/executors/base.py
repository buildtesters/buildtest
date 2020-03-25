"""
BuildExecutor: manager for test executors
Copyright (C) 2020 Vanessa Sochat. 
"""

import os
import sys

from buildtest.config import config_opts
from buildtest.log import init_logfile, init_log


class BuildExecutor:
    """A BuildExector is a base class some type of executor, defined under
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

           config_opts: the validated config opts provided by buildtest.
        """
        self.executors = {}

        # Load the executors
        for name, executor in config_opts.get("executors", {}).items():
            if executor["type"] == "local":
                self.executors[name] = LocalExecutor(name, executor)
            elif executor["type"] == "slurm":
                self.executors[name] = SlurmExecutor(name, executor)

    def __str__(self):
        return "[buildtest-executor]"

    def __repr__(self):
        return "[buildtest-executor]"

    def get(self, name):
        """Given the name of an executor return the executor for running 
           a buildtest build.
        """
        return self.executors.get(name)


class BaseExecutor:
    """The BaseExecutor is an abstract base class for all executors
    """

    def __init__(self, name, settings):
        """initiate a base executor, meaning we provide a name (also held
           by the BuildExecutor base that holds it) and the loaded dictionary
           of config opts to parse.

           name: a name for the base executor and key provided in the configuration file
           settings: the original config opts to extract variables from.
        """

        self.name = name
        self._settings = settings

        # Set defaults based on provided config
        self.type = self._settings.get("type")
        self.load(name)

    def load(self, name=None):
        """Load a particular configuration based on the name. This method
           should set defaults for the executor, and will vary based on the
           class.
        """
        pass

    def __str__(self):
        return "[executor-%s-%s]" % (self.type, self.name)

    def __repr__(self):
        return self.__str__()


class LocalExecutor(BaseExecutor):
    type = "local"


class SlurmExecutor(BaseExecutor):
    type = "slurm"

    def load(self, name):
        """Load the executor preferences from the provided config, which is
           added and indexed with "name." For slurm we look for the following
           in vars:

           launcher: defaults to sbatch
        """
        variables = self._settings.get("vars", {})
        self.launcher = variables.get("launcher", "sbatch")
