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

logger = logging.getLogger(__name__)

def is_file(fname):
    """This method will check if file exist and if not found throws an exception.

    :param file: file path
    :type file: str, required

    :return: returns True if file exists otherwise terminates with an exception
    :rtype: bool
    """

    fname = resolve_path(fname)
    if os.path.isfile(fname):
        return True

    return False


def is_dir(dirname):
    """This method will check if a directory exist and if not found throws an exception.

       Parameters:

       :param dir: directory path
       :type dir: str, required

       :return: returns ``True`` if directory exists otherwise returns ``False``
       :rtype: bool
    """

    dirname = resolve_path(dirname)

    if os.path.isdir(dirname):
        return True

    return False


def walk_tree(root_dir, ext):
    """This method will traverse a directory tree and return list of files
       based on extension type. This method invokes is_dir() to check if directory
       exists before traversal.

       Parameters:

       :param root_dir: directory path to traverse
       :type root_dir: str, required
       :param ext: file extensions to search in traversal
       :type ext: str, required

       :return: returns a list of file paths
       :rtype: list
    """

    list_files = []
    is_dir(root_dir)
    for root, subdir, files in os.walk(root_dir):
        for fname in files:
            if fname.endswith(ext):
                list_files.append(os.path.join(root, fname))

    return list_files


def create_dir(dirname):
    """Create directory if it doesn't exist. Runs a "try" block
       to run os.makedirs() which creates all sub-directories if they
       dont exist. Catches exception of type OSError and prints message

       Parameters:

       :param dirname: directory path to create
       :type dirname: string, required

       :return: creates the directory or print an exception message upon failure
       :rtype: Catches exception of type OSError
    """

    dirname = resolve_path(dirname)

    if not os.path.isdir(dirname):
        try:
            os.makedirs(dirname)
            logger.debug("Creating Directory: %s", dirname)
        except OSError as err:
            print(err)
            raise


def resolve_path(path):
    """This method will resolve a file path to account for shell expansion and resolve paths in
       when a symlink is provided in the file. This method assumes file already exists.

       Parameters:

       :param path: file path to resolve
       :type path: str, required
       :return: return realpath to file if found otherwise return None
       :rtype: str or None
    """

    # apply shell expansion  when file includes something like $HOME/example
    path = os.path.expandvars(path)
    # apply user expansion when file includes something like  ~/example
    path = os.path.expanduser(path)

    real_path = os.path.realpath(path)
    #if os.path.exists(real_path):
    return real_path
