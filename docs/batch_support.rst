.. _batch_support:

Batch Scheduler Support
========================


Slurm
------

buildtest can submit jobs to `Slurm <https://slurm.schedmd.com/>`_ assuming you have slurm executors defined
in your configuration file. The ``SlurmExecutor`` class is responsible for managing slurm jobs which
will perform the following action

  1. Check slurm binary ``sbatch`` and ``sacct``.
  2. Dispatch Job and acquire job ID using ``sacct``.
  3. Poll all slurm jobs until all have finished
  4. Gather Job results once job is complete via ``sacct``.

buildtest will dispatch slurm jobs and poll all jobs until all
jobs are complete. If job is in **PENDING** or  **RUNNING** state, then buildtest will
keep polling at a set interval defined by ``pollinterval`` setting in buildtest.
Once job is not in **PENDING** or **RUNNING** stage, buildtest will gather job results
and wait until all jobs have finished.

In this example we have a slurm executor ``cori.slurm.knl_debug``,
in addition we can specify **#SBATCH** directives using ``sbatch`` field.
The sbatch field is a list of string types, buildtest will
insert **#SBATCH** directive in front of each value.

Shown below is an example buildspec

.. code-block:: yaml
    :emphasize-lines: 6,8-10

    version: "1.0"
    buildspecs:
      slurm_metadata:
        description: Get metadata from compute node when submitting job
        type: script
        executor: cori.slurm.knl_debug
        tags: [jobs]
        sbatch:
          - "-t 00:05"
          - "-N 1"
        run: |
          export SLURM_JOB_NAME="firstjob"
          echo "jobname:" $SLURM_JOB_NAME
          echo "slurmdb host:" $SLURMD_NODENAME
          echo "pid:" $SLURM_TASK_PID
          echo "submit host:" $SLURM_SUBMIT_HOST
          echo "nodeid:" $SLURM_NODEID
          echo "partition:" $SLURM_JOB_PARTITION


buildtest will add the ``#SBATCH`` directives at top of script followed by
content in the ``run`` section. Shown below is the example test content. Every slurm
will insert ``#SBATCH --job-name``, ``#SBATCH --output`` and ``#SBATCH --error`` line
which is determined by the name of the test.


.. code-block:: shell
    :emphasize-lines: 2-6

    #!/bin/bash
    #SBATCH -t 00:05
    #SBATCH -N 1
    #SBATCH --job-name=slurm_metadata
    #SBATCH --output=slurm_metadata.out
    #SBATCH --error=slurm_metadata.err
    export SLURM_JOB_NAME="firstjob"
    echo "jobname:" $SLURM_JOB_NAME
    echo "slurmdb host:" $SLURMD_NODENAME
    echo "pid:" $SLURM_TASK_PID
    echo "submit host:" $SLURM_SUBMIT_HOST
    echo "nodeid:" $SLURM_NODEID
    echo "partition:" $SLURM_JOB_PARTITION


The ``cori.slurm.knl_debug`` executor in our configuration file is defined as follows

.. code-block:: yaml
    :emphasize-lines: 5-10

    system:
      cori:
        executors:
          slurm:
            knl_debug:
              qos: debug
              cluster: cori
              options:
              - -C knl,quad,cache
              description: debug queue on KNL partition

With this setting, any buildspec test that use ``cori.slurm.knl_debug`` executor will result
in the following launch option: ``sbatch --qos debug --clusters=cori -C knl,quad,cache </path/to/script.sh>``.

Unlike the LocalExecutor, the **Run Stage**, will dispatch the slurm job and poll
until job is completed. Once job is complete, it will gather the results and terminate.
In Run Stage, buildtest will mark test status as ``N/A`` because job is submitted
to scheduler and pending in queue. In order to get job result, we need to wait
until job is complete then we gather results and determine test state. buildtest
keeps track of all buildspecs, testscripts to be run and their results. A test
using LocalExecutor will run test in **Run Stage** and returncode will be retrieved
and status can be calculated immediately. For Slurm Jobs, buildtest dispatches
the job and process next job. buildtest will show output of all tests after
**Polling Stage** with test results of all tests. A slurm job with exit code 0 will
be marked with status ``PASS``.

Shown below is an example build for this test

