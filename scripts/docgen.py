"""
This file is used for generating documentation tests.
"""
import os
import shutil
import subprocess

from buildtest.defaults import BUILDTEST_USER_HOME, VAR_DIR
from buildtest.utils.file import create_dir, write_file

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
docgen = os.path.join(root, "docs", "docgen")

os.environ["BUILDTEST_COLOR"] = "False"


def buildspecs_page():

    prefix = "buildspecs/overview"

    cmd_dict = {
        "run_only_platform.txt": "buildtest build -b tutorials/run_only_platform.yml",
        "run_only_distro.txt": "buildtest build -b tutorials/run_only_distro.yml",
    }

    generate_tests(prefix, cmd_dict)

    prefix = "buildspecs/compiler"
    cmd_dict = {
        "gnu_hello.txt": "buildtest build -b tutorials/compilers/gnu_hello_fortran.yml"
    }

    generate_tests(prefix, cmd_dict)


def run(query):
    """The ``run()`` method will execute the command and retrieve the output as part of documentation examples"""

    print(f"Executing Command: {query}")
    out = subprocess.check_output(query, shell=True, universal_newlines=True)
    # out = "".join(out)
    return out


def generate_tests(prefix, cmd_dict):
    create_dir(os.path.join(docgen, prefix))

    for k, v in cmd_dict.items():
        out = run(v)
        out = f"$ {v} \n" + out

        fname = os.path.join(docgen, prefix, k)
        write_file(fname, out)
        print(f"Writing File: {fname}")


def writer(fname, out, query):
    fd = open(fname, "w")
    fd.write(f"$ {query}\n")
    fd.write(out)
    fd.close()
    print(f"Writing file: {fname}")


def main():

    # remove $BUILDTEST_ROOT/var
    shutil.rmtree(VAR_DIR)
    shutil.rmtree(BUILDTEST_USER_HOME)

    create_dir(docgen)
    buildspecs_page()


if __name__ == "__main__":
    main()
