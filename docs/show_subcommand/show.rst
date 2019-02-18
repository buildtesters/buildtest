Show Options (``buildtest show --help``)
============================================

.. program-output:: cat scripts/show_subcommand/help.txt

Show Configuration (``buildtest show --config``)
-------------------------------------------------

buildtest can display it's configuration by running ``buildtest show --config``. The
configuration can be changed by the following.

 1. Command Line
 2. Environment Variable (``BUILDTEST_``)
 3. Configuration File (``settings.yml``)

buildtest will read configuration from ``settings.yml``. User may override any configuration
values by environment variables that start with ``BUILDTEST_``. The command line will 
override environment variables and configuration variables runtime.

Shown below is a sample configuration from buildtest.


.. program-output:: cat scripts/show_subcommand/configuration.txt



``buildtest show --show`` will update the output as you set any BUILDTEST environment
variables.

For instance, if you want to customize the buildtest log via environment variable. ``buildtest --show`` will report
which values are overridden by environment variable with a notation **(E)**.

See example below

::

    (buildtest) [siddis14@gorgon buildtest-framework]$ export BUILDTEST_LOGDIR=/tmp
    (buildtest) [siddis14@gorgon buildtest-framework]$ buildtest show -c | grep BUILDTEST_LOGDIR
    BUILDTEST_LOGDIR                                   (E) = /tmp



.. Note:: if you plan to customize your buildtest configuration with configuration file
    and environment variable, always check your shell environment first to avoid having
    values overridden accidentally

Show Keys
-----------

buildtest can show YAML keys based on testblock. Currently, there is one testblock 
defined **singlesource**. 

To show yaml keys you can run ``buildtest show -k singlesource`` to view all the YAML
keys that pertain to ``testblock: singlesource`` found in YAML files

.. program-output:: cat scripts/show_subcommand/singlesource.txt