.. code-block:: console

    (buildtest) siddiq90@cori01> buildtest build -b buildspecs/jobs/metadata.yml
    ╭──────────────────────────────────────────────── buildtest summary ────────────────────────────────────────────────╮
    │                                                                                                                   │
    │ User:               siddiq90                                                                                      │
    │ Hostname:           cori01                                                                                        │
    │ Platform:           Linux                                                                                         │
    │ Current Time:       2021/10/13 09:23:35                                                                           │
    │ buildtest path:     /global/homes/s/siddiq90/github/buildtest/bin/buildtest                                       │
    │ buildtest version:  0.11.0                                                                                        │
    │ python path:        /global/homes/s/siddiq90/.conda/envs/buildtest/bin/python                                     │
    │ python version:     3.8.8                                                                                         │
    │ Configuration File: /global/u1/s/siddiq90/github/buildtest-cori/config.yml                                        │
    │ Test Directory:     /global/u1/s/siddiq90/github/buildtest/var/tests                                              │
    │ Command:            /global/homes/s/siddiq90/github/buildtest/bin/buildtest build -b buildspecs/jobs/metadata.yml │
    │                                                                                                                   │
    ╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
    ──────────────────────────────────────────────────────────────────  Discovering Buildspecs ──────────────────────────────────────────────────────────────────
    Discovered Buildspecs:  1
    Excluded Buildspecs:  0
    Detected Buildspecs after exclusion:  1
                               Discovered buildspecs
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║ Buildspecs                                                               ║
    ╟──────────────────────────────────────────────────────────────────────────╢
    ║ /global/u1/s/siddiq90/github/buildtest-cori/buildspecs/jobs/metadata.yml ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    ──────────────────────────────────────────────────────────────────── Parsing Buildspecs ─────────────────────────────────────────────────────────────────────
    Valid Buildspecs: 1
    Invalid Buildspecs: 0
    /global/u1/s/siddiq90/github/buildtest-cori/buildspecs/jobs/metadata.yml: VALID


    Total builder objects created: 1


                                                                           Builder Details
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Builder                 ┃ Executor             ┃ description                                        ┃ buildspecs                                          ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ slurm_metadata/a45a9f6a │ cori.slurm.knl_debug │ Get metadata from compute node when submitting job │ /global/u1/s/siddiq90/github/buildtest-cori/buildsp │
    │                         │                      │                                                    │ ecs/jobs/metadata.yml                               │
    └─────────────────────────┴──────────────────────┴────────────────────────────────────────────────────┴─────────────────────────────────────────────────────┘
    ─────────────────────────────────────────────────────────────────────── Building Test ───────────────────────────────────────────────────────────────────────
    [09:23:35] slurm_metadata/a45a9f6a: Creating test directory -                                                                                     base.py:440
               /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/metadata/slurm_metadata/a45a9f6a
               slurm_metadata/a45a9f6a: Creating stage directory -                                                                                    base.py:450
               /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/metadata/slurm_metadata/a45a9f6a/stage
               slurm_metadata/a45a9f6a: Writing build script:                                                                                         base.py:567
               /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/metadata/slurm_metadata/a45a9f6a/slurm_metadata_build.sh
    ─────────────────────────────────────────────────────────────────────── Running Tests ───────────────────────────────────────────────────────────────────────
    ______________________________
    Launching test: slurm_metadata/a45a9f6a
    slurm_metadata/a45a9f6a: Running Test script
    /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/metadata/slurm_metadata/a45a9f6a/slurm_metadata_build.sh
    slurm_metadata/a45a9f6a: JobID 48410143 dispatched to scheduler
    Polling Jobs in 30 seconds
    slurm_metadata/a45a9f6a: Job 48410143 is complete!
    slurm_metadata/a45a9f6a: Writing output file -
    /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/metadata/slurm_metadata/a45a9f6a/slurm_metadata.out
    slurm_metadata/a45a9f6a: Writing error file -
    /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/metadata/slurm_metadata/a45a9f6a/slurm_metadata.err
                       Pending Jobs
    ┏━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┓
    ┃ Builder ┃ executor ┃ JobID ┃ JobState ┃ runtime ┃
    ┡━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━┩
    └─────────┴──────────┴───────┴──────────┴─────────┘
                                       Completed Jobs
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┓
    ┃ Builder                 ┃ executor             ┃ JobID    ┃ JobState  ┃ runtime   ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━┩
    │ slurm_metadata/a45a9f6a │ cori.slurm.knl_debug │ 48410143 │ COMPLETED │ 30.714244 │
    └─────────────────────────┴──────────────────────┴──────────┴───────────┴───────────┘
                                                           Test Summary
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━┓
    ┃ Builder                 ┃ executor             ┃ status ┃ Checks (ReturnCode, Regex, Runtime) ┃ ReturnCode ┃ Runtime   ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━┩
    │ slurm_metadata/a45a9f6a │ cori.slurm.knl_debug │ PASS   │ N/A N/A N/A                         │ 0          │ 30.714244 │
    └─────────────────────────┴──────────────────────┴────────┴─────────────────────────────────────┴────────────┴───────────┘



    Passed Tests: 1/1 Percentage: 100.000%
    Failed Tests: 0/1 Percentage: 0.000%


    Writing Logfile to: /tmp/buildtest_8pfljnkx.log
    A copy of logfile can be found at $BUILDTEST_ROOT/buildtest.log -  /global/homes/s/siddiq90/github/buildtest/buildtest.log

