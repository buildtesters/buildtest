"""
This module detects System changes defined in class BuildTestSystem.
"""

import getpass
import json
import logging
import os
import platform
import shutil
import sys

import distro
from buildtest.defaults import BUILDTEST_ROOT
from buildtest.exceptions import BuildTestError
from buildtest.utils.command import BuildTestCommand


class BuildTestSystem:
    """BuildTestSystem is a class that detects system configuration"""

    system = {}
    supported_platforms = ["Linux", "Darwin"]

    def __init__(self):
        """Constructor method for BuildTestSystem(). Defines all system
        configuration using class variable **system** which is a dictionary.
        """

        self.logger = logging.getLogger(__name__)

        self.check()

    def get(self):
        return self.system

    def check(self):
        """Based on the module "distro" get system details like linux distro,
        processor, hostname, etc...
        """

        self.logger.debug("Starting System Compatibility Check")
        """
        microarch = archspec.cpu.detect.host()
        self.system["model"] = archspec.cpu.detect.raw_info_dictionary()["model name"]
        self.system["arch"] = microarch.name
        self.system["vendor"] = microarch.vendor
        self.system["features"] = " ".join(list(microarch.features))
        """

        self.system["platform"] = platform.system()
        if self.system["platform"] not in self.supported_platforms:
            print(
                f"We have detected the following platform: {platform.system()}, however buildtest is supported on following platforms: {self.supported_platforms}."
            )
            sys.exit(1)

        self.system["os"] = distro.id()
        self.system["cpus"] = os.cpu_count()
        self.system["user"] = getpass.getuser()
        self.system["python"] = os.getenv("BUILDTEST_PYTHON")
        self.system["pyver"] = platform.python_version()
        self.system["processor"] = platform.processor()
        self.system["host"] = platform.node()
        self.system["machine"] = platform.machine()

        self.logger.debug(f"Machine: {self.system['machine']}")
        self.logger.debug(f"Host: {self.system['host']}")
        self.logger.debug(f"User: {self.system['user']}")
        self.logger.debug(f"Operating System: {self.system['os']}")
        self.logger.debug(
            f"System Kernel: {platform.uname().system} and Kernel Release: {platform.uname().release}"
        )
        self.logger.debug(f"Python Path: {self.system['python']}")
        self.logger.debug(f"Python Version: {self.system['pyver']}")
        self.logger.debug(f"BUILDTEST_ROOT: {BUILDTEST_ROOT}")
        self.logger.debug(f"Path to Buildtest: {shutil.which('buildtest')}")

        self.detect_module_tool()
        self.check_scheduler()

        self.logger.debug("Finished System Compatibility Check")

    def check_scheduler(self):
        """Check existence of batch scheduler and if so determine which scheduler
        it is. Currently we support Slurm, LSF, and Cobalt we invoke each
        class and see if its valid state. The checks determine if scheduler
        binaries exist in $PATH.
        """

        slurm = Slurm()
        lsf = LSF()
        cobalt = Cobalt()
        pbs = PBS()

        # the "scheduler" property is used with run_only section in buildspecs for
        # running test based on scheduler.
        self.system["scheduler"] = []

        if slurm.state:
            self.logger.debug("Detected Slurm Scheduler")
            self.system["scheduler"].append("slurm")

        if lsf.state:
            self.logger.debug("Detected LSF Scheduler")
            self.system["scheduler"].append("lsf")

        if cobalt.state:
            self.logger.debug("Detected Cobalt Scheduler")
            self.system["scheduler"].append("cobalt")

        if pbs.state:
            self.logger.debug("Detected PBS Scheduler")
            self.system["scheduler"].append("pbs")

    def detect_module_tool(self):
        """Check if module tool exists, we check for Lmod or environment-modules by
        checking if environment variable ``LMOD_VERSION``, ``MODULE_VERSION`` or
        ``MODULES_CMD`` exist. We check this with input specification in buildtest
        configuration. If user specifies lmod as the module tool but detected
        environment-modules, buildtest should pick this up and report this as part
        of configuration check
        """

        self.system["moduletool"] = None
        lmod_version = os.getenv("LMOD_VERSION")
        # 3.x module versions define MODULE_VERSION while 4.5 version has MODULES_CMD, it doesn't have MODULE_VERSION set
        environmodules_version = os.getenv("MODULE_VERSION") or os.getenv("MODULES_CMD")

        if lmod_version:
            self.system["moduletool"] = "lmod"
            self.logger.debug(f"Detected Lmod with version: {lmod_version}")

        if environmodules_version:
            self.system["moduletool"] = "environment-modules"
            self.logger.debug(
                f"Detected environment-modules with version: {environmodules_version}"
            )


