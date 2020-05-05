"""
This file is used for generating documentation tests.
"""
import os, sys

from buildtest.defaults import BUILDTEST_ROOT
from buildtest.utils.command import BuildTestCommand
from buildtest.utils.file import create_dir

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
docgen = os.path.join(root, "docs", "docgen")


def build_helper():
    """This method will write output of several helper options for all sub-commands in buildtest"""
    help_cmds = [
        "buildtest --help",
        "buildtest show --help",
        "buildtest show schema --help",
        "buildtest build --help",
        "buildtest config --help",
        "buildtest get --help",
    ]
    for cmd in help_cmds:
        out = run(cmd)
        tmp_fname = cmd.replace(" ", "_") + ".txt"
        fname = os.path.join(docgen, tmp_fname)
        writer(fname, out, cmd)


def run(query):
    """The ``run()`` method will execute the command and retrieve the output as part of documentation examples """
    print(f"Executing Command: {query}")
    cmd = BuildTestCommand(query)
    cmd.execute()
    out = cmd.get_output()
    out = " ".join(out)
    return out


def introspection_cmds():
    cmd_dict = {
        "config-view.txt": "buildtest config view",
        "config-reset.txt": "buildtest config reset",
        "script-schema.txt": "buildtest show schema -n script",
    }

    for k, v in cmd_dict.items():
        out = run(v)
        fname = os.path.join(docgen, k)
        writer(fname, out, v)


def build_cmds():
    build_dict = {
        "gettingstarted-example1.txt": f"buildtest build -b {BUILDTEST_ROOT}/site/github.com/buildtesters/tutorials/system/systemd.yml",
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
