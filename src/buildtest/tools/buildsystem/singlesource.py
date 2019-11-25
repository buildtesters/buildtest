"""
The file implements the singlesource build system responsible
"""

import logging
import os
import random
import stat
import subprocess
import yaml
import sys

from buildtest.tools.config import config_opts, BUILDTEST_BUILD_HISTORY, logID
from buildtest.tools.file import create_dir, is_file
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
                self.cxx = "g++"

            if self.language == "fortran":
                self.ftn = "gfortran"

        elif self.compiler == "intel":
            if self.language == "c":
                self.cc = "icc"

            if self.language == "c++":
                self.cxx = "icpc"

            if self.language == "fortran":
                self.ftn = "ifort"

        elif self.compiler == "pgi":
            if self.language == "c":
                self.cc = "pgcc"

            if self.language == "c++":
                self.cxx = "pgc++"

            if self.language == "fortran":
                self.ftn = "pgfortran"

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


    def __init__(self,file=None):
        """Class constructor for SingleSource"""

        bsub_schema = {
            'type': dict,
            'required': False,
            'description': "bsub block for specifying #BSUB directives in test.",

            'n': {
                'type': str,
                'required': False,
                'opt_mapping': "-n",
                'description': "Equivalent to #BSUB -n"
            },
            'M': {
                'type': str,
                'required': False,
                'opt_mapping': "-M",
                'description': "Equivalent to #BSUB -M"
            },
            'R': {
                'type': str,
                'required': False,
                'opt_mapping': "-R",
                'description': "Equivalent to #BSUB -R"
            },
            'q': {
                'type': str,
                'required': False,
                'opt_mapping': "-q",
                'description': "Equivalent to #BSUB -q"
            },
            'W': {
                'type': str,
                'required': False,
                'opt_mapping': "-W",
                'description': "Equivalent to #BSUB -W"
            }
        }
        sbatch_schema = {
            'type': dict,
            'required': False,
            'description': "sbatch block for specifying #SBATCH directives in test.",

            'n': {
                'type': str,
                'required': False,
                'opt_mapping': "-n",
                'description': "Equivalent to #SBATCH -n"
            },
            'N': {
                'type': str,
                'required': False,
                'opt_mapping': "-N",
                'description': "Equivalent to #SBATCH -N"
            },
            'mem': {
                'type': str,
                'required': False,
                'opt_mapping': "--mem",
                'description': "Equivalent to #SBATCH --mem"
            },
            'C': {
                'type': str,
                'required': False,
                'opt_mapping': "-C",
                'description': "Equivalent to #SBATCH -C"
            },
            'p': {
                'type': str,
                'required': False,
                'opt_mapping': "-p",
                'description': "Equivalent to #SBATCH -p"
            },
            't': {
                'type': str,
                'required': False,
                'opt_mapping': "-t",
                'description': "Equivalent to #SBATCH -t"
            }
        }
        mpi_schema = {
            'type': dict,
            'required': False,
            'description': "MPI block for specifying mpi configuration.",
            "flavor": {
                'type': str,
                'required': False,
                'values': ["openmpi", "mpich"],
                'description': "Specify MPI Flavor. This is used to detect MPI wrapper."
            },
            "launcher": {
                'type': str,
                'required': False,
                'values': ["mpirun", "mpiexec", "mpiexec.hydra"],
                'description': "Specify the MPI Launcher to run MPI jobs"
            },
            "launcher_opts": {
                'type': str,
                'required': False,
                'description': "Pass options to MPI Launcher"
            }
        }
        self.schema = {
            "testtype": {
                'type': str,
                'required': True,
                'values': "singlesource",
                'description': "Buildtest Class for Single Source Compilation"
            },
            "description": {
                'type': str,
                'required': True,
                'description': "Description Text for test configuration limited to 80 characters"
            },
            "maintainer": {
                'type': list,
                'required': True,
                'description': "List of Maintainers for the test"
            },
            "scheduler": {
                'type': str,
                'required': True,
                'values': ["local", "LSF", "SLURM"],
                'description': "Pick Scheduler Type."
            },
            "mpi": {
                'type': bool,
                'required': False,
                'values': [False, True],
                'description': "Instruct buildtest if this test is a MPI test"
            },
            "program": {
                'type': dict,
                'required': True,
                'description': "Start of Program. This section where you specify test parameters.",
                'source': {
                    'type': str,
                    'required': True,
                    'description': "Source File to compile. This file must be in 'src' directory"
                },
                'compiler': {
                    'type': str,
                    'required': True,
                    'values': ["gnu","intel","pgi","cuda"],
                    'description': "Specify Compiler Name to detect compiler wrapper."
                },
                'env': {
                    'type': dict,
                    'required': False,
                    'description': "Specify List of Environment Varaibles in Test"
                },
                'cflags': {
                    'type': str,
                    'required': False,
                    'description': "Specify compiler flags to C compiler (i.e $CC)"
                },
                'cxxflags': {
                    'type': str,
                    'required': False,
                    'description': "Specify compiler flags to C++ compiler (i.e $CXX)"
                },
                'fflags': {
                    'type': str,
                    'required': False,
                    'description': "Specify compiler flags to Fortran compiler (i.e $FC)"
                },
                'ldflags': {
                    'type': str,
                    'required': False,
                    'description': "Specify linker flags"
                },
                'pre_build': {
                    'type': str,
                    'required': False,
                    'description': "Shell commands to run before building."
                },
                'post_build': {
                    'type': str,
                    'required': False,
                    'description': "Shell commands to run after building."
                },
                'pre_run': {
                    'type': str,
                    'required': False,
                    'description': "Shell commands to run before running executable."
                },
                'post_run': {
                    'type': str,
                    'required': False,
                    'description': "Shell commands to run after running executable."
                },
                'pre_exec': {
                    'type': str,
                    'required': False,
                    'description': "Command in front of executable."
                },
                'exec_opts': {
                    'type': str,
                    'required': False,
                    'description': "Passing options to executable."
                },
                'post_exec': {
                    'type': str,
                    'required': False,
                    'description': "Commands after executable."
                },
                'bsub': bsub_schema,
                'sbatch': sbatch_schema,
                'mpi': mpi_schema
            }
        }
        if file is None:
            return

        logger = logging.getLogger(logID)

        fd = open(file,'r')
        self.test_yaml = yaml.safe_load(fd)
        fd.close()
        print(f"Loading Test Configuration (YAML) file: {file}")
        logger.info(f"Loading Test Configuration (YAML) file: {file}")
        print("Checking schema of YAML file")
        logger.info("Checking schema of YAML file")
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

        print ("Schema Check Passed")

        if "mpi" in self.test_yaml.keys():
            self.mpi= self.test_yaml['mpi']
        self.srcfile = os.path.join(self.srcdir, self.test_yaml["program"]["source"])
        self.execname = "%s.%s.exe" % (os.path.basename(file), hex(random.getrandbits(32)))
        # invoke setup method from base class to detect language, compiler, and mpi wrapper
        self.testscript_content["testpath"] = "%s.%s.sh" % (os.path.join(config_opts["BUILDTEST_TESTDIR"],os.path.basename(file)), hex(random.getrandbits(32)))

        logger.debug(f"Scheduler: {self.scheduler}")
        logger.debug(f"Parent Directory: {self.parent_dir}")
        logger.debug(f"Source Directory: {self.srcdir}")
        logger.debug(f"Source File: {self.srcfile}")



        print(f"Scheduler: {self.scheduler}")
        print(f"Parent Directory: {self.parent_dir}")
        print(f"Source Directory: {self.srcdir}")
        print(f"Source File: {self.srcfile}")

        print ("Detecting Programming Language, Compiler and MPI wrapper")
        super().__init__(self.srcfile,self.test_yaml["program"]["compiler"],self.mpi)
        print (f"Programming Language: {self.language}")

        self.buildcmd = self.build_command()

        if self.language == "c":
            print(f"CC: {self.cc}")
            print(f"CFLAGS: {self.cflags}")
        if self.language == "c++":
            print(f"CXX: {self.cxx}")
            print(f"CXXFLAGS: {self.cxxflags}")
        if self.language == "fortran":
            print(f"FC: {self.ftn}")
            print(f"FFLAGS: {self.fflags}")
        if self.language == "cuda":
            print(f"NVCC: {self.nvcc}")

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return self.schema

    def get_schema(self):
        """Return the yaml schema for singlesource class."""
        return self.schema

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

    def check_program_keys(self):
        """Check keys in dictionary program:"""
        # enable mpi key in program dictionary if self.mpi == yes
        if self.mpi:
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
            # skip keys of they are "type" or "required" or "description" these are metadata for program key
            if k in ["type","required","description"]:
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

            if k == "sbatch":
                self.check_sbatch_keys()

            if k == 'mpi':
                self.check_mpi_keys()

    def check_bsub_keys(self):
        """Checking bsub keys."""

        for k in self.schema['program']['bsub'].keys():
            if k in ["type", "required", "description"]:
                continue

            # if required key not found in test configuration then report error.
            if self.schema['program']['bsub'][k]['required'] and (k not in self.test_yaml['program']["bsub"].keys()):
                raise BuildTestError(f"Key: {k} is required in test configuration!")

            if (k in self.test_yaml['program']["bsub"].keys()):
                # check instance type of key in test configuration and match with one defined in self.schema.
                if not isinstance(self.test_yaml['program']['bsub'][k], self.schema['program']['bsub'][k]['type']):
                    raise BuildTestError(f"Error in Key: bsub:{k} --> Expecting of type: {self.schema['program']['bsub'][k]['type']} and received of type: {type(self.test_yaml['program']['bsub'][k])}")

    def check_sbatch_keys(self):
        """Checking bsub keys."""

        for k in self.schema['program']['sbatch'].keys():
            if k in ["type", "required", "description"]:
                continue

            # if required key not found in test configuration then report error.
            if self.schema['program']['sbatch'][k]['required'] and (k not in self.test_yaml['program']["sbatch"].keys()):
                raise BuildTestError(f"Key: {k} is required in test configuration!")

            if (k in self.test_yaml['program']["sbatch"].keys()):
                # check instance type of key in test configuration and match with one defined in self.schema.
                if not isinstance(self.test_yaml['program']['sbatch'][k], self.schema['program']['sbatch'][k]['type']):
                    raise BuildTestError(f"Error in Key: sbatch:{k} --> Expecting of type: {self.schema['program']['sbatch'][k]['type']} and received of type: {type(self.test_yaml['program']['sbatch'][k])}")

    def check_mpi_keys(self):
        """Check program:mpi keys."""

        for k in self.schema['program']['mpi'].keys():

            if k in ["type", "required", "description"]:
                continue
            # if required key not found in test configuration then report error.
            if self.schema['program']['mpi'][k]['required'] and k not in self.test_yaml['program']['mpi'].keys():
                raise BuildTestError(f"Key: {k} is required in test configuration!")

            # check instance type of key in test configuration and match with one defined in self.schema.
            if not isinstance(self.test_yaml['program']['mpi'][k], self.schema['program']['mpi'][k]['type']):
                raise BuildTestError(f"Expecting of type: {self.schema['program']['mpi'][k]['type']} and received of type: {type(self.test_yaml['program']['mpi'][k])}")

            # checking value of mpi flavor confirm with valid value in self.schema
            if k == "flavor" and self.test_yaml['program']['mpi']['flavor'] not in self.schema['program']['mpi']['flavor']['values']:
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
                buildcmd = ["$CC", "$CFLAGS", "-o", "$EXECUTABLE", "$SRCFILE" ]
            else:
                buildcmd = ["$CC", "-o", "$EXECUTABLE", "$SRCFILE"]

        elif self.language == "c++":
            # check if cflags is defined
            if "cxxflags" in self.test_yaml['program']:
                self.cxxflags = self.test_yaml['program']["cxxflags"]
                buildcmd = ["$CXX", "$CXXFLAGS", "-o", "$EXECUTABLE", "$SRCFILE"]
            else:
                buildcmd = ["$CXX", "-o", "$EXECUTABLE", "$SRCFILE"]

        elif self.language == "fortran":
            # check if cflags is defined
            if "fflags" in self.test_yaml['program']:
                self.fflags = self.test_yaml['program']["fflags"]
                buildcmd = ["$FC", "$FFLAGS", "-o", "$EXECUTABLE", "$SRCFILE"]
            else:
                buildcmd = ["$FC", "-o", "$EXECUTABLE", "$SRCFILE"]

        elif self.language == "cuda":
            # check if cflags is defined
            if "cflags" in self.test_yaml['program']:
                self.cflags = self.test_yaml['program']["cflags"]
                buildcmd = ["$CC", "$CFLAGS", "-o", "$EXECUTABLE", "$SRCFILE"]
            else:
                buildcmd = ["$CC", "-o", "$EXECUTABLE", "$SRCFILE"]

        if "ldflags" in self.test_yaml['program']:
            self.ldflags = self.test_yaml['program']["ldflags"]
            buildcmd.append("$LDFLAGS")

        return buildcmd
    def bsub_commands(self):
        """Convert bsub keys into #BSUB directives."""
        cmd = []
        for k,v in self.test_yaml['program']["bsub"].items():
            cmd.append(f"#BSUB {self.schema['program']['bsub'][k]['opt_mapping']} {v}")
        return cmd
    def sbatch_commands(self):
        """Convert sbatch keys into #SBATCH directives."""
        cmd = []
        for k,v in self.test_yaml['program']["sbatch"].items():
            cmd.append(f"#SBATCH {self.schema['program']['sbatch'][k]['opt_mapping']} {v}")
        return cmd
    def build_test_content(self):
        """This method brings all the components together to form the test structure."""

        logger = logging.getLogger(logID)

        if self.scheduler == "LSF":
            self.testscript_content["scheduler"] = self.bsub_commands()
        elif self.scheduler == "SLURM":
            self.testscript_content["scheduler"] = self.sbatch_commands()

        self.testscript_content["metavars"].append(f"TESTDIR={config_opts['BUILDTEST_TESTDIR']}")
        self.testscript_content["metavars"].append(f"SRCDIR={self.srcdir}")
        self.testscript_content["metavars"].append(f"SRCFILE={self.srcfile}")

        if self.cc:
            self.testscript_content["metavars"].append(f"CC={self.cc}")

        if self.nvcc:
            self.testscript_content["metavars"].append(f"CC={self.nvcc}")

        if self.ftn:
            self.testscript_content["metavars"].append(f"FC={self.ftn}")

        if self.cxx:
            self.testscript_content["metavars"].append(f"CXX={self.cxx}")

        if self.cflags:
            self.testscript_content["metavars"].append(f'CFLAGS="{self.cflags}"')

        if self.cxxflags:
            self.testscript_content["metavars"].append(f'CXXFLAGS="{self.cxxflags}"')

        if self.fflags:
            self.testscript_content["metavars"].append(f'FFLAGS="{self.fflags}"')
        if self.ldflags:
            self.testscript_content["metavars"].append(f'LDFLAGS="{self.ldflags}"')

        if self.execname:
            self.testscript_content["metavars"].append(f"EXECUTABLE={self.execname}")

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

        exec_cmd = []
        if "pre_exec" in self.test_yaml['program'].keys():
            exec_cmd.append(self.test_yaml['program']['pre_exec'])


        if self.mpi:
            exec_cmd.append(self.test_yaml['program']['mpi']['launcher'])
            exec_cmd.append(self.test_yaml['program']['mpi']['launcher_opts'])

        exec_cmd.append("$EXECUTABLE")

        if "exec_opts" in self.test_yaml['program'].keys():
            exec_cmd.append(self.test_yaml['program']['exec_opts'])

        if "post_exec" in self.test_yaml['program'].keys():
            exec_cmd.append(self.test_yaml['program']['post_exec'])


        self.testscript_content['run'].append(" ".join(exec_cmd))

        if "post_run" in self.test_yaml['program'].keys():
            self.testscript_content['run'].append(self.test_yaml['program']["post_run"])

        self.testscript_content['run'].append(f"rm ./$EXECUTABLE")
        for k,v in self.testscript_content.items():
            logger.debug(f"{k}:{v}")

        return self.testscript_content