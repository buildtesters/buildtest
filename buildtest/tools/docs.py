import os
import subprocess

from buildtest.defaults import BUILDTEST_ROOT, console
from buildtest.exceptions import BuildTestError
from buildtest.utils.file import create_dir, write_file


def run(query):
    """This method will execute command for the tutorials examples. If returncode
    is non-zero we raise exception otherwise we return output of command.

    Args:
        query (str): Run a arbitrary shell command.
    """

    print(f"Executing Command: {query}")
    command = subprocess.run(
        [query], shell=True, check=True, universal_newlines=True, capture_output=True
    )

    # for non-negative returncode
    if command.returncode != 0:
        raise BuildTestError(f"[red]Returncode: {command.returncode}")

    console.print(f"[green]Returncode: {command.returncode}")
    return command.stdout


def write_example(fname, command):
    """Given a shell command, we will write output to file. We will print first
    10 lines from upon writing file to ensure file was written properly.

    Args:
        fname (str): Path to file where output of command will be written
        command (str): Command that was executed

    """
    out = f"$ {command} \n"
    out += run(command)
    write_file(fname, out)

    console.print(f"Writing output to {fname}")
    console.rule(fname)

    # read first 10 lines of files written in example
    N = 10
    with open(fname, "r") as fd:
        firstNlines = fd.readlines()[0:N]
        firstNlines = "".join(firstNlines)

    console.print(firstNlines)


def build_aws_examples(autogen_dir):
    """This method will build AWS examples for the tutorial

    Args:
        autogen_dir (str): Directory where auto generated documentation examples will be written.
    """

    build_dir = os.path.join(autogen_dir)

    create_dir(build_dir)

    AWS_EXAMPLE_DIR = os.path.join(BUILDTEST_ROOT, "aws_tutorial")

    commands_to_run = {
        f"{build_dir}/hello_build.txt": f"buildtest build -b {AWS_EXAMPLE_DIR}/hello_world/hello.yml",
        f"{build_dir}/hello_inspect.txt": "buildtest inspect query -o -t hello_world_example",
        f"{build_dir}/multi_compiler_hello_build.txt": f"buildtest build -b {AWS_EXAMPLE_DIR}/hello_world/multi_compiler_hello.yml",
        f"{build_dir}/multi_compiler_hello_inspect.txt": "buildtest inspect query -o -t hello_world_multi_compiler/",
        f"{build_dir}/compiler_list_yaml.txt": "buildtest config compilers list --yaml",
        f"{build_dir}/mpiproc_build.txt": f"buildtest build -b {AWS_EXAMPLE_DIR}/mpiproc.yml",
        f"{build_dir}/mpiproc_inspect.txt": "buildtest inspect query -o mpiprocname",
        f"{build_dir}/osu_bandwidth_test_build.txt": f"buildtest build -b {AWS_EXAMPLE_DIR}/osu_bandwidth_test.yml",
        f"{build_dir}/osu_bandwidth_test_inspect.txt": "buildtest inspect query -o osu_bandwidth osu_bandwidth_perf",
        f"{build_dir}/openmp_example_build.txt": f"buildtest build -b {AWS_EXAMPLE_DIR}/openmp_example_custom_compiler.yml",
        f"{build_dir}/openmp_example_inspect.txt": "buildtest inspect query -o -t hello_world_openmp_custom_compiler/",
        f"{build_dir}/docker_helloworld_build.txt": f"buildtest build -b {BUILDTEST_ROOT}/tutorials/containers/hello_world.yml",
        f"{build_dir}/docker_helloworld_inspect.txt": "buildtest inspect query -o -t hello_world_docker",
        f"{build_dir}/singularity_helloworld_build.txt": f"buildtest build -b {BUILDTEST_ROOT}/tutorials/containers/hello_world_singularity.yml",
        f"{build_dir}/singularity_helloworld_inspect.txt": "buildtest inspect query -o -t hello_world_singularity",
        f"{build_dir}/container_executor_list.txt": f"buildtest -c $BUILDTEST_ROOT/buildtest/settings/container_executor.yml config executors list --yaml",
        f"{build_dir}/container_executor_build.txt": f"buildtest -c $BUILDTEST_ROOT/buildtest/settings/container_executor.yml build -b $BUILDTEST_ROOT/tutorials/containers/container_executor/ubuntu.yml",
        f"{build_dir}/container_executor_inspect.txt": "buildtest inspect query -o -t -b ubuntu_container_example",
    }

    for fname, command in commands_to_run.items():
        write_example(fname, command)


