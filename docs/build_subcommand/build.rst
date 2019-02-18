Build Overview
=================

.. contents::
   :backlinks: none

Build Options (``buildtest build --help``)
---------------------------------------------


.. program-output:: cat scripts/build_subcommand/help.txt

Test Suites
-------------

Tests are categorized into test suite which can be found at https://github.com/HPC-buildtest/buildtest-configs/tree/master/buildtest/suite.
To run a test suite, you will need to run with ``buildtest build -S <suite>``  which will run all tests defined in the suite.

To know more about test suite see :ref:`Suite`


Building test for System Packages
----------------------------------

To build test for system package you will want to use ``buildtest build --package`` and
specify the name of the system package. This will be a system package installed
in your system.

For instance, lets build the tests for ``coreutils`` package by running ``buildtest build --package coreutils``

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

.. program-output:: cat scripts/build_subcommand/custom_test_dir.txt
