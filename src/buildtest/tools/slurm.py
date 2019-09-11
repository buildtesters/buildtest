############################################################################
#
#  Copyright 2017-2019
#
#   https://github.com/HPC-buildtest/buildtest-framework
#
#  This file is part of buildtest.
#
#    buildtest is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    buildtest is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with buildtest.  If not, see <http://www.gnu.org/licenses/>.
#############################################################################

"""
Methods for Slurm configuration
"""

from buildtest.tools.system import BuildTestCommand

def get_slurm_configuration():
    """This method retrieves slurm queues and compute nodes part of the SLURM cluster.
    Runs sinfo command to get nodes and slurm partition (queues).

    :return: two list objects that contains list of queues and compute nodes
    :rtype: two lists (queues, compute_nodes)
    """
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
    return queues,compute_nodes