############################################################################
#
#  Copyright 2017-2018
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

:author: Shahzeb Siddiqui (Pfizer)
"""
from shutil import copyfile
import os
import glob
import subprocess
import sys

from buildtest.tools.config import BUILDTEST_ROOT, BUILDTEST_JOB_EXTENSION, config_opts

def detect_scheduler():
    """ detect scheduler for host system"""
    SCHEDULER_LSF = "LSF"
    SCHEDULER_SLURM = "SLURM"

    cmdlist = ["lsid", "sinfo"]
    for cmd in cmdlist:
        ret = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        ret.communicate()
        errcode = ret.returncode
        if errcode == 0 and cmd == "lsid":
            return SCHEDULER_LSF
        if errcode == 0 and cmd == "sinfo":
            return SCHEDULER_SLURM

def update_job_template(job_template):

    #config_opts['BUILDTEST_JOB_TEMPLATE']=bt_opts.job_template
    if not os.path.isfile(job_template):
        print ("Cant file job template file ", job_template)
        sys.exit(1)

    # checking if extension is job template file extension is valid to detect type of scheduler
    if os.path.splitext(job_template)[1]  not in BUILDTEST_JOB_EXTENSION:
        print ("Invalid file extension, must be one of the following extension %s", BUILDTEST_JOB_EXTENSION)
        sys.exit(1)

    config_opts['BUILDTEST_JOB_TEMPLATE'] = job_template


def generate_job(testpath,shell_type, jobtemplate, config):
    """ generate job script based on template file, shell type and path to
    test file """

    if "scheduler" in config:
        return

    if not os.path.isabs(jobtemplate):
        jobtemplate=os.path.join(BUILDTEST_ROOT,jobtemplate)

    jobname = os.path.splitext(testpath)[0]
    jobext = os.path.splitext(jobtemplate)[1]
    jobname += jobext
    copyfile(jobtemplate,jobname)
    fd = open(jobname,'a')
    test_fd = open(testpath,'r')
    test_content = test_fd.read().splitlines()

    shell_magic = "#!/" + os.path.join("bin",shell_type)
    cmd  = shell_type + " " + testpath

    for line in test_content:
        # need to add shell magic at beginning of line which we will do
        # below
        if line == shell_magic:
                continue
        fd.write(line + "\n")
    fd.close()

    # writing shell_magic as 1st line in job submission script
    with open(jobname,"r+") as f: s = f.read(); f.seek(0); f.write(shell_magic + "\n" + s)

def generate_job_by_config(testpath, shell_type, config):
    """ generate job based on YAML configuration """
    SCHEDULER = ""
    ext = ""

    if config["scheduler"] == "LSF":
        ext = ".lsf"
        SCHEDULER = "LSF"
    elif config["scheduler"] == "SLURM":
        ext = ".slurm"
        SCHEDULER = "SLURM"

    jobname = os.path.splitext(testpath)[0] + ext
    dirname = os.path.dirname(testpath)
    job_path = os.path.join(dirname,jobname)
    fd = open(job_path, 'w')
    shell_magic = "#!/" + os.path.join("bin",shell_type)

    fd.write(shell_magic + "\n")

    if SCHEDULER == "LSF":
        fd.write("#BSUB -n " + str(config["jobslots"]) + "\n")
    elif SCHEDULER == "SLURM":
        fd.write("#SBATCH -N " + str(config["jobslots"]) + "\n")

    # skip 1st line and get the rest of content
    content = open(testpath,'r').readlines()[1:]

    for line in content:
        # don't write shell magic line from test file since it is
        # already written. This is the first line in test script

        fd.write(line)
    fd.close()

def submit_job_to_scheduler(job_path):
    """ module used to automate batch job submission to scheduler,
    this module is used when passing --submitjob flag. module takes a
    directory or path to a job script"""


    SCHEDULER = detect_scheduler()
    if SCHEDULER == "LSF":
        job_ext = ".lsf"
        job_launcher = "bsub"
    elif SCHEDULER == "SLURM":
        job_ext = ".slurm"
        job_launcher = "sbatch"

    if os.path.isdir(job_path):
        for root, dirs, files in os.walk(job_path):
            for file in files:
                if file.endswith(job_ext):
                    cmd = job_launcher + " < " + os.path.join(root,file)
                    os.system(cmd)

                    print ("Submitting Job: ",os.path.join(root,file), " to scheduler")
    if os.path.isfile(job_path):
        if SCHEDULER == "LSF":
            cmd = job_launcher + " < " + job_path
        elif SCHEDULER == "SLURM":
            cmd = job_launcher + " " + job_path

        os.system(cmd)
        print ("Submitting Job:", job_path, " to scheduler ")
