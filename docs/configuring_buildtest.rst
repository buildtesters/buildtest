.. _configuring_buildtest:

Configuring buildtest
======================

The buildtest configuration file is used for configuring behavior of buildtest.
There is a json schema file `settings.schema.json <https://raw.githubusercontent.com/buildtesters/buildtest/devel/buildtest/schemas/settings.schema.json>`_
that defines structure on how to write your configuration file.

For more details on schema attributes see `Settings Schema Documentation <https://buildtesters.github.io/schemas/schemadocs/settings.html>`_


Default Configuration
-----------------------

The default configuration for buildtest can be found in the git repo relative
to root of buildtest at ``buildtest/settings/config.yml``.
User may override the default configuration by creating their custom file in
``$HOME/.buildtest/config.yml``.

Shown below is the default configuration.

.. program-output:: cat ../buildtest/settings/config.yml

Executors
----------

Executors are responsible for running jobs, currently buildtest supports the following
executors:

- local
- slurm
- lsf

Their is a **ssh** executor is supported in schema but currently not implemented
in buildtest.

The local executor is responsible for submitting jobs locally. Currently, buildtest
supports ``bash``, ``sh`` and ``python`` shell. The executors are referenced in
your buildspec with the ``executor`` key as follows::

    executor: local.bash

The ``executor`` key in buildtest settings is of type ``object``, the sub-fields
are ``local``, ``ssh``, and ``slurm``.

Local Executors
~~~~~~~~~~~~~~~~

In this example below we define a local executor named `bash` that is referenced
in buildspec ``executor: local.bash``::

    executors:
      local:
        bash:
          shell: bash

Each local executor requires the ``shell`` key which takes the pattern
``^(/bin/bash|/bin/sh|sh|bash|python).*``

Any buildspec that references the executor ``local.bash`` will submit job
as ``bash /path/to/test.sh``.

You can pass options to shell which will get passed into each job submission.
For instance if you want bash executor to submit jobs by login mode you can do
the following::

    executors:
      local:
        login_bash:
          shell: bash --login

Then you can reference this executor as ``executor: local.login_bash`` and your
tests will be submitted via ``bash --login /path/to/test.sh``.

.. _slurm_executors:

Slurm Executors
~~~~~~~~~~~~~~~~~

The slurm executors are defined in the following section::

    executors:
      slurm:
        <slurm-executor1>:
        <slurm-executor2>:

Slurm executors are responsible for submitting jobs to slurm resource manager.
You can define as many slurm executors as you wish, so long as you have a unique
name to reference each executor. Generally, you will need one slurm executor
per partition or qos that you have at your site. Let's take a look at an example
slurm executor called ``normal``::

    executors:
      slurm:
        normal:
          options: ["-C haswell"]
          qos: normal

This executor can be referenced in buildspec as ``executor: slurm.normal``. This
executor defines the following:

- ``qos: normal`` will add ``-q normal`` to the launcher command. buildtest will check if qos is found in slurm configuration. If not found, buildtest will reject job submission.
- ``options`` key is used to pass any options to launcher command. In this example we add ``-C haswell``.

buildtest configuration for Cori @ NERSC
------------------------------------------

Let's take a look at Cori buildtest configuration::

    executors:

      defaults:
        pollinterval: 10
        launcher: sbatch

      local:
        bash:
          description: submit jobs on local machine using bash shell
          shell: bash

        sh:
          description: submit jobs on local machine using sh shell
          shell: sh

        python:
          description: submit jobs on local machine using python shell
          shell: python

      slurm:
        debug:
          description: jobs for debug qos
          qos: debug
          cluster: cori

        shared:
          description: jobs for shared qos
          qos: shared

        bigmem:
          description: bigmem jobs
          cluster: escori
          qos: bigmem

        xfer:
          description: xfer qos jobs
          qos: xfer

        gpu:
          description: submit jobs to GPU partition
          options: ["-C gpu"]
          cluster: escori

    config:
      editor: vi
      paths:
        prefix: $HOME/cache/

