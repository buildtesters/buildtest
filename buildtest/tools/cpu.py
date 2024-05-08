import platform

import archspec.cpu
import psutil


def cpuinfo():
    """Return CPU information using archspec and psutil library"""

    cpu_details = {}

    cpu_details["arch"] = archspec.cpu.host().name
    cpu_details["vendor"] = archspec.cpu.host().vendor
    cpu_details["model"] = archspec.cpu.brand_string()
    cpu_details["platform"] = platform.machine()
    cpu_details["cpu"] = psutil.cpu_count(logical=False)
    cpu_details["vcpu"] = psutil.cpu_count(logical=True)
    cpu_details["virtualmemory"] = {}
    cpu_details["virtualmemory"]["used"] = psutil.virtual_memory().used
    cpu_details["virtualmemory"]["total"] = psutil.virtual_memory().total
    cpu_details["virtualmemory"]["available"] = psutil.virtual_memory().available
    cpu_details["virtualmemory"]["free"] = psutil.virtual_memory().free

    return cpu_details
