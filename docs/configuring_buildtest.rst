Configuring buildtest
_______________________

.. contents::
   :backlinks: none

Configuration File
--------------------

To configure buildtest you will need to create a YAML file at ``$HOME/.buildtest/settings.yml``.
This file is responsible for configuring  buildtest to work for your test system. Shown below is the
configuration file that can be found in the git repo.


**Configuration File**

::

    # root of buildtest-configs repo
    BUILDTEST_CONFIGS_REPO:

    # root of Ruby-buildtest-config repo
    BUILDTEST_RUBY_REPO:

    # root of R-buildtest-config repo
    BUILDTEST_R_REPO:

    #  root of Python-buildtest-config repo
    BUILDTEST_PYTHON_REPO:

    #  root of Perl-buildtest-config repo
    BUILDTEST_PERL_REPO:

    # Specify Module Naming Scheme for your module tree. Valid Options: [FNS, HMNS]
    BUILDTEST_MODULE_NAMING_SCHEME:

    # easybuild integration. Valid Options: [True, False]
    BUILDTEST_EASYBUILD: False
    # Delete Build Directory before writing tests.  Valid Options: [True, False]
    BUILDTEST_CLEAN_BUILD: False
    # enable support for job scripts. Valid Options: [True, False]
    BUILDTEST_ENABLE_JOB: False
    # OpenHPC integration. Valid options: [True, False]
    BUILDTEST_OHPC: False
    # binary test support. Valid options [True, False]
    BUILDTEST_BINARY: False
    # Configure shell when running test. Valid options [bash, csh, sh]. Default: [sh]
    BUILDTEST_SHELL: sh
    # Specify job template script to generate test
    BUILDTEST_JOB_TEMPLATE:
    # list root of module tree where modules are installed. Specify multiple module tree as a list
    BUILDTEST_MODULE_ROOT:
    # criteria for success threshold when running job. Valid Option: [0.0-1.0]
    BUILDTEST_SUCCESS_THRESHOLD: 0.90

    # directory where buildtest logs will be written.
    BUILDTEST_LOGDIR:
    # directory where test scripts will be generated
    BUILDTEST_TESTDIR:
    # directory where buildtest will write .run files
    BUILDTEST_RUN_DIR:


Variable Description
---------------------

.. include:: configuring_buildtest/buildtest-environment.txt


Adding a module tree
---------------------

``BUILDTEST_MODULE_ROOT`` colon separated list of root of a module tree in your system. buildtest will
read all module files and use this to figure out what modules can be tested.

Let's assume ``/opt/apps`` and ``/workspace/apps`` are root of the module tree,
so we can specify this in your configuration as follows

::

	BUILDTEST_MODULE_ROOT:
		- /opt/apps
		- /workspace/apps


If you want to set this as environment variable you can do the following

::

	export BUILDTEST_MODULE_ROOT=/opt/apps:/workspace/apps

If you set an invalid directory path in ``BUILDTEST_MODULE_ROOT`` you will get the following
message

.. Error::
    /opt/apps directory does not exist, specified in BUILDTEST_MODULE_ROOT
    /workspace/apps directory does not exist, specified in BUILDTEST_MODULE_ROOT


Configure Module Naming Scheme
-------------------------------

To configure the module naming scheme in buildtest you can set the variable ``BUILDTEST_MODULE_NAMING_SCHEME``
in your configuration file.

**Flat Naming Scheme** is when your module names are in format ``<APP>/<VERSION>-<TOOLCHAIN>`` and all modules are under
one tree.

**Hierarchical Module Naming Scheme** is when you have nested module trees where ``MODULEPATH`` is set in some module files (compiler, mpi).
Typically the module naming format is ``<APP>/<VERSION>``.

To set flat naming scheme you can set the following

::

	BUILDTEST_MODULE_NAMING_SCHEME: FNS



To set hierarchical module naming scheme you can set the following

::

	BUILDTEST_MODULE_NAMING_SCHEME: HMNS

The module naming scheme is assumed to be consistent across all module trees defined in ``BUILDTEST_MODULE_ROOT``

If you specify an invalid value for ``BUILDTEST_MODULE_NAMING_SCHEME`` you will get the following message

.. Error::
	BUILDTEST_MODULE_NAMING_SCHEME expects value ['HMNS', 'FNS'] current value is custom


Configure Shell
----------------

buildtest supports test creation for ``sh``, ``bash``, and ``csh``. The test are created
with the appropriate extension. The default shell is ``sh``.

To configure the shell use the variable ``BUILDTEST_SHELL`` in your configuration file

::

	BUILDTEST_SHELL: sh

