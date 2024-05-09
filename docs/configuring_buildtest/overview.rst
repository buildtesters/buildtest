Configuring Buildtest
=======================

We assume you are familiar with general concepts presented in :ref:`getting started <getting_started>` and your next
step is to configure buildtest to run at your site. This guide will present you the necessary steps to get
you started.

When you clone buildtest, we provide a :ref:`default configuration <default_configuration>`
that can be used to run on your laptop or workstation that supports Linux or Mac. The
buildtest configuration uses a JSON schemafile `settings.schema.json <https://raw.githubusercontent.com/buildtesters/buildtest/devel/buildtest/schemas/settings.schema.json>`_.
for validating your configuration.

.. _which_configuration_file_buildtest_reads:

Which configuration file does buildtest read?
------------------------------------------------

buildtest will read configuration files in the following order:

1. Command line ``buildtest -c <config>.yml build``
2. Environment variable - **BUILDTEST_CONFIGFILE**
3. User Configuration - ``$HOME/.buildtest/config.yml``
4. Default Configuration - ``$BUILDTEST_ROOT/buildtest/settings/config.yml``

.. _default_configuration:

Default Configuration
-----------------------

Buildtest comes with a default configuration  that can be found at `buildtest/settings/config.yml <https://raw.githubusercontent.com/buildtesters/buildtest/devel/buildtest/settings/config.yml>`_
relative to root of repo. At the start of buildtest execution, buildtest will load
the configuration file and validate the configuration with JSON schema ``settings.schema.json``.
If it's fails to validate, buildtest will raise an error.

We recommend you copy the default configuration as a template to configure buildtest for your site.

Shown below is the default configuration provided by buildtest.

.. literalinclude:: ../../buildtest/settings/config.yml
   :language: yaml

As you can see the layout of configuration starts with keyword ``system`` which is
used to define one or more systems. Your HPC site may contain more than one cluster,
so you should define your clusters with meaningful names as this will impact when you
reference :ref:`executors <configuring_executors>` in buildspecs. In this example, we define one
cluster called ``generic`` which is a dummy cluster used for running tutorial examples.

.. _config_hostnames:

Hostnames
-----------

The ``hostnames`` field is a list of nodes that belong to the cluster where buildtest should be run. Generally,
these hosts should be your login nodes in your cluster. buildtest will process **hostnames** field across
all system entry using `re.fullmatch <https://docs.python.org/3/library/re.html#re.fullmatch>`_ until a hostname is found, if
none is found we report an error.


In this example we defined two systems `machine`, `machine2` with the following hostnames.

.. code-block:: yaml
    :emphasize-lines: 1-5

    system:
      machine1:
        hostnames:  ['loca$', '^1DOE']
      machine2:
        hostnames: ['BOB|JOHN']

In this example, none of the host entries match with hostname **DOE-7086392.local** so we get an error
since buildtest needs to detect a system before proceeding.

.. code-block:: shell

      buildtest.exceptions.BuildTestError: "Based on current system hostname: DOE-7086392.local we cannot find a matching system  ['machine1', 'machine2'] based on current hostnames: {'machine1': ['loca$', '^1DOE'], 'machine2': ['BOB|JOHN']} "


Let's assume you we have a system named ``mycluster`` that should  run on nodes ``login1``, ``login2``, and ``login3``.
You can specify hostnames as a list of strings

.. code-block:: yaml

    system:
      mycluster:
        hostnames: ["login1", "login2", "login3"]

Alternately, you can use regular expression to condense this list

.. code-block:: yaml

    system:
      mycluster:
        hostnames: ["login[1-3]"]

.. _module_configuration:

Module Tool
------------

If your system supports `environment-modules <https://modules.readthedocs.io/en/latest/>`_ or
`Lmod <https://lmod.readthedocs.io/en/latest/index.html>`_ for managing user environment then you can
configure buildtest to use the module tool. This can be defined via ``moduletool`` property.