def build_spack_examples(autogen_dir):
    """This method will build spack examples for the tutorial

    Args:
        autogen_dir (str): Directory where auto generated documentation examples will be written.
    """

    build_dir = os.path.join(autogen_dir, "spack", "build")
    inspect_dir = os.path.join(autogen_dir, "spack", "inspect")

    create_dir(build_dir)
    create_dir(inspect_dir)

    SPACK_EXAMPLE_DIR = os.path.join(BUILDTEST_ROOT, "examples", "spack")
    commands_to_run = {
        f"{build_dir}/install_specs.txt": f"buildtest build -b {SPACK_EXAMPLE_DIR}/install_specs.yml",
        f"{build_dir}/env_install.txt": f"buildtest build -b {SPACK_EXAMPLE_DIR}/env_install.yml",
        f"{build_dir}/env_create_directory.txt": f"buildtest build -b {SPACK_EXAMPLE_DIR}/env_create_directory.yml",
        f"{build_dir}/env_create_manifest.txt": f"buildtest build -b {SPACK_EXAMPLE_DIR}/env_create_manifest.yml",
        f"{build_dir}/remove_environment_example.txt": f"buildtest build -b {SPACK_EXAMPLE_DIR}/remove_environment_example.yml",
        f"{build_dir}/spack_env_deactivate.txt": f"buildtest build -b {SPACK_EXAMPLE_DIR}/spack_env_deactivate.yml",
        f"{build_dir}/pre_post_cmds.txt": f"buildtest build -b {SPACK_EXAMPLE_DIR}/pre_post_cmds.yml",
        f"{build_dir}/mirror_example.txt": f"buildtest build -b {SPACK_EXAMPLE_DIR}/mirror_example.yml",
        f"{build_dir}/spack_load.txt": f"buildtest build -b {SPACK_EXAMPLE_DIR}/spack_load.yml",
        f"{build_dir}/spack_test.txt": f"buildtest build -b {SPACK_EXAMPLE_DIR}/spack_test.yml",
        f"{build_dir}/spack_test_specs.txt": f"buildtest build -b {SPACK_EXAMPLE_DIR}/spack_test_specs.yml",
        f"{build_dir}/spack_sbatch.txt": f"buildtest build -b {SPACK_EXAMPLE_DIR}/spack_sbatch.yml",
        f"{build_dir}/e4s_testsuite_mpich.txt": f"buildtest build -b {SPACK_EXAMPLE_DIR}/e4s_testsuite_mpich.yml",
        f"{build_dir}/clone_spack.txt": f"buildtest build -b {SPACK_EXAMPLE_DIR}/clone_spack.yml",
        f"{inspect_dir}/install_specs.txt": "buildtest inspect query -o -t install_specs_example",
        f"{inspect_dir}/env_install.txt": "buildtest inspect query -t install_in_spack_env",
        f"{inspect_dir}/env_create_directory.txt": "buildtest inspect query -o -t spack_env_directory",
        f"{inspect_dir}/env_create_manifest.txt": "buildtest inspect query -o -t spack_env_create_from_manifest",
        f"{inspect_dir}/spack_env_deactivate.txt": "buildtest inspect query -t spack_env_deactivate_first",
        f"{inspect_dir}/remove_environment_example.txt": "buildtest inspect query -t remove_environment_automatically remove_environment_explicit",
        f"{inspect_dir}/pre_post_cmds.txt": "buildtest inspect query -o -t run_pre_post_commands",
        f"{inspect_dir}/mirror_example.txt": "buildtest inspect query -o  -t add_mirror add_mirror_in_spack_env",
        f"{inspect_dir}/spack_load.txt": "buildtest inspect query -t spack_load_example",
        f"{inspect_dir}/spack_test.txt": "buildtest inspect query -o -t spack_test_m4",
        f"{inspect_dir}/spack_test_specs.txt": "buildtest inspect query -o -t spack_test_results_specs_format",
        f"{inspect_dir}/spack_sbatch.txt": "buildtest inspect query -t spack_sbatch_example",
        f"{inspect_dir}/clone_spack.txt": "buildtest inspect query -o -t clone_spack_automatically clone_spack_and_specify_root",
        f"{inspect_dir}/e4s_testsuite_mpich.txt": "buildtest inspect query -o -e -t mpich_e4s_testsuite",
    }

    for fname, command in commands_to_run.items():
        write_example(fname, command)
