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
This file generates the job scripts, detects scheduler, and submits jobs to scheduler
"""
from shutil import copyfile
import os
import glob
import subprocess
import sys

from buildtest.tools.config import BUILDTEST_ROOT, BUILDTEST_JOB_EXTENSION, config_opts
from buildtest.tools.system import BuildTestSystem

def submit_job_to_scheduler(suite):
    """ module used to automate batch job submission to scheduler,
    this module is used when passing --submitjob flag. module takes a
    directory or path to a job script"""

    test_dir = os.path.join(config_opts["BUILDTEST_TESTDIR"],"suite",suite)
    system_info = BuildTestSystem()
    system = system_info.get_system()
    if system["SCHEDULER"] == "LSF":
        job_ext = ".lsf"
        job_launcher = "bsub"
    elif system["SCHEDULER"] == "SLURM":
        job_ext = ".slurm"
        job_launcher = "sbatch"

    if os.path.isdir(test_dir):
        for root, dirs, files in os.walk(test_dir):
            for file in files:
                if file.endswith(job_ext):
                    if system["SCHEDULER"] == "LSF":
                        cmd = job_launcher + " < " + os.path.join(root,file)
                    elif system["SCHEDULER"] == "SLURM":
                        cmd = job_launcher + " " + os.path.join(root,file)
                    os.system(cmd)
                    print (f"Submitting Job: {os.path.join(root,file)} to scheduler")
