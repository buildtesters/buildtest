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
import sys
import yaml
from datetime import datetime
from ruamel.yaml import YAML

from buildtest.tools.config import config_opts
from buildtest.tools.ohpc import check_ohpc
from buildtest.tools.software import get_software_stack
from buildtest.test.sourcetest import get_environment_variable
from buildtest.tools.file import isFile

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
SUPPORTED_COMPILERS = ['gnu','intel']
TEMPLATE_VARS = {
    'foo': 'bar'
}
TEMPLATE_GENERAL = {
    'source': "file.c",
    'input': "inputfile",
    'flags': "-O3 -fast",
    'vars': TEMPLATE_VARS,
    'module': ["gcc","zlib"],
    'compiler': "gnu",
    'ldflags': "-lm",
    'args': "args1 args2 args3",
    'slurm': TEMPLATE_JOB_SLURM,
    'lsf': TEMPLATE_JOB_LSF,
    'mpi': TEMPLATE_MPI,
}

#TEMPLATE = ['test', TEMPLATE_GENERAL]

class BuildTestYamlSingleSource():

    yaml_file = ""
    def __init__(self,yaml_file,test_suite,shell):

        isFile(yaml_file)

        ext = os.path.splitext(yaml_file)[1]

        if ext != ".yml":
            print("Invalid File extension: " + ext)
            sys.exit(1)

        self.yaml_file=yaml_file
        self.test_suite = test_suite
        self.shell = shell
        self.parent_dir = os.path.basename(os.path.dirname(self.yaml_file))
        self.test_suite_dir = os.path.join(config_opts["BUILDTEST_CONFIGS_REPO"],"buildtest","suite")
        self.srcdir = os.path.join(self.test_suite_dir, self.test_suite, self.parent_dir,"src")

    def _check_keys(self, dict):
        """ check keys specified in YAML file with buildtest templates and type check value """
        mpi_keys =  None
        for k,v in dict.items():
            if k not in TEMPLATE_GENERAL.keys():
                print("Invalid Key: " + k)
                sys.exit(1)

            # type checking against corresponding value of key in template
            if type(v) != type(TEMPLATE_GENERAL[k]):
                    print("Type mismatch for key: " + k  + " Got Type: " + str(type(v)) + " Expecting Type:" + str(type(TEMPLATE_GENERAL[k])))
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
                print("Type mismatch for key: " + k  + " Got Type: " + str(type(v)) + " Expecting Type:" + str(type(TEMPLATE_JOB_LSF[k])))
                sys.exit(1)
    def _check_slurm(self,slurm_dict):
        for k,v in  slurm_dict.items():
            if k not in TEMPLATE_JOB_SLURM.keys():
                print("Invalid Key: " + k)
                sys.exit(1)

            if type(v) != type(TEMPLATE_JOB_SLURM[k]):
                print("Type mismatch for key: " + k  + " Got Type: " + str(type(v)) + " Expecting Type:" + str(type(TEMPLATE_JOB_SLURM[k])))
                sys.exit(1)

    def parse(self):
        """ parse a yaml file to determine if content follows buildtest yaml schema"""
        flags = module_str = env_vars = ""
        testscript_dict = {}

        fd=open(self.yaml_file,'r')
        content=yaml.load(fd)
        test_dict = content['test']
        self._check_keys(test_dict)

        srcfile = os.path.join(self.srcdir,test_dict['source'])
        isFile(srcfile)

        ext = os.path.splitext(srcfile)[1]
        language = get_programming_language(ext)
        exec_name = '%s.exe' % test_dict['source']
        cmd = []

        if "lsf" in test_dict:
            self._check_lsf(test_dict['lsf'])
            testscript_dict["lsf"] = lsf_key_parse(test_dict['lsf'])
        if "slurm" in test_dict:
            self._check_slurm(test_dict['slurm'])
            testscript_dict["slurm"] = slurm_key_parse(test_dict['slurm'])

        if "input" in test_dict:
            inputfile = os.path.join(self.srcdir,test_dict['input'])
            isFile(inputfile)
        if "compiler" in test_dict:
            self._check_compiler(test_dict['compiler'])
            compiler_name = get_compiler(language,test_dict['compiler'])
            cmd += [compiler_name]

            if "flags" in test_dict:
                cmd += [test_dict['flags']]

            cmd += ['-o',exec_name,srcfile]

            if "ldflags" in test_dict:
                cmd += [test_dict['ldflags']]

        if "input" in test_dict:
            cmd += ["<", os.path.join(self.srcdir,inputfile) ]

        # if module key is defined then figure out module load
        if "module" in test_dict:
            module_key_dict = test_dict['module']
            modulelist = get_software_stack()
            module_str = "module purge \n"
            # go through all modules in software stack and check if name matches one specified specified in module yaml construct
            for module in modulelist:
                for k in module_key_dict:
                    if os.path.dirname(module.lower()) == k:
                        module_str += "module load " + os.path.dirname(module) + "\n"

        # if vars key is defined then get all environment variables
        if "vars" in test_dict:
            for k,v in test_dict['vars'].items():
                env_vars += get_environment_variable(self.shell,k,v)

        workdir = os.path.join(config_opts["BUILDTEST_TESTDIR"],"suite",self.test_suite,self.parent_dir)

        testscript_dict["vars"] = env_vars
        testscript_dict["module"] = module_str
        testscript_dict["workdir"] = "cd " + workdir + "\n"
        testscript_dict["command"] = cmd

        if "args" in test_dict:
            testscript_dict["run"] = "./" + exec_name + " " + test_dict["args"] + "\n"
        else:
            testscript_dict["run"] = "./" + exec_name + "\n"

        testscript_dict["post_run"] = "rm ./" + exec_name + "\n"

        return test_dict, testscript_dict

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
    if ext in ['.f90', '.f95', '.f03', '.f', '.F', '.F90', '.FPP', '.FOR', '.FTN', '.for', '.ftn']:
        return "fortran"
    if ext in ['.cu']:
        return "cuda"
    if ext in ['.py']:
        return "python"


def get_compiler_wrapper(filext, compiler_choice):
    """ get compiler wrapper """


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
        config_opts["BUILDTEST_OHPC"]=True

    sys.exit(0)
