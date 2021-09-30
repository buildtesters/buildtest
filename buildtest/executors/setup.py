"""
This module is responsible for setup of executors defined in buildtest
configuration. The BuildExecutor class initializes the executors and chooses the
executor class (LocalExecutor, LSFExecutor, SlurmExecutor, CobaltExecutor) to call depending
on executor name.
"""

import logging
import multiprocessing as mp
import os

from buildtest.buildsystem.base import BuilderBase
from buildtest.defaults import BUILDTEST_EXECUTOR_DIR, console
from buildtest.exceptions import ExecutorError
from buildtest.executors.base import BaseExecutor
from buildtest.executors.cobalt import CobaltExecutor
from buildtest.executors.local import LocalExecutor
from buildtest.executors.lsf import LSFExecutor
from buildtest.executors.pbs import PBSExecutor
from buildtest.executors.slurm import SlurmExecutor
from buildtest.utils.file import create_dir, write_file

logger = logging.getLogger(__name__)


class BuildExecutor:
    """A BuildExecutor is responsible for initialing executors from buildtest configuration
    file which provides a list of executors. This class keeps track of all executors and provides
    the following methods:

    - **setup**: This method will  write executor's ``before_script.sh``  that is sourced in each test upon calling executor.
    - **run**: Responsible for invoking executor's **run** method based on builder object which is of type BuilderBase.
    - **poll**: This is responsible for invoking ``poll`` method for corresponding executor from the builder object by checking job state
    """

    def __init__(self, site_config, account=None, max_pend_time=None):
        """Initialize executors, meaning that we provide the buildtest
        configuration that are validated, and can instantiate
        each executor to be available.

        Args:
            site_config (buildtest.config.SiteConfiguration): instance of SiteConfiguration class that has the buildtest configuration
            account (str, optional): pass account name to charge batch jobs.
            max_pend_time (int, optional): maximum pend time in second until job is cancelled.
        """

        # stores a list of builders objects
        self.builders = []

        # store a list of valid builders
        self.valid_builders = []

        self.executors = {}
        logger.debug("Getting Executors from buildtest settings")

        if site_config.valid_executors["local"]:
            for name in site_config.valid_executors["local"].keys():
                self.executors[name] = LocalExecutor(
                    name=name,
                    settings=site_config.valid_executors["local"][name]["setting"],
                    site_configs=site_config,
                )

        if site_config.valid_executors["slurm"]:
            for name in site_config.valid_executors["slurm"]:
                self.executors[name] = SlurmExecutor(
                    name=name,
                    account=account,
                    settings=site_config.valid_executors["slurm"][name]["setting"],
                    site_configs=site_config,
                    max_pend_time=max_pend_time,
                )

        if site_config.valid_executors["lsf"]:
            for name in site_config.valid_executors["lsf"]:
                self.executors[name] = LSFExecutor(
                    name=name,
                    account=account,
                    settings=site_config.valid_executors["lsf"][name]["setting"],
                    site_configs=site_config,
                    max_pend_time=max_pend_time,
                )

        if site_config.valid_executors["pbs"]:
            for name in site_config.valid_executors["pbs"]:
                self.executors[name] = PBSExecutor(
                    name=name,
                    account=account,
                    settings=site_config.valid_executors["pbs"][name]["setting"],
                    site_configs=site_config,
                    max_pend_time=max_pend_time,
                )

        if site_config.valid_executors["cobalt"]:
            for name in site_config.valid_executors["cobalt"]:
                self.executors[name] = CobaltExecutor(
                    name=name,
                    account=account,
                    settings=site_config.valid_executors["cobalt"][name]["setting"],
                    site_configs=site_config,
                    max_pend_time=max_pend_time,
                )
        self.setup()

    def __str__(self):
        return "[buildtest-executor]"

    def __repr__(self):
        return "[buildtest-executor]"

    def list_executors(self):
        return list(self.executors.keys())

    def is_local(self, executor_type):
        return executor_type == "local"

    def is_slurm(self, executor_type):
        return executor_type == "slurm"

    def is_lsf(self, executor_type):
        return executor_type == "lsf"

    def is_pbs(self, executor_type):
        return executor_type == "pbs"

    def is_cobalt(self, executor_type):
        return executor_type == "cobalt"

    def get(self, name):
        """Given the name of an executor return the executor object which is of subclass of `BaseExecutor`"""
        return self.executors.get(name)

    def _choose_executor(self, builder):
        """Choose executor is called at the onset of a run and poll stage. Given a builder
        object we retrieve the executor property ``builder.executor`` of the builder and check if
        there is an executor object and of type `BaseExecutor`.

        Args:
            builder (buildtest.buildsystem.base.BuilderBase): An instance object of BuilderBase type
        """

        # Get the executor by name, and add the builder to it
        executor = self.executors.get(builder.executor)
        if not isinstance(executor, BaseExecutor):
            raise ExecutorError(
                f"{executor} is not a valid executor because it is not of type BaseExecutor class."
            )

        return executor

    def setup(self):
        """This method creates directory ``var/executors/<executor-name>`` for every executor defined
        in buildtest configuration and write scripts `before_script.sh` if the field ``before_script``
        is specified in executor section. This method is called after executors are initialized in the
        class **__init__** method.
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

    def load_builders(self, builders):
        """Adds builder objects into self.builders class variable. This method will only add objects that are instance of BuilderBase class.

        Args:
            builder (buildtest.buildsystem.base.BuilderBase): An instance object of BuilderBase type
        """
        for builder in builders:
            # only add items that are of class BuilderBase
            if not isinstance(builder, BuilderBase):
                continue

            executor = self._choose_executor(builder)
            executor.add_builder(builder)

            self.builders.append(builder)

    def run(self):
        """This method is responsible for running the build script for each builder async and
        gather the results. We setup a pool of worker settings by invoking ``multiprocessing.pool.Pool``
        and use `multiprocessing.pool.Pool.apply_sync() <https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool.apply_async>`_
        method for running test async which returns
        an object of type `multiprocessing.pool.AsyncResult <https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.AsyncResult>`_
        which holds the result. Next we wait for results to arrive using `multiprocessing.pool.AsyncResult.get() <https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.AsyncResult.get>`_
        method in a infinite loop until all test results are retrieved. The return type is the same builder object which is added to list
        of valid builders that is returned at end of method.
        """

        results = []

        workers = mp.Pool(2)

        # for name in self.executors.keys():
        #    print(f"Name: {name}  Builders:  {self.executors[name].get_builder()}")

        # if there are no builders loaded we return from method
        if not self.builders:
            return

        for builder in self.builders:
            print("{:_<30}".format(""))
            console.print(f"Launching test: [blue]{builder}[/]")
            console.print(
                f"[blue]{builder}[/]: Running Test script [cyan]{builder.metadata['build_script']}"
            )

            executor = self._choose_executor(builder)
            if executor.type == "local":
                # local_builders.append(builder)
                result = workers.apply_async(executor.run, args=(builder,))
            else:
                # batch_builders.append(builder)
                result = workers.apply_async(executor.dispatch, args=(builder,))

            results.append(result)

        # loop until all async results are complete. results is a list of multiprocessing.pool.AsyncResult objects
        while results:
            async_results_ready = []
            for result in results:
                try:
                    # line below will raise TimeoutError if result is not ready, if its ready we append item to list and break
                    task = result.get(0.1)
                except mp.TimeoutError:
                    continue

                async_results_ready.append(result)

                # the task object could be None if it fails to submit job therefore we only add items that are valid builders
                if isinstance(task, BuilderBase):
                    self.valid_builders.append(task)

            # remove result that are complete
            for result in async_results_ready:
                results.remove(result)

        # close the worker pool by preventing any more tasks from being submitted
        workers.close()

        # terminate all worker processes
        workers.join()

        return self.valid_builders

    def get_builders(self):
        """Return a list of valid builders that were run"""
        return self.valid_builders
