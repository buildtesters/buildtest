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

- Command line ``buildtest -c <config>.yml build``
- User Configuration - ``$HOME/.buildtest/config.yml``
- Default Configuration - ``$BUILDTEST_ROOT/buildtest/settings/config.yml``

.. _default_configuration:

Default Configuration
-----------------------

Buildtest comes with a default configuration  that can be found at `buildtest/settings/config.yml <https://raw.githubusercontent.com/buildtesters/buildtest/devel/buildtest/settings/config.yml>`_
relative to root of repo. At the start of buildtest execution, buildtest will load
the configuration file and validate the configuration with JSON schema ``settings.schema.json``.
If it's fails to validate, buildtest will raise an error.

We recommend you copy the default configuration as a template to configure buildtest for your site. To get
started you should copy the file in ``$HOME/.buildtest/config.yml``. Please
run the following command::

    $ cp $BUILDTEST_ROOT/buildtest/settings/config.yml $HOME/.buildtest/config.yml

Shown below is the default configuration provided by buildtest.

.. command-output:: cat $BUILDTEST_ROOT/buildtest/settings/config.yml
   :shell:

As you can see the layout of configuration starts with keyword ``system`` which is
used to define one or more systems. Your HPC site may contain more than one cluster,
so you should define your clusters with meaningful names as this will impact when you
reference :ref:`executors <configuring_executors>` in buildspecs. In this example, we define one
cluster called ``generic`` which is a dummy cluster used for running tutorial examples. The
**required** fields in the system scope are the following::

    "required": ["executors", "moduletool", "load_default_buildspecs","hostnames", "compilers"]

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

In this example, none of the host entries match with hostname `DOE-7086392.local` so we get an error
since buildtest needs to detect a system before proceeding.

.. code-block:: shell

      buildtest.exceptions.BuildTestError: "Based on current system hostname: DOE-7086392.local we cannot find a matching system  ['machine1', 'machine2'] based on current hostnames: {'machine1': ['loca$', '^1DOE'], 'machine2': ['BOB|JOHN']} "


Let's assume you we have a system named ``mycluster`` that should  run on nodes ``login1``, ``login2``, and ``login3``.
You can specify hostnames as follows.

.. code-block:: yaml

    system:
      mycluster:
        hostnames: ["login1", "login2", "login3"]

Alternately, you can use regular expression to condense this list

.. code-block:: yaml

    system:
      mycluster:
        hostnames: ["login[1-3]"]

If your system supports module-system (`environment-modules <https://modules.readthedocs.io/en/latest/>`_ or `Lmod <Mhttps://lmod.readthedocs.io/en/latest/index.html>`_) you
will need to define the ``moduletool`` property. For more details see :ref:`configuring module tool <module_configuration>`. The
``load_default_buildspecs`` is a boolean value that determines if buildtest will load the default
buildspecs into buildspec cache via ``buildtest buildspec find`` command. To configure this property see :ref:`load default buildspecs <load_default_buildspecs>`.


.. _module_configuration:

Configuring Module Tool
------------------------

You should configure the ``moduletool`` property to the module-system installed
at your site. Valid options are the following:

.. code-block:: yaml

    # environment-modules
    moduletool: environment-modules

    # for lmod
    moduletool: lmod

    # specify N/A if you don't have modules
    moduletool: N/A


.. _buildspec_roots:

buildspec roots
-----------------

buildtest can discover buildspec using ``buildspec_roots`` keyword. This field is a list
of directory paths to search for buildspecs. For example we clone the repo
https://github.com/buildtesters/buildtest-cori at **$HOME/buildtest-cori** and assign
this to **buildspec_roots** as follows:

.. code-block:: yaml

    buildspec_roots:
      - $HOME/buildtest-cori

This field is used with the ``buildtest buildspec find`` command. If you rebuild
your buildspec cache via ``--rebuild`` option, buildtest will search for all buildspecs in
directories specified by **buildspec_roots** property. buildtest will recursively
find all **.yml** extension and validate each buildspec with appropriate schema.

.. _load_default_buildspecs:

Load Default Buildspecs
------------------------

By default buildtest will add the ``$BUILDTEST_ROOT/tutorials`` and ``$BUILDTEST_ROOT/general_tests``
to search path when searching for buildspecs with ``buildtest buildspec find`` command.
This can configured via ``load_default_buildspecs`` property which expects a boolean value.

By default we enable this property, however in practice you would want to disable this
``load_default_buildspecs: False`` if you only care about running your facility tests.


