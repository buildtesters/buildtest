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
This module checks if your system is configured with OpenHPC before proceeding
with anything

@author: Shahzeb Siddiqui (shahzebmsiddiqui@gmail.com)
"""

import subprocess
import sys
def check_ohpc():
        packages_required = "ohpc-release"
        cmd = "rpm -q " + packages_required
        ret = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        ret.communicate()

        ret_code = ret.returncode
        if ret_code != 0:
            print(f"This system is not configured with OpenHPC. Package {packages_required} is not installed.")
            sys.exit(0)
