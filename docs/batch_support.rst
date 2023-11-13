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
    :emphasize-lines: 5,7-9

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

.. dropdown:: ``buildtest build -b metadata.yml``

    .. code-block:: console

           buildtest build -b metadata.yml
        ╭───────────────────────────────────────── buildtest summary ─────────────────────────────────────────╮
        │                                                                                                     │
        │ User:               siddiq90                                                                        │
        │ Hostname:           cori05                                                                          │
        │ Platform:           Linux                                                                           │
        │ Current Time:       2022/10/11 13:00:37                                                             │
        │ buildtest path:     /global/homes/s/siddiq90/gitrepos/buildtest/bin/buildtest                       │
        │ buildtest version:  0.15.0                                                                          │
        │ python path:        /global/u1/s/siddiq90/.local/share/virtualenvs/buildtest-WqshQcL1/bin/python3   │
        │ python version:     3.9.7                                                                           │
        │ Configuration File: /global/u1/s/siddiq90/gitrepos/buildtest-nersc/config.yml                       │
        │ Test Directory:     /global/u1/s/siddiq90/gitrepos/buildtest/var/tests                              │
        │ Report File:        /global/u1/s/siddiq90/gitrepos/buildtest/var/report.json                        │
        │ Command:            /global/homes/s/siddiq90/gitrepos/buildtest/bin/buildtest build -b metadata.yml │
        │                                                                                                     │
        ╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯
        ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────  Discovering Buildspecs ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
                                     Discovered buildspecs
        ╔═════════════════════════════════════════════════════════════════════════════╗
        ║ buildspec                                                                   ║
        ╟─────────────────────────────────────────────────────────────────────────────╢
        ║ /global/u1/s/siddiq90/gitrepos/buildtest-nersc/buildspecs/jobs/metadata.yml ║
        ╚═════════════════════════════════════════════════════════════════════════════╝


        Total Discovered Buildspecs:  1
        Total Excluded Buildspecs:  0
        Detected Buildspecs after exclusion:  1
        ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── Parsing Buildspecs ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
        Buildtest will parse 1 buildspecs
        Valid Buildspecs: 1
        Invalid Buildspecs: 0
        /global/u1/s/siddiq90/gitrepos/buildtest-nersc/buildspecs/jobs/metadata.yml: VALID
        Total builder objects created: 1
        Total compiler builder: 0
        Total script builder: 1
        Total spack builder: 0
                                                                                                     Script Builder Details
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ builder                 ┃ executor             ┃ compiler ┃ nodes ┃ procs ┃ description                                        ┃ buildspecs                                                                  ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ slurm_metadata/9329516f │ cori.slurm.knl_debug │ None     │ None  │ None  │ Get metadata from compute node when submitting job │ /global/u1/s/siddiq90/gitrepos/buildtest-nersc/buildspecs/jobs/metadata.yml │
        └─────────────────────────┴──────────────────────┴──────────┴───────┴───────┴────────────────────────────────────────────────────┴─────────────────────────────────────────────────────────────────────────────┘
                                                               Batch Job Builders
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ builder                 ┃ executor             ┃ buildspecs                                                                  ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ slurm_metadata/9329516f │ cori.slurm.knl_debug │ /global/u1/s/siddiq90/gitrepos/buildtest-nersc/buildspecs/jobs/metadata.yml │
        └─────────────────────────┴──────────────────────┴─────────────────────────────────────────────────────────────────────────────┘
        ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── Building Test ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
        slurm_metadata/9329516f: Creating test directory: /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/metadata/slurm_metadata/9329516f
        slurm_metadata/9329516f: Creating the stage directory: /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/metadata/slurm_metadata/9329516f/stage
        slurm_metadata/9329516f: Writing build script: /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/metadata/slurm_metadata/9329516f/slurm_metadata_build.sh
        ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── Running Tests ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
        Spawning 64 processes for processing builders
        ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── Iteration 1 ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
        slurm_metadata/9329516f does not have any dependencies adding test to queue
        In this iteration we are going to run the following tests: [slurm_metadata/9329516f]
        slurm_metadata/9329516f: Running Test via command: bash --norc --noprofile -eo pipefail slurm_metadata_build.sh
        slurm_metadata/9329516f: JobID 63477998 dispatched to scheduler
        Polling Jobs in 30 seconds
        slurm_metadata/9329516f: Job 63477998 is complete!
        slurm_metadata/9329516f: Test completed in 31.963472 seconds
        slurm_metadata/9329516f: Test completed with returncode: 0
        slurm_metadata/9329516f: Writing output file -  /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/metadata/slurm_metadata/9329516f/slurm_metadata.out
        slurm_metadata/9329516f: Writing error file - /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/metadata/slurm_metadata/9329516f/slurm_metadata.err
                                           Completed Jobs
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┓
        ┃ builder                 ┃ executor             ┃ jobid    ┃ jobstate  ┃ runtime   ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━┩
        │ slurm_metadata/9329516f │ cori.slurm.knl_debug │ 63477998 │ COMPLETED │ 31.963472 │
        └─────────────────────────┴──────────────────────┴──────────┴───────────┴───────────┘
                                                               Test Summary
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━┓
        ┃ builder                 ┃ executor             ┃ status ┃ checks (ReturnCode, Regex, Runtime) ┃ returnCode ┃ runtime   ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━┩
        │ slurm_metadata/9329516f │ cori.slurm.knl_debug │ PASS   │ N/A N/A N/A                         │ 0          │ 31.963472 │
        └─────────────────────────┴──────────────────────┴────────┴─────────────────────────────────────┴────────────┴───────────┘



        Passed Tests: 1/1 Percentage: 100.000%
        Failed Tests: 0/1 Percentage: 0.000%


        Adding 1 test results to /global/u1/s/siddiq90/gitrepos/buildtest/var/report.json
        Writing Logfile to: /global/u1/s/siddiq90/gitrepos/buildtest/var/logs/buildtest_o3rpx3zs.log



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
    :emphasize-lines: 7-8

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

