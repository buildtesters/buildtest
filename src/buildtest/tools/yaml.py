############################################################################
#
#  Copyright 2017-2019
#
#   https://github.com/HPC-buildtest/buildtest-framework
#
#  This file is part of buildtest.
#
#    buildtest is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    buildtest is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with buildtest.  If not, see <http://www.gnu.org/licenses/>.
#############################################################################

import subprocess
import yaml

TEMPLATE_JOB_SLURM = {
    'nodes': "10",
    'cpus-per-task': "4",
    'ntasks': "2",
    'ntasks-per-node': "4",
    'mem': "20G",
    'mem-per-cpu': "1G",
    'time': "01:00:00",
    'constraint': "gpu",
}
TEMPLATE_JOB_LSF = {
    'M': "200M",
    "n": "[min,max]",
    'R': "gpu",
    "T": "4",
    "W": "01:00:00",
}
TEMPLATE_MPI = {
    'wrapper': "mpicc",
    'launcher': "mpirun",
    'procs': 4
}
SUPPORTED_COMPILERS = ['gnu','intel','cuda']
SUPPORTED_MPI_WRAPPERS = [
    "mpicc",
    "mpifort",
    "mpicxx",
    "mpiicc",
    "mpiifort",
    "mpiicpc"
]
SUPPORTED_MPI_LAUNCHERS = [
    "mpirun",
    "mpiexec",
    "srun"
]
SUPPORTED_MPI_FLAVORS = [
    "openmpi",
    "intelmpi",
    "mpich",
    "mvapich2"
]
TEMPLATE_VARS = {
    'foo': 'bar'
}
TEMPLATE_VARIANT = [
    {'variant': {"flags": "-O1"}},
    {'variant': {"flags": "-O3"}},
]

TEMPLATE_SINGLESOURCE = {
    'description': 'description of test',
    'source': "file.c",
    'input': "inputfile",
    'flags': "-O3 -fast",
    'vars': TEMPLATE_VARS,
    'compiler': "gnu",
    'ldflags': "-lm",
    'args': "args1 args2 args3",
    'slurm': TEMPLATE_JOB_SLURM,
    'lsf': TEMPLATE_JOB_LSF,
    'variants': TEMPLATE_VARIANT,
    'mpi': TEMPLATE_MPI,
    'maintainer': [
        "shahzeb siddiqui shahzebmsiddiqui@gmail.com"
    ]
}

KEY_DESCRIPTION = {
    'description': "Specify a brief description of test",
    'source': "Specify the name of the source file that is in the \"src\" "
              "directory relative to yaml configuration",
    'input': "Specify input file for the executable. This file must be in "
             "\"src\" directory",
    'flags': "Specify the build flags for compiling the source program",
    'vars': "Specify a list of environment variables that will be declared in "
            "the test script",
    'compiler': "Specify a compiler that will be used for compiling the "
                "source program",
    'ldflags': "Flags that will be passed to linkder (ld)",
    'args': "Input arguments to be passed to the executable",
    'slurm': "Specify SLURM configuration",
    'lsf': "Specify LSF configuration",
    'mpi': "Specify MPI configuration"
}
LSF_KEY_DESC = {
    'M': ["#BSUB -M", "Memory Limit"],
    'n': ["#BSUB -n", "Submits a parallel job and specifies the number of "
                      "processors required to run the job"],
    'R': ["#BSUB -R", "Runs the job on a host that meets the specified "
                      "resource requirements"],
    'T': ["#BSUB -T", "Sets the limit of the number of concurrent threads to "
                      "thread_limit for the whole job"],
    'W': ["#BSUB -W", "Sets the runtime limit of the job."]
}
SLURM_KEY_DESC = {
    'nodes':  ["#SBATCH --nodes", "number of nodes on which to run (N = min[-max])"],
    'cpus-per-task': ["#SBATCH --cpus-per-task", "number of cpus required per task."],
    'ntasks': ["#SBATCH --ntasks", "number of tasks to run."],
    'ntasks-per-node': ["#SBATCH --ntasks-per-node", "number of tasks to invoke on each node"],
    'mem': ["#SBATCH --mem", "minimum amount of real memory."],
    'mem-per-cpu':["#SBATCH --mem-per-cpu", "maximum amount of real memory per allocated"],
    'time': ["#SBATCH --time", "time limit"],
    'constraint': ["#SBATCH --constraint", "specify a list of constraints"]
}
MPI_KEY_DESC = {
    'srun': ['srun', "use the srun job launcher"],
    'openmpi': ['openmpi', "use the orterun job launcher"],
    'mpich': ['mpich', "use the mpiexec.hydra job launcher"]
}
ORTERUN_KEY_DESC = {
    'n': ["-n", "Run  this many copies of the program on the given nodes"],
    'npernode': ["-npernode", "On each node, launch this many processes."],
    'npersocket': ["--npersocket", "On each node, launch this many processes "
                                   "times the number of processor sockets on "
                                   "the node"],
    'report-bindings': ["--report-bindings","Report any bindings for "
                                            "launched processes."],
    'display-map': ["--display-map", "Display a table showing the mapped "
                                     "location of each process prior to launch."]
}

