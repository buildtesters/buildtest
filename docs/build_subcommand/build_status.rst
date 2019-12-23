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

Fetch Log files (``buildtest build log``)
-----------------------------------------
To get the log file for a particular build you can run the following::


    $ buildtest build log <ID>

buildtest will open the log file using ``less`` command so you can interactively search the logfile.

For instance let's check the build log for ``ID=0``. You can get this by running either of the two commands::

    $ buildtest build log 0
    $ buildtest build log id=0

Here is a snapshot of the build log::

    2019-09-13 16:27:34,178 [binarytest.py:93 - generate_binary_test() ] - [INFO] Test Destination Directory: /home/siddis14/tmp/system/gcc
    2019-09-13 16:27:34,178 [binarytest.py:94 - generate_binary_test() ] - [INFO] Creating Test Directory: /home/siddis14/tmp/system/gcc
    2019-09-13 16:27:34,178 [binarytest.py:95 - generate_binary_test() ] - [INFO] Following binaries will be tested: ['/usr/bin/c89', '/usr/bin/c99', '/usr/bin/gcc', '/usr/bin/gcc-ar', '/usr/bin/gcc-nm', '/usr/bin/gcc-ranlib', '/usr/bin/gcov', '/usr/bin/x86_64-redhat-linux-gcc']
    2019-09-13 16:27:34,182 [binarytest.py:119 - generate_binary_test() ] - [DEBUG] Creating and Opening  test file: /home/siddis14/tmp/system/gcc/_usr_bin_c89.sh for writing
    2019-09-13 16:27:34,182 [binarytest.py:145 - generate_binary_test() ] - [INFO] Writing Test: /home/siddis14/tmp/system/gcc/_usr_bin_c89.sh and setting permission to 755
    2019-09-13 16:27:34,183 [binarytest.py:153 - generate_binary_test() ] - [INFO] Content of test file: /home/siddis14/tmp/system/gcc/_usr_bin_c89.sh
    2019-09-13 16:27:34,183 [binarytest.py:154 - generate_binary_test() ] - [INFO] [START]
    2019-09-13 16:27:34,183 [binarytest.py:156 - generate_binary_test() ] - [INFO] #!/bin/sh
    2019-09-13 16:27:34,183 [binarytest.py:156 - generate_binary_test() ] - [INFO]
    2019-09-13 16:27:34,183 [binarytest.py:156 - generate_binary_test() ] - [INFO] which /usr/bin/c89
    2019-09-13 16:27:34,183 [binarytest.py:159 - generate_binary_test() ] - [INFO] [END]

Fetching Tests associated to a build (``buildtest build test``)
-----------------------------------------------------------------

To view the test generated from the build you will need the build ID and run the following::

    $ buildtest build test id=<ID>

You may omit the ``id=<ID>`` and specify the number as argument to ``test`` as follows::

    $ buildtest build test <ID>

Shown below is the generated test from build ``ID=0``.

.. program-output:: cat docgen/build-test-example.txt

Running Test Locally (``buildtest build run``)
----------------------------------------------------

To run a test, you may invoke ``buildtest build run <ID>`` which will run all tests for the particular build ID. If
you are not sure what tests will be run, you can use a combination of ``buildtest build report`` and ``buildtest build test <ID>``
to retrieve the build command and tests associated to the build ID.

Shown below is an example run for on build ``ID=1``

.. program-output:: cat docgen/build-run-example.txt

