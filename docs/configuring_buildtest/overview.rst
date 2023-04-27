Overview
=========

We assume you are familiar with general concepts presented in :ref:`getting started <getting_started>` and your next
step is to configure buildtest to run at your site. This guide will present you the necessary steps to get
you started.

When you clone buildtest, we provide a :ref:`default configuration <default_configuration>`
that can be used to run on your laptop or workstation that supports Linux or Mac. The
buildtest configuration uses a JSON schemafile `settings.schema.json <https://raw.githubusercontent.com/buildtesters/buildtest/devel/buildtest/schemas/settings.schema.json>`_.
for validating your configuration. We have published the schema guide for settings schema which
you can find `here <https://buildtesters.github.io/buildtest/pages/schemadocs/settings.html>`_.

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
cluster called ``generic`` which is a dummy cluster used for running tutorial examples. The
**required** fields in the system scope are the following::

    "required": ["executors", "moduletool", "hostnames", "compilers"]

.. _config_hostnames:

Configuring Hostnames
----------------------

The ``hostnames`` field is a list of nodes that belong to the cluster where buildtest should be run. Generally,
these hosts should be your login nodes in your cluster. buildtest will process **hostnames** field across
all system entry using `re.match <https://docs.python.org/3/library/re.html#re.match>`_ until a hostname is found, if
none is found we report an error.


In this example we defined two systems `machine`, `machine2` with the following hostnames.

.. code-block:: yaml

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

Configuring Module Tool
------------------------

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

.. _configuring_executors:

Configuring Executors
----------------------

An executor is responsible for running the test and capture output/error file and
return code. An executor can be local executor which runs tests on local machine or
batch executor that can be modelled as partition/queue. A batch executor is
responsible for **dispatching** job, then **poll** job until its finish, and
**gather** job metrics from scheduler.

Executor Declaration
~~~~~~~~~~~~~~~~~~~~~~

The ``executors`` is a JSON `object`, that defines one or more executors. The executors
are grouped by their type followed by executor name. In this example we define two
local executors ``bash``, ``sh`` and one slurm executor called ``regular``:

.. code-block:: yaml

  system:
    generic:
      executors:
        local:
          bash:
            shell: bash
            description: bash shell
          sh:
            shell: sh
            description: sh shell
        slurm:
          regular:
            queue: regular

The **LocalExecutors** are defined in section `local` where each executor must be
unique name and they are referenced in buildspec using ``executor`` field in the following format:

.. code-block:: yaml

    executor: <system>.<type>.<name>

For instance, if a buildspec wants to reference the LocalExecutor `bash` from the `generic`
cluster, you would specify the following in the buildspec:

.. code-block:: yaml

     executor: generic.local.bash

In our example configuration, we defined a ``bash`` executor as follows:

.. code-block:: yaml

    executors:
      # define local executors for running jobs locally
      local:
        bash:
          description: submit jobs on local machine using bash shell
          shell: bash

The local executors require the ``shell`` key which is one of supported shells in your system. On Linux/Mac system
you can find all supported shells in file `/etc/shells`. Any buildspec that references this executor will submit
job using ``bash`` shell.

You can pass options to shell which will get passed into each job submission.
For instance if you want all bash scripts to run in login shell you can specify ``bash --login``:

.. code-block:: yaml

    executors:
      local:
        login_bash:
          shell: bash --login

Then you can reference this executor as ``executor: generic.local.login_bash`` and your
tests will be submitted via ``bash --login /path/to/test.sh``.

Once you define your executors, you can :ref:`query the executors <view_executors>` via ``buildtest config executors``
command.

Disable an executor
~~~~~~~~~~~~~~~~~~~~

buildtest will run checks for every executor instance depending on the executor type, for instance
local executors such as `bash`, `sh`, `csh` executor will be checked to see if shell is
valid by checking the path. If shell doesn't exist, buildtest will raise an error. You
can circumvent this issue by disabling the executor via ``disable`` property. A disabled executor won't
serve any jobs which means any buildspec that reference the executor won't create a test.

