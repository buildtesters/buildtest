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

from shutil import copyfile
import os
def generate_job(testpath,shell_type, jobtemplate):

        jobname = os.path.splitext(testpath)[0]
        jobext = os.path.splitext(jobtemplate)[1]
        jobname += jobext
        copyfile(jobtemplate,jobname)
        fd = open(jobname,'a')
        cmd  = shell_type + " " + testpath
        fd.write(cmd)
        fd.close()

