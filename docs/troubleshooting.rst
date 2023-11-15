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
