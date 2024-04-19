import json
import logging
import os
import re
import time

from buildtest.exceptions import JobSchedulerError
from buildtest.scheduler.job import Job
from buildtest.utils.command import BuildTestCommand

logger = logging.getLogger(__name__)


class PBSJob(Job):
    """The PBSJob models a PBS Job with helper methods to retrieve job state, check if job is running/pending/suspended. We have methods
    to poll job state, gather job results upon completion and cancel job.
    """

    def __init__(self, jobID, sched_cmds):
        self._outfile = None
        self._errfile = None
        self.qdel_cmd = sched_cmds["qdel"]
        self.poll_command = f"{sched_cmds['qstat']} -xf"
        super().__init__(jobID)

    def is_pending(self):
        """Return ``True`` if job is pending. A pending job is in state ``Q``."""
        return self._state == "Q"

    def is_running(self):
        """Return ``True`` if job is running. A completed job is in state ``R``."""
        return self._state == "R"

    def is_complete(self):
        """Return ``True`` if job is complete. A completed job is in state ``F``."""
        return self._state == "C"

    def is_suspended(self):
        """Return ``True`` if job is suspended which would be in one of these states ``H``, ``U``, ``S``."""
        return self._state in ["H", "U", "S"]

    def success(self):
        """This method determines if job was completed successfully and returns ``True`` if exit code is 0.

        According to https://help.altair.com/2021.1.3/PBS%20Professional/PBSAdminGuide2021.1.3.pdf section 14.9 Job Exit Status Codes we have the following

         - Exit Code:  X < 0         - Job could not be executed
         - Exit Code: 0 <= X < 128   -  Exit value of Shell or top-level process
         - Exit Code: X >= 128       - Job was killed by signal
         - Exit Code: X == 0         - Job executed was a successful
        """
        return self._exitcode == 0

    def fail(self):
        """Return ``True`` if their is a job failure which would be if exit code is not 0"""
        return not self.success()

    def get_output_error_files(self):
        """Fetch output and error files right after job submission."""
        query = f"{self.poll_command} {self.jobid}"
        cmd = BuildTestCommand(query)
        cmd.execute()
        output = " ".join(cmd.get_output())

        # Regular expression pattern to match the OutPut_Path field. This will account for text spanning multiple lines
        pattern = r"Output_Path\s*=\s*(.*?)\s*Priority"
        match = re.search(pattern, output, re.DOTALL)

        if match:
            lines = match.group(1).split(":")[1].split("\n")
            # Remove leading whitespace from lines after the first line
            formatted_lines = [lines[0]] + [line.strip() for line in lines[1:]]

            self._outfile = "".join(formatted_lines)
            logger.debug(self._outfile)

        # Regular expression pattern to match the Error_Path field
        pattern = r"Error_Path\s*=\s*(.*?)\s*(?:\n\s*(?:\w+\s*=)|$)"
        match = re.search(pattern, output, re.DOTALL)
        if match:
            lines = match.group(1).split(":")[1].split("\n")
            # Remove leading whitespace from lines after the first line
            formatted_lines = [lines[0]] + [line.strip() for line in lines[1:]]

            self._errfile = "".join(formatted_lines)

    def is_output_ready(self):
        """Check if the output and error file exists."""
        if not self._outfile or not self._errfile:
            self.get_output_error_files()
        return os.path.exists(self._outfile) and os.path.exists(self._errfile)

    def poll(self):
        """This method will poll the PBS Job by running ``qstat -f <jobid>`` which will retrieve the job details and extract
        data such as job state, exit code, output and error file.
        A typical output for the PBS job looks something like this

        .. code-block:: console

            (buildtest) adaptive50@e4spro-cluster:~/Documents/buildtest/aws_oddc$ qstat -f  40680075.e4spro-cluster
            Job Id: 40680075.e4spro-cluster
                Job_Name = hostname_test
                Job_Owner = adaptive50@server.nodus.com
                resources_used.cput = 00:00:00
                resources_used.vmem = 0kb
                resources_used.walltime = 00:00:05
                resources_used.mem = 0kb
                resources_used.energy_used = 0
                job_state = C
                queue = e4spro-cluster
                server = e4spro-cluster
                Checkpoint = u
                ctime = Mon Mar 25 17:42:02 2024
                Error_Path = e4spro-cluster:/home/adaptive50/Documents/buildtest/var/tests
                    /generic.torque.e4spro/sleep/hostname_test/b10fea47/stage/hostname_tes
                    t.e
                exec_host = ac-d160-0-0/0
                Hold_Types = n
                Join_Path = n
                Keep_Files = n
                Mail_Points = a
                mtime = Mon Mar 25 17:42:38 2024
                Output_Path = e4spro-cluster:/home/adaptive50/Documents/buildtest/var/test
                    s/generic.torque.e4spro/sleep/hostname_test/b10fea47/stage/hostname_te
                    st.o
                Priority = 0
                qtime = Mon Mar 25 17:42:02 2024
                Rerunable = True
                Resource_List.nodes = 1
                Resource_List.nodect = 1
                Resource_List.walltime = 24:00:00
                session_id = 1806
                Variable_List = PBS_O_QUEUE=e4spro-cluster,PBS_O_HOME=/home/adaptive50,
                    PBS_O_LOGNAME=adaptive50,
                    PBS_O_PATH=/home/adaptive50/Documents/buildtest/bin:/home/adaptive50/
                    .local/share/virtualenvs/buildtest-hH765GEg/bin:/home/adaptive50/packa
                    ges/bin:/usr/local/paraview-5.11.2/bin:/home/adaptive50/.local/bin:/us
                    r/local/cuda/bin:/usr/local/julia/1.10.0/bin:/usr/local/go/bin:/usr/lo
                    cal/libexec/osu-micro-benchmarks/mpi/startup:/usr/local/libexec/osu-mi
                    cro-benchmarks/mpi/pt2pt:/usr/local/libexec/osu-micro-benchmarks/mpi/o
                    ne-sided:/usr/local/libexec/osu-micro-benchmarks/mpi/collective:/opt/b
                    ootstrap/view/bin:/home/adaptive50/packages/bin:/usr/local/paraview-5.
                    11.2/bin:/home/adaptive50/.local/bin:/usr/local/cuda/bin:/usr/local/ju
                    lia/1.10.0/bin:/usr/local/go/bin:/usr/local/libexec/osu-micro-benchmar
                    ks/mpi/startup:/usr/local/libexec/osu-micro-benchmarks/mpi/pt2pt:/usr/
                    local/libexec/osu-micro-benchmarks/mpi/one-sided:/usr/local/libexec/os
                    u-micro-benchmarks/mpi/collective:/opt/bootstrap/view/bin:/home/adapti
                    ve50/spack/bin:/home/adaptive50/packages/bin:/spack/bin:/usr/local/vis
                    it/bin:/usr/local/paraview-5.11.2/bin:/home/adaptive50/.local/bin:/usr
                    /local/cuda/bin:/usr/local/julia/1.10.0/bin:/usr/local/go/bin:/usr/loc
                    al/libexec/osu-micro-benchmarks/mpi/startup:/usr/local/libexec/osu-mic
                    ro-benchmarks/mpi/pt2pt:/usr/local/libexec/osu-micro-benchmarks/mpi/on
                    e-sided:/usr/local/libexec/osu-micro-benchmarks/mpi/collective:/opt/bo
                    otstrap/view/bin:/home/adaptive50/.local/bin:/home/adaptive50/bin:/opt
                    /mvapich2-x/gnu11.1.0/mofed/aws/mpirun/bin:/usr/local/bin:/usr/local/s
                    bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/
                    games:/usr/local/games:/snap/bin:/opt/mvapich2-x/gnu11.1.0/mofed/aws/m
                    pirun/libexec/osu-micro-benchmarks/mpi/startup:/opt/mvapich2-x/gnu11.1
                    .0/mofed/aws/mpirun/libexec/osu-micro-benchmarks/mpi/one-sided:/opt/mv
                    apich2-x/gnu11.1.0/mofed/aws/mpirun/libexec/osu-micro-benchmarks/mpi/c
                    ollective:/opt/mvapich2-x/gnu11.1.0/mofed/aws/mpirun/libexec/osu-micro
                    -benchmarks/mpi/pt2pt:/usr/local/cuda/bin:/usr/local/tau-2.33/x86_64/b
                    in:/spack/opt/spack/linux-ubuntu20.04-x86_64/gcc-11.4.0/openjdk-11.0.2
                    0.1_1-qg3jd2dpwz6bwi455lcljdkiv5rifjmr/bin:/usr/local/cuda/bin:/usr/lo
                    cal/tau-2.33/x86_64/bin:/spack/opt/spack/linux-ubuntu20.04-x86_64/gcc-
                    11.4.0/openjdk-11.0.20.1_1-qg3jd2dpwz6bwi455lcljdkiv5rifjmr/bin:/usr/l
                    ocal/cuda/bin:/usr/local/tau-2.33/x86_64/bin:/spack/opt/spack/linux-ub
                    untu20.04-x86_64/gcc-11.4.0/openjdk-11.0.20.1_1-qg3jd2dpwz6bwi455lcljd
                    kiv5rifjmr/bin,PBS_O_MAIL=/var/mail/adaptive50,
                    PBS_O_SHELL=/usr/bin/bash,PBS_O_LANG=C.UTF-8,
                    PBS_O_WORKDIR=/home/adaptive50/Documents/buildtest/var/tests/generic.
                    torque.e4spro/sleep/hostname_test/b10fea47/stage,
                    PBS_O_HOST=e4spro-cluster,PBS_O_SERVER=e4spro-cluster
                euser = adaptive50
                egroup = adaptive50
                queue_type = E
                etime = Mon Mar 25 17:42:02 2024
                exit_status = 0
                submit_args = -q e4spro-cluster /home/adaptive50/Documents/buildtest/var/t
                    ests/generic.torque.e4spro/sleep/hostname_test/b10fea47/stage/hostname
                    _test.sh
                start_time = Mon Mar 25 17:42:32 2024
                start_count = 1
                fault_tolerant = False
                comp_time = Mon Mar 25 17:42:38 2024
                job_radix = 0
                total_runtime = 6.235349
                submit_host = e4spro-cluster
                init_work_dir = /home/adaptive50/Documents/buildtest/var/tests/generic.tor
                    que.e4spro/sleep/hostname_test/b10fea47/stage
                request_version = 1
                req_information.task_count.0 = 1
                req_information.lprocs.0 = 1
                req_information.thread_usage_policy.0 = allowthreads
                req_information.hostlist.0 = ac-d160-0-0:ppn=1
                req_information.task_usage.0.task.0.cpu_list = 0
                req_information.task_usage.0.task.0.mem_list = 0
                req_information.task_usage.0.task.0.cores = 0
                req_information.task_usage.0.task.0.threads = 1
                req_information.task_usage.0.task.0.host = ac-d160-0-0
                copy_on_rerun = False

        """
        query = f"{self.poll_command} {self.jobid}"

        logger.debug(f"Polling job by running: {query}")
        cmd = BuildTestCommand(query)
        cmd.execute()
        output = " ".join(cmd.get_output())

        pattern = r"^Job Id:\s*(?P<jobid>\S+)"
        jobid_match = re.search(pattern, output, re.MULTILINE)
        logger.debug(
            f"Extracting Job ID from output of command: {query} by applying regular expression pattern: '{pattern}'. The return value is {jobid_match}"
        )
        if jobid_match:
            self.jobid = jobid_match.group("jobid")
        else:
            raise JobSchedulerError(
                f"Unable to extract Job ID from output of qstat command: {query}"
            )

        # job_data = json.loads(output)
        pattern = r"^\s*job_state = (?P<state>[A-Z])"
        state_match = re.search(pattern, output, re.MULTILINE)

        """
        if not state_match:
            self.log(f'Job state not found (job info follows):\n{output}')
            continue
        """

        self._state = state_match.group("state")

        pattern = r"^\s*exit_status = (?P<code>\d+)"
        exitcode_match = re.search(pattern, output, re.MULTILINE)

        logger.debug(
            f"Retrieving exitcode for Job: {self.jobid} by applying regular expression pattern: '{pattern}'. The return value is {exitcode_match}"
        )
        if exitcode_match:
            self._exitcode = int(exitcode_match.group("code"))
            logger.debug(f"Retrieve exitcode: {self._exitcode} for Job: {self.jobid}")

        # ---- Get output and error files ----
        self.is_output_ready()

        # if job is running and the start time is not recorded then we record the start time
        if self.is_running() and not self.starttime:
            self.starttime = time.time()

    def retrieve_jobdata(self):
        """This method is called once job is complete. We will gather record of job by running
        ``qstat -x -f -F json <jobid>`` and return the json object as a dict.  This method is responsible
        for getting output file, error file and exit status of job.
        """

        query = f"{self.poll_command} -F json {self.jobid}"
        logger.debug(f"Retrieving job data by running: {query}")
        cmd = BuildTestCommand(query)
        cmd.execute()
        output = " ".join(cmd.get_output())
        job_data = json.loads(output)

        logger.debug(f"Retrieved job data for job: {self.jobid}:\n{job_data}")

        return job_data

    def cancel(self):
        """Cancel PBS job by running ``qdel <jobid>``."""
        query = f"{self.qdel_cmd} {self.jobid}"
        logger.debug(f"Cancelling job {self.jobid} by running: {query}")
        cmd = BuildTestCommand(query)
        cmd.execute()


class TorqueJob(PBSJob):

    def __init__(self, jobID, sched_cmds):
        self._outfile = None
        self._errfile = None
        super().__init__(jobID, sched_cmds)
        self.qdel_cmd = sched_cmds["qdel"]
        # need to redeclare this since we are using qstat -f and not qstat -xf (PBS)
        self.poll_command = f"{sched_cmds['qstat']} -f"

    def retrieve_jobdata(self):
        """This method is called once job is complete. We will gather record of job by running
        `qstat -f <jobid>` and return the output as a string.
        """
        query = f"{self.poll_command} {self.jobid}"
        logger.debug(f"Retrieving job data by running: {query}")
        cmd = BuildTestCommand(query)
        cmd.execute()
        output = " ".join(cmd.get_output())

        logger.debug(f"Retrieved job data for job: {self.jobid}:\n{output}")

        return output