The **SlurmExecutor** class is responsible for processing slurm job that may include:
dispatch, poll, gather, or cancel job. The SlurmExecutor will gather job metrics
via `sacct <https://slurm.schedmd.com/sacct.html>`_.

buildtest can check status based on Slurm Job State, this is defined by ``State`` field
in sacct. In next example, we introduce field ``slurm_job_state`` which
is part of ``status`` field. This field expects one of the following values: ``[COMPLETED, FAILED, OUT_OF_MEMORY, TIMEOUT ]``
This is an example of simulating fail job by expecting a return code of 1 with job
state of ``FAILED``.

.. code-block:: yaml
    :linenos:
    :emphasize-lines: 8-9

    version: "1.0"
    buildspecs:
      wall_timeout:
        type: script
        executor: cori.slurm.knl_debug
        sbatch: [ "-t '00:00:10'", "-n 1"]
        description: "This job simulates job timeout by sleeping for 180sec while requesting 10sec"
        tags: ["jobs", "fail"]
        run: sleep 180
        status:
          slurm_job_state: "TIMEOUT"


If we run this test, buildtest will mark this test as ``PASS`` because the slurm job
state matches with expected result defined by field ``slurm_job_state``. This job will
be TIMEOUT because we requested 2 mins while this job will sleep 300sec (5min).