.. dropdown:: ``buildtest build -b buildspecs/jobs/fail/timeout.yml``

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

buildtest can support job submission to `PBS Pro <https://community.altair.com/community?id=altair_product_documentation>`_ or `OpenPBS <https://openpbs.atlassian.net/wiki/spaces/PBSPro/overview>`_
scheduler. Assuming you have configured :ref:`pbs_executors` in your configuration file you can submit jobs
to the PBS executor by selecting the appropriate pbs executor via ``executor`` property in buildspec. The ``#PBS``
directives can be specified using ``pbs`` field which is a list of PBS options that get inserted at top of script. Shown
below is an example buildspec using the `script` schema.

.. literalinclude:: ../tests/examples/pbs/sleep.yml
   :emphasize-lines: 5
   :language: yaml

buildtest will poll PBS jobs using ``qstat -x -f -F json <jobID>`` until job is finished. Note that
we use **-x** option to retrieve finished jobs which is required in-order for buildtest to detect job
state upon completion.

Shown below is an example build of the buildspec using PBS scheduler and polling job every 2 seconds.

.. dropdown:: ``buildtest build -b tests/examples/pbs/sleep.yml  --pollinterval=2``

    .. code-block:: console

        (buildtest) -bash-4.2$ buildtest build -b tests/examples/pbs/sleep.yml --pollinterval=2
        ╭─────────────────────────────────────────────── buildtest summary ────────────────────────────────────────────────╮
        │                                                                                                                  │
        │ User:               pbsuser                                                                                      │
        │ Hostname:           pbs                                                                                          │
        │ Platform:           Linux                                                                                        │
        │ Current Time:       2023/10/03 18:14:44                                                                          │
        │ buildtest path:     /home/pbsuser/buildtest/bin/buildtest                                                        │
        │ buildtest version:  1.6                                                                                          │
        │ python path:        /home/pbsuser/miniconda/bin/python3                                                          │
        │ python version:     3.11.4                                                                                       │
        │ Configuration File: /home/pbsuser/buildtest/tests/settings/pbs.yml                                               │
        │ Test Directory:     /home/pbsuser/buildtest/var/tests                                                            │
        │ Report File:        /home/pbsuser/buildtest/var/report.json                                                      │
        │ Command:            /home/pbsuser/buildtest/bin/buildtest build -b tests/examples/pbs/sleep.yml --pollinterval=2 │
        │                                                                                                                  │
        ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
        ───────────────────────────────────────────────────────────────────────────────────────────────────────  Discovering Buildspecs ────────────────────────────────────────────────────────────────────────────────────────────────────────
                         Discovered buildspecs
        ╔══════════════════════════════════════════════════════╗
        ║ buildspec                                            ║
        ╟──────────────────────────────────────────────────────╢
        ║ /home/pbsuser/buildtest/tests/examples/pbs/sleep.yml ║
        ╚══════════════════════════════════════════════════════╝


        Total Discovered Buildspecs:  1
        Total Excluded Buildspecs:  0
        Detected Buildspecs after exclusion:  1
        ────────────────────────────────────────────────────────────────────────────────────────────────────────── Parsing Buildspecs ──────────────────────────────────────────────────────────────────────────────────────────────────────────
        Valid Buildspecs: 1
        Invalid Buildspecs: 0
        /home/pbsuser/buildtest/tests/examples/pbs/sleep.yml: VALID
        Total builder objects created: 1
                                                                      Builders by type=script
        ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ builder            ┃ type   ┃ executor          ┃ compiler ┃ nodes ┃ procs ┃ description ┃ buildspecs                                           ┃
        ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ pbs_sleep/55acd305 │ script │ generic.pbs.workq │ None     │ None  │ None  │             │ /home/pbsuser/buildtest/tests/examples/pbs/sleep.yml │
        └────────────────────┴────────┴───────────────────┴──────────┴───────┴───────┴─────────────┴──────────────────────────────────────────────────────┘
                                               Batch Job Builders
        ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ builder            ┃ executor          ┃ buildspecs                                           ┃
        ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ pbs_sleep/55acd305 │ generic.pbs.workq │ /home/pbsuser/buildtest/tests/examples/pbs/sleep.yml │
        └────────────────────┴───────────────────┴──────────────────────────────────────────────────────┘
        ──────────────────────────────────────────────────────────────────────────────────────────────────────────── Building Test ─────────────────────────────────────────────────────────────────────────────────────────────────────────────
        pbs_sleep/55acd305: Creating test directory: /home/pbsuser/buildtest/var/tests/generic.pbs.workq/sleep/pbs_sleep/55acd305
        pbs_sleep/55acd305: Creating the stage directory: /home/pbsuser/buildtest/var/tests/generic.pbs.workq/sleep/pbs_sleep/55acd305/stage
        pbs_sleep/55acd305: Writing build script: /home/pbsuser/buildtest/var/tests/generic.pbs.workq/sleep/pbs_sleep/55acd305/pbs_sleep_build.sh
        ──────────────────────────────────────────────────────────────────────────────────────────────────────────── Running Tests ─────────────────────────────────────────────────────────────────────────────────────────────────────────────
        Spawning 1 processes for processing builders
        ───────────────────────────────────────────────────────────────────────────────────────────────────────────── Iteration 1 ──────────────────────────────────────────────────────────────────────────────────────────────────────────────
        pbs_sleep/55acd305 does not have any dependencies adding test to queue
        Builders Eligible to Run
        ┏━━━━━━━━━━━━━━━━━━━━┓
        ┃ Builder            ┃
        ┡━━━━━━━━━━━━━━━━━━━━┩
        │ pbs_sleep/55acd305 │
        └────────────────────┘
        pbs_sleep/55acd305: Current Working Directory : /home/pbsuser/buildtest/var/tests/generic.pbs.workq/sleep/pbs_sleep/55acd305/stage
        pbs_sleep/55acd305: Running Test via command: bash --norc --noprofile -eo pipefail pbs_sleep_build.sh
        pbs_sleep/55acd305: JobID: 28.pbs dispatched to scheduler
        Polling Jobs in 2 seconds
                                                  Running Jobs
        ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
        ┃ builder            ┃ executor          ┃ jobid  ┃ jobstate ┃ runtime ┃ elapsedtime ┃ pendtime ┃
        ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
        │ pbs_sleep/55acd305 │ generic.pbs.workq │ 28.pbs │ R        │ 2.037   │ 0.0         │ 0        │
        └────────────────────┴───────────────────┴────────┴──────────┴─────────┴─────────────┴──────────┘
        Polling Jobs in 2 seconds
                                                  Running Jobs
        ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
        ┃ builder            ┃ executor          ┃ jobid  ┃ jobstate ┃ runtime ┃ elapsedtime ┃ pendtime ┃
        ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
        │ pbs_sleep/55acd305 │ generic.pbs.workq │ 28.pbs │ R        │ 4.055   │ 2.02        │ 0        │
        └────────────────────┴───────────────────┴────────┴──────────┴─────────┴─────────────┴──────────┘
        Polling Jobs in 2 seconds
        pbs_sleep/55acd305: Job 28.pbs is complete!
        pbs_sleep/55acd305: Test completed in 2.02 seconds
        pbs_sleep/55acd305: Test completed with returncode: 0
        pbs_sleep/55acd305: Writing output file -  /home/pbsuser/buildtest/var/tests/generic.pbs.workq/sleep/pbs_sleep/55acd305/pbs_sleep.o28
        pbs_sleep/55acd305: Writing error file - /home/pbsuser/buildtest/var/tests/generic.pbs.workq/sleep/pbs_sleep/55acd305/pbs_sleep.e28
                                                 Completed Jobs
        ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
        ┃ builder            ┃ executor          ┃ jobid  ┃ jobstate ┃ runtime ┃ elapsedtime ┃ pendtime ┃
        ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
        │ pbs_sleep/55acd305 │ generic.pbs.workq │ 28.pbs │ F        │ 2.02    │ 2.02        │ 0        │
        └────────────────────┴───────────────────┴────────┴──────────┴─────────┴─────────────┴──────────┘
                                                          Test Summary
        ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━┓
        ┃ builder            ┃ executor          ┃ status ┃ checks (ReturnCode, Regex, Runtime) ┃ returncode ┃ runtime ┃
        ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━┩
        │ pbs_sleep/55acd305 │ generic.pbs.workq │ PASS   │ None None None                      │ 0          │ 2.02    │
        └────────────────────┴───────────────────┴────────┴─────────────────────────────────────┴────────────┴─────────┘



        Passed Tests: 1/1 Percentage: 100.000%
        Failed Tests: 0/1 Percentage: 0.000%


        Adding 1 test results to /home/pbsuser/buildtest/var/report.json
        Writing Logfile to: /home/pbsuser/buildtest/var/logs/buildtest_eafhrjlu.log

