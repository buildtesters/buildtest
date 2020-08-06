Batch Scheduler Support
========================

buildtest batch scheduler support is an experimental feature, currently buildtest
supports Slurm and LSF Executor. In order for buildtest to submit jobs to scheduler,
you must define a slurm or lsf executor.

Slurm Executor (Experimental Feature)
--------------------------------------

The ``SlurmExecutor`` class is responsible for managing slurm jobs which
will perform the following action

  1. Check slurm binary ``sbatch`` and ``sacct``.
  2. Dispatch Job and acquire job ID using ``sacct``.
  3. Poll all slurm jobs until all have finished
  4. Gather Job results once job is complete via ``sacct``.

buildtest will dispatch all jobs and poll all jobs in a ``while (True)`` until all
jobs are complete. If job is in [**PENDING** | **RUNNING** ] then buildtest will
keep polling at a set interval. Once job is not in **PENDING**
or **RUNNING** stage, buildtest will gather job results and wait until all jobs have
finished.

In order to use a slurm scheduler, you must define a :ref:`slurm_executors` and reference
it via ``executor``. In this example we have a slurm executor ``slurm.debug``,
in addition we can specify **#SBATCH** directives using ``sbatch`` field.
The sbatch field is a list of string types, buildtest will
insert **#SBATCH** directive in front of each value.

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

buildtest will add the ``#SBATCH`` directives at top of script followed by
content in the ``run`` section. Shown below is the example test content ::

    #!/bin/bash
    #SBATCH -t 00:05
    #SBATCH -C haswell
    #SBATCH -N 1
    export SLURM_JOB_NAME="firstjob"
    echo "jobname:" $SLURM_JOB_NAME
    echo "slurmdb host:" $SLURMD_NODENAME
    echo "pid:" $SLURM_TASK_PID
    echo "submit host:" $SLURM_SUBMIT_HOST
    echo "nodeid:" $SLURM_NODEID
    echo "partition:" $SLURM_JOB_PARTITION

The slurm.debug executor in our ``settings.yml`` is defined as follows::

    slurm:
      debug:
        description: jobs for debug qos
        qos: debug
        cluster: cori

With this setting, any buildspec test that use ``slurm.debug`` executor will result
in the following launch option: ``sbatch --qos debug --cluster cori </path/to/script.sh>``.

Unlike the LocalExecutor, the **Run stage**, will dispatch the slurm job and poll
until job is completed. Once job is complete, it will gather the results and terminate.
In Run stage, buildtest will mark status as ``N/A`` for jobs submitted to scheduler, this
is because we don't have result until we finish polling and gather results. buildtest
keeps track of all buildspecs, testscripts to be run and their results. A test
using LocalExecutor will run test in **Run Stage** and returncode will be retrieved
and status can be calculated immediately. For Slurm Jobs, buildtest dispatches
the job and process next job. buildtest will show output of all tests after
**Polling Stage** with test results of all tests. A slurm job with exit code 0 will
be marked with status ``PASS``.

Shown below is an example build for this test ::

    $ buildtest build -b metadata.yml
    Paths:
    __________
    Prefix: /global/u1/s/siddiq90/cache
    Buildspec Search Path: ['/global/homes/s/siddiq90/.buildtest/site']
    Test Directory: /global/u1/s/siddiq90/cache/tests

    +-------------------------------+
    | Stage: Discovered Buildspecs  |
    +-------------------------------+

    /global/u1/s/siddiq90/buildtest-cori/slurm/valid_jobs/metadata.yml

    +----------------------+
    | Stage: Building Test |
    +----------------------+

     Name           | Schema File             | Test Path                                                    | Buildspec
    ----------------+-------------------------+--------------------------------------------------------------+--------------------------------------------------------------------
     slurm_metadata | script-v1.0.schema.json | /global/u1/s/siddiq90/cache/tests/metadata/slurm_metadata.sh | /global/u1/s/siddiq90/buildtest-cori/slurm/valid_jobs/metadata.yml

    +----------------------+
    | Stage: Running Test  |
    +----------------------+

    [slurm_metadata] job dispatched to scheduler
    [slurm_metadata] acquiring job id in 2 seconds
     name           | executor    | status   |   returncode | testpath
    ----------------+-------------+----------+--------------+--------------------------------------------------------------
     slurm_metadata | slurm.debug | N/A      |            0 | /global/u1/s/siddiq90/cache/tests/metadata/slurm_metadata.sh


    Polling Jobs in 10 seconds
    ________________________________________
    [slurm_metadata]: JobID 32740760 in PENDING state


    Polling Jobs in 10 seconds
    ________________________________________
    [slurm_metadata]: JobID 32740760 in COMPLETED state


    Polling Jobs in 10 seconds
    ________________________________________

    +---------------------------------------------+
    | Stage: Final Results after Polling all Jobs |
    +---------------------------------------------+

     name           | executor    | status   |   returncode | testpath
    ----------------+-------------+----------+--------------+--------------------------------------------------------------
     slurm_metadata | slurm.debug | PASS     |            0 | /global/u1/s/siddiq90/cache/tests/metadata/slurm_metadata.sh

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Executed 1 tests
    Passed Tests: 1/1 Percentage: 100.000%
    Failed Tests: 0/1 Percentage: 0.000%

