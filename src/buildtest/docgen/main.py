"""
This file is used for generating documentation tests.
"""
import os, sys
sys.path.insert(0, os.path.join(os.getenv("BUILDTEST_ROOT"), 'src'))

from buildtest.tools.system import BuildTestCommand
from buildtest.tools.file import create_dir

docgen=os.path.join(os.getenv("BUILDTEST_ROOT"),"docs","docgen")

def build_helper():
    help_cmds = [
     "buildtest -h",
     "buildtest list -h",
     "buildtest show -h",
     "buildtest testconfigs -h",
     "buildtest testconfigs maintainer -h",
     "buildtest build -h",
     "buildtest build bsub -h",
     "buildtest benchmark -h",
     "buildtest benchmark osu -h",
     "buildtest module -h",
     "buildtest module tree -h",
     "buildtest module collection -h",
     "buildtest config -h",
     "buildtest system -h"
    ]
    for cmd in help_cmds:
        out = run(cmd)
        tmp_fname = cmd.replace(" ","_") + ".txt"
        fname = os.path.join(docgen,tmp_fname)

        writer(fname,out,cmd)

def run(query):
    print (f"Executing Command: {query}")
    cmd = BuildTestCommand()
    cmd.execute(query)
    out = cmd.get_output()
    return out

def introspection_cmds():

    queries = [
        "buildtest list --software",
        "buildtest list --modules",
        "buildtest list --easyconfigs",
        "buildtest show -k singlesource",
        "buildtest show --config",
        "buildtest config view",
        "buildtest config restore"
    ]
    for cmd in queries:
        out = run(cmd)
        tmp_fname = cmd.replace(" ", "_") + ".txt"
        fname = os.path.join(docgen, tmp_fname)

        writer(fname, out, cmd)



def writer(fname,out,query):
    fd = open(fname,"w")
    fd.write(f"$ {query}\n")
    fd.write(out)
    fd.close()
    print (f"Writing file: {fname}")

def main():
    create_dir(docgen)
    build_helper()
    introspection_cmds()


if __name__ == "__main__":
    """Entry Point, invoking main() method"""
    main()