.. code-block:: yaml

    # environment-modules
    moduletool: environment-modules

    # for lmod
    moduletool: lmod

    # specify N/A if you don't have modules
    moduletool: N/A


The `moduletool` property is used for :ref:`detecting compilers <detect_compilers>` when you run ``buildtest config compilers find``.

Test directory
---------------

The default location where tests are written is **$BUILDTEST_ROOT/var/tests** where
$BUILDTEST_ROOT is the root of buildtest repo. You may specify ``testdir`` in your
configuration to instruct where tests can be written. For instance, if
you want to write tests in **/tmp** you can set the following:

.. code-block:: yaml

    testdir: /tmp

Alternately, one can specify test directory via ``buildtest build --testdir <path>`` which
has highest precedence and overrides configuration and default value.

Log Path
---------

You can configure where buildtest will write logs using ``logdir`` property. For
example, in example below buildtest will write log files ``$HOME/Documents/buildtest/var/logs``.
buildtest will resolve variable expansion to get real path on filesystem.


.. code-block:: yaml

    # location of log directory
    logdir: $HOME/Documents/buildtest/var/logs


``logdir`` is not required field in configuration, if it's not specified then buildtest will write logs
based on `tempfile <https://docs.python.org/3/library/tempfile.html>`_ library which may vary
based on platform (Linux, Mac).

The buildtest logs will start with **buildtest_** followed by random identifier with
a **.log** extension.

Specify directory paths to search for binaries
----------------------------------------------

The ``paths`` property can be used to search for binaries for batch schedulers. If your scheduler binaries
are installed in a non-standard location that is not in $PATH, you can use this to specify the directory path.

In example below we will, we will specify directories for SLURM, LSF, PBS and TORQUE binaries that
are not in $PATH and installed in `/usr/local/slurm/bin`, `/usr/local/lsf/bin`,
`/usr/local/pbs/bin`, `/usr/local/torque/bin` respectively.

.. code-block:: yaml

    paths:
      slurm: /usr/local/slurm/bin
      lsf: /usr/local/lsf/bin
      pbs: /usr/local/pbs/bin
      torque: /usr/local/torque/bin


Buildspec Cache
----------------

The :ref:`buildtest buildspec find <find_buildspecs>` command can be configured using the configuration file to provide sensible
defaults. This can be shown in the configuration file below:

.. code-block:: yaml

        buildspecs:
          # whether to rebuild cache file automatically when running `buildtest buildspec find`
          rebuild: False
          # limit number of records to display when running `buildtest buildspec find`
          count: 15
          # format fields to display when running `buildtest buildspec find`, By default we will show name,description
          format: "name,description"
          # enable terse mode
          terse: False
          # specify list of directories to search for buildspecs when building cache
          #root: [ $BUILDTEST_ROOT/examples, /tmp/buildspecs ]


The ``rebuild: False`` means buildtest won't rebuild the buildcache every time you run ``buildtest buildspec find``. If the
cache file is not present, it will automatically rebuild the cache, otherwise it will build the cache if one specifies
``--rebuild`` option or ``rebuild: True`` is set in the configuration file.

The buildspec cache is built by reading the contents of the buildspec file on the filesystem; therefore if you make changes
to the buildspecs then you will need to rebuild the buildspec cache by running ``buildtest buildspec find --rebuild``.
If you want buildtest to always rebuild cache you can set the following in your configuration file

.. code-block:: yaml

    buildspecs:
      rebuild: True

The configuration options such as ``count``, ``format``, ``terse`` can  be tweaked to your preference. These configuration values
can be overridden by command line option.

.. _buildspec_roots:

Specify Root Directories for searching buildspecs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Buildtest will search for buildspecs by recursively searching for files with **.yml** extension. The ``root`` property in configuration file
is a list of string types which is used to search for buildspecs. The ``root`` property is not required in configuration file, but it can be a good
idea to set this value if you have a predetermined location where buildspecs are stored.

