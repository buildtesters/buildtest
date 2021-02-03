"""
This module detects System changes defined in class BuildTestSystem.
"""

import distro
import logging
import json
import os
import platform
import shutil
import sys
from buildtest.utils.command import BuildTestCommand


class BuildTestSystem:
    """ BuildTestSystem is a class that detects system configuration and outputs the result
        in .run file which are generated upon test execution. This module also keeps
        track of what is supported (or not supported) for a system.
    """

    system = {}

    def __init__(self):
        """ Constructor method for BuildTestSystem(). Defines all system
            configuration using class variable **system** which is a dictionary.
        """

        self.logger = logging.getLogger(__name__)

    def check(self):
        """ Based on the module "distro" get system details like linux distro,
            processor, hostname, etc...
        """

        self.logger.debug("Starting System Compatibility Check")

        self.system["os"] = distro.id()
        self.system["env"] = dict(os.environ)
        self.system["python"] = shutil.which("python")
        self.system["pyver"] = platform.python_version()
        self.system["processor"] = platform.processor()
        self.system["host"] = platform.node()
        self.system["machine"] = platform.machine()
        self.logger.debug(f"Operating System: {self.system['os']}")
        self.logger.debug(f"Python Path: {self.system['python']}")

        self.system["platform"] = platform.system()
        if self.system["platform"] not in ["Linux", "Darwin"]:
            print("System must be Linux or Darwin")
            sys.exit(1)

        self.detect_module_tool()
        self.check_scheduler()

        self.logger.debug("Finished System Compatibility Check")

    def check_scheduler(self):
        """ Check existence of batch scheduler and if so determine which scheduler
            it is. Currently we support Slurm, LSF, and Cobalt we invoke each
            class and see if its valid state. The checks determine if scheduler
            binaries exist in $PATH.
        """

        slurm = Slurm()
        lsf = LSF()
        cobalt = Cobalt()

        # the "scheduler" property is used with run_only section in buildspecs for
        # running test based on scheduler.
        self.system["scheduler"] = []

        if slurm.get_state():
            self.system["scheduler"] = "slurm"
            return

        if lsf.get_state():
            self.system["scheduler"] = "lsf"
            return

        if cobalt.get_state():
            self.system["scheduler"] = "cobalt"
            return

    def detect_module_tool(self):
        """ Check if module tool exists, we check for Lmod or environment-modules by
            checking if environment variable ``LMOD_VERSION``, ``MODULE_VERSION`` or
            ``MODULES_CMD`` exist. We check this with input specification in buildtest
            configuration. If user specifies lmod as the module tool but detected
            environment-modules, buildtest should pick this up and report this as part
            of configuration check
        """

        self.system["moduletool"] = None

        if os.getenv("LMOD_VERSION"):
            self.system["moduletool"] = "lmod"
            self.logger.debug(
                f"Detected Lmod with version: {os.getenv('LMOD_VERSION')}"
            )
        # 3.x module versions define MODULE_VERSION while 4.5 version has MODULES_CMD, it doesn't have MODULE_VERSION set
        elif os.getenv("MODULE_VERSION") or os.getenv("MODULES_CMD"):
            self.system["moduletool"] = "environment-modules"
            self.logger.debug(
                f"Detected environment-modules with version: {os.getenv('LMOD_VERSION')}"
            )


class Scheduler:
    """ This is a base Scheduler class used for implementing common methods for
        detecting Scheduler details. The subclass implement specific queries that
        are scheduler specific. The ``Slurm``, ``LSF`` and ``Cobalt`` class inherit
        from Base Class ``Scheduler``.
    """

    state = True
    logger = logging.getLogger(__name__)

    def check(self):
        """Check if binaries exist binary exist in $PATH"""

        for command in self.binaries:
            if not shutil.which(command):
                self.logger.debug(f"Cannot find {command} command in $PATH")
                self.state = False

    def get_state(self):
        """Return state of cluster, the return is a boolean to indicate scheduler
        is valid or not.
        """
        return self.state


class Slurm(Scheduler):
    """The Slurm class implements common functions to query Slurm cluster
        including partitions, qos, cluster. We check existence of slurm binaries
        in $PATH and return if slurm cluster is in valid state.
    """

    # all of these commands are used later when submitting, polling or cancelling job
    binaries = ["sbatch", "sacct", "sacctmgr", "sinfo", "scancel"]

    def __init__(self):

        self.logger = logging.getLogger(__name__)

        self.check()
        self.partitions = self.get_partitions()
        self.clusters = self.get_clusters()
        self.qos = self.get_qos()

    def get_partitions(self):
        """Get list of all partitions slurm partitions"""

        # get list of partitions

        query = "sinfo -a -h -O partitionname"
        cmd = BuildTestCommand(query)
        cmd.execute()
        out = cmd.get_output()

        self.logger.debug(f"Get all Slurm Partitions by running: {query}")
        partitions = [partition.rstrip() for partition in out]
        return partitions

    def get_clusters(self):
        """Get list of slurm clusters"""

        query = "sacctmgr list cluster -P -n format=Cluster"
        cmd = BuildTestCommand(query)
        cmd.execute()
        out = cmd.get_output()

        self.logger.debug(f"Get all Slurm Clusters by running: {query}")
        slurm_clusters = [clustername.rstrip() for clustername in out]
        return slurm_clusters

    def get_qos(self):
        """Return a list of all slurm qos"""

        query = "sacctmgr list qos -P -n  format=Name"
        cmd = BuildTestCommand(query)
        cmd.execute()
        out = cmd.get_output()

        self.logger.debug(f"Get all Slurm Quality of Service (QOS) by running: {query}")
        slurm_qos = [qos.rstrip() for qos in out]
        return slurm_qos


class LSF(Scheduler):
    """The LSF class checks for LSF binaries and returns a list of LSF queues"""

    binaries = ["bsub", "bqueues", "bkill", "bjobs"]

    def __init__(self):

        self.logger = logging.getLogger(__name__)

        self.check()
        self.queues = self.get_queues()

    def get_queues(self):
        """Return json dictionary of available LSF Queues and their queue states"""

        query = "bqueues -o 'queue_name status' -json"
        cmd = BuildTestCommand(query)
        cmd.execute()
        out = cmd.get_output()

        self.logger.debug(f"Get all LSF Queues by running {query}")
        # if command returns output, we convert to string and return as json object
        if out:
            out = "".join(cmd.get_output()).rstrip()
            return json.loads(out)


class Cobalt(Scheduler):
    """The Cobalt class checks for Cobalt binaries and gets a list of Cobalt queues"""

    binaries = ["qsub", "qstat", "qdel"]

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.check()
        self.queues = self.get_queues()

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


system = BuildTestSystem()
system.check()