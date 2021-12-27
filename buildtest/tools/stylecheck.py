import os
import shutil

from buildtest.defaults import BUILDTEST_ROOT, console
from buildtest.utils.command import BuildTestCommand


def run_black(source_files, black_opts):

    if not shutil.which("black"):
        return

    source_files = " ".join(source_files)
    black_cmd = f"black {black_opts} {source_files}"
    console.print(f"Running black check: {black_cmd}")
    cmd = BuildTestCommand(black_cmd)
    out, err = cmd.execute()

    if out:
        console.rule("black output message")
        console.print("".join(out))

    if err:
        console.rule("black error message")
        console.print("".join(err))

    # console.print(Panel.fit(''.join(out), title="Black output message"))
    # console.print(Panel.fit(''.join(err), title="Black error messages"))


def run_isort(source_files, isort_opts):

    if not shutil.which("isort"):
        return

    source_files = " ".join(source_files)

    isort_cmd = f"isort --settings-path {os.path.join(BUILDTEST_ROOT, '.isort.cfg')} {isort_opts} {source_files}"
    console.print(f"Running isort check: {isort_cmd}")

    cmd = BuildTestCommand(isort_cmd)
    out, err = cmd.execute()

    if out:
        console.rule("isort output message")
        console.print("".join(out))

    if err:
        console.rule("isort error message")
        console.print("".join(err))


def run_pyflakes(source_files):

    if not shutil.which("pyflakes"):
        return

    source_files = " ".join(source_files)

    pyflakes_cmd = f"pyflakes {source_files}"
    console.print(f"Running pyflakes check: {pyflakes_cmd}")

    cmd = BuildTestCommand(pyflakes_cmd)
    out, err = cmd.execute()
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
