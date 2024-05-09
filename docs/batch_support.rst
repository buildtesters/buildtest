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

In this example we have a slurm executor ``perlmutter.slurm.debug``,
in addition we can specify **#SBATCH** directives using ``sbatch`` field.
The sbatch field is a list of string types, buildtest will
insert **#SBATCH** directive in front of each value.

Shown below is an example buildspec

.. code-block:: yaml
    :emphasize-lines: 5,7-10

    buildspecs:
      slurm_metadata:
        description: Get metadata from compute node when submitting job
        type: script
        executor: perlmutter.slurm.debug
        tags: [jobs]
        sbatch:
          - "-t 00:05"
          - "-N 1"
          - "-C cpu"
        run: |
          export SLURM_JOB_NAME="firstjob"
          echo "jobname:" $SLURM_JOB_NAME
          echo "slurmdb host:" $SLURMD_NODENAME
          echo "pid:" $SLURM_TASK_PID
          echo "submit host:" $SLURM_SUBMIT_HOST
          echo "nodeid:" $SLURM_NODEID
          echo "partition:" $SLURM_JOB_PARTITION


buildtest will add the ``#SBATCH`` directives at top of script followed by
content in the ``run`` section.  Take note, buildtest will
will the following lines that is determined by the name of test
- ``#SBATCH --job-name``
- ``#SBATCH --output``
- ``#SBATCH --error``


.. code-block:: shell
    :emphasize-lines: 2-7

    #!/usr/bin/bash
    #SBATCH -t 00:05
    #SBATCH -N 1
    #SBATCH -C cpu
    #SBATCH --job-name=slurm_metadata
    #SBATCH --output=slurm_metadata.out
    #SBATCH --error=slurm_metadata.err
    set -eo pipefail
    # Content of run section
    export SLURM_JOB_NAME="firstjob"
    echo "jobname:" $SLURM_JOB_NAME
    echo "slurmdb host:" $SLURMD_NODENAME
    echo "pid:" $SLURM_TASK_PID
    echo "submit host:" $SLURM_SUBMIT_HOST
    echo "nodeid:" $SLURM_NODEID
    echo "partition:" $SLURM_JOB_PARTITION


buildtest will dispatch the job to batch scheduler and poll
job until completion. During poll interval, buildtest will query the job state to determine if job is complete.
Buildtest will report the job state for all tests at each poll interval. Upon completion, buildtest will
gather the results and terminate.

Shown below is an example build for this test

.. dropdown:: ``buildtest build -b metadata.yml``

    .. code-block:: console

        (buildtest) siddiq90@login10> buildtest build -b metadata.yml
        ╭───────────────────────────────────────── buildtest summary ─────────────────────────────────────────╮
        │                                                                                                     │
        │ User:               siddiq90                                                                        │
        │ Hostname:           login10                                                                         │
        │ Platform:           Linux                                                                           │
        │ Current Time:       2023/11/07 16:39:31                                                             │
        │ buildtest path:     /global/homes/s/siddiq90/gitrepos/buildtest/bin/buildtest                       │
        │ buildtest version:  1.6                                                                             │
        │ python path:        /global/u1/s/siddiq90/.local/share/virtualenvs/buildtest-WqshQcL1/bin/python3   │
        │ python version:     3.9.7                                                                           │
        │ Configuration File: /global/u1/s/siddiq90/gitrepos/buildtest-nersc/config.yml                       │
        │ Test Directory:     /global/u1/s/siddiq90/gitrepos/buildtest/var/tests                              │
        │ Report File:        /global/u1/s/siddiq90/gitrepos/buildtest/var/report.json                        │
        │ Command:            /global/homes/s/siddiq90/gitrepos/buildtest/bin/buildtest build -b metadata.yml │
        │                                                                                                     │
        ╰─────────────────────────────────────────────────────────────────────────────────────────────────────╯
        ──────────────────────────────────────────────────────────  Discovering Buildspecs ───────────────────────────────────────────────────────────
                                     Discovered buildspecs
        ╔═════════════════════════════════════════════════════════════════════════════╗
        ║ buildspec                                                                   ║
        ╟─────────────────────────────────────────────────────────────────────────────╢
        ║ /global/u1/s/siddiq90/gitrepos/buildtest-nersc/buildspecs/jobs/metadata.yml ║
        ╚═════════════════════════════════════════════════════════════════════════════╝


        Total Discovered Buildspecs:  1
        Total Excluded Buildspecs:  0
        Detected Buildspecs after exclusion:  1
        ───────────────────────────────────────────────────────────── Parsing Buildspecs ─────────────────────────────────────────────────────────────
        Valid Buildspecs: 1
        Invalid Buildspecs: 0
        /global/u1/s/siddiq90/gitrepos/buildtest-nersc/buildspecs/jobs/metadata.yml: VALID
        Total builder objects created: 1
                                                                   Builders by type=script
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ builder                 ┃ type   ┃ executor               ┃ compiler ┃ nodes ┃ procs ┃ description              ┃ buildspecs               ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ slurm_metadata/07da5a5e │ script │ perlmutter.slurm.debug │ None     │ None  │ None  │ Get metadata from        │ /global/u1/s/siddiq90/gi │
        │                         │        │                        │          │       │       │ compute node when        │ trepos/buildtest-nersc/b │
        │                         │        │                        │          │       │       │ submitting job           │ uildspecs/jobs/metadata. │
        │                         │        │                        │          │       │       │                          │ yml                      │
        └─────────────────────────┴────────┴────────────────────────┴──────────┴───────┴───────┴──────────────────────────┴──────────────────────────┘
                                                                Batch Job Builders
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ builder                 ┃ executor               ┃ buildspecs                                                                  ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ slurm_metadata/07da5a5e │ perlmutter.slurm.debug │ /global/u1/s/siddiq90/gitrepos/buildtest-nersc/buildspecs/jobs/metadata.yml │
        └─────────────────────────┴────────────────────────┴─────────────────────────────────────────────────────────────────────────────┘
        ─────────────────────────────────────────────────────────────── Building Test ────────────────────────────────────────────────────────────────
        slurm_metadata/07da5a5e: Creating test directory: /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/perlmutter.slurm.debug/metadata/slurm_metadata/07da5a5e
        slurm_metadata/07da5a5e: Creating the stage directory: /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/perlmutter.slurm.debug/metadata/slurm_metadata/07da5a5e/stage
        slurm_metadata/07da5a5e: Writing build script: /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/perlmutter.slurm.debug/metadata/slurm_metadata/07da5a5e/slurm_metadata_build.sh
        ─────────────────────────────────────────────────────────────── Running Tests ────────────────────────────────────────────────────────────────
        Spawning 8 processes for processing builders
        ──────────────────────────────────────────────────────────────── Iteration 1 ─────────────────────────────────────────────────────────────────
        slurm_metadata/07da5a5e does not have any dependencies adding test to queue
         Builders Eligible to Run
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ Builder                 ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ slurm_metadata/07da5a5e │
        └─────────────────────────┘
        slurm_metadata/07da5a5e: Current Working Directory : /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/perlmutter.slurm.debug/metadata/slurm_metadata/07da5a5e/stage
        slurm_metadata/07da5a5e: Running Test via command: bash --norc --noprofile -eo pipefail slurm_metadata_build.sh
        slurm_metadata/07da5a5e: JobID 18004649 dispatched to scheduler
        Polling Jobs in 30 seconds
        slurm_metadata/07da5a5e: Job 18004649 is complete!
        slurm_metadata/07da5a5e: Test completed in 0 seconds
        slurm_metadata/07da5a5e: Test completed with returncode: 0
        slurm_metadata/07da5a5e: Writing output file -  /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/perlmutter.slurm.debug/metadata/slurm_metadata/07da5a5e/slurm_metadata.out
        slurm_metadata/07da5a5e: Writing error file - /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/perlmutter.slurm.debug/metadata/slurm_metadata/07da5a5e/slurm_metadata.err
                                                      Completed Jobs (1)
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
        ┃ builder                 ┃ executor               ┃ jobid    ┃ jobstate  ┃ runtime ┃ elapsedtime ┃ pendtime ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
        │ slurm_metadata/07da5a5e │ perlmutter.slurm.debug │ 18004649 │ COMPLETED │ 0       │ 0           │ 0        │
        └─────────────────────────┴────────────────────────┴──────────┴───────────┴─────────┴─────────────┴──────────┘
                                                               Test Summary
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━┓
        ┃ builder                 ┃ executor               ┃ status ┃ checks (ReturnCode, Regex, Runtime) ┃ returncode ┃ runtime ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━┩
        │ slurm_metadata/07da5a5e │ perlmutter.slurm.debug │ PASS   │ None None None                      │ 0          │ 0       │
        └─────────────────────────┴────────────────────────┴────────┴─────────────────────────────────────┴────────────┴─────────┘



        Passed Tests: 1/1 Percentage: 100.000%
        Failed Tests: 0/1 Percentage: 0.000%


        Adding 1 test results to /global/u1/s/siddiq90/gitrepos/buildtest/var/report.json
        Writing Logfile to: /global/u1/s/siddiq90/gitrepos/buildtest/var/logs/buildtest_hmh8u3tr.log


The **SlurmExecutor** class is responsible for processing slurm job that may include:
dispatch, poll, gather, or cancel job. The SlurmExecutor will gather job metrics
via `sacct <https://slurm.schedmd.com/sacct.html>`_.

buildtest can check status based on Slurm Job State, this is defined by ``State`` field
in sacct. In next example, we introduce field ``slurm_job_state`` which
is part of ``status`` field. This field expects one of the following values: ``[COMPLETED, FAILED, OUT_OF_MEMORY, TIMEOUT ]``
This is an example of simulating fail job by running an invalid command

.. code-block:: yaml
    :emphasize-lines: 8-10

    buildspecs:
      fail_job_state:
        type: script
        executor: '(perlmutter|muller).slurm.debug'
        sbatch: [ "-t '00:00:10'", "-n 1", "-C cpu"]
        description: "This job run an invalid command and match job with FAILED job state"
        tags: ["jobs", "fail"]
        run: xyz
        status:
          slurm_job_state: "FAILED"

Let's try building this test, take note of the job state and notice that this test will pass because the job
state matches the expected value defined by ``slurm_job_state`` field.

.. dropdown:: ``buildtest build -b failed_job_state.yml --pollinterval=10``

    .. code-block:: console

        (buildtest) siddiq90@login10> buildtest build -b failed_job_state.yml --pollinterval=10
        ╭────────────────────────────────────────────────────── buildtest summary ──────────────────────────────────────────────────────╮
        │                                                                                                                               │
        │ User:               siddiq90                                                                                                  │
        │ Hostname:           login10                                                                                                   │
        │ Platform:           Linux                                                                                                     │
        │ Current Time:       2023/11/07 16:54:40                                                                                       │
        │ buildtest path:     /global/homes/s/siddiq90/gitrepos/buildtest/bin/buildtest                                                 │
        │ buildtest version:  1.6                                                                                                       │
        │ python path:        /global/u1/s/siddiq90/.local/share/virtualenvs/buildtest-WqshQcL1/bin/python3                             │
        │ python version:     3.9.7                                                                                                     │
        │ Configuration File: /global/u1/s/siddiq90/gitrepos/buildtest-nersc/config.yml                                                 │
        │ Test Directory:     /global/u1/s/siddiq90/gitrepos/buildtest/var/tests                                                        │
        │ Report File:        /global/u1/s/siddiq90/gitrepos/buildtest/var/report.json                                                  │
        │ Command:            /global/homes/s/siddiq90/gitrepos/buildtest/bin/buildtest build -b failed_job_state.yml --pollinterval=10 │
        │                                                                                                                               │
        ╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
        ──────────────────────────────────────────────────────────  Discovering Buildspecs ───────────────────────────────────────────────────────────
                                         Discovered buildspecs
        ╔═════════════════════════════════════════════════════════════════════════════════════╗
        ║ buildspec                                                                           ║
        ╟─────────────────────────────────────────────────────────────────────────────────────╢
        ║ /global/u1/s/siddiq90/gitrepos/buildtest-nersc/buildspecs/jobs/failed_job_state.yml ║
        ╚═════════════════════════════════════════════════════════════════════════════════════╝


        Total Discovered Buildspecs:  1
        Total Excluded Buildspecs:  0
        Detected Buildspecs after exclusion:  1
        ───────────────────────────────────────────────────────────── Parsing Buildspecs ─────────────────────────────────────────────────────────────
        Valid Buildspecs: 1
        Invalid Buildspecs: 0
        /global/u1/s/siddiq90/gitrepos/buildtest-nersc/buildspecs/jobs/failed_job_state.yml: VALID
        Total builder objects created: 1
                                                                   Builders by type=script
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ builder                 ┃ type   ┃ executor               ┃ compiler ┃ nodes ┃ procs ┃ description              ┃ buildspecs               ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ fail_job_state/6ddbaab1 │ script │ perlmutter.slurm.debug │ None     │ None  │ None  │ This job run an invalid  │ /global/u1/s/siddiq90/gi │
        │                         │        │                        │          │       │       │ command and match job    │ trepos/buildtest-nersc/b │
        │                         │        │                        │          │       │       │ with FAILED job state    │ uildspecs/jobs/failed_jo │
        │                         │        │                        │          │       │       │                          │ b_state.yml              │
        └─────────────────────────┴────────┴────────────────────────┴──────────┴───────┴───────┴──────────────────────────┴──────────────────────────┘
                                                                    Batch Job Builders
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ builder                 ┃ executor               ┃ buildspecs                                                                          ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ fail_job_state/6ddbaab1 │ perlmutter.slurm.debug │ /global/u1/s/siddiq90/gitrepos/buildtest-nersc/buildspecs/jobs/failed_job_state.yml │
        └─────────────────────────┴────────────────────────┴─────────────────────────────────────────────────────────────────────────────────────┘
        ─────────────────────────────────────────────────────────────── Building Test ────────────────────────────────────────────────────────────────
        fail_job_state/6ddbaab1: Creating test directory: /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/perlmutter.slurm.debug/failed_job_state/fail_job_state/6ddbaab1
        fail_job_state/6ddbaab1: Creating the stage directory: /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/perlmutter.slurm.debug/failed_job_state/fail_job_state/6ddbaab1/stage
        fail_job_state/6ddbaab1: Writing build script: /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/perlmutter.slurm.debug/failed_job_state/fail_job_state/6ddbaab1/fail_job_state_build.sh
        ─────────────────────────────────────────────────────────────── Running Tests ────────────────────────────────────────────────────────────────
        Spawning 8 processes for processing builders
        ──────────────────────────────────────────────────────────────── Iteration 1 ─────────────────────────────────────────────────────────────────
        fail_job_state/6ddbaab1 does not have any dependencies adding test to queue
         Builders Eligible to Run
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ Builder                 ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ fail_job_state/6ddbaab1 │
        └─────────────────────────┘
        fail_job_state/6ddbaab1: Current Working Directory : /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/perlmutter.slurm.debug/failed_job_state/fail_job_state/6ddbaab1/stage
        fail_job_state/6ddbaab1: Running Test via command: bash --norc --noprofile -eo pipefail fail_job_state_build.sh
        fail_job_state/6ddbaab1: JobID 18005239 dispatched to scheduler
        Polling Jobs in 10 seconds
                                                      Running Jobs (1)
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
        ┃ builder                 ┃ executor               ┃ jobid    ┃ jobstate ┃ runtime ┃ elapsedtime ┃ pendtime ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
        │ fail_job_state/6ddbaab1 │ perlmutter.slurm.debug │ 18005239 │ RUNNING  │ 17.72   │ 0.0         │ 0        │
        └─────────────────────────┴────────────────────────┴──────────┴──────────┴─────────┴─────────────┴──────────┘
        Polling Jobs in 10 seconds
        fail_job_state/6ddbaab1: Job 18005239 is complete!
        fail_job_state/6ddbaab1: Test completed in 0.0 seconds
        fail_job_state/6ddbaab1: Test completed with returncode: 127
        fail_job_state/6ddbaab1: Writing output file -  /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/perlmutter.slurm.debug/failed_job_state/fail_job_state/6ddbaab1/fail_job_state.out
        fail_job_state/6ddbaab1: Writing error file - /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/perlmutter.slurm.debug/failed_job_state/fail_job_state/6ddbaab1/fail_job_state.err
                                                     Completed Jobs (1)
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
        ┃ builder                 ┃ executor               ┃ jobid    ┃ jobstate ┃ runtime ┃ elapsedtime ┃ pendtime ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
        │ fail_job_state/6ddbaab1 │ perlmutter.slurm.debug │ 18005239 │ FAILED   │ 0.0     │ 0.0         │ 0        │
        └─────────────────────────┴────────────────────────┴──────────┴──────────┴─────────┴─────────────┴──────────┘
                                                               Test Summary
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━┓
        ┃ builder                 ┃ executor               ┃ status ┃ checks (ReturnCode, Regex, Runtime) ┃ returncode ┃ runtime ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━┩
        │ fail_job_state/6ddbaab1 │ perlmutter.slurm.debug │ PASS   │ None None None                      │ 127        │ 0.0     │
        └─────────────────────────┴────────────────────────┴────────┴─────────────────────────────────────┴────────────┴─────────┘



        Passed Tests: 1/1 Percentage: 100.000%
        Failed Tests: 0/1 Percentage: 0.000%


        Adding 1 test results to /global/u1/s/siddiq90/gitrepos/buildtest/var/report.json
        Writing Logfile to: /global/u1/s/siddiq90/gitrepos/buildtest/var/logs/buildtest_7xc4urxe.log

