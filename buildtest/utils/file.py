"""
This module provides some generic file and directory level operation that
include the following:
1. Check if path is a File or Directory via is_file(), is_dir()
2. Create a directory via create_dir()
3. Walk a directory tree based on single extension using walk_tree()
4. Resolve path including shell and user expansion along with getting realpath to file using resolve_path()
5. Read and write a file via read_file(), write_file()
"""

import json
import os
import re

from buildtest.exceptions import BuildTestError


def is_file(fname):
    """Check if file exist and returns True/False

    Args:
        fname (str): file path to check

    Returns:
        bool: True if path is a file and is a realpath otherwise returns False
    """

    # resolve_path will return the full canonical filename or return None if file doesn't exist
    fname = resolve_path(fname)

    # if return is None we return False since file is non-existent
    if not fname:
        return False

    # at this stage we know it's a valid file but we don't know if its a file or directory
    return os.path.isfile(fname)


def is_dir(dirname):
    """Check if input directory exist and is a directory. If so return ``True`` otherwise returns ``False``.
    We resolve path by invoking :func:`resolve_path`

    Args:
        dirname (str): directory path to check

    Returns:
        bool: True if directory exists otherwise returns False.
    """

    # resolve_path will return the full canonical directory name or return None if directory doesn't exist
    dirname = resolve_path(dirname)

    # if return is None we stop here and return False since directory is non-existent.
    if not dirname:
        return False

    # at this stage we know it's a valid file, so return if file is a directory or not
    return os.path.isdir(dirname)


def is_symlink(filename):
    """Check if the given link is a symlink and return ``True``, if it is not a symlink or the symlink is broken return ``False``.

    Args:
        filename (str): Input filename to check if its a symbolic link

    Returns:
        bool: True if filename is a symbolic link otherwise return False if its not a symbolic link or broken link
    """

    # apply shell expansion  when file includes something like $HOME/example
    expanded_filepath = os.path.expandvars(filename)

    # apply user expansion when file includes something like  ~/example
    expanded_filepath = os.path.expanduser(expanded_filepath)

    # resolve path will return canonical path eliminating any symbolic links encountered
    resolved_sym_link = resolve_path(filename)

    return os.path.islink(expanded_filepath) and resolved_sym_link


def search_files(root_dir, regex_pattern, max_depth=None):
    """
    This method will search for files in a directory based on a regex pattern.

    Args:
        root_dir (str): Root directory to search for files
        regex_pattern (str): A regex pattern to search for files
        max_depth (int, optional): Specify maximum depth to traverse during directory walk.

    Returns: A list of files that match the regex pattern

    """
    files_list = []

    # re.compile can raise exception if regex pattern is not valid which will raise re.error
    try:
        pattern = re.compile(regex_pattern)
    except re.error as err:
        print(err)
        raise BuildTestError(
            f"Unable to compile regular expression: {regex_pattern}, please try again"
        )

    if not is_dir(root_dir):
        return files_list

    resolved_dirpath = resolve_path(root_dir, exist=True)

    for root, dirs, files in os.walk(resolved_dirpath):
        if (
            max_depth is not None
            and root.count(os.sep) - resolved_dirpath.count(os.sep) >= max_depth
        ):
            del dirs[:]
            continue
        for file in files:
            if pattern.search(file):
                file_path = os.path.join(root, file)
                files_list.append(file_path)

    return [os.path.abspath(fname) for fname in files_list]


def walk_tree(root_dir, ext=None, max_depth=None):
    """This method will traverse a directory tree and return list of files
    based on extension type. This method invokes :func:`is_dir` to check if directory
    exists before traversal.

    Args:
        root_dir (str): directory path to traverse
        ext (str): File extension to search in traversal
        max_depth (int, optional): Maximum depth to traverse

    Returns:
        list: A list of file paths for a directory traversal based on extension type. If ``ext`` is **None** we retrieve all files
    """

    files_list = []
    if not is_dir(root_dir):
        return files_list

    resolved_dirpath = resolve_path(root_dir, exist=True)

    for root, dirs, files in os.walk(resolved_dirpath):
        if (
            max_depth is not None
            and root.count(os.sep) - resolved_dirpath.count(os.sep) >= max_depth
        ):
            del dirs[:]
            continue
        for file in files:
            if ext is None or file.endswith(ext):
                file_path = os.path.join(root, file)
                files_list.append(file_path)

    return [os.path.abspath(fname) for fname in files_list]


def create_dir(dirname):
    """Create a directory if it doesn't exist. If directory contains variable
    expansion (**$HOME**) or user expansion (**~**), we resolve this before creating directory.
    If there is an error creating directory we raise an exception BuildTestError

    :param dirname: directory path to create
    :type dirname: str, required
    :return: creates the directory or print an exception message upon failure
    :rtype: Catches exception of type OSError and raise exception BuildTestError or returns None
    """

    # these three lines implement same as ``resolve_path`` will return None when it's not a known file. We expect
    # input to create_dir will be a non-existent path so we run these lines manually
    dirname = os.path.expanduser(dirname)
    dirname = os.path.expandvars(dirname)
    dirname = os.path.realpath(dirname)

    if not os.path.isdir(dirname):
        try:
            os.makedirs(dirname)
        except OSError as err:
            print(err)
            raise BuildTestError(f"Cannot create directory {dirname}")