To change the shell to ``bash`` or ```csh`` you can do either

::

	BUILDTEST_SHELL: bash
	BUILDTEST_SHELL: csh


If you specify an invalid value you may get the following message

.. Error::
	BUILDTEST_SHELL expects value ['sh', 'bash', 'csh'] current value is tcsh


Clean Build
-------------

buildtest will write test in ``BUILDTEST_TESTDIR``. Often times, you may want to preserve
tests across subsequent builds.

For instance you may be interested in building test for different shell and preserve all tests during the
previous builds, this can be done by setting ``BUILDTEST_CLEAN_BUILD`` as follows

::

    BUILDTEST_CLEAN_BUILD: False

Setting ``BUILDTEST_CLEAN_BUILD`` to ``False`` tells buildtest to preserve build directory
where test are written. This will allow user to keep test if they ran the following

::

        buildtest build -p gcc  --shell sh
        buildtest build -p gcc --shell csh
        buildtest build -p gcc --shell bash

If you want buildtest to delete the build directory before writing any tests you can set
BUILDTEST_CLEAN_BUILD to True as follows

::

        BUILDTEST_CLEAN_BUILD: True

Configure Test Directory
-------------------------

buildtest will write test scripts in ``BUILDTEST_TESTDIR``. This can be specified
in configuration file or environment variable.

Setting ``BUILDTEST_TESTDIR`` to ``/tmp/buildtest/tests`` can be done as follows

::

    BUILDTEST_TESTDIR: /tmp/buildtest/tests

If the directory does not exist, buildtest will create it assuming you have the appropriate
permissions.

You may specify this at the command line via ``--testdir``

See example below where tests are written to ``/tmp/buildtest/tests``

::

    (buildtest) [siddis14@gorgon buildtest-framework]$ buildtest build -s GCCcore/6.4.0
    Check Configuration
    Creating Log directory:  /tmp/buildtest/logs
    Detecting Software:  GCCcore/6.4.0
    --------------------------------------------
    [STAGE 1]: Building Binary Tests
    --------------------------------------------
    Detecting Test Type: Software
    Processing Binary YAML configuration:  /home/siddis14/github/buildtest-configs/buildtest/ebapps/gcccore/6.4.0/command.yaml
    Generating  10  binary tests
    Binary Tests are written in  /tmp/buildtest/tests/ebapp/GCCcore/6.4.0/
    --------------------------------------------
    [STAGE 2]: Building Source Tests
    --------------------------------------------
    Processing all YAML files in directory:  /home/siddis14/github/buildtest-configs/buildtest/source/gcccore/config
    Generating 22  Source Tests and writing at  /tmp/buildtest/tests/ebapp/GCCcore/6.4.0/
    Writing Log file:  /tmp/buildtest/logs/GCCcore/6.4.0/buildtest_21_20_20_01_2019.log


Log Directory
----------------

buildtest will write the logs specified by ``BUILDTEST_LOGDIR`` this can be set at the
configuration file or environment variable.

Setting this at the configuration file can be done as follows

::

        BUILDTEST_LOGDIR: /tmp/buildtest/logs


Once this is set you will find a log file per execution. For instance, if you build
tests for ``GCCcore/6.4.0``, you will find the logs in the following path

::

    /tmp/buildtest/logs/GCCcore/6.4.0/

All log files are named as follows ``buildtest_HH_MM_DD_MM_YYYY.log`` to preserve the
date and time stamp.

Here is an example for a buildtest log file from Jan 20th 2019

::

    (buildtest) [siddis14@gorgon buildtest-framework]$ ls -l /tmp/buildtest/logs/GCCcore/6.4.0/buildtest_21_20_20_01_2019.log
    -rw-r--r-- 1 siddis14 amer 81358 Jan 20 21:20 /tmp/buildtest/logs/GCCcore/6.4.0/buildtest_21_20_20_01_2019.log

Easybuild Check
----------------

To enable easybuild check on module files you can set ``BUILDTEST_EASYBUILD`` as follows

::

    BUILDTEST_EASYBUILD: True

The default mode to disable easybuild check

For more details on easybuild integration check out  :ref:`EasyBuild_Integration`

OpenHPC Integration
--------------------

If you want to build software for OpenHPC software stack you can set the following in your
configuration file

::

    BUILDTEST_OHPC: True

For more details check out :ref:`OHPC_Integration`

Job Integration
----------------

buildtest can support job script creation so you can submit tests to your batch scheduler.
To enable this feature you will need to set ``BUILDTEST_ENABLE_JOB``

::

    BUILDTEST_ENABLE_JOB: True

By default this is disabled.



When set this will automatically create job scripts based on the variable ``BUILDTEST_JOB_TEMPLATE``
along with the test scripts in the same directory.

BUILDTEST_JOB_TEMPLATE can be set at configuration file or as environment variable. buildtest will
check if file exists and if it contains a valid extension. You may get the following message if you specify
an invalid extension

.. Error::
    Invalid File extension .slurm1 must be one of the following extension['.lsf', '.slurm', '.pbs']


For more information check out :ref:`Job_Template`

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

    (siddis14-TgVBs13r) buildtest-framework[master !x?] $ buildtest run -s GCCcore/6.4.0
    Check Configuration
    ==============================================================
                             Test summary
    Application:  GCCcore/6.4.0
    Executed 32 tests
    Passed Tests: 32    Percentage: 100.0%
    Failed Tests: 0    Percentage: 0.0%
    SUCCESS: Threshold of 100.0% was achieved
    Writing results to /tmp/buildtest_10_26_30_01_2019.run