.. code-block:: console

    (buildtest) siddiq90@cori01> buildtest build -b buildspecs/jobs/fail/timeout.yml
    ╭────────────────────────────────────────────────── buildtest summary ──────────────────────────────────────────────────╮
    │                                                                                                                       │
    │ User:               siddiq90                                                                                          │
    │ Hostname:           cori01                                                                                            │
    │ Platform:           Linux                                                                                             │
    │ Current Time:       2021/10/13 09:38:26                                                                               │
    │ buildtest path:     /global/homes/s/siddiq90/github/buildtest/bin/buildtest                                           │
    │ buildtest version:  0.11.0                                                                                            │
    │ python path:        /global/homes/s/siddiq90/.conda/envs/buildtest/bin/python                                         │
    │ python version:     3.8.8                                                                                             │
    │ Configuration File: /global/u1/s/siddiq90/github/buildtest-cori/config.yml                                            │
    │ Test Directory:     /global/u1/s/siddiq90/github/buildtest/var/tests                                                  │
    │ Command:            /global/homes/s/siddiq90/github/buildtest/bin/buildtest build -b buildspecs/jobs/fail/timeout.yml │
    │                                                                                                                       │
    ╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
    ──────────────────────────────────────────────────────────────────  Discovering Buildspecs ──────────────────────────────────────────────────────────────────
    Discovered Buildspecs:  1
    Excluded Buildspecs:  0
    Detected Buildspecs after exclusion:  1
                                 Discovered buildspecs
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║ Buildspecs                                                                   ║
    ╟──────────────────────────────────────────────────────────────────────────────╢
    ║ /global/u1/s/siddiq90/github/buildtest-cori/buildspecs/jobs/fail/timeout.yml ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    ──────────────────────────────────────────────────────────────────── Parsing Buildspecs ─────────────────────────────────────────────────────────────────────
    Valid Buildspecs: 1
    Invalid Buildspecs: 0
    /global/u1/s/siddiq90/github/buildtest-cori/buildspecs/jobs/fail/timeout.yml: VALID


    Total builder objects created: 1


                                                                           Builder Details
    ┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Builder               ┃ Executor             ┃ description                                          ┃ buildspecs                                          ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ wall_timeout/13d288ff │ cori.slurm.knl_debug │ This job simulates job timeout by sleeping for       │ /global/u1/s/siddiq90/github/buildtest-cori/buildsp │
    │                       │                      │ 180sec while requesting 10sec                        │ ecs/jobs/fail/timeout.yml                           │
    └───────────────────────┴──────────────────────┴──────────────────────────────────────────────────────┴─────────────────────────────────────────────────────┘
    ─────────────────────────────────────────────────────────────────────── Building Test ───────────────────────────────────────────────────────────────────────
    [09:38:26] wall_timeout/13d288ff: Creating test directory -                                                                                       base.py:440
               /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/timeout/wall_timeout/13d288ff
               wall_timeout/13d288ff: Creating stage directory -                                                                                      base.py:450
               /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/timeout/wall_timeout/13d288ff/stage
               wall_timeout/13d288ff: Writing build script:                                                                                           base.py:567
               /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/timeout/wall_timeout/13d288ff/wall_timeout_build.sh
    ─────────────────────────────────────────────────────────────────────── Running Tests ───────────────────────────────────────────────────────────────────────
    ______________________________
    Launching test: wall_timeout/13d288ff
    wall_timeout/13d288ff: Running Test script
    /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/timeout/wall_timeout/13d288ff/wall_timeout_build.sh
    wall_timeout/13d288ff: JobID 48410498 dispatched to scheduler
    Polling Jobs in 30 seconds
                                      Pending Jobs
    ┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┓
    ┃ Builder               ┃ executor             ┃ JobID    ┃ JobState ┃ runtime ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━┩
    │ wall_timeout/13d288ff │ cori.slurm.knl_debug │ 48410498 │ RUNNING  │ 30.423  │
    └───────────────────────┴──────────────────────┴──────────┴──────────┴─────────┘
    Polling Jobs in 30 seconds
                                      Pending Jobs
    ┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┓
    ┃ Builder               ┃ executor             ┃ JobID    ┃ JobState ┃ runtime ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━┩
    │ wall_timeout/13d288ff │ cori.slurm.knl_debug │ 48410498 │ RUNNING  │ 60.564  │
    └───────────────────────┴──────────────────────┴──────────┴──────────┴─────────┘
    Polling Jobs in 30 seconds
    wall_timeout/13d288ff: Job 48410498 is complete!
    wall_timeout/13d288ff: Writing output file -
    /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/timeout/wall_timeout/13d288ff/wall_timeout.out
    wall_timeout/13d288ff: Writing error file -
    /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/timeout/wall_timeout/13d288ff/wall_timeout.err
                       Pending Jobs
    ┏━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┓
    ┃ Builder ┃ executor ┃ JobID ┃ JobState ┃ runtime ┃
    ┡━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━┩
    └─────────┴──────────┴───────┴──────────┴─────────┘
                                      Completed Jobs
    ┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━┓
    ┃ Builder               ┃ executor             ┃ JobID    ┃ JobState ┃ runtime   ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━┩
    │ wall_timeout/13d288ff │ cori.slurm.knl_debug │ 48410498 │ TIMEOUT  │ 90.675675 │
    └───────────────────────┴──────────────────────┴──────────┴──────────┴───────────┘
                                                          Test Summary
    ┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━┓
    ┃ Builder               ┃ executor             ┃ status ┃ Checks (ReturnCode, Regex, Runtime) ┃ ReturnCode ┃ Runtime   ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━┩
    │ wall_timeout/13d288ff │ cori.slurm.knl_debug │ PASS   │ False False False                   │ 0          │ 90.675675 │
    └───────────────────────┴──────────────────────┴────────┴─────────────────────────────────────┴────────────┴───────────┘



    Passed Tests: 1/1 Percentage: 100.000%
    Failed Tests: 0/1 Percentage: 0.000%


    Writing Logfile to: /tmp/buildtest_4lvnkxge.log
    A copy of logfile can be found at $BUILDTEST_ROOT/buildtest.log -  /global/homes/s/siddiq90/github/buildtest/buildtest.log


buildtest marked this test ``PASS`` because the jobstate **TIMEOUT** match the value provided by ``slurm_job_state`` in the buildspec.


LSF
----

buildtest can support job submission to `IBM Spectrum LSF <https://www.ibm.com/support/knowledgecenter/en/SSWRJV/product_welcome_spectrum_lsf.html>`_
if you have defined LSF executors in your configuration file.

The ``bsub`` property can be used to  specify **#BSUB** directive into job script. This example
will use the executor ``ascent.lsf.batch`` executor that was defined in buildtest configuration.

.. code-block:: yaml
    :linenos:
    :emphasize-lines: 6

    version: "1.0"
    buildspecs:
      hostname:
        type: script
        executor: ascent.lsf.batch
        bsub: [ "-W 10",  "-nnodes 1"]

        run: jsrun hostname

