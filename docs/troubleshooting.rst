Troubleshooting Buildtest
===========================

This guide will discuss how to troubleshoot buildtest when you encounter issues.

How to enable debugging?
---------------------------

Whenever you run into issues with buildtest, you should enable debug mode by running
``buildtest --debug <command>`` which will stream debug messages to console. The debug
messages can help pinpoint issues and provide additional details.

buildtest will write a log file, you can view content of log via::

    buildtest --view-log
    buildtest --print-log

The ``--print-log`` will print output to console, while ``--view-log`` will display in paginated
mode. By default, buildtest will write logfile in **$BUILDTEST_ROOT/var/buildtest.log**. You can
view path to logfile via ``buildtest --logpath``.

If you want to filter log messages when running command you can run ``buildtest --loglevel <LOG_LEVEL>``.
The `logging levels <https://docs.python.org/3/library/logging.html#levels>`_ are defined in the python
`logging <https://docs.python.org/3/library/logging.html>`_ library.

The ``buildtest info`` command can be useful when debugging buildtest, it will report a
summary of details related to buildtest and system details that can help pinpoint issue.

How to troubleshoot buildtest configuration?
---------------------------------------------

buildtest provides several location where configuration file can be defined. You can
see :ref:`which configuration file is used by buildtest <which_configuration_file_buildtest_reads>`.
You can retrieve path to configuration used by buildtest by running ``buildtest config path``.
Check if the path to configuration file is one you want to use.

The environment variable **BUILDTEST_CONFIGFILE** can be used to specify path to configuration file,
you should check if this variable is set in your shell.

To validate your configuration file with JSON Schema you should run the following::

    buildtest config validate

If your configuration is invalid, please review the error message and fix the configuration. Please
run ``buildtest config validate`` until your configuration is valid.

Hostname mismatch
~~~~~~~~~~~~~~~~~~

The configuration file must specify ``hostnames`` for determining where buildtest
can run, please see :ref:`config_hostnames`. If you see an error message when validating configuration
file, please consider updating ``hostnames`` property or login to the desired host where buildtest should
be run. An example below shows an error message when you run into hostname issues.

.. code-block:: console

    ConfigurationError: "[/Users/siddiq90/Documents/github/buildtest/buildtest/settings/config.yml]: Based on current system hostname: DOE-7086392.vpn-dhcp.lbl.gov\n we cannot
    find a matching system  ['generic'] based on current hostnames: {'generic': ['foo']} "

How to troubleshoot a buildspec?
---------------------------------

If you are developing a buildspec file, please consider checking file is valid, there are several way to validate
file, the most convenient way is to run::

  buildtest buildspec validate -b <file>

If your buildspec is valid, your next step is to run the test. You should check if test is generated properly,
this can be done by running ``buildtest build -b <file> --stage=build`` which will generate
the test and stop execution. Next you can navigate to the generated test and inspect
the content of test and run your test manually.

How to view past builds?
-------------------------

You can :ref:`access build history <build_history>` via ``buildtest history`` command. To see a list
of builds you can run::

    buildtest history list

Next you can query a given build you can run::

    buildtest history query <id>

To view output of ``buildtest build`` command for a given build you can run::

    buildtest history query -o <id>

The build history is valid until files are removed, which could be done via ``buildtest clean`` or
files are remove manually. The build history provides a means for accessing old builds along with logfile
for each build.

How to view all available tests in buildspec cache?
----------------------------------------------------

First, make sure your buildspec cache is built, you can run ``buildtest buildspec find --rebuild`` to rebuild the
cache. Once buildspec cache is built, you can view query all tests in buildspec cache by running::

    buildtest buildspec find --format name --terse --no-header

Shown below is a sample output where we query 5 records from the buildspec cache

.. command-output:: buildtest buildspec find --format name --terse --no-header --count=5

To get all tests in buildspec cache, consider setting to any negative value ``--count=-1`` or a really high number.

Unable to query test details
------------------------------

Let's say you are trying to query a test name ``hello_world``, and you get an error message such as following

.. code-block:: console

      buildtest it query hello_world
    Unable to find any tests by name ['hello_world'], please select one of the following tests: ['returncode_list_mismatch', 'returncode_int_match', 'exit1_pass', 'exit1_fail', 'python_hello', 'circle_area']

To address this issue, you will need to first build the test, so that buildtest can capture the results in the report file. This can be done
in various ways, typically you can do ``buildtest build -b <file>`` to specify the buildspec file that will run the test ``hello_world``.
You can also use ``buildtest build --name hello_world`` which will let buildtest find the buildspec that corresponds to test ``hello_world`` and then run the test.

Once test is built, the test will be added to the report file and you can query the test by name.

If you use ``buildtest --report`` to write test result to alternate report file, please make sure you specify the report path. You can run into
issues if you don't the correct report path which could lead to error. You can query the current report file using ``buildtest report path`` or
use ``buildtest report list`` to show all report files.

Unable to query all test results
---------------------------------

If you run into situation where you are unable to query all test results,
you should check the buildtest configuration file see :ref:`configuring_buildtest_report`. In this section, check if
``count`` property is set in configuration file. For instance if you have ``count: 25``, everytime you run ``buildtest report`` it
will query 25 records

.. code-block:: yaml

    report:
      count: 25

You will have a situation where buildtest will only show 25 records as shown below

.. code-block:: console

      buildtest report --terse --no-header | wc -l
     25

You can work around this issue by passing ``--count`` on command line and it will override the configuration.
To retrieve all content you can specify a negative value and buildtest will fetch all records or alternatively you
can specify a really high number

.. code-block:: console

      buildtest report --terse --no-header --count=-1 | wc -l
    30

If you want to make this change permanent, you can update the configuration file and set ``count`` to a high number

