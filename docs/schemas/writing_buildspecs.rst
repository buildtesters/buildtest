.. writing_buildspecs:

Writing buildspecs
===================

buildspec is your test recipe that buildtest processes to generate a test script.
A buildspec can be composed of several test sections. The buildspec file is
validated with the :ref:`global_schema` and each test section is validated with
a sub-schema defined by the ``type`` field.

Let's start off with an example::

    version: "1.0"
    buildspecs:
      variables:
        type: script
        executor: local.bash
        vars:
          X: 1
          Y: 2
        run: echo "$X+$Y=" $(($X+$Y))

buildtest will validate the entire file with ``global.schema.json``, the schema
requires **version** and **buildspec** in order to validate file. The **buildspec**
is where you define each test. In this example their is one test called **variables**.
The test requires a **type** field which is the sub-schema used to validate the
test section. In this example ``type: script`` informs buildtest to use the :ref:`script_schema`
when validating test section.

Each subschema has a list of field attributes that are supported, for example the
fields: **type**, **executor**, **vars** and **run** are all valid fields supported
by the script schema. The **version** field informs which version of subschema to use.
Currently all sub-schemas are at version ``1.0`` where buildtest will validate
with a schema ``script-v1.0.schema.json``. In future, we can support multiple versions
of subschema for backwards compatibility.

The **executor** key is required for all sub-schemas which instructs buildtest
which executor to use when running the test. The executors are defined in your
buildtest settings in :ref:`configuring_buildtest`.

In this example we define variables using the `vars` section which is a Key/Value
pair for variable assignment. The `run` section is required for script schema which
defines the content of the test script.

Let's look at a more interesting example, shown below is a multi line run
example using the `script` schema with test name called
`systemd_default_target`, shown below is the content of test::

    version: "1.0"
    buildspecs:
      systemd_default_target:
        executor: local.bash
        type: script
        description: check if default target is multi-user.target
        run: |
          if [ "multi-user.target" == `systemctl get-default` ]; then
            echo "multi-user is the default target";
            exit 0
          fi
          echo "multi-user is not the default target";
          exit 1
        status:
          returncode: 0

The test name **systemd_default_target** defined in **buildspec** section is
validated with the following pattern ``"^[A-Za-z_][A-Za-z0-9_]*$"``. This test
will use the executor **local.bash** which means it will use the Local Executor
with an executor name `bash` defined in the buildtest settings. The default
buildtest settings will provide a bash executor as follows::

    executors:
      local:
        bash:
          description: submit jobs on local machine using bash shell
          shell: bash

The ``shell: bash`` indicates this executor will use `bash` to run the test scripts.
To reference this executor use the format ``<type>.<name>`` in this case **local.bash**
refers to bash executor.

The ``description`` field is an optional key that can be used to provide a brief
summary of the test. In this example we can a full multi-line run section, this
is achieved in YAML using ``run: |`` followed by content of run section tab indented
2 spaces.

In this example we introduce a new field `status` that is used for controlling how
buildtest will mark test state. By default, a returncode of **0** is PASS and non-zero
is a **FAIL**. Currently buildtest reports only two states: ``PASS``, ``FAIL``.
In this example, buildtest will match the actual returncode with one defined
in key `returncode` in the status section.

Return Code Matching
---------------------

In this next example we will illustrate the concept of returncode match with
different exit codes. In this example we have three tests called ``exit1_fail``,
``exit1_pass`` and ``returncode_mismatch``. All test are using the ``local.sh``
executor which is using ``sh`` to run the test. We expect **exit1_fail** and
**returncode_mismatch** to FAIL while **exit1_pass** will PASS since returncode matches

::

    version: "1.0"
    buildspecs:

      exit1_fail:
        executor: local.sh
        type: script
        description: exit 1 by default is FAIL
        run: exit 1

      exit1_pass:
        executor: local.sh
        type: script
        description: report exit 1 as PASS
        run: exit 1
        status:
          returncode: 1

      returncode_mismatch:
        executor: local.sh
        type: script
        description: exit 2 failed since it failed to match returncode 1
        run: exit 2
        status:
          returncode: 1

