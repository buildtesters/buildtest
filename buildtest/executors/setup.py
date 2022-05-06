"""
This module is responsible for setup of executors defined in buildtest
configuration. The BuildExecutor class initializes the executors and chooses the
executor class (LocalExecutor, LSFExecutor, SlurmExecutor, CobaltExecutor) to call depending
on executor name.
"""

import logging
import multiprocessing as mp
import os
import time

from buildtest.builders.base import BuilderBase
from buildtest.defaults import BUILDTEST_EXECUTOR_DIR, console
from buildtest.exceptions import BuildTestError, ExecutorError
from buildtest.executors.base import BaseExecutor
from buildtest.executors.cobalt import CobaltExecutor
from buildtest.executors.local import LocalExecutor
from buildtest.executors.lsf import LSFExecutor
from buildtest.executors.pbs import PBSExecutor
from buildtest.executors.slurm import SlurmExecutor
from buildtest.tools.modules import get_module_commands
from buildtest.utils.file import create_dir, write_file
from buildtest.utils.tools import deep_get
from rich.table import Table

logger = logging.getLogger(__name__)


class BuildExecutor:
    """A BuildExecutor is responsible for initialing executors from buildtest configuration
    file which provides a list of executors. This class keeps track of all executors and provides
    the following methods:

    - **setup**: This method will  write executor's ``before_script.sh``  that is sourced in each test upon calling executor.
    - **run**: Responsible for invoking executor's **run** method based on builder object which is of type BuilderBase.
    - **poll**: This is responsible for invoking ``poll`` method for corresponding executor from the builder object by checking job state
    """

    def __init__(
        self,
        site_config,
        account=None,
        maxpendtime=None,
        pollinterval=None,
        timeout=None,
    ):
        """Initialize executors, meaning that we provide the buildtest
        configuration that are validated, and can instantiate
        each executor to be available.

        Args:
            site_config (buildtest.config.SiteConfiguration): instance of SiteConfiguration class that has the buildtest configuration
            account (str, optional): pass account name to charge batch jobs.
            maxpendtime (int, optional): maximum pend time in second until job is cancelled.
            pollinterval (int, optional): Number of seconds to wait until polling batch jobs
        """

        # stores a list of builders objects
        self.builders = set()

        # default poll interval if not specified
        default_interval = 30

        self.configuration = site_config

        self.pollinterval = (
            pollinterval
            or deep_get(
                self.configuration.target_config,
                "executors",
                "defaults",
                "pollinterval",
            )
            or default_interval
        )

        self._completed = set()

        self._pending_jobs = set()

        self.executors = {}
        logger.debug("Getting Executors from buildtest settings")

        if site_config.valid_executors["local"]:
            for name in self.configuration.valid_executors["local"].keys():
                self.executors[name] = LocalExecutor(
                    name=name,
                    settings=self.configuration.valid_executors["local"][name][
                        "setting"
                    ],
                    site_configs=self.configuration,
                    timeout=timeout,
                )

        if site_config.valid_executors["slurm"]:
            for name in self.configuration.valid_executors["slurm"]:
                self.executors[name] = SlurmExecutor(
                    name=name,
                    account=account,
                    settings=self.configuration.valid_executors["slurm"][name][
                        "setting"
                    ],
                    site_configs=self.configuration,
                    maxpendtime=maxpendtime,
                    timeout=timeout,
                )

        if self.configuration.valid_executors["lsf"]:
            for name in self.configuration.valid_executors["lsf"]:
                self.executors[name] = LSFExecutor(
                    name=name,
                    account=account,
                    settings=self.configuration.valid_executors["lsf"][name]["setting"],
                    site_configs=self.configuration,
                    maxpendtime=maxpendtime,
                    timeout=timeout,
                )

        if self.configuration.valid_executors["pbs"]:
            for name in self.configuration.valid_executors["pbs"]:
                self.executors[name] = PBSExecutor(
                    name=name,
                    account=account,
                    settings=self.configuration.valid_executors["pbs"][name]["setting"],
                    site_configs=self.configuration,
                    maxpendtime=maxpendtime,
                    timeout=timeout,
                )

        if self.configuration.valid_executors["cobalt"]:
            for name in self.configuration.valid_executors["cobalt"]:
                self.executors[name] = CobaltExecutor(
                    name=name,
                    account=account,
                    settings=self.configuration.valid_executors["cobalt"][name][
                        "setting"
                    ],
                    site_configs=self.configuration,
                    maxpendtime=maxpendtime,
                    timeout=timeout,
                )
        self.setup()

    def __str__(self):
        return "[buildtest-executor]"

    def __repr__(self):
        return "[buildtest-executor]"

    def names(self):
        """Return a list of executor names"""
        return list(self.executors.keys())

    def get(self, name):
        """Given the name of an executor return the executor object which is of subclass of `BaseExecutor`"""
        return self.executors.get(name)

    def get_validbuilders(self):
        """Return a list of valid builders that were run"""
        complete_builders = []
        for builder in self.builders:
            if builder.is_complete():
                complete_builders.append(builder)

        return complete_builders

    def _choose_executor(self, builder):
        """Choose executor is called at the onset of a run and poll stage. Given a builder
        object we retrieve the executor property ``builder.executor`` of the builder and check if
        there is an executor object and of type `BaseExecutor`.

        Args:
            builder (buildtest.buildsystem.base.BuilderBase): An instance object of BuilderBase type
        """

        # Get the executor by name, and add the builder to it
        executor = self.get(builder.executor)
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

        for executor_name in self.names():
            create_dir(os.path.join(BUILDTEST_EXECUTOR_DIR, executor_name))
            executor_settings = self.executors[executor_name]._settings

            # if before_script field defined in executor section write content to var/executors/<executor>/before_script.sh
            file = os.path.join(
                BUILDTEST_EXECUTOR_DIR, executor_name, "before_script.sh"
            )
            module_cmds = get_module_commands(executor_settings.get("module"))

            content = "#!/bin/bash" + "\n"

            if module_cmds:
                content += "\n".join(module_cmds) + "\n"

            content += executor_settings.get("before_script") or ""
            write_file(file, content)

    def select_builders_to_run(self, builders):
        """This method will return list of builders that need to run. We need to check any builders that have a job dependency
        and make sure the dependent jobs are finished prior to running builder. The return method will be a list of builders
        to run.
        """

        run_builders = set()

        testnames = {builder.name: builder for builder in self.builders}

        # This section must be executed sequentially if job dependency are found for
        # any test. Test will be executed async but when checking if test is complete via
        # .is_complete() we need the builders to be processed to get updated state.
        for builder in builders:

            if not builder.recipe.get("needs"):
                console.print(
                    f"[green]{builder} does not have any dependencies adding test to queue"
                )
                run_builders.add(builder)
                continue

            builder.dependency = False
            #
            for name in builder.recipe["needs"]:

                # if element in needs is a string then we check if job is complete
                if isinstance(name, str):
                    if name not in list(testnames.keys()):
                        continue

                    if testnames[name].is_pending():
                        builder.dependency = True
                        console.print(
                            f"[blue]{builder}[/blue] [red]Skipping job because it has job dependency on {testnames[name]} which is in state {testnames[name].state()} [/red]"
                        )
                        break
                else:
                    testname = list(name.keys())[0]

                    if testname not in testnames.keys():
                        continue

                    if testnames[testname].is_pending():
                        builder.dependency = True
                        console.print(
                            f"[blue]{builder}[/blue] [red]Skipping job because it has job dependency on {testnames[testname]} [/red]"
                        )
                        break

                    if "state" in name[testname]:

                        match_state = (
                            name[testname]["state"]
                            == testnames[testname].metadata["result"]["state"]
                        )

                        if not match_state:

                            if testnames[testname].is_pending():
                                builder.dependency = True
                                console.print(
                                    f"[blue]{builder}[/blue] skipping test because it depends on {testnames[testname]} to have state: {name[testname]['state']} but actual value is {testnames[testname].metadata['result']['state']}"
                                )
                                break
                            # if there is no match but in 'state' property but job is not pending then we cancel job
                            else:
                                builder.failed()

                                builder.dependency = True
                                console.print(
                                    f"[red]{builder} is cancelled because it depends on {testnames[testname]} to have state: {name[testname]['state']} but actual value is {testnames[testname].metadata['result']['state']}"
                                )

                    if "returncode" in name[testname]:
                        rc = []
                        if isinstance(name[testname]["returncode"], int):
                            rc.append(name[testname]["returncode"])
                        else:
                            rc = name[testname]["returncode"]

                        no_match = (
                            testnames[testname].metadata["result"]["returncode"]
                            not in rc
                        )
                        if no_match:

                            if testnames[testname].is_pending():
                                console.print(
                                    f"[red]{builder} is cancelled because it expects one of these returncode {rc} from {testnames[testname]} but test has {testnames[testname].metadata['result']['returncode']} "
                                )
                                builder.dependency = True

                            # if test is not complete we check if test returncode with value specified in needs property for corresponding test
                            else:
                                builder.dependency = True
                                builder.failed()
                                continue

            if builder.dependency:
                continue

            run_builders.add(builder)

        builders = []
        for builder in run_builders:
            if builder.is_pending():
                builders.append(builder)

        # console.print(f"In this iteration we will run the following tests: {builders}", )
        return builders

    def run(self, builders):
        """This method is responsible for running the build script for each builder async and
        gather the results. We setup a pool of worker settings by invoking ``multiprocessing.pool.Pool``
        and use `multiprocessing.pool.Pool.apply_sync() <https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool.apply_async>`_
        method for running test async which returns
        an object of type `multiprocessing.pool.AsyncResult <https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.AsyncResult>`_
        which holds the result. Next we wait for results to arrive using `multiprocessing.pool.AsyncResult.get() <https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.AsyncResult.get>`_
        method in a infinite loop until all test results are retrieved. The return type is the same builder object which is added to list
        of valid builders that is returned at end of method.
        """

        for builder in builders:
            executor = self._choose_executor(builder)
            executor.add_builder(builder)
            self.builders.add(builder)

        num_workers = self.configuration.target_config.get("numprocs") or os.cpu_count()
        # in case user specifies more process than available CPU count use the min of the two numbers
        num_workers = min(num_workers, os.cpu_count())

        pool = mp.Pool(num_workers)
        console.print(f"Spawning {num_workers} processes for processing builders")
        count = 0
        while True:

            active_builders = []
            count += 1
            console.rule(f"Iteration {count}")

            for builder in self.builders:
                if builder.is_pending():
                    active_builders.append(builder)

            run_builders = self.select_builders_to_run(active_builders)

            if not run_builders:
                raise BuildTestError("Unable to run tests ")

            print(
                f"In this iteration we are going to run the following tests: {run_builders}"
            )
            results = []

            for builder in run_builders:
                executor = self._choose_executor(builder)
                results.append(pool.apply_async(executor.run, args=(builder,)))
                self.builders.remove(builder)

            for result in results:
                task = result.get()
                if isinstance(task, BuilderBase):
                    self.builders.add(task)

            pending_jobs = set()
            for builder in self.builders:
                # returns True if attribute builder.job is an instance of class Job. Only add jobs that are active running for pending
                if builder.is_batch_job() and builder.is_running():
                    pending_jobs.add(builder)

            self.poll(pending_jobs)

            # remove any failed jobs from list
            # for builder in self.builders:
            #    if builder.is_failed():
            #        self.builders.remove(builder)

            terminate = True

            # condition below checks if all tests are complete, if any are pending or running we need to stay in loop until jobs are finished
            # until finished
            for builder in self.builders:
                if builder.is_pending() or builder.is_running():
                    terminate = False

            if terminate:
                break

        # close the worker pool by preventing any more tasks from being submitted
        pool.close()

        # terminate all worker processes
        pool.join()

    def poll(self, pending_jobs):
        """Poll all until all jobs are complete. At each poll interval, we poll each builder
        job state. If job is complete or failed we remove job from pending queue. In each interval we sleep
        and poll jobs until there is no pending jobs."""
        # only add builders that are batch jobs

        # poll until all pending jobs are complete
        while pending_jobs:
            print(f"Polling Jobs in {self.pollinterval} seconds")
            time.sleep(self.pollinterval)
            jobs = pending_jobs.copy()

            # for every pending job poll job and mark if job is finished or cancelled
            for job in jobs:

                # get executor instance for corresponding builder. This would be one of the following: SlurmExecutor, PBSExecutor, LSFExecutor, CobaltExecutor
                executor = self.get(job.executor)
                # if builder is local executor we shouldn't be polling so we set job to
                # complete and return

                executor.poll(job)

                if job.is_complete():
                    pending_jobs.remove(job)

                elif job.is_failed():
                    pending_jobs.remove(job)
                    # need to remove builder from self._validbuilders when job is cancelled because these builders are ones
                    # self._validbuilders.remove(job)

            self.print_job_details(jobs)

    def print_job_details(self, active_jobs):
        """Print pending jobs in table format during each poll step

        args:
            active_jobs (list): List of builders whose jobs are pending, suspended or running
            completed_jobs (list): List of builders whose jobs are completed
        """
        table_columns = ["builder", "executor", "jobid", "jobstate", "runtime"]
        pending_jobs_table = Table(
            title="Pending and Suspended Jobs", header_style="blue"
        )
        running_jobs_table = Table(title="Running Jobs", header_style="blue")
        completed_jobs_table = Table(title="Completed Jobs", header_style="blue")

        for column in table_columns:
            pending_jobs_table.add_column(column)
            running_jobs_table.add_column(column)
            completed_jobs_table.add_column(column)

        for builder in active_jobs:

            if builder.job.is_pending() or builder.job.is_suspended():
                pending_jobs_table.add_row(
                    f"[blue]{str(builder)}",
                    f"[green]{builder.executor}",
                    f"[red]{builder.job.get()}",
                    f"[cyan]{builder.job.state()}",
                    f"[magenta]{str(builder.timer.duration())}",
                )

            if builder.job.is_running():
                running_jobs_table.add_row(
                    f"[blue]{str(builder)}",
                    f"[green]{builder.executor}",
                    f"[red]{builder.job.get()}",
                    f"[cyan]{builder.job.state()}",
                    f"[magenta]{str(builder.timer.duration())}",
                )

            if builder.job.is_complete():
                completed_jobs_table.add_row(
                    f"[blue]{str(builder)}",
                    f"[green]{builder.executor}",
                    f"[red]{builder.job.get()}",
                    f"[cyan]{builder.job.state()}",
                    f"[magenta]{str(builder.metadata['result']['runtime'])}",
                )

        # only print table if there are rows in table
        if pending_jobs_table.row_count:
            console.print(pending_jobs_table)

        if running_jobs_table.row_count:
            console.print(running_jobs_table)

        if completed_jobs_table.row_count:
            console.print(completed_jobs_table)
