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
This python module provides some generic file level operation such as creating
file, and directory and strip hidden file character. This module also
provides function to update log file, check if file is hidden and determine
if a string is found in file

:author: Shahzeb Siddiqui (Pfizer)
"""
import os
import logging
from datetime import datetime

from buildtest.tools.config import logID

def stripHiddenFile(file):
    """  removes the leading "." character from file """
    file=file[1:]
    return file

def create_file(filename):
    """ Create an empty file if it doesn't exist   """
    logger = logging.getLogger(logID)
    if not os.path.isfile(filename):
        try:
            fd=open(filename,'w')
            logger.debug("Creating File: %s", filename)
            fd.close()
        except OSError as err:
            print (f"{err}")

def create_dir(dirname):
    """Create directory if it doesn't exist"""
    logger = logging.getLogger(logID)
    if not os.path.isdir(dirname):
        try:
            os.makedirs(dirname)
            logger.debug("Creating Directory: %s", dirname)
        except OSError as err:
            print (f"{err}")
            raise




def string_in_file(string,filename):
    """ returns true/false to indicate if string is in file """
    if string in open(filename).read():
        return True
    else:
        return False

def isHiddenFile(inputfile):
    """ Return true/false to indicate if its a hidden file """

    if os.path.isdir(inputfile) == True:
        return False

    cmd = "basename " + inputfile
    filename=os.popen(cmd).read().strip()
    if filename[0] == ".":
        return True
    else:
        return False