.. _configuring_executors:

What is an executor?
----------------------

An executor is responsible for running the test and capture output/error file and
return code. An executor can be local executor which runs tests on local machine or
batch executor that can be modelled as partition/queue. A batch executor is
responsible for **dispatching** job, then **poll** job until its finish, and
**gather** job metrics from scheduler.

Executor Declaration
--------------------

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
unique name. The *LocalExecutors* can be ``bash``, ``sh``, ``csh``, ``tcsh`` and ``python`` shell and they are
referenced in buildspec using ``executor`` field in the following format:

.. code-block:: yaml

    executor: <system>.<type>.<name>

For instance, if a buildspec wants to reference the LocalExecutor `bash` from the `generic`
cluster, you would specify the following in the buildspec:

.. code-block:: yaml

     executor: generic.local.bash

In our example configuration, we defined a local `bash` executor as follows:

.. code-block:: yaml

    executors:
      # define local executors for running jobs locally
      local:
        bash:
          description: submit jobs on local machine using bash shell
          shell: bash

The local executors requires the ``shell`` key which takes the pattern
``"^(/bin/bash|/bin/sh|/bin/csh|/bin/tcsh|/bin/zsh|sh|bash|csh|tcsh|zsh|python).*"``.
Any buildspec that references this executor will submit job using ``bash`` shell.

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


``logdir`` is not required in configuration, if it's not specified buildtest will write logs
based on `tempfile <https://docs.python.org/3/library/tempfile.html>`_ library which may vary
based on platform (Linux, Mac).

For instance, on Mac the directory path may be something as follows::

    /var/folders/1m/_jjv09h17k37mkktwnmbkmj0002t_q/T/buildtest_dy_xu1eb.log

The buildtest logs will start with **buildtest_** followed by random identifier with
a **.log** extension.

buildtest will write the same log file in **$BUILDTEST_ROOT/buildtest.log** which can
be used to fetch last build log. This is convenient if you don't remember the directory
path to log file.


before_script and after_script for executors
---------------------------------------------

Often times, you may want to run a set of commands before or after tests for more than
one test. For this reason, we support ``before_script`` and ``after_script`` section
per executor which is of string type where you can specify multi-line commands.

This can be demonstrated with an executor name **local.e4s** responsible for
building `E4S Testsuite <https://github.com/E4S-Project/testsuite>`_

.. code-block:: yaml

    local:
      e4s:
        description: "E4S testsuite locally"
        shell: bash
        before_script: |
          cd $SCRATCH
          git clone https://github.com/E4S-Project/testsuite.git
          cd testsuite
          source /global/common/software/spackecp/luke-wyatt-testing/spack/share/spack/setup-env.sh
          source setup.sh

The `e4s` executor attempts to clone E4S Testsuite in $SCRATCH and activate
a spack environment and run the initialize script ``source setup.sh``. buildtest
will write a ``before_script.sh`` and ``after_script.sh`` for every executor.
This can be found in ``var/executors`` directory as shown below

.. code-block:: console

    $ tree var/executors/
    var/executors/
    |-- local.bash
    |   |-- after_script.sh
    |   `-- before_script.sh
    |-- local.e4s
    |   |-- after_script.sh
    |   `-- before_script.sh
    |-- local.python
    |   |-- after_script.sh
    |   `-- before_script.sh
    |-- local.sh
    |   |-- after_script.sh
    |   `-- before_script.sh


    4 directories, 8 files

The ``before_script`` and ``after_script`` field is available for all executors and
if its not specified the file will be empty. Every test will source these scripts for
the appropriate executor.

.. _slurm_executors:

Cori @ NERSC
--------------

Shown below is the configuration file used at Cori.

.. command-output:: wget -q -O - https://raw.githubusercontent.com/buildtesters/buildtest-cori/devel/config.yml 2>&1
   :shell:

Default Executor Settings
---------------------------

One can define default executor configurations for all executors using the ``defaults`` property. Shown below is an
example

.. code-block:: yaml

    executors:
      defaults:
        pollinterval: 10
        launcher: sbatch
        max_pend_time: 90
        account: nstaff

The `launcher` field is applicable for batch executors in this
case, ``launcher: sbatch`` inherits **sbatch** as the job launcher for all slurm executors.

The ``account: nstaff`` will instruct buildtest to charge all jobs to account
``nstaff`` from Slurm Executors. The ``account`` option can be set in ``defaults``
field to all executors or defined per executor instance which overrides the default value.