LSF
----

buildtest can support job submission to `IBM Spectrum LSF <https://www.ibm.com/support/knowledgecenter/en/SSWRJV/product_welcome_spectrum_lsf.html>`_
if you have defined :ref:`lsf_executors` in your configuration file.

The ``bsub`` property can be used to  specify **#BSUB** directive into job script. This example
will use the executor ``summit.lsf.batch`` executor that was defined in buildtest configuration.

.. code-block:: yaml
    :emphasize-lines: 6

    buildspecs:
      hostname:
        type: script
        executor: summit.lsf.batch
        bsub: [ "-W 10",  "-nnodes 1"]
        run: jsrun hostname

The LSF Executor poll jobs and retrieve job state using ``bjobs`` command. Furthermore, we get the exit code and output
and error file for job upon completion. Once job is complete we extract several fields from the job records that is stored in
the test.

.. dropdown:: LSF Job Submission Example

    Shown below is an example job submission with LSF scheduler in debug mode on Summit. You will notice that the job is dispatched and polled via ``bjobs`` command. Furthermore, you
    will see the job state and job runtime in the output.

    .. code-block:: console

        (buildtest) [siddiq90@login1.summit summit]$ buildtest -d build -b hostname.yml --pollinterval=10
        [04/08/24 16:57:02] DEBUG    Starting System Compatibility Check                                                                                                                                                                                                  system.py:45
                            INFO     Machine: ppc64le                                                                                                                                                                                                                     system.py:62
                            INFO     Host: login1.summit.olcf.ornl.gov                                                                                                                                                                                                    system.py:63
                            INFO     User: siddiq90                                                                                                                                                                                                                       system.py:64
                            INFO     Operating System: rhel                                                                                                                                                                                                               system.py:65
                            INFO     System Kernel: Linux and Kernel Release: 4.18.0-372.52.1.el8_6.ppc64le                                                                                                                                                               system.py:66
                            INFO     Python Path: /autofs/nccs-svm1_home1/siddiq90/.local/share/virtualenvs/buildtest-PJVB0tHr/bin/python3                                                                                                                                system.py:69
                            INFO     Python Version: 3.11.6                                                                                                                                                                                                               system.py:70
                            INFO     BUILDTEST_ROOT: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest                                                                                                                                                                   system.py:71
                            INFO     Path to Buildtest: /ccs/home/siddiq90/gitrepo/buildtest/bin/buildtest                                                                                                                                                                system.py:72
                            INFO     Detected module system: lmod                                                                                                                                                                                                        system.py:107
                            INFO     Detected Lmod with version: 8.6.14                                                                                                                                                                                                  system.py:108
                            DEBUG    We will check the following binaries ['sbatch', 'sacct', 'sacctmgr', 'sinfo', 'scancel', 'scontrol'] for existence.                                                                                                               detection.py:31
                            DEBUG    sbatch: /usr/bin/sbatch                                                                                                                                                                                                           detection.py:39
                            DEBUG    sacct: /usr/bin/sacct                                                                                                                                                                                                             detection.py:39
                            DEBUG    sacctmgr: /usr/bin/sacctmgr                                                                                                                                                                                                       detection.py:39
                            DEBUG    sinfo: /usr/bin/sinfo                                                                                                                                                                                                             detection.py:39
                            DEBUG    scancel: /usr/bin/scancel                                                                                                                                                                                                         detection.py:39
                            DEBUG    scontrol: /usr/bin/scontrol                                                                                                                                                                                                       detection.py:39
                            DEBUG    Running command: sinfo -a -h -O partitionname                                                                                                                                                                                     detection.py:85
                            DEBUG    Running command: sacctmgr list cluster -P -n format=Cluster                                                                                                                                                                       detection.py:85
        [04/08/24 16:57:03] DEBUG    Running command: sacctmgr list qos -P -n  format=Name                                                                                                                                                                             detection.py:85
                            DEBUG    Detected Slurm Scheduler                                                                                                                                                                                                             system.py:89
                            DEBUG    We will check the following binaries ['bsub', 'bqueues', 'bkill', 'bjobs'] for existence.                                                                                                                                         detection.py:31
                            DEBUG    bsub: /sw/sources/lsf-tools/2.0/summit/bin/bsub                                                                                                                                                                                   detection.py:39
                            DEBUG    bqueues: /opt/ibm/spectrumcomputing/lsf/10.1.0.13/linux3.10-glibc2.17-ppc64le-csm/bin/bqueues                                                                                                                                     detection.py:39
                            DEBUG    bkill: /opt/ibm/spectrumcomputing/lsf/10.1.0.13/linux3.10-glibc2.17-ppc64le-csm/bin/bkill                                                                                                                                         detection.py:39
                            DEBUG    bjobs: /opt/ibm/spectrumcomputing/lsf/10.1.0.13/linux3.10-glibc2.17-ppc64le-csm/bin/bjobs                                                                                                                                         detection.py:39
                            DEBUG    Get all LSF Queues by running bqueues -o 'queue_name status' -json                                                                                                                                                               detection.py:251
                            DEBUG    Detected LSF Scheduler                                                                                                                                                                                                               system.py:89
                            DEBUG    We will check the following binaries ['qsub', 'qstat', 'qdel', 'nodelist', 'showres', 'partlist'] for existence.                                                                                                                  detection.py:31
                            DEBUG    Cannot find qsub command in $PATH                                                                                                                                                                                                 detection.py:36
                            DEBUG    We will check the following binaries ['qsub', 'qstat', 'qdel', 'qstart', 'qhold', 'qmgr'] for existence.                                                                                                                          detection.py:31
                            DEBUG    Cannot find qsub command in $PATH                                                                                                                                                                                                 detection.py:36
                            DEBUG    We will check the following binaries ['qsub', 'qstat', 'qdel', 'qstart', 'qhold', 'qmgr'] for existence.                                                                                                                          detection.py:31
                            DEBUG    Cannot find qsub command in $PATH                                                                                                                                                                                                 detection.py:36
                            INFO     Finished System Compatibility Check                                                                                                                                                                                                  system.py:77
                            DEBUG    List of available systems: ['summit'] found in configuration file                                                                                                                                                                   config.py:100
                            DEBUG    Checking hostname: login1.summit.olcf.ornl.gov in system: 'summit' with hostnames: ['login1.summit.olcf.ornl.gov', 'login2.summit.olcf.ornl.gov']                                                                                   config.py:115
                            INFO     Found matching system: summit based on hostname: login1.summit.olcf.ornl.gov                                                                                                                                                        config.py:122
                            DEBUG    Loading default settings schema: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/buildtest/schemas/settings.schema.json                                                                                                          config.py:141
                            DEBUG    Successfully loaded schema file: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/buildtest/schemas/settings.schema.json                                                                                                            utils.py:41
                            DEBUG    Validating configuration file with schema: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/buildtest/schemas/settings.schema.json                                                                                                config.py:144
                            DEBUG    Validation was successful                                                                                                                                                                                                           config.py:152
                            DEBUG    We will check the following binaries ['bsub', 'bqueues', 'bkill', 'bjobs'] for existence.                                                                                                                                         detection.py:31
                            DEBUG    bsub: /sw/sources/lsf-tools/2.0/summit/bin/bsub                                                                                                                                                                                   detection.py:39
                            DEBUG    bqueues: /opt/ibm/spectrumcomputing/lsf/10.1.0.13/linux3.10-glibc2.17-ppc64le-csm/bin/bqueues                                                                                                                                     detection.py:39
                            DEBUG    bkill: /opt/ibm/spectrumcomputing/lsf/10.1.0.13/linux3.10-glibc2.17-ppc64le-csm/bin/bkill                                                                                                                                         detection.py:39
                            DEBUG    bjobs: /opt/ibm/spectrumcomputing/lsf/10.1.0.13/linux3.10-glibc2.17-ppc64le-csm/bin/bjobs                                                                                                                                         detection.py:39
                            DEBUG    Get all LSF Queues by running bqueues -o 'queue_name status' -json                                                                                                                                                               detection.py:251
                            INFO     Processing buildtest configuration file: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/tests/settings/summit.yml                                                                                                                 main.py:149
                            DEBUG    Tests will be written in /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/tests                                                                                                                                                build.py:791
                            DEBUG    Getting Executors from buildtest settings                                                                                                                                                                                             setup.py:89
        ╭──────────────────────────────────────────────── buildtest summary ────────────────────────────────────────────────╮
        │                                                                                                                   │
        │ User:               siddiq90                                                                                      │
        │ Hostname:           login1                                                                                        │
        │ Platform:           Linux                                                                                         │
        │ Current Time:       2024/04/08 16:57:03                                                                           │
        │ buildtest path:     /ccs/home/siddiq90/gitrepo/buildtest/bin/buildtest                                            │
        │ buildtest version:  1.8                                                                                           │
        │ python path:        /autofs/nccs-svm1_home1/siddiq90/.local/share/virtualenvs/buildtest-PJVB0tHr/bin/python3      │
        │ python version:     3.11.6                                                                                        │
        │ Configuration File: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/tests/settings/summit.yml                  │
        │ Test Directory:     /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/tests                                  │
        │ Report File:        /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/report.json                            │
        │ Command:            /ccs/home/siddiq90/gitrepo/buildtest/bin/buildtest -d build -b hostname.yml --pollinterval=10 │
        │                                                                                                                   │
        ╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
                            DEBUG    Discovering buildspecs based on tags=None, executor=None, buildspec=['hostname.yml'], excluded buildspec=None                                                                                                                        build.py:149
                            DEBUG    Buildspec: hostname.yml is a file                                                                                                                                                                                                    build.py:560
                            INFO     Based on input argument we discovered the following buildspecs: ['/autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/tests/examples/summit/hostname.yml']                                                                            build.py:572
                            DEBUG    buildtest discovered the following Buildspecs: ['/autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/tests/examples/summit/hostname.yml']                                                                                             build.py:228
        ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────  Discovering Buildspecs ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
                                          Discovered buildspecs
        ╔═══════════════════════════════════════════════════════════════════════════════════════╗
        ║ buildspec                                                                             ║
        ╟───────────────────────────────────────────────────────────────────────────────────────╢
        ║ /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/tests/examples/summit/hostname.yml ║
        ╟───────────────────────────────────────────────────────────────────────────────────────╢
        ║ Total: 1                                                                              ║
        ╚═══════════════════════════════════════════════════════════════════════════════════════╝


        Total Discovered Buildspecs:  1
        Total Excluded Buildspecs:  0
        Detected Buildspecs after exclusion:  1
        ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── Parsing Buildspecs ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
                            INFO     Validating /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/tests/examples/summit/hostname.yml with schema: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/buildtest/schemas/global.schema.json                               parser.py:164
                            INFO     Validating test - 'hostname' in recipe: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/tests/examples/summit/hostname.yml                                                                                                       parser.py:176
                            INFO     Test: 'hostname' is using schema type: 'script'                                                                                                                                                                                     parser.py:118
                            INFO     Validating /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/tests/examples/summit/hostname.yml with schema:  /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/buildtest/schemas/script.schema.json                              parser.py:193
                            DEBUG    Searching for builders for test: hostname by applying regular expression with available builders: ['summit.local.bash', 'summit.local.sh', 'summit.local.csh', 'summit.local.python', 'summit.lsf.batch']                         builders.py:269
                            DEBUG    Found a match in buildspec with available executors via re.fullmatch(summit.lsf.batch,summit.lsf.batch)                                                                                                                           builders.py:277
                            DEBUG    Processing Buildspec File: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/tests/examples/summit/hostname.yml                                                                                                                      base.py:144
                            DEBUG    Processing Test: hostname                                                                                                                                                                                                             base.py:145
                            DEBUG    Using shell bash                                                                                                                                                                                                                      base.py:181
                            DEBUG    Shebang used for test: #!/usr/bin/bash                                                                                                                                                                                                base.py:182
        Valid Buildspecs: 1
        Invalid Buildspecs: 0
        /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/tests/examples/summit/hostname.yml: VALID
        Total builder objects created: 1
                                                                                            Builders by type=script
        ┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ builder           ┃ type   ┃ executor         ┃ compiler ┃ nodes ┃ procs ┃ description               ┃ buildspecs                                                                            ┃
        ┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ hostname/411112cb │ script │ summit.lsf.batch │ None     │ None  │ None  │ Run hostname in batch job │ /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/tests/examples/summit/hostname.yml │
        └───────────────────┴────────┴──────────────────┴──────────┴───────┴───────┴───────────────────────────┴───────────────────────────────────────────────────────────────────────────────────────┘
                                                               Batch Job Builders
        ┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ builder           ┃ executor         ┃ buildspecs                                                                            ┃
        ┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ hostname/411112cb │ summit.lsf.batch │ /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/tests/examples/summit/hostname.yml │
        └───────────────────┴──────────────────┴───────────────────────────────────────────────────────────────────────────────────────┘
        ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── Building Test ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
                            DEBUG    Creating test directory: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/tests/summit.lsf.batch/hostname/hostname/411112cb                                                                                                     base.py:527
                            DEBUG    Creating the stage directory: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/tests/summit.lsf.batch/hostname/hostname/411112cb/stage                                                                                          base.py:536
        hostname/411112cb: Creating Test Directory: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/tests/summit.lsf.batch/hostname/hostname/411112cb
                            INFO     Opening Test File for Writing: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/tests/summit.lsf.batch/hostname/hostname/411112cb/stage/hostname.sh                                                                             base.py:658
                            DEBUG    Changing permission to 755 for script: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/tests/summit.lsf.batch/hostname/hostname/411112cb/stage/hostname.sh                                                                     base.py:856
                            DEBUG    Writing build script: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/tests/summit.lsf.batch/hostname/hostname/411112cb/stage/hostname_build.sh                                                                                base.py:631
                            DEBUG    Changing permission to 755 for script: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/tests/summit.lsf.batch/hostname/hostname/411112cb/stage/hostname_build.sh                                                               base.py:856
                            DEBUG    Copying build script to: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/tests/summit.lsf.batch/hostname/hostname/411112cb/hostname_build.sh                                                                                   base.py:637
        ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── Running Tests ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
        Spawning 8 processes for processing builders
        ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── Iteration 1 ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
        hostname/411112cb does not have any dependencies adding test to queue
        Builders Eligible to Run
        ┏━━━━━━━━━━━━━━━━━━━┓
        ┃ Builder           ┃
        ┡━━━━━━━━━━━━━━━━━━━┩
        │ hostname/411112cb │
        └───────────────────┘
                            DEBUG    Changing to stage directory /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/tests/summit.lsf.batch/hostname/hostname/411112cb/stage                                                                                              lsf.py:80
        hostname/411112cb: Current Working Directory : /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/tests/summit.lsf.batch/hostname/hostname/411112cb/stage
        hostname/411112cb: Running Test via command: bash hostname_build.sh
                            DEBUG    Running Test via command: bash hostname_build.sh                                                                                                                                                                                      base.py:378
                            DEBUG    Applying regular expression '(\d+)' to output: 'Job <3386667> is submitted to queue <batch>.                                                                                                                                            lsf.py:98
                                     '
                            DEBUG    hostname/411112cb: JobID: 3386667 dispatched to scheduler                                                                                                                                                                              lsf.py:120
        hostname/411112cb: JobID: 3386667 dispatched to scheduler
        Polling Jobs in 10 seconds
        [04/08/24 16:57:13] DEBUG    bjobs -noheader -o 'stat' 3386667                                                                                                                                                                                                       lsf.py:52
                            DEBUG    Extracting Job State for job: 3386667 by running  'bjobs -noheader -o 'stat' 3386667'                                                                                                                                                   lsf.py:53
                            DEBUG    Job State: RUN                                                                                                                                                                                                                          lsf.py:60
                            DEBUG    Extracting EXIT CODE for job: 3386667 by running  'bjobs -noheader -o 'EXIT_CODE' 3386667 '                                                                                                                                             lsf.py:63
                            DEBUG    Exit Code: 0                                                                                                                                                                                                                            lsf.py:76
                                                Running Jobs (1)
        ┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
        ┃ builder           ┃ executor         ┃ jobid   ┃ jobstate ┃ runtime ┃ elapsedtime ┃ pendtime ┃
        ┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
        │ hostname/411112cb │ summit.lsf.batch │ 3386667 │ RUN      │ 10.358  │ 0.0         │ 0        │
        └───────────────────┴──────────────────┴─────────┴──────────┴─────────┴─────────────┴──────────┘
        Polling Jobs in 10 seconds
        [04/08/24 16:57:23] DEBUG    bjobs -noheader -o 'stat' 3386667                                                                                                                                                                                                       lsf.py:52
                            DEBUG    Extracting Job State for job: 3386667 by running  'bjobs -noheader -o 'stat' 3386667'                                                                                                                                                   lsf.py:53
                            DEBUG    Job State: RUN                                                                                                                                                                                                                          lsf.py:60
                            DEBUG    Extracting EXIT CODE for job: 3386667 by running  'bjobs -noheader -o 'EXIT_CODE' 3386667 '                                                                                                                                             lsf.py:63
                            DEBUG    Exit Code: 0                                                                                                                                                                                                                            lsf.py:76
                                                Running Jobs (1)
        ┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
        ┃ builder           ┃ executor         ┃ jobid   ┃ jobstate ┃ runtime ┃ elapsedtime ┃ pendtime ┃
        ┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
        │ hostname/411112cb │ summit.lsf.batch │ 3386667 │ RUN      │ 20.464  │ 10.11       │ 0        │
        └───────────────────┴──────────────────┴─────────┴──────────┴─────────┴─────────────┴──────────┘
        Polling Jobs in 10 seconds
        [04/08/24 16:57:33] DEBUG    bjobs -noheader -o 'stat' 3386667                                                                                                                                                                                                       lsf.py:52
                            DEBUG    Extracting Job State for job: 3386667 by running  'bjobs -noheader -o 'stat' 3386667'                                                                                                                                                   lsf.py:53
                            DEBUG    Job State: RUN                                                                                                                                                                                                                          lsf.py:60
                            DEBUG    Extracting EXIT CODE for job: 3386667 by running  'bjobs -noheader -o 'EXIT_CODE' 3386667 '                                                                                                                                             lsf.py:63
                            DEBUG    Exit Code: 0                                                                                                                                                                                                                            lsf.py:76
                                                Running Jobs (1)
        ┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
        ┃ builder           ┃ executor         ┃ jobid   ┃ jobstate ┃ runtime ┃ elapsedtime ┃ pendtime ┃
        ┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
        │ hostname/411112cb │ summit.lsf.batch │ 3386667 │ RUN      │ 30.575  │ 20.22       │ 0        │
        └───────────────────┴──────────────────┴─────────┴──────────┴─────────┴─────────────┴──────────┘
        Polling Jobs in 10 seconds
        [04/08/24 16:57:43] DEBUG    bjobs -noheader -o 'stat' 3386667                                                                                                                                                                                                       lsf.py:52
                            DEBUG    Extracting Job State for job: 3386667 by running  'bjobs -noheader -o 'stat' 3386667'                                                                                                                                                   lsf.py:53
        [04/08/24 16:57:44] DEBUG    Job State: RUN                                                                                                                                                                                                                          lsf.py:60
                            DEBUG    Extracting EXIT CODE for job: 3386667 by running  'bjobs -noheader -o 'EXIT_CODE' 3386667 '                                                                                                                                             lsf.py:63
                            DEBUG    Exit Code: 0                                                                                                                                                                                                                            lsf.py:76
                                                Running Jobs (1)
        ┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
        ┃ builder           ┃ executor         ┃ jobid   ┃ jobstate ┃ runtime ┃ elapsedtime ┃ pendtime ┃
        ┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
        │ hostname/411112cb │ summit.lsf.batch │ 3386667 │ RUN      │ 40.686  │ 30.33       │ 0        │
        └───────────────────┴──────────────────┴─────────┴──────────┴─────────┴─────────────┴──────────┘
        Polling Jobs in 10 seconds
        [04/08/24 16:57:54] DEBUG    bjobs -noheader -o 'stat' 3386667                                                                                                                                                                                                       lsf.py:52
                            DEBUG    Extracting Job State for job: 3386667 by running  'bjobs -noheader -o 'stat' 3386667'                                                                                                                                                   lsf.py:53
                            DEBUG    Job State: RUN                                                                                                                                                                                                                          lsf.py:60
                            DEBUG    Extracting EXIT CODE for job: 3386667 by running  'bjobs -noheader -o 'EXIT_CODE' 3386667 '                                                                                                                                             lsf.py:63
                            DEBUG    Exit Code: 0                                                                                                                                                                                                                            lsf.py:76
                                                Running Jobs (1)
        ┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
        ┃ builder           ┃ executor         ┃ jobid   ┃ jobstate ┃ runtime ┃ elapsedtime ┃ pendtime ┃
        ┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
        │ hostname/411112cb │ summit.lsf.batch │ 3386667 │ RUN      │ 50.793  │ 40.44       │ 0        │
        └───────────────────┴──────────────────┴─────────┴──────────┴─────────┴─────────────┴──────────┘
        Polling Jobs in 10 seconds
        [04/08/24 16:58:04] DEBUG    bjobs -noheader -o 'stat' 3386667                                                                                                                                                                                                       lsf.py:52
                            DEBUG    Extracting Job State for job: 3386667 by running  'bjobs -noheader -o 'stat' 3386667'                                                                                                                                                   lsf.py:53
                            DEBUG    Job State: DONE                                                                                                                                                                                                                         lsf.py:60
                            DEBUG    Extracting EXIT CODE for job: 3386667 by running  'bjobs -noheader -o 'EXIT_CODE' 3386667 '                                                                                                                                             lsf.py:63
                            DEBUG    Exit Code: 0                                                                                                                                                                                                                            lsf.py:76
                            DEBUG    Extracting OUTPUT FILE for job: 3386667 by running  'bjobs -noheader -o 'output_file' 3386667 '                                                                                                                                         lsf.py:98
                            DEBUG    Output File: hostname.out                                                                                                                                                                                                              lsf.py:104
                            DEBUG    Extracting ERROR FILE for job: 3386667 by running  'bjobs -noheader -o 'error_file' 3386667 '                                                                                                                                          lsf.py:108
                            DEBUG    Error File: hostname.err                                                                                                                                                                                                               lsf.py:114
                            DEBUG    Gather LSF job: 3386667 data by running: bjobs -o 'job_name stat user user_group queue proj_name pids exit_code from_host exec_host submit_time start_time finish_time nthreads exec_home exec_cwd output_file error_file' 3386667     lsf.py:177
                                     -json
                            DEBUG    {                                                                                                                                                                                                                                      lsf.py:185
                                       "COMMAND": "bjobs",
                                       "JOBS": 1,
                                       "RECORDS": [
                                         {
                                           "JOB_NAME": "hostname",
                                           "STAT": "DONE",
                                           "USER": "siddiq90",
                                           "USER_GROUP": "GEN243-HPCTEST",
                                           "QUEUE": "batch",
                                           "PROJ_NAME": "GEN243-HPCTEST",
                                           "PIDS": "",
                                           "EXIT_CODE": "",
                                           "FROM_HOST": "login1",
                                           "EXEC_HOST":
                                     "batch1:a01n10:a01n10:a01n10:a01n10:a01n10:a01n10:a01n10:a01n10:a01n10:a01n10:a01n10:a01n10:a01n10:a01n10:a01n10:a01n10:a01n10:a01n10:a01n10:a01n10:a01n10:a01n10:a01n10:a01n10:a01n10:a01n10:a01n10:a01n10:a01n10:a01n10:a01n10:a01n1
                                     0:a01n10:a01n10:a01n10:a01n10:a01n10:a01n10:a01n10:a01n10:a01n10:a01n10",
                                           "SUBMIT_TIME": "Apr  8 16:57",
                                           "START_TIME": "Apr  8 16:57",
                                           "FINISH_TIME": "Apr  8 16:57 L",
                                           "NTHREADS": "",
                                           "EXEC_HOME": "/ccs/home/siddiq90",
                                           "EXEC_CWD": "/autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/tests/summit.lsf.batch/hostname/hostname/411112cb/stage",
                                           "OUTPUT_FILE": "hostname.out",
                                           "ERROR_FILE": "hostname.err"
                                         }
                                       ]
                                     }
                            DEBUG     returncode: 0                                                                                                                                                                                                                        base.py:133
        hostname/411112cb: Job 3386667 is complete!
        hostname/411112cb: Test completed in 40.44 seconds with returncode: 0
        hostname/411112cb: Writing output file -  /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/tests/summit.lsf.batch/hostname/hostname/411112cb/hostname.out
        hostname/411112cb: Writing error file - /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/tests/summit.lsf.batch/hostname/hostname/411112cb/hostname.err
                                               Completed Jobs (1)
        ┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
        ┃ builder           ┃ executor         ┃ jobid   ┃ jobstate ┃ runtime ┃ elapsedtime ┃ pendtime ┃
        ┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
        │ hostname/411112cb │ summit.lsf.batch │ 3386667 │ DONE     │ 40.44   │ 40.44       │ 0        │
        └───────────────────┴──────────────────┴─────────┴──────────┴─────────┴─────────────┴──────────┘
                                      Test Summary
        ┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━┓
        ┃ builder           ┃ executor         ┃ status ┃ returncode ┃ runtime ┃
        ┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━┩
        │ hostname/411112cb │ summit.lsf.batch │ PASS   │ 0          │ 40.440  │
        └───────────────────┴──────────────────┴────────┴────────────┴─────────┘



        Passed Tests: 1/1 Percentage: 100.000%
        Failed Tests: 0/1 Percentage: 0.000%


                            DEBUG    Updating report file: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/report.json                                                                                                                                            build.py:1719
        Adding 1 test results to report file: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/report.json
        Writing Logfile to /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/logs/buildtest_i42712_e.log


