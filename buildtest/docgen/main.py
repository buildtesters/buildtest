"""
This file is used for generating documentation tests.
"""
import os

from buildtest.menu.repo import active_repos, func_repo_add
from buildtest.utils.command import BuildTestCommand
from buildtest.utils.file import create_dir, write_file

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
docgen = os.path.join(root, "docs", "docgen")


def build_helper():
    """This method will write output of several helper options for all sub-commands in buildtest"""
    help_cmds = [
        "buildtest --help",
        "buildtest schema --help",
        "buildtest build --help",
        "buildtest config --help",
        "buildtest repo --help",
        "buildtest buildspec --help",
        "buildtest report --help",
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


def generate_tests(prefix, cmd_dict):
    create_dir(os.path.join(docgen, prefix))

    for k, v in cmd_dict.items():
        out = run(v)
        out = f"$ {v} \n" + out

        fname = os.path.join(docgen, k)
        write_file(fname, out)
        print(f"Writing File: {fname}")


def tutorial():
    prefix = "getting_started"
    cmd_dict = {
        f"{os.path.join(prefix, 'buildspec-find.txt')}": "buildtest buildspec find",
        f"{os.path.join(prefix, 'buildspec-view.txt')}": "buildtest buildspec view systemd_default_target",
        f"{os.path.join(prefix,'buildspec-abspath.txt')}": "buildtest build -b /tmp/github.com/buildtesters/tutorials/examples/systemd.yml",
        f"{os.path.join(prefix,'buildspec-relpath.txt')}": "buildtest build -b examples/systemd.yml",
        f"{os.path.join(prefix, 'buildspec-directory.txt')}": "buildtest build -b tests/examples/buildspecs/",
        f"{os.path.join(prefix, 'multi-buildspecs.txt')}": "buildtest build -b tests/examples/buildspecs/ -b examples/selinux.yml",
        f"{os.path.join(prefix, 'invalid-buildspec.txt')}": "buildtest build -b examples/invalid_buildspec_section.yml -b examples/systemd.yml",
        f"{os.path.join(prefix, 'invalid-executor.txt')}": "buildtest build -b examples/invalid_executor.yml",
    }

    generate_tests(prefix, cmd_dict)


def schemas():
    prefix = "schemas"
    cmd_dict = {
        f"{os.path.join(prefix, 'avail-schemas.txt')}": "buildtest schema",
        f"{os.path.join(prefix, 'compiler-json.txt')}": "buildtest schema -n compiler-v1.0.schema.json -j",
        f"{os.path.join(prefix, 'compiler-examples.txt')}": "buildtest schema -n compiler-v1.0.schema.json -e",
        f"{os.path.join(prefix,'script-json.txt')}": "buildtest schema -n script-v1.0.schema.json -j",
        f"{os.path.join(prefix,'script-examples.txt')}": "buildtest schema -n script-v1.0.schema.json -e",
        f"{os.path.join(prefix, 'global-json.txt')}": "buildtest schema -n global.schema.json -j",
        f"{os.path.join(prefix, 'global-examples.txt')}": "buildtest schema -n global.schema.json -e",
        f"{os.path.join(prefix, 'settings-json.txt')}": "buildtest schema -n settings.schema.json -j",
        f"{os.path.join(prefix, 'settings-examples.txt')}": "buildtest schema -n settings.schema.json -e",
    }
    generate_tests(prefix, cmd_dict)


def introspection_cmds():
    cmd_dict = {
        "config-view.txt": "buildtest config view",
        "config-reset.txt": "buildtest config reset",
        "config-validate.txt": "buildtest config validate",
        "config-summary.txt": "buildtest config summary",
        "report.txt": "buildtest report",
        "report-helpformat.txt": "buildtest report --helpformat",
        "report-format.txt": "buildtest report --format name,schemafile,executor,state,returncode",
    }

    for k, v in cmd_dict.items():
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

    if "buildtesters/tutorial" not in active_repos():

        class args:
            repo = "https://github.com/buildtesters/tutorials.git"
            branch = "master"

        func_repo_add(args)

    create_dir(docgen)
    build_helper()
    tutorial()
    schemas()
    introspection_cmds()


if __name__ == "__main__":
    """Entry Point, invoking main() method"""
    main()
