############################################################################
#
#  Copyright 2017
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
Function that process the YAML config and verify key/value.
Also declares the valid YAML keys that can be used when writing YAML configs


:author: Shahzeb Siddiqui (Pfizer)
"""

import os
import sys
import yaml
import textwrap

field={
	'name':'',
	'source':'',
	'envvars':'',
	'args':'',
	'scheduler':['SLURM','LSF','PBS'],
	'buildopts':'',
	'buildcmd':'',
	'inputfile':'',
	'iter':'',
	'outputfile':'',
	'runcmd':'',
	'runextracmd':'',
	'mpi':'enabled',
	'cuda':'enabled',
	'nproc': '',
	'threadrange':'',
	'procrange':'',
	'jobslots':'',

}

yaml_keys = {
    'name': 'Name of the test script to be generated by buildtest. It must match the name of the yaml file.',

    'source': 'Name of the source file to compile or run.',

    'envvars': 'A list to declare environment variables inside the test script',

    'buildopts': 'build options passed to build command.',
    'buildcmd': 'A list of commands to be executed for building the program. Must include runcmd key for running the code. If test doesnt require anything to run, then declare runcmd with no value',
    'runcmd': 'A list of commands to be executed in order after the buildcmd. The buildcmd must be specified, if nothing to build set buildcmd key no value. Use this key to run the program',
    'runextracmd': 'Add extra commands after running code, only used when buildcmd and runcmd are not specified and additional instructions need to be specified',
    'inputfile': 'inputfile is used to change stdin to a file that is passed to executable',
    'outputfile': 'outputfile is used to change stdout to a file',
    'iter': 'Create N tests scripts from a particular YAML file',
    'mpi': 'enable mpi wrapper. Sets the compiler wrapper accordingly. value: [enabled]',
    'nproc': 'Argument to -np to indicate number of processes to use with mpirun',
    'cuda': 'enable cuda. Sets the compiler wrapper to nvcc. (Not implemented).    value: [enabled]',
    'binaries': 'list of binary command to execute in command.yaml',
    'threadrange': 'Specify range for OpenMP thread for buildtest to create a parameterized set of test scripts. Format: <start>,<end>,<interval>',
    'procrange': 'Specify range for MPI process (argument to -np) for buildtest to create a parameterized set of test scripts. Format: <start>,<end>, <interval>',
    'scheduler': 'Specify type of resource scheduler to create job script automatically. Valid options : [ LSF, SLURM ]',
    'jobslots': 'Specify total job slots to use in jobscript',
}


def show_yaml_keys():
    print ('{:>20}'.format("Key"), "\t \t ", '{:<20}'.format("Description"))
    print ('{:>20}'.format("--------------------------------------------------------------------------------"))
    for key in sorted(yaml_keys):
        print  ('{:>20}'.format(key), "\t \t ", '{:.<40}'.format(textwrap.fill(yaml_keys[key],120)))
    sys.exit(1)

def parse_config(filename,codedir):
    """
    read config file and verify the key-value content with dictionary field
    """
    fd=open(filename,'r')
    content=yaml.load(fd)
    # iterate over dictionary to seek any invalid keys
    for key in content:
        if key not in field:
            print ("ERROR: invalid key %s", key)
            sys.exit(1)
        # key-value name must match the yaml file name, but strip out .yaml extension for comparison
        if key == "name":
            strip_ext=os.path.splitext(filename)[0]
            # get name of file only for comparison with key value "name"
            testname=os.path.basename(strip_ext)
            if content[key] != testname:
                print ("Invalid value for key: %s : %s,  Value should be:", key, content[key], testname)
                sys.exit(1)
        if key == "mpi":
            if content[key] != "enabled":
                print("Error processing YAML file: %s", filename)
                print (""" "mpi" key must take value "enabled" """)
                sys.exit(1)
        # source must match a valid file name
        if key == "source" or key == "inputfile":
            codefile=os.path.join(codedir,content[key])
            if not os.path.exists(codefile):
                print ("Can't find source file: %s . Verify source file in directory: %s", codefile, codedir)
                sys.exit(1)
        # checking for invalid scheduler option
        if key == "scheduler":
            if content[key] not in field["scheduler"]:
                print ("Invalid scheduler option: %s. Please select on of the following:" , key,  field["scheduler"])
                sys.exit(1)
        if key == "nproc" or key == "iter" or key =="jobslots":
            # checking whether value of nproc and iter is integer
            if not str(content[key]).isdigit():
                print ("%s key must be an integer value",key)
                sys.exit(1)
                # checking whether key is negative or zero
            else:
                if int(content[key]) <= 0:
                    print ("%s must be greater than 0", key)
            sys.exit(1)
        if key == "procrange" or key == "threadrange":
            # format procrange: 2,10,3
            if len(content[key].split(",")) != 3:
                print ("Error processing YAML file: %s", filename)
                print ("Format expected: <start>,<end>,<interval> i.e 4,40,10")
                sys.exit(1)

            startproc = content[key].split(",")[0]
            endproc = content[key].split(",")[1]
            procinterval = content[key].split(",")[2]
            if not startproc.isdigit():
                print ("Error in %s expecting integer but found %s", filename, startproc)
                sys.exit(1)

            if not endproc.isdigit():
                print ("Error in %s expecting integer but found %s",  filename, endproc)
                sys.exit(1)

            if not procinterval.isdigit():
                print ("Error in %s  expecting integer but found %s", filename, procinterval)
                sys.exit(1)

    fd.close()
    return content
