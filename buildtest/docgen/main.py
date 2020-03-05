"""
This file is used for generating documentation tests.
"""
import os, sys

from buildtest.tools.defaults import BUILDTEST_ROOT
from buildtest.tools.system import BuildTestCommand
from buildtest.tools.file import create_dir

docgen = os.path.join(BUILDTEST_ROOT, "docs", "docgen")


def build_helper():
    """This method will write output of several helper options for all sub-commands in buildtest"""
    help_cmds = [
        "buildtest -h",
        "buildtest show -h",
        "buildtest build -h",
        "buildtest config -h",
    ]
    for cmd in help_cmds:
        out = run(cmd)
        tmp_fname = cmd.replace(" ", "_") + ".txt"
        fname = os.path.join(docgen, tmp_fname)
        writer(fname, out, cmd)


def run(query):
    """The ``run()`` method will execute the command and retrieve the output as part of documentation examples """
    print(f"Executing Command: {query}")
    cmd = BuildTestCommand()
    cmd.execute(query)
    out = cmd.get_output()
    return out


def introspection_cmds():

    queries = [
        "buildtest show schema",
        "buildtest show --config",
        "buildtest config view",
        "buildtest config restore",
    ]

    for cmd in queries:
        out = run(cmd)
        tmp_fname = cmd.replace(" ", "_") + ".txt"
        fname = os.path.join(docgen, tmp_fname)

        writer(fname, out, cmd)


def build_cmds():
    build_dict = {
        "buildtest-build-clear.txt": "buildtest build --clear",
        "build-report.txt": "buildtest build report",
    }
    for k, v in build_dict.items():
        out = run(v)
        fname = os.path.join(docgen, k)
        writer(fname, out, v)


def writer(fname, out, query):
    fd = open(fname, "w")
    fd.write(f"$ {query}\n")
    fd.write(out)
    fd.close()
    print(f"Writing file: {fname}")


def main():
    create_dir(docgen)
    build_helper()
    introspection_cmds()
    build_cmds()


if __name__ == "__main__":
    """Entry Point, invoking main() method"""
    main()