You can specify the root path via command line ``buildtest buildspec find --root <dir1> --root <dir2>`` which will override the configuration value. In a
practical situation, you will want to write your buildspecs in a separate repository which you can clone in your filesystem. Let's say they are cloned in
your $HOME directory named **$HOME/buildtest-examples**. You have one of two options, one you can specify the root path in configuration file as shown below:

.. code-block:: yaml

    buildspecs:
      root: [ $HOME/buildtest-examples ]

This above configuration will instruct buildtest to search for buildspecs in ``$HOME/buildtest-examples`` directory, and you won't
have to specify the ``--root`` option when running ``buildtest buildspec find``. The second option would be to specify the ``--root`` everytime
you need to build the cache. If neither is specified, buildtest will load the default buildspecs which are **$BUILDTEST_ROOT/tutorials** and
**$BUILDTEST_ROOT/general_tests**.

.. _configuring_buildtest_report:

Configuring buildtest report
-----------------------------

The ``report`` section in configuration file allows you to configure behavior of ``buildtest report`` command. The
``report`` section is shown below:

.. code-block:: yaml

    report:
      count: 25
      #enable terse mode for report
      terse: False
      format: "name,id,state,runtime,returncode"


The ``count`` property limits the number of records to display when running ``buildtest report`` command. The ``format`` property
controls the fields to display when running ``buildtest report``. The ``terse`` property enables terse mode for ``buildtest report``.

.. _cdash_configuration:

CDASH Configuration
--------------------

buildtest can be configured to push test to `CDASH <https://www.cdash.org/>`_. The default configuration
file provides a CDASH configuration for buildtest project is the following.

.. code-block:: yaml

    cdash:
      url: https://my.cdash.org/
      project: buildtest
      site: generic
      buildname: tutorials

The cdash section can be summarized as follows:

 - ``url``: URL to CDASH server

 - ``project``: Project Name in CDASH server

 - ``site``: Site name that shows up in CDASH entry. This should be name of your system name

 - ``buildname``: Build Name that shows up in CDASH, this can be any name you want.

The cdash settings can be used with ``buildtest cdash`` command. For more details
see :ref:`cdash_integration`.

Test Timeout
-------------

The ``timeout`` property is number of seconds a test can run before it is called. **The timeout property must be a positive integer**.
For instance if you want all test to timeout within 60 sec you can do the following

.. code-block:: yaml

    timeout: 60

The ``timeout`` field is not set by default, it can be configured in the configuration file but can be overridden via command line
option ``buildtest build --timeout``. For more details see :ref:`test_timeout`

Pool Size
-----------

buildtest makes use of `multiprocessing.Pool <https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool>`_ which is used
to control pool size for worker processes used for processing builders during run phase. We can use the ``poolsize`` property
to control the size of pool. The pool size must be 1 or higher, if value exceeds maximum CPU count (i.e. `os.cpu_count() <https://docs.python.org/3/library/os.html#os.cpu_count>`_)
then value is set to maximum CPU count.

Shown below we set ``poolsize`` to 1.


.. code-block:: yaml
    :emphasize-lines: 14

    system:
      generic:
        # specify list of hostnames where buildtest can run for given system record
        hostnames: [".*"]

        # system description
        description: Generic System
        # specify module system used at your site (environment-modules, lmod)
        moduletool: N/A

        # specify test timeout duration in number of seconds
        # timeout: 60

        poolsize: 1

.. _configuring_max_jobs:

Maximum Jobs
--------------

The ``max_jobs`` property is used to limit number of jobs that can run concurrently. This is useful if you want to limit,
the workload on your system. Buildtest will run all jobs in parallel by default, if ``max_jobs`` is not specified.
If you want to run all tests in serial, you can set ``max_jobs: 1`` as shown below.

.. code-block:: yaml

    max_jobs: 1

This value can be overridden via ``buildtest build --max-jobs`` option. For more details see :ref:`limit_max_jobs`

Managing Profiles
------------------