In LSF, you can determine status check based on job state. For LSF jobs you can use ``lsf_job_state`` under the **status** to specify a matching
state. In this example, we are checking if the job state is ``EXIT``. If the job state is ``EXIT`` the test will pass, otherwise it will test will fail.

.. code-block:: yaml
    :emphasize-lines: 10

    buildspecs:
      lsf_job_state_example:
        type: script
        executor: summit.lsf.batch
        description: This job will only PASS if LSF Job state is EXIT
        tags: [jobs]
        bsub: ["-W 10", "-nnodes 1"]
        run: jsrun hostname
        status:
          lsf_job_state: EXIT


Take note when you run this test, the job will be in ``RUN`` state and will transition to ``DONE`` state after the job completes. The test will run to completion,
however the status check reported test failed, which is because the job state did not match the expected state.

.. dropdown:: ``buildtest -d build -b lsf_job_state.yml --pollinterval=15``


    .. code-block:: console

        (buildtest) [siddiq90@login1.summit summit]$ buildtest -d build -b lsf_job_state.yml --pollinterval=15
        [04/08/24 17:04:49] DEBUG    Starting System Compatibility Check                                                                                                                                                                                                  system.py:45
                            INFO     Machine: ppc64le                                                                                                                                                                                                                     system.py:62
                            INFO     Host: login1.summit.olcf.ornl.gov                                                                                                                                                                                                    system.py:63
                            INFO     User: siddiq90                                                                                                                                                                                                                       system.py:64
                            INFO     Operating System: rhel                                                                                                                                                                                                               system.py:65
                            INFO     System Kernel: Linux and Kernel Release: 4.18.0-372.52.1.el8_6.ppc64le                                                                                                                                                               system.py:66
                            INFO     Python Path: /autofs/nccs-svm1_home1/siddiq90/.local/share/virtualenvs/buildtest-PJVB0tHr/bin/python3                                                                                                                                system.py:69
                            INFO     Python Version: 3.11.6                                                                                                                                                                                                               system.py:70
                            INFO     BUILDTEST_ROOT: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest                                                                                                                                                                   system.py:71
                            INFO     Path to Buildtest: /ccs/home/siddiq90/gitrepo/buildtest/bin/buildtest                                                                                                                                                                system.py:72
                            INFO     Detected module system: lmod                                                                                                                                                                                                        system.py:107
                            INFO     Detected Lmod with version: 8.6.14                                                                                                                                                                                                  system.py:108
                            DEBUG    We will check the following binaries ['sbatch', 'sacct', 'sacctmgr', 'sinfo', 'scancel', 'scontrol'] for existence.                                                                                                               detection.py:31
                            DEBUG    sbatch: /usr/bin/sbatch                                                                                                                                                                                                           detection.py:39
                            DEBUG    sacct: /usr/bin/sacct                                                                                                                                                                                                             detection.py:39
                            DEBUG    sacctmgr: /usr/bin/sacctmgr                                                                                                                                                                                                       detection.py:39
                            DEBUG    sinfo: /usr/bin/sinfo                                                                                                                                                                                                             detection.py:39
                            DEBUG    scancel: /usr/bin/scancel                                                                                                                                                                                                         detection.py:39
                            DEBUG    scontrol: /usr/bin/scontrol                                                                                                                                                                                                       detection.py:39
                            DEBUG    Running command: sinfo -a -h -O partitionname                                                                                                                                                                                     detection.py:85
        [04/08/24 17:04:50] DEBUG    Running command: sacctmgr list cluster -P -n format=Cluster                                                                                                                                                                       detection.py:85
                            DEBUG    Running command: sacctmgr list qos -P -n  format=Name                                                                                                                                                                             detection.py:85
                            DEBUG    Detected Slurm Scheduler                                                                                                                                                                                                             system.py:89
                            DEBUG    We will check the following binaries ['bsub', 'bqueues', 'bkill', 'bjobs'] for existence.                                                                                                                                         detection.py:31
                            DEBUG    bsub: /sw/sources/lsf-tools/2.0/summit/bin/bsub                                                                                                                                                                                   detection.py:39
                            DEBUG    bqueues: /opt/ibm/spectrumcomputing/lsf/10.1.0.13/linux3.10-glibc2.17-ppc64le-csm/bin/bqueues                                                                                                                                     detection.py:39
                            DEBUG    bkill: /opt/ibm/spectrumcomputing/lsf/10.1.0.13/linux3.10-glibc2.17-ppc64le-csm/bin/bkill                                                                                                                                         detection.py:39
                            DEBUG    bjobs: /opt/ibm/spectrumcomputing/lsf/10.1.0.13/linux3.10-glibc2.17-ppc64le-csm/bin/bjobs                                                                                                                                         detection.py:39
                            DEBUG    Get all LSF Queues by running bqueues -o 'queue_name status' -json                                                                                                                                                               detection.py:251
                            DEBUG    Detected LSF Scheduler                                                                                                                                                                                                               system.py:89
                            DEBUG    We will check the following binaries ['qsub', 'qstat', 'qdel', 'nodelist', 'showres', 'partlist'] for existence.                                                                                                                  detection.py:31
                            DEBUG    Cannot find qsub command in $PATH                                                                                                                                                                                                 detection.py:36
                            DEBUG    We will check the following binaries ['qsub', 'qstat', 'qdel', 'qstart', 'qhold', 'qmgr'] for existence.                                                                                                                          detection.py:31
                            DEBUG    Cannot find qsub command in $PATH                                                                                                                                                                                                 detection.py:36
                            DEBUG    We will check the following binaries ['qsub', 'qstat', 'qdel', 'qstart', 'qhold', 'qmgr'] for existence.                                                                                                                          detection.py:31
                            DEBUG    Cannot find qsub command in $PATH                                                                                                                                                                                                 detection.py:36
                            INFO     Finished System Compatibility Check                                                                                                                                                                                                  system.py:77
                            DEBUG    List of available systems: ['summit'] found in configuration file                                                                                                                                                                   config.py:100
                            DEBUG    Checking hostname: login1.summit.olcf.ornl.gov in system: 'summit' with hostnames: ['login1.summit.olcf.ornl.gov', 'login2.summit.olcf.ornl.gov']                                                                                   config.py:115
                            INFO     Found matching system: summit based on hostname: login1.summit.olcf.ornl.gov                                                                                                                                                        config.py:122
                            DEBUG    Loading default settings schema: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/buildtest/schemas/settings.schema.json                                                                                                          config.py:141
                            DEBUG    Successfully loaded schema file: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/buildtest/schemas/settings.schema.json                                                                                                            utils.py:41
                            DEBUG    Validating configuration file with schema: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/buildtest/schemas/settings.schema.json                                                                                                config.py:144
                            DEBUG    Validation was successful                                                                                                                                                                                                           config.py:152
                            DEBUG    We will check the following binaries ['bsub', 'bqueues', 'bkill', 'bjobs'] for existence.                                                                                                                                         detection.py:31
                            DEBUG    bsub: /sw/sources/lsf-tools/2.0/summit/bin/bsub                                                                                                                                                                                   detection.py:39
                            DEBUG    bqueues: /opt/ibm/spectrumcomputing/lsf/10.1.0.13/linux3.10-glibc2.17-ppc64le-csm/bin/bqueues                                                                                                                                     detection.py:39
                            DEBUG    bkill: /opt/ibm/spectrumcomputing/lsf/10.1.0.13/linux3.10-glibc2.17-ppc64le-csm/bin/bkill                                                                                                                                         detection.py:39
                            DEBUG    bjobs: /opt/ibm/spectrumcomputing/lsf/10.1.0.13/linux3.10-glibc2.17-ppc64le-csm/bin/bjobs                                                                                                                                         detection.py:39
                            DEBUG    Get all LSF Queues by running bqueues -o 'queue_name status' -json                                                                                                                                                               detection.py:251
                            INFO     Processing buildtest configuration file: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/tests/settings/summit.yml                                                                                                                 main.py:149
                            DEBUG    Tests will be written in /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/tests                                                                                                                                                build.py:791
                            DEBUG    Getting Executors from buildtest settings                                                                                                                                                                                             setup.py:89
        ╭────────────────────────────────────────────────── buildtest summary ───────────────────────────────────────────────────╮
        │                                                                                                                        │
        │ User:               siddiq90                                                                                           │
        │ Hostname:           login1                                                                                             │
        │ Platform:           Linux                                                                                              │
        │ Current Time:       2024/04/08 17:04:50                                                                                │
        │ buildtest path:     /ccs/home/siddiq90/gitrepo/buildtest/bin/buildtest                                                 │
        │ buildtest version:  1.8                                                                                                │
        │ python path:        /autofs/nccs-svm1_home1/siddiq90/.local/share/virtualenvs/buildtest-PJVB0tHr/bin/python3           │
        │ python version:     3.11.6                                                                                             │
        │ Configuration File: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/tests/settings/summit.yml                       │
        │ Test Directory:     /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/tests                                       │
        │ Report File:        /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/report.json                                 │
        │ Command:            /ccs/home/siddiq90/gitrepo/buildtest/bin/buildtest -d build -b lsf_job_state.yml --pollinterval=15 │
        │                                                                                                                        │
        ╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
                            DEBUG    Discovering buildspecs based on tags=None, executor=None, buildspec=['lsf_job_state.yml'], excluded buildspec=None                                                                                                                   build.py:149
                            DEBUG    Buildspec: lsf_job_state.yml is a file                                                                                                                                                                                               build.py:560
                            INFO     Based on input argument we discovered the following buildspecs: ['/autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/tests/examples/summit/lsf_job_state.yml']                                                                       build.py:572
                            DEBUG    buildtest discovered the following Buildspecs: ['/autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/tests/examples/summit/lsf_job_state.yml']                                                                                        build.py:228
        ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────  Discovering Buildspecs ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
                                            Discovered buildspecs
        ╔════════════════════════════════════════════════════════════════════════════════════════════╗
        ║ buildspec                                                                                  ║
        ╟────────────────────────────────────────────────────────────────────────────────────────────╢
        ║ /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/tests/examples/summit/lsf_job_state.yml ║
        ╟────────────────────────────────────────────────────────────────────────────────────────────╢
        ║ Total: 1                                                                                   ║
        ╚════════════════════════════════════════════════════════════════════════════════════════════╝


        Total Discovered Buildspecs:  1
        Total Excluded Buildspecs:  0
        Detected Buildspecs after exclusion:  1
        ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── Parsing Buildspecs ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
                            INFO     Validating /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/tests/examples/summit/lsf_job_state.yml with schema: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/buildtest/schemas/global.schema.json                          parser.py:164
                            INFO     Validating test - 'lsf_job_state_example' in recipe: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/tests/examples/summit/lsf_job_state.yml                                                                                     parser.py:176
                            INFO     Test: 'lsf_job_state_example' is using schema type: 'script'                                                                                                                                                                        parser.py:118
                            INFO     Validating /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/tests/examples/summit/lsf_job_state.yml with schema:  /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/buildtest/schemas/script.schema.json                         parser.py:193
                            DEBUG    Searching for builders for test: lsf_job_state_example by applying regular expression with available builders: ['summit.local.bash', 'summit.local.sh', 'summit.local.csh', 'summit.local.python', 'summit.lsf.batch']            builders.py:269
                            DEBUG    Found a match in buildspec with available executors via re.fullmatch(summit.lsf.batch,summit.lsf.batch)                                                                                                                           builders.py:277
                            DEBUG    Processing Buildspec File: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/tests/examples/summit/lsf_job_state.yml                                                                                                                 base.py:144
                            DEBUG    Processing Test: lsf_job_state_example                                                                                                                                                                                                base.py:145
                            DEBUG    Using shell bash                                                                                                                                                                                                                      base.py:181
                            DEBUG    Shebang used for test: #!/usr/bin/bash                                                                                                                                                                                                base.py:182
        Valid Buildspecs: 1
        Invalid Buildspecs: 0
        /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/tests/examples/summit/lsf_job_state.yml: VALID
        Total builder objects created: 1
                                                                                                                 Builders by type=script
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ builder                        ┃ type   ┃ executor         ┃ compiler ┃ nodes ┃ procs ┃ description                                      ┃ buildspecs                                                                                 ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ lsf_job_state_example/49179e87 │ script │ summit.lsf.batch │ None     │ None  │ None  │ This job will only PASS if LSF Job state is EXIT │ /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/tests/examples/summit/lsf_job_state.yml │
        └────────────────────────────────┴────────┴──────────────────┴──────────┴───────┴───────┴──────────────────────────────────────────────────┴────────────────────────────────────────────────────────────────────────────────────────────┘
                                                                        Batch Job Builders
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ builder                        ┃ executor         ┃ buildspecs                                                                                 ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ lsf_job_state_example/49179e87 │ summit.lsf.batch │ /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/tests/examples/summit/lsf_job_state.yml │
        └────────────────────────────────┴──────────────────┴────────────────────────────────────────────────────────────────────────────────────────────┘
        ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── Building Test ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
                            DEBUG    Creating test directory: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/tests/summit.lsf.batch/lsf_job_state/lsf_job_state_example/49179e87                                                                                   base.py:527
                            DEBUG    Creating the stage directory: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/tests/summit.lsf.batch/lsf_job_state/lsf_job_state_example/49179e87/stage                                                                        base.py:536
        lsf_job_state_example/49179e87: Creating Test Directory: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/tests/summit.lsf.batch/lsf_job_state/lsf_job_state_example/49179e87
                            INFO     Opening Test File for Writing: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/tests/summit.lsf.batch/lsf_job_state/lsf_job_state_example/49179e87/stage/lsf_job_state_example.sh                                              base.py:658
                            DEBUG    Changing permission to 755 for script: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/tests/summit.lsf.batch/lsf_job_state/lsf_job_state_example/49179e87/stage/lsf_job_state_example.sh                                      base.py:856
                            DEBUG    Writing build script: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/tests/summit.lsf.batch/lsf_job_state/lsf_job_state_example/49179e87/stage/lsf_job_state_example_build.sh                                                 base.py:631
                            DEBUG    Changing permission to 755 for script: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/tests/summit.lsf.batch/lsf_job_state/lsf_job_state_example/49179e87/stage/lsf_job_state_example_build.sh                                base.py:856
                            DEBUG    Copying build script to: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/tests/summit.lsf.batch/lsf_job_state/lsf_job_state_example/49179e87/lsf_job_state_example_build.sh                                                    base.py:637
        ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── Running Tests ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
        Spawning 8 processes for processing builders
        ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── Iteration 1 ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
        lsf_job_state_example/49179e87 does not have any dependencies adding test to queue
             Builders Eligible to Run
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ Builder                        ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ lsf_job_state_example/49179e87 │
        └────────────────────────────────┘
                            DEBUG    Changing to stage directory /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/tests/summit.lsf.batch/lsf_job_state/lsf_job_state_example/49179e87/stage                                                                            lsf.py:80
        lsf_job_state_example/49179e87: Current Working Directory : /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/tests/summit.lsf.batch/lsf_job_state/lsf_job_state_example/49179e87/stage
        lsf_job_state_example/49179e87: Running Test via command: bash lsf_job_state_example_build.sh
                            DEBUG    Running Test via command: bash lsf_job_state_example_build.sh                                                                                                                                                                         base.py:378
                            DEBUG    Applying regular expression '(\d+)' to output: 'Job <3386735> is submitted to queue <batch>.                                                                                                                                            lsf.py:98
                                     '
                            DEBUG    lsf_job_state_example/49179e87: JobID: 3386735 dispatched to scheduler                                                                                                                                                                 lsf.py:120
        lsf_job_state_example/49179e87: JobID: 3386735 dispatched to scheduler
        Polling Jobs in 15 seconds
        [04/08/24 17:05:05] DEBUG    bjobs -noheader -o 'stat' 3386735                                                                                                                                                                                                       lsf.py:52
                            DEBUG    Extracting Job State for job: 3386735 by running  'bjobs -noheader -o 'stat' 3386735'                                                                                                                                                   lsf.py:53
                            DEBUG    Job State: RUN                                                                                                                                                                                                                          lsf.py:60
                            DEBUG    Extracting EXIT CODE for job: 3386735 by running  'bjobs -noheader -o 'EXIT_CODE' 3386735 '                                                                                                                                             lsf.py:63
        [04/08/24 17:05:06] DEBUG    Exit Code: 0                                                                                                                                                                                                                            lsf.py:76
                                                      Running Jobs (1)
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
        ┃ builder                        ┃ executor         ┃ jobid   ┃ jobstate ┃ runtime ┃ elapsedtime ┃ pendtime ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
        │ lsf_job_state_example/49179e87 │ summit.lsf.batch │ 3386735 │ RUN      │ 15.396  │ 0.0         │ 0        │
        └────────────────────────────────┴──────────────────┴─────────┴──────────┴─────────┴─────────────┴──────────┘
        Polling Jobs in 15 seconds
        [04/08/24 17:05:21] DEBUG    bjobs -noheader -o 'stat' 3386735                                                                                                                                                                                                       lsf.py:52
                            DEBUG    Extracting Job State for job: 3386735 by running  'bjobs -noheader -o 'stat' 3386735'                                                                                                                                                   lsf.py:53
                            DEBUG    Job State: RUN                                                                                                                                                                                                                          lsf.py:60
                            DEBUG    Extracting EXIT CODE for job: 3386735 by running  'bjobs -noheader -o 'EXIT_CODE' 3386735 '                                                                                                                                             lsf.py:63
                            DEBUG    Exit Code: 0                                                                                                                                                                                                                            lsf.py:76
                                                      Running Jobs (1)
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
        ┃ builder                        ┃ executor         ┃ jobid   ┃ jobstate ┃ runtime ┃ elapsedtime ┃ pendtime ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
        │ lsf_job_state_example/49179e87 │ summit.lsf.batch │ 3386735 │ RUN      │ 30.504  │ 15.11       │ 0        │
        └────────────────────────────────┴──────────────────┴─────────┴──────────┴─────────┴─────────────┴──────────┘
        Polling Jobs in 15 seconds
        [04/08/24 17:05:36] DEBUG    bjobs -noheader -o 'stat' 3386735                                                                                                                                                                                                       lsf.py:52
                            DEBUG    Extracting Job State for job: 3386735 by running  'bjobs -noheader -o 'stat' 3386735'                                                                                                                                                   lsf.py:53
                            DEBUG    Job State: RUN                                                                                                                                                                                                                          lsf.py:60
                            DEBUG    Extracting EXIT CODE for job: 3386735 by running  'bjobs -noheader -o 'EXIT_CODE' 3386735 '                                                                                                                                             lsf.py:63
                            DEBUG    Exit Code: 0                                                                                                                                                                                                                            lsf.py:76
                                                      Running Jobs (1)
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
        ┃ builder                        ┃ executor         ┃ jobid   ┃ jobstate ┃ runtime ┃ elapsedtime ┃ pendtime ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
        │ lsf_job_state_example/49179e87 │ summit.lsf.batch │ 3386735 │ RUN      │ 45.663  │ 30.27       │ 0        │
        └────────────────────────────────┴──────────────────┴─────────┴──────────┴─────────┴─────────────┴──────────┘
        Polling Jobs in 15 seconds
        [04/08/24 17:05:51] DEBUG    bjobs -noheader -o 'stat' 3386735                                                                                                                                                                                                       lsf.py:52
                            DEBUG    Extracting Job State for job: 3386735 by running  'bjobs -noheader -o 'stat' 3386735'                                                                                                                                                   lsf.py:53
                            DEBUG    Job State: DONE                                                                                                                                                                                                                         lsf.py:60
                            DEBUG    Extracting EXIT CODE for job: 3386735 by running  'bjobs -noheader -o 'EXIT_CODE' 3386735 '                                                                                                                                             lsf.py:63
                            DEBUG    Exit Code: 0                                                                                                                                                                                                                            lsf.py:76
                            DEBUG    Extracting OUTPUT FILE for job: 3386735 by running  'bjobs -noheader -o 'output_file' 3386735 '                                                                                                                                         lsf.py:98
                            DEBUG    Output File: lsf_job_state_example.out                                                                                                                                                                                                 lsf.py:104
                            DEBUG    Extracting ERROR FILE for job: 3386735 by running  'bjobs -noheader -o 'error_file' 3386735 '                                                                                                                                          lsf.py:108
                            DEBUG    Error File: lsf_job_state_example.err                                                                                                                                                                                                  lsf.py:114
                            DEBUG    Gather LSF job: 3386735 data by running: bjobs -o 'job_name stat user user_group queue proj_name pids exit_code from_host exec_host submit_time start_time finish_time nthreads exec_home exec_cwd output_file error_file' 3386735     lsf.py:177
                                     -json
                            DEBUG    {                                                                                                                                                                                                                                      lsf.py:185
                                       "COMMAND": "bjobs",
                                       "JOBS": 1,
                                       "RECORDS": [
                                         {
                                           "JOB_NAME": "lsf_job_state_example",
                                           "STAT": "DONE",
                                           "USER": "siddiq90",
                                           "USER_GROUP": "GEN243-HPCTEST",
                                           "QUEUE": "batch",
                                           "PROJ_NAME": "GEN243-HPCTEST",
                                           "PIDS": "",
                                           "EXIT_CODE": "",
                                           "FROM_HOST": "login1",
                                           "EXEC_HOST":
                                     "batch1:h15n09:h15n09:h15n09:h15n09:h15n09:h15n09:h15n09:h15n09:h15n09:h15n09:h15n09:h15n09:h15n09:h15n09:h15n09:h15n09:h15n09:h15n09:h15n09:h15n09:h15n09:h15n09:h15n09:h15n09:h15n09:h15n09:h15n09:h15n09:h15n09:h15n09:h15n09:h15n0
                                     9:h15n09:h15n09:h15n09:h15n09:h15n09:h15n09:h15n09:h15n09:h15n09:h15n09",
                                           "SUBMIT_TIME": "Apr  8 17:04",
                                           "START_TIME": "Apr  8 17:04",
                                           "FINISH_TIME": "Apr  8 17:05 L",
                                           "NTHREADS": "",
                                           "EXEC_HOME": "/ccs/home/siddiq90",
                                           "EXEC_CWD": "/autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/tests/summit.lsf.batch/lsf_job_state/lsf_job_state_example/49179e87/stage",
                                           "OUTPUT_FILE": "lsf_job_state_example.out",
                                           "ERROR_FILE": "lsf_job_state_example.err"
                                         }
                                       ]
                                     }
                            DEBUG     returncode: 0                                                                                                                                                                                                                        base.py:133
        lsf_job_state_example/49179e87: Job 3386735 is complete!
        lsf_job_state_example/49179e87: Test completed in 30.27 seconds with returncode: 0
        lsf_job_state_example/49179e87: Writing output file -  /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/tests/summit.lsf.batch/lsf_job_state/lsf_job_state_example/49179e87/lsf_job_state_example.out
        lsf_job_state_example/49179e87: Writing error file - /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/tests/summit.lsf.batch/lsf_job_state/lsf_job_state_example/49179e87/lsf_job_state_example.err
                                                     Completed Jobs (1)
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
        ┃ builder                        ┃ executor         ┃ jobid   ┃ jobstate ┃ runtime ┃ elapsedtime ┃ pendtime ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
        │ lsf_job_state_example/49179e87 │ summit.lsf.batch │ 3386735 │ DONE     │ 30.27   │ 30.27       │ 0        │
        └────────────────────────────────┴──────────────────┴─────────┴──────────┴─────────┴─────────────┴──────────┘
                                            Test Summary
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━┓
        ┃ builder                        ┃ executor         ┃ status ┃ returncode ┃ runtime ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━┩
        │ lsf_job_state_example/49179e87 │ summit.lsf.batch │ FAIL   │ 0          │ 30.270  │
        └────────────────────────────────┴──────────────────┴────────┴────────────┴─────────┘



        Passed Tests: 0/1 Percentage: 0.000%
        Failed Tests: 1/1 Percentage: 100.000%


                            DEBUG    Updating report file: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/report.json                                                                                                                                            build.py:1719
        Adding 1 test results to report file: /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/report.json
        Writing Logfile to /autofs/nccs-svm1_home1/siddiq90/gitrepo/buildtest/var/logs/buildtest_873njlcb.log

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

