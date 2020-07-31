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
    """BuildTestSystem is a class that detects system configuration and outputs the result
       in .run file which are generated upon test execution. This module also keeps
       track of what is supported (or not supported) for a system.
    """

    system = {}

    def __init__(self):
        """Constructor method for BuildTestSystem(). Defines all system configuration using
           class variable **system** which is a dictionary
        """
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Starting System Compatibility Check")
        self.init_system()
        self.system["platform"] = platform.system()
        self.scheduler = self.check_scheduler()
        self.check_lmod()

        if self.system["platform"] not in ["Linux", "Darwin"]:
            print("System must be Linux")
            sys.exit(1)

        self.logger.debug("Finished System Compatibility Check")

    def init_system(self):
        """Based on the module "distro" set the linux distrubution name and version
        """

        self.system["os"] = " ".join(distro.linux_distribution())

        self.system["env"] = dict(os.environ)
        self.system["python"] = shutil.which("python")
        self.system["pyver"] = platform.python_version()
        self.system["processor"] = platform.processor()
        self.system["host"] = platform.node()
        self.system["machine"] = platform.machine()
        self.logger.debug(f"Operating System: {self.system['os']}")
        self.logger.debug(f"Python Path: {self.system['python']}")

    def check_lmod(self):
        """Check if the system has Lmod installed, determine by setting
           of LMOD_DIR variable
        """
        # Boolean to indicate there is lmod support
        self.lmod = "LMOD_DIR" in os.environ and os.path.exists(
            os.environ.get("LMOD_DIR", "")
        )
        self.logger.debug(f"LMOD_DIR: {self.lmod}")

    def check_scheduler(self):
        """Check for batch scheduler. Currently checks for LSF or SLURM by running
           ``bhosts`` and ``sinfo`` command. It must be present in $PATH when running buildtest.
           Since it's unlikely for a single host to have more than one scheduler,
           we check for multiple and return the first found.

           :return: return string **LSF** or **SLURM**. If neither found returns **None**
           :rtype: str or None
        """
        # Assue we don't have either installed to start
        lsf_ec_code = 255
        slurm_ec_code = 255

        if shutil.which("bhosts"):
            lsf_cmd = BuildTestCommand("bhosts")
            lsf_cmd.execute()
            lsf_ec_code = lsf_cmd.returncode

        elif shutil.which("sinfo"):
            slurm_cmd = BuildTestCommand("sinfo")
            slurm_cmd.execute()
            slurm_ec_code = slurm_cmd.returncode

        if slurm_ec_code == 0:
            return "SLURM"
        if lsf_ec_code == 0:
            return "LSF"


def get_slurm_partitions():
    """Get slurm partitions"""

    # get list of partitions
    query = "sinfo -a -h -O partitionname"
    cmd = BuildTestCommand(query)
    cmd.execute()
    out = cmd.get_output()

    partitions = [partition.rstrip() for partition in out]
    return partitions


def get_slurm_clusters():

    query = "sacctmgr list cluster -P -n format=Cluster"
    cmd = BuildTestCommand(query)
    cmd.execute()
    out = cmd.get_output()

    slurm_clusters = [clustername.rstrip() for clustername in out]
    return slurm_clusters


def get_slurm_qos():
    """Return all slurm qos"""
    query = "sacctmgr list qos -P -n  format=Name"
    cmd = BuildTestCommand(query)
    cmd.execute()
    out = cmd.get_output()
    slurm_qos = [qos.rstrip() for qos in out]
    return slurm_qos


def get_lsf_queues():
    """Return json dictionary of available LSF Queues and their queue states"""

    query = "bqueues -o 'queue_name status' -json"
    cmd = BuildTestCommand(query)
    cmd.execute()
    out = cmd.get_output()
    json_queue = json.loads(out)
    return json_queue
