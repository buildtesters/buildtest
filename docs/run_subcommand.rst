Run Subcommands
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