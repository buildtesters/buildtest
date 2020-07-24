.. _configuring_buildtest:

Configuring buildtest
======================

Schema File
------------

The schema file used for configuring and validating buildtest is done
by `settings.script.json <https://raw.githubusercontent.com/buildtesters/buildtest/devel/buildtest/settings/settings.schema.json>`_

For more details on schema attributes see `Settings Schema Documentation <https://buildtesters.github.io/schemas/settings/>`_


Default Settings
-----------------------

The default settings for buildtest is found in ``buildtest/settings/settings.yml``.
At start of buildtest this file is copied to ``$HOME/.buildtest/settings.yml`` to
help you get started. Shown below is the default settings file.

.. program-output:: cat ../buildtest/settings/settings.yml

Executors
----------

Executors are responsible for running jobs, currently buildtest supports **local**
and **slurm** executor, while **ssh** executor supported in schema but currently is not
supported by buildtest at the moment.

The local executor is responsible for submitting jobs locally. Currently, buildtest
supports ``bash``, ``sh`` and ``python`` shell. The executors are referenced in
your buildspec with the ``executor`` key such as::

    executor: local.bash

The ``executor`` key in buildtest settings is of type ``object``, the sub-fields
are ``local``, ``ssh``, and ``slurm``.

Local Executors
~~~~~~~~~~~~~~~~

The local executors are defined in the following section::

    executors:
      local:
        <local-executor1>:
        <local-executor2>:

Each local executor requires the ``shell`` key which takes the pattern
``^(/bin/bash|/bin/sh|sh|bash|python).*``. A bash executor is defined as
follows::

    executors:
      local:
        bash:
          shell: bash

A buildspec can reference this executor via ``executor: local.bash`` and buildtest
will submit job as ``bash /path/to/test.sh``.

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

- The ``launcher`` controls the launcher method, currently we only support sbatch as the launcher.
- ``qos: normal`` will add ``-q normal`` to the launcher command. buildtest will check if qos is found in slurm configuration. If not found, buildtest will reject job submission.
- ``options`` key is used to pass any options to launcher command. In this example we add ``-C haswell``.

buildtest setting for Cori - NERSC
------------------------------------

Let's take a look at Cori buildtest setting::

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
We also introduce section ``default`` in executor section which is used for setting default
setting for all executor. At the moment, the ``launcher`` and ``pollinterval`` are available
fields in default which only apply for SlurmExecutors. Currently, buildtest supports
batch submission via ``sbatch`` so all SlurmExecutors will inherit ``sbatch`` as launcher.
The ``pollinterval`` field is used with SlurmExecutor to poll jobs at set interval in seconds
when job active in queue (PENDING, RUNNING).


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

Settings Example
-----------------

To retrieve a list of settings example you can run ``buildtest schema -n settings.schema.json -e``
which will show a listing a valid buildtest settings.

.. program-output:: cat docgen/schemas/settings-examples.txt

Settings Schema
-----------------

Shown below is the json schema for buildtest settings that can be retrieved via
``buildtest schema -n settings.schema.json -j``

.. program-output:: cat docgen/schemas/settings-json.txt