The **SlurmExecutor** class responsible for managing slurm job will retrieve the
following format fields using ``sacct`` during ``gather`` stage once job is finished:

-    "Account"
-    "AllocNodes"
-    "AllocTRES"
-    "ConsumedEnergyRaw"
-    "CPUTimeRaw"
-    "End"
-    "ExitCode"
-    "JobID"
-    "JobName"
-    "NCPUS"
-    "NNodes"
-    "QOS"
-    "ReqGRES"
-    "ReqMem"
-    "ReqNodes"
-    "ReqTRES"
-    "Start"
-    "State"
-    "Submit"
-    "UID"
-    "User"
-    "WorkDir"

buildtest can check status based on Slurm Job State, this is defined by ``State`` field
in sacct. In next example, we introduce field ``slurm_job_state_codes`` which
is part of ``status`` field. This field expects one of the following values: ``[COMPLETED, FAILED, OUT_OF_MEMORY, TIMEOUT ]``
This is an example of simulating fail job by expecting a return code of 1 with job
state of ``FAILED``.

::

    version: "1.0"
    buildspecs:
      wall_timeout:
        type: script
        executor: slurm.debug
        sbatch: [ "-t 2", "-C haswell", "-n 1"]
        run: exit 1
        status:
          slurm_job_state_codes: "FAILED"


If we run this test, buildtest will mark this test as ``PASS`` because the slurm job
state matches with expected result even though returncode is 1.

::

    +---------------------------------------------+
    | Stage: Final Results after Polling all Jobs |
    +---------------------------------------------+

     name         | executor    | status   |   returncode | testpath
    --------------+-------------+----------+--------------+---------------------------------------------------------
     wall_timeout | slurm.debug | PASS     |            1 | /global/u1/s/siddiq90/cache/tests/exit1/wall_timeout.sh

If you examine the logfile ``buildtest.log`` you will see an entry of ``sacct`` command run to gather
results followed by list of field and value output::

    2020-07-22 18:20:48,170 [base.py:587 - gather() ] - [DEBUG] Gather slurm job data by running: sacct -j 32741040 -X -n -P -o Account,AllocNodes,AllocTRES,ConsumedEnergyRaw,CPUTimeRaw,End,ExitCode,JobID,JobName,NCPUS,NNodes,QOS,ReqGRES,ReqMem,ReqNodes,ReqTRES,Start,State,Submit,UID,User,WorkDir -M cori
    ...
    2020-07-22 18:20:48,405 [base.py:598 - gather() ] - [DEBUG] field: State   value: FAILED




LSF Executor (Experimental)
----------------------------

The **LSFExecutor** is responsible for submitting jobs to LSF scheduler. The LSFExecutor
behaves similar to SlurmExecutor with the five stages implemented as class methods:

- Check: check lsf binaries (``bsub``, ``bjobs``)
- Load: load lsf executor from buildtest configuration ``config.yml``
- Dispatch: Dispatch job using bsub and retrieve JobID
- Poll: Poll job using ``bjobs`` to retrieve job state
- Gather: Retrieve job results once job is finished

The ``bsub`` key works similar to ``sbatch`` key which allows one to specify **#BSUB**
directive into job script. This example will use the ``lsf.batch`` executor with
executor name ``batch`` defined in buildtest configuration.

::

    version: "1.0"
    buildspecs:
      hostname:
        type: script
        executor: lsf.batch
        bsub: [ "-W 10",  "-nnodes 1", "-P gen014ecpci"]

        run: jsrun hostname

The LSFExecutor ``poll`` method will retrieve job state using
``bjobs -noheader -o 'stat' <JOBID>``. The LSFExecutor will poll
job so long as they are in **PEND** or **RUN** state. Once job is not in
any of the two states, LSFExecutor will proceed to ``gather`` stage and acquire
job results.

The LSFExecutor ``gather`` method will retrieve the following format fields using
``bjobs``

-    "job_name"
-    "stat"
-    "user"
-    "user_group"
-    "queue"
-    "proj_name"
-    "pids"
-    "exit_code"
-    "from_host"
-    "exec_host"
-    "submit_time"
-    "start_time"
-    "finish_time"
-    "nthreads"
-    "exec_home"
-    "exec_cwd"
-    "output_file"
-    "error_file"