Poll Interval
----------------

The ``pollinterval`` field is used  to poll jobs at set interval in seconds
when job is active in queue. The poll interval can be configured on command line
using ``buildtest build --poll-interval`` which overrides the configuration value.




`pollinterval`, `launcher` and `max_pend_time` have no effect on local executors.


Max Pend Time
---------------

The ``max_pend_time`` is **maximum** time job can be pending
within an executor, if it exceeds the limit buildtest will cancel the job.

The **max_pend_time** option can be overridden per executor level for example the
section below overrides the default to 300 seconds:

.. code-block:: yaml

        bigmem:
          description: bigmem jobs
          cluster: escori
          qos: bigmem
          max_pend_time: 300

The ``max_pend_time`` is used to cancel job only if job is pending in queue, it has
no impact if job is running. buildtest starts a timer at job submission and every poll interval
(``pollinterval`` field) checks if job has exceeded **max_pend_time** only if job is in **PENDING** (SLURM)
or **PEND** (LSF) state. If job pendtime exceeds `max_pend_time` limit, buildtest will
cancel job using ``scancel`` or ``bkill`` depending on the scheduler. Buildtest
will remove cancelled jobs from poll queue, in addition cancelled jobs won't be
reported in test report.

For more details on `max_pend_time` click :ref:`here <max_pend_time>`.

Specifying QoS (Slurm)
-----------------------

At Cori, jobs are submitted via qos instead of partition so we model a slurm executor
named by qos. The ``qos`` field instructs which Slurm QOS to use when submitting job. For
example we defined a slurm executor named **haswell_debug** which will submit jobs to **debug**
qos on the haswell partition as follows:

.. code-block:: yaml

    executors:
      slurm:
        haswell_debug:
          qos: debug
          cluster: cori
          options:
          - -C haswell

The ``cluster`` field specifies which slurm cluster to use
(i.e ``sbatch --clusters=<string>``). In-order to use ``bigmem``, ``xfer``,
or ``gpu`` qos at Cori, we need to specify **escori** cluster (i.e ``sbatch --clusters=escori``).

buildtest will detect slurm configuration and check qos, partition, cluster
match with buildtest configuration. In addition, buildtest supports multi-cluster
job submission and monitoring from remote cluster. This means if you specify
``cluster`` field buildtest will poll jobs using `sacct` with the
cluster name as follows: ``sacct -M <cluster>``.

The ``options`` field is use to specify any additional options to launcher (``sbatch``)
on command line. For instance, ``slurm.gpu`` executor, we use the ``options: -C gpu``
to submit to Cori GPU cluster which requires ``sbatch -M escori -C gpu``.
Any additional **#SBATCH** options are defined in buildspec for more details see :ref:`batch scheduler support <batch_support>`.

.. _pbs_executors:

PBS Executors
--------------

buildtest supports `PBS <https://www.altair.com/pbs-works-documentation/>`_ scheduler
which can be defined in the ``executors`` section. Shown below is an example configuration using
one ``pbs`` executor named ``workq``.  The property ``queue: workq`` defines
the name of PBS queue that is available in your system.

.. code-block:: yaml
    :linenos:
    :emphasize-lines: 12-14

    system:
      generic:
        hostnames: ['.*']

        moduletool: N/A
        load_default_buildspecs: True
        executors:
          defaults:
             pollinterval: 10
             launcher: qsub
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

buildtest will detect the PBS queues in your system and determine if queues are valid
and queue state `enabled` or `started` are set to **True**. In this example below, buildtest will
query the queue configuration and check the output of all pbs executors with this JSON format. In example
below we have one queue `workq` defined that is ``enabled`` and ``started``.

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

.. _pbs_limitation:

PBS Limitation
~~~~~~~~~~~~~~~~~~

.. Note:: Please note that buildtest PBS support relies on job history set because buildtest needs to query job after completion using `qstat -x`. This
          can be configured using ``qmgr`` by setting ``set server job_history_enable=True``. For more details see section **13.15.5.1 Enabling Job History** in `PBS 2020.1 Admin Guide <https://www.altair.com/pdfs/pbsworks/PBSAdminGuide2020.1.pdf>`_

.. _cdash_configuration:

CDASH Configuration
--------------------

buildtest can be configured to push test to `CDASH <https://www.kitware.com/cdash/project/about.html>`_. The default configuration
file provides a CDASH configuration for buildtest project is the following::

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