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


def is_file(fname):
    """This method will check if file exist and if not found throws an exception.

    :param file: file path
    :type file: string, required

    :raises BuildTestError: sub-class of Exception
    :return: returns True if file exists otherwise terminates with an exception
    :rtype: True if successful, otherwise throws an exception
    """
    fname = os.path.expandvars(fname)
    fname = os.path.expanduser(fname)
    if os.path.exists(fname):
        return True

    raise BuildTestError("Invalid File Path %s. " % fname)


def is_dir(dirname):
    """This method will check if a directory exist and if not found throws an exception.

    :param dir: directory path
    :type dir: string, required

    :raises BuildTestError: sub-class of Exception
    :return: returns True if directory exists otherwise terminates with an exception
    :rtype: True if successful, otherwise throws an exception
    """

    dirname = os.path.expandvars(dirname)
    dirname = os.path.expanduser(dirname)

    if os.path.isdir(dirname):
        return True

    raise BuildTestError("Invalid Directory Path %s" % dirname)


def walk_tree(root_dir, ext):
    """This method will traverse a directory tree and return list of files
    based on extension type. This method invokes is_dir() to check if directory
    exists before traversal.

    :param root_dir: directory path to traverse
    :type root_dir: string, required
    :param ext: file extensions to search in traversal
    :type ext: string, required

    :return: returns a list of file paths
    :rtype: List
    """
    list_files = []
    is_dir(root_dir)
    for root, subdir, files in os.walk(root_dir):
        for fname in files:
            if fname.endswith(ext):
                list_files.append(os.path.join(root, fname))

    return list_files


def walk_tree_multi_ext(root_dir, ext_list):
    """This method will traverse a directory tree and return list of files
    based on extension type where extension is a list of extension types.
    This method invokes is_dir() to check if directory exists before traversal

    :param root_dir: directory path to traverse
    :type root_dir: string, required
    :param ext_list: list of file extensions to search in traversal
    :type ext: List, required

    :return: returns a list of file paths
    :rtype: List
    """
    list_files = []
    is_dir(root_dir)
    for root, subdir, files in os.walk(root_dir):
        for fname in files:
            # return a list of True, False based on file extension
            ext_bool_list = [fname.endswith(ext) for ext in ext_list]
            if any(ext_bool_list):
                list_files.append(os.path.join(root, fname))

    return list_files


def create_file(filename):
    """Create an empty file if file doesn't exist. Logs details
    in log file. Runs a "try" block to write an empty file, if an
    exception of type OSError then print exception error

    :param filename: file name to create
    :type filename: str, required

    :return: writes an empty file or print an exception message if failed to write file
    :rtype: Catches exception of type OSError
    """
    logger = logging.getLogger(logID)
    filename = os.path.expandvars(filename)
    filename = os.path.expanduser(filename)
    if not os.path.isfile(filename):
        try:
            fd = open(filename, "w")
            logger.debug("Creating File: %s", filename)
            fd.close()
        except OSError as err:
            print(err)


def create_dir(dirname):
    """Create directory if it doesn't exist. Runs a "try" block
    to run os.makedirs() which creates all sub-directories if they
    dont exist. Catches exception of type OSError and prints message

    :param dirname: directory path to create
    :type dirname: string, required

    :return: creates the directory or print an exception message upon failure
    :rtype: Catches exception of type OSError
    """
    dirname = os.path.expandvars(dirname)
    dirname = os.path.expanduser(dirname)
    logger = logging.getLogger(logID)
    if not os.path.isdir(dirname):
        try:
            os.makedirs(dirname)
            logger.debug("Creating Directory: %s", dirname)
        except OSError as err:
            print(err)
            raise


def string_in_file(string, filename):
    """Returns True/False to indicate if string is in file.

    :param string: string to search
    :type string: str, required
    :param filename: file to check string
    :type filename: str, required

    :return: return True if string found, False on failure
    :rtype: True or False
    """

    if string in open(filename).read():
        return True

    return False
