"""
This module detects System changes defined in class BuildTestSystem.
"""

import getpass
import logging
import os
import platform
import shutil
import socket

import distro

from buildtest.defaults import BUILDTEST_ROOT
from buildtest.exceptions import BuildTestError
from buildtest.scheduler.detection import LSF, PBS, Cobalt, Slurm, Torque

SUPPORTED_PLATFORMS = ["Linux", "Darwin"]

SCHEDULERS = [Slurm, LSF, Cobalt, PBS, Torque]


class BuildTestSystem:
    """BuildTestSystem is a class that detects system configuration"""

    system = {}

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

        self.system["platform"] = platform.system()
        if self.system["platform"] not in SUPPORTED_PLATFORMS:
            raise BuildTestError(
                f"We have detected the following platform: {platform.system()}, however buildtest is supported on following platforms: {SUPPORTED_PLATFORMS}."
            )

        self.system["os"] = distro.id()
        self.system["cpus"] = os.cpu_count()
        self.system["user"] = getpass.getuser()
        self.system["python"] = os.getenv("BUILDTEST_PYTHON")
        self.system["pyver"] = platform.python_version()
        self.system["processor"] = platform.processor()
        self.system["host"] = socket.getfqdn()
        self.system["machine"] = platform.machine()

        self.logger.info(f"Machine: {self.system['machine']}")
        self.logger.info(f"Host: {self.system['host']}")
        self.logger.info(f"User: {self.system['user']}")
        self.logger.info(f"Operating System: {self.system['os']}")
        self.logger.info(
            f"System Kernel: {platform.uname().system} and Kernel Release: {platform.uname().release}"
        )
        self.logger.info(f"Python Path: {self.system['python']}")
        self.logger.info(f"Python Version: {self.system['pyver']}")
        self.logger.info(f"BUILDTEST_ROOT: {BUILDTEST_ROOT}")
        self.logger.info(f"Path to Buildtest: {shutil.which('buildtest')}")

        self.detect_module_tool()
        self.check_scheduler()

        self.logger.info("Finished System Compatibility Check")

    def check_scheduler(self):
        """Check existence of batch scheduler and if so determine which scheduler
        it is. Currently, we support Slurm, LSF, Cobalt, PBS and Torque. We invoke each
        class and see if its valid state. The checks determine if scheduler
        binaries exist in $PATH.
        """

        for scheduler in SCHEDULERS:
            sched = scheduler()
            if sched.active():
                self.logger.debug(f"Detected {sched.__class__.__name__} Scheduler")

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
            self.logger.info("Detected module system: lmod")
            self.logger.info(f"Detected Lmod with version: {lmod_version}")

        if environmodules_version:
            self.system["moduletool"] = "environment-modules"
            self.logger.info("Detected module system: environment-modules")
            self.logger.info(
                f"Detected environment-modules with version: {environmodules_version}"
            )