buildtest will poll PBS jobs using ``qstat``  until job is finished. Note that
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
        │ Current Time:       2023/11/08 01:02:24                                                                          │
        │ buildtest path:     /home/pbsuser/buildtest/bin/buildtest                                                        │
        │ buildtest version:  1.6                                                                                          │
        │ python path:        /home/pbsuser/miniconda/bin/python3                                                          │
        │ python version:     3.11.5                                                                                       │
        │ Configuration File: /home/pbsuser/buildtest/tests/settings/pbs.yml                                               │
        │ Test Directory:     /home/pbsuser/buildtest/var/tests                                                            │
        │ Report File:        /home/pbsuser/buildtest/var/report.json                                                      │
        │ Command:            /home/pbsuser/buildtest/bin/buildtest build -b tests/examples/pbs/sleep.yml --pollinterval=2 │
        │                                                                                                                  │
        ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
        ─────────────────────────────────────────────────────────────────────────  Discovering Buildspecs ──────────────────────────────────────────────────────────────────────────
                         Discovered buildspecs
        ╔══════════════════════════════════════════════════════╗
        ║ buildspec                                            ║
        ╟──────────────────────────────────────────────────────╢
        ║ /home/pbsuser/buildtest/tests/examples/pbs/sleep.yml ║
        ╚══════════════════════════════════════════════════════╝


        Total Discovered Buildspecs:  1
        Total Excluded Buildspecs:  0
        Detected Buildspecs after exclusion:  1
        ──────────────────────────────────────────────────────────────────────────── Parsing Buildspecs ────────────────────────────────────────────────────────────────────────────
        Valid Buildspecs: 1
        Invalid Buildspecs: 0
        /home/pbsuser/buildtest/tests/examples/pbs/sleep.yml: VALID
        Total builder objects created: 1
                                                                      Builders by type=script
        ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ builder            ┃ type   ┃ executor          ┃ compiler ┃ nodes ┃ procs ┃ description ┃ buildspecs                                           ┃
        ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ pbs_sleep/8c334820 │ script │ generic.pbs.workq │ None     │ None  │ None  │             │ /home/pbsuser/buildtest/tests/examples/pbs/sleep.yml │
        └────────────────────┴────────┴───────────────────┴──────────┴───────┴───────┴─────────────┴──────────────────────────────────────────────────────┘
                                               Batch Job Builders
        ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ builder            ┃ executor          ┃ buildspecs                                           ┃
        ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ pbs_sleep/8c334820 │ generic.pbs.workq │ /home/pbsuser/buildtest/tests/examples/pbs/sleep.yml │
        └────────────────────┴───────────────────┴──────────────────────────────────────────────────────┘
        ────────────────────────────────────────────────────────────────────────────── Building Test ───────────────────────────────────────────────────────────────────────────────
        pbs_sleep/8c334820: Creating test directory: /home/pbsuser/buildtest/var/tests/generic.pbs.workq/sleep/pbs_sleep/8c334820
        pbs_sleep/8c334820: Creating the stage directory: /home/pbsuser/buildtest/var/tests/generic.pbs.workq/sleep/pbs_sleep/8c334820/stage
        pbs_sleep/8c334820: Writing build script: /home/pbsuser/buildtest/var/tests/generic.pbs.workq/sleep/pbs_sleep/8c334820/pbs_sleep_build.sh
        ────────────────────────────────────────────────────────────────────────────── Running Tests ───────────────────────────────────────────────────────────────────────────────
        Spawning 1 processes for processing builders
        ─────────────────────────────────────────────────────────────────────────────── Iteration 1 ────────────────────────────────────────────────────────────────────────────────
        pbs_sleep/8c334820 does not have any dependencies adding test to queue
        Builders Eligible to Run
        ┏━━━━━━━━━━━━━━━━━━━━┓
        ┃ Builder            ┃
        ┡━━━━━━━━━━━━━━━━━━━━┩
        │ pbs_sleep/8c334820 │
        └────────────────────┘
        pbs_sleep/8c334820: Current Working Directory : /home/pbsuser/buildtest/var/tests/generic.pbs.workq/sleep/pbs_sleep/8c334820/stage
        pbs_sleep/8c334820: Running Test via command: bash --norc --noprofile -eo pipefail pbs_sleep_build.sh
        pbs_sleep/8c334820: JobID: 0.pbs dispatched to scheduler
        Polling Jobs in 2 seconds
                                                Running Jobs (1)
        ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
        ┃ builder            ┃ executor          ┃ jobid ┃ jobstate ┃ runtime ┃ elapsedtime ┃ pendtime ┃
        ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
        │ pbs_sleep/8c334820 │ generic.pbs.workq │ 0.pbs │ R        │ 2.057   │ 0.0         │ 0        │
        └────────────────────┴───────────────────┴───────┴──────────┴─────────┴─────────────┴──────────┘
        Polling Jobs in 2 seconds
                                                Running Jobs (1)
        ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
        ┃ builder            ┃ executor          ┃ jobid ┃ jobstate ┃ runtime ┃ elapsedtime ┃ pendtime ┃
        ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
        │ pbs_sleep/8c334820 │ generic.pbs.workq │ 0.pbs │ R        │ 4.081   │ 2.02        │ 0        │
        └────────────────────┴───────────────────┴───────┴──────────┴─────────┴─────────────┴──────────┘
        Polling Jobs in 2 seconds
        pbs_sleep/8c334820: Job 0.pbs is complete!
        pbs_sleep/8c334820: Test completed in 2.02 seconds
        pbs_sleep/8c334820: Test completed with returncode: 0
        pbs_sleep/8c334820: Writing output file -  /home/pbsuser/buildtest/var/tests/generic.pbs.workq/sleep/pbs_sleep/8c334820/pbs_sleep.o0
        pbs_sleep/8c334820: Writing error file - /home/pbsuser/buildtest/var/tests/generic.pbs.workq/sleep/pbs_sleep/8c334820/pbs_sleep.e0
                                               Completed Jobs (1)
        ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
        ┃ builder            ┃ executor          ┃ jobid ┃ jobstate ┃ runtime ┃ elapsedtime ┃ pendtime ┃
        ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
        │ pbs_sleep/8c334820 │ generic.pbs.workq │ 0.pbs │ F        │ 2.02    │ 2.02        │ 0        │
        └────────────────────┴───────────────────┴───────┴──────────┴─────────┴─────────────┴──────────┘
                                                          Test Summary
        ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━┓
        ┃ builder            ┃ executor          ┃ status ┃ checks (ReturnCode, Regex, Runtime) ┃ returncode ┃ runtime ┃
        ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━┩
        │ pbs_sleep/8c334820 │ generic.pbs.workq │ PASS   │ None None None                      │ 0          │ 2.02    │
        └────────────────────┴───────────────────┴────────┴─────────────────────────────────────┴────────────┴─────────┘



        Passed Tests: 1/1 Percentage: 100.000%
        Failed Tests: 0/1 Percentage: 0.000%


        Adding 1 test results to /home/pbsuser/buildtest/var/report.json
        Writing Logfile to: /home/pbsuser/buildtest/var/logs/buildtest_25m8ryje.log



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
        │ Current Time:       2023/11/08 01:04:07                                                                               │
        │ buildtest path:     /home/pbsuser/buildtest/bin/buildtest                                                             │
        │ buildtest version:  1.6                                                                                               │
        │ python path:        /home/pbsuser/miniconda/bin/python3                                                               │
        │ python version:     3.11.5                                                                                            │
        │ Configuration File: /home/pbsuser/buildtest/tests/settings/pbs.yml                                                    │
        │ Test Directory:     /home/pbsuser/buildtest/var/tests                                                                 │
        │ Report File:        /home/pbsuser/buildtest/var/report.json                                                           │
        │ Command:            /home/pbsuser/buildtest/bin/buildtest bd -b tests/examples/pbs/pbs_job_state.yml --pollinterval=2 │
        │                                                                                                                       │
        ╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
        ─────────────────────────────────────────────────────────────────────────  Discovering Buildspecs ──────────────────────────────────────────────────────────────────────────
                             Discovered buildspecs
        ╔══════════════════════════════════════════════════════════════╗
        ║ buildspec                                                    ║
        ╟──────────────────────────────────────────────────────────────╢
        ║ /home/pbsuser/buildtest/tests/examples/pbs/pbs_job_state.yml ║
        ╚══════════════════════════════════════════════════════════════╝


        Total Discovered Buildspecs:  1
        Total Excluded Buildspecs:  0
        Detected Buildspecs after exclusion:  1
        ──────────────────────────────────────────────────────────────────────────── Parsing Buildspecs ────────────────────────────────────────────────────────────────────────────
        Valid Buildspecs: 1
        Invalid Buildspecs: 0
        /home/pbsuser/buildtest/tests/examples/pbs/pbs_job_state.yml: VALID
        Total builder objects created: 1
                                                                                  Builders by type=script
        ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ builder            ┃ type   ┃ executor          ┃ compiler ┃ nodes ┃ procs ┃ description                       ┃ buildspecs                                              ┃
        ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ pbs_sleep/3c5e92d7 │ script │ generic.pbs.workq │ None     │ None  │ None  │ pass test based on PBS job state. │ /home/pbsuser/buildtest/tests/examples/pbs/pbs_job_stat │
        │                    │        │                   │          │       │       │                                   │ e.yml                                                   │
        └────────────────────┴────────┴───────────────────┴──────────┴───────┴───────┴───────────────────────────────────┴─────────────────────────────────────────────────────────┘
                                                   Batch Job Builders
        ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ builder            ┃ executor          ┃ buildspecs                                                   ┃
        ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ pbs_sleep/3c5e92d7 │ generic.pbs.workq │ /home/pbsuser/buildtest/tests/examples/pbs/pbs_job_state.yml │
        └────────────────────┴───────────────────┴──────────────────────────────────────────────────────────────┘
        ────────────────────────────────────────────────────────────────────────────── Building Test ───────────────────────────────────────────────────────────────────────────────
        pbs_sleep/3c5e92d7: Creating test directory: /home/pbsuser/buildtest/var/tests/generic.pbs.workq/pbs_job_state/pbs_sleep/3c5e92d7
        pbs_sleep/3c5e92d7: Creating the stage directory: /home/pbsuser/buildtest/var/tests/generic.pbs.workq/pbs_job_state/pbs_sleep/3c5e92d7/stage
        pbs_sleep/3c5e92d7: Writing build script: /home/pbsuser/buildtest/var/tests/generic.pbs.workq/pbs_job_state/pbs_sleep/3c5e92d7/pbs_sleep_build.sh
        ────────────────────────────────────────────────────────────────────────────── Running Tests ───────────────────────────────────────────────────────────────────────────────
        Spawning 1 processes for processing builders
        ─────────────────────────────────────────────────────────────────────────────── Iteration 1 ────────────────────────────────────────────────────────────────────────────────
        pbs_sleep/3c5e92d7 does not have any dependencies adding test to queue
        Builders Eligible to Run
        ┏━━━━━━━━━━━━━━━━━━━━┓
        ┃ Builder            ┃
        ┡━━━━━━━━━━━━━━━━━━━━┩
        │ pbs_sleep/3c5e92d7 │
        └────────────────────┘
        pbs_sleep/3c5e92d7: Current Working Directory : /home/pbsuser/buildtest/var/tests/generic.pbs.workq/pbs_job_state/pbs_sleep/3c5e92d7/stage
        pbs_sleep/3c5e92d7: Running Test via command: bash --norc --noprofile -eo pipefail pbs_sleep_build.sh
        pbs_sleep/3c5e92d7: JobID: 1.pbs dispatched to scheduler
        Polling Jobs in 2 seconds
                                                Running Jobs (1)
        ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
        ┃ builder            ┃ executor          ┃ jobid ┃ jobstate ┃ runtime ┃ elapsedtime ┃ pendtime ┃
        ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
        │ pbs_sleep/3c5e92d7 │ generic.pbs.workq │ 1.pbs │ R        │ 2.043   │ 0.0         │ 0        │
        └────────────────────┴───────────────────┴───────┴──────────┴─────────┴─────────────┴──────────┘
        Polling Jobs in 2 seconds
                                                Running Jobs (1)
        ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
        ┃ builder            ┃ executor          ┃ jobid ┃ jobstate ┃ runtime ┃ elapsedtime ┃ pendtime ┃
        ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
        │ pbs_sleep/3c5e92d7 │ generic.pbs.workq │ 1.pbs │ R        │ 4.067   │ 2.02        │ 0        │
        └────────────────────┴───────────────────┴───────┴──────────┴─────────┴─────────────┴──────────┘
        Polling Jobs in 2 seconds
        pbs_sleep/3c5e92d7: Job 1.pbs is complete!
        pbs_sleep/3c5e92d7: Test completed in 2.02 seconds
        pbs_sleep/3c5e92d7: Test completed with returncode: 0
        pbs_sleep/3c5e92d7: Writing output file -  /home/pbsuser/buildtest/var/tests/generic.pbs.workq/pbs_job_state/pbs_sleep/3c5e92d7/pbs_sleep.o1
        pbs_sleep/3c5e92d7: Writing error file - /home/pbsuser/buildtest/var/tests/generic.pbs.workq/pbs_job_state/pbs_sleep/3c5e92d7/pbs_sleep.e1
                                               Completed Jobs (1)
        ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
        ┃ builder            ┃ executor          ┃ jobid ┃ jobstate ┃ runtime ┃ elapsedtime ┃ pendtime ┃
        ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
        │ pbs_sleep/3c5e92d7 │ generic.pbs.workq │ 1.pbs │ F        │ 2.02    │ 2.02        │ 0        │
        └────────────────────┴───────────────────┴───────┴──────────┴─────────┴─────────────┴──────────┘
                                                          Test Summary
        ┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━┓
        ┃ builder            ┃ executor          ┃ status ┃ checks (ReturnCode, Regex, Runtime) ┃ returncode ┃ runtime ┃
        ┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━┩
        │ pbs_sleep/3c5e92d7 │ generic.pbs.workq │ FAIL   │ None None None                      │ 0          │ 2.02    │
        └────────────────────┴───────────────────┴────────┴─────────────────────────────────────┴────────────┴─────────┘



        Passed Tests: 0/1 Percentage: 0.000%
        Failed Tests: 1/1 Percentage: 100.000%


        Adding 1 test results to /home/pbsuser/buildtest/var/report.json
        Writing Logfile to: /home/pbsuser/buildtest/var/logs/buildtest_vnk2erx5.log