buildtest can determine status of test based on PBS Job State. This can be configured via ``pbs_job_state`` property
that is an attribute of **status** field. The ``pbs_job_state`` can be one of three values **H**, **S**, **F**. ``H`` refers to Job Held, ``S`` refers
to suspended job and ``F`` refers to Finished job. Please see **Table 8-1: Job States** in https://2021.help.altair.com/2021.1.2/PBS%20Professional/PBSReferenceGuide2021.1.2.pdf.

In example below we simulate a failed job by expecting job to be in Hold state (``H``) however job will finish with a job state of ``F``. buildtest will match
the actual job state reported by PBS and value of ``pbs_job_state``, if there is a match we will report a ``PASS`` otherwise job will be a ``FAIL``.

.. literalinclude:: ../tests/examples/pbs/pbs_job_state.yml
   :language: yaml

Let's run this example and notice that this job ran to completion but it was reported as **FAIL**

.. dropdown:: ``buildtest bd -b tests/examples/pbs/pbs_job_state.yml --pollinterval=2``

    .. code-block:: console

        (buildtest) -bash-4.2$ buildtest bd -b tests/examples/pbs/pbs_job_state.yml --pollinterval=2
        ╭────────────────────────────────────────────────── buildtest summary ──────────────────────────────────────────────────╮
        │                                                                                                                       │
        │ User:               pbsuser                                                                                           │
        │ Hostname:           pbs                                                                                               │
        │ Platform:           Linux                                                                                             │
        │ Current Time:       2023/10/03 18:18:08                                                                               │
        │ buildtest path:     /home/pbsuser/buildtest/bin/buildtest                                                             │
        │ buildtest version:  1.6                                                                                               │
        │ python path:        /home/pbsuser/miniconda/bin/python3                                                               │
        │ python version:     3.11.4                                                                                            │
        │ Configuration File: /home/pbsuser/buildtest/tests/settings/pbs.yml                                                    │
        │ Test Directory:     /home/pbsuser/buildtest/var/tests                                                                 │
        │ Report File:        /home/pbsuser/buildtest/var/report.json                                                           │
        │ Command:            /home/pbsuser/buildtest/bin/buildtest bd -b tests/examples/pbs/pbs_job_state.yml --pollinterval=2 │
        │                                                                                                                       │
        ╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
        ───────────────────────────────────────────────────────────────────────────────────────────────────────  Discovering Buildspecs ────────────────────────────────────────────────────────────────────────────────────────────────────────
                             Discovered buildspecs
        ╔══════════════════════════════════════════════════════════════╗
        ║ buildspec                                                    ║
        ╟──────────────────────────────────────────────────────────────╢
        ║ /home/pbsuser/buildtest/tests/examples/pbs/pbs_job_state.yml ║
        ╚══════════════════════════════════════════════════════════════╝


        Total Discovered Buildspecs:  1
        Total Excluded Buildspecs:  0
        Detected Buildspecs after exclusion:  1
        ────────────────────────────────────────────────────────────────────────────────────────────────────────── Parsing Buildspecs ──────────────────────────────────────────────────────────────────────────────────────────────────────────
        Valid Buildspecs: 1
        Invalid Buildspecs: 0
        /home/pbsuser/buildtest/tests/examples/pbs/pbs_job_state.yml: VALID
        Total builder objects created: 1
                                                                                     Builders by type=script
        ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ builder            ┃ type   ┃ executor          ┃ compiler ┃ nodes ┃ procs ┃ description                       ┃ buildspecs                                                   ┃
        ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ pbs_sleep/d6381a95 │ script │ generic.pbs.workq │ None     │ None  │ None  │ pass test based on PBS job state. │ /home/pbsuser/buildtest/tests/examples/pbs/pbs_job_state.yml │
        └────────────────────┴────────┴───────────────────┴──────────┴───────┴───────┴───────────────────────────────────┴──────────────────────────────────────────────────────────────┘
                                                   Batch Job Builders
        ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ builder            ┃ executor          ┃ buildspecs                                                   ┃
        ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ pbs_sleep/d6381a95 │ generic.pbs.workq │ /home/pbsuser/buildtest/tests/examples/pbs/pbs_job_state.yml │
        └────────────────────┴───────────────────┴──────────────────────────────────────────────────────────────┘
        ──────────────────────────────────────────────────────────────────────────────────────────────────────────── Building Test ─────────────────────────────────────────────────────────────────────────────────────────────────────────────
        pbs_sleep/d6381a95: Creating test directory: /home/pbsuser/buildtest/var/tests/generic.pbs.workq/pbs_job_state/pbs_sleep/d6381a95
        pbs_sleep/d6381a95: Creating the stage directory: /home/pbsuser/buildtest/var/tests/generic.pbs.workq/pbs_job_state/pbs_sleep/d6381a95/stage
        pbs_sleep/d6381a95: Writing build script: /home/pbsuser/buildtest/var/tests/generic.pbs.workq/pbs_job_state/pbs_sleep/d6381a95/pbs_sleep_build.sh
        ──────────────────────────────────────────────────────────────────────────────────────────────────────────── Running Tests ─────────────────────────────────────────────────────────────────────────────────────────────────────────────
        Spawning 1 processes for processing builders
        ───────────────────────────────────────────────────────────────────────────────────────────────────────────── Iteration 1 ──────────────────────────────────────────────────────────────────────────────────────────────────────────────
        pbs_sleep/d6381a95 does not have any dependencies adding test to queue
        Builders Eligible to Run
        ┏━━━━━━━━━━━━━━━━━━━━┓
        ┃ Builder            ┃
        ┡━━━━━━━━━━━━━━━━━━━━┩
        │ pbs_sleep/d6381a95 │
        └────────────────────┘
        pbs_sleep/d6381a95: Current Working Directory : /home/pbsuser/buildtest/var/tests/generic.pbs.workq/pbs_job_state/pbs_sleep/d6381a95/stage
        pbs_sleep/d6381a95: Running Test via command: bash --norc --noprofile -eo pipefail pbs_sleep_build.sh
        pbs_sleep/d6381a95: JobID: 32.pbs dispatched to scheduler
        Polling Jobs in 2 seconds
                                                  Running Jobs
        ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
        ┃ builder            ┃ executor          ┃ jobid  ┃ jobstate ┃ runtime ┃ elapsedtime ┃ pendtime ┃
        ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
        │ pbs_sleep/d6381a95 │ generic.pbs.workq │ 32.pbs │ R        │ 2.07    │ 0.0         │ 0        │
        └────────────────────┴───────────────────┴────────┴──────────┴─────────┴─────────────┴──────────┘
        Polling Jobs in 2 seconds
                                                  Running Jobs
        ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
        ┃ builder            ┃ executor          ┃ jobid  ┃ jobstate ┃ runtime ┃ elapsedtime ┃ pendtime ┃
        ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
        │ pbs_sleep/d6381a95 │ generic.pbs.workq │ 32.pbs │ R        │ 4.095   │ 2.03        │ 0        │
        └────────────────────┴───────────────────┴────────┴──────────┴─────────┴─────────────┴──────────┘
        Polling Jobs in 2 seconds
        pbs_sleep/d6381a95: Job 32.pbs is complete!
        pbs_sleep/d6381a95: Test completed in 2.03 seconds
        pbs_sleep/d6381a95: Test completed with returncode: 0
        pbs_sleep/d6381a95: Writing output file -  /home/pbsuser/buildtest/var/tests/generic.pbs.workq/pbs_job_state/pbs_sleep/d6381a95/pbs_sleep.o32
        pbs_sleep/d6381a95: Writing error file - /home/pbsuser/buildtest/var/tests/generic.pbs.workq/pbs_job_state/pbs_sleep/d6381a95/pbs_sleep.e32
                                                 Completed Jobs
        ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
        ┃ builder            ┃ executor          ┃ jobid  ┃ jobstate ┃ runtime ┃ elapsedtime ┃ pendtime ┃
        ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
        │ pbs_sleep/d6381a95 │ generic.pbs.workq │ 32.pbs │ F        │ 2.03    │ 2.03        │ 0        │
        └────────────────────┴───────────────────┴────────┴──────────┴─────────┴─────────────┴──────────┘
                                                          Test Summary
        ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━┓
        ┃ builder            ┃ executor          ┃ status ┃ checks (ReturnCode, Regex, Runtime) ┃ returncode ┃ runtime ┃
        ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━┩
        │ pbs_sleep/d6381a95 │ generic.pbs.workq │ FAIL   │ None None None                      │ 0          │ 2.03    │
        └────────────────────┴───────────────────┴────────┴─────────────────────────────────────┴────────────┴─────────┘



        Passed Tests: 0/1 Percentage: 0.000%
        Failed Tests: 1/1 Percentage: 100.000%


        Adding 1 test results to /home/pbsuser/buildtest/var/report.json
        Writing Logfile to: /home/pbsuser/buildtest/var/logs/buildtest_8jpykfg9.log


