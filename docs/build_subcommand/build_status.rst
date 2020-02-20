.. _build_status:

Retrieve Build Status
======================

buildtest is keeping track of all builds such as build time, build log file, command
executed and test scripts generated as result of build. This information is stored in a file ``BUILDTEST_ROOT/var/build.json``
that is updated by buildtest whenever you issue ``buildtest build`` command.

Build Report (``buildtest build report``)
------------------------------------------

To see a status report of all builds you can run::

    $ buildtest build report

This will show the build report of all builds executed in a tabular output.

.. program-output:: cat docgen/build-report.txt

Each row corresponds to a unique build identified by build **ID** that can be used to dig up the log file
and report tests.