The LSFExecutor poll jobs  and retrieve job state using
``bjobs -noheader -o 'stat' <JOBID>``. The LSFExecutor will poll
job so long as they are in **PEND** or **RUN** state. Once job is not in
any of the two states, LSFExecutor will gather job results. buildtest will retrieve
the following format fields using ``bjobs``: **job_name**, **stat**, **user**, **user_group**, **queue**, **proj_name**,
**pids**, **exit_code**, **from_host**, **exec_host**, **submit_time**, **start_time**,
**finish_time**, **nthreads**, **exec_home**, **exec_cwd**, **output_file**, **error_file** to
get job record.


PBS
----

buildtest can support job submission to `PBS Pro <https://www.altair.com/pbs-works-documentation/>`_ or `OpenPBS <https://openpbs.atlassian.net/wiki/spaces/PBSPro/overview>`_
scheduler. Assuming you have configured :ref:`pbs_executors` in your configuration file you can submit jobs
to the PBS executor by selecting the appropriate pbs executor via ``executor`` property in buildspec. The ``#PBS``
directives can be specified using ``pbs`` field which is a list of PBS options that get inserted at top of script. Shown
below is an example buildspec using the `script` schema.

.. code-block:: yaml
   :emphasize-lines: 6

    version: "1.0"
    buildspecs:
      pbs_sleep:
        type: script
        executor: generic.pbs.workq
        pbs: ["-l nodes=1", "-l walltime=00:02:00"]
        run: sleep 10


buildtest will poll PBS jobs using ``qstat -x -f -F json <jobID>`` until job is finished. Note that
we use **-x** option to retrieve finished jobs which is required in-order for buildtest to detect job
state upon completion.

Shown below is an example build of the buildspec using PBS scheduler.


