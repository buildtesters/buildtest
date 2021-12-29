import os
import shutil

from buildtest.defaults import BUILDTEST_ROOT, console
from buildtest.utils.command import BuildTestCommand


def run_black(source_files, black_opts):
    """This method will run `black <https://black.readthedocs.io/>`_ check given a set of source files and black options. If black is not
     available we will return immediately otherwise we run black checks and print output and error message reported by black.

    Args:
        source_files (list): List of source files to run black check
        black_opts (str): Specify options to black
    """

    if not shutil.which("black"):
        return

    source_files = " ".join(source_files)
    black_cmd = f"black {black_opts} {source_files}"
    console.print(f"Running black check: {black_cmd}")
    cmd = BuildTestCommand(black_cmd)
    out, err = cmd.execute()

    if cmd.returncode() == 0:
        console.print("[green]black style check PASSED")
    else:
        console.print("[red]black style check FAILED")

    if out:
        console.rule("black output message")
        console.print("".join(out))

    if err:
        console.rule("black error message")
        console.print("".join(err))


def run_isort(source_files, isort_opts):
    """This method will run `isort <https://pycqa.github.io/isort/index.html>`_ checks which performs import sorting for buildtest
    codebase. If `isort` is not available we return immediately.

    Args:
        source_files (list): A list of source files to run isort
        isort_opts (str): Specify options to isort command
    """

    if not shutil.which("isort"):
        return

    source_files = " ".join(source_files)

    isort_cmd = f"isort --settings-path {os.path.join(BUILDTEST_ROOT, '.isort.cfg')} {isort_opts} {source_files}"
    console.print(f"Running isort check: {isort_cmd}")

    cmd = BuildTestCommand(isort_cmd)
    out, err = cmd.execute()

    if cmd.returncode() == 0:
        console.print("[green]isort style check PASSED")
    else:
        console.print("[red]Black style check FAILED")

    if out:
        console.rule("isort output message")
        console.print("".join(out))

    if err:
        console.rule("isort error message")
        console.print("".join(err))


def run_pyflakes(source_files):
    """This method will run `pyflakes <https://pypi.org/project/pyflakes/>`_ checks which checks for unused imports and errors
    in source files.

    Args:
        source_files (list): List of source files to apply pyflakes check
    """

    if not shutil.which("pyflakes"):
        return

    source_files = " ".join(source_files)

    pyflakes_cmd = f"pyflakes {source_files}"
    console.print(f"Running pyflakes check: {pyflakes_cmd}")

    cmd = BuildTestCommand(pyflakes_cmd)
    out, err = cmd.execute()

    if cmd.returncode() == 0:
        console.print("[green]pyflakes style check PASSED")
    else:
        console.print("[red]pyflakes style check FAILED")

    if out:
        console.rule("pyflakes output message")
        console.print("".join(out))

    if err:
        console.rule("pyflakes error message")
        console.print("".join(err))


def run_style_checks(no_black, no_isort, no_pyflakes, apply_stylechecks):
    """Run buildtest style checks"""

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
        run_black(source_files, black_opts=black_opts)

    if not no_isort:
        run_isort(source_files, isort_opts=isort_opts)

    if not no_pyflakes:
        run_pyflakes(source_files)