In this next example the executor `zsh` is disabled which can be used if you don't have **zsh** on your system

.. code-block:: yaml
   :emphasize-lines: 5

    executors:
      local:
        zsh:
          shell: zsh
          disable: true

Default commands run per executors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can configure an executor to run a set of commands when using an executor. We
can do this via ``before_script`` field that is a string type that can be used to specify
shell commands.

In this example below we have a bash executor will define some shell code that will be run when
using this executor. The content of the `before_script` will be inserted in a shell script that is sourced
by all tests.

.. code-block:: yaml

      local:
        bash:
          description: submit jobs on local machine using bash shell
          shell: bash
          before_script: |
            today=$(date "+%D")
            echo "Today is $today, running test with user: $(whoami)"

buildtest will write a ``before_script.sh`` for every executor.
This can be found in ``$BUILDTEST_ROOT/var/executors`` directory as shown below

.. code-block:: console

    $ find $BUILDTEST_ROOT/var/executor -type f
    /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/executor/generic.local.bash/before_script.sh
    /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/executor/generic.local.csh/before_script.sh
    /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/executor/generic.local.zsh/before_script.sh
    /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/executor/generic.local.sh/before_script.sh


If you run a test using this executor you will see the code is inserted from `before_script.sh` which is sourced
for all given test.

.. code-block:: console

    $ cat  $BUILDTEST_ROOT/var/executor/generic.local.bash/before_script.sh
    #!/bin/bash
    today=$(date "+%D")
    echo "Today is $today, running test with user: $(whoami)"


Specifying Modules
~~~~~~~~~~~~~~~~~~~~

You can configure executors to load modules, purge or restore from collection which will be run for all tests that use the executor.
This can be achieved via ``module`` property that can be defined in the executor definition. In this next example, we create a bash executor
that will purge modules and load gcc. The ``purge`` property is a boolean, if set to **True** we will run **module purge** before
loading commands. The ``load`` property is a list of modules to **module load**.

.. code-block:: yaml

    executors:
      local:
        bash:
          shell: bash
          module:
            purge: True
            load: ["gcc"]

.. _slurm_executors:

Specifying QoS (Slurm)
~~~~~~~~~~~~~~~~~~~~~~~~

At Cori, jobs are submitted via qos instead of partition so we model a slurm executor
named by qos. The ``qos`` field instructs which Slurm QOS to use when submitting job. For
example we defined a slurm executor named **haswell_debug** which will submit jobs to **debug**
qos on the haswell partition as follows:

.. code-block:: yaml
   :emphasize-lines: 4

    executors:
      slurm:
        haswell_debug:
          qos: debug
          cluster: cori
          options: ["-C haswell"]

The ``cluster`` field specifies which slurm cluster to use
(i.e ``sbatch --clusters=<string>``).

buildtest will detect slurm configuration and check qos, partition, cluster
match with buildtest configuration. In addition, buildtest supports multi-cluster
job submission and monitoring from remote cluster. This means if you specify
``cluster`` field buildtest will poll jobs using `sacct` with the
cluster name as follows: ``sacct -M <cluster>``.

The ``options`` field is use to specify any additional options to launcher (``sbatch``)
on command line. Any additional **#SBATCH** options are defined in buildspec for more details see
:ref:`batch scheduler support <batch_support>`.

Specify Slurm Partitions
~~~~~~~~~~~~~~~~~~~~~~~~~~

You can specify slurm partitions instead of qos if your slurm cluster requires jobs to be submitted by partitions. This
can be done via ``partition`` property. In this next example we define an executor name `regular_hsw` which maps
to slurm partition **regular_hsw**.

.. code-block:: yaml
   :emphasize-lines: 4

    executors:
      slurm:
        regular_hsw:
          partition: regular_hsw
          description: regular haswell queue