.. code-block:: console

    [pbsuser@pbs tmp]$ buildtest -c tests/settings/pbs.yml build -b tests/examples/pbs/sleep.yml --pollinterval=5
    ╭─────────────────────────────────────────────────── buildtest summary ────────────────────────────────────────────────────╮
    │                                                                                                                          │
    │ User:               pbsuser                                                                                              │
    │ Hostname:           pbs                                                                                                  │
    │ Platform:           Linux                                                                                                │
    │ Current Time:       2021/10/13 16:59:34                                                                                  │
    │ buildtest path:     /tmp/bin/buildtest                                                                                   │
    │ buildtest version:  0.11.0                                                                                               │
    │ python path:        /bin/python                                                                                          │
    │ python version:     3.7.11                                                                                               │
    │ Configuration File: /tmp/tests/settings/pbs.yml                                                                          │
    │ Test Directory:     /tmp/var/tests                                                                                       │
    │ Command:            /tmp/bin/buildtest -c tests/settings/pbs.yml build -b tests/examples/pbs/sleep.yml --pollinterval=5 │
    │                                                                                                                          │
    ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
    ─────────────────────────────────────────────────────────────────────────  Discovering Buildspecs ──────────────────────────────────────────────────────────────────────────
    Discovered Buildspecs:  1
    Excluded Buildspecs:  0
    Detected Buildspecs after exclusion:  1
            Discovered buildspecs
    ╔═══════════════════════════════════╗
    ║ Buildspecs                        ║
    ╟───────────────────────────────────╢
    ║ /tmp/tests/examples/pbs/sleep.yml ║
    ╚═══════════════════════════════════╝
    ──────────────────────────────────────────────────────────────────────────── Parsing Buildspecs ────────────────────────────────────────────────────────────────────────────
    Valid Buildspecs: 1
    Invalid Buildspecs: 0
    /tmp/tests/examples/pbs/sleep.yml: VALID


    Total builder objects created: 1


                                          Builder Details
    ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Builder            ┃ Executor          ┃ description ┃ buildspecs                        ┃
    ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ pbs_sleep/c7bc6a9c │ generic.pbs.workq │             │ /tmp/tests/examples/pbs/sleep.yml │
    └────────────────────┴───────────────────┴─────────────┴───────────────────────────────────┘
    ────────────────────────────────────────────────────────────────────────────── Building Test ───────────────────────────────────────────────────────────────────────────────
    [16:59:34] pbs_sleep/c7bc6a9c: Creating test directory - /tmp/var/tests/generic.pbs.workq/sleep/pbs_sleep/c7bc6a9c                                               base.py:440
               pbs_sleep/c7bc6a9c: Creating stage directory - /tmp/var/tests/generic.pbs.workq/sleep/pbs_sleep/c7bc6a9c/stage                                        base.py:450
               pbs_sleep/c7bc6a9c: Writing build script: /tmp/var/tests/generic.pbs.workq/sleep/pbs_sleep/c7bc6a9c/pbs_sleep_build.sh                                base.py:567
    ────────────────────────────────────────────────────────────────────────────── Running Tests ───────────────────────────────────────────────────────────────────────────────
    ______________________________
    Launching test: pbs_sleep/c7bc6a9c
    pbs_sleep/c7bc6a9c: Running Test script /tmp/var/tests/generic.pbs.workq/sleep/pbs_sleep/c7bc6a9c/pbs_sleep_build.sh
    pbs.generic.pbs.workq: JobID: 0.pbs dispatched to scheduler
    Polling Jobs in 5 seconds
                                 Pending Jobs
    ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┓
    ┃ Builder            ┃ executor          ┃ JobID ┃ JobState ┃ runtime ┃
    ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━┩
    │ pbs_sleep/c7bc6a9c │ generic.pbs.workq │ 0.pbs │ R        │ 5.138   │
    └────────────────────┴───────────────────┴───────┴──────────┴─────────┘
    Polling Jobs in 5 seconds
    pbs_sleep/c7bc6a9c: Job 0.pbs is complete!
    pbs_sleep/c7bc6a9c: Writing output file -  /tmp/var/tests/generic.pbs.workq/sleep/pbs_sleep/c7bc6a9c/pbs_sleep.o0
    pbs_sleep/c7bc6a9c: Writing error file - /tmp/var/tests/generic.pbs.workq/sleep/pbs_sleep/c7bc6a9c/pbs_sleep.e0
                       Pending Jobs
    ┏━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┓
    ┃ Builder ┃ executor ┃ JobID ┃ JobState ┃ runtime ┃
    ┡━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━┩
    └─────────┴──────────┴───────┴──────────┴─────────┘
                                 Completed Jobs
    ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━┓
    ┃ Builder            ┃ executor          ┃ JobID ┃ JobState ┃ runtime   ┃
    ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━┩
    │ pbs_sleep/c7bc6a9c │ generic.pbs.workq │ 0.pbs │ F        │ 10.173252 │
    └────────────────────┴───────────────────┴───────┴──────────┴───────────┘
                                                       Test Summary
    ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━┓
    ┃ Builder            ┃ executor          ┃ status ┃ Checks (ReturnCode, Regex, Runtime) ┃ ReturnCode ┃ Runtime   ┃
    ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━┩
    │ pbs_sleep/c7bc6a9c │ generic.pbs.workq │ PASS   │ N/A N/A N/A                         │ 0          │ 10.173252 │
    └────────────────────┴───────────────────┴────────┴─────────────────────────────────────┴────────────┴───────────┘



    Passed Tests: 1/1 Percentage: 100.000%
    Failed Tests: 0/1 Percentage: 0.000%


    Writing Logfile to: /tmp/buildtest_fgm9gtu2.log
    A copy of logfile can be found at $BUILDTEST_ROOT/buildtest.log -  /tmp/buildtest.log

Cobalt
-------

`Cobalt <https://trac.mcs.anl.gov/projects/cobalt>`_ is a job scheduler developed
by `Argonne National Laboratory <https://www.anl.gov/>`_ that runs on compute
resources and IBM BlueGene series. Cobalt resembles `PBS <https://www.altair.com/pbs-works-documentation/>`_
in terms of command line interface such as ``qsub``, ``qacct`` however they
slightly differ in their behavior.

Cobalt support has been tested on JLSE and `Theta <https://www.alcf.anl.gov/support-center/theta>`_
system. Cobalt directives are specified using ``#COBALT`` this can be specified
using ``cobalt`` property which accepts a list of strings. Shown below is an example
using cobalt property.

.. code-block:: yaml
    :emphasize-lines: 6
    :linenos:

    version: "1.0"
    buildspecs:
      yarrow_hostname:
        executor: jlse.cobalt.yarrow
        type: script
        cobalt: ["-n 1", "--proccount 1", "-t 10"]
        run: hostname

In this example, we allocate 1 node with 1 processor for 10min. This is translated into
the following job script.

.. code-block:: console

    #!/usr/bin/bash
    #COBALT -n 1
    #COBALT --proccount 1
    #COBALT -t 10
    #COBALT --jobname yarrow_hostname
    source /home/shahzebsiddiqui/buildtest/var/executors/cobalt.yarrow/before_script.sh
    hostname
    source /home/shahzebsiddiqui/buildtest/var/executors/cobalt.yarrow/after_script.sh

