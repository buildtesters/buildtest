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
        f"{build_dir}/pre_post_cmds.txt": f"buildtest build -b {SPACK_EXAMPLE_DIR}/pre_post_cmds.yml",
        f"{build_dir}/mirror_example.txt": f"buildtest build -b {SPACK_EXAMPLE_DIR}/mirror_example.yml",
        f"{build_dir}/spack_test.txt": f"buildtest build -b {SPACK_EXAMPLE_DIR}/spack_test.yml",
        f"{build_dir}/spack_test_specs.txt": f"buildtest build -b {SPACK_EXAMPLE_DIR}/spack_test_specs.yml",
        f"{build_dir}/spack_sbatch.txt": f"buildtest build -b {SPACK_EXAMPLE_DIR}/spack_sbatch.yml",
        f"{build_dir}/e4s_testuite_mpich.txt": f"buildtest build -b {SPACK_EXAMPLE_DIR}/e4s_testuite_mpich.yml",
        f"{inspect_dir}/install_specs.txt": "buildtest inspect query -o -t install_specs_example clone_spack_and_install_zlib",
        f"{inspect_dir}/env_install.txt": "buildtest inspect query -t install_in_spack_env",
        f"{inspect_dir}/env_create_directory.txt": "buildtest inspect query -o -t spack_env_directory",
        f"{inspect_dir}/env_create_manifest.txt": "buildtest inspect query -o -t spack_env_create_from_manifest",
        f"{inspect_dir}/remove_environment_example.txt": "buildtest inspect query -t remove_environment_automatically remove_environment_explicit",
        f"{inspect_dir}/pre_post_cmds.txt": "buildtest inspect query -o -t run_pre_post_commands",
        f"{inspect_dir}/mirror_example.txt": "buildtest inspect query -o  -t add_mirror add_mirror_in_spack_env",
        f"{inspect_dir}/spack_test.txt": "buildtest inspect query -o -t spack_test_m4",
        f"{inspect_dir}/spack_test_specs.txt": "buildtest inspect query -o -t spack_test_results_specs_format",
        f"{inspect_dir}/spack_sbatch.txt": "buildtest inspect query -t spack_sbatch_example",
        f"{inspect_dir}/e4s_testuite_mpich.txt": "buildtest inspect query -o -e -t mpich_e4s_testsuite",
    }

    for fname, command in commands_to_run.items():
        write_example(fname, command)


def build_compiler_examples(autogen_dir):
    """This method will build examples for compiler examples for the tutorial

    Args:
        autogen_dir (str): Directory where auto generated documentation examples will be written.
    """
    compiler_dir = os.path.join(autogen_dir, "compilers")
    build_dir = os.path.join(compiler_dir, "build")
    inspect_dir = os.path.join(compiler_dir, "inspect")

    create_dir(compiler_dir)
    create_dir(build_dir)
    create_dir(inspect_dir)

    COMPILER_EXAMPLE_DIR = os.path.join(BUILDTEST_ROOT, "examples", "compilers")
    commands_to_run = {
        f"{build_dir}/gnu_hello_fortran.txt": f"buildtest build -b {COMPILER_EXAMPLE_DIR}/gnu_hello_fortran.yml",
        f"{inspect_dir}/gnu_hello_fortran.txt": "buildtest inspect query -t hello_f",
        f"{compiler_dir}/compilers_list.txt": "buildtest config compilers -y",
        f"{build_dir}/vecadd.txt": f"buildtest build -b {COMPILER_EXAMPLE_DIR}/vecadd.yml",
        f"{build_dir}/gnu_hello_c.txt": f"buildtest build -b {COMPILER_EXAMPLE_DIR}/gnu_hello_c.yml",
        f"{inspect_dir}/gnu_hello_c.txt": "buildtest inspect query -t hello_c/",
        f"{build_dir}/compiler_exclude.txt": f"buildtest build -b {COMPILER_EXAMPLE_DIR}/compiler_exclude.yml",
        f"{build_dir}/openmp_hello.txt": f"buildtest build -b {COMPILER_EXAMPLE_DIR}/openmp_hello.yml",
        f"{inspect_dir}/openmp_hello.txt": "buildtest inspect query -t openmp_hello_c_example",
        f"{build_dir}/envvar_override.txt": f"buildtest build -b {COMPILER_EXAMPLE_DIR}/envvar_override.yml",
        f"{inspect_dir}/envvar_override.txt": "buildtest inspect query -t override_environmentvars/",
        f"{build_dir}/compiler_status_regex.txt": f"buildtest build -b {COMPILER_EXAMPLE_DIR}/compiler_status_regex.yml",
        f"{inspect_dir}/compiler_status_regex.txt": "buildtest inspect query -o override_status_regex/",
        f"{build_dir}/custom_run.txt": f"buildtest build -b {COMPILER_EXAMPLE_DIR}/custom_run.yml",
        f"{inspect_dir}/custom_run.txt": "buildtest inspect query -b  -t custom_run_by_compilers/",
        f"{build_dir}/pre_post_build_run.txt": f"buildtest build -b {COMPILER_EXAMPLE_DIR}/pre_post_build_run.yml",
        f"{inspect_dir}/pre_post_build_run.txt": "buildtest inspect query -t pre_post_build_run",
        f"{build_dir}/stream_example.txt": f"buildtest build -b {COMPILER_EXAMPLE_DIR}/stream_example.yml",
        f"{inspect_dir}/stream_example.txt": "buildtest inspect query -t stream_openmp_c/",
        f"{build_dir}/stream_example_metrics.txt": f"buildtest build -b {COMPILER_EXAMPLE_DIR}/stream_example_metrics.yml",
        f"{inspect_dir}/stream_openmp_metrics.txt": "buildtest inspect query -o stream_openmp_metrics/",
    }

    for fname, command in commands_to_run.items():
        write_example(fname, command)
