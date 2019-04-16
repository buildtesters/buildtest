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
import stat
import subprocess

from buildtest.tools.config import config_opts
from buildtest.tools.file import create_dir
from buildtest.tools.yaml import BuildTestYamlSingleSource
from buildtest.tools.system import BuildTestCommand

class BuildTestBuilderSingleSource():
    """ Class responsible for building a single source test."""
    yaml_dict = {}
    test_dict = {}
    def __init__(self,yaml,args,parent_dir):
        """ Entry point to class. This method will set all class variables.

            :param yaml: The yaml file to be processed
            :param test_suite: Name of the test suite (buildtest build -S <suite>)
            :param parent_dir: parent directory where test script will be written
            :param software_module: Name of software module to write in test script.
        """
        self.shell = config_opts["BUILDTEST_SHELL"]
        self.yaml = yaml
        self.testname = '%s.%s' % (os.path.basename(self.yaml),self.shell)
        self.test_suite = args.suite
        self.parent_dir = parent_dir
        yaml_parser = BuildTestYamlSingleSource(self.yaml,args,self.shell)
        self.yaml_dict, self.test_dict = yaml_parser.parse()
        self.verbose = args.verbose
    def build(self):
        """Logic to build the test script.

        This class will invoke class BuildTestYamlSingleSource to return a
        dictionary that will contain all the information required to write
        the test script.

        This method will write the test script with one of the shell
        extensions (.bash, .csh, .sh) depending on what shell was requested.

        For a job script the shell extension .lsf or .slurm will be inserted.
        The test script will be set with 755 permission upon completion.
        """
        #print (self.yaml_dict)
        #if "variants" in self.yaml_dict:

        # if this is a LSF job script then create .lsf extension for testname
        if "lsf" in self.test_dict:
            self.testname = '%s.%s' % (os.path.basename(self.yaml),"lsf")
        # if this is a slurm job script then create .lsf extension for testname
        if "slurm" in self.test_dict:
            self.testname = '%s.%s' % (os.path.basename(self.yaml),"slurm")

        test_dir  = os.path.join(config_opts["BUILDTEST_TESTDIR"],
                                 "suite",
                                 self.test_suite,
                                 self.parent_dir)
        create_dir(test_dir)
        abs_test_path = os.path.join(test_dir, self.testname)

        self._write_test(abs_test_path)

    def _write_test(self,abs_test_path):

        print(f'Writing Test: {abs_test_path}')
        fd = open(abs_test_path, "w")

        # return the shell path i.e #!/bin/bash, #!/bin/sh
        shell_path = BuildTestCommand().which(self.shell)[0]

        fd.write(f'#!{shell_path}')

        if "lsf" in self.test_dict:
            fd.write(self.test_dict["lsf"])
        if "slurm" in self.test_dict:
            fd.write(self.test_dict["slurm"])

        fd.write(self.test_dict["module"])
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
            fd.write(self.test_dict["run"])
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