buildtest will check if slurm partition is in ``up`` state before adding executor. buildtest will be
performing these checks when validating configuration file and this avoids creating tests that reference
a partition that is in **down** state. Internally, we are running the following command for every defined
defined partition

.. code-block:: console

    $ sinfo -p regular_hsw -h -O available
    up

.. _project_account:

Specifying Project Account
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Batch jobs require project account to charge jobs and depending on your site this could
be required in order to submit job. Some scheduler like Slurm can detect your default project account
in that case you don't need to specify on command line.

In your configuration file you can specify ``account`` property which will inherit this
setting for all executors. You can specify ``account`` property within an executor which will override the
default section.

In this example, we have two pbs executors **testing** and **development**. All pbs jobs will use the project account ``development``
because this is defined in ``defaults`` section however we can force all jobs using **testing** executor to charge
jobs to ``qa_test``.

.. code-block:: yaml
   :emphasize-lines: 5,9

    executors:
      defaults:
        pollinterval: 10
        maxpendtime: 90
        account: development
      pbs:
       testing:
         queue: test
         account: qa_test
       development:
         queue: dev

Alternately, you can override configuration setting via ``buildtest build --account`` command which will be applied
for all batch jobs.

Poll Interval
~~~~~~~~~~~~~~

The ``pollinterval`` field is used  to poll jobs at set interval in seconds
when job is active in queue. The poll interval can be configured on command line
using ``buildtest build --pollinterval`` which overrides the configuration value.

.. Note::

    ``pollinterval``  and ``maxpendtime`` have no effect on local executors.


Max Pend Time
~~~~~~~~~~~~~~

The ``maxpendtime`` is **maximum** time job can be pending
within an executor, if it exceeds the limit buildtest will cancel the job.

The **maxpendtime** option can be overridden per executor level for example the
section below overrides the default to 300 seconds:

.. code-block:: yaml
    :emphasize-lines: 5

        bigmem:
          description: bigmem jobs
          cluster: escori
          qos: bigmem
          maxpendtime: 300

The ``maxpendtime`` is used to cancel job only if job is pending in queue, it has
no impact if job is running. buildtest starts a timer at job submission and every poll interval
(``pollinterval`` field) checks if job has exceeded **maxpendtime** only if job is pending.
If job pendtime exceeds `maxpendtime` limit, buildtest will
cancel job the job using the appropriate scheduler command like (``scancel``, ``bkill``, ``qdel``).
Buildtestwill remove cancelled jobs from poll queue, in addition cancelled jobs won't be
reported in test report.

For more details on `maxpendtime` click :ref:`here <max_pend_time>`.

.. _pbs_executors:

PBS Executors
~~~~~~~~~~~~~~

.. Note:: buildtest PBS support relies on job history set because buildtest needs to query job after completion using ``qstat -x``. This
          can be configured using ``qmgr`` by setting ``set server job_history_enable=True``. For more details see section **14.15.5.1 Enabling Job History** in `PBS 2021.1.3 Admin Guide <https://help.altair.com/2021.1.3/PBS%20Professional/PBSAdminGuide2021.1.3.pdf>`_


buildtest supports `PBS <https://community.altair.com/community?id=altair_product_documentation>`_ scheduler
which can be defined in the ``executors`` section. Shown below is an example configuration using
one ``pbs`` executor named ``workq``.  The property ``queue: workq`` defines
the name of PBS queue that is available in your system.

.. code-block:: yaml
    :linenos:
    :emphasize-lines: 10-12

    system:
      generic:
        hostnames: ['.*']

        moduletool: N/A
        executors:
          defaults:
             pollinterval: 10
             max_pend_time: 30
          pbs:
            workq:
              queue: workq
        compilers:
          compiler:
            gcc:
              default:
                cc: /usr/bin/gcc
                cxx: /usr/bin/g++
                fc: /usr/bin/gfortran

