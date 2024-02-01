.. _configuring_executors:

Configuring Executors
======================

An executor is responsible for running the test and capture output/error file and
return code. An executor can be local executor which runs tests on local machine or
batch executor that can be modelled as partition/queue. A batch executor is
responsible for dispatching job, then poll job until its finish and
gather job results.

Executor Declaration
---------------------

The ``executors`` is a JSON `object`, that defines one or more executors. The executors
are grouped by their type followed by executor name. In this example we define two
local executors ``bash``, ``sh`` which will run tests on local machine.

.. code-block:: yaml
   :emphasize-lines: 3-10

      system:
        generic:
          executors:
            local:
              bash:
                description: submit jobs on local machine using bash shell
                shell: bash
              sh:
                description: submit jobs on local machine using sh shell
                shell: sh

The local executors are defined in section ``local`` where each executor must be
unique name and they are referenced in buildspec using ``executor`` field in the following format:

.. code-block:: yaml

    executor: <system>.<type>.<name>

For instance, if a buildspec wants to reference the local executor **bash** from the **generic**
cluster, you would specify the following in the buildspec:

.. code-block:: yaml

     executor: generic.local.bash

In our example configuration, we defined a ``bash`` executor as follows:

.. code-block:: yaml
    :emphasize-lines: 3-6

    executors:
      # define local executors for running jobs locally
      local:
        bash:
          description: submit jobs on local machine using bash shell
          shell: bash

The local executors require the ``shell`` key which is one of supported shells in your system. On Linux/Mac system
you can find all supported shells in file **/etc/shells**. Any buildspec that references this executor will submit
job using ``bash`` shell.

You can pass options to shell which will get passed into each job submission.
For instance if you want all bash scripts to run in login shell you can specify ``bash --login``:

.. code-block:: yaml
    :emphasize-lines: 4

    executors:
      local:
        login_bash:
          shell: bash --login

Then you can reference this executor as ``executor: generic.local.login_bash`` and your
tests will be submitted via ``bash --login /path/to/test.sh``.

Once you define your executors, you can :ref:`query the executors <view_executors>` via ``buildtest config executors list``
command.

.. _slurm_executors:

Slurm Executors
----------------

If you have a `Slurm <https://slurm.schedmd.com/documentation.html>`_ cluster, you can define
slurm executors in your configuration via ``slurm`` property.

Depending on your slurm configuration, you can submit jobs via **qos** or **partition**. Buildtest supports
both methods and you can specify either ``qos`` or ``partition`` property.

In this example below, we will define a slurm executor named **haswell_debug** which will submit jobs to **debug**
qos on the haswell partition as follows. The ``qos`` property is used to select slurm qos, the ``options`` property
is used to pass additional options to ``sbatch`` command. In this example we are passing ``-C haswell`` to select
haswell nodes. Any additional **#SBATCH** options are defined in buildspec for more details see
:ref:`batch scheduler support <batch_support>`.

.. code-block:: yaml
   :emphasize-lines: 3-6

    executors:
      slurm:
        haswell_debug:
          qos: debug
          cluster: cori
          options: ["-C haswell"]

buildtest will detect slurm configuration and check qos, partition, cluster
match with buildtest configuration. In addition, buildtest supports multi-cluster
job submission and monitoring from remote cluster. This means if you specify
``cluster`` field buildtest will poll jobs using **sacct** with the
cluster name as follows: ``sacct -M <cluster>``.

You can configure your slurm executors to use slurm partitions instead of qos.  This
can be done via ``partition`` property. In this next example we define an executor name ``regular_hsw`` which will
submit jobs to partition **regular_hsw**. The ``description`` field may be used for information purposes.

.. code-block:: yaml
   :emphasize-lines: 4

    executors:
      slurm:
        regular_hsw:
          partition: regular_hsw
          description: regular haswell queue

Buildtest will check if slurm partition is in ``up`` state before adding executor. If any partition is in ``down`` state,
buildtest will mark the executor in **invalid** state and will be unusable.

