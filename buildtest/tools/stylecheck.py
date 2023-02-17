import os
import shutil

from buildtest.defaults import BUILDTEST_ROOT, console
from buildtest.utils.command import BuildTestCommand


def run_command(cmd, msg):
    """This method is a wrapper to BuildTestCommand used with running black, isort, and pyflakes during style check

    Args:
        cmd (str): Name of command to run
        msg (str): Message printed during style check
    """
    console.print(f"{msg}: {cmd}")
    result = BuildTestCommand(cmd)
    out, err = result.execute()
    if result.returncode() == 0:
        console.print(f"[green]{msg} PASSED")
    else:
        console.print(f"[red]{msg} FAILED")
    console.rule(f"{msg} output message")
    console.print("".join(out))
    console.rule(f"{msg} error message")
    console.print("".join(err))


def run_black(source_files, black_opts):
    """This method will run `black <https://black.readthedocs.io/>`_ check given a set of source files and black options.
    If black is not available we will return immediately otherwise we run black checks and print output and error message
    reported by black.

    Args:
        source_files (list): List of source files to run black check
        black_opts (str): Specify options to black
    """

    if not shutil.which("black"):
        return

    cmd = f"black {black_opts} {' '.join(source_files)}"
    run_command(cmd, "Running black check")


def run_isort(source_files, isort_opts):
    """This method will run `isort <https://pycqa.github.io/isort/index.html>`_ checks which performs import sorting for buildtest
    codebase. If `isort` is not available we return immediately.

    Args:
        source_files (list): A list of source files to run isort
        isort_opts (str): Specify options to isort command
    """

    if not shutil.which("isort"):
        return

    # source_files = " ".join(source_files)
    cmd = f"isort --settings-path {os.path.join(BUILDTEST_ROOT, '.isort.cfg')} {isort_opts} {' '.join(source_files)}"
    run_command(cmd, "Running isort check")


def run_pyflakes(source_files):
    """This method will run `pyflakes <https://pypi.org/project/pyflakes/>`_ checks which checks for unused imports and errors
    in source files.

    Args:
        source_files (list): List of source files to apply pyflakes check
    """

    if not shutil.which("pyflakes"):
        return

    cmd = f"pyflakes {' '.join(source_files)}"
    run_command(cmd, "Running pyflakes check")


def run_style_checks(no_black, no_isort, no_pyflakes, apply_stylechecks):
    """This method runs buildtest style checks which is invoked via ``buildtest stylecheck`` command.

    Args:
        no_black (bool): Disable black check if `no_black=True`.
        no_isort (bool): Disable isort check if `no_isort=True`.
        no_pyflakes (bool): Disable pyflakes check if `no_pyflakes=True`.
        apply_stylechecks (bool):  If `apply_stylechecks=True` then black and isort stylecheck will be applied to codebase, by default these checks will report changes to codebase without applying changes.
    """

    source_files = [
        os.path.join(BUILDTEST_ROOT, "buildtest"),
        os.path.join(BUILDTEST_ROOT, "tests"),
        os.path.join(BUILDTEST_ROOT, "docs"),
    ]

    black_opts = "" if apply_stylechecks else "--check --diff"
    isort_opts = (
        "--profile black" if apply_stylechecks else "--profile black --check --diff"
    )

    if not no_black:
        run_black(source_files=source_files, black_opts=black_opts)

    if not no_isort:
        run_isort(source_files=source_files, isort_opts=isort_opts)

    if not no_pyflakes:
        run_pyflakes(source_files)
