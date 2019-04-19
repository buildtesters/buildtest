Overview
=================

.. contents::
   :backlinks: none

Build Options (``buildtest build --help``)
---------------------------------------------


.. program-output:: cat scripts/buildtest-build-help.txt

Test Configuration
-------------------

buildtest makes use of test configuration to generate the test script. This
can be done by running ``buildtest build -c /path/to/configuration``

Shown below is an example.

::

    $ buildtest build -c $BUILDTEST_ROOT/toolkit/buildtest/suite/compilers/helloworld/hello_gnu.yml
    Writing Test: /home/siddis14/buildtest/suite/compilers/helloworld/hello_gnu.yml.sh


buildtest has two levels of verbosity that can be set by using ``-v`` option.
buildtest will check the programming language, compiler and verify all the
keys in configuration file before building the test.

buildtest will set the permission of test script to ``755``.

::

    $ buildtest build -c $BUILDTEST_ROOT/toolkit/buildtest/suite/compilers/helloworld/hello_gnu.yml -v
    Key Check PASSED for file /home/siddis14/buildtest-framework/toolkit/buildtest/suite/compilers/helloworld/hello_gnu.yml
    Programming Language Detected: c++
    Compiler Check Passed
    Writing Test: /home/siddis14/buildtest/suite/compilers/helloworld/hello_gnu.yml.sh
    Changing permission to 755 for test: /home/siddis14/buildtest/suite/compilers/helloworld/hello_gnu.yml.sh



You may specify additional level verbosity by ``-vv`` or specify ``-v -v``
which will give additional output including the output of configuration file and test
script.

::

    $ buildtest build -c $BUILDTEST_ROOT/toolkit/buildtest/suite/compilers/helloworld/hello_gnu.yml -v -v
    ________________________________________________________________________________
    compiler: gnu
    flags: -O3
    maintainer:
    - shahzeb siddiqui shahzebmsiddiqui@gmail.com
    source: hello.cpp
    testblock: singlesource

    ________________________________________________________________________________
    Key Check PASSED for file /home/siddis14/buildtest-framework/toolkit/buildtest/suite/compilers/helloworld/hello_gnu.yml
    Source File /home/siddis14/buildtest-framework/toolkit/buildtest/suite/compilers/helloworld/src/hello.cpp exists!
    Programming Language Detected: c++
    Compiler Check Passed
    Writing Test: /home/siddis14/buildtest/suite/compilers/helloworld/hello_gnu.yml.sh
    Changing permission to 755 for test: /home/siddis14/buildtest/suite/compilers/helloworld/hello_gnu.yml.sh
    ________________________________________________________________________________
    #!/bin/sh
    module purge
    module load eb/2018
    cd /home/siddis14/buildtest/suite/compilers/helloworld
    g++ -O3 -o hello.cpp.exe /home/siddis14/buildtest-framework/toolkit/buildtest/suite/compilers/helloworld/src/hello.cpp
    ./hello.cpp.exe
    rm ./hello.cpp.exe
    ________________________________________________________________________________


Test Suites
-------------

Test Suite is a collection of test configuration that is meant for organizing
tests. Test suite can be found at
https://github.com/HPC-buildtest/buildtest-framework/tree/master/toolkit/buildtest/suite.
and each sub-directory is a separate test suite.

A test suite is capable of building all test configuration (``.yml`` files)
found in its subdirectories. To build a test suite you can execute
``buildtest build -S <suite>``

To know more about test suite see :ref:`Suite`


Sanity Check for System Packages
---------------------------------

buildtest can perform sanity check for all binaries defined by a system
package. This may be useful when running test periodically to monitor system
changes.

To build test for system package you will want to use
``buildtest build --package <package>`` and specify the name of the
installed system package.

For instance, lets build the tests for ``coreutils`` package by running
``buildtest build --package coreutils``

The output will be the following

.. program-output:: cat scripts/coreutils-binary-test.txt


Sanity Check for Modules
------------------------

buildtest can conduct sanity check for all active modules by running ``-b``,
``--binary`` option or setting ``BUILDTEST_BINARY=True`` in your
configuration file.

For instance let's assume the following modules are active modules in your
shell

::

    $ ml

    Currently Loaded Modules:
      1) eb/2018   2) GCCcore/6.4.0   3) binutils/2.28-GCCcore-6.4.0   4) GCC/6.4.0-2.28


buildtest will seek out all binary executables in each module file and run
``which`` command against the binary and load the appropriate modules

Shown below is an example.

::

    $ buildtest build -b
    Detecting Software:eb/2018
    No $PATH set in your module  eb/2018   so no possible binaries can be found
    There are no binaries for package: eb/2018
    Detecting Software:GCCcore/6.4.0
    Generating  19  binary tests
    Binary Tests are written in  /home/siddis14/buildtest/software/GCCcore/6.4.0
    Detecting Software:binutils/2.28-GCCcore-6.4.0
    Generating  18  binary tests
    Binary Tests are written in  /home/siddis14/buildtest/software/binutils/2.28-GCCcore-6.4.0
    Detecting Software:GCC/6.4.0-2.28
    No $PATH set in your module  GCC/6.4.0-2.28   so no possible binaries can be found
    There are no binaries for package: GCC/6.4.0-2.28


modules that dont have ``PATH`` set or no binary executables are found in
the directory, then buildtest will not generate any test.

Shown below is an example test script for gcc binary

::

    #!/bin/sh


    module load GCCcore/6.4.0
    which gcc


Clean build (``buildtest build --clean-build``)
-------------------------------------------------------

buildtest will preserve the testing directory when tests are generated. For example, if you
run the following

::

    buildtest build --package gcc --shell sh
    buildtest build --package gcc --shell csh
    buildtest build --package gcc --shell bash

This will write the test for shell ("sh", "bash", "csh") in the same directory. If you
want to remove the directory prior to running test you can do the following

::

    buildtest build --package gcc --clean-build

Customize Test Directory (``buildtest build --testdir``)
-------------------------------------------------------------

If you want to customize the path to BUILDTEST_TESTDIR you may use the option ``--testdir``
or update the environment variable ``BUILDTEST_TESTDIR``. The command line option will override
environment variable and environment variable will override configuration value.

.. program-output:: cat scripts/gcc-binary-test.txt

Shell Types
--------------

Currently buildtest supports ``sh``, ``bash``, ``csh`` shell for creating
test scripts. buildtest defaults to ``sh`` but this can be tweaked

To create tests for different shell types try ``buildtest build --shell <shell>``
or set the variable ``BUILDTEST_SHELL`` in your configuration file or via
environment variable

Let's build test with ``csh``

.. program-output:: cat scripts/build-shell-csh.txt

buildtest will add the appropriate shell extension for the test script to
avoid name conflicts.

Another way to build for different shell is to set ``BUILDTEST_SHELL`` as we
see in example below

.. program-output:: cat scripts/build-shell-bash.txt