To check availability of partition state, let's say ``regular_hsw``, buildtest will run the following command.

.. code-block:: console

    $ sinfo -p regular_hsw -h -O available
    up

.. _project_account:

Specifying Project Account
---------------------------

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
--------------

The ``pollinterval`` field is used  to poll jobs at set interval in seconds
when job is active in queue. The poll interval can be configured on command line
using ``buildtest build --pollinterval`` which overrides the configuration value.

.. Note::

    ``pollinterval``  and ``maxpendtime`` have no effect on local executors.


Max Pend Time
--------------

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
--------------

.. Note:: buildtest PBS support relies on job history set because buildtest needs to query job after completion using ``qstat -x``. This
          can be configured using ``qmgr`` by setting ``set server job_history_enable=True``. For more details see section **14.15.5.1 Enabling Job History** in `PBS 2021.1.3 Admin Guide <https://help.altair.com/2021.1.3/PBS%20Professional/PBSAdminGuide2021.1.3.pdf>`_


buildtest supports `PBS <https://community.altair.com/community?id=altair_product_documentation>`_ scheduler
which can be defined in the ``executors`` section. Shown below is an example configuration using
one ``pbs`` executor named ``workq``.  The property ``queue: workq`` defines
the name of PBS queue that is available in your system.

.. code-block:: yaml
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

.. _container_executor:

Container Executor
--------------------

Buildtest supports executor declaration for container based jobs. The container executor will run all associated test for the executor
on the specified container image. Currently, we support `docker`, `podman` and `singularity` as the container platforms. We assume container
runtime is installed on your system and is accessible in your $PATH.

Let's take a look at the following container executor declaration. The top level keyword ``container`` is used to define the container
executor which can follow any arbitrary name. We have defined two container executors named **ubuntu** and **python** that specify the
container image and platform via ``image`` and ``platform`` property. The ``description`` is used for information purposes and does not
impact buildtest in any way.

You can specify the full URI to the container image which is useful if you are using a custom registry

.. code-block:: yaml
    :emphasize-lines: 2-10

    executors:
      container:
        ubuntu:
          image: ubuntu:20.04
          platform: docker
          description: submit jobs on ubuntu container
        python:
          image: python:3.11.0
          platform: docker
          description: submit jobs on python container

You can specify container runtime options via ``options`` and bind mount via ``mount`` property. Both properties are
are string type, for instance let's say you want to bind mount ``/tmp`` directory to ``/tmp``

.. code-block:: yaml
    :emphasize-lines: 6-7

    executors:
      container:
        ubuntu:
          image: ubuntu:20.04
          platform: docker
          mount: "/tmp:/tmp"
          options: "--user root"
          description: submit jobs on ubuntu container


Run command commands before executing test
--------------------------------------------

You can configure an executor to run a set of commands when using an executor. You
can use ``before_script`` property to specify a list of commands to run prior to running
test.

The content of the ``before_script`` will be inserted in a shell script that is sourced
by all tests.

.. code-block:: yaml
    :emphasize-lines: 5-7

      local:
        bash:
          description: submit jobs on local machine using bash shell
          shell: bash
          before_script: |
            today=$(date "+%D")
            echo "Today is $today, running test with user: $(whoami)"

buildtest will write a ``before_script.sh`` in ``$BUILDTEST_ROOT/var/executors`` directory that will contain
contents of ``before_script``. Shown below is a list of ``before_script.sh`` for all local executors.

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


Disabling an executor
----------------------

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

Loading Modules in Executors
-----------------------------

You can configure executors to load modules, purge or restore from collection which will be run for all tests that use the executor.
This can be achieved via ``module`` property that can be defined in the executor definition. In this next example, we create a bash executor
that will purge modules and load gcc. The ``purge`` property is a boolean, if set to **True** we will run **module purge** before
loading commands. The ``load`` property is a list of modules to **module load**.

.. code-block:: yaml
   :emphasize-lines: 5-7

    executors:
      local:
        bash:
          shell: bash
          module:
            purge: True
            load: ["gcc"]