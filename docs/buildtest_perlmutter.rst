Buildtest Tutorial on Perlmutter
===================================

This tutorial will be conducted on `Perlmutter <https://docs.nersc.gov/systems/perlmutter/>`_ system. If you need account access please
`obtain a user account <https://docs.nersc.gov/accounts/>`_.

Setup
------

Once you have a NERSC account, you can `connect to NERSC system <https://docs.nersc.gov/connect/>`_. You will need access to a
terminal client and ssh into perlmutter as follows::

    ssh <user>@perlmutter-p1.nersc.gov

To get started please load the **python** module since you will need python 3.7 or higher to use buildtest. This can be done by running::

    module load python

Next, you should :ref:`Install buildtest <installing_buildtest>` by cloning the repository in your $HOME directory.

Once you have buildtest setup, please clone the following repository https://github.com/buildtesters/buildtest-nersc in your $HOME directory as follows::

    cd $HOME
    git clone https://github.com/buildtesters/buildtest-nersc $HOME/buildtest-nersc
    export BUILDTEST_CONFIGFILE=$HOME/buildtest-nersc/config.yml

Once you are done, please navigate back to root of buildtest which can be done by running::

    cd $BUILDTEST_ROOT

Exercise 1: Running a Batch Job
--------------------------------

In this exercise, we will submit a batch job that will run `hostname` in the slurm cluster. Shown below is the example buildspec

.. literalinclude:: ../perlmutter_tutorial/ex1/hostname.yml
   :language: yaml

Let's run this test and poll interval for 10 secs::

   buildtest build -b $BUILDTEST_ROOT/perlmutter_tutorial/ex1/hostname.yml --pollinterval=10

Once test is complete, check the output of test by running::

    buildtest inspect query -o hostname_perlmutter

Next, let's update the test such that it runs on both **regular** and **debug** queue. You will need to update the **executor** property and
specify a regular expression. Please refer to :ref:`Multiple Executors <multiple_executors>` for reference. You can retrieve a list of available executors
by running ``buildtest config executors``.

Once you have updated the test, please rerun the test, now you should expect to see two runs for same test.

Exercise 2: Performing Status Check
------------------------------------

In this exercise, we will check version of Lmod via environment **LMOD_VERSION** and specify the
the output using :ref:`regular expression <regex>`.

.. literalinclude:: ../perlmutter_tutorial/ex2/module_version.yml
   :language: yaml

This buildspec is invalid, your first task is to make sure buildspec is valid. Once you have accomplished this task, try building
the test and check the output of test. If your test passes, try updating the regular expression and see if test fails. Revert the change
back and make the test pass.

Exercise 3: Querying Buildspec Cache
-------------------------------------

In this exercise you will learn how to use the :ref:`buildspec_interface`. Let's build the cache by running the following::

    buildtest buildspec find --root $HOME/buildtest-nersc/buildspecs --rebuild -q

In this task you will be required to do the following

1. Find all tags
2. List all filter and format fields
3. Format table via fields ``name``, ``description``
4. Filter buildspec by tag ``e4s``
5. List all invalid buildspecs
6. Validate all buildspecs by tag ``e4s``
7. Show content of test ``hello_world_openmp``

Exercise 4: Querying Test Reports
----------------------------------

In this exercise you will be learn how to :ref:`query test report <test_reports>`. This can be done by
running ``buildtest report``. In this task please do the following

1. List all filter and format fields
2. Query all test by returncode 0
3. Query all test by tag ``e4s``
4. Print total count of failed tests

Let's upload the test to CDASH by running the following::

    buildtest cdash upload $USER-buildtest-tutorial

Take some time to analyze the output in CDASH by opening the link including PASS/FAIL test.

Exercise 5: Specifying Performance Checks
--------------------------------------------

In this task, we will using :ref:`performance checks <perf_checks>` to determine state of test.
In this exercise, we will be running the STREAM benchmark. Shown below is an example buildspec that you
will be working with

.. literalinclude:: ../perlmutter_tutorial/ex5/stream.yml
   :language: yaml

First, let's build this test and analyze the output::

  buildtest build -b perlmutter_tutorial/ex5/stream.yml
  buildtest inspect query -o stream_test

Take a close look at the metrics value. In this task, you are requested to use use :ref:`assert_ge` with metric ``copy`` and
``scale`` with reference value. For reference value please experiment with different metrics and see if test pass/fail.