Cobalt
-------

`Cobalt <https://trac.mcs.anl.gov/projects/cobalt>`_ is a job scheduler developed
by `Argonne National Laboratory <https://www.anl.gov/>`_ that runs on compute
resources and IBM BlueGene series. Cobalt resembles `PBS <https://community.altair.com/community?id=altair_product_documentation>`_
in terms of command line interface such as ``qsub``, ``qacct`` however they
slightly differ in their behavior.

Cobalt support has been tested on JLSE and `Theta <https://www.alcf.anl.gov/support-center/theta>`_
system. Cobalt directives are specified using ``#COBALT`` this can be specified
using ``cobalt`` property which accepts a list of strings. Shown below is an example
using cobalt property.

.. code-block:: yaml
    :emphasize-lines: 5
    :linenos:

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

.. dropdown:: ``buildtest build -b tests/examples/pbs/hold.yml --pollinterval=3 --maxpendtime=5``

    .. code-block:: console

        (buildtest) -bash-4.2$ buildtest build -b tests/examples/pbs/hold.yml --pollinterval=3 --maxpendtime=5
        ╭─────────────────────────────────────────────────────── buildtest summary ───────────────────────────────────────────────────────╮
        │                                                                                                                                 │
        │ User:               pbsuser                                                                                                     │
        │ Hostname:           pbs                                                                                                         │
        │ Platform:           Linux                                                                                                       │
        │ Current Time:       2023/10/03 18:19:48                                                                                         │
        │ buildtest path:     /home/pbsuser/buildtest/bin/buildtest                                                                       │
        │ buildtest version:  1.6                                                                                                         │
        │ python path:        /home/pbsuser/miniconda/bin/python3                                                                         │
        │ python version:     3.11.4                                                                                                      │
        │ Configuration File: /home/pbsuser/buildtest/tests/settings/pbs.yml                                                              │
        │ Test Directory:     /home/pbsuser/buildtest/var/tests                                                                           │
        │ Report File:        /home/pbsuser/buildtest/var/report.json                                                                     │
        │ Command:            /home/pbsuser/buildtest/bin/buildtest build -b tests/examples/pbs/hold.yml --pollinterval=3 --maxpendtime=5 │
        │                                                                                                                                 │
        ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
        ───────────────────────────────────────────────────────────────────────────────────────────────────────  Discovering Buildspecs ────────────────────────────────────────────────────────────────────────────────────────────────────────
                         Discovered buildspecs
        ╔═════════════════════════════════════════════════════╗
        ║ buildspec                                           ║
        ╟─────────────────────────────────────────────────────╢
        ║ /home/pbsuser/buildtest/tests/examples/pbs/hold.yml ║
        ╚═════════════════════════════════════════════════════╝


        Total Discovered Buildspecs:  1
        Total Excluded Buildspecs:  0
        Detected Buildspecs after exclusion:  1
        ────────────────────────────────────────────────────────────────────────────────────────────────────────── Parsing Buildspecs ──────────────────────────────────────────────────────────────────────────────────────────────────────────
        Valid Buildspecs: 1
        Invalid Buildspecs: 0
        /home/pbsuser/buildtest/tests/examples/pbs/hold.yml: VALID
        Total builder objects created: 1
                                                                       Builders by type=script
        ┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ builder               ┃ type   ┃ executor          ┃ compiler ┃ nodes ┃ procs ┃ description  ┃ buildspecs                                          ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ pbs_hold_job/447c7fd9 │ script │ generic.pbs.workq │ None     │ None  │ None  │ PBS Hold Job │ /home/pbsuser/buildtest/tests/examples/pbs/hold.yml │
        └───────────────────────┴────────┴───────────────────┴──────────┴───────┴───────┴──────────────┴─────────────────────────────────────────────────────┘
                                                Batch Job Builders
        ┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ builder               ┃ executor          ┃ buildspecs                                          ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ pbs_hold_job/447c7fd9 │ generic.pbs.workq │ /home/pbsuser/buildtest/tests/examples/pbs/hold.yml │
        └───────────────────────┴───────────────────┴─────────────────────────────────────────────────────┘
        ──────────────────────────────────────────────────────────────────────────────────────────────────────────── Building Test ─────────────────────────────────────────────────────────────────────────────────────────────────────────────
        pbs_hold_job/447c7fd9: Creating test directory: /home/pbsuser/buildtest/var/tests/generic.pbs.workq/hold/pbs_hold_job/447c7fd9
        pbs_hold_job/447c7fd9: Creating the stage directory: /home/pbsuser/buildtest/var/tests/generic.pbs.workq/hold/pbs_hold_job/447c7fd9/stage
        pbs_hold_job/447c7fd9: Writing build script: /home/pbsuser/buildtest/var/tests/generic.pbs.workq/hold/pbs_hold_job/447c7fd9/pbs_hold_job_build.sh
        ──────────────────────────────────────────────────────────────────────────────────────────────────────────── Running Tests ─────────────────────────────────────────────────────────────────────────────────────────────────────────────
        Spawning 1 processes for processing builders
        ───────────────────────────────────────────────────────────────────────────────────────────────────────────── Iteration 1 ──────────────────────────────────────────────────────────────────────────────────────────────────────────────
        pbs_hold_job/447c7fd9 does not have any dependencies adding test to queue
        Builders Eligible to Run
        ┏━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ Builder               ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━┩
        │ pbs_hold_job/447c7fd9 │
        └───────────────────────┘
        pbs_hold_job/447c7fd9: Current Working Directory : /home/pbsuser/buildtest/var/tests/generic.pbs.workq/hold/pbs_hold_job/447c7fd9/stage
        pbs_hold_job/447c7fd9: Running Test via command: bash --norc --noprofile -eo pipefail pbs_hold_job_build.sh
        pbs_hold_job/447c7fd9: JobID: 33.pbs dispatched to scheduler
        Polling Jobs in 3 seconds
                                             Pending and Suspended Jobs
        ┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
        ┃ builder               ┃ executor          ┃ jobid  ┃ jobstate ┃ runtime ┃ elapsedtime ┃ pendtime ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
        │ pbs_hold_job/447c7fd9 │ generic.pbs.workq │ 33.pbs │ H        │ 3.059   │ 0           │ 2.99     │
        └───────────────────────┴───────────────────┴────────┴──────────┴─────────┴─────────────┴──────────┘
        Polling Jobs in 3 seconds
        pbs_hold_job/447c7fd9: Cancelling Job 33.pbs because job exceeds max pend time of 5 sec with current pend time of 6.02 sec
                                             Pending and Suspended Jobs
        ┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
        ┃ builder               ┃ executor          ┃ jobid  ┃ jobstate ┃ runtime ┃ elapsedtime ┃ pendtime ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
        │ pbs_hold_job/447c7fd9 │ generic.pbs.workq │ 33.pbs │ H        │ 6.088   │ 0           │ 6.02     │
        └───────────────────────┴───────────────────┴────────┴──────────┴─────────┴─────────────┴──────────┘
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

We need to configure PBS queue and enable job history to poll PBS job. Please run the following as root::

    qmgr -c "create node pbs"
    qmgr -c "set  node pbs queue=workq"
    qmgr -c "set server job_history_enable=True"


Please run the following, for some reason `/home/pbsuser` is owned by root where it should be owned by user **pbsuser**::

    chown pbsuser:pbsuser /home/pbsuser

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
