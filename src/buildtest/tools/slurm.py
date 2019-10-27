"""
Methods for Slurm configuration
"""

from buildtest.tools.system import BuildTestCommand

def get_slurm_configuration():
    """This method retrieves slurm queues and compute nodes part of the SLURM cluster.
    Runs ``sinfo`` command to get nodes and slurm partition (queues).

    :return: two list objects that contains list of queues and compute nodes
    :rtype: two lists (queues, compute_nodes)
    """
    slurm = {}
    cmd = BuildTestCommand()
    query = """ sinfo -h -o %n | sort """
    cmd.execute(query)
    out = cmd.get_output()

    compute_nodes = out.split("\n")
    # need to delete last element
    del compute_nodes[-1]


    query = """ sinfo -h -o %R """
    cmd.execute(query)
    out = cmd.get_output()

    queues = out.split("\n")
    del queues[-1]
    slurm["queues"] = queues
    slurm["nodes"] = compute_nodes
    return slurm