When job starts, Cobalt will write a cobalt log file ``<JOBID>.cobaltlog`` which
is provided by scheduler for troubleshooting. The output and error file are generated
once job finishes. Cobalt job progresses through job state ``starting`` --> ``pending`` --> ``running`` --> ``exiting``.
buildtest will capture Cobalt job details using ``qstat -lf <JOBID>`` and this
is updated in the report file.

buildtest will poll job at set interval, where we run ``qstat --header State <JobID>`` to
check state of job, if job is finished then we gather results. Once job is finished,
qstat will not be able to poll job this causes an issue where buildtest can't poll
job since qstat will not return anything. This is a transient issue depending on when
you poll job, generally at ALCF qstat will not report existing job within 30sec after
job is terminated. buildtest will assume if it's able to poll job and is in `exiting`
stage that job is complete, if its unable to retrieve this state we check for
output and error file. If file exists we assume job is complete and buildtest will
gather the results.

buildtest will determine exit code by parsing cobalt log file, the file contains a line
such as ::

    Thu Nov 05 17:29:30 2020 +0000 (UTC) Info: task completed normally with an exit code of 0; initiating job cleanup and removal

qstat has no job record for capturing returncode so buildtest must rely on Cobalt Log file.

.. _max_pend_time:

Jobs exceeds `max_pend_time`
-----------------------------

Recall from :ref:`configuring_buildtest` that `max_pend_time` will cancel jobs if
job exceed timelimit. buildtest will start a timer for each job right after job
submission and keep track of time duration, and if job is in **pending** state and it exceeds `max_pend_time`,
then job will be cancelled.

We can also override `max_pend_time` configuration via command line ``--maxpendtime``.
To demonstrate, here is an example where job  was cancelled after job was pending and exceeds `max_pend_time`.
Note that cancelled job is not reported in final output nor updated in report hence
it won't be present in the report (``buildtest report``). In this example, we only
had one test so upon job cancellation we found there was no tests to report hence,
buildtest will terminate after run stage.

.. code-block:: console

    [pbsuser@pbs tmp]$ buildtest -c tests/settings/pbs.yml build -b tests/examples/pbs/hold.yml --pollinterval=3 --maxpendtime=5
    ╭──────────────────────────────────────────────────────────── buildtest summary ────────────────────────────────────────────────────────────╮
    │                                                                                                                                           │
    │ User:               pbsuser                                                                                                               │
    │ Hostname:           pbs                                                                                                                   │
    │ Platform:           Linux                                                                                                                 │
    │ Current Time:       2021/10/13 17:00:51                                                                                                   │
    │ buildtest path:     /tmp/bin/buildtest                                                                                                    │
    │ buildtest version:  0.11.0                                                                                                                │
    │ python path:        /bin/python                                                                                                           │
    │ python version:     3.7.11                                                                                                                │
    │ Configuration File: /tmp/tests/settings/pbs.yml                                                                                           │
    │ Test Directory:     /tmp/var/tests                                                                                                        │
    │ Command:            /tmp/bin/buildtest -c tests/settings/pbs.yml build -b tests/examples/pbs/hold.yml --pollinterval=3 --maxpendtime=5 │
    │                                                                                                                                           │
    ╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
    ─────────────────────────────────────────────────────────────────────────  Discovering Buildspecs ──────────────────────────────────────────────────────────────────────────
    Discovered Buildspecs:  1
    Excluded Buildspecs:  0
    Detected Buildspecs after exclusion:  1
           Discovered buildspecs
    ╔══════════════════════════════════╗
    ║ Buildspecs                       ║
    ╟──────────────────────────────────╢
    ║ /tmp/tests/examples/pbs/hold.yml ║
    ╚══════════════════════════════════╝
    ──────────────────────────────────────────────────────────────────────────── Parsing Buildspecs ────────────────────────────────────────────────────────────────────────────
    Valid Buildspecs: 1
    Invalid Buildspecs: 0
    /tmp/tests/examples/pbs/hold.yml: VALID


    Total builder objects created: 1


                                            Builder Details
    ┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Builder               ┃ Executor          ┃ description  ┃ buildspecs                       ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ pbs_hold_job/7cbe643c │ generic.pbs.workq │ PBS Hold Job │ /tmp/tests/examples/pbs/hold.yml │
    └───────────────────────┴───────────────────┴──────────────┴──────────────────────────────────┘
    ────────────────────────────────────────────────────────────────────────────── Building Test ───────────────────────────────────────────────────────────────────────────────
    [17:00:51] pbs_hold_job/7cbe643c: Creating test directory - /tmp/var/tests/generic.pbs.workq/hold/pbs_hold_job/7cbe643c                                          base.py:440
               pbs_hold_job/7cbe643c: Creating stage directory - /tmp/var/tests/generic.pbs.workq/hold/pbs_hold_job/7cbe643c/stage                                   base.py:450
               pbs_hold_job/7cbe643c: Writing build script: /tmp/var/tests/generic.pbs.workq/hold/pbs_hold_job/7cbe643c/pbs_hold_job_build.sh                        base.py:567
    ────────────────────────────────────────────────────────────────────────────── Running Tests ───────────────────────────────────────────────────────────────────────────────
    ______________________________
    Launching test: pbs_hold_job/7cbe643c
    pbs_hold_job/7cbe643c: Running Test script /tmp/var/tests/generic.pbs.workq/hold/pbs_hold_job/7cbe643c/pbs_hold_job_build.sh
    pbs.generic.pbs.workq: JobID: 1.pbs dispatched to scheduler
    Polling Jobs in 3 seconds
                                   Pending Jobs
    ┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┓
    ┃ Builder               ┃ executor          ┃ JobID ┃ JobState ┃ runtime ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━┩
    │ pbs_hold_job/7cbe643c │ generic.pbs.workq │ 1.pbs │ H        │ 3.143   │
    └───────────────────────┴───────────────────┴───────┴──────────┴─────────┘
    Polling Jobs in 3 seconds
    pbs_hold_job/7cbe643c: Cancelling Job: 1.pbs because job exceeds max pend time: 5 sec with current pend time of 6.176
                       Pending Jobs
    ┏━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┓
    ┃ Builder ┃ executor ┃ JobID ┃ JobState ┃ runtime ┃
    ┡━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━┩
    └─────────┴──────────┴───────┴──────────┴─────────┘

    Cancelled Jobs: [pbs_hold_job/7cbe643c]
    Unable to run any tests