To demonstrate we will build this test and pay close attention to the Status field
in output::


    $ buildtest build -b pass_returncode.yml
    Paths:
    __________
    Prefix: /private/tmp
    Buildspec Search Path: ['/private/tmp/github.com/buildtesters/buildtest-cori', '/Users/siddiq90/.buildtest/site']
    Test Directory: /private/tmp/tests

    Stage: Discovered Buildspecs


    +-------------------------------+
    | Stage: Discovered Buildspecs  |
    +-------------------------------+

    /Users/siddiq90/Documents/tutorials/examples/pass_returncode.yml

    Excluded Buildspecs:  []

    +----------------------+
    | Stage: Building Test |
    +----------------------+

    Name                      Schema Validation File    TestPath                                 Buildspec
    ________________________________________________________________________________________________________________________________________________________________
    exit1_fail                script-v1.0.schema.json   /private/tmp/tests/pass_returncode/exit1_fail.sh /Users/siddiq90/Documents/tutorials/examples/pass_returncode.yml
    exit1_pass                script-v1.0.schema.json   /private/tmp/tests/pass_returncode/exit1_pass.sh /Users/siddiq90/Documents/tutorials/examples/pass_returncode.yml
    returncode_mismatch       script-v1.0.schema.json   /private/tmp/tests/pass_returncode/returncode_mismatch.sh /Users/siddiq90/Documents/tutorials/examples/pass_returncode.yml

    +----------------------+
    | Stage: Running Test  |
    +----------------------+

    Name                 Executor             Status               Return Code          Buildspec Path
    ________________________________________________________________________________________________________________________
    exit1_fail           local.sh             FAIL                 1                    /Users/siddiq90/Documents/tutorials/examples/pass_returncode.yml
    exit1_pass           local.sh             PASS                 1                    /Users/siddiq90/Documents/tutorials/examples/pass_returncode.yml
    returncode_mismatch  local.sh             FAIL                 2                    /Users/siddiq90/Documents/tutorials/examples/pass_returncode.yml

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Executed 3 tests
    Passed Tests: 1/3 Percentage: 33.333%
    Failed Tests: 2/3 Percentage: 66.667%


Python example
---------------

You can use *script* schema to write python scripts using the run section. This
can be achieved if you use the ``local.python`` executor assuming you have this
defined in your buildtest configuration.

Here is a python example calculating area of circle::

    version: "1.0"
    buildspecs:
      circle_area:
        executor: local.python
        type: script
        shell: python
        description: "Calculate circle of area given a radius"
        tags: ["python"]
        run: |
          import math
          radius = 2
          area = math.pi * radius * radius
          print("Circle Radius ", radius)
          print("Area of circle ", area)


The ``shell: python`` will let us write python script in the ``run`` section.
The ``tags`` field can be used to classify test, the field expects an array of
string items.

.. note::
    Python scripts are very picky when it comes to formatting, in the ``run`` section
    if you are defining multiline python script you must remember to use 2 space indent
    to register multiline string. buildtest will extract the content from run section
    and inject in your test script. To ensure proper formatting for a more complex python
    script you may be better of writing a python script in separate file and call it
    in ``run`` section.

Skipping test
-------------

By default, buildtest will run all tests defined in ``buildspecs`` section, if you
want to skip a test use the ``skip:`` field which expects a boolean value. Shown
below is an example test::

    version: "1.0"
    buildspecs:
      skip:
        type: script
        executor: local.bash
        skip: true
        run: hostname

      unskipped:
        type: script
        executor: local.bash
        skip: false
        run: hostname

The first test `skip` will be skipped by buildtest because ``skip: true`` is defined.

.. note::

    YAML and JSON have different representation for boolean. For json schema
    valid values are ``true`` and ``false`` see https://json-schema.org/understanding-json-schema/reference/boolean.html
    however YAML has many more representation for boolean see https://yaml.org/type/bool.html. You
    may use any of the YAML boolean, however it's best to stick with json schema values
    ``true`` and ``false``.


Here is an example build, notice message ``[skip] test is skipped`` during the build
stage::

    $ buildtest build -b examples/skip_tests.yml
    Paths:
    __________
    Prefix: /private/tmp
    Buildspec Search Path: ['/private/tmp/github.com/buildtesters/tutorials', '/Users/siddiq90/.buildtest/site']
    Test Directory: /private/tmp/tests

    Stage: Discovered Buildspecs


    +-------------------------------+
    | Stage: Discovered Buildspecs  |
    +-------------------------------+

    /Users/siddiq90/Documents/tutorials/examples/skip_tests.yml

    Excluded Buildspecs:  []

    +----------------------+
    | Stage: Building Test |
    +----------------------+

    Name                      Schema Validation File    TestPath                                 Buildspec
    ________________________________________________________________________________________________________________________________________________________________
    [skip] test is skipped.
    unskipped                 script-v1.0.schema.json   /private/tmp/tests/skip_tests/unskipped.sh /Users/siddiq90/Documents/tutorials/examples/skip_tests.yml

    +----------------------+
    | Stage: Running Test  |
    +----------------------+

    Name                 Executor             Status               Return Code          Buildspec Path
    ________________________________________________________________________________________________________________________
    unskipped            local.bash           PASS                 0                    /Users/siddiq90/Documents/tutorials/examples/skip_tests.yml

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Executed 1 tests
    Passed Tests: 1/1 Percentage: 100.000%
    Failed Tests: 0/1 Percentage: 0.000%


Slurm Executor (Experimental Feature)
--------------------------------------

