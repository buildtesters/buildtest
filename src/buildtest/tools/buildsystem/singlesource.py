############################################################################
#
#  Copyright 2017-2019
#
#  https://github.com/HPC-buildtest/buildtest-framework
#
#  This file is part of buildtest.
#
#  buildtest is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  buildtest is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with buildtest.  If not, see <http://www.gnu.org/licenses/>.
#############################################################################

"""
The file implements the singlesource build system responsible
"""

import os
import random
import stat
import subprocess
import yaml
import sys

from buildtest.tools.config import config_opts, BUILDTEST_BUILD_HISTORY
from buildtest.tools.file import create_dir, is_file
from buildtest.tools.mpi import openmpi_opt_table, mpich_opt_table
from buildtest.tools.yaml import TEMPLATE_SINGLESOURCE, SUPPORTED_COMPILERS, \
    SUPPORTED_MPI_WRAPPERS, SUPPORTED_MPI_LAUNCHERS, SUPPORTED_MPI_FLAVORS, \
    TEMPLATE_JOB_LSF, TEMPLATE_JOB_SLURM, \
    get_programming_language, get_compiler, lsf_key_parse, slurm_key_parse, \
    get_environment_variable, get_mpi_wrapper
from buildtest.tools.system import BuildTestCommand, BuildTestSystem
from buildtest.tools.log import BuildTestError




class BuildTestBuilder():
    """Class responsible for parsing the test configuration."""


    def __init__(self, file, compiler, mpi=False):
        """Class constructor for BuildTestBuilder"""

        self.ext = os.path.splitext(file)[1]
        self.compiler = compiler
        self.mpi = mpi
        self.cc = None
        self.cxx = None
        self.ftn = None
        self.nvcc = None
        self.cflags = None
        self.cxxflags = None
        self.cppflags = None
        self.fflags = None
        self.ldflags = None
        self.language = None

        self._detect_language()
        self._detect_compiler()
        if self.mpi:
            self._detect_mpi()

    def get_cc(self):
        """Return cc variable"""

        return self.cc

    def get_cxx(self):
        """Return cxx variable"""
        return self.cxx

    def get_ftn(self):
        """Return ftn variable"""
        return self.ftn

    def get_nvcc(self):
        """Return cc variable"""
        return self.nvcc

    def get_cflags(self):
        """Return cflags variable"""
        return self.cflags

    def get_fflags(self):
        """Return fflags variable"""
        return self.fflags

    def get_ldflags(self):
        """Return fflags variable"""
        return self.ldflags

    def get_language(self):
        """Return language variable."""
        return self.language

    def _detect_language(self):
        """ Return Programming Language  based on extension

        :param ext: File extension of source file
        :type ext: str, required
        :return: return programming language
        :rtype: str
        """

        if self.ext in ['.c']:
            self.language = "c"

        if self.ext in ['.cc', '.cxx', '.cpp', '.c++', '.C']:
            self.language = "c++"

        if self.ext in ['.f90', '.f95', '.f03', '.f', '.F', '.F90', '.FPP', '.FOR',
                   '.FTN', '.for', '.ftn']:
            self.language = "fortran"

        if self.ext in ['.cu']:
            self.language =  "cuda"

    def _detect_compiler(self):
        """Detect compiler based on language

        :param language: Language type
        :type language: str, required
        :param compiler: Compiler Type
        :type compiler: str, required
        :return: return compiler wrapper
        :rtype: str
        """
        if self.compiler == "gnu":
            if self.language == "c":
                self.cc = "gcc"

            if self.language == "c++":
                self.cxx = "gxx"

            if self.language == "fortran":
                self.ftn = "gfortran"

        elif self.compiler == "intel":
            if self.language == "c":
                self.cc = "icc"

            if self.language == "c++":
                self.cxx = "icpc"

            if self.language == "fortran":
                self.ftn = "ifort"

        elif self.compiler == "cuda":
            self.nvcc = "nvcc"

    def _detect_mpi(self):
        """Detect MPI wrapper based on Language and compiler.

        :param language: Language type
        :type language: str, required
        :param compiler: Compiler Type
        :type compiler: str, required

        :return: return compiler wrapper
        :rtype: str
        """
        if self.language == "c" and self.compiler == "gnu":
            self.cc = "mpicc"

        if self.language == "c++" and self.compiler == "gnu":
            self.cxx = "mpicxx"
        if self.language == "fortran" and self.compiler == "gnu":
            self.ftn = "mpifort"

        if self.language == "c" and self.compiler == "intel":
            self.cc = "mpiicc"
        if self.language == "c++" and self.compiler == "intel":
            self.cxx = "mpiicpc"
        if self.language == "fortran" and self.compiler == "intel":
            self.ftn = "mpiifort"

