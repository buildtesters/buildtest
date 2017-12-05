############################################################################
#
#  Copyright 2017
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
This file generates the job script
:author: Shahzeb Siddiqui (Pfizer)
"""
from framework.env import BUILDTEST_ROOT
from shutil import copyfile
import os
import glob
def generate_job(testpath,shell_type, jobtemplate):

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

def submit_job_to_scheduler(job_path):

	job_ext = ".lsf"
	job_launcher = "bsub"
	if os.path.isdir(job_path):
		for root, dirs, files in os.walk(job_path):
			for file in files:
				if file.endswith(job_ext):
					cmd = job_launcher + " < " + os.path.join(root,file) 
					os.system(cmd)
				
					print "Submitting Job:", os.path.join(root,file), " to scheduler"
	if os.path.isfile(job_path):
		cmd = job_launcher + " < " + job_path
		os.system(cmd)
		print "Submitting Job:", job_path, " to scheduler"

