import getpass
import os
import shutil
import subprocess
import sys

from buildtest.cli.clean import clean
from buildtest.config import SiteConfiguration
from buildtest.defaults import BUILDTEST_ROOT
from buildtest.utils.file import create_dir, is_dir, is_file, write_file

doc_example_dir = os.path.join(BUILDTEST_ROOT, "docs", "buildtest_tutorial_examples")
config = SiteConfiguration(
    os.path.join(BUILDTEST_ROOT, "settings", "spack_container.yml")
)
config.detect_system()
config.validate(validate_executors=True)


def run(query):
    """The ``run()`` method will execute the command and retrieve the output as part of documentation examples"""

    print(f"Executing Command: {query}")
    command = subprocess.run(
        [query], shell=True, check=True, universal_newlines=True, capture_output=True
    )
    return command.stdout


def build_examples():

    build_dir = os.path.join(doc_example_dir, "build")
    inspect_dir = os.path.join(doc_example_dir, "inspect")

    create_dir(build_dir)
    create_dir(inspect_dir)

    commands_to_run = {
        f"{build_dir}/install_specs.txt": f"buildtest build -b {BUILDTEST_ROOT}/examples/spack/install_specs.yml",
        f"{build_dir}/env_install.txt": f"buildtest build -b {BUILDTEST_ROOT}/examples/spack/env_install.yml",
        f"{build_dir}/env_create_directory.txt": f"buildtest build -b {BUILDTEST_ROOT}/examples/spack/env_create_directory.yml",
        f"{build_dir}/env_create_manifest.txt": f"buildtest build -b {BUILDTEST_ROOT}/examples/spack/env_create_manifest.yml",
        f"{build_dir}/remove_environment_example.txt": f"buildtest build -b {BUILDTEST_ROOT}/examples/spack/remove_environment_example.yml",
        f"{build_dir}/pre_post_cmds.txt": f"buildtest build -b {BUILDTEST_ROOT}/examples/spack/pre_post_cmds.yml",
        f"{build_dir}/mirror_example.txt": f"buildtest build -b {BUILDTEST_ROOT}/examples/spack/mirror_example.yml",
        f"{build_dir}/spack_test.txt": f"buildtest build -b {BUILDTEST_ROOT}/examples/spack/spack_test.yml",
        f"{build_dir}/spack_test_specs.txt": f"buildtest build -b {BUILDTEST_ROOT}/examples/spack/spack_test_specs.yml",
        f"{build_dir}/spack_sbatch.txt": f"buildtest build -b {BUILDTEST_ROOT}/examples/spack/spack_sbatch.yml",
        f"{inspect_dir}/install_specs.txt": "buildtest inspect query -o -t install_specs_example",
        f"{inspect_dir}/env_install.txt": "buildtest inspect query -t install_in_spack_env",
        f"{inspect_dir}/env_create_directory.txt": "buildtest inspect query -o -t spack_env_directory",
        f"{inspect_dir}/env_create_manifest.txt": "buildtest inspect query -o -t spack_env_create_from_manifest",
        f"{inspect_dir}/remove_environment_example.txt": "buildtest inspect query -t remove_environment_automatically remove_environment_explicit",
        f"{inspect_dir}/pre_post_cmds.txt": "buildtest inspect query -o -t run_pre_post_commands",
        f"{inspect_dir}/mirror_example.txt": "buildtest inspect query -o  -t add_mirror add_mirror_in_spack_env",
        f"{inspect_dir}/spack_test.txt": "buildtest inspect query -o -t spack_test_m4",
        f"{inspect_dir}/spack_test_specs.txt": "buildtest inspect query -o -t spack_test_results_specs_format",
        f"{inspect_dir}/spack_sbatch.txt": "buildtest inspect query -t spack_sbatch_example",
    }
    for fname, command in commands_to_run.items():
        out = f"$ {command} \n"
        out += run(command)
        write_file(fname, out)


if __name__ == "__main__":

    if getpass.getuser() != "spack" or os.getenv("HOME") != "/home/spack":
        sys.exit(
            "This script can only be run inside container please run the following 'docker run -it -v $BUILDTEST_ROOT:/home/spack/buildtest shahzebsiddiqui/buildtest_spack'"
        )

    if is_file(doc_example_dir):
        os.remove(doc_example_dir)

    if is_dir(doc_example_dir):
        shutil.rmtree(doc_example_dir)

    create_dir(doc_example_dir)

    clean(config, yes=True)
    build_examples()