class SingleSource(BuildTestBuilder):


    def __init__(self,file):
        """Class constructor for SingleSource"""

        bsub_schema = {
            'type': dict,
            'required': False,
            'n': {'type': str, 'required': False},
            'M': {'type': str, 'required': False},
            'R': {'type': str, 'required': False},
            'q': {'type': str, 'required': False},
            'W': {'type': str, 'required': False}
        }
        mpi_schema = {
            'type': dict,
            'required': False,
            "flavor": {'type': str, 'required': False, 'values': ["openmpi", "mpich"]},
            "launcher": {'type': str, 'required': False, 'values': ["mpirun", "mpiexec", "mpiexec.hydra"]},
        }
        self.schema = {
            "testtype": {'type': str, 'required': True, 'values': "singlesource"},
            "description": {'type': str, 'required': True},
            "maintainer": {'type': list, 'required': True},
            "scheduler": {'type': str, 'required': True, 'values': ["local", "LSF", "SLURM"]},
            "mpi": {'type': bool, 'required': False, 'values': [False, True]},
            "program": {
                'type': dict,
                'required': True,
                'source': {'type': str, 'required': True},
                'compiler': {'type': str, 'required': True, 'values': ["gnu"]},
                'env': {'type': dict, 'required': False},
                'cflags': {'type': str, 'required': False},
                'cxxflags': {'type': str, 'required': False},
                'fflags': {'type': str, 'required': False},
                'ldflags': {'type': str, 'required': False},
                'pre_build': {'type': str, 'required': False},
                'post_build': {'type': str, 'required': False},
                'pre_run': {'type': str, 'required': False},
                'post_run': {'type': str, 'required': False},
                'exec_opts': {'type': str, 'required': False},
                'bsub': bsub_schema,
                'mpi': mpi_schema
            }
        }
        fd = open(file,'r')
        self.test_yaml = yaml.safe_load(fd)
        fd.close()

        self.check_top_keys()

        # self.scheduler is used to determine if scheduler check needs to be performed.
        self.scheduler = self.test_yaml["scheduler"]
        # self.mpi used to enable/disable mpi check
        self.mpi = False
        self.parent_dir = os.path.dirname(file)
        self.srcdir = os.path.join(self.parent_dir,"src")

        # content to store the test script
        self.testscript_content = {
            "testpath": "",
            "scheduler":[],
            "module":[],
            "metavars": [],
            "envs": [],
            "build": [],
            "run": []
        }
        
        self.envs = []

        self.check_program_keys()

        self.srcfile = os.path.join(self.srcdir, self.test_yaml["program"]["source"])
        self.execname = "%s.%s.exe" % (os.path.basename(file), hex(random.getrandbits(32)))
        # invoke setup method from base class to detect language, compiler, and mpi wrapper
        self.testscript_content["testpath"] = "%s.%s.sh" % (os.path.join(config_opts["BUILDTEST_TESTDIR"],os.path.basename(file)), hex(random.getrandbits(32)))

        super().__init__(self.srcfile,self.test_yaml["program"]["compiler"])
        
        
        self.buildcmd = self.build_command()


    def check_top_keys(self):
        """Check Top Level Keys in self.schema dictionary"""
        for k in self.schema.keys():
            #print (self.schema[k]['required'],k,test_keys.keys(),k not in test_keys.keys())
            #print (self.schema[k]['required'], k not in test_keys.keys())

            # if required key not found in test configuration then report error.
            if self.schema[k]['required'] and (k not in self.test_yaml.keys()):
                raise BuildTestError(f"Key: {k} is required in test configuration!")

            # check instance type of key in test configuration and match with one defined in self.schema.
            if k in self.test_yaml.keys() and not isinstance(self.test_yaml[k],self.schema[k]['type']):
                raise BuildTestError(f"Expecting of type: {self.schema[k]['type']} and received of type: {type(self.test_yaml[k])}")

            # value of key must be testtype: singlesource
            if k == "testtype" and self.test_yaml['testtype'] != self.schema['testtype']['values']:
                raise BuildTestError(f"Key must be testtype: singlesource. Received {k}:{self.test_yaml['testtype']}")

            # description text can't be more than 80 chars
            if k == "description" and len(self.test_yaml["description"]) > 80:
                raise BuildTestError("Description can't be more than 80 characters."
                                     f"Length: {len(self.test_yaml['description'])} " 
                                     f"{k}:{self.test_yaml['description']}")

            # check scheduler value types
            if k == 'scheduler' and self.test_yaml['scheduler'] not in self.schema['scheduler']['values']:
                raise BuildTestError(f"{self.test_yaml['scheduler']} is not valid value. Must be one of the following: {self.schema['scheduler']['values']}")

            # first check if "mpi" key is in test configuration because it is not a required key
            if k == 'mpi' and 'mpi' in self.test_yaml:
                # if found, then check value type. By default, if it is not found, mpi will be disabled
                if self.test_yaml['mpi'] not in self.schema['mpi']['values']:
                    raise BuildTestError(f"{self.test_yaml['mpi']} is not valid value. Must be one of the following: {self.schema['mpi']['values']}")

                self.mpi = self.test_yaml['mpi']

    def check_program_keys(self):
        """Check keys in dictionary program:"""
        # enable mpi key in program dictionary if self.mpi == yes
        if self.mpi == "yes":
            self.schema['program']['mpi']["required"] = True
            self.schema['program']['mpi']["flavor"]["required"] = True
            self.schema['program']['mpi']["launcher"]["required"] = True
        # enable bsub key if scheduler is set to LSF
        if self.scheduler == "LSF":
            self.schema['program']["bsub"]["required"] = True

        # type check for top level program key
        if not isinstance(self.test_yaml['program'], self.schema['program']['type']):
            raise BuildTestError(f"Expecting of type: {self.schema['program']['type']} for program key. Received of type: {self.test_yaml['program']}")

        for k in self.schema['program'].keys():
            # skip keys of they are "type" or "required" these are metadata for program key
            if k == "type" or k == "required":
                continue
            # if required key not found in test configuration then report error.
            if self.schema['program'][k]['required'] and (k not in self.test_yaml['program'].keys()):
                raise BuildTestError(f'Key: {k} is required in test configuration!')

            # skip to next key if not found in test configuration.
            if k not in self.test_yaml['program'].keys():
                continue
            # check instance type of key in test configuration and match with one defined in self.schema.
            if not isinstance(self.test_yaml['program'][k], self.schema['program'][k]['type']):
                raise BuildTestError(f"Expecting of type: {self.schema['program'][k]['type']} and received of type: {type(self.test_yaml['program'][k])}")

            if k == "compiler":
                if self.test_yaml['program'][k] not in self.schema['program'][k]['values']:
                    raise BuildTestError(f"Expecting value for {k}: {self.schema['program'][k]['values']} and received value: {self.test_yaml['program'][k]}")

            if k == "bsub":
                self.check_bsub_keys()

            if k == 'mpi':
                self.check_mpi_keys()

    def check_bsub_keys(self):
        """Checking bsub keys."""

        for k in self.schema['program']['bsub'].keys():
            if k == "type" or k == "required":
                continue

            # if required key not found in test configuration then report error.
            if self.schema['program']['bsub'][k]['required'] and (k not in self.test_yaml['program']["bsub"].keys()):
                raise BuildTestError(f"Key: {k} is required in test configuration!")

            # check instance type of key in test configuration and match with one defined in self.schema.
            if not isinstance(self.test_yaml['program']['bsub'][k], self.schema['program']['bsub'][k]['type']):
                raise BuildTestError(f"Error in Key: bsub:{k} --> Expecting of type: {self.schema['program']['bsub'][k]['type']} and received of type: {type(self.test_yaml['program']['bsub'][k])}")

    def check_mpi_keys(self):
        """Check program:mpi keys."""
        for k in self.schema['program']['mpi'].keys():
            # if required key not found in test configuration then report error.
            if self.schema['program']['mpi'][k]['required'] and k not in self.test_yaml['program']['mpi'].keys():
                raise BuildTestError(f"Key: {k} is required in test configuration!")

            # check instance type of key in test configuration and match with one defined in self.schema.
            if not isinstance(self.test_yaml['program']['mpi'][k], self.schema['program']['mpi'][k]['type']):
                raise BuildTestError(f"Expecting of type: {self.schema['program']['mpi'][k]['type']} and received of type: {type(self.test_yaml['program']['mpi'][k])}")

            # checking value of mpi flavor confirm with valid value in self.schema
            if k == "flavor" and self.test_yaml['program']['mpi']['flavor'] not in self.schema['program']['mpi']["flavor"]['values']:
                raise BuildTestError(f"{self.test_yaml['program']['mpi']['flavor']} is not valid value. Must be one of the following: {self.schema['program']['mpi']['flavor']['values']}")

            # checking value of mpi flavor confirm with valid value in self.schema
            if k == "launcher" and self.test_yaml['program']['mpi']["launcher"] not in self.schema['program']['mpi']["launcher"]['values']:
                raise BuildTestError(f"{self.test_yaml['program']['mpi']['launcher']} is not valid value. Must be one of the following: {self.schema['program']['mpi']['launcher']['values']}")

    def build_command(self):
        """Generate the compilation command based on language and compiler. """

        if "env" in self.test_yaml['program']:
            for k,v in self.test_yaml['program']['env'].items():
                self.envs.append(["export", f'{k}={v}'])

        buildcmd = []

        if self.language == "c":
            # check if cflags is defined
            if "cflags" in self.test_yaml['program']:
                self.cflags = self.test_yaml['program']["cflags"]
                buildcmd = [self.cc, "$CFLAGS", "-o", self.execname, "$SRCFILE" ]
            else:
                buildcmd = [self.cc, "-o", self.execname, "$SRCFILE"]

        elif self.language == "c++":
            # check if cflags is defined
            if "cxxflags" in self.test_yaml['program']:
                self.cxxflags = self.test_yaml['program']["cxxflags"]
                buildcmd = [self.cxx, "$CXXFLAGS", "-o", self.execname, "$SRCFILE"]
            else:
                buildcmd = [self.cxx, "-o", self.execname, "$SRCFILE"]

        elif self.language == "fortran":
            # check if cflags is defined
            if "fflags" in self.test_yaml['program']:
                self.fflags = self.test_yaml['program']["fflags"]
                buildcmd = [self.ftn, "$FFLAGS", "-o", self.execname, "$SRCFILE"]
            else:
                buildcmd = [self.ftn, "-o", self.execname, "$SRCFILE"]

        elif self.language == "cuda":
            # check if cflags is defined
            if "cflags" in self.test_yaml['program']:
                self.cflags = self.test_yaml['program']["cflags"]
                buildcmd = [self.nvcc, "$CFLAGS", "-o", self.execname, "$SRCFILE"]
            else:
                buildcmd = [self.nvcc, "-o", self.execname, "$SRCFILE"]

        if "ldflags" in self.test_yaml['program']:
            self.ldflags = self.test_yaml['program']["ldflags"]
            buildcmd.append(self.ldflags)

        return buildcmd
    def bsub_commands(self):
        """Convert bsub keys into #BSUB directives."""
        cmd = []
        for k,v in self.test_yaml['program']["bsub"].items():
            cmd.append(f"#BSUB -{k} {v}")
        return cmd
    def build_test_content(self):
        """This method brings all the components together to form the test structure."""


        if self.scheduler == "LSF":
            self.testscript_content["scheduler"] = self.bsub_commands()

        self.testscript_content["metavars"].append(f"TESTDIR={config_opts['BUILDTEST_TESTDIR']}")
        self.testscript_content["metavars"].append(f"SRCDIR={self.srcdir}")
        self.testscript_content["metavars"].append(f"SRCFILE={self.srcfile}")

        if self.cflags:
            self.testscript_content["metavars"].append(f'CFLAGS="{self.cflags}"')

        if self.cxxflags:
            self.testscript_content["metavars"].append(f'CXXFLAGS="{self.cxxflags}"')

        if self.fflags:
            self.testscript_content["metavars"].append(f'FFLAGS="{self.fflags}"')

        # adding environment variables
        for k in self.envs:
            self.testscript_content["envs"].append(" ".join(k))

        self.testscript_content["build"].append("cd $TESTDIR")

        if "pre_build" in self.test_yaml['program'].keys():
            self.testscript_content["build"].append(self.test_yaml['program']['pre_build'])

        self.testscript_content['build'].append(" ".join(self.buildcmd))

        if "post_build" in self.test_yaml['program'].keys():
            self.testscript_content['build'].append(self.test_yaml['program']['post_build'])

        if "pre_run" in self.test_yaml['program'].keys():
            self.testscript_content['run'].append(self.test_yaml['program']["pre_run"])

        if "exec_opts" in self.test_yaml['program'].keys():
            self.testscript_content['run'].append(self.execname + " " + self.test_yaml['program']["exec_opts"])

        if "pre_run" in self.test_yaml['program'].keys():
            self.testscript_content['run'].append(self.test_yaml['program']["post_run"])


        return self.testscript_content