Torque
-------

Buildtest has support for running jobs on `Torque <https://adaptivecomputing.com/cherry-services/torque-resource-manager/>`_ scheduler. You must
define a :ref:`torque_executors` in your configuration file to use Torque scheduler. The ``#PBS`` directives can be specified using
``pbs`` property which is a list of PBS options that get inserted at top of script. Shown below is an example sleep job that will run on
a single node for 5 seconds.

.. code-block:: yaml
    :emphasize-lines: 4,6

    buildspecs:
      hostname_test:
        type: script
        executor: generic.torque.e4spro
        description: run sleep for 5 seconds
        pbs: ["-l nodes=1"]
        run: |
          sleep 5

We will run this test and poll every 10 second. We have enabled debug mode so you can see the detailed output including the
scheduler commands that are used to submit and poll the job.

.. code-block:: console

    adaptive50@lbl-cluster $ buildtest -d build -b sleep.yml --pollinterval=10
    [04/01/24 17:57:54] DEBUG    Starting System Compatibility Check                                                                                                                                               system.py:44
                        INFO     Machine: x86_64                                                                                                                                                                   system.py:61
                        INFO     Host: lbl-cluster                                                                                                                                                                 system.py:62
                        INFO     User: adaptive50                                                                                                                                                                  system.py:63
                        INFO     Operating System: ubuntu                                                                                                                                                          system.py:64
                        INFO     System Kernel: Linux and Kernel Release: 5.15.0-1036-aws                                                                                                                          system.py:65
                        INFO     Python Path: /home/adaptive50/.local/share/virtualenvs/buildtest-k4u5TT7g/bin/python3                                                                                             system.py:68
                        INFO     Python Version: 3.8.10                                                                                                                                                            system.py:69
                        INFO     BUILDTEST_ROOT: /home/adaptive50/buildtest                                                                                                                                        system.py:70
                        INFO     Path to Buildtest: /home/adaptive50/buildtest/bin/buildtest                                                                                                                       system.py:71
                        INFO     Detected module system: environment-modules                                                                                                                                      system.py:111
                        INFO     Detected environment-modules with version: /usr/lib/x86_64-linux-gnu/modulecmd.tcl                                                                                               system.py:112
                        DEBUG    We will check the following binaries ['sbatch', 'sacct', 'sacctmgr', 'sinfo', 'scancel'] for existence.                                                                        detection.py:22
                        DEBUG    Cannot find sbatch command in $PATH                                                                                                                                            detection.py:27
                        DEBUG    We will check the following binaries ['bsub', 'bqueues', 'bkill', 'bjobs'] for existence.                                                                                      detection.py:22
                        DEBUG    Cannot find bsub command in $PATH                                                                                                                                              detection.py:27
                        DEBUG    We will check the following binaries ['qsub', 'qstat', 'qdel', 'nodelist', 'showres', 'partlist'] for existence.                                                               detection.py:22
                        DEBUG    qsub: /usr/local/bin/qsub                                                                                                                                                      detection.py:30
                        DEBUG    qstat: /usr/local/bin/qstat                                                                                                                                                    detection.py:30
                        DEBUG    qdel: /usr/local/bin/qdel                                                                                                                                                      detection.py:30
                        DEBUG    Cannot find nodelist command in $PATH                                                                                                                                          detection.py:27
                        DEBUG    We will check the following binaries ['qsub', 'qstat', 'qdel', 'qstart', 'qhold', 'qmgr'] for existence.                                                                       detection.py:22
                        DEBUG    qsub: /usr/local/bin/qsub                                                                                                                                                      detection.py:30
                        DEBUG    qstat: /usr/local/bin/qstat                                                                                                                                                    detection.py:30
                        DEBUG    qdel: /usr/local/bin/qdel                                                                                                                                                      detection.py:30
                        DEBUG    qstart: /usr/local/bin/qstart                                                                                                                                                  detection.py:30
                        DEBUG    qhold: /usr/local/bin/qhold                                                                                                                                                    detection.py:30
                        DEBUG    qmgr: /usr/local/bin/qmgr                                                                                                                                                      detection.py:30
                        DEBUG    Check PBS version by running qsub --version command                                                                                                                           detection.py:261
                        DEBUG    Output of qsub --version:                                                                                                                                                     detection.py:262
                        DEBUG    Cannot find 'pbs_version' in output of qsub --version, this is not a OpenPBS Scheduler                                                                                        detection.py:265
                        DEBUG    We will check the following binaries ['qsub', 'qstat', 'qdel', 'qstart', 'qhold', 'qmgr'] for existence.                                                                       detection.py:22
                        DEBUG    qsub: /usr/local/bin/qsub                                                                                                                                                      detection.py:30
                        DEBUG    qstat: /usr/local/bin/qstat                                                                                                                                                    detection.py:30
                        DEBUG    qdel: /usr/local/bin/qdel                                                                                                                                                      detection.py:30
                        DEBUG    qstart: /usr/local/bin/qstart                                                                                                                                                  detection.py:30
                        DEBUG    qhold: /usr/local/bin/qhold                                                                                                                                                    detection.py:30
                        DEBUG    qmgr: /usr/local/bin/qmgr                                                                                                                                                      detection.py:30
                        DEBUG    Check Torque version by running qsub --version command                                                                                                                        detection.py:354
                        DEBUG    Output of qsub --version: Version: 7.0.1                                                                                                                                      detection.py:355
                                  Commit: b405f8c22d41d29cbf9b9016bc1146bf4559e895

                        DEBUG    Check if 'Commit:' exists in output of qsub --version                                                                                                                         detection.py:356
                        DEBUG    Found 'Commit:' in output of qsub --version, this must be a Torque Scheduler                                                                                                  detection.py:360
    [04/01/24 17:57:55] DEBUG    Get Torque Queues details by running 'qstat -Qf'                                                                                                                              detection.py:388
                        DEBUG    Output of qstat -Qf: Queue: lbl-cluster                                                                                                                                       detection.py:391
                                      queue_type = Execution
                                      total_jobs = 2
                                      state_count = Transit:0 Queued:0 Held:0 Waiting:0 Running:0 Exiting:0 Comp
                                         lete:2
                                      resources_default.nodes = 1
                                      resources_default.walltime = 24:00:00
                                      mtime = 1711641211
                                      resources_assigned.nodect = 0
                                      enabled = True
                                      started = True

                        DEBUG    Parse output of qstat -Qf to get queue details                                                                                                                                detection.py:392
                        DEBUG    {                                                                                                                                                                             detection.py:407
                                   "lbl-cluster": {
                                     "queue_type": "Execution",
                                     "total_jobs": "2",
                                     "state_count": "Transit:0 Queued:0 Held:0 Waiting:0 Running:0 Exiting:0 Comp",
                                     "resources_default.nodes": "1",
                                     "resources_default.walltime": "24:00:00",
                                     "mtime": "1711641211",
                                     "resources_assigned.nodect": "0",
                                     "enabled": "True",
                                     "started": "True"
                                   }
                                 }
                        DEBUG    Available Queues: ['lbl-cluster']                                                                                                                                             detection.py:408
                        DEBUG    Detected Torque Scheduler                                                                                                                                                         system.py:88
                        INFO     Finished System Compatibility Check                                                                                                                                               system.py:76
                        DEBUG    List of available systems: ['generic'] found in configuration file                                                                                                               config.py:102
                        DEBUG    Checking hostname: lbl-cluster in system: 'generic' with hostnames: ['.*']                                                                                                       config.py:117
                        INFO     Found matching system: generic based on hostname: lbl-cluster                                                                                                                    config.py:124
                        DEBUG    Loading default settings schema: /home/adaptive50/buildtest/buildtest/schemas/settings.schema.json                                                                               config.py:143
                        DEBUG    Successfully loaded schema file: /home/adaptive50/buildtest/buildtest/schemas/settings.schema.json                                                                                 utils.py:41
                        DEBUG    Validating configuration file with schema: /home/adaptive50/buildtest/buildtest/schemas/settings.schema.json                                                                     config.py:146
                        DEBUG    Validation was successful                                                                                                                                                        config.py:154
                        DEBUG    We will check the following binaries ['qsub', 'qstat', 'qdel', 'qstart', 'qhold', 'qmgr'] for existence.                                                                       detection.py:22
                        DEBUG    qsub: /usr/local/bin/qsub                                                                                                                                                      detection.py:30
                        DEBUG    qstat: /usr/local/bin/qstat                                                                                                                                                    detection.py:30
                        DEBUG    qdel: /usr/local/bin/qdel                                                                                                                                                      detection.py:30
                        DEBUG    qstart: /usr/local/bin/qstart                                                                                                                                                  detection.py:30
                        DEBUG    qhold: /usr/local/bin/qhold                                                                                                                                                    detection.py:30
                        DEBUG    qmgr: /usr/local/bin/qmgr                                                                                                                                                      detection.py:30
                        DEBUG    Check Torque version by running qsub --version command                                                                                                                        detection.py:354
                        DEBUG    Output of qsub --version: Version: 7.0.1                                                                                                                                      detection.py:355
                                  Commit: b405f8c22d41d29cbf9b9016bc1146bf4559e895

                        DEBUG    Check if 'Commit:' exists in output of qsub --version                                                                                                                         detection.py:356
                        DEBUG    Found 'Commit:' in output of qsub --version, this must be a Torque Scheduler                                                                                                  detection.py:360
                        DEBUG    Get Torque Queues details by running 'qstat -Qf'                                                                                                                              detection.py:388
                        DEBUG    Output of qstat -Qf: Queue: lbl-cluster                                                                                                                                       detection.py:391
                                      queue_type = Execution
                                      total_jobs = 2
                                      state_count = Transit:0 Queued:0 Held:0 Waiting:0 Running:0 Exiting:0 Comp
                                         lete:2
                                      resources_default.nodes = 1
                                      resources_default.walltime = 24:00:00
                                      mtime = 1711641211
                                      resources_assigned.nodect = 0
                                      enabled = True
                                      started = True

                        DEBUG    Parse output of qstat -Qf to get queue details                                                                                                                                detection.py:392
                        DEBUG    {                                                                                                                                                                             detection.py:407
                                   "lbl-cluster": {
                                     "queue_type": "Execution",
                                     "total_jobs": "2",
                                     "state_count": "Transit:0 Queued:0 Held:0 Waiting:0 Running:0 Exiting:0 Comp",
                                     "resources_default.nodes": "1",
                                     "resources_default.walltime": "24:00:00",
                                     "mtime": "1711641211",
                                     "resources_assigned.nodect": "0",
                                     "enabled": "True",
                                     "started": "True"
                                   }
                                 }
                        DEBUG    Available Queues: ['lbl-cluster']                                                                                                                                             detection.py:408
                        INFO     Processing buildtest configuration file: /home/adaptive50/buildtest/buildtest/settings/aws_oddc_pbs.yml                                                                            main.py:149
                        DEBUG    Tests will be written in /home/adaptive50/buildtest/var/tests                                                                                                                     build.py:792
                        DEBUG    Getting Executors from buildtest settings                                                                                                                                          setup.py:89
    ╭───────────────────────────────────────── buildtest summary ──────────────────────────────────────────╮
    │                                                                                                      │
    │ User:               adaptive50                                                                       │
    │ Hostname:           lbl-cluster                                                                      │
    │ Platform:           Linux                                                                            │
    │ Current Time:       2024/04/01 17:57:55                                                              │
    │ buildtest path:     /home/adaptive50/buildtest/bin/buildtest                                         │
    │ buildtest version:  1.8                                                                              │
    │ python path:        /home/adaptive50/.local/share/virtualenvs/buildtest-k4u5TT7g/bin/python3         │
    │ python version:     3.8.10                                                                           │
    │ Configuration File: /home/adaptive50/buildtest/buildtest/settings/aws_oddc_pbs.yml                   │
    │ Test Directory:     /home/adaptive50/buildtest/var/tests                                             │
    │ Report File:        /home/adaptive50/buildtest/var/report.json                                       │
    │ Command:            /home/adaptive50/buildtest/bin/buildtest -d build -b sleep.yml --pollinterval=10 │
    │                                                                                                      │
    ╰──────────────────────────────────────────────────────────────────────────────────────────────────────╯
                        DEBUG    Discovering buildspecs based on tags=None, executor=None, buildspec=['sleep.yml'], excluded buildspec=None                                                                        build.py:148
                        DEBUG    Buildspec: sleep.yml is a file                                                                                                                                                    build.py:559
                        INFO     Based on input argument we discovered the following buildspecs: ['/home/adaptive50/buildtest/aws_oddc/sleep.yml']                                                                 build.py:571
                        DEBUG    buildtest discovered the following Buildspecs: ['/home/adaptive50/buildtest/aws_oddc/sleep.yml']                                                                                  build.py:227
    ─────────────────────────────────────────────────────────────────────────────────────────────────  Discovering Buildspecs ─────────────────────────────────────────────────────────────────────────────────────────────────
                  Discovered buildspecs
    ╔═══════════════════════════════════════════════╗
    ║ buildspec                                     ║
    ╟───────────────────────────────────────────────╢
    ║ /home/adaptive50/buildtest/aws_oddc/sleep.yml ║
    ╟───────────────────────────────────────────────╢
    ║ Total: 1                                      ║
    ╚═══════════════════════════════════════════════╝


    Total Discovered Buildspecs:  1
    Total Excluded Buildspecs:  0
    Detected Buildspecs after exclusion:  1
    ─────────────────────────────────────────────────────────────────────────────────────────────────── Parsing Buildspecs ────────────────────────────────────────────────────────────────────────────────────────────────────
                        INFO     Validating /home/adaptive50/buildtest/aws_oddc/sleep.yml with schema: /home/adaptive50/buildtest/buildtest/schemas/global.schema.json                                            parser.py:164
                        INFO     Validating test - 'hostname_test' in recipe: /home/adaptive50/buildtest/aws_oddc/sleep.yml                                                                                       parser.py:176
                        INFO     Test: 'hostname_test' is using schema type: 'script'                                                                                                                             parser.py:118
                        INFO     Validating /home/adaptive50/buildtest/aws_oddc/sleep.yml with schema:  /home/adaptive50/buildtest/buildtest/schemas/script.schema.json                                           parser.py:193
                        DEBUG    Searching for builders for test: hostname_test by applying regular expression with available builders: ['generic.local.bash', 'generic.torque.e4spro']                         builders.py:272
                        DEBUG    Found a match in buildspec with available executors via re.fullmatch(generic.torque.e4spro,generic.torque.e4spro)                                                              builders.py:280
                        DEBUG    Processing Buildspec File: /home/adaptive50/buildtest/aws_oddc/sleep.yml                                                                                                           base.py:144
                        DEBUG    Processing Test: hostname_test                                                                                                                                                     base.py:145
                        DEBUG    Using shell bash                                                                                                                                                                   base.py:181
                        DEBUG    Shebang used for test: #!/usr/bin/bash                                                                                                                                             base.py:182
    Valid Buildspecs: 1
    Invalid Buildspecs: 0
    /home/adaptive50/buildtest/aws_oddc/sleep.yml: VALID
    Total builder objects created: 1
                                                                        Builders by type=script
    ┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ builder                ┃ type   ┃ executor              ┃ compiler ┃ nodes ┃ procs ┃ description             ┃ buildspecs                                    ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ hostname_test/3509bd3d │ script │ generic.torque.e4spro │ None     │ None  │ None  │ run sleep for 5 seconds │ /home/adaptive50/buildtest/aws_oddc/sleep.yml │
    └────────────────────────┴────────┴───────────────────────┴──────────┴───────┴───────┴─────────────────────────┴───────────────────────────────────────────────┘
                                            Batch Job Builders
    ┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ builder                ┃ executor              ┃ buildspecs                                    ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ hostname_test/3509bd3d │ generic.torque.e4spro │ /home/adaptive50/buildtest/aws_oddc/sleep.yml │
    └────────────────────────┴───────────────────────┴───────────────────────────────────────────────┘
    ────────────────────────────────────────────────────────────────────────────────────────────────────── Building Test ──────────────────────────────────────────────────────────────────────────────────────────────────────
                        DEBUG    Creating test directory: /home/adaptive50/buildtest/var/tests/generic.torque.e4spro/sleep/hostname_test/3509bd3d                                                                   base.py:527
                        DEBUG    Creating the stage directory: /home/adaptive50/buildtest/var/tests/generic.torque.e4spro/sleep/hostname_test/3509bd3d/stage                                                        base.py:536
    hostname_test/3509bd3d: Creating Test Directory: /home/adaptive50/buildtest/var/tests/generic.torque.e4spro/sleep/hostname_test/3509bd3d
                        INFO     Opening Test File for Writing: /home/adaptive50/buildtest/var/tests/generic.torque.e4spro/sleep/hostname_test/3509bd3d/stage/hostname_test.sh                                      base.py:658
                        DEBUG    Changing permission to 755 for script: /home/adaptive50/buildtest/var/tests/generic.torque.e4spro/sleep/hostname_test/3509bd3d/stage/hostname_test.sh                              base.py:856
                        DEBUG    Writing build script: /home/adaptive50/buildtest/var/tests/generic.torque.e4spro/sleep/hostname_test/3509bd3d/stage/hostname_test_build.sh                                         base.py:631
                        DEBUG    Changing permission to 755 for script: /home/adaptive50/buildtest/var/tests/generic.torque.e4spro/sleep/hostname_test/3509bd3d/stage/hostname_test_build.sh                        base.py:856
                        DEBUG    Copying build script to: /home/adaptive50/buildtest/var/tests/generic.torque.e4spro/sleep/hostname_test/3509bd3d/hostname_test_build.sh                                            base.py:637
    ────────────────────────────────────────────────────────────────────────────────────────────────────── Running Tests ──────────────────────────────────────────────────────────────────────────────────────────────────────
    Spawning 4 processes for processing builders
    ─────────────────────────────────────────────────────────────────────────────────────────────────────── Iteration 1 ───────────────────────────────────────────────────────────────────────────────────────────────────────
    hostname_test/3509bd3d does not have any dependencies adding test to queue
     Builders Eligible to Run
    ┏━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Builder                ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ hostname_test/3509bd3d │
    └────────────────────────┘
    hostname_test/3509bd3d: Current Working Directory : /home/adaptive50/buildtest/var/tests/generic.torque.e4spro/sleep/hostname_test/3509bd3d/stage
    hostname_test/3509bd3d: Running Test via command: bash hostname_test_build.sh
                        DEBUG    Running Test via command: bash hostname_test_build.sh                                                                                                                              base.py:378
    hostname_test/3509bd3d: JobID: 48970006.lbl-cluster dispatched to scheduler
                        DEBUG    hostname_test/3509bd3d: JobID: 48970006.lbl-cluster dispatched to scheduler                                                                                                          pbs.py:96
    Polling Jobs in 10 seconds
    [04/01/24 17:58:05] DEBUG    Polling job by running: qstat -f 48970006.lbl-cluster                                                                                                                               pbs.py:203
                        DEBUG    Extracting Job ID from output of command: qstat -f 48970006.lbl-cluster by applying regular expression pattern: '^Job Id:\s*(?P<jobid>\S+)'. The return value is <re.Match object;  pbs.py:210
                                 span=(0, 28), match='Job Id: 48970006.lbl-cluster'>
                        DEBUG    Retrieving exitcode for Job: 48970006.lbl-cluster by applying regular expression pattern: '^\s*exit_status = (?P<code>\d+)'. The return value is None                               pbs.py:235
                        DEBUG    /home/adaptive50/buildtest/var/tests/generic.torque.e4spro/sleep/hostname_test/3509bd3d/stage/hostname_test.o                                                                        pbs.py:72
                                                Pending and Suspended Jobs (1)
    ┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
    ┃ builder                ┃ executor              ┃ jobid                ┃ jobstate ┃ runtime ┃ elapsedtime ┃ pendtime ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
    │ hostname_test/3509bd3d │ generic.torque.e4spro │ 48970006.lbl-cluster │ Q        │ 10.086  │ 0           │ 10.05    │
    └────────────────────────┴───────────────────────┴──────────────────────┴──────────┴─────────┴─────────────┴──────────┘
    Polling Jobs in 10 seconds
    [04/01/24 17:58:15] DEBUG    Polling job by running: qstat -f 48970006.lbl-cluster                                                                                                                               pbs.py:203
                        DEBUG    Extracting Job ID from output of command: qstat -f 48970006.lbl-cluster by applying regular expression pattern: '^Job Id:\s*(?P<jobid>\S+)'. The return value is <re.Match object;  pbs.py:210
                                 span=(0, 28), match='Job Id: 48970006.lbl-cluster'>
                        DEBUG    Retrieving exitcode for Job: 48970006.lbl-cluster by applying regular expression pattern: '^\s*exit_status = (?P<code>\d+)'. The return value is None                               pbs.py:235
                                                Pending and Suspended Jobs (1)
    ┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
    ┃ builder                ┃ executor              ┃ jobid                ┃ jobstate ┃ runtime ┃ elapsedtime ┃ pendtime ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
    │ hostname_test/3509bd3d │ generic.torque.e4spro │ 48970006.lbl-cluster │ Q        │ 20.114  │ 0           │ 20.08    │
    └────────────────────────┴───────────────────────┴──────────────────────┴──────────┴─────────┴─────────────┴──────────┘
    Polling Jobs in 10 seconds
    [04/01/24 17:58:25] DEBUG    Polling job by running: qstat -f 48970006.lbl-cluster                                                                                                                               pbs.py:203
                        DEBUG    Extracting Job ID from output of command: qstat -f 48970006.lbl-cluster by applying regular expression pattern: '^Job Id:\s*(?P<jobid>\S+)'. The return value is <re.Match object;  pbs.py:210
                                 span=(0, 28), match='Job Id: 48970006.lbl-cluster'>
                        DEBUG    Retrieving exitcode for Job: 48970006.lbl-cluster by applying regular expression pattern: '^\s*exit_status = (?P<code>\d+)'. The return value is <re.Match object; span=(3956,      pbs.py:235
                                 3976), match='     exit_status = 0'>
                        DEBUG    Retrieve exitcode: 0 for Job: 48970006.lbl-cluster                                                                                                                                  pbs.py:240
                        DEBUG     returncode: 0                                                                                                                                                                     base.py:132
    hostname_test/3509bd3d: Job 48970006.lbl-cluster is complete!
    hostname_test/3509bd3d: Test completed in 0 seconds with returncode: 0
    hostname_test/3509bd3d: Writing output file -  /home/adaptive50/buildtest/var/tests/generic.torque.e4spro/sleep/hostname_test/3509bd3d/hostname_test.o
    hostname_test/3509bd3d: Writing error file - /home/adaptive50/buildtest/var/tests/generic.torque.e4spro/sleep/hostname_test/3509bd3d/hostname_test.e
                                                      Completed Jobs (1)
    ┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
    ┃ builder                ┃ executor              ┃ jobid                ┃ jobstate ┃ runtime ┃ elapsedtime ┃ pendtime ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
    │ hostname_test/3509bd3d │ generic.torque.e4spro │ 48970006.lbl-cluster │ C        │ 0       │ 0           │ 20.08    │
    └────────────────────────┴───────────────────────┴──────────────────────┴──────────┴─────────┴─────────────┴──────────┘
                                       Test Summary
    ┏━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━┓
    ┃ builder                ┃ executor              ┃ status ┃ returncode ┃ runtime ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━┩
    │ hostname_test/3509bd3d │ generic.torque.e4spro │ PASS   │ 0          │ 0.000   │
    └────────────────────────┴───────────────────────┴────────┴────────────┴─────────┘



    Passed Tests: 1/1 Percentage: 100.000%
    Failed Tests: 0/1 Percentage: 0.000%


                        DEBUG    Updating report file: /home/adaptive50/buildtest/var/report.json                                                                                                                 build.py:1721
    Adding 1 test results to report file: /home/adaptive50/buildtest/var/report.json
    Writing Logfile to /home/adaptive50/buildtest/var/logs/buildtest_z2vikoox.log

