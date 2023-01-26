Buildtest Tutorial on Perlmutter
===================================

This tutorial will be conducted on the `Perlmutter <https://docs.nersc.gov/systems/perlmutter/>`_ system. If you need account access please
`obtain a user account <https://docs.nersc.gov/accounts/>`_.

Setup
------

Once you have a NERSC account, you can any `connect to NERSC system <https://docs.nersc.gov/connect/>`_.
terminal client and ssh into perlmutter as follows::

    ssh <user>@perlmutter-p1.nersc.gov

To get started please load the **python** module since you will need python 3.7 or higher to use buildtest. This can be done by running::

    module load python

Next, you should :ref:`Install buildtest <installing_buildtest>` by cloning the repository into your home directory::

    git clone https://github.com/buildtesters/buildtest.git

Once you have buildtest setup, please clone the following repository in your home directory as follows::

    cd $HOME
    git clone https://github.com/buildtesters/buildtest-nersc $HOME/buildtest-nersc
    export BUILDTEST_CONFIGFILE=$HOME/buildtest-nersc/config.yml

Once you are done, please navigate back to the root of buildtest::

    cd $BUILDTEST_ROOT

Exercise 1: Running a Batch Job
--------------------------------

In this exercise, we will submit a batch job that will run `hostname` in the slurm cluster. Shown below is the example buildspec

.. literalinclude:: ../perlmutter_tutorial/ex1/hostname.yml
   :language: yaml

Let's run this test with a poll interval of ten seconds::

   buildtest build -b $BUILDTEST_ROOT/perlmutter_tutorial/ex1/hostname.yml --pollinterval=10

Once test is complete, check the output of the test by running::

    buildtest inspect query -o hostname_perlmutter

Next, let's update the test such that it runs on both the **regular** and **debug** queue. You will need to update the **executor** property and
specify a regular expression. Please refer to :ref:`Multiple Executors <multiple_executors>` for reference. You can retrieve a list of available executors
by running ``buildtest config executors``.

Once you have updated and re-run the test, you should see two runs for the same test. If you ran this successfully, you should
see the following when running the test

.. code-block:: console

    hostname_perlmutter/80e317c1 does not have any dependencies adding test to queue
    hostname_perlmutter/b1d7b318 does not have any dependencies adding test to queue
    In this iteration we are going to run the following tests: [hostname_perlmutter/80e317c1, hostname_perlmutter/b1d7b318]
    hostname_perlmutter/b1d7b318: Current Working Directory : /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/perlmutter.slurm.regular/solution/hostname_perlmutter/b1d7b318/stage
    hostname_perlmutter/80e317c1: Current Working Directory : /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/perlmutter.slurm.debug/solution/hostname_perlmutter/80e317c1/stage
    hostname_perlmutter/b1d7b318: Running Test via command: bash --norc --noprofile -eo pipefail hostname_perlmutter_build.sh
    hostname_perlmutter/80e317c1: Running Test via command: bash --norc --noprofile -eo pipefail hostname_perlmutter_build.sh
    hostname_perlmutter/80e317c1: JobID 4990982 dispatched to scheduler
    hostname_perlmutter/b1d7b318: JobID 4990983 dispatched to scheduler
    Polling Jobs in 30 seconds
    hostname_perlmutter/80e317c1: Job 4990982 is complete!
    hostname_perlmutter/80e317c1: Test completed in 30.248888 seconds
    hostname_perlmutter/80e317c1: Test completed with returncode: 0
    hostname_perlmutter/80e317c1: Writing output file -  /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/perlmutter.slurm.debug/solution/hostname_perlmutter/80e317c1/hostname_perlmutter.out
    hostname_perlmutter/80e317c1: Writing error file - /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/perlmutter.slurm.debug/solution/hostname_perlmutter/80e317c1/hostname_perlmutter.err
                                    Pending and Suspended Jobs
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┓
    ┃ builder                      ┃ executor                 ┃ jobid   ┃ jobstate ┃ runtime ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━┩
    │ hostname_perlmutter/b1d7b318 │ perlmutter.slurm.regular │ 4990983 │ PENDING  │ 30.455  │
    └──────────────────────────────┴──────────────────────────┴─────────┴──────────┴─────────┘
                                          Completed Jobs
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┓
    ┃ builder                      ┃ executor               ┃ jobid   ┃ jobstate  ┃ runtime   ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━┩
    │ hostname_perlmutter/80e317c1 │ perlmutter.slurm.debug │ 4990982 │ COMPLETED │ 30.248888 │
    └──────────────────────────────┴────────────────────────┴─────────┴───────────┴───────────┘


Exercise 2: Performing Status Check
------------------------------------

In this exercise, we will check the version of Lmod using the environment variable **LMOD_VERSION** and specifying the
the output using a :ref:`regular expression <regex>`.

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
2. List all filters and format fields
3. Format tables via fields ``name``, ``description``
4. Filter buildspecs by tag ``e4s``
5. List all invalid buildspecs
6. Validate all buildspecs by tag ``e4s``
7. Show content of test ``hello_world_openmp``

Exercise 4: Querying Test Reports
----------------------------------

In this exercise you will be learn how to :ref:`query test reports <test_reports>`. This can be done by
running ``buildtest report``. In this task please do the following

1. List all filters and format fields
2. Query all tests by returncode 0
3. Query all tests by tag ``e4s``
4. Print total count of all failed tests

Let's upload the tests to CDASH by running the following::

    buildtest cdash upload $USER-buildtest-tutorial

Take some time to analyze the output in CDASH by opening the link.

Exercise 5: Specifying Performance Checks
--------------------------------------------

In this task, we will running the STREAM benchmark and use :ref:`performance checks <perf_checks>` to determine if
test will pass based on the performance results. Shown below is stream example that we will be using for this exercise

.. literalinclude:: ../perlmutter_tutorial/ex5/stream.yml
   :language: yaml

First, let's build this test and analyze the output::

  buildtest build -b perlmutter_tutorial/ex5/stream.yml
  buildtest inspect query -o stream_test

Take a close look at the metrics value. In this task, you are requested to use use :ref:`assert_ge` with metric ``copy`` and
``scale`` with a reference value. For the reference value please experiment with different metrics and see if test passes or fails.
