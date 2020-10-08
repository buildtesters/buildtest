"""
This file is used for generating documentation tests.
"""
import os
import subprocess
from buildtest.utils.file import create_dir, write_file

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
docgen = os.path.join(root, "docs", "docgen")


def build_helper():
    """This method will write output of several helper options for all sub-commands in buildtest"""
    help_cmds = [
        "buildtest --help",
        "buildtest schema --help",
        "buildtest build --help",
        "buildtest config --help",
        "buildtest buildspec --help",
        "buildtest buildspec find --help",
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
    out = subprocess.check_output(query, shell=True, universal_newlines=True)
    out = "".join(out)
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
        f"{os.path.join(prefix,'buildspec-abspath.txt')}": "buildtest build -b /Users/siddiq90/Documents/buildtest/tutorials/systemd.yml",
        f"{os.path.join(prefix, 'buildspec-directory.txt')}": "buildtest build -b tests/examples/buildspecs/",
        f"{os.path.join(prefix, 'multi-buildspecs.txt')}": "buildtest build -b tests/examples/buildspecs/ -b tutorials/systemd.yml",
        f"{os.path.join(prefix, 'invalid-buildspec.txt')}": "buildtest build -b tutorials/invalid_buildspec_section.yml",
        f"{os.path.join(prefix, 'invalid-executor.txt')}": "buildtest build -b tutorials/invalid_executor.yml",
        f"{os.path.join(prefix, 'tags.txt')}": "buildtest build --tags tutorials",
        f"{os.path.join(prefix, 'multi-tags.txt')}": "buildtest build --tags compile --tags python",
        f"{os.path.join(prefix, 'combine-tags-buildspec-exclude.txt')}": "buildtest build --tags python -b tutorials/compilers -x tutorials/compilers/vecadd.yml",
        f"{os.path.join(prefix, 'single-executor.txt')}": "buildtest build --executor local.sh",
        f"{os.path.join(prefix, 'multi-executor.txt')}": "buildtest build --executor local.sh --executor local.bash",
        f"{os.path.join(prefix, 'shebang.txt')}": "buildtest build -b tutorials/shebang.yml",
        f"{os.path.join(prefix, 'stage_parse.txt')}": "buildtest build -b tutorials/systemd.yml --stage=parse",
        f"{os.path.join(prefix, 'stage_build.txt')}": "buildtest build -b tutorials/systemd.yml --stage=build",
        f"{os.path.join(prefix, 'rebuild.txt')}": "buildtest build -b tutorials/python-shell.yml --rebuild=3",
        f"{os.path.join(prefix, 'rebuild-tags.txt')}": "buildtest build --tags fail --rebuild=2",
        f"{os.path.join(prefix, 'debug-mode.txt')}": "buildtest -d DEBUG build -b tutorials/invalid_executor.yml",
    }

    generate_tests(prefix, cmd_dict)


def schemas():
    prefix = "schemas"
    cmd_dict = {
        f"{os.path.join(prefix, 'avail-schemas.txt')}": "buildtest schema",
        f"{os.path.join(prefix, 'settings-examples.txt')}": "buildtest schema -n settings.schema.json -e",
        f"{os.path.join(prefix, 'definitions-json.txt')}": "buildtest schema -n definitions.schema.json --json",
        f"{os.path.join(prefix, 'global-examples.txt')}": "buildtest schema -n global.schema.json --example",
        f"{os.path.join(prefix, 'global-json.txt')}": "buildtest schema -n global.schema.json --json",
        f"{os.path.join(prefix, 'script-examples.txt')}": "buildtest schema -n script-v1.0.schema.json --example",
        f"{os.path.join(prefix, 'script-json.txt')}": "buildtest schema -n script-v1.0.schema.json --json",
        f"{os.path.join(prefix, 'compiler-examples.txt')}": "buildtest schema -n compiler-v1.0.schema.json --example",
        f"{os.path.join(prefix, 'compiler-json.txt')}": "buildtest schema -n compiler-v1.0.schema.json --json",
    }
    generate_tests(prefix, cmd_dict)

    cmd_dict = {
        f"{os.path.join(prefix, 'gnu_hello.txt')}": "buildtest build -b tutorials/compilers/gnu_hello.yml",
        f"{os.path.join(prefix, 'vecadd.txt')}": "buildtest build -b tutorials/compilers/vecadd.yml",
        f"{os.path.join(prefix, 'pass_returncode.txt')}": "buildtest build -b tutorials/pass_returncode.yml",
        f"{os.path.join(prefix, 'skip_tests.txt')}": "buildtest build -b tutorials/skip_tests.yml",
        f"{os.path.join(prefix, 'root_user.txt')}": "buildtest build -b tutorials/root_user.yml",
        f"{os.path.join(prefix, 'run_only_platform.txt')}": "buildtest build -b tutorials/run_only_platform.yml",
        f"{os.path.join(prefix, 'bmgroups.txt')}": "buildtest build -b general_tests/sched/lsf/bmgroups.yml",
        f"{os.path.join(prefix, 'run_only_distro.txt')}": "buildtest build -b tutorials/run_only_distro.yml",
    }

    generate_tests(prefix, cmd_dict)


def introspection_cmds():
    cmd_dict = {
        "config-view.txt": "buildtest config view",
        "config-validate.txt": "buildtest config validate",
        "config-summary.txt": "buildtest config summary",
        "report.txt": "buildtest report",
        "buildspec-filter.txt": "buildtest buildspec find --helpfilter",
        "buildspec_find_tags.txt": "buildtest buildspec find --tags",
        "buildspec_find_buildspecfiles.txt": "buildtest buildspec find --buildspec-files",
        "buildspec_find_executors.txt": "buildtest buildspec find --list-executors",
        "buildspec_filter_type.txt": "buildtest buildspec find --filter type=script",
        "buildspec_filter_tags.txt": "buildtest buildspec find --filter tags=fail",
        "buildspec_multifield_filter.txt": "buildtest buildspec find --filter tags=tutorials,executor=local.sh,type=script",
        "report-helpformat.txt": "buildtest report --helpformat",
        "report-helpfilter.txt": "buildtest report --helpfilter",
        "report-format.txt": "buildtest report --format name,id,executor,state,returncode",
        "report-filter-name.txt": "buildtest report --filter name=exit1_pass --format=name,id,returncode,state",
        "report-filter-buildspec.txt": "buildtest report --filter buildspec=tutorials/pass_returncode.yml --format=name,id,state,buildspec",
        "report-multifilter.txt": "buildtest report --filter state=FAIL,executor=local.sh --format=name,id,state,executor",
        "report-returncode.txt": "buildtest report --filter returncode=2 --format=name,id,returncode",
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

    create_dir(docgen)
    build_helper()
    tutorial()
    schemas()
    introspection_cmds()


if __name__ == "__main__":
    main()
