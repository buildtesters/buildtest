Running Test
==================


.. program-output:: cat scripts/run_subcommand/help.txt


Run an Application Test Suite (``buildtest run --software``)
---------------------------------------------------------------

buildtest can run test written in ``$BUILDTEST_TESTDIR`` for a particular application
specified by option ``--software``. The choice field for this option is populated based
on directories found in ``$BUILDTEST_TESTDIR`` which were created by subsequent runs
of ``buildtest build -s <application>``.

::

    (buildtest) [siddis14@adwnode11 buildtest-framework]$ buildtest run --software
    GCC/6.4.0-2.28             GCCcore/6.4.0              Perl/5.26.0-GCCcore-6.4.0


Shown below is an output of ``buildtest run --software GCCcore/6.4.0`` which attempts
to run all tests for application ``GCCcore/6.4.0``

.. program-output:: tail -n 15 scripts/run_subcommand/app_GCCcore.txt


Run a System Package Test Suite (``buildtest run --package``)
------------------------------------------------------------------

Similarly, ``buildtest run --package`` is used to run test suite for system packages
that were built by option ``buildtest build --package <package>``

Shown below is an output of ``buildtest run --package gcc``

.. program-output:: cat scripts/run_subcommand/systempkg_gcc.txt

Submitting Jobs to Scheduler (``buildtest run -j``)
----------------------------------------------------

buildtest can submit jobs to scheduler for test scripts with the scheduler extension (``.slurm``, ``.lsf``).
Depending on the scheduler you have at site, buildtest will auto-detect the scheduler and attempt to submit
all jobs that are available.

To utilize the ``-j`` or long option ``--job`` it must be used in conjunction with test suite option
``-S`` or long option ``--suite``. For more details on test suite see :ref:`Suite`

For example, we have 3 tests in the mpi test suite (``-S mpi``) in the test directory which
we want to run. Tests that have the extension (``.sh``, ``.bash``, ``.csh``) will be run locally
and test with extension (``.slurm``, ``.lsf``) will be sent to the scheduler.

In example below one test was run locally and two were sent to scheduler.

::

    $ buildtest run -S mpi -j
    Running All Tests from Test Directory: /tmp/ec2-user/buildtest/tests/suite/mpi
    ==============================================================
                             Test summary
    Package:  mpi
    Executed 3 tests
    Passed Tests: 3 Percentage: 100.0%
    Failed Tests: 0 Percentage: 0.0%
    SUCCESS: Threshold of 100.0% was achieved
    Writing results to /tmp/ec2-user/buildtest/run/buildtest_15_29_19_08_2019.run
    Submitted batch job 17
    Submitting Job: /tmp/ec2-user/buildtest/tests/suite/mpi/examples/mpi_ping.c.slurm.yml.slurm to scheduler
    Submitted batch job 18
    Submitting Job: /tmp/ec2-user/buildtest/tests/suite/mpi/examples/mpi_ping.c_ex1.yml.slurm to scheduler

Let's take a look at the top-level mpi directory which is a single directory ``examples``

::

    $ ls -l /tmp/ec2-user/buildtest/tests/suite/mpi
    total 0
    drwxrwxr-x 2 ec2-user ec2-user 94 Aug 19 15:29 examples

The sub-directory consists of three tests which were created using ``buildtest build``

::

    (buildtest-framework) [ec2-user@buildtest buildtest-framework]$ ls -l /tmp/ec2-user/buildtest/tests/suite/mpi/examples/
    total 12
    -rwxr-xr-x 1 ec2-user ec2-user 629 Aug 19 15:27 hello.c.yml.sh
    -rwxr-xr-x 1 ec2-user ec2-user 672 Aug 19 15:28 mpi_ping.c_ex1.yml.slurm
    -rwxr-xr-x 1 ec2-user ec2-user 690 Aug 19 15:27 mpi_ping.c.slurm.yml.slurm

If we were to run without ``-j`` option, then buildtest will skip tests with extension (``.slurm``, ``.lsf``)
and run the test locally. In this case, it will run 1 test.

::

    $ buildtest run -S mpi
    Running All Tests from Test Directory: /tmp/ec2-user/buildtest/tests/suite/mpi
    ==============================================================
                             Test summary
    Package:  mpi
    Executed 1 tests
    Passed Tests: 1 Percentage: 100.0%
    Failed Tests: 0 Percentage: 0.0%
    SUCCESS: Threshold of 100.0% was achieved
    Writing results to /tmp/ec2-user/buildtest/run/buildtest_15_51_19_08_2019.run

