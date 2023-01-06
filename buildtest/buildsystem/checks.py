from buildtest.defaults import console
from buildtest.utils.file import is_dir, is_file, resolve_path


def exists_check(builder, status):
    """This method will perform status check for ``exists`` property. Each value is tested for file
    existence and returns a boolean to inform if all files exist or not.

    Args:
        builder (buildtest.builders.base.BuilderBase): An instance of BuilderBase class used for printing the builder name
        status (dict): A dictionary containing the ``status`` property from the buildspec
    Returns:
        bool: A boolean for exists status check
    """
    assert_exists = all(resolve_path(file, exist=True) for file in status["exists"])
    console.print(
        f"[blue]{builder}[/]: Test all files:  {status['exists']}  existences "
    )
    for fname in status["exists"]:
        resolved_fname = resolve_path(fname)
        if resolved_fname:
            console.print(f"[blue]{builder}[/]: file: {resolved_fname} exists")
        else:
            console.print(f"[blue]{builder}[/]: file: {fname} does not exist")

    console.print(f"[blue]{builder}[/]: Exist Check: {assert_exists}")
    return assert_exists


def is_file_check(builder, status):
    """This method will perform status check for ``is_file`` property. Each item in ``is_file`` is
     checked by determining if its a file. The return is a single boolean where we perform a logical AND
     to determine final status check for is_file

    Args:
        builder (buildtest.builders.base.BuilderBase): An instance of BuilderBase class used for printing the builder name
        status (dict): A dictionary containing the ``status`` property from the buildspec
    Returns:
        bool: A boolean for is_file status check
    """

    assert_is_file = all(is_file(file) for file in status["is_file"])
    console.print(
        f"[builder]{builder}[/]: Test all files:  {status['is_file']}  existences "
    )
    for fname in status["is_file"]:
        resolved_fname = resolve_path(fname, exist=True)
        if is_file(resolved_fname):
            console.print(f"[blue]{builder}[/]: file: {resolved_fname} is a file ")
        else:
            console.print(f"[blue]{builder}[/]: file: {fname} is not a file")

    console.print(f"[blue]{builder}[/]: File Existence Check: {assert_is_file}")
    return assert_is_file


def is_dir_check(builder, status):
    """This method will perform status check for ``is_dir`` property. Each item in ``is_dir`` is
     checked by determining if its a directory. The return is a single boolean where we perform a logical AND
     to determine final status check for ``is_dir``

    Args:
        builder (buildtest.builders.base.BuilderBase): An instance of BuilderBase class used for printing the builder name
        status (dict): A dictionary containing the ``status`` property from the buildspec
    Returns:
        bool: A boolean for ``is_dir`` status check
    """

    assert_is_dir = all(is_dir(file) for file in status["is_dir"])
    console.print(
        f"[blue]{builder}[/]: Test all files:  {status['is_dir']}  existences "
    )
    for dirname in status["is_dir"]:
        resolved_dirname = resolve_path(dirname)
        if is_dir(resolved_dirname):
            console.print(
                f"[blue]{builder}[/]: file: {resolved_dirname} is a directory "
            )
        else:
            console.print(f"[blue]{builder}[/]: file: {dirname} is not a directory")

    console.print(f"[blue]{builder}[/]: Directory Existence Check: {assert_is_dir}")
    return assert_is_dir
