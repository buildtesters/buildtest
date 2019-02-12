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
def get_all_yaml_files(root_dir=None):
    """ return a list of all yml files"""

    if root_dir == None:
        root_dir = os.path.join(config_opts['BUILDTEST_CONFIGS_REPO'],"buildtest/suite")


    yaml_list = []

    for root, dirs, files in os.walk(root_dir):
        for file in files:

            if file.endswith(".yml"):
                yaml_list.append(os.path.join(root,file))
    return yaml_list
class BuildTestYaml():


    yaml_file = ""
    def __init__(self,yaml_file,test_class,shell):
        if not os.path.exists(yaml_file):
            print("Invalid File Path: " + yaml_file)
            sys.exit(1)
        ext = os.path.splitext(yaml_file)[1]

        if ext != ".yml":
            print("Invalid File extension: " + ext)
            sys.exit(1)
        self.yaml_file=yaml_file
        self.lsf = False
        self.slurm = False
        self.vars = False
        self.test_class = test_class
        self.shell = shell
        self.parent_dir = os.path.basename(os.path.dirname(self.yaml_file))
        self.args = ""
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

            # check if compiler value is in list of supported compiler supported
            if k == "compiler":
                if v not in SUPPORTED_COMPILERS:
                    print (v + " is not a supported compiler:")
                    sys.exit(0)

            if k == "vars":
                self.vars = True
            if k == "lsf":
                self.lsf = True

            if k == "slurm":
                self.slurm = True

            if k == "mpi":
                mpi_keys = dict['mpi']

        if self.lsf:
            for k,v in dict['lsf'].items():
                if k not in TEMPLATE_JOB_LSF.keys():
                    print("Invalid Key: " + k)
                    sys.exit(1)


                if type(v) != type(TEMPLATE_JOB_LSF[k]):
                    print("Type mismatch for key: " + k  + " Got Type: " + str(type(v)) + " Expecting Type:" + str(type(TEMPLATE_JOB_LSF[k])))
                    sys.exit(1)

        if self.slurm:
            for k,v in  dict['slurm'].items():
                if k not in TEMPLATE_JOB_SLURM.keys():
                    print("Invalid Key: " + k)
                    sys.exit(1)

                if type(v) != type(TEMPLATE_JOB_SLURM[k]):
                    print("Type mismatch for key: " + k  + " Got Type: " + str(type(v)) + " Expecting Type:" + str(type(TEMPLATE_JOB_SLURM[k])))
                    sys.exit(1)


    def parse(self):
        """ parse a yaml file to determine if content follows buildtest yaml schema"""
        fd=open(self.yaml_file,'r')
        content=yaml.load(fd)
        test_dict = content['test']
        self._check_keys(test_dict)

        flags = ""
        testscript_dict = {}

        if self.lsf:
            testscript_dict["lsf"] = lsf_key_parse(test_dict['lsf'])
        if self.slurm:
            testscript_dict["slurm"] = slurm_key_parse(test_dict['slurm'])

        module_key_dict = test_dict['module']
        srcfile = test_dict['source']

        if "flags" in test_dict:
            flags = test_dict['flags']

        if "args" in test_dict:
            self.args = test_dict["args"]

        compiler = test_dict['compiler']
        ldflags = ""
        if "ldflags" in test_dict:
            ldflags = test_dict['ldflags']
        exec_name = '%s.exe' % srcfile
        class_dir = os.path.join(config_opts["BUILDTEST_CONFIGS_REPO"],"buildtest","suite")
        updated_srcfile = os.path.join(class_dir, self.test_class, self.parent_dir,"src",test_dict["source"])
        test_dict['source'] = updated_srcfile
        ext = os.path.splitext(test_dict['source'])[1]

        language = get_programming_language(ext)
        cmd = []

        if language == "c":
            cc = get_compiler(language,compiler)
            cmd += [cc,flags,'-o',exec_name,updated_srcfile, ldflags]
        if language == "c++":
            cxx = get_compiler(language,compiler)
            cmd += [cxx,flags,'-o',exec_name,updated_srcfile, ldflags]
        if language == "fortran":
            fc = get_compiler(language,compiler)
            cmd += [fc,flags,'-o',exec_name,updated_srcfile, ldflags]
        if language == "cuda":
            nvcc = get_compiler(language,compiler)
            cmd += [nvcc,flags,'-o',exec_name,updated_srcfile, ldflags]

        modulelist = get_software_stack()
        module_str = "module purge \n"
        # go through all modules in software stack and check if name matches one specified specified in module yaml construct
        for module in modulelist:
            for k in module_key_dict:
                if os.path.dirname(module.lower()) == k:
                    module_str += "module load " + os.path.dirname(module) + "\n"

        env_vars = ""
        # if vars key is defined then get all environment variables
        if self.vars:
            for k,v in test_dict['vars'].items():
                env_vars += get_environment_variable(self.shell,k,v)

        workdir = os.path.join(config_opts["BUILDTEST_TESTDIR"],"suite",self.test_class,self.parent_dir)

        testscript_dict["vars"] = env_vars
        testscript_dict["module"] = module_str
        testscript_dict["workdir"] = "cd " + workdir + "\n"
        testscript_dict["command"] = cmd
        testscript_dict["run"] = "./" + exec_name + " " + self.args + "\n"
        testscript_dict["post_run"] = "rm ./" + exec_name + "\n"

        #print (testscript_dict)
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
