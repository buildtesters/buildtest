from buildtest.utils.command import BuildTestCommand
from buildtest.executors.base import BaseExecutor


class CobaltExecutor(BaseExecutor):
    """The CobaltExecutor class is responsible for submitting jobs to Cobalt Scheduler.

    """

    type = "cobalt"

    job_state = None
    poll_cmd = "qstat"
    qstat_fields = "-lf"

    def check(self):
        """Check cobalt binary is available before running tests. This will check
        the launcher (``qsub``) and ``qstat`` are available.
        """

        if not shutil.which(self.launcher):
            sys.exit(
                f"[{self.builder.metadata['name']}]: Cannot find launcher program: {self.launcher}"
            )

        if not shutil.which(self.poll_cmd):
            sys.exit(
                f"[{self.builder.metadata['name']}]: Cannot find cobalt poll command: {self.poll_cmd}"
            )

    def load(self):
        """Load the a Cobalt executor configuration from buildtest settings."""

        self.launcher = self._settings.get("launcher") or self._buildtestsettings[
            "executors"
        ].get("defaults", {}).get("launcher")
        self.launcher_opts = self._settings.get("options")

        self.queue = self._settings.get("queue")
        self.account = self._settings.get("account") or self._buildtestsettings[
            "executors"
        ].get("defaults", {}).get("account")
        self.max_pend_time = self._settings.get(
            "max_pend_time"
        ) or self._buildtestsettings["executors"].get("defaults", {}).get(
            "max_pend_time"
        )

    def dispatch(self):

        self.check()
        self.result = {}

        batch_cmd = [self.launcher]

        if self.queue:
            batch_cmd += [f"-q {self.queue}"]

        batch_cmd += [self.builder.metadata["testpath"]]
        self.builder.metadata["command"] = " ".join(batch_cmd)
        self.logger.debug(
            f"Running Test via command: {self.builder.metadata['command']}"
        )

        command = BuildTestCommand(self.builder.metadata["command"])
        command.execute()
        self.builder.start()

        # if qsub job submission returns non-zero exit that means we have failure, exit immediately
        if command.returncode != 0:
            err = f"[{self.builder.metadata['name']}] failed to submit job with returncode: {command.returncode} \n"
            err += f"[{self.builder.metadata['name']}] running command: {' '.join(batch_cmd)}"
            sys.exit(err)

        parse_jobid = command.get_output()
        parse_jobid = " ".join(parse_jobid)

        # convert JobID into integer
        self.job_id = int(parse_jobid)

        self.builder.metadata["jobid"] = self.job_id

        msg = f"[{self.builder.metadata['name']}] JobID: {self.builder.metadata['jobid']} dispatched to scheduler"
        print(msg)
        self.logger.debug(msg)

        self.result["state"] = "N/A"
        self.result["runtime"] = "0"
        self.result["returncode"] = "0"

    def poll(self):

        self.logger.debug(f"Query Job: {self.builder.metadata['jobid']}")

        qstat_cmd = (
            f"{self.poll_cmd} {self.qstat_fields} {self.builder.metadata['jobid']}"
        )

        self.logger.debug(qstat_cmd)
        cmd = BuildTestCommand(qstat_cmd)
        cmd.execute()
        poll_content = cmd.get_output()
        print(poll_content, type(poll_content))

        job_data = {}
        for line in poll_content:
            key, sep, value = line.partition(":")
            job_data[key] = value

        print(job_data)
        self.builder.job_state = job_data["State"]
        print(self.builder.job_state)

    def gather(self):

        self.builder.metadata["job"] = job_data
