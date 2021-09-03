import os
import time

from tabulate import tabulate
from termcolor import colored


class PollQueue:
    def __init__(self, builders, interval, buildexecutor):
        self.builders = builders
        self.interval = interval
        self.buildexecutor = buildexecutor
        self._completed = set()
        self._cancelled = set()

        self._pending = []
        # only add builders that are batch jobs
        for builder in self.builders:
            # returns True if attribute builder.job is an instance of class Job
            if builder.is_batch_job():
                self._pending.append(builder)

    def cancelled(self):
        """Return a list of cancelled builders"""
        return self._cancelled

    def completed(self):
        return self._completed

    def sleep(self):
        time.sleep(self.interval)

    def poll(self):
        """Poll all pending jobs until all jobs are complete. At each poll interval, we poll each builder
        job state. If job is complete or failed we remove job from pending queue. In each interval we sleep
        and poll jobs until there is no pending jobs."""
        while self._pending:
            print(f"Polling Jobs in {self.interval} seconds")
            self.sleep()

            # store list of cancelled and completed job at each interval
            cancelled = []
            completed = []

            for builder in self._pending:

                # get executor instance for corresponding builder. This would be one of the following: SlurmExecutor, PBSExecutor, LSFExecutor, CobaltExecutor
                executor = self.buildexecutor.get(builder.executor)
                # if builder is local executor we shouldn't be polling so we set job to
                # complete and return

                executor.poll(builder)

                if builder.is_complete():
                    completed.append(builder)
                elif builder.is_failure():
                    cancelled.append(builder)

            # remove completed jobs from pending queue
            if completed:
                for builder in completed:
                    self._pending.remove(builder)
                    self._completed.add(builder)

            # remove cancelled jobs from pending queue
            if cancelled:
                for builder in cancelled:
                    self._pending.remove(builder)
                    self._cancelled.add(builder)

            self.print_pending_jobs()

    def print_pending_jobs(self):
        """Print pending jobs in table format during each poll step"""
        pending_jobs_table = {
            "name": [],
            "id": [],
            "executor": [],
            "jobID": [],
            "jobstate": [],
            "runtime": [],
        }
        headers = pending_jobs_table.keys()
        if os.getenv("BUILDTEST_COLOR") == "True":
            headers = list(map(lambda x: colored(x, "blue", attrs=["bold"]), headers))

        for job in self._pending:
            pending_jobs_table["name"].append(job.name)
            pending_jobs_table["id"].append(job.metadata["id"])
            pending_jobs_table["executor"].append(job.executor)
            pending_jobs_table["jobID"].append(job.metadata["jobid"])
            pending_jobs_table["jobstate"].append(job.job.state())
            pending_jobs_table["runtime"].append(job.timer.duration())

        if pending_jobs_table["name"]:
            print("\n")
            print("Current Jobs")
            print("{:_<15}".format(""))
            print("\n")
            print(
                tabulate(
                    pending_jobs_table,
                    headers=headers,
                    tablefmt="pretty",
                )
            )

    def print_polled_jobs(self):

        if not self._completed:
            return

        table = {
            "name": [],
            "id": [],
            "executor": [],
            "jobID": [],
            "jobstate": [],
            "status": [],
            "returncode": [],
            "runtime": [],
        }

        msg = """
+-----------------------+
| Completed Polled Jobs |
+-----------------------+ 
                """
        if os.getenv("BUILDTEST_COLOR") == "True":
            msg = colored(msg, "red", attrs=["bold"])

        print(msg)

        for builder in self._completed:
            table["name"].append(builder.name)
            table["id"].append(builder.metadata["id"])
            table["executor"].append(builder.executor)
            table["jobID"].append(builder.job.get())
            table["jobstate"].append(builder.job.state())
            table["status"].append(builder.metadata["result"]["state"])
            table["returncode"].append(builder.metadata["result"]["returncode"])
            table["runtime"].append(builder.metadata["result"]["runtime"])

        headers = table.keys()
        if os.getenv("BUILDTEST_COLOR") == "True":
            headers = list(map(lambda x: colored(x, "blue", attrs=["bold"]), headers))

        print(tabulate(table, headers=headers, tablefmt="presto"))