buildtest can dispatch jobs to slurm, in order to use a slurm scheduler, you must
define a :ref:`slurm_executors` and reference it via ``executor``. In this example
we have a slurm executor ``slurm.debug``, in addition we can specify #SBATCH directives
using ``sbatch`` field. The sbatch field is a list of string types, buildtest will
insert #SBATCH in front of each option.

Shown below is an example buildspec::

    version: "1.0"
    buildspecs:
      slurm_metadata:
        description: Get metadata from compute node when submitting job
        type: script
        executor: slurm.debug
        sbatch:
          - "-t 00:05"
          - "-C haswell"
          - "-N 1"
        run: |
          export SLURM_JOB_NAME="firstjob"
          echo "jobname:" $SLURM_JOB_NAME
          echo "slurmdb host:" $SLURMD_NODENAME
          echo "pid:" $SLURM_TASK_PID
          echo "submit host:" $SLURM_SUBMIT_HOST
          echo "nodeid:" $SLURM_NODEID
          echo "partition:" $SLURM_JOB_PARTITION


Shown below is an example build of this test::

    $ buildtest build -b metadata.yml
    Paths:
    __________
    Prefix: /global/u1/s/siddiq90/cache
    Buildspec Search Path: ['/global/homes/s/siddiq90/.buildtest/site']
    Test Directory: /global/u1/s/siddiq90/cache/tests

    Stage: Discovered Buildspecs


    +-------------------------------+
    | Stage: Discovered Buildspecs  |
    +-------------------------------+

    /global/u1/s/siddiq90/buildtest-cori/slurm/valid_jobs/metadata.yml

    Excluded Buildspecs:  []

    +----------------------+
    | Stage: Building Test |
    +----------------------+

    Name                      Schema Validation File    TestPath                                 Buildspec
    ________________________________________________________________________________________________________________________________________________________________
    slurm_metadata            script-v1.0.schema.json   /global/u1/s/siddiq90/cache/tests/metadata/slurm_metadata.sh /global/u1/s/siddiq90/buildtest-cori/slurm/valid_jobs/metadata.yml

    +----------------------+
    | Stage: Running Test  |
    +----------------------+

    Name                 Executor             Status               Return Code          Buildspec Path
    ________________________________________________________________________________________________________________________
    [slurm_metadata] job dispatched to scheduler
    [slurm_metadata] acquiring job id in 10 seconds
    slurm_metadata       slurm.debug          N/A                  0                    /global/u1/s/siddiq90/buildtest-cori/slurm/valid_jobs/metadata.yml


    Polling Jobs in 10 seconds
    ________________________________________
    [slurm_metadata]: JobID 32501309 in COMPLETED state


    Polling Jobs in 10 seconds
    ________________________________________

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Executed 1 tests
    Passed Tests: 0/1 Percentage: 0.000%
    Failed Tests: 1/1 Percentage: 100.000%


Unlike the LocalExecutor, the Run stage, will dispatch the slurm job and poll
until job is completed. Once job is complete, it will gather the results and terminate.

Shown below, we perform hostname for every slurm executor for Cori system at NERSC.

::

    version: "1.0"
    buildspecs:
      debug_qos_knl_hostname:
        description: run hostname on KNL computenode
        type: script
        executor: slurm.debug
        sbatch:
          - "-t 5"
          - "-C knl"
          - "-N 1"
        run: hostname

      debug_qos_haswell_hostname:
        description: run hostname on KNL computenode
        type: script
        executor: slurm.debug
        sbatch:
          - "-t 5"
          - "-C haswell"
          - "-N 1"
        run: hostname

      shared_qos_hostname:
        description: run hostname through shared qos
        type: script
        executor: slurm.shared
        sbatch:
          - "-t 5"
          - "-C haswell"
          - "-N 1"
        run: hostname

      bigmem_qos_hostname:
        description: run hostname through bigmem qos
        type: script
        executor: slurm.bigmem
        sbatch:
          - "-t 5"
          - "-C haswell"
          - "-N 1"
        run: hostname

      xfer_qos_hostname:
        description: run hostname through bigmem qos
        type: script
        executor: slurm.xfer
        sbatch:
          - "-t 5"
          - "-N 1"
        run: hostname


The ``SlurmExecutor`` class responsible for managing slurm jobs will perform the
following action

  1. Check slurm binary ``sbatch`` and ``sacct``.
  2. Dispatch Job and acquire job ID
  3. Poll Job
  4. Gather Job results

buildtest will dispatch all jobs and poll all jobs in a ``while (True)`` until all
jobs are complete. If job is in [**PENDING** | **RUNNING** ] then buildtest will
keep polling at set interval until job is complete. Once job is not in **PENDING**
or **RUNNING** stage, buildtest will gather job results and wait until all jobs have
finished.

