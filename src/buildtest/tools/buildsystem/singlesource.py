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

class BuildTestBuilderSingleSource():
    """ Class responsible for building a single source test."""
    yaml_dict = {}
    test_dict = {}
    def __init__(self, yaml, args, parent_dir,module_cmd_list,build_id):
        """ Entry point to class. This method will set all class variables.

            :param yaml: The yaml file to be processed
            :param args: Command line argument passed to buildtest
            :param parent_dir: parent directory where test script will be written
            :param module_cmd_list: Name of software module to write in test script.
            :param build_id: build id to identify build
        """
        self.build_id = build_id
        self.module_collection = None
        self.internal_module_collection = None
        self.shell = config_opts["BUILDTEST_SHELL"]
        self.conf_file = yaml
        self.testname = '%s.%s' % (os.path.basename(self.conf_file),self.shell)
        self.test_suite = args.suite
        self.parent_dir = parent_dir

        self.test_suite_dir = os.path.join(
            config_opts["BUILDTEST_CONFIGS_REPO"],
            "buildtest",
            "suite")
        self.srcdir = os.path.join(self.test_suite_dir,
                                   self.test_suite,
                                   self.parent_dir,
                                   "src")
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
        #exec_name = '%s.exe' % test_dict['source']
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
            print(f"Writing {count} tests for {self.conf_file}")

            BUILDTEST_BUILD_HISTORY[self.build_id]["TESTS"].append(abs_test_path)

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
