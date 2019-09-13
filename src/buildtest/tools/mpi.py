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


def openmpi_opt_table(opts):
    """Translate openmpi YAML keys to mpirun options.

    :param opts: dictionary from "openmpi" key that translates to options for orterun
    :type opts: dict, required

    :return: a list of options from orterun
    :rtype: list
    """
    opt_table = {
        "n": "-n",
        "npernode": "-npernode",
        "npersocket": "-npersocket",
        "report-bindings": "--report-bindings",
        "display-devel-map": "--display-devel-map",
        "display-map": "--display-map",
    }

    val_list = []
    # check if mpirun option
    for opt in opts:
        if opt in opt_table:
            val_list.append(opt_table[opt])

    return val_list

def mpich_opt_table(opts):
    """Translate mpich YAML keys to mpiexec.hydra options

    :param opts: dictionary from "mpich" key that translates to options for mpicexec.hydra
    :type opts: dict, required

    :return: a list of options from mpiexec.hydra
    :rtype: list
    """
    opt_table = {
        "n": "-n",
    }

    val_list = []
    # check if mpirun option
    for opt in opts:
        if opt in opt_table:
            val_list.append(opt_table[opt])

    return val_list