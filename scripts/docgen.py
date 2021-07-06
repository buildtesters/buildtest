"""
This file is used for generating documentation tests.
"""
import os
import subprocess
import shutil
from buildtest.utils.file import create_dir, write_file
from buildtest.defaults import VAR_DIR, BUILDTEST_USER_HOME

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
docgen = os.path.join(root, "docs", "docgen")

os.environ["BUILDTEST_COLOR"] = "False"


def build_helper():
    """This method will write output of several helper options for all sub-commands in buildtest"""
    help_cmds = [
        "buildtest --help",
        "buildtest schema --help",
        "buildtest build --help",
        "buildtest config --help",
        "buildtest config compilers --help",
        "buildtest config executors --help",
        "buildtest buildspec --help",
        "buildtest buildspec validate --help",
        "buildtest buildspec find --help",
        "buildtest report --help",
        "buildtest inspect --help",
        "buildtest cdash --help",
        "buildtest cdash upload --help",
        "buildtest help",
    ]
    for cmd in help_cmds:
        out = run(cmd)
        tmp_fname = cmd.replace(" ", "_") + ".txt"
        fname = os.path.join(docgen, tmp_fname)
        writer(fname, out, cmd)


def getting_started():

    prefix = "getting_started/buildspecs"

    cmd_dict = {
        "buildspec_find.txt": "buildtest buildspec find",
        "buildspec_filter.txt": "buildtest buildspec find --helpfilter",
        "buildspec_format.txt": "buildtest buildspec find --helpformat",
        "buildspec_find_tags.txt": "buildtest buildspec find --tags",
        "buildspec_find_buildspecfiles.txt": "buildtest buildspec find --buildspec",
        "buildspec_find_executors.txt": "buildtest buildspec find --executors",
        "buildspec_filter_type.txt": "buildtest buildspec find --filter type=script",
        "buildspec_filter_tags.txt": "buildtest buildspec find --filter tags=fail",
        "buildspec_multifield_filter.txt": "buildtest buildspec find --filter tags=tutorials,executor=generic.local.sh,type=script",
        "buildspec_format_example.txt": "buildtest buildspec find --format name,description,file --filter tags=tutorials,executor=generic.local.sh",
        "buildspec_find_group_by_tags.txt": "buildtest buildspec find --group-by-tags",
        "buildspec_find_group_by_executor.txt": "buildtest buildspec find --group-by-executor",
        "buildspec_find_maintainers.txt": "buildtest buildspec find --maintainers",
        "buildspec_find_maintainers_by_buildspecs.txt": "buildtest buildspec find --maintainers-by-buildspecs",
        "validate_buildspec.txt": "buildtest buildspec validate -b tutorials/vars.yml",
        "invalid_buildspec.txt": "buildtest buildspec validate -b tutorials/invalid_tags.yml",
        "validate_tags.txt": "buildtest buildspec validate -t python -t pass",
        "validate_executors.txt": "buildtest buildspec validate -e generic.local.csh",
    }
    generate_tests(prefix, cmd_dict)

    prefix = "getting_started/building"

    cmd_dict = {
        "buildspec_abspath.txt": "buildtest build -b $BUILDTEST_ROOT/tutorials/vars.yml",
        "buildspec_directory.txt": "buildtest build -b general_tests/configuration/",
        "multi_buildspecs.txt": "buildtest build -b general_tests/configuration/ -b tutorials/vars.yml",
        "exclude_buildspecs.txt": "buildtest build -b general_tests/configuration/ -x general_tests/configuration/ulimits.yml -x general_tests/configuration/ssh_localhost.yml",
        "invalid_buildspec.txt": "buildtest build -b tutorials/invalid_buildspec_section.yml",
        "invalid_executor.txt": "buildtest build -b tutorials/invalid_executor.yml",
        "tags.txt": "buildtest build --tags tutorials",
        "multi_tags.txt": "buildtest build --tags pass --tags python",
        "combine_tags_buildspec.txt": "buildtest build --tags pass --buildspec tutorials/python-hello.yml",
        "combine_filter_tags_buildspec.txt": "buildtest build --tags pass --filter-tags pass -b tutorials/python-hello.yml",
        "filter_tags_nobuildspecs.txt": "buildtest build -b tutorials/shell_examples.yml --filter-tags compile",
        "single_executor.txt": "buildtest build --executor generic.local.python",
        "multi_executor.txt": "buildtest build --executor generic.local.python --executor generic.local.csh",
        "stage_parse.txt": "buildtest build -b tutorials/vars.yml --stage=parse",
        "stage_build.txt": "buildtest build -b tutorials/vars.yml --stage=build",
        "rebuild.txt": "buildtest build -b tutorials/python-shell.yml --rebuild=3",
        "rebuild_tags.txt": "buildtest build --tags fail --rebuild=2",
    }

    generate_tests(prefix, cmd_dict)

    prefix = "getting_started/report"

    cmd_dict = {
        "report.txt": "buildtest report",
        "report_helpformat.txt": "buildtest report --helpformat",
        "report_helpfilter.txt": "buildtest report --helpfilter",
        "report_format.txt": "buildtest report --format name,id,executor,state,returncode",
        "report_filter_name.txt": "buildtest report --filter name=exit1_pass --format=name,id,returncode,state",
        "report_filter_buildspec.txt": "buildtest report --filter buildspec=tutorials/python-hello.yml --format=name,id,state,buildspec",
        "report_multifilter.txt": "buildtest report --filter state=FAIL,executor=generic.local.sh --format=name,id,state,executor",
        "report_returncode.txt": "buildtest report --filter returncode=2 --format=name,id,returncode",
        "buildtest_inspect_list.txt": "buildtest inspect list",
        "buildtest_inspect_names.txt": "buildtest inspect name shell_options",
        "buildtest_inspect_multi_names.txt": "buildtest inspect name bash_shell python_hello",
    }
    generate_tests(prefix, cmd_dict)

    prefix = "getting_started/features"
    cmd_dict = {
        "buildtest_history_list.txt": "buildtest history list",
        "buildtest_history_query.txt": "buildtest history query 0",
    }
    generate_tests(prefix, cmd_dict)

    prefix = "configuring"
    cmd_dict = {
        "config_view.txt": "buildtest config view",
        "config_validate.txt": "buildtest config validate",
        "config_summary.txt": "buildtest config summary",
        "config_executors.txt": "buildtest config executors",
    }
    generate_tests(prefix, cmd_dict)


