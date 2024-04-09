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
            self._partitions = self._get_partitions()
            self._clusters = self._get_clusters()
            self._qos = self._get_qos()

    def partitions(self):
        return self._partitions

    def clusters(self):
        return self._clusters

    def qos(self):
        return self._qos

    def run_command(self, query):
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

        return self.run_command("sinfo -a -h -O partitionname")

    def _get_clusters(self):
        """Get list of slurm clusters by running ``sacctmgr list cluster -P -n format=Cluster``.
        The output is a list of slurm clusters something as follows

        .. code-block:: console

             $ sacctmgr list cluster -P -n format=Cluster
             cori
             escori

        """
        return self.run_command("sacctmgr list cluster -P -n format=Cluster")

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

        return self.run_command("sacctmgr list qos -P -n  format=Name")

    def validate_partition(self, slurm_executor):
        """Validate the partition for a given executor.

        Args:
            slurm_executor (dict): The configuration of the executor.

        Returns:
            bool: True if the partition is valid and in 'up' state, False otherwise.
        """

        # if 'partition' key defined check if its valid partition
        if slurm_executor["partition"] not in self._partitions:
            self.logger.error(
                f"Executor Configuration: {json.dumps(slurm_executor, indent=2)}"
            )
            self.logger.error(
                f"executor -  '{slurm_executor['partition']}' is not a valid partition. Please select one of the following partitions: {self._partitions}"
            )
            return False

        self.logger.debug(
            "Slurm partition: {slurm_executor['partition']} is found in list of partitions."
        )
        # check if partition is in 'up' state. If not we raise an error.
        part_state = self.run_command(
            f"sinfo -p {slurm_executor['partition']} -h -O available"
        )

        if part_state != "up":
            self.logger.error(
                f"partition - {slurm_executor['partition']} is in state: {part_state}. It must be in 'up' state in order to accept jobs"
            )
            return False

        return True

    def validate_cluster(self, executor, slurm_executor):
        """This method will validate a cluster for a given executor. If 'cluster' key is defined in slurm executor configuration
        we will check if cluster is valid, if so we return True otherwise we return False.

        Args:
            executor (str): The name of the executor.
            slurm_executor (dict): The configuration of the executor.
        """
        # check if 'cluster' key is valid slurm cluster
        cluster = slurm_executor.get("cluster")
        if cluster is not None and cluster not in self._clusters:
            self.logger.error(
                f"Executor Configuration: {json.dumps(slurm_executor, indent=2)}"
            )
            self.logger.error(
                f"executor - {executor} has invalid slurm cluster - {cluster}. Please select one of the following slurm clusters: {self._clusters}"
            )
            return False
        self.logger.debug(
            f"Slurm cluster: {cluster} is found in list of slurm clusters."
        )
        return True

    def validate_qos(self, executor, slurm_executor):
        """This method will validate a qos for a given executor. If 'qos' key is defined in slurm executor configuration
        we will check if qos is valid, if so we return True otherwise we return False.

        Args:
            executor (str): The name of the executor.
            slurm_executor (dict): The configuration of the executor.
        """
        # check if 'qos' key is valid slurm qos
        qos = slurm_executor["qos"]
        if qos is not None and qos not in self._qos:
            self.logger.error(
                f"executor - {executor} has invalid slurm qos - {qos}. Please select one of the following slurm qos: {self._qos}"
            )
            return False
        self.logger.debug(f"Slurm qos: {qos} is found in list of slurm qos.")
        return True


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

    def validate_queue(self, executor):
        """Validate a LSF queue.

        Args:
            executor (dict): The dictionary containing the LSF executor configuration.
        """

        queue_name = executor["queue"]
        queue_active_state = "Open:Active"

        queue_list = [name["QUEUE_NAME"] for name in self._queues["RECORDS"]]
        if queue_name not in queue_list:
            return False

        for record in self._queues["RECORDS"]:
            # check queue record for Status
            for name in record:
                # skip record until we find matching queue
                if name["QUEUE_NAME"] != queue_name:
                    continue

                queue_state = name["STATUS"]
                # if state not Open:Active we raise error
                if not queue_state == queue_active_state:
                    self.logger.error(
                        f"'{queue_name}' is in state: {queue_state}. It must be in {queue_active_state} state in order to accept jobs"
                    )
                    return False

        return True


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
        self.is_active = self.check()

        if self.is_active:
            self._queues = self.get_queues()

    def check(self):
        """Check if binaries exist in $PATH and run ``qsub --version`` to see output to
        determine if its OpenPBS scheduler. The return will be a boolean type where ``True`` indicates
        the check has passed.

        Output of ``qsub --version`` from OpenPBS scheduler would be as follows, we will search for string `pbs_version`

        [pbsuser@pbs tmp]$ qsub --version
        pbs_version = 19.0.0

        Args:
            binaries (list): list of binaries to check for existence in $PATH
        """

        if not super().check_binaries(self.binaries):
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

    def get_queues(self):
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
        content = " ".join(cmd.get_output())

        self.logger.debug(f"Get PBS Queues details by running '{query}'")
        try:
            queue_summary = json.loads(content)
        except json.JSONDecodeError:
            raise BuildTestError(f"Unable to process PBS Queues when running: '{query}")

        self.logger.debug("PBS Queue Configuration")
        self.logger.debug(json.dumps(queue_summary, indent=2))

        queues = list(queue_summary["Queue"].keys())
        self.logger.debug(
            f"The following queues: {queues} are available in PBS Scheduler."
        )

        return queue_summary

    def validate_queue(self, queue_name):
        """Validate a PBS queue. Return True if queue exists and is enabled and started, False otherwise.

        Args:
            queue_name (str): The name of the queue to validate.
        """
        avail_queues = list(self._queues["Queue"].keys())

        if queue_name not in avail_queues:
            self.logger.error(
                f"PBS queue - '{queue_name}' not in list of available queues: {avail_queues} "
            )
            return False

        self.logger.debug(
            f"PBS queue: {queue_name} is found in list of available queues."
        )

        if (
            self._queues["Queue"][queue_name]["enabled"] != "True"
            or self._queues["Queue"][queue_name]["started"] != "True"
        ):
            self.logger.info(f"PBS Queue Configuration: {queue_name}")
            self.logger.info(json.dumps(self._queues["Queue"][queue_name], indent=2))
            self.logger.error(f"'{queue_name}' not 'enabled' or 'started' properly.")
            return False

        return True


class Torque(PBS):
    """The Torque class is a subclass of PBS class and inherits all methods from PBS class"""

    def check(self):
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

        if not super().check_binaries(self.binaries):
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
            self.logger.debug("Torque Queue Configuration")
            self.logger.debug(json.dumps(queues, indent=2))
            self.logger.debug(f"List of available Queues: {list(queues.keys())}")

        return queues

    def validate_queue(self, torque_executor):
        """This method will validate queue for a given executor. We will check if queue is available
        and check queue configuration to see if queue is enabled and started properly.
        """

        queue = torque_executor["queue"]
        if queue not in self._queues:

            self.logger.error(
                f"Torque queue - '{queue}' not in list of available queues: {list(self._queues)} "
            )
            return False
        self.logger.debug(
            f"Torque queue: {queue} is found in list of available queues."
        )
        if (
            self._queues[queue]["enabled"] != "True"
            or self._queues[queue]["started"] != "True"
        ):
            self.logger.debug(f"Torque Queue Configuration: {queue}")
            self.logger.debug(json.dumps(self._queues[queue], indent=2))
            self.logger.error(f"Queue '{queue}' not 'enabled' or 'started' properly.")
            return False

        return True