buildtest will detect the PBS queues in your system and determine if queues are active
and enabled before submitting job to scheduler. buildtest will run ``qstat -Q -f -F json`` command to check for
queue state which reports in JSON format and check if queue has the fields ``enabled: "True"`` or ``started: "True"`` set
in the queue definition. If these values are not set, buildtest will raise an exception.

Shown below is an example with one queue **workq** that is ``enabled`` and ``started``.

.. code-block:: console
    :emphasize-lines: 6-7, 17-18
    :linenos:

    $ qstat -Q -f -F json
    {
        "timestamp":1615924938,
        "pbs_version":"19.0.0",
        "pbs_server":"pbs",
        "Queue":{
            "workq":{
                "queue_type":"Execution",
                "total_jobs":0,
                "state_count":"Transit:0 Queued:0 Held:0 Waiting:0 Running:0 Exiting:0 Begun:0 ",
                "resources_assigned":{
                    "mem":"0kb",
                    "ncpus":0,
                    "nodect":0
                },
                "hasnodes":"True",
                "enabled":"True",
                "started":"True"
            }
        }
    }

Configuring test directory
---------------------------

The default location where tests are written is **$BUILDTEST_ROOT/var/tests** where
$BUILDTEST_ROOT is the root of buildtest repo. You may specify ``testdir`` in your
configuration to instruct where tests can be written. For instance, if
you want to write tests in **/tmp** you can set the following::

    testdir: /tmp

Alternately, one can specify test directory via ``buildtest build --testdir <path>`` which
has highest precedence and overrides configuration and default value.

Configuring log path
----------------------

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

Configuring Buildspec Cache
----------------------------

The :ref:`buildtest buildspec find <find_buildspecs>`_ command can be configured using the configuration file to provide sensible
defaults. This can be shown in the configuration file below:

.. code-block::

    :language: yaml

        buildspecs:
          # whether to rebuild cache file automatically when running `buildtest buildspec find`
          rebuild: False
          # limit number of records to display when running `buildtest buildspec find`
          count: 15
          # format fields to display when running `buildtest buildspec find`, By default we will show name,description
          formatfields: "name,description"
          # enable terse mode
          terse: False
          # determine whether to enable pagination
          pager: False

Each configuration can be overridden by command line option. For instance, the default behavior for pagination is disabled
with ``pager: False`` but if you want to enable pagination you can run ``buildtest buildspec find --pager``.

.. _buildspec_roots:

buildspec roots
-----------------

buildtest can discover buildspec using ``buildspec_roots`` keyword. This field is a list
of directory paths to search for buildspecs. For example we clone the repo
https://github.com/buildtesters/buildtest-nersc at **$HOME/buildtest-nersc** and assign
this to **buildspec_roots** as follows:

.. code-block:: yaml

    buildspec_roots:
      - $HOME/buildtest-nersc

This field is used with the ``buildtest buildspec find`` command. If you rebuild
your buildspec cache via ``--rebuild`` option, buildtest will search for all buildspecs in
directories specified by **buildspec_roots** property. buildtest will recursively
find all **.yml** extension and validate each buildspec with appropriate schema.

By default buildtest will add the ``$BUILDTEST_ROOT/tutorials`` and ``$BUILDTEST_ROOT/general_tests``
to search path when searching for buildspecs with ``buildtest buildspec find`` command. This
is only true if there is no root buildspec directory specified which can be done via `buildspec_roots`
or `--root` option.


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

Configuring Test Timeout
-------------------------

The ``timeout`` property is number of seconds a test can run before it is called. **The timeout property must be a positive integer**.
For instance if you want all test to timeout within 60 sec you can do the following

.. code-block:: yaml

    timeout: 60

The ``timeout`` field is not set by default, it can be configured in the configuration file but can be overridden via command line
option ``buildtest build --timeout``. For more details see :ref:`test_timeout`

Configuring Pool Size
----------------------

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