In this setting, we define 3 LocalExecutors: ``local.bash``, ``local.sh`` and ``local.python``
and 5 SlurmExecutors: ``slurm.debug``, ``slurm.shared``, ``slurm.bigmem``, ``slurm.xfer``, and ``slurm.gpu``.
We also introduce section ``defaults`` section to default configuration for executors.

At the moment, the ``launcher`` and ``pollinterval`` are available
fields in default which only apply for SlurmExecutor and LSFExecutor. Currently, buildtest supports
batch submission via ``sbatch`` so all SlurmExecutors will inherit ``sbatch`` as launcher.
The ``pollinterval`` field is used with SlurmExecutor to poll jobs at set interval in seconds
when job active in queue (``PENDING``, ``RUNNING``).

At Cori, jobs are submitted via qos instead of partition so each slurm executor
has the `qos` key. The ``description`` key is a brief description of the executor
which you can use to document the behavior of the executor. The ``cluster`` field
specifies which slurm cluster to use, at Cori in order to use ``bigmem`` qos we
need to specify ``-M escori`` where escori is the slurm cluster. buildtest will
detect slurm configuration and check if cluster is a valid cluster name.
In addition, `sacct` will poll job against the cluster name (``sacct -M <cluster>``).

The ``options`` field is use to specify any additional options to launcher (``sbatch``)
on command line. For ``slurm.gpu`` executor, we use this executor for submit to CoriGPU
which requires ``sbatch -M escori -C gpu``. Any additional #SBATCH options are defined
in buildspec using ``sbatch`` key.

buildtest configuration for Ascent @ OLCF
------------------------------------------

`Ascent <https://docs.olcf.ornl.gov/systems/ascent_user_guide.html>`_ is a training
system for Summit at OLCF, which is using a IBM Load Sharing
Facility (LSF) as their batch scheduler. Ascent has two
queues `batch` and `test`. To define LSF Executor we set
top-level key `lsf` in `executors` section.

The default launcher is `bsub` which can be defined under ``defaults``. The
``pollinterval`` will poll LSF jobs every 10 seconds using ``bjobs``. The
``pollinterval`` accepts a range between `10` - `300` seconds as defined in
schema. In order to avoid polling scheduler excessively pick a number that is best
suitable for your site.

::

    executors:
      defaults:
        launcher: bsub
        pollinterval: 10
      local:
        bash:
          description: submit jobs on local machine using bash shell
          shell: bash

        sh:
          description: submit jobs on local machine using sh shell
          shell: sh

        python:
          description: submit jobs on local machine using python shell
          shell: python
      lsf:
        batch:
          queue: batch
        test:
          queue: test
    config:
      editor: vi
      paths:
        prefix: /tmp

.. _buildspec_roots:

buildspec roots
-----------------

buildtest can detect buildspec using ``buildspec_roots`` keyword.  For example we
clone the repo https://github.com/buildtesters/buildtest-cori at **/Users/siddiq90/Documents/buildtest-cori**

config:
  editor: vi
  paths:
    buildspec_roots:
      - /Users/siddiq90/Documents/buildtest-cori


If you run ``buildtest buildspec find --clear`` it will detect all buildspecs in
buildspec_roots. buildtest will find all `.yml` extension. By default buildtest will
add the ``$BUILDTEST_ROOT/tutorials`` to search path, where $BUILDTEST_ROOT is root
of buildtest repo.

Example Configurations
-------------------------

buildtest provides a few example configurations for configuring buildtest this
can be retrieved by running ``buildtest schema -n settings.schema.json --examples``
or short option (``-e``), which will validate each example with schema file
``settings.schema.json``.

.. program-output:: cat docgen/schemas/settings-examples.txt

If you want to retrieve full json schema file run
``buildtest schema -n settings.schema.json --json`` or short option ``-j``

.. program-output:: cat docgen/schemas/settings-json.txt