The ``profile`` section allows you to define build profiles that can be used to encapsulate ``buildtest build`` options.
This section is auto-generated when using ``buildtest build --save-profile`` option, see :ref:`using_profiles` for more details.

Shown below is an example profile, the ``python-tests`` is the name of the profile. The ``tags`` property is a list of tags to use
which are used by ``buildtest build --tags`` option. The ``testdir`` option is the path where tests are written that is used by ``buildtest build --testdir``.

.. code-block:: yaml
    :emphasize-lines: 2-5

    profiles:
      python-tests:
        tags:
        - python
        testdir: /Users/siddiq90/Documents/github/buildtest/var/tests


The profile can be configured with many other options supported by ``buildtest build``, shown below are additional examples.
Configuration properties like ``rebuild``, ``limit``, ``timeout`` are integer and must be positive numbers.

.. code-block:: yaml
   :emphasize-lines: 13-15

    profiles:
      profile-2:
        buildspecs:
        - /Users/siddiq90/Documents/github/buildtest/tutorials/job_dependency
        exclude-buildspecs:
        - tutorials/job_dependency/ex1.yml
        tags:
        - python
        exclude-tags:
        - network
        executors:
        - generic.local.csh
        rebuild: 2
        limit: 10
        timeout: 10
        account: dev
        procs:
        - 2
        - 4
        nodes:
        - 1
        - 2
        testdir: /Users/siddiq90/Documents/github/buildtest/var/tests
        executor-type: local

Shown below is a generated profile using
``buildtest build -b tutorials --filter "tags=pass;maintainers=@shahzebsiddiqui;type=script" --save-profile=filter_profile``. The ``filter``
is an object and attributes ``tags``, ``maintainers``, ``type`` correspond to the filter fields.

.. code-block:: yaml
   :emphasize-lines: 6-12

    profiles:
      filter_profile:
        buildspecs:
        - /Users/siddiq90/Documents/github/buildtest/tutorials
        testdir: /Users/siddiq90/Documents/github/buildtest/var/tests
        filter:
          tags:
          - pass
          maintainers:
          - '@shahzebsiddiqui'
          type:
          - script

We have added additional checks in the JSON schema for valid values for each type, for instance if you specify an invalid value for ``type`` field
which is used to filter buildspecs by the ``type`` field, then you will get an invalid configuration file.


Listing Profiles
~~~~~~~~~~~~~~~~~

This section in the profile permits you to enumerate the profiles available for encapsulating buildtest build options.

Lets create a profile by running the following buildtest command.

.. command-output:: buildtest build -t python --save-profile=python

The `--save-profile` is used to specify name of profile that will be written in configuration file.

In order to see all profiles you can run ``buildtest config profiles list`` as shown below

.. command-output:: buildtest config profiles list

.. command-output:: buildtest config profiles list --yaml

Removing Profiles
~~~~~~~~~~~~~~~~~~

You can remove a profile by running ``buildtest config profiles remove <profile>``, where <profile> is the name of profile.

This command will update your configuration file and remove the profile name from configuration. You can
remove multiple profiles at once, buildtest will check if profile name exist and attempt to remove it. If its not
found, it will simply skip it.

First, lets create two profile using ``buildtest build --save-profile``

.. dropdown:: Creating profiles

    .. command-output:: buildtest build -t python --save-profile=prof1

    .. command-output:: buildtest build -b tutorials/shell_examples.yml  --save-profile=prof2

Now we will list the profiles to confirm they are created and remove them. Next we will rerun ``buildtest config profiles list`` to confirm
profiles are removed

.. dropdown:: Example on how to remove profiles

    .. code-block:: console

        $ buildtest config profiles list
        python-tests
        python
        prof1
        prof2

    .. code-block:: console

        $ buildtest config profiles remove prof1 prof2
        Removing profile: prof1
        Removing profile: prof2
        Updating configuration file: /Users/siddiq90/Documents/github/buildtest/buildtest/settings/config.yml

    .. code-block:: console

        $ buildtest config profiles list
        python-tests
        python