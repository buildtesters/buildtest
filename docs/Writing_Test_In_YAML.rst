.. _Writing_Test_In_YAML:


Writing Test in YAML
====================

.. contents::
   :backlinks: none



Writing test in YAML is easy. YAML test are processed by buildtest using the 
yaml library into a dictionary which is then processed to generate the test-script.
The buildtest will parse the YAML config and generate the build and run command line
based on the key/values provided.  


YAML Key Description
--------------------

.. include:: Writing_Test_In_YAML/yaml_table.txt

The binary test configs are stored in a file **command.yaml** which contains a 
list of executables along with any arguments. Buildtest will create a separate 
test-script for each executable. The keyword **binaries** is only specified to
command.yaml file. The binary test are specific to the software packge to test. 
Figure out the binaries in the install path for the software, typically in 
**bin** directory and add this to the command.yaml file.

**GCC BinaryTest YAML Example** 

.. program-output:: cat scripts/Writing_Test_In_YAML/command.yaml


**GCC-5.4.0-2.27 buildtest Test Script**

.. program-output:: cat scripts/Writing_Test_In_YAML/gcc.sh

**BuildTest YAML Hello World Example**

.. program-output:: cat scripts/Writing_Test_In_YAML/hello.c.yaml

**BuildTest Hello World Test Script** 

.. program-output:: cat scripts/Writing_Test_In_YAML/hello.c.sh


**inputfile Example**

.. program-output:: cat scripts/Writing_Test_In_YAML/inputfile.yaml

.. program-output:: cat scripts/Writing_Test_In_YAML/inputfile.sh


**outputfile Example**

.. program-output:: cat scripts/Writing_Test_In_YAML/outputfile.yaml

.. program-output:: cat scripts/Writing_Test_In_YAML/outputfile.sh

**args Example**


.. program-output:: cat scripts/Writing_Test_In_YAML/args.yaml

.. program-output:: cat scripts/Writing_Test_In_YAML/args.sh


**iter Example**

We can create duplicate test scripts using the iter keyword in YAML. 

.. program-output:: cat scripts/Writing_Test_In_YAML/iter.yaml

.. program-output:: cat scripts/Writing_Test_In_YAML/iter.txt


