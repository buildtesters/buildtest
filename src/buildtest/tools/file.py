############################################################################
#
#  Copyright 2017-2019
#
#  https://github.com/HPC-buildtest/buildtest-framework
#
#  This file is part of buildtest.
#
#  buildtest is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  buildtest is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with buildtest.  If not, see <http://www.gnu.org/licenses/>.
#############################################################################


"""
This module provides some generic file and directory level operation that
include the following:
1. Check if File and Directory exist
2. Create File and Directory
3. Check if string is in file
4. Walk a directory tree based on single and multiple extension
5. Strip Hidden file character
"""

import os
import logging

from buildtest.tools.config import logID
from buildtest.tools.log import BuildTestError


def is_file(file):
    """ This method will check if a directory exist and return True if found
            otherwise throw an error."""
    if not os.path.isfile(file):
        raise BuildTestError("Invalid File Path %s. " % file)


def is_dir(dir):
    """ This method will check if a directory exist and return True if found
        otherwise throw an error."""
    if not os.path.isdir(dir):
        raise BuildTestError("Invalid Directory Path %s" % dir)
    return True


def walk_tree(root_dir, ext):
    """ This method will traverse a directory tree and return list of files
        based on extension type."""
    list_files = []
    is_dir(root_dir)
    for root, subdir, files in os.walk(root_dir):
        for file in files:
            if file.endswith(ext):
                list_files.append(os.path.join(root, file))

    return list_files


def walk_tree_multi_ext(root_dir, ext_list):
    """ This method will traverse a directory tree and return list of files
        based on extension type where extension is a list of extension types."""
    list_files = []
    is_dir(root_dir)
    for root, subdir, files in os.walk(root_dir):
        for file in files:
            # return a list of True, False based on file extension
            ext_bool_list = [file.endswith(ext) for ext in ext_list]
            if any(ext_bool_list):
                list_files.append(os.path.join(root, file))

    return list_files


def create_file(filename):
    """Create an empty file if it doesn't exist."""
    logger = logging.getLogger(logID)
    if not os.path.isfile(filename):
        try:
            fd=open(filename,'w')
            logger.debug("Creating File: %s", filename)
            fd.close()
        except OSError as err:
            print (err)


def create_dir(dirname):
    """Create directory if it doesn't exist."""
    logger = logging.getLogger(logID)
    if not os.path.isdir(dirname):
        try:
            os.makedirs(dirname)
            logger.debug("Creating Directory: %s", dirname)
        except OSError as err:
            print (err)
            raise


def string_in_file(string, filename):

    """ Returns True/False to indicate if string is in file."""
    if string in open(filename).read():
        return True
    else:
        return False