class BuildTestBuilderSingleSource():
    """ Class responsible for building a single source test."""
    yaml_dict = {}
    test_dict = {}
    def __init__(self, yaml, args, module_cmd_list,build_id):
        """ Entry point to class. This method will set all class variables.

            :param yaml: The yaml file to be processed
            :param args: Command line argument passed to buildtest
            :param module_cmd_list: Name of software module to write in test script.
            :param build_id: build id to identify build
        """
        self.build_id = build_id
        self.module_collection = None
        self.internal_module_collection = None
        self.shell = config_opts["BUILDTEST_SHELL"]
        self.conf_file = yaml
        self.testname = '%s.%s' % (os.path.basename(self.conf_file),self.shell)


        self.srcdir = os.path.join(os.path.dirname(self.conf_file),"src")
        self.verbose = args.verbose

        self.yaml_dict, self.test_dict = self._parse()
        self.module_cmd_list = module_cmd_list

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
    def _check_mpi(self,mpi_wrapper):
        if mpi_wrapper not in SUPPORTED_MPI_WRAPPERS:
            print (f"{mpi_wrapper} is not supported mpi wrapper")
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

    def _parse(self):
        """ Parse yaml file to determine if content follows the defined yaml
        schema."""

        testscript_dict = {}

        fd=open(self.conf_file,'r')
        test_dict=yaml.safe_load(fd)

        if self.verbose >= 2:
            print ("{:_<80}".format(""))
            print (yaml.dump(test_dict,default_flow_style=False))
            print ("{:_<80}".format(""))

        self._check_keys(test_dict)
        if self.verbose >= 1:
            print (f"Key Check PASSED for file {self.conf_file}")

        srcfile = os.path.join(self.srcdir,test_dict['source'])
        is_file(srcfile)

        if self.verbose >= 2:
            print (f"Source File {srcfile} exists!")
        ext = os.path.splitext(srcfile)[1]
        language = get_programming_language(ext)
        if self.verbose >= 1:
            print (f"Programming Language Detected: {language}")

        hash = hex(random.getrandbits(128))

        exec_name = '%s.exe' % hash
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

            if "mpi" in test_dict:
                # detecting the mpi wrapper based on compiler
                mpi_wrapper = get_mpi_wrapper(language,test_dict['compiler'])
                cmd.append(mpi_wrapper)
            else:
                cmd.append(compiler_name)

            if "flags" in test_dict:
                cmd.append(test_dict['flags'])

            cmd += ['-o',exec_name,srcfile]

            if "ldflags" in test_dict:
                cmd.append(test_dict['ldflags'])


        if "input" in test_dict:
            cmd += ["<", os.path.join(self.srcdir,inputfile)]



        # env_list used for storing environment variables
        env_list = []
        # if vars key is defined then get all environment variables
        if "vars" in test_dict:
            for k,v in test_dict['vars'].items():
                if self.verbose >= 1:
                    print (f"Detecting environment {k}={v}")

                env_vars = get_environment_variable(self.shell,k,v)
                # add each environment key=value into list
                env_list.append(env_vars)



        if len(env_list) > 0:
            testscript_dict["vars"] = '\n'.join(env_list) + "\n"

        testscript_dict["workdir"] = "cd " + config_opts["BUILDTEST_TESTDIR"]  + "\n"
        testscript_dict["command"] = cmd
        testscript_dict["run"] = []
        # build the run command for mpi jobs
        if "mpi" in test_dict.keys():
            # if launcher is specified in configuration check if it is valid
            #  and add it directly as part of run command
            if "srun" in test_dict["mpi"].keys():
                testscript_dict["run"].append("srun")
            # add openmpi yaml keys to build command orterun command
            elif "openmpi" in test_dict["mpi"].keys():

                testscript_dict["run"].append("orterun")
                mpirun_opts = test_dict["mpi"]["openmpi"].keys()
                mpirun_flags = openmpi_opt_table(mpirun_opts)
                for flag,opts in zip(mpirun_flags,mpirun_opts):
                    testscript_dict["run"].append(flag)
                    testscript_dict["run"].append(test_dict["mpi"]["openmpi"][opts])
            # add mpich yaml keys to build command mpiexec.hydra
            elif "mpich" in test_dict["mpi"].keys():
                testscript_dict["run"].append("mpiexec.hydra")
                mpirun_keys = test_dict["mpi"]["mpich"].keys()
                mpirun_flags = mpich_opt_table(mpirun_keys)
                for flag, opts in zip(mpirun_flags, mpirun_keys):
                    testscript_dict["run"].append(flag)
                    testscript_dict["run"].append(
                        test_dict["mpi"]["mpich"][opts])

            testscript_dict["run"].append(f"./{exec_name}")

        else:
            testscript_dict["run"].append(f"./{exec_name}")

        if "args" in test_dict:
            testscript_dict["run"].append(test_dict['args'])

        testscript_dict["run"].append("\n")

        testscript_dict["post_run"] = f"rm ./{exec_name} \n"

        return test_dict, testscript_dict
    def build(self,modules_permutation=False,module_collection=False,
              internal_module_collection=False):
        """This method builds the test script.

        This method will write the test script with one of the shell
        extensions (.bash, .csh, .sh) depending on what shell was requested.

        For a job script the shell extension .lsf or .slurm will be inserted.
        The test script will be set with 755 permission upon completion.
        """


        if module_collection:
            self.module_collection = module_collection
        if internal_module_collection:
            self.internal_module_collection = internal_module_collection
        # write test for every module permutation
        if modules_permutation:
            count = 0
            for cmd in self.module_cmd_list:

                hash = hex(random.getrandbits(128))
                file = '%s_%s.%s' % (os.path.basename(self.conf_file), hash,
                                     self.shell)
                # if this is a LSF job script then create .lsf extension for testname
                if "lsf" in self.test_dict:
                    file = '%s_%s.%s' % (os.path.basename(self.conf_file),
                                         hash,
                                         "lsf")
                if "slurm" in self.test_dict:
                    file ='%s_%s.%s' % (os.path.basename(self.conf_file),
                                        hash,
                                        "slurm")


                abs_test_path = os.path.join(config_opts["BUILDTEST_TESTDIR"], file)

                self._write_test(abs_test_path,module=cmd)
                count+=1
                BUILDTEST_BUILD_HISTORY[self.build_id]["TESTS"].append(abs_test_path)
            print(f"Writing {count} tests for {self.conf_file}")



            return
        # if this is a LSF job script then create .lsf extension for testname
        if "lsf" in self.test_dict:
            self.testname = '%s.%s' % (os.path.basename(self.conf_file),"lsf")
        # if this is a slurm job script then create .lsf extension for testname
        if "slurm" in self.test_dict:
            self.testname = '%s.%s' % (os.path.basename(self.conf_file),"slurm")


        abs_test_path = os.path.join(config_opts["BUILDTEST_TESTDIR"], self.testname)
        self._write_test(abs_test_path)

        BUILDTEST_BUILD_HISTORY[self.build_id]["TESTS"].append(abs_test_path)

    def _write_test(self,abs_test_path,module=None):

        print(f'Writing Test: {abs_test_path}')
        fd = open(abs_test_path, "w")

        # return the shell path i.e #!/bin/bash, #!/bin/sh
        shell_path = BuildTestCommand().which(self.shell)[0]

        fd.write(f'#!{shell_path}')

        if "lsf" in self.test_dict:
            fd.write(self.test_dict["lsf"])
        if "slurm" in self.test_dict:
            fd.write(self.test_dict["slurm"])

        # write purge modules before loading any modules to avoid issues with
        # active modules in user environment

        if config_opts["BUILDTEST_MODULE_FORCE_PURGE"]:
            fd.write("module --force purge \n")
        else:
            fd.write("module purge \n")

        if module != None:
            fd.write(module)
            fd.write("\n")
        elif self.module_collection is not None:
            fd.write(f"module restore {self.module_collection}")
            fd.write("\n")
        elif self.internal_module_collection:
            fd.write(f"{self.internal_module_collection}")
            fd.write("\n")
        else:
            cmd = "module -t list"
            out = subprocess.getoutput(cmd)
            # output of module -t list when no modules are loaded is "No modules
            #  loaded"
            if out != "No modules loaded":
                out = out.split()
                # module load each module
                for i in out:
                    fd.write(f"module load {i} \n")


        if "vars" in self.test_dict:
            fd.write(self.test_dict["vars"])

        fd.write(self.test_dict["workdir"])
        [ fd.write(k + " ") for k in self.test_dict["command"] ]
        fd.write("\n")

        if "run" in self.test_dict:
            [fd.write(k + " ") for k in self.test_dict["run"]]
            fd.write(self.test_dict["post_run"])

        fd.close()
        # setting perm to 755 on testscript
        os.chmod(abs_test_path, stat.S_IRWXU |
                                stat.S_IRGRP |
                                stat.S_IXGRP |
                                stat.S_IROTH |
                                stat.S_IXOTH)

        if self.verbose >= 1:
            print (f"Changing permission to 755 for test: {abs_test_path}")

        if self.verbose >= 2:
            test_output = subprocess.getoutput(f"cat {abs_test_path}").splitlines()
            print ("{:_<80}".format(""))
            for line in test_output:
                print (line)
            print ("{:_<80}".format(""))
