"""
Functions for system package
"""

import distro
import os
import platform
import sys
import subprocess

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
        self.init_system()
        self.system["SYSTEM"] = platform.system()
        self.scheduler = self.check_scheduler()
        self.check_lmod()

    def init_system(self):
        """Based on the module "distro" set the linux distrubution name and version
        """
        self.system["OS_NAME"] = distro.linux_distribution(
            full_distribution_name=False
        )[0]
        self.system["OS_VERSION"] = distro.linux_distribution(
            full_distribution_name=False
        )[1]

    def check_lmod(self):
        """Check if the system has Lmod installed, determine by setting
           of LMOD_DIR variable
        """
        # Boolean to indicate there is lmod support
        self.lmod = "LMOD_DIR" in os.environ and os.path.exists(
            os.environ.get("LMOD_DIR", "")
        )

    def check_scheduler(self):
        """Check for batch scheduler. Currently checks for LSF or SLURM by running
          ``bhosts`` and ``sinfo`` command. It must be present in $PATH when running buildtest.
            Since it's unlikely for a single host to have more than one scheduler,
            we check for multiple and return the first found.

           :return: return string **LSF** or **SLURM**. If neither found returns **None**
           :rtype: str or None
        """

        lsf_cmd = BuildTestCommand()
        lsf_cmd.execute("bhosts")
        lsf_ec_code = lsf_cmd.returnCode()

        slurm_cmd = BuildTestCommand()
        slurm_cmd.execute("sinfo")
        slurm_ec_code = slurm_cmd.returnCode()

        if slurm_ec_code == 0:
            return "SLURM"
        if lsf_ec_code == 0:
            return "LSF"

        return None

    def check_system_requirements(self):
        """Checking system requirements."""

        if self.system["SYSTEM"] != "Linux":
            print("System must be Linux")
            sys.exit(1)
