import logging
import re
import time

from buildtest.scheduler.job import Job
from buildtest.utils.command import BuildTestCommand

logger = logging.getLogger(__name__)


class SlurmJob(Job):
    """The SlurmJob class models a Slurm Job ID with helper methods to perform operation against an active slurm job. The SlurmJob class
    can poll job to get updated job state, gather job data upon completion of test and cancel job if necessary. We can also retrieve job
    state and determine if job is running, pending, suspended, or cancelled. Jobs are polled via `sacct <https://slurm.schedmd.com/sacct.html>`_
    command which can retrieve pending, running and complete jobs.
    """

    def __init__(self, jobID, slurm_cmds, cluster=None):
        super().__init__(jobID)
        self.cluster = cluster
        self.slurm_cmds = slurm_cmds

    def is_pending(self):
        """If job is pending return ``True`` otherwise return ``False``. Slurm Job state for pending
        is ``PENDING``."""
        return self._state == "PENDING"

    def is_running(self):
        """If job is running return ``True`` otherwise return ``False``. Slurm will report ``RUNNING``
        for job state."""

        return self._state == "RUNNING"

    def is_suspended(self):
        """If job is suspended return ``True`` otherwise return ``False``. Slurm will report ``SUSPENDED``
        for job state."""

        return self._state == "SUSPENDED"

    def is_cancelled(self):
        """If job is cancelled return ``True`` otherwise return ``False``. Slurm will report ``CANCELLED``
        for job state."""

        return self._state == "CANCELLED"

    def is_complete(self):
        """If job is complete return ``True`` otherwise return ``False``. Slurm will report ``COMPLETED``
        for job state."""

        return self._state in ["COMPLETED", "FAILED", "TIMEOUT", "OUT_OF_MEMORY"]

    def is_failed(self):
        """If job failed return ``True`` otherwise return ``False``. Slurm will report ``FAILED``
        for job state."""

        return self._state == "FAILED"

    def is_out_of_memory(self):
        """If job is out of memory return ``True`` otherwise return ``False``. Slurm will report ``OUT_OF_MEMORY``
        for job state."""

        return self._state == "OUT_OF_MEMORY"

    def is_timeout(self):
        """If job timed out return ``True`` otherwise return ``False``. Slurm will report ``TIMEOUT``
        for job state."""

        return self._state == "TIMEOUT"

    def complete(self):
        """This method is used for gathering job result we assume job is complete if it's
        in any of the following state: ``COMPLETED``, ``FAILED``, ``OUT_OF_MEMORY``, ``TIMEOUT``
        """

        return any(
            [
                self.is_complete(),
                self.is_failed(),
                self.is_out_of_memory(),
                self.is_timeout(),
            ]
        )

    def state(self):
        """Return job state"""

        return self._state

    def workdir(self):
        """Return job work directory"""

        return self._workdir

    def cancel(self):
        """Cancel job by running ``scancel <jobid>``. If job is specified to a slurm
        cluster we cancel job using ``scancel <jobid> --clusters=<cluster>``. This method
        is called if job exceeds `maxpendtime`."""

        query = f"{self.slurm_cmds['scancel']} {self.jobid}"
        if self.cluster:
            query = (
                f"{self.slurm_cmds['scancel']} {self.jobid} --clusters={self.cluster}"
            )

        cmd = BuildTestCommand(query)
        cmd.execute()
        logger.debug(f"Cancelling Job: {self.jobid} by running: {query}")

        self.poll()
        self._state = "CANCELLED"

    def poll(self):
        """This method will poll job via ``sacct`` command to get updated job state by running the
        following command: ``sacct -j <jobid> -o State -n -X -P``

        Slurm will report the job state that can be parsed. Shown below is an example job
        that is ``PENDING`` state

        .. code-block:: console

            $ sacct -j 46641229 -o State -n -X -P
            PENDING
        """

        query = f"{self.slurm_cmds['sacct']} -j {self.jobid} -o State -n -X -P"
        if self.cluster:
            query += f" --clusters={self.cluster}"

        # there is a delay when test is run until slurm can query job via 'sacct'. This is relevant when using
        # 1 sec pollinterval. The sacct query will not return the job state so we sleep and try until we get value
        while True:
            cmd = BuildTestCommand(query)
            cmd.execute()

            logger.debug(f"Querying JobID: '{self.jobid}' by running: '{query}'")
            output = cmd.get_output()
            self._state = "".join(output).rstrip()

            if self._state:
                logger.debug(f"JobID: '{self.jobid}' Job State: {self._state}")
                break
            logger.debug(
                f"Unable to get job state for JobID: '{self.jobid}' so trying again"
            )
            time.sleep(0.1)

        if self.is_running() and not self.starttime:
            self.starttime = time.time()

    def get_output_and_error_files(self):
        """This method will extract file paths to StdOut and StdErr using ``scontrol show job <jobid>`` command that will
        be used to set output and error file.

        .. code-block:: console

            siddiq90@login07> scontrol show job 23608796
            JobId=23608796 JobName=perlmutter-gpu.slurm
                UserId=siddiq90(92503) GroupId=siddiq90(92503) MCS_label=N/A
                Priority=69119 Nice=0 Account=nstaff_g QOS=gpu_debug
                JobState=PENDING Reason=Priority Dependency=(null)
                Requeue=0 Restarts=0 BatchFlag=1 Reboot=0 ExitCode=0:0
                RunTime=00:00:00 TimeLimit=00:05:00 TimeMin=N/A
                SubmitTime=2024-03-28T12:36:05 EligibleTime=2024-03-28T12:36:05
                AccrueTime=2024-03-28T12:36:05
                StartTime=2024-03-28T12:36:14 EndTime=2024-03-28T12:41:14 Deadline=N/A
                SuspendTime=None SecsPreSuspend=0 LastSchedEval=2024-03-28T12:36:12 Scheduler=Backfill:*
                Partition=gpu_ss11 AllocNode:Sid=login07:1529462
                ReqNodeList=(null) ExcNodeList=(null)
                NodeList=
                NumNodes=1-1 NumCPUs=4 NumTasks=4 CPUs/Task=1 ReqB:S:C:T=0:0:*:*
                ReqTRES=cpu=4,mem=229992M,node=1,billing=4,gres/gpu=1
                AllocTRES=(null)
                Socks/Node=* NtasksPerN:B:S:C=4:0:*:* CoreSpec=*
                MinCPUsNode=4 MinMemoryNode=0 MinTmpDiskNode=0
                Features=gpu&a100 DelayBoot=00:00:00
                OverSubscribe=NO Contiguous=0 Licenses=u1:1 Network=(null)
                Command=/global/u1/s/siddiq90/jobs/perlmutter-gpu.slurm
                WorkDir=/global/u1/s/siddiq90/jobs
                StdErr=/global/u1/s/siddiq90/jobs/slurm-23608796.out
                StdIn=/dev/null
                StdOut=/global/u1/s/siddiq90/jobs/slurm-23608796.out
                Power=
                TresPerJob=gres:gpu:1


        """

        query = f"{self.slurm_cmds['scontrol']} show job {self.jobid}"
        if self.cluster:
            query += f" --clusters={self.cluster}"

        cmd = BuildTestCommand(query)
        cmd.execute()
        logger.debug(f"Querying JobID: '{self.jobid}' by running: '{query}'")
        content = " ".join(cmd.get_output())

        logger.debug(f"Output of scontrol show job {self.jobid}:\n{content}")

        pattern = r"StdOut=(?P<stdout>.+)"
        match = re.search(pattern, content)
        logger.debug(
            f"Extracting StdOut file by applying regular expression: {pattern}"
        )
        if match:
            self._outfile = match.group("stdout")
        else:
            logger.error(f"Unable to extract StdOut file from output: {content}")

        pattern = r"StdErr=(?P<stderr>.+)"
        match = re.search(pattern, content)
        logger.debug(
            f"Extracting StdOut file by applying regular expression: {pattern}"
        )
        if match:
            self._errfile = match.group("stderr")
        else:
            logger.error(f"Unable to extract StdErr file from error: {content}")

        logger.debug(f"Output File: {self._outfile}")
        logger.debug(f"Error File: {self._errfile}")

    def retrieve_jobdata(self):
        """This method will get job record which is called after job completion. We use `sacct` to gather
        job record and return the job record as a dictionary. The command we run is
        ``sacct -j <jobid> -X -n -P -o <field1>,<field2>,...,<fieldN>``. We retrieve the following
        format fields from job record:

            - "Account"
            - "AllocNodes"
            - "AllocTRES"
            - "ConsumedEnergyRaw"
            - "CPUTimeRaw"
            - "Elapsed"
            - "ElapsedRaw"
            - "End"
            - "ExitCode"
            - "JobID"
            - "JobName"
            - "NCPUS"
            - "NNodes"
            - "QOS"
            - "ReqMem"
            - "ReqNodes"
            - "Start"
            - "State"
            - "Submit"
            - "UID"
            - "User"
            - "WorkDir"

        The output of sacct is parseable using the pipe symbol (**|**) and stored into a dict

        .. code-block:: console

            $ sacct -j 42909266 -X -n -P -o Account,AllocNodes,AllocTRES,ConsumedEnergyRaw,CPUTimeRaw,Elapsed,End,ExitCode,JobID,JobName,NCPUS,NNodes,QOS,ReqMem,ReqNodes,Start,State,Submit,UID,User,WorkDir --clusters=cori
            nstaff|1|billing=272,cpu=272,energy=262,mem=87G,node=1|262|2176|00:00:08|2021-05-27T18:47:49|0:0|42909266|slurm_metadata|272|1|debug_knl|87Gn|1|2021-05-27T18:47:41|COMPLETED|2021-05-27T18:44:07|92503|siddiq90|/global/u1/s/siddiq90/.buildtest/tests/cori.slurm.knl_debug/metadata/slurm_metadata/0/stage

        We retrieve ExitCode and WorkDir via sacct command to get returncode. Slurm will write output and error file in WorkDir location. We
        run the following command below and parse the output. The ExitCode is in form ``<exitcode>:<signal>`` which is colon
        separated list. For more details on Slurm Exit code see https://slurm.schedmd.com/job_exit_code.html

        .. code-block:: console

            $ sacct -j 46294283 --clusters=cori -X -n -P -o ExitCode,Workdir
            0:0|/global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/hostname/hostname_knl/cd39a853/stage
        """

        sacct_fields = [
            "Account",
            "AllocNodes",
            "AllocTRES",
            "ConsumedEnergyRaw",
            "CPUTimeRaw",
            "Elapsed",
            "ElapsedRaw",
            "End",
            "ExitCode",
            "JobID",
            "JobName",
            "NCPUS",
            "NNodes",
            "QOS",
            "ReqMem",
            "ReqNodes",
            "Start",
            "State",
            "Submit",
            "UID",
            "User",
            "WorkDir",
        ]

        query = (
            f"{self.slurm_cmds['sacct']} -j {self.jobid} -X -n -P -o ExitCode,Workdir"
        )
        if self.cluster:
            query += f" --clusters={self.cluster}"

        cmd = BuildTestCommand(query)
        cmd.execute()

        logger.debug(
            f"Querying JobID: '{self.jobid}' ExitCode and Workdir by running: '{query}'"
        )

        out = "".join(cmd.get_output()).rstrip()

        exitcode, workdir = out.split("|")
        # Exit Code field is in format <ExitCode>:<Signal> for now we care only about first number
        self._exitcode = int(exitcode.split(":")[0])
        self._workdir = workdir
        logger.debug(f"JobID: '{self.jobid}' finished with exitcode: {self._exitcode}")
        query = f"{self.slurm_cmds['sacct']} -j {self.jobid} -X -n -P -o {','.join(sacct_fields)}"

        # to query jobs from another cluster we must add -M <cluster> to sacct
        if self.cluster:
            query += f" --clusters={self.cluster}"

        logger.debug(f"Gather slurm job data by running: {query}")
        cmd = BuildTestCommand(query)
        cmd.execute()
        out = "".join(cmd.get_output())
        # split by | since
        out = out.split("|")
        job_data = {}
        for field, value in zip(sacct_fields, out):
            job_data[field] = value

        self._jobdata = job_data
