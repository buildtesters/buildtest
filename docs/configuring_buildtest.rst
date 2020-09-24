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

::

    config:
      editor: vi
      paths:
        buildspec_roots:
          - /Users/siddiq90/Documents/buildtest-cori


If you run ``buildtest buildspec find --clear`` it will detect all buildspecs in
buildspec_roots. buildtest will find all `.yml` extension. By default buildtest will
add the ``$BUILDTEST_ROOT/tutorials`` to search path, where $BUILDTEST_ROOT is root
of buildtest repo.

Before & After scripts for executors
-------------------------------------

Often times, you may want to run a set of commands before or after tests for more than
one test. For this reason, we support ``before_script`` and ``after_script`` section
per executor which is of string type where you can specify arbitrary commands.

This can be demonstrated with this executor name **local.e4s** responsible for
building `E4S Testsuite <https://github.com/E4S-Project/testsuite>`_::

    e4s:
      description: "E4S testsuite locally"
      shell: bash
      before_script: |
        cd $SCRATCH
        git clone https://github.com/E4S-Project/testsuite.git
        cd testsuite
        source /global/common/software/spackecp/luke-wyatt-testing/spack/share/spack/setup-env.sh
        source setup.sh

buildtest will write a ``before_script.sh`` and ``after_script.sh`` for every executor.
This can be found in ``var/executors`` directory as shown below::

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
if its not specified the file will be empty. Every test will source the before
and after script for the given executor.

CLI to buildtest configuration
-----------------------------------------------

The ``buildtest config`` command provides access to buildtest configuration, shown
below is the command usage.


.. program-output:: cat docgen/buildtest_config_--help.txt

If you want to view buildtest configuration you can run::

    buildtest config view

Shown below is an example output.

.. program-output:: cat docgen/config-view.txt

Likewise, you can edit the file by running::

    buildtest config edit

To check if your buildtest settings is valid, run ``buildtest config validate``.
This will validate your ``settings.yml`` with the schema **settings.schema.json**.
The output will be the following.

.. program-output:: cat docgen/config-validate.txt

If there is an error during validation, the output from **jsonschema.exceptions.ValidationError**
will be displayed in terminal. For example the error below indicates there was an error
on ``editor`` key in **config** object which expects the editor to be one of the
enum types [``vi``, ``vim``, ``nano``, ``emacs``]::

    $ buildtest config validate
    Traceback (most recent call last):
      File "/Users/siddiq90/.local/share/virtualenvs/buildtest-1gHVG2Pd/bin/buildtest", line 11, in <module>
        load_entry_point('buildtest', 'console_scripts', 'buildtest')()
      File "/Users/siddiq90/Documents/buildtest/buildtest/main.py", line 32, in main
        check_settings()
      File "/Users/siddiq90/Documents/buildtest/buildtest/config.py", line 71, in check_settings
        validate(instance=user_schema, schema=config_schema)
      File "/Users/siddiq90/.local/share/virtualenvs/buildtest-1gHVG2Pd/lib/python3.7/site-packages/jsonschema/validators.py", line 899, in validate
        raise error
    jsonschema.exceptions.ValidationError: 'gedit' is not one of ['vi', 'vim', 'nano', 'emacs']

    Failed validating 'enum' in schema['properties']['config']['properties']['editor']:
        {'default': 'vim',
         'enum': ['vi', 'vim', 'nano', 'emacs'],
         'type': 'string'}

    On instance['config']['editor']:
        'gedit'


You can get a summary of buildtest using ``buildtest config summary``, this will
display information from several sources into one single command along.

.. program-output:: cat docgen/config-summary.txt


Example Configurations
-------------------------

buildtest provides a few example configurations for configuring buildtest this
can be retrieved by running ``buildtest schema -n settings.schema.json --examples``
or short option (``-e``), which will validate each example with schema file
``settings.schema.json``.

.. program-output:: cat docgen/schemas/settings-examples.txt

If you want to retrieve full json schema file run
``buildtest schema -n settings.schema.json --json`` or short option ``-j``
