"""
This module provides some generic file and directory level operation that
include the following:
1. Check if path is a File or Directory via is_file(), is_dir()
2. Create a directory via create_dir()
3. Walk a directory tree based on single extension using walk_tree()
4. Resolve path including shell and user expansion along with getting realpath to file using resolve_path()
5. Read and write a file via read_file(), write_file()
"""

import os
import logging
import sys
from buildtest.exceptions import BuildTestError

logger = logging.getLogger(__name__)


def is_file(fname):
    """This method will check if file exist and if not found throws an exception.

    :param file: file path
    :type file: str, required

    :return: returns a boolean True/False depending on if input is a valid file.
    :rtype: bool
    """

    # resolve_path will return the full canonical filename or return None if file doesn't exist
    fname = resolve_path(fname)

    # if return is None we return False since file is non-existent
    if not fname:
        return False

    # at this stage we know it's a valid file but we don't know if its a file or directory
    return os.path.isfile(fname)


def is_dir(dirname):
    """This method will check if a directory exist and if not found throws an exception.

       Parameters:

       :param dir: directory path
       :type dir: str, required

       :return: returns a boolean True/False depending on if input is a valid directory.
       :rtype: bool
    """

    # resolve_path will return the full canonical directory name or return None if directory doesn't exist
    dirname = resolve_path(dirname)

    # if return is None we stop here and return False since directory is non-existent.
    if not dirname:
        return False

    # at this stage we know it's a valid file, so return if file is a directory or not
    return os.path.isdir(dirname)


def walk_tree(root_dir, ext=None):
    """This method will traverse a directory tree and return list of files
       based on extension type. This method invokes is_dir() to check if directory
       exists before traversal.

       Parameters:

       :param root_dir: directory path to traverse
       :type root_dir: str, required
       :param ext: file extensions to search in traversal
       :type ext: str, optional

       :return: returns a list of file paths
       :rtype: list
    """

    list_files = []
    # if directory doesn't exist let's return empty list before doing a directory traversal since no files to traverse
    if not is_dir(root_dir):
        return list_files

    for root, subdir, files in os.walk(root_dir):
        for fname in files:
            # if ext is provided check if file ends with extension and add to list, otherwise
            # add all files to list and return
            if ext:
                if fname.endswith(ext):
                    list_files.append(os.path.join(root, fname))
            else:
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

    # these three lines implement same as ``resolve_path`` will return None when it's not a known file. We expect
    # input to create_dir will be a non-existent path so we run these lines manually
    dirname = os.path.expanduser(dirname)
    dirname = os.path.expandvars(dirname)
    dirname = os.path.realpath(dirname)

    if not os.path.isdir(dirname):
        try:
            os.makedirs(dirname)
            logger.debug("Creating Directory: %s", dirname)
        except OSError as err:
            print(err)
            raise


def resolve_path(path, exist=True):
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

    if os.path.exists(real_path):
        return real_path

    if not exist:
        return real_path


def read_file(filepath):
    """ This method is used to read a file specified by argument ``filepath``. If filepath is not a string we raise
        an error. We also run ``resolve_path`` to get realpath to file and account for shell or user expansion. The
        return from ``resolve_path`` will be a valid file or ``None`` so  we check if input is an invalid file.
        Finally we read the file and return the content of the file as a string.

        Parameters:

        :param filepath: file name to read
        :type filepath: str, required
        :raises:
          SystemError: If filepath is not a string
          SystemError: If filepath is not valid file
        :return: return content of file as a string
        :rtype: str
    """

    # ensure filepath is a string, if not, we raise an error.
    if not isinstance(filepath, str):
        sys.exit(f"Invalid type for file: {filepath} must be of type 'str' ")

    input_file = filepath
    # resolve_path will handle shell and user expansion and account for any symlinks and check for file existence.
    # if resolve_path does not return gracefully it implies file does not exist and will return None
    filepath = resolve_path(filepath)

    # if it's invalid file let's raise an error
    if not filepath:
        sys.exit(
            f"Unable to find input file: {input_file}. Please specify a valid file"
        )
    try:
        with open(filepath, "r") as fd:
            content = fd.read()
    except IOError as err:
        raise BuildTestError("Failed to read: %s: %s" % (filepath, err))

    return content


def write_file(filepath, content):
    """ This method is used to write an input ``content`` to a file specified by ``filepath. Both filepath
        and content must be a str. An error is raised if filepath is not a string or a directory. If ``content``
        is not a str, we return ``None`` since we can't process the content for writing. Finally, we write the content
        to file and return. A successful write will return nothing otherwise an exception will occur during the write
        process.

        Parameters:

        :param filepath: file name to write
        :type filepath: str, required
        :param content: content to write to file
        :type content: str, required
        :raises:
          SystemError: System error if filepath is not string
          SystemError: System error if filepath is a directory
        :return: Return nothing if write is successful. A system error if ``filepath`` is not str or directory. If
                 argument ``content`` is not str we return ``None``
    """

    # ensure filepath is a string, if not we raise an error
    if not isinstance(filepath, str):
        sys.exit(f"Invalid type for file: {filepath} must be of type 'str' ")

    #  if filepath is a directory, we raise an exception noting that user must specify a filepath
    if is_dir(filepath):
        sys.exit(f"Detected {filepath} is a directory, please specify a file path.")

    # ensure content is of type string
    if not isinstance(content, str):
        return

    try:
        with open(filepath, "w") as fd:
            fd.write(content)
    except IOError as err:
        raise BuildTestError(f"Failed to write: {filepath}: {err}")
