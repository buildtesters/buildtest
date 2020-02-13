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
    BUILDTEST_SYSTEM,
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
        self.system["KERNEL_RELEASE"] = platform.release()
        self.system["PROCESSOR_FAMILY"] = platform.processor()
        self.system["HOSTNAME"] = platform.node()
        self.system["PYTHON_VERSION"] = platform.python_version()
        self.system["PLATFORM"] = platform.platform()
        self.system["LIBC_VERSION"] = platform.libc_ver()[1]
        self.system["SCHEDULER"] = self.check_scheduler()
        if self.system["SYSTEM"] == "Linux":
            # logger.debug("Trying to determine total memory size on Linux via /proc/meminfo")
            meminfo = open("/proc/meminfo").read()

            mem_mo = re.match(r"^MemTotal:\s*(\d+)\s*kB", meminfo, re.M)
            if mem_mo:
                self.system["MEMORY_TOTAL"] = int(mem_mo.group(1)) / 1024

        cmd = BuildTestCommand()

        cmd.which("python")
        self.system["PYTHON"] = cmd.get_output().rstrip()

        if self.system["SCHEDULER"] == "LSF":
            from buildtest.tools.lsf import get_lsf_configuration

            self.system["LSF"] = get_lsf_configuration()
        if self.system["SCHEDULER"] == "SLURM":
            from buildtest.tools.slurm import get_slurm_configuration

            self.system["SLURM"] = get_slurm_configuration()

        cmd.execute("""lscpu | grep "Vendor" """)
        vendor_name = cmd.get_output()

        cmd.execute("""lscpu | grep "Model:" | cut -b 10-""")
        model_hex = hex(int(cmd.get_output()))

        if "GenuineIntel" in vendor_name:
            self.system["VENDOR"] = "Intel"
            arch = intel_cpuid_lookup(model_hex)
        self.system["ARCH"] = arch

        self.get_modules()



        if not os.path.exists(BUILDTEST_SYSTEM):
            with open(BUILDTEST_SYSTEM, "w") as outfile:
                json.dump(self.system, outfile, indent=2, sort_keys=True)

    def get_system(self):
        """Return class variable system that contains detail for system configuration

        :return: return ``self.system``
        :rtype: dict
        """

        return self.system

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

    def get_modules(self):
        """"""
        module_dict = module_obj.get_module_spider_json()
        module_version = module_obj.get_version()
        module_major_version = module_version[0]
        keys = module_dict.keys()
        json_dict = {}
        for key in keys:
            json_dict[key] = {}
            for mpath in module_dict[key].keys():
                if module_major_version == 6:
                    fullname = module_dict[key][mpath]["full"]
                    parent = module_dict[key][mpath]["parent"]
                else:
                    fullname = module_dict[key][mpath]["fullName"]
                    if "parentAA" not in module_dict[key][mpath]:
                        parent = []
                    else:
                        parent = module_dict[key][mpath]["parentAA"]

                json_dict[key][mpath] = {}
                json_dict[key][mpath]["fullName"] = fullname
                json_dict[key][mpath]["parent"] = []
                if module_major_version == 6:
                    for entry in parent:
                        json_dict[key][mpath]["parent"].append(entry.split(":")[1:])
                else:
                    json_dict[key][mpath]["parent"] = parent

        create_dir(os.path.dirname(BUILDTEST_MODULE_FILE))
        with open(BUILDTEST_MODULE_FILE, "w") as outfile:
            json.dump(json_dict, outfile, indent=4)


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


def intel_cpuid_lookup(model):
    """Lookup table to map Module Number to Architecture."""

    # Intel based : https://software.intel.com/en-us/articles/intel-architecture-and-processor-identification-with-cpuid-model-and-family-numbers
    model_numbers = {
        "0x55": "SkyLake",
        "0x4f": "Broadwell",
        "0x57": "KnightsLanding",
        "0x3f": "Haswell",
        "0x46": "Haswell",
        "0x3e": "IvyBridge",
        "0x3a": "IvyBridge",
        "0x2a": "SandyBridge",
        "0x2d": "SandyBridge",
        "0x25": "Westmere",
        "0x2c": "Westmere",
        "0x2f": "Westmere",
        "0x1e": "Nehalem",
        "0x1a": "Nehalem",
        "0x2e": "Nehalem",
        "0x17": "Penryn",
        "0x1D": "Penryn",
        "0x0f": "Merom",
    }
    if model in model_numbers:
        return model_numbers[model]
    else:
        print(f"Unable to find model {model}")
