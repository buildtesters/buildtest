"""
Functions for system package
"""


import distro
import json
import os
import platform
import re
import stat
import sys
import subprocess
from buildtest.tools.config import (
    BUILDTEST_MODULE_COLLECTION_FILE,
    BUILDTEST_MODULE_FILE,
    BUILDTEST_BUILD_LOGFILE,
)
from buildtest.tools.file import create_dir, is_file
from buildtest.tools.modules import module_obj


class BuildTestCommand:
    """Class method to invoke shell commands and retrieve output and error. This class
    makes use of **subprocess.Popen()** to run the shell command. This class has no
    **__init__()** method
    """

    ret = []
    out = ""
    err = ""

    def execute(self, cmd):
        """Execute a system command and return output and error

        :param cmd: shell command to execute
        :type cmd: str, required
        :return: Output and Error from shell command
        :rtype: two str objects
        """

        self.ret = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        (self.out, self.err) = self.ret.communicate()
        self.out = self.out.decode("utf-8")
        self.err = self.err.decode("utf-8")
        return (self.out, self.err)

    def which(self, cmd):
        """Run a ``which`` against the command.

        :param cmd: shell command to execute
        :type cmd: str, required
        :return: Output and Error from shell command
        :rtype: two str objects
        """

        which_cmd = "which " + cmd
        self.ret = subprocess.Popen(
            which_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        (self.out, self.err) = self.ret.communicate()
        self.out = self.out.decode("utf-8")
        self.err = self.err.decode("utf-8")
        return (self.out, self.err)

    def returnCode(self):
        """Returns the return code from shell command

        :rtype: int
        """

        return self.ret.returncode

    def get_output(self):
        """Returns the output from shell command

        :rtype: str
        """

        return self.out

    def get_error(self):
        """Returns the error from shell command

        :rtype: str
        """

        return self.err


class BuildTestSystem:
    """BuildTestSystem is a class that detects system configuration and outputs the result
    in .run file which are generated upon test execution."""

    # class variable used for storing system configuration
    system = {}

    def __init__(self):
        """Constructor method for BuildTestSystem(). Defines all system configuration using
        class variable **system** which is a dictionary """

        self.system["OS_NAME"] = distro.linux_distribution(
            full_distribution_name=False
        )[0]

        self.system["OS_VERSION"] = distro.linux_distribution(
            full_distribution_name=False
        )[1]
        self.system["SYSTEM"] = platform.system()

        scheduler = self.check_scheduler()

    def check_scheduler(self):
        """Check for batch scheduler. Currently checks for LSF or SLURM by running
        ``bhosts`` and ``sinfo`` command. It must be present in $PATH when running buildtest.

        :return: return string **LSF** or **SLURM**. If neither found returns **None**
        :rtype: str or None
        """

        lsf_cmd = BuildTestCommand()
        lsf_cmd.execute("bhosts")
        lsf_ec_code = lsf_cmd.returnCode()

        slurm_cmd = BuildTestCommand()
        slurm_cmd.execute("sinfo")
        slurm_ec_code = slurm_cmd.returnCode()

        if lsf_ec_code == 0:
            return "LSF"
        if slurm_ec_code == 0:
            return "SLURM"

        return None

    def check_system_requirements(self):
        """Checking system requirements."""
        req_pass = True
        # If system is not Linux

        if self.system["SYSTEM"] != "Linux" or not is_file(os.getenv("LMOD_CMD")):
            msg = """
System Requirements not satisfied.

Requirements:
1. System must be Linux
2. Lmod must be installed
"""
            print(msg)
            sys.exit(1)


def get_module_collection():
    """Return user Lmod module collection. Lmod collection can be retrieved
    using command: ``module -t savelist``

    :return: list of Lmod module collection
    :rtype: list
    """
    return subprocess.getoutput("module -t savelist").split("\n")


def distro_short(distro_fname):
    """Map Long Linux Distribution Name to short name."""

    if "Red Hat Enterprise Linux Server" == distro_fname:
        return "rhel"
    elif "CentOS" == distro_fname:
        return "centos"
    elif "SUSE Linux Enterprise Server" == distro_fname:
        return "suse"