def buildspecs_page():

    prefix = "buildspecs/overview"

    cmd_dict = {
        "regex_executor_script.txt": "buildtest build -b tutorials/executor_regex_script.yml",
        "runtime_status.txt": "buildtest build -b tutorials/runtime_status_test.yml",
        "runtime_status_report.txt": "buildtest report --filter buildspec=tutorials/runtime_status_test.yml --format name,id,state,runtime --latest",
        "vars.txt": "buildtest build -b tutorials/vars.yml",
        "shebang.txt": "buildtest build -b tutorials/shebang.yml",
        "pass_returncode.txt": "buildtest build -b tutorials/pass_returncode.yml",
        "skip_tests.txt": "buildtest build -b tutorials/skip_tests.yml",
        "root_user.txt": "buildtest build -b tutorials/root_user.yml",
        "run_only_platform.txt": "buildtest build -b tutorials/run_only_platform.yml",
        "bmgroups.txt": "buildtest build -b general_tests/sched/lsf/bmgroups.yml",
        "run_only_distro.txt": "buildtest build -b tutorials/run_only_distro.yml",
    }

    generate_tests(prefix, cmd_dict)

    prefix = "buildspecs/compiler"
    cmd_dict = {
        "gnu_hello.txt": "buildtest build -b tutorials/compilers/gnu_hello_fortran.yml"
    }

    generate_tests(prefix, cmd_dict)


def schemas():
    prefix = "schemas"
    cmd_dict = {
        "avail_schemas.txt": "buildtest schema",
        "settings_json.txt": "buildtest schema -n settings.schema.json --json",
        "settings_examples.txt": "buildtest schema -n settings.schema.json -e",
        "definitions_json.txt": "buildtest schema -n definitions.schema.json --json",
        "global_examples.txt": "buildtest schema -n global.schema.json --example",
        "global_json.txt": "buildtest schema -n global.schema.json --json",
        "script_examples.txt": "buildtest schema -n script-v1.0.schema.json --example",
        "script_json.txt": "buildtest schema -n script-v1.0.schema.json --json",
        "compiler_examples.txt": "buildtest schema -n compiler-v1.0.schema.json --example",
        "compiler_json.txt": "buildtest schema -n compiler-v1.0.schema.json --json",
        "spack_json.txt": "buildtest schema -n spack-v1.0.schema.json --json",
        "spack_examples.txt": "buildtest schema -n spack-v1.0.schema.json --example",
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
    build_helper()
    getting_started()
    buildspecs_page()
    schemas()


if __name__ == "__main__":
    main()