.. _max_pend_time:

Jobs exceeds `max_pend_time`
-----------------------------

Recall from :ref:`configuring_buildtest` that `max_pend_time` will cancel jobs if
job exceed timelimit. buildtest will start a timer for each job right after job
submission and keep track of time duration, and if job is in **pending** state and it exceeds `max_pend_time`,
then job will be cancelled.

We can also override ``maxpendtime`` configuration via command line ``--maxpendtime``.
To demonstrate, here is an example where job  was cancelled after job was pending and exceeds `max_pend_time`.
Note that cancelled job is not reported in final output nor updated in report hence
it won't be present in the report (``buildtest report``). In this example, we only
had one test so upon job cancellation we found there was no tests to report hence,
buildtest will terminate after run stage.

.. dropdown:: ``buildtest build -b tau.yml --pollinterval=3 --maxpendtime=7``

    .. code-block:: console

       (buildtest) siddiq90@login10> buildtest build -b tau.yml --pollinterval=3 --maxpendtime=7
        ╭─────────────────────────────────────────────────────── buildtest summary ───────────────────────────────────────────────────────╮
        │                                                                                                                                 │
        │ User:               siddiq90                                                                                                    │
        │ Hostname:           login10                                                                                                     │
        │ Platform:           Linux                                                                                                       │
        │ Current Time:       2023/11/07 17:12:41                                                                                         │
        │ buildtest path:     /global/homes/s/siddiq90/gitrepos/buildtest/bin/buildtest                                                   │
        │ buildtest version:  1.6                                                                                                         │
        │ python path:        /global/u1/s/siddiq90/.local/share/virtualenvs/buildtest-WqshQcL1/bin/python3                               │
        │ python version:     3.9.7                                                                                                       │
        │ Configuration File: /global/u1/s/siddiq90/gitrepos/buildtest-nersc/config.yml                                                   │
        │ Test Directory:     /global/u1/s/siddiq90/gitrepos/buildtest/var/tests                                                          │
        │ Report File:        /global/u1/s/siddiq90/gitrepos/buildtest/var/report.json                                                    │
        │ Command:            /global/homes/s/siddiq90/gitrepos/buildtest/bin/buildtest build -b tau.yml --pollinterval=3 --maxpendtime=7 │
        │                                                                                                                                 │
        ╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
        ──────────────────────────────────────────────────────────  Discovering Buildspecs ───────────────────────────────────────────────────────────
                                                Discovered buildspecs
        ╔═══════════════════════════════════════════════════════════════════════════════════════════════════╗
        ║ buildspec                                                                                         ║
        ╟───────────────────────────────────────────────────────────────────────────────────────────────────╢
        ║ /global/u1/s/siddiq90/gitrepos/buildtest-nersc/buildspecs/e4s/spack_test/perlmutter/23.05/tau.yml ║
        ╚═══════════════════════════════════════════════════════════════════════════════════════════════════╝


        Total Discovered Buildspecs:  1
        Total Excluded Buildspecs:  0
        Detected Buildspecs after exclusion:  1
        ───────────────────────────────────────────────────────────── Parsing Buildspecs ─────────────────────────────────────────────────────────────
        Valid Buildspecs: 1
        Invalid Buildspecs: 0
        /global/u1/s/siddiq90/gitrepos/buildtest-nersc/buildspecs/e4s/spack_test/perlmutter/23.05/tau.yml: VALID
        Total builder objects created: 1
                                                                    Builders by type=spack
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ builder                  ┃ type  ┃ executor                ┃ compiler ┃ nodes ┃ procs ┃ description              ┃ buildspecs              ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ tau_spack-test_23.05/126 │ spack │ perlmutter.slurm.regula │ None     │ None  │ None  │ Run spack test for tau   │ /global/u1/s/siddiq90/g │
        │ e2cb5                    │       │ r                       │          │       │       │ from e4s/23.05 gcc stack │ itrepos/buildtest-nersc │
        │                          │       │                         │          │       │       │                          │ /buildspecs/e4s/spack_t │
        │                          │       │                         │          │       │       │                          │ est/perlmutter/23.05/ta │
        │                          │       │                         │          │       │       │                          │ u.yml                   │
        └──────────────────────────┴───────┴─────────────────────────┴──────────┴───────┴───────┴──────────────────────────┴─────────────────────────┘
                                                                      Batch Job Builders
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ builder                       ┃ executor                 ┃ buildspecs                                                                      ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ tau_spack-test_23.05/126e2cb5 │ perlmutter.slurm.regular │ /global/u1/s/siddiq90/gitrepos/buildtest-nersc/buildspecs/e4s/spack_test/perlmu │
        │                               │                          │ tter/23.05/tau.yml                                                              │
        └───────────────────────────────┴──────────────────────────┴─────────────────────────────────────────────────────────────────────────────────┘
        ─────────────────────────────────────────────────────────────── Building Test ────────────────────────────────────────────────────────────────
        tau_spack-test_23.05/126e2cb5: Creating test directory: /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/perlmutter.slurm.regular/tau/tau_spack-test_23.05/126e2cb5
        tau_spack-test_23.05/126e2cb5: Creating the stage directory: /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/perlmutter.slurm.regular/tau/tau_spack-test_23.05/126e2cb5/stage
        tau_spack-test_23.05/126e2cb5: Writing build script: /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/perlmutter.slurm.regular/tau/tau_spack-test_23.05/126e2cb5/tau_spack-test_23.05_build.sh
        ─────────────────────────────────────────────────────────────── Running Tests ────────────────────────────────────────────────────────────────
        Spawning 8 processes for processing builders
        ──────────────────────────────────────────────────────────────── Iteration 1 ─────────────────────────────────────────────────────────────────
        tau_spack-test_23.05/126e2cb5 does not have any dependencies adding test to queue
            Builders Eligible to Run
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃ Builder                       ┃
        ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
        │ tau_spack-test_23.05/126e2cb5 │
        └───────────────────────────────┘
        tau_spack-test_23.05/126e2cb5: Current Working Directory : /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/perlmutter.slurm.regular/tau/tau_spack-test_23.05/126e2cb5/stage
        tau_spack-test_23.05/126e2cb5: Running Test via command: bash --norc --noprofile -eo pipefail tau_spack-test_23.05_build.sh
        tau_spack-test_23.05/126e2cb5: JobID 18005951 dispatched to scheduler
        Polling Jobs in 3 seconds
        tau_spack-test_23.05/126e2cb5: Cancelling Job 18005951 because job exceeds max pend time of 7 sec with current pend time of 8.6 sec
        buildtest build command failed
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