MPIEXEC_KEY_DESC = {
    'n': ["-n", "Run  this many copies of the program on the given nodes"],
}

def get_environment_variable(shell,key,value):
    """ get environment variable based on shell type"""

    if shell == "sh" or shell == "bash":
        return "export %s=%s" %(key,value)
    elif shell == "csh":
        return ("setenv %s %s" %(key,value))

def get_compiler(language, compiler):
    """Return compiler based on language

    :param language: Language type
    :type language: str, required
    :param compiler: Compiler Type
    :type compiler: str, required
    :return: return compiler wrapper
    :rtype: str
    """

    if language == "c" and compiler == "gnu":
        return "gcc"
    if language == "c++" and compiler == "gnu":
        return "g++"
    if language == "fortran" and compiler == "gnu":
        return "gfortran"

    if language == "c" and compiler == "intel":
        return "icc"
    if language == "c++" and compiler == "intel":
        return "icpc"
    if language == "fortran" and compiler == "intel":
        return "ifort"

    if language == "cuda":
        return "nvcc"

def get_mpi_wrapper(language, compiler):
    """ Get MPI wrapper based on Language and compiler.

    :param language: Language type
    :type language: str, required
    :param compiler: Compiler Type
    :type compiler: str, required

    :return: return compiler wrapper
    :rtype: str
    """
    if language == "c" and compiler == "gnu":
        return "mpicc"
    if language == "c++" and compiler == "gnu":
        return "mpicxx"
    if language == "fortran" and compiler == "gnu":
        return "mpifort"

    if language == "c" and compiler == "intel":
        return "mpiicc"
    if language == "c++" and compiler == "intel":
        return "mpiicpc"
    if language == "fortran" and compiler == "intel":
        return "mpiifort"

def get_programming_language(ext):
    """ Return Programming Language  based on extension

    :param ext: File extension of source file
    :type ext: str, required
    :return: return programming language
    :rtype: str
    """
    if ext in ['.c']:
        return "c"
    if ext in ['.cc', '.cxx', '.cpp', '.c++', '.C']:
         return "c++"
    if ext in ['.f90', '.f95', '.f03', '.f', '.F', '.F90', '.FPP', '.FOR',
               '.FTN', '.for', '.ftn']:
        return "fortran"
    if ext in ['.cu']:
        return "cuda"
    if ext in ['.py']:
        return "python"

def lsf_key_parse(lsf_dict):
    """Convert lsf keys to ``#BSUB`` command

    :param lsf_dict: LSF YAML keys
    :type lsf_dict: dict, required
    :return: return #BSUB command to be injected in test script.
    :rtype: str
    """
    lsf_str = ""
    for key,val in lsf_dict.items():
        lsf_str += "#BSUB -" + key + " " + str(val) + "\n"
    return lsf_str

def slurm_key_parse(slurm_dict):
    """Convert slurm keys to ``#SBATCH`` command.

    :param slurm_dict: LSF YAML keys
    :type slurm_dict: dict, required
    :return: return #SBATCH command to be injected in test script.
    :rtype: str
    """
    slurm_str = ""
    for key,val in slurm_dict.items():
        slurm_str += "#SBATCH --" + key + " " + str(val) + "\n"
    return slurm_str
