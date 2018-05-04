############################################################################
#
#  Copyright 2017
#
#   https://github.com/HPC-buildtest/buildtest-framework
#
#    This file is part of buildtest.
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
This file sets the buildtest specific environment variables used throughout all
the scripts

:author: Shahzeb Siddiqui (Pfizer)
"""
import os
import yaml

# read the BUILDTEST env vars from the shell environment that is sourced by setup.sh
BUILDTEST_VERSION="0.1.9"
BUILDTEST_ROOT = os.environ['BUILDTEST_ROOT']

BUILDTEST_JOB_EXTENSION = [".lsf", ".slurm", ".pbs"]
BUILDTEST_SHELLTYPES = ["sh", "bash", "csh"]

PYTHON_APPS = ["python","anaconda2", "anaconda3"]
MPI_APPS = ["OpenMPI", "MPICH","MVAPICH2", "intel", "impi"]

#BUILDTEST_DEFAULT_CONFIG=os.path.join(BUILDTEST_ROOT,"config.yaml")
#print BUILDTEST_DEFAULT_CONFIG
#fd = open(BUILDTEST_DEFAULT_CONFIG,'r')
fd = open("config.yaml",'r')
config_opts = yaml.load(fd)

#global logID
logID = "buildtest"
