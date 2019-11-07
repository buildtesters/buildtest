.. _configuring_buildtest:

Configuring buildtest
======================


Configuration File
--------------------

buildtest will store the user's buildtest configuration at ``$HOME/.buildtest/settings.yml``. This file is responsible for
configuring buildtest which can be customized to fit your site requirements. buildtest will automatically
generate this file if it is not present. To view the buildtest configuration you can run the following::

    $ buildtest config view

Shown below is the user's buildtest configuration.

.. program-output:: cat docgen/buildtest_config_view.txt

buildtest keeps a backup configuration (``~/.buildtest/settings.yml.bak``) in case you want to restore to
the original settings. This can be done by running::

.. program-output:: cat docgen/buildtest_config_restore.txt

Similarly, if you want to edit the configuration you may run::

    $ buildtest config edit

This will open the configuration in ``vim`` editor. For list of options on buildtest configuration, run
``buildtest config --help`` for more details.


Next section will discuss the variables defined in the configuration file.


Configuring Module Trees
--------------------------

**BUILDTEST_MODULEPATH** takes colon separated list of root of a module tree
in your system that serves as module files. buildtest will read all module
files and use this to figure out what modules can be tested.

Let's assume ``/opt/apps`` and ``/workspace/apps`` are root of the module tree,
so we can specify this in your configuration as follows::

	BUILDTEST_MODULEPATH:
        - /opt/apps
        - /workspace/apps

If you set an invalid directory path in ``BUILDTEST_MODULEPATH`` you will get
the following message

.. Error::
    /opt/apps directory does not exist, specified in BUILDTEST_MODULEPATH


If you don't specify a module tree for BUILDTEST_MODULEPATH then buildtest
will read the value of MODULEPATH. You may add,remove or list module tree.

To see the list of module tree you can run ``buildtest module -l``::

    $ buildtest module -l
    /nfs/grid/software/moduledomains
    /etc/modulefiles
    /usr/share/modulefiles
    /usr/share/lmod/lmod/modulefiles/Core

At this time you will notice BUILDTEST_MODULEPATH is not set and it takes
value of MODULEPATH::

    $ cat ~/.buildtest/settings.yml  | grep -i BUILDTEST_MODULEPATH
    BUILDTEST_MODULEPATH: []

    $ echo $MODULEPATH
    /nfs/grid/software/moduledomains:/etc/modulefiles:/usr/share/modulefiles:/usr/share/modulefiles/Linux:/usr/share/modulefiles/Core:/usr/share/lmod/lmod/modulefiles/Core


You can add new module tree through command line using ``buildtest module
-a`` which will update the configuration file::

    $ buildtest module -a /usr/share/lmod/lmod/modulefiles/Core
    Adding module tree: /usr/share/lmod/lmod/modulefiles/Core
    Configuration File: /home/siddis14/.buildtest/settings.yml has been updated


Similarly you can remove module tree from your configuration via
``buildtest module -r``::

    (siddis14-TgVBs13r) buildtest-framework[master !?] $ buildtest module -r /etc/modulefiles
    Removing module tree: /etc/modulefiles
    Configuration File: /home/siddis14/.buildtest/settings.yml has been updated

Configure Spider View
---------------------

Lmod ``spider`` retrieves module details in json format, buildtest is running
``spider -o spider-json $BUILDTEST_MODULEPATH`` to get all the modules. The
configuration ``BUILDTEST_SPIDER_VIEW`` can control the output. When ``BUILDTEST_SPIDER_VIEW=all``
then buildtest will retrieve all records including records for modules that
are not part of current ``MODULEPATH``.

If you want to restrict the search of module retrieval to those defined in ``BUILDTEST_MODULEPATH``
then set ``BUILDTEST_SPIDER_VIEW=current``. buildtest will only retrieve
records whose modulefile absolute path is a subdirectory of ``BUILDTEST_MODULEPATH``. When
``BUILDTEST_MODULEPATH`` is not set, it will take the value of
``MODULEPATH`` and setting ``BUILDTEST_SPIDER_VIEW=current`` can be useful
in testing modules that are visible to module environment.

Test Threshold
----------------

buildtest provides a mechanism to set a success threshold during test execution that
can be used to determine if your software passes or fails.

This can be set by using ``BUILDTEST_SUCCESS_THRESHOLD`` which is a value between ``[0.0-1.0]``
which will be used when running test.

::

    if success_threshold >= <passed tests>/< total tests>
        SUCCESS
    else
        FAIL

Here is an example test run where all test have passed and success threshold is 1.0

::

    $ buildtest run -s GCCcore/6.4.0
    Check Configuration
    ==============================================================
                             Test summary
    Application:  GCCcore/6.4.0
    Executed 32 tests
    Passed Tests: 32    Percentage: 100.0%
    Failed Tests: 0    Percentage: 0.0%
    SUCCESS: Threshold of 100.0% was achieved
    Writing results to /tmp/buildtest_10_26_30_01_2019.run

Force Purge Modules
--------------------------

buildtest will automatically run ``module purge`` before loading modules in test
script. This is to avoid unexpected behaviors when user shell has active modules
loaded that may affect the behavior of the test.

If you want to force purge the modules (i.e ``module --force purge``), then
set **BUILDTEST_MODULE_FORCE_PURGE=True**. By default, this
is set to **False**. This option is useful if you have sticky modules that
need to be removed prior to running test.