Access PBS Container
---------------------

If you want to experiment with PBS Scheduler with buildtest, you can run the following to get in the
container. These instructions are outlined in https://openpbs.atlassian.net/wiki/spaces/PBSPro/pages/79298561/Using+Docker+to+Instantiate+PBS.
This container will start PBS and start an interactive shell as ``pbsuser``.

.. code-block:: console

    $ docker run -it --name pbs -h pbs -e PBS_START_MOM=1 pbspro/pbspro bash
    Starting PBS
    PBS Home directory /var/spool/pbs needs updating.
    Running /opt/pbs/libexec/pbs_habitat to update it.
    ***
    *** Setting default queue and resource limits.
    ***
    Connecting to PBS dataservice.....connected to PBS dataservice@pbs
    *** End of /opt/pbs/libexec/pbs_habitat
    Home directory /var/spool/pbs updated.
    /opt/pbs/sbin/pbs_comm ready (pid=1226), Proxy Name:pbs:17001, Threads:4
    PBS comm
    PBS mom
    Creating usage database for fairshare.
    PBS sched
    Connecting to PBS dataservice.....connected to PBS dataservice@pbs
    Licenses valid for 10000000 Floating hosts
    PBS server
    [pbsuser@pbs ~]$

Next we need to switch to **root** user to install additional packages. You can run **exit** and it will switch to root

.. code-block:: console

    [pbsuser@pbs ~]$ exit
    logout
    [root@pbs /]#

We need to install some basic system packages which were not provided in this container. Please run the following::

    yum install -y which git wget make gcc

We also need to configure PBS to enable job history which is required to poll PBS job. Please run the following::

    /opt/pbs/bin/qmgr -c "set server job_history_enable=True"


Now let's switch to `pbsuser`


.. code-block:: console

    [root@pbs /]# su - pbsuser
    Last login: Mon Jan 24 00:45:57 UTC 2022 on pts/0
    [pbsuser@pbs ~]$

As the pbsuser we will clone buildtest and setup the environment required to use pbs for the container.
Please run the following commands::

    git clone https://github.com/buildtesters/buildtest/
    source ~/buildtest/scripts/pbs/setup.sh

The example buildspecs for this container are located in directory `tests/examples/pbs <https://github.com/buildtesters/buildtest/tree/devel/tests/examples/pbs>`_,
if you want to run all of them you can run the following::

    buildtest build -b tests/examples/pbs
