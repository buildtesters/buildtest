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
if you have defined LSF executors in your configuration file.

The ``bsub`` property can be used to  specify **#BSUB** directive into job script. This example
will use the executor ``ascent.lsf.batch`` executor that was defined in buildtest configuration.

.. code-block:: yaml
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


Cobalt
-------

`Cobalt <https://trac.mcs.anl.gov/projects/cobalt>`_ is a job scheduler developed
by `Argonne National Laboratory <https://www.anl.gov/>`_ that runs on compute
resources and IBM BlueGene series. Cobalt resembles `PBS <https://community.altair.com/community?id=altair_product_documentation>`_
in terms of command line interface such as ``qsub``, ``qacct`` however they
slightly differ in their behavior.

Cobalt support has been tested on JLSE and Theta system. Cobalt directives
are specified using ``#COBALT`` this can be specified using ``cobalt`` property
which accepts a list of strings. Shown below is an example using cobalt property.

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