def resolve_path(path, exist=True):
    """This method will resolve a file path to account for shell expansion and resolve paths in
    when a symlink is provided in the file. This method assumes file already exists.

    Args:
        path (str): file path to resolve
        exist (bool): a boolean to determine if filepath should be returned if filepath doesn't exist on filesystem.

    Returns:
        str: Full path to file if file exists or ``exist=True`` is set. We could return ``None`` if path is not defined or file path doesn't exist and ``exist=False``

    Raises:
        BuildTestError: If input path is not of type str

    >>> a = resolve_path("$HOME/.bashrc")
    >>> assert a
    >>> b = resolve_path("$HOME/.bashrc1", exist=False)
    >>> assert b
    >>> c = resolve_path("$HOME/.bashrc1", exist=True)
    >>> assert not c
    """

    # if path not set return None
    if not path:
        return

    if not isinstance(path, str):
        raise BuildTestError(
            f"Input must be a string type, {path} is of type {type(path)}"
        )

    # apply shell expansion  when file includes something like $HOME/example
    path = os.path.expandvars(path)
    # apply user expansion when file includes something like  ~/example
    path = os.path.expanduser(path)

    real_path = os.path.realpath(path)
    if os.path.exists(real_path) or not exist:
        return real_path


def read_file(filepath):
    """This method is used to read a file and return content of file.
    If filepath is not a string we raise an error. We run :func:`resolve_path`
    to get realpath to file and account for shell or user expansion. The
    return will be a valid file or ``None`` so we check if input is an invalid file.
    Finally we read the file and return the content of the file as a string.

    Args:
        filepath (str): File name to read

    Raises:
        BuildTestError:
          - if filepath is invalid
          - filepath is not an instance of type :class:`str`.
          - An exception can be raised if there is an issue reading file with an exception of :class:`IOError`

    Returns:
        str: content of input file
    """

    # ensure filepath is a string, if not, we raise an error.
    if not isinstance(filepath, str):
        raise BuildTestError(
            f"Invalid type for file: {filepath} must be of type 'str' "
        )

    input_file = filepath
    # resolve_path will handle shell and user expansion and account for any symlinks and check for file existence.
    # if resolve_path does not return gracefully it implies file does not exist and will return None
    filepath = resolve_path(filepath)

    # if it's invalid file let's raise an error
    if not filepath:
        raise BuildTestError(
            f"Unable to find input file: {input_file}. Please specify a valid file"
        )
    try:
        with open(filepath, "r") as fd:
            content = fd.read()
    except IOError as err:
        raise BuildTestError("Failed to read: %s: %s" % (filepath, err))

    return content


def write_file(filepath, content):
    """This method is used to write an input ``content`` to a file specified by
    ``filepath``. Both filepath and content must be a str. An error is raised
    if filepath is not a string or a directory. If ``content`` is not a str,
    we return ``None`` since we can't write the content to file.
    Finally, we write the content to file and return. A successful write
    will return nothing otherwise an exception will occur during the write
    process.

    Args:
        filepath (str): file name to write
        content (str): content to write to file

    Raises:
        BuildTestError:
            - filepath is not :class:`str`
            - filepath is directory via :class:`is_dir`
            - content of file is not of type :class:`str`
            - Error writing file with an exception of type :class:`IOError`
    """

    # ensure filepath is a string, if not we raise an error
    if not isinstance(filepath, str):
        raise BuildTestError(
            f"Invalid type for file: {filepath} must be of type 'str' "
        )

    #  if filepath is a directory, we raise an exception noting that user must specify a filepath
    if is_dir(filepath):
        raise BuildTestError(
            f"Detected {filepath} is a directory, please specify a file path."
        )

    # ensure content is of type string
    if not isinstance(content, str):
        raise BuildTestError(
            f"Expecting type str but got type: {type(content)} when writing file"
        )

    try:
        with open(filepath, "w") as fd:
            fd.write(content)
    except IOError as err:
        raise BuildTestError(f"Failed to write: {filepath}: {err}")


def remove_file(fpath):
    """This method is responsible for removing a file. The input path is an absolute path
    to file. We check for exceptions first, and return immediately before removing file.

    Args:
        fpath (str): full path to file to remove

    Raises:
          BuildTestError:
            - If fpath is not instance of :class:`str`
            - If fpath is not a file using :func:`is_file`
            - An exception of type :class:`OSError` when removing file via :func:`os.remove`
    """

    if not fpath:
        return

    if not isinstance(fpath, str):
        raise BuildTestError(
            f"Unable to remove file: {fpath} because we have a type mismatch. It must be a string type"
        )

    # if its not a file return
    if not is_file(fpath):
        raise BuildTestError(
            f"The filepath: {fpath} must be a file and must exist on file system"
        )

    try:
        os.remove(fpath)
    except OSError:
        raise BuildTestError(f"Unable to delete file: {fpath}")


def load_json(fname):
    """Given a filename, resolves full path to file and loads json file. This method will
    catch exception :class:`json.JSONDecodeError` and raise an exception with useful message. If there is no
    error we return content of json file

    Args:
        fname (str): Name of file to read and load json content

    Raises:
        BuildTestError: Raise exception if file is not resolved via :func:`resolve_path` or failure to load JSON document
    """

    abspath_fname = resolve_path(fname)
    # if filename doesn't exist we raise an exception
    if not abspath_fname:
        raise BuildTestError(f"Unable to resolve path: {fname}")

    # attempt to open file for reading and use json.loads to read the content and check for exception
    with open(abspath_fname) as fd:
        try:
            content = json.loads(fd.read())
        except json.JSONDecodeError as err:
            print(err)
            raise BuildTestError(
                f"Unable to read file: {fname}, please make sure its valid json file"
            )

        return content
