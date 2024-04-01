import json
import logging
import re
import shutil

from buildtest.exceptions import BuildTestError
from buildtest.utils.command import BuildTestCommand


class Scheduler:
    """This is a base Scheduler class used for implementing common methods for
    detecting Scheduler details. The subclass implements specific queries that
    are scheduler specific.
    """

    logger = logging.getLogger(__name__)
    binaries = []

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.is_active = self.check_binaries(self.binaries)
        if self.is_active:
            self._queues = self.get_queues()

    def queues(self):
        return self._queues

    def check_binaries(self, binaries):
        """Check if binaries exist binary exist in $PATH"""

        self.logger.debug(
            f"We will check the following binaries {binaries} for existence."
        )
        for command in binaries:
            if not shutil.which(command):
                self.logger.debug(f"Cannot find {command} command in $PATH")
                return False

            self.logger.debug(f"{command}: {shutil.which(command)}")
        return True

    def active(self):
        """Returns ``True`` if buildtest is able to retrieve queues from Scheduler otherwises returns ``False``"""
        return self.is_active

    def get_queues(self):
        """This method is implemented by subclass to return a list of queues for a given scheduler"""
        raise NotImplementedError


class Slurm(Scheduler):
    """The Slurm class implements common functions to query Slurm cluster
    including partitions, qos, cluster. We check existence of slurm binaries
    in $PATH and return if slurm cluster is in valid state.
    """

    # specify a set of Slurm commands to check for file existence
    binaries = ["sbatch", "sacct", "sacctmgr", "sinfo", "scancel", "scontrol"]

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.is_active = self.check_binaries(self.binaries)

        # retrieve slurm partitions, qos, and cluster only if slurm is detected.
        if self.is_active:
            self.partitions = self._get_partitions()
            self.clusters = self._get_clusters()
            self.qos = self._get_qos()

    def _run_command(self, query):
        """Run a command and return output as list of lines"""
        cmd = BuildTestCommand(query)
        cmd.execute()
        out = cmd.get_output()
        self.logger.debug(f"Running command: {query}")

        return [item.rstrip() for item in out]

    def _get_partitions(self):
        """Get list of all partitions slurm partitions using ``sinfo -a -h -O partitionname``. The output
        is a list of queue names

        .. code-block:: console

             $ sinfo -a -h -O partitionname
             system
             system_shared
             debug_hsw
             debug_knl
             jupyter

        """
        # get list of partitions

        return self._run_command("sinfo -a -h -O partitionname")

    def _get_clusters(self):
        """Get list of slurm clusters by running ``sacctmgr list cluster -P -n format=Cluster``.
        The output is a list of slurm clusters something as follows

        .. code-block:: console

             $ sacctmgr list cluster -P -n format=Cluster
             cori
             escori

        """
        return self._run_command("sacctmgr list cluster -P -n format=Cluster")

    def _get_qos(self):
        """Retrieve a list of all slurm qos by running ``sacctmgr list qos -P -n  format=Name``. The output
        is a list of qos. Shown below is an example output

        .. code-block:: console

            $ sacctmgr list qos -P -n  format=Name
            normal
            premium
            low
            serialize
            scavenger

        """

        return self._run_command("sacctmgr list qos -P -n  format=Name")


class LSF(Scheduler):
    """The LSF class checks for LSF binaries and returns a list of LSF queues"""

    # specify a set of LSF commands to check for file existence
    binaries = ["bsub", "bqueues", "bkill", "bjobs"]

    def get_queues(self):
        """Return json dictionary of available LSF Queues and their queue states.
        The command we run is the following: ``bqueues -o 'queue_name status' -json`` which
        returns a JSON record of all queue details.

        .. code-block:: console

            $ bqueues -o 'queue_name status' -json
                {
                  "COMMAND":"bqueues",
                  "QUEUES":2,
                  "RECORDS":[
                    {
                      "QUEUE_NAME":"batch",
                      "STATUS":"Open:Active"
                    },
                    {
                      "QUEUE_NAME":"test",
                      "STATUS":"Open:Active"
                    }
                  ]
                }

        """

        query = "bqueues -o 'queue_name status' -json"
        cmd = BuildTestCommand(query)
        cmd.execute()
        out = cmd.get_output()

        self.logger.debug(f"Get all LSF Queues by running {query}")
        # if command returns output, we convert to string and return as json object
        if out:
            out = "".join(cmd.get_output()).rstrip()
            try:
                queues = json.loads(out)
            except json.JSONDecodeError:
                raise BuildTestError(
                    f"Unable to process LSF Queues when running: {query}"
                )

        return queues


class Cobalt(Scheduler):
    """The Cobalt class checks for Cobalt binaries and gets a list of Cobalt queues"""

    # specify a set of Cobalt commands to check for file existence
    binaries = ["qsub", "qstat", "qdel", "nodelist", "showres", "partlist"]

    def get_queues(self):
        """Get all Cobalt queues by running ``qstat -Ql`` and parsing output"""

        query = "qstat -Ql"
        cmd = BuildTestCommand(query)
        cmd.execute()
        content = cmd.get_output()

        self.logger.debug(f"Get all Cobalt Queues by running {query}")
        # remove all None from list
        content = list(filter(None, content))

        queues = []
        for line in content:
            if line.startswith("Name"):
                name = line.partition(":")[2].strip()
                queues.append(name)
        return queues


