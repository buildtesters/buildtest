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

import textwrap
import os
import yaml
from buildtest.tools.config import show_configuration, config_opts
from buildtest.tools.yaml import KEY_DESCRIPTION, SLURM_KEY_DESC, \
    LSF_KEY_DESC, MPI_KEY_DESC, ORTERUN_KEY_DESC, MPIEXEC_KEY_DESC
from buildtest.tools.file import walk_tree

def func_show_subcmd(args):
    """Entry point to show sub command."""
    if args.config:
        show_configuration()

    if args.keys:
        show_yaml_keys()


def show_yaml_keys():
    """Implements buildtest show -k. This method display the yaml keys
     for a particular testblock."""

    print ('{:>50}'.format("General Keys"))

    print ('{:20} | {:<30}'.format("Keys", "Description"))
    print('{:-<100}'.format(""))
    for k in sorted(KEY_DESCRIPTION):
        print('{:20} | {:<30}'.format(k, textwrap.fill(KEY_DESCRIPTION[k], 120)))

    # ---------------------------------------------------
    print()
    print ('{:>50}'.format("LSF Keys"))
    print()
    print ('{:20} | {:<30} | {:<30}'.format("Keys",
                                            "LSF Equivalents",
                                            "Description"))
    print('{:-<100}'.format(""))
    for k in sorted(LSF_KEY_DESC):
        print('{:20} | {:<30} | {:<30}'.format(k,
                                        textwrap.fill(LSF_KEY_DESC[k][0],120),
                                        textwrap.fill(LSF_KEY_DESC[k][1],120)))

    # ---------------------------------------------------
    print()
    print ('{:>50}'.format("SLURM Keys"))
    print()
    print ('{:20} | {:<30} | {:<30}'.format("Keys",
                                            "Slurm Equivalents",
                                            "Description"))
    print('{:-<100}'.format(""))
    for k in sorted(SLURM_KEY_DESC):
        print('{:20} | {:<30} | {:<30}'.format(k,
                                    textwrap.fill(SLURM_KEY_DESC[k][0],120),
                                    textwrap.fill(SLURM_KEY_DESC[k][1],120)))

    # ---------------------------------------------------
    print()
    print ('{:>50}'.format("MPI Keys"))
    print()
    print ('{:20} | {:<30} | {:<30}'.format("Keys",
                                            "MPI Launchers",
                                            "Description"))
    print('{:-<100}'.format(""))
    for k in sorted(MPI_KEY_DESC):
        print('{:20} | {:<30} | {:<30}'.format(k,
                                    textwrap.fill(MPI_KEY_DESC[k][0],120),
                                    textwrap.fill(MPI_KEY_DESC[k][1],120)))

    # ---------------------------------------------------
    print()
    print ('{:>50}'.format("ORTERUN Keys"))
    print()
    print ('{:20} | {:<30} | {:<30}'.format("Keys",
                                            "ORTERUN Options",
                                            "Description"))
    print('{:-<100}'.format(""))
    for k in sorted(ORTERUN_KEY_DESC):
        print('{:20} | {:<30} | {:<30}'.format(k,
                                    textwrap.fill(ORTERUN_KEY_DESC[k][0],120),
                                    textwrap.fill(ORTERUN_KEY_DESC[k][1],120)))

    # ---------------------------------------------------
    print()
    print ('{:>50}'.format("MPIEXEC.HYDRA Keys"))
    print()
    print ('{:20} | {:<30} | {:<30}'.format("Keys",
                                            "MPIEXEC.HYDRA Options",
                                            "Description"))
    print('{:-<100}'.format(""))
    for k in sorted(MPIEXEC_KEY_DESC):
        print('{:20} | {:<30} | {:<30}'.format(k,
                                               textwrap.fill(
                                                   MPIEXEC_KEY_DESC[k][0], 120),
                                               textwrap.fill(
                                                   MPIEXEC_KEY_DESC[k][1],
                                                   120)))
def func_show_testconfigs(args):
    yml_files = walk_tree(config_opts['BUILDTEST_CONFIGS_REPO'], ".yml")

    print ('{:60} | {:<30}'.format("Test Configuration Name", "Description"))
    print('{:-<100}'.format(""))

    for f in yml_files:
        fd = open(f,"r")
        config = yaml.safe_load(fd)
        fd.close()


        description = ""

        if "description" in config:
            description = config["description"]
        parent_parent = os.path.basename(os.path.dirname(os.path.dirname(f)))
        parent = os.path.basename(os.path.dirname(f))
        testconfig_name = f"{parent_parent}.{parent}.{os.path.basename(f)}"
        print('{:60} | {:<30}'.format(testconfig_name, textwrap.fill(description, 120)))


