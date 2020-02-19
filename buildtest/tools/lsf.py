import json
import os
from buildtest.tools.config import BUILDTEST_BUILD_LOGFILE
from buildtest.tools.system import BuildTestCommand


def get_lsf_configuration():
    """Get LSF configuration such as queues, hosts, resources, host types,
       and models"""
    lsf = {}

    cmd = BuildTestCommand()
    query = """ bqueues | cut -d " " -f 1 """

    cmd.execute(query)
    out = cmd.get_output()

    queue_names = out.split("\n")
    # remove the first and last entry. First entry is just header and last entry is empty string
    del queue_names[0]
    del queue_names[-1]

    query = """ bhosts -w | cut -d " " -f 1 """
    cmd.execute(query)
    out = cmd.get_output()

    compute_nodes = out.split("\n")
    del compute_nodes[0]
    del compute_nodes[-1]

    query = """lsinfo -r | cut -d " " -f 1 """
    cmd.execute(query)
    out = cmd.get_output()

    resources = out.split("\n")
    del resources[0]
    del resources[-1]

    query = """lsinfo -m | cut -d " " -f 1 """
    cmd.execute(query)
    out = cmd.get_output()

    running_models = out.split("\n")
    del running_models[0]
    del running_models[-1]

    query = """lsinfo -t | cut -d " " -f 1 """
    cmd.execute(query)
    out = cmd.get_output()

    host_type = out.split("\n")
    del host_type[0]
    del host_type[-1]

    lsf["queues"] = queue_names
    lsf["nodes"] = compute_nodes
    lsf["resources"] = resources
    lsf["running_models"] = running_models
    lsf["host_type"] = host_type

    return lsf