class PBS(Scheduler):
    """The PBS class checks for PBS binaries and gets a list of available queues"""

    # specify a set of PBS commands to check for file existence
    binaries = ["qsub", "qstat", "qdel", "qstart", "qhold", "qmgr"]

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.is_active = self.check(self.binaries)

        if self.is_active:
            self._queues = self.get_queues()

    def check(self, binaries):
        """Check if binaries exist in $PATH and run ``qsub --version`` to see output to
        determine if its OpenPBS scheduler. The return will be a boolean type where ``True`` indicates
        the check has passed.

        Output of ``qsub --version`` from OpenPBS scheduler would be as follows, we will search for string `pbs_version`

        [pbsuser@pbs tmp]$ qsub --version
        pbs_version = 19.0.0

        Args:
            binaries (list): list of binaries to check for existence in $PATH
        """
        binary_validation = super().check_binaries(binaries)

        if not binary_validation:
            return False

        # check output of qsub --version to see if it contains string 'pbs_version'
        # [pbsuser@pbs tmp]$ qsub --version
        # pbs_version = 19.0.0
        qsub_version = "qsub --version"
        cmd = BuildTestCommand(qsub_version)
        cmd.execute()
        out = " ".join(cmd.get_output())

        self.logger.debug(f"Check PBS version by running {qsub_version} command")
        self.logger.debug(f"Output of {qsub_version}: {out}")

        if not out.startswith("pbs_version"):
            self.logger.debug(
                f"Cannot find 'pbs_version' in output of {qsub_version}, this is not a OpenPBS Scheduler"
            )
            return False

        return True

    def _get_queues(self):
        """Get queue configuration using ``qstat -Q -f -F json`` and retrieve a
        list of queues.

        Shown below is an example output of ``qstat -Q -f -F json``

         .. code-block:: console

            $ qstat -Q -f -F json
             {
                 "timestamp":1615924938,
                 "pbs_version":"19.0.0",
                 "pbs_server":"pbs",
                 "Queue":{
                     "workq":{
                         "queue_type":"Execution",
                         "total_jobs":0,
                         "state_count":"Transit:0 Queued:0 Held:0 Waiting:0 Running:0 Exiting:0 Begun:0 ",
                         "resources_assigned":{
                             "mem":"0kb",
                             "ncpus":0,
                             "nodect":0
                         },
                         "hasnodes":"True",
                         "enabled":"True",
                         "started":"True"
                     }
                 }
             }
        """
        query = "qstat -Q -f -F json"
        cmd = BuildTestCommand(query)
        cmd.execute()
        content = cmd.get_output()

        self.logger.debug(f"Get PBS Queues details by running '{query}'")
        try:
            self.queue_summary = json.loads(" ".join(content))
        except json.JSONDecodeError:
            raise BuildTestError(f"Unable to process PBS Queues when running: '{query}")

        self.logger.debug(json.dumps(self.queue_summary, indent=2))

        queues = list(self.queue_summary["Queue"].keys())
        self.logger.debug(f"Available Queues: {queues}")
        return queues


class Torque(PBS):
    """The Torque class is a subclass of PBS class and inherits all methods from PBS class"""

    def check(self, binaries):
        """Check if binaries exist in $PATH and run ``qsub --version`` to see output if its Torque Scheduler.
        The return will be a boolean type where ``True`` indicates the check has passed.

        Output from ``qsub --version`` from Torque scheduler would be as follows, we will search for
        `Commit:` in output to distinguish Torque from OpenPBS

        .. code-block:: console

            $ qsub --version
            Version: 7.0.1
            Commit: b405f8c22d41d29cbf9b9016bc1146bf4559e895

        Args:
            binaries (list): list of binaries to check for existence in $PATH

        """

        if not super().check_binaries(binaries):
            return False

        # check output of qsub --version to see if it contains 'Commit:'
        # (buildtest) adaptive50@e4spro-cluster:$ qsub --version
        # Version: 7.0.1
        # Commit: b405f8c22d41d29cbf9b9016bc1146bf4559e895
        qsub_version = "qsub --version"
        cmd = BuildTestCommand(qsub_version)
        cmd.execute()
        # output goes to error stream
        content = " ".join(cmd.get_error())

        self.logger.debug(f"Check Torque version by running {qsub_version} command")
        self.logger.debug(f"Output of {qsub_version}: %s", content)
        self.logger.debug(f"Check if 'Commit:' exists in output of {qsub_version}")
        match = re.search(r"Commit:\s*(.*)$", content, re.MULTILINE)

        if match:
            self.logger.debug(
                f"Found 'Commit:' in output of {qsub_version}, this must be a Torque Scheduler"
            )
            return True
        return False

    def get_queues(self):
        """Get queue configuration using 'qstat -Qf' and parse the output into a JSON dictionary.
        The output of this command will be as follows

        .. code-block:: console

            $ qstat -Qf
             Queue: lbl-cluster
                 queue_type = Execution
                 total_jobs = 0
                 state_count = Transit:0 Queued:0 Held:0 Waiting:0 Running:0 Exiting:0 Complete:0
                 resources_default.nodes = 1
                 resources_default.walltime = 24:00:00
                 mtime = 1711400391
                 enabled = True
                 started = True

        """

        query = "qstat -Qf"
        cmd = BuildTestCommand(query)
        cmd.execute()
        self.logger.debug(f"Get Torque Queues details by running '{query}'")

        output = " ".join(cmd.get_output())
        self.logger.debug(f"Output of {query}: {output}")
        self.logger.debug(f"Parse output of {query} to get queue details")
        queues = {}
        current_queue = None

        for line in output.split("\n"):
            if line.startswith("Queue:"):
                current_queue = line.split()[1]
                queues[current_queue] = {}
                continue

            if "=" in line:
                key, value = [x.strip() for x in line.split("=", 1)]
                queues[current_queue][key] = value

        if queues:
            self.logger.debug(json.dumps(queues, indent=2))
            self.logger.debug(f"Available Queues: {list(queues.keys())}")

        return queues
