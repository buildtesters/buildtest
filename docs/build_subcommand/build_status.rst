Retrieve Build Status (``buildtest status``)
=============================================

buildtest is keeping track of all builds including start/end time of build process, build log file, command
executed and test scripts generated as result of build. This information is stored in a file ``BUILDTEST_ROOT/var/build.json``
that is updated by buildtest whenever you issue ``buildtest build`` command.

To retrieve status detail of builds, use the following command::

    $ buildtest status


Currently, buildtest can report all builds and access logfile and list tests generated from a given build.
To get a sense of the command usage you can run ``buildtest status -h``.

.. program-output:: cat scripts/buildtest_status_help.txt

To see a status report of all builds you can run::

    $ buildtest status report

This will show the build report of all builds executed in a tabular output.

.. program-output:: cat scripts/buildtest_status_report.txt

Each row corresponds to a unique build identified by build **ID** that can be used to dig up the log file
and report tests. To get the log file for a build you can run the following::


    $ buildtest status log <ID>

buildtest will open the log file using ``less`` command so you can interactively search the logfile.

For instance let's check the build log for ``ID=0``. You can get this by running either of the two commands::

    $ buildtest status log 0
    $ buildtest status log id=0

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

To view the test generated from the build you will need the build ID and run the following::

    $ buildtest status test id=<ID>

You may omit the ``id=<ID>`` and specify the number as argument to ``test`` as follows::

    $ buildtest status test <ID>

Shown below is the generated test from build ``ID=0``.

.. program-output:: cat scripts/buildtest_status_test.txt
