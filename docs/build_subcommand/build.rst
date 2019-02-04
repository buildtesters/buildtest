Build Tests
=================

.. contents::
   :backlinks: none

Build Subcommand (``buildtest build``)
----------------------------------------


.. program-output:: cat scripts/build_subcommand/help.txt

Building tests for Software Packages
-------------------------------------


To build test via buildtest you will need to use ``buildtest build -s`` option. To
demonstrate this lets run the following

::

    buildtest build -s CMake/3.9.5-GCCcore-6.4.0

The output will be the following

.. program-output:: cat scripts/build_subcommand/CMake-3.9.5-GCCcore-6.4.0.txt

Building test for System Packages
----------------------------------

To build test for system package you will want to use ``buildtest build --package`` and
specify the name of the system package. This should be a system package that is installed
in your system.

To demonstrate this example, lets build the test for package ``coreutils``

::

    buildtest build --package coreutils

The output will be the following

.. program-output:: cat scripts/build_subcommand/coreutils.txt


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

::

    (buildtest-0.5.0) [siddis14@adwnode1 buildtest-framework]$ buildtest build --package gcc --testdir /home/siddis14/tmp/
    --------------------------------------------
    [STAGE 1]: Building Binary Tests
    --------------------------------------------
    Detecting Test Type: System Package
    Processing Binary YAML configuration:  /home/siddis14/github/buildtest-configs/buildtest/system/gcc/command.yaml
    Generating  7  binary tests
    Binary Tests are written in  /home/siddis14/tmp/system/gcc
    Writing Log file to:  /tmp/buildtest/system/gcc/buildtest_12_38_17_10_2018.log
