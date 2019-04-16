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

"""
buildtest yaml subcommand entry point
"""

import os
import subprocess
import sys
import yaml

from buildtest.tools.config import config_opts
from buildtest.tools.ohpc import check_ohpc
from buildtest.tools.file import is_file


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
   'type': "openmpi",
   'num_procs':  4
}
SUPPORTED_COMPILERS = ['gnu','intel','cuda']
TEMPLATE_VARS = {
    'foo': 'bar'
}
TEMPLATE_VARIANT = [
    {'variant': {"flags": "-O1"}},
    {'variant': {"flags": "-O3"}},
]

TEMPLATE_SINGLESOURCE = {
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
    'maintainer': [
        "shahzeb siddiqui shahzebmsiddiqui@gmail.com"
    ]
}

KEY_DESCRIPTION = {
    'source': "Specify the name of the source file that is in the \"src\" directory relative to yaml configuration",
    'input': "Specify input file for the executable. This file must be in \"src\" directory",
    'flags': "Specify the build flags for compiling the source program",
    'vars': "Specify a list of environment variables that will be declared in the test script",
    'compiler': "Specify a compiler that will be used for compiling the source program",
    'ldflags': "Flags that will be passed to linkder (ld)",
    'args': "Input arguments to be passed to the executable",
    'slurm': "Specify SLURM configuration",
    'lsf': "Specify LSF configuration",
}
LSF_KEY_DESC = {
    'M': ["#BSUB -M", "Memory Limit"],
    'n': ["#BSUB -n", "Submits a parallel job and specifies the number of processors required to run the job"],
    'R': ["#BSUB -R", "Runs the job on a host that meets the specified resource requirements"],
    'T': ["#BSUB -T", "Sets the limit of the number of concurrent threads to thread_limit for the whole job"],
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
class BuildTestYamlSingleSource():

    yaml_file = ""
    def __init__(self,yaml_file,args,shell):

        is_file(yaml_file)

        ext = os.path.splitext(yaml_file)[1]

        if ext != ".yml":
            print("Invalid File extension: " + ext)
            sys.exit(1)

        self.yaml_file=yaml_file
        self.test_suite = args.suite
        self.shell = shell
        self.parent_dir = os.path.basename(os.path.dirname(self.yaml_file))
        self.test_suite_dir = os.path.join(config_opts["BUILDTEST_CONFIGS_REPO"],
                                           "buildtest",
                                           "suite")
        self.srcdir = os.path.join(self.test_suite_dir,
                                   self.test_suite,
                                   self.parent_dir,
                                   "src")
        self.software_module = args.software
        self.verbose = args.verbose

    def _check_keys(self, dict):
        """Check keys specified in YAML file with buildtest templates and
        type check value. """
        mpi_keys =  None
        for k,v in dict.items():
            # ignore key testblock
            if k == "testblock":
                continue
            if k not in TEMPLATE_SINGLESOURCE.keys():
                print("Invalid Key: " + k)
                sys.exit(1)

            # type checking against corresponding value of key in template
            if type(v) != type(TEMPLATE_SINGLESOURCE[k]):
                    print(f"Type mismatch for key: {k}"
                          + f"Got Type: {str(type(v))} +  Expecting Type:"
                          + str(type(TEMPLATE_SINGLESOURCE[k])))
                    sys.exit(1)
    def _check_compiler(self,compiler):
        # check if compiler value is in list of supported compiler supported
        if compiler not in SUPPORTED_COMPILERS:
            print (compiler + " is not a supported compiler:")
            sys.exit(0)

    def _check_lsf(self,lsf_dict):
        for k,v in lsf_dict.items():
            if k not in TEMPLATE_JOB_LSF.keys():
                print("Invalid Key: " + k)
                sys.exit(1)

            if type(v) != type(TEMPLATE_JOB_LSF[k]):
                print(f"Type mismatch for key: {k} Got Type: {str(type(v))}"
                      + f"Expecting Type: {str(type(TEMPLATE_JOB_LSF[k]))}" )
                sys.exit(1)
    def _check_slurm(self,slurm_dict):
        for k,v in  slurm_dict.items():
            if k not in TEMPLATE_JOB_SLURM.keys():
                print("Invalid Key: " + k)
                sys.exit(1)

            if type(v) != type(TEMPLATE_JOB_SLURM[k]):
                print(f"Type mismatch for key: {k} Got Type: {str(type(v))}"
                      + f"Expecting Type: {str(type(TEMPLATE_JOB_SLURM[k]))}")
                sys.exit(1)

    def parse(self):
        """ Parse yaml file to determine if content follows the defined yaml
        schema."""
        module_str = env_vars = ""
        testscript_dict = {}

        fd=open(self.yaml_file,'r')
        test_dict=yaml.safe_load(fd)

        if self.verbose >= 2:
            print ("{:_<80}".format(""))
            print (yaml.dump(test_dict,default_flow_style=False))
            print ("{:_<80}".format(""))

        self._check_keys(test_dict)
        if self.verbose >= 1:
            print (f"Key Check PASSED for file {self.yaml_file}")

        srcfile = os.path.join(self.srcdir,test_dict['source'])
        is_file(srcfile)

        if self.verbose >= 2:
            print (f"Source File {srcfile} exists!")
        ext = os.path.splitext(srcfile)[1]
        language = get_programming_language(ext)
        if self.verbose >= 1:
            print (f"Programming Language Detected: {language}")
        exec_name = '%s.exe' % test_dict['source']
        cmd = []

        if "lsf" in test_dict:
            self._check_lsf(test_dict['lsf'])
            if self.verbose >= 1:
                print ("LSF Keys Passed")

            testscript_dict["lsf"] = lsf_key_parse(test_dict['lsf'])

        if "slurm" in test_dict:
            self._check_slurm(test_dict['slurm'])
            if self.verbose >= 1:
                print ("SLURM Keys Passed")
            testscript_dict["slurm"] = slurm_key_parse(test_dict['slurm'])

        if "input" in test_dict:
            inputfile = os.path.join(self.srcdir,test_dict['input'])
            is_file(inputfile)
        if "compiler" in test_dict:
            self._check_compiler(test_dict['compiler'])
            if self.verbose >= 1:
                print ("Compiler Check Passed")
            compiler_name = get_compiler(language,test_dict['compiler'])
            cmd += [compiler_name]

            if "flags" in test_dict:
                cmd += [test_dict['flags']]

            cmd += ['-o',exec_name,srcfile]

            if "ldflags" in test_dict:
                cmd += [test_dict['ldflags']]

        if "input" in test_dict:
            cmd += ["<", os.path.join(self.srcdir,inputfile) ]


        module_str = "module purge"

        # if vars key is defined then get all environment variables
        if "vars" in test_dict:
            for k,v in test_dict['vars'].items():
                if self.verbose >= 1:
                    print (f"Detecting environment {k}={v}")

                env_vars += get_environment_variable(self.shell,k,v)


        workdir = os.path.join(config_opts["BUILDTEST_TESTDIR"],
                               "suite",
                               self.test_suite,
                               self.parent_dir)

        testscript_dict["vars"] = env_vars
        testscript_dict["module"] = module_str + "\n"
        testscript_dict["workdir"] = "cd " + workdir + "\n"
        testscript_dict["command"] = cmd

        if "args" in test_dict:
            testscript_dict["run"] = f"./{exec_name} {test_dict['args']} \n"
        else:
            testscript_dict["run"] = f"./{exec_name} \n"

        testscript_dict["post_run"] = f"rm ./{exec_name} \n"

        return test_dict, testscript_dict
def get_environment_variable(shell,key,value):
    """ get environment variable based on shell type"""
    if shell == "sh" or shell == "bash":
        return "export %s=%s \n" %(key,value)
    elif shell == "csh":
        return ("setenv %s %s \n" %(key,value))

def get_compiler(language, compiler):
    """ return compiler based on language"""

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

def get_programming_language(ext):
    """ return Programming Language  based on extension"""
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
    """ parse lsf keys """
    lsf_str = ""
    for key,val in lsf_dict.items():
        lsf_str += "#BSUB -" + key + " " + str(val) + "\n"
    return lsf_str

def slurm_key_parse(slurm_dict):
    """ parse lsf keys """
    lsf_str = ""
    for key,val in slurm_dict.items():
        lsf_str += "#SBATCH -" + key + " " + str(val) + "\n"
    return lsf_str

def func_yaml_subcmd(args):
    """ entry point to _buildtest yaml """

    if args.ohpc:
        check_ohpc()
        config_opts["BUILDTEST_OHPC"] = True
    if args.maintainer:
        update_maintainer(args)

def update_maintainer(args):
    """Update maintainer key in test configuration."""

    git_user_name = subprocess.getoutput(
        "git config --get user.name").rstrip().lower()
    git_user_email = subprocess.getoutput(
        "git config --get user.email").rstrip().lower()

    entry = (f"{git_user_name} {git_user_email}")

    fd = open(args.config, "r")
    content = yaml.safe_load(fd)
    fd.close()

    # if user wants to be maintainer of file
    if args.maintainer == "yes":
        # if user the first maintainer to file
        if "maintainer" not in content:
            content["maintainer"] = []
            content["maintainer"].append(entry)
        else:
            if entry not in content["maintainer"]:
                content["maintainer"].append(entry)
                print (f"Adding Maintainer: {entry} to file {args.config}")
            else:
                print (f"{entry} is already a maintainer")
                return


        write_fd = open(args.config, "w")
        yaml.dump(content, write_fd, default_flow_style=False)
        write_fd.close()

    # if user wants to be removed from maintainer
    else:
        # if maintainer key found then only check if user exist in list,
        # otherwise no action is needed
        if "maintainer" in content:
            if entry in content["maintainer"]:
                write_fd = open(args.config, "w")
                content["maintainer"].remove(entry)
                # if no maintainers are left after removal, then delete the
                # key. It may be worth changing this behavior to ensure one
                # maintainer is always present
                if len(content["maintainer"]) == 0:
                    del(content["maintainer"])

                yaml.dump(content, write_fd, default_flow_style=False)
                write_fd.close()

                print (f"Removing Maintainer: {entry} from file {args.config}")
            else:
                print (f"{entry} is not a maintainer of file {args.config}")
                return

    print (f"----------------- FILE:{args.config} ----------------------")
    print (yaml.dump(content, default_flow_style=False))