import time

from buildtest.defaults import console
from rich.table import Table


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

    def poll(self):
        """Poll all until all jobs are complete. At each poll interval, we poll each builder
        job state. If job is complete or failed we remove job from pending queue. In each interval we sleep
        and poll jobs until there is no pending jobs."""
        while self._pending:
            print(f"Polling Jobs in {self.interval} seconds")

            time.sleep(self.interval)

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

        self.print_polled_jobs()

    def print_pending_jobs(self):
        """Print pending jobs in table format during each poll step"""
        table = Table(
            "[blue]Builder",
            "[blue]executor",
            "[blue]JobID",
            "[blue]JobState",
            "[blue]runtime",
            title="Pending Jobs",
        )
        for builder in self._pending:
            table.add_row(
                str(builder),
                builder.executor,
                builder.job.get(),
                builder.job.state(),
                str(builder.timer.duration()),
            )
        console.print(table)

    def print_polled_jobs(self):

        if not self._completed:
            return

        table = Table(
            "[blue]Builder",
            "[blue]executor",
            "[blue]JobID",
            "[blue]JobState",
            "[blue]runtime",
            title="Completed Jobs",
        )
        for builder in self._completed:
            table.add_row(
                str(builder),
                builder.executor,
                builder.job.get(),
                builder.job.state(),
                str(builder.metadata["result"]["runtime"]),
            )
        console.print(table)