class Scheduler:
    """This is a base Scheduler class used for implementing common methods for
    detecting Scheduler details. The subclass implement specific queries that
    are scheduler specific. The ``Slurm``, ``LSF``, ``PBS`` and ``Cobalt`` class inherit
    from Base Class ``Scheduler``.
    """

    logger = logging.getLogger(__name__)

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
        return hasattr(self, "queues")


class Slurm(Scheduler):
    """The Slurm class implements common functions to query Slurm cluster
    including partitions, qos, cluster. We check existence of slurm binaries
    in $PATH and return if slurm cluster is in valid state.
    """

    # specify a set of Slurm commands to check for file existence
    binaries = ["sbatch", "sacct", "sacctmgr", "sinfo", "scancel"]

    def __init__(self):

        self.logger = logging.getLogger(__name__)

        self.state = self.check_binaries(self.binaries)

        # retrieve slurm partitions, qos, and cluster only if slurm is detected.
        if self.state:
            self.partitions = self._get_partitions()
            self.clusters = self._get_clusters()
            self.qos = self._get_qos()

    def active(self):
        """Slurm scheduler is active if we are able to retrieve partitions or qos from scheduler. This method
        will return a boolean type where ``True`` indicates that slurm executors can be validated."""

        return hasattr(self, "partitions") or hasattr(self, "qos")

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

        query = "sinfo -a -h -O partitionname"
        cmd = BuildTestCommand(query)
        cmd.execute()
        out = cmd.get_output()

        self.logger.debug(f"Get all Slurm Partitions by running: {query}")
        partitions = [partition.rstrip() for partition in out]
        return partitions

    def _get_clusters(self):
        """Get list of slurm clusters by running ``sacctmgr list cluster -P -n format=Cluster``.
        The output is a list of slurm clusters something as follows

        .. code-block:: console

             $ sacctmgr list cluster -P -n format=Cluster
             cori
             escori

        """

        query = "sacctmgr list cluster -P -n format=Cluster"
        cmd = BuildTestCommand(query)
        cmd.execute()
        out = cmd.get_output()

        self.logger.debug(f"Get all Slurm Clusters by running: {query}")
        slurm_clusters = [clustername.rstrip() for clustername in out]
        return slurm_clusters

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

        query = "sacctmgr list qos -P -n  format=Name"
        cmd = BuildTestCommand(query)
        cmd.execute()
        out = cmd.get_output()

        self.logger.debug(f"Get all Slurm Quality of Service (QOS) by running: {query}")
        slurm_qos = [qos.rstrip() for qos in out]
        return slurm_qos


class LSF(Scheduler):
    """The LSF class checks for LSF binaries and returns a list of LSF queues"""

    # specify a set of LSF commands to check for file existence
    binaries = ["bsub", "bqueues", "bkill", "bjobs"]

    def __init__(self):

        self.logger = logging.getLogger(__name__)

        self.state = self.check_binaries(self.binaries)

        # retrieve LSF queues if LSF is detected
        if self.state:
            self.queues = self._get_queues()

    def _get_queues(self):
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

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.state = self.check_binaries(self.binaries)

        if self.state:
            self.queues = self._get_queues()

    def _get_queues(self):
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
        self.state = self.check(self.binaries)

        if self.state:
            self.queues = self._get_queues()

    def check(self, binaries):

        binary_validation = super().check_binaries(binaries)

        if not binary_validation:
            return False

        # check output of qsub --version to see if it contains string 'pbs_version' I
        # [pbsuser@pbs tmp]$ qsub --version
        # pbs_version = 19.0.0
        cmd = BuildTestCommand("qsub --version")
        cmd.execute()
        out = " ".join(cmd.get_output())

        if not out.startswith("pbs_version"):
            return False

        return True

    def _get_queues(self):
        """Get queue configuration using ``qstat -Q -f -F json`` and retrieve a
        list of queues.
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
