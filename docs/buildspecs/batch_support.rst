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
    :linenos:
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
    :linenos:
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
    :linenos:
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

    $ buildtest build -b buildspecs/jobs/metadata.yml


    User:  siddiq90
    Hostname:  cori02
    Platform:  Linux
    Current Time:  2021/06/11 09:24:44
    buildtest path: /global/homes/s/siddiq90/github/buildtest/bin/buildtest
    buildtest version:  0.9.5
    python path: /global/homes/s/siddiq90/.conda/envs/buildtest/bin/python
    python version:  3.8.8
    Test Directory:  /global/u1/s/siddiq90/github/buildtest/var/tests
    Configuration File:  /global/u1/s/siddiq90/.buildtest/config.yml
    Command: /global/homes/s/siddiq90/github/buildtest/bin/buildtest build -b buildspecs/jobs/metadata.yml

    +-------------------------------+
    | Stage: Discovering Buildspecs |
    +-------------------------------+

    +--------------------------------------------------------------------------+
    | Discovered Buildspecs                                                    |
    +==========================================================================+
    | /global/u1/s/siddiq90/github/buildtest-cori/buildspecs/jobs/metadata.yml |
    +--------------------------------------------------------------------------+
    Discovered Buildspecs:  1
    Excluded Buildspecs:  0
    Detected Buildspecs after exclusion:  1

    +---------------------------+
    | Stage: Parsing Buildspecs |
    +---------------------------+

     schemafile              | validstate   | buildspec
    -------------------------+--------------+--------------------------------------------------------------------------
     script-v1.0.schema.json | True         | /global/u1/s/siddiq90/github/buildtest-cori/buildspecs/jobs/metadata.yml



    name            description
    --------------  --------------------------------------------------
    slurm_metadata  Get metadata from compute node when submitting job

    +----------------------+
    | Stage: Building Test |
    +----------------------+

     name           | id       | type   | executor             | tags     | testpath
    ----------------+----------+--------+----------------------+----------+-------------------------------------------------------------------------------------------------------------------------
     slurm_metadata | 722b3291 | script | cori.slurm.knl_debug | ['jobs'] | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/metadata/slurm_metadata/0/slurm_metadata_build.sh



    +---------------------+
    | Stage: Running Test |
    +---------------------+

    [slurm_metadata] JobID: 43308838 dispatched to scheduler
     name           | id       | executor             | status   |   returncode
    ----------------+----------+----------------------+----------+--------------
     slurm_metadata | 722b3291 | cori.slurm.knl_debug | N/A      |           -1


    Polling Jobs in 30 seconds
    ________________________________________
    Job Queue: [43308838]


    Pending Jobs
    ________________________________________


    +----------------+----------------------+----------+-----------+
    |      name      |       executor       |  jobID   | jobstate  |
    +----------------+----------------------+----------+-----------+
    | slurm_metadata | cori.slurm.knl_debug | 43308838 | COMPLETED |
    +----------------+----------------------+----------+-----------+


    Polling Jobs in 30 seconds
    ________________________________________
    Job Queue: []


    Completed Jobs
    ________________________________________


    +----------------+----------------------+----------+-----------+
    |      name      |       executor       |  jobID   | jobstate  |
    +----------------+----------------------+----------+-----------+
    | slurm_metadata | cori.slurm.knl_debug | 43308838 | COMPLETED |
    +----------------+----------------------+----------+-----------+

    +---------------------------------------------+
    | Stage: Final Results after Polling all Jobs |
    +---------------------------------------------+

     name           | id       | executor             | status   |   returncode
    ----------------+----------+----------------------+----------+--------------
     slurm_metadata | 722b3291 | cori.slurm.knl_debug | PASS     |            0

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Passed Tests: 1/1 Percentage: 100.000%
    Failed Tests: 0/1 Percentage: 0.000%


    Writing Logfile to: /tmp/buildtest_u8ehladd.log
    A copy of logfile can be found at $BUILDTEST_ROOT/buildtest.log -  /global/homes/s/siddiq90/github/buildtest/buildtest.log

The **SlurmExecutor** class is responsible for processing slurm job that may include:
dispatch, poll, gather, or cancel job. The SlurmExecutor will gather job metrics
via `sacct <https://slurm.schedmd.com/sacct.html>`_ using the following format fields:
**Account**, **AllocNodes**, **AllocTRES**, **ConsumedEnergyRaw**, **CPUTimeRaw**, **Elapsed**,
**End**, **ExitCode**, **JobID**, **JobName**, **NCPUS**, **NNodes**, **QOS**, **ReqGRES**,
**ReqMem**, **ReqNodes**, **ReqTRES**, **Start**, **State**, **Submit**, **UID**, **User**, **WorkDir**.
For a complete list of format fields see ``sacct -e``. For now, we support only these fields of interest
for reporting purpose.

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
        executor: cori.slurm.debug
        sbatch: [ "-t 2", "-C haswell", "-n 1"]
        run: sleep 300
        status:
          slurm_job_state: "TIMEOUT"


If we run this test, buildtest will mark this test as ``PASS`` because the slurm job
state matches with expected result defined by field ``slurm_job_state``. This job will
be TIMEOUT because we requested 2 mins while this job will sleep 300sec (5min).

.. code-block:: console
    :emphasize-lines: 8,17

       Completed Jobs
    ________________________________________


    +--------------+--------------------------+----------+----------+
    |     name     |         executor         |  jobID   | jobstate |
    +--------------+--------------------------+----------+----------+
    | wall_timeout | cori.slurm.haswell_debug | 43309265 | TIMEOUT  |
    +--------------+--------------------------+----------+----------+

    +---------------------------------------------+
    | Stage: Final Results after Polling all Jobs |
    +---------------------------------------------+

     name         | id       | executor                 | status   |   returncode
    --------------+----------+--------------------------+----------+--------------
     wall_timeout | 3b43850c | cori.slurm.haswell_debug | PASS     |            0

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Passed Tests: 1/1 Percentage: 100.000%
    Failed Tests: 0/1 Percentage: 0.000%


    Writing Logfile to: /tmp/buildtest_k6h246yx.log
    A copy of logfile can be found at $BUILDTEST_ROOT/buildtest.log -  /global/homes/s/siddiq90/github/buildtest/buildtest.log


If you examine the logfile ``buildtest.log`` you will see an entry of ``sacct`` command run to gather
results followed by list of field and value output::

    2021-06-11 09:52:27,826 [slurm.py:292 -  poll() ] - [DEBUG] Querying JobID: '43309265'  Job State by running: 'sacct -j 43309265 -o State -n -X -P --clusters=cori'
    2021-06-11 09:52:27,826 [slurm.py:296 -  poll() ] - [DEBUG] JobID: '43309265' job state:TIMEOUT

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
we use **-x** option to retrieve finished jobs which is required inorder for buildtest to detect job
state upon completion. Please see :ref:`pbs_limitation` to ensure your PBS cluster supports job history.

Shown below is an example build of the buildspec using PBS scheduler.


.. code-block:: console

    [pbsuser@pbs buildtest]$ buildtest build -b general_tests/sched/pbs/hostname.yml

    +-------------------------------+
    | Stage: Discovering Buildspecs |
    +-------------------------------+


    Discovered Buildspecs:

    /tmp/Documents/buildtest/general_tests/sched/pbs/hostname.yml

    +---------------------------+
    | Stage: Parsing Buildspecs |
    +---------------------------+

     schemafile              | validstate   | buildspec
    -------------------------+--------------+---------------------------------------------------------------
     script-v1.0.schema.json | True         | /tmp/Documents/buildtest/general_tests/sched/pbs/hostname.yml

    +----------------------+
    | Stage: Building Test |
    +----------------------+

     name      | id       | type   | executor          | tags   | testpath
    -----------+----------+--------+-------------------+--------+---------------------------------------------------------------------------------------------
     pbs_sleep | 2adfc3c1 | script | generic.pbs.workq |        | /tmp/Documents/buildtest/var/tests/generic.pbs.workq/hostname/pbs_sleep/3/stage/generate.sh



    +----------------------+
    | Stage: Running Test  |
    +----------------------+

    [pbs_sleep] JobID: 40.pbs dispatched to scheduler
     name      | id       | executor          | status   |   returncode | testpath
    -----------+----------+-------------------+----------+--------------+---------------------------------------------------------------------------------------------
     pbs_sleep | 2adfc3c1 | generic.pbs.workq | N/A      |           -1 | /tmp/Documents/buildtest/var/tests/generic.pbs.workq/hostname/pbs_sleep/3/stage/generate.sh


    Polling Jobs in 10 seconds
    ________________________________________
    Job Queue: ['40.pbs']


    Completed Jobs
    ________________________________________


    ╒════════╤════════════╤═════════╤════════════╕
    │ name   │ executor   │ jobID   │ jobstate   │
    ╞════════╪════════════╪═════════╪════════════╡
    ╘════════╧════════════╧═════════╧════════════╛


    Pending Jobs
    ________________________________________


    ╒═══════════╤═══════════════════╤═════════╤════════════╕
    │ name      │ executor          │ jobID   │ jobstate   │
    ╞═══════════╪═══════════════════╪═════════╪════════════╡
    │ pbs_sleep │ generic.pbs.workq │ 40.pbs  │ R          │
    ╘═══════════╧═══════════════════╧═════════╧════════════╛


    Polling Jobs in 10 seconds
    ________________________________________
    Job Queue: ['40.pbs']


    Completed Jobs
    ________________________________________


    ╒════════╤════════════╤═════════╤════════════╕
    │ name   │ executor   │ jobID   │ jobstate   │
    ╞════════╪════════════╪═════════╪════════════╡
    ╘════════╧════════════╧═════════╧════════════╛


    Pending Jobs
    ________________________________________


    ╒═══════════╤═══════════════════╤═════════╤════════════╕
    │ name      │ executor          │ jobID   │ jobstate   │
    ╞═══════════╪═══════════════════╪═════════╪════════════╡
    │ pbs_sleep │ generic.pbs.workq │ 40.pbs  │ F          │
    ╘═══════════╧═══════════════════╧═════════╧════════════╛


    Polling Jobs in 10 seconds
    ________________________________________
    Job Queue: []


    Completed Jobs
    ________________________________________


    ╒═══════════╤═══════════════════╤═════════╤════════════╕
    │ name      │ executor          │ jobID   │ jobstate   │
    ╞═══════════╪═══════════════════╪═════════╪════════════╡
    │ pbs_sleep │ generic.pbs.workq │ 40.pbs  │ F          │
    ╘═══════════╧═══════════════════╧═════════╧════════════╛


    Pending Jobs
    ________________________________________


    ╒════════╤════════════╤═════════╤════════════╕
    │ name   │ executor   │ jobID   │ jobstate   │
    ╞════════╪════════════╪═════════╪════════════╡
    ╘════════╧════════════╧═════════╧════════════╛

    +---------------------------------------------+
    | Stage: Final Results after Polling all Jobs |
    +---------------------------------------------+

     name      | id       | executor          | status   |   returncode | testpath
    -----------+----------+-------------------+----------+--------------+---------------------------------------------------------------------------------------------
     pbs_sleep | 2adfc3c1 | generic.pbs.workq | PASS     |            0 | /tmp/Documents/buildtest/var/tests/generic.pbs.workq/hostname/pbs_sleep/3/stage/generate.sh

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Executed 1 tests
    Passed Tests: 1/1 Percentage: 100.000%
    Failed Tests: 0/1 Percentage: 0.000%



    Writing Logfile to: /tmp/buildtest_mu285m58.log

buildtest will preserve the job record from ``qstat -x -f -F json <jobID>`` in the test report if job was complete.
If we take a look at the test result using **buildtest inspect** you will see the ``job`` section is
prepopulated from the JSON record provided by **qstat**.


.. code-block:: console
    :emphasize-lines: 22-88
    :linenos:

    [pbsuser@pbs buildtest]$ buildtest inspect id 2adfc3c1
    {
      "id": "2adfc3c1",
      "full_id": "2adfc3c1-1c81-43d0-a151-6fa1a9818eb4",
      "testroot": "/tmp/Documents/buildtest/var/tests/generic.pbs.workq/hostname/pbs_sleep/3",
      "testpath": "/tmp/Documents/buildtest/var/tests/generic.pbs.workq/hostname/pbs_sleep/3/stage/generate.sh",
      "stagedir": "/tmp/Documents/buildtest/var/tests/generic.pbs.workq/hostname/pbs_sleep/3/stage",
      "rundir": "/tmp/Documents/buildtest/var/tests/generic.pbs.workq/hostname/pbs_sleep/3/run",
      "command": "qsub -q workq /tmp/Documents/buildtest/var/tests/generic.pbs.workq/hostname/pbs_sleep/3/stage/generate.sh",
      "outfile": "/tmp/Documents/buildtest/var/tests/generic.pbs.workq/hostname/pbs_sleep/3/stage/pbs_sleep.o40",
      "errfile": "/tmp/Documents/buildtest/var/tests/generic.pbs.workq/hostname/pbs_sleep/3/stage/pbs_sleep.e40",
      "schemafile": "script-v1.0.schema.json",
      "executor": "generic.pbs.workq",
      "tags": "",
      "starttime": "Wed Mar 17 20:36:48 2021",
      "endtime": "Wed Mar 17 20:36:48 2021",
      "runtime": "00:00:10",
      "state": "PASS",
      "returncode": 0,
      "output": "",
      "error": "",
      "job": {
        "timestamp": 1616013438,
        "pbs_version": "19.0.0",
        "pbs_server": "pbs",
        "Jobs": {
          "40.pbs": {
            "Job_Name": "pbs_sleep",
            "Job_Owner": "pbsuser@pbs",
            "resources_used": {
              "cpupercent": 0,
              "cput": "00:00:00",
              "mem": "5620kb",
              "ncpus": 1,
              "vmem": "25632kb",
              "walltime": "00:00:10"
            },
            "job_state": "F",
            "queue": "workq",
            "server": "pbs",
            "Checkpoint": "u",
            "ctime": "Wed Mar 17 20:36:48 2021",
            "Error_Path": "pbs:/tmp/Documents/buildtest/var/tests/generic.pbs.workq/hostname/pbs_sleep/3/stage/pbs_sleep.e40",
            "exec_host": "pbs/0",
            "exec_vnode": "(pbs:ncpus=1)",
            "Hold_Types": "n",
            "Join_Path": "n",
            "Keep_Files": "n",
            "Mail_Points": "a",
            "mtime": "Wed Mar 17 20:36:58 2021",
            "Output_Path": "pbs:/tmp/Documents/buildtest/var/tests/generic.pbs.workq/hostname/pbs_sleep/3/stage/pbs_sleep.o40",
            "Priority": 0,
            "qtime": "Wed Mar 17 20:36:48 2021",
            "Rerunable": "True",
            "Resource_List": {
              "ncpus": 1,
              "nodect": 1,
              "nodes": 1,
              "place": "scatter",
              "select": "1:ncpus=1",
              "walltime": "00:02:00"
            },
            "stime": "Wed Mar 17 20:36:48 2021",
            "session_id": 7154,
            "jobdir": "/home/pbsuser",
            "substate": 92,
            "Variable_List": {
              "PBS_O_HOME": "/home/pbsuser",
              "PBS_O_LANG": "en_US.utf8",
              "PBS_O_LOGNAME": "pbsuser",
              "PBS_O_PATH": "/tmp/Documents/buildtest/bin:/tmp/Documents/github/buildtest/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/opt/pbs/bin:/home/pbsuser/.local/bin:/home/pbsuser/bin",
              "PBS_O_MAIL": "/var/spool/mail/pbsuser",
              "PBS_O_SHELL": "/bin/bash",
              "PBS_O_WORKDIR": "/tmp/Documents/buildtest/var/tests/generic.pbs.workq/hostname/pbs_sleep/3/stage",
              "PBS_O_SYSTEM": "Linux",
              "PBS_O_QUEUE": "workq",
              "PBS_O_HOST": "pbs"
            },
            "comment": "Job run at Wed Mar 17 at 20:36 on (pbs:ncpus=1) and finished",
            "etime": "Wed Mar 17 20:36:48 2021",
            "run_count": 1,
            "Stageout_status": 1,
            "Exit_status": 0,
            "Submit_arguments": "-q workq /tmp/Documents/buildtest/var/tests/generic.pbs.workq/hostname/pbs_sleep/3/stage/generate.sh",
            "history_timestamp": 1616013418,
            "project": "_pbs_project_default"
          }
        }
      }
    }



    Output File
    ______________________________




    Error File
    ______________________________




    Test Content
    ______________________________
    #!/bin/bash
    #PBS -l nodes=1
    #PBS -l walltime=00:02:00
    #PBS -N pbs_sleep
    source /tmp/Documents/buildtest/var/executors/generic.pbs.workq/before_script.sh
    sleep 10
    source /tmp/Documents/buildtest/var/executors/generic.pbs.workq/after_script.sh



    buildspec:  /tmp/Documents/buildtest/general_tests/sched/pbs/hostname.yml
    ______________________________
    version: "1.0"
    buildspecs:
      pbs_sleep:
        type: script
        executor: generic.pbs.workq
        pbs: ["-l nodes=1", "-l walltime=00:02:00"]
        run: sleep 10

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


Let's run this test and notice the job states.

.. code-block:: console

    $ buildtest build -b yarrow_hostname.yml

    +-------------------------------+
    | Stage: Discovering Buildspecs |
    +-------------------------------+


    Discovered Buildspecs:

    /home/shahzebsiddiqui/jlse_tests/yarrow_hostname.yml

    +---------------------------+
    | Stage: Parsing Buildspecs |
    +---------------------------+

     schemafile              | validstate   | buildspec
    -------------------------+--------------+------------------------------------------------------
     script-v1.0.schema.json | True         | /home/shahzebsiddiqui/jlse_tests/yarrow_hostname.yml

    +----------------------+
    | Stage: Building Test |
    +----------------------+

     name            | id       | type   | executor      | tags   | testpath
    -----------------+----------+--------+---------------+--------+-------------------------------------------------------------------------------------------------------------
     yarrow_hostname | f86b93f6 | script | cobalt.yarrow |        | /home/shahzebsiddiqui/buildtest/var/tests/cobalt.yarrow/yarrow_hostname/yarrow_hostname/3/stage/generate.sh

    +----------------------+
    | Stage: Running Test  |
    +----------------------+

    [yarrow_hostname] JobID: 284752 dispatched to scheduler
     name            | id       | executor      | status   |   returncode | testpath
    -----------------+----------+---------------+----------+--------------+-------------------------------------------------------------------------------------------------------------
     yarrow_hostname | f86b93f6 | cobalt.yarrow | N/A      |           -1 | /home/shahzebsiddiqui/buildtest/var/tests/cobalt.yarrow/yarrow_hostname/yarrow_hostname/3/stage/generate.sh


    Polling Jobs in 10 seconds
    ________________________________________
    builder: yarrow_hostname in None
    [yarrow_hostname]: JobID 284752 in starting state


    Polling Jobs in 10 seconds
    ________________________________________
    builder: yarrow_hostname in starting
    [yarrow_hostname]: JobID 284752 in starting state


    Polling Jobs in 10 seconds
    ________________________________________
    builder: yarrow_hostname in starting
    [yarrow_hostname]: JobID 284752 in running state


    Polling Jobs in 10 seconds
    ________________________________________
    builder: yarrow_hostname in running
    [yarrow_hostname]: JobID 284752 in exiting state


    Polling Jobs in 10 seconds
    ________________________________________
    builder: yarrow_hostname in done

    +---------------------------------------------+
    | Stage: Final Results after Polling all Jobs |
    +---------------------------------------------+

     name            | id       | executor      | status   |   returncode | testpath
    -----------------+----------+---------------+----------+--------------+-------------------------------------------------------------------------------------------------------------
     yarrow_hostname | f86b93f6 | cobalt.yarrow | PASS     |          0   | /home/shahzebsiddiqui/buildtest/var/tests/cobalt.yarrow/yarrow_hostname/yarrow_hostname/3/stage/generate.sh

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Executed 1 tests
    Passed Tests: 1/1 Percentage: 100.000%
    Failed Tests: 0/1 Percentage: 0.000%

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

qstat has no job record for capturing returncode so buildtest must rely on Cobalt Log file.:

.. _max_pend_time:

Jobs exceeds `max_pend_time`
-----------------------------

Recall from :ref:`configuring_buildtest` that `max_pend_time` will cancel jobs if
job exceed timelimit. buildtest will start a timer for each job right after job
submission and keep track of time duration, and if job is in **pending** state and it exceeds `max_pend_time`,
then job will be cancelled.

We can also override `max_pend_time` configuration via command line ``--max-pend-time``.
To demonstrate, here is an example where job  was cancelled after job was pending and exceeds `max_pend_time`.
Note that cancelled job is not reported in final output nor updated in report hence
it won't be present in the report (``buildtest report``). In this example, we only
had one test so upon job cancellation we found there was no tests to report hence,
buildtest will terminate after run stage.

.. code-block:: console
    :emphasize-lines: 124
    :linenos:

    $ buildtest build -b buildspecs/queues/shared.yml --max-pend-time 15 --poll-interval 5 -k


    User:  siddiq90
    Hostname:  cori08
    Platform:  Linux
    Current Time:  2021/06/11 13:31:46
    buildtest path: /global/homes/s/siddiq90/github/buildtest/bin/buildtest
    buildtest version:  0.9.5
    python path: /global/homes/s/siddiq90/.conda/envs/buildtest/bin/python
    python version:  3.8.8
    Test Directory:  /global/u1/s/siddiq90/github/buildtest/var/tests
    Configuration File:  /global/u1/s/siddiq90/.buildtest/config.yml
    Command: /global/homes/s/siddiq90/github/buildtest/bin/buildtest build -b buildspecs/queues/shared.yml --max-pend-time 15 --poll-interval 5 -k

    +-------------------------------+
    | Stage: Discovering Buildspecs |
    +-------------------------------+

    +--------------------------------------------------------------------------+
    | Discovered Buildspecs                                                    |
    +==========================================================================+
    | /global/u1/s/siddiq90/github/buildtest-cori/buildspecs/queues/shared.yml |
    +--------------------------------------------------------------------------+
    Discovered Buildspecs:  1
    Excluded Buildspecs:  0
    Detected Buildspecs after exclusion:  1

    +---------------------------+
    | Stage: Parsing Buildspecs |
    +---------------------------+

     schemafile              | validstate   | buildspec
    -------------------------+--------------+--------------------------------------------------------------------------
     script-v1.0.schema.json | True         | /global/u1/s/siddiq90/github/buildtest-cori/buildspecs/queues/shared.yml



    name                         description
    ---------------------------  ------------------------------------------
    shared_qos_haswell_hostname  run hostname through shared qos on Haswell

    +----------------------+
    | Stage: Building Test |
    +----------------------+

     name                        | id       | type   | executor                  | tags                          | testpath
    -----------------------------+----------+--------+---------------------------+-------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------
     shared_qos_haswell_hostname | 94b2de5d | script | cori.slurm.haswell_shared | ['queues', 'jobs', 'reframe'] | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.haswell_shared/shared/shared_qos_haswell_hostname/2/shared_qos_haswell_hostname_build.sh



    +---------------------+
    | Stage: Running Test |
    +---------------------+

    [shared_qos_haswell_hostname] JobID: 43313766 dispatched to scheduler
     name                        | id       | executor                  | status   |   returncode
    -----------------------------+----------+---------------------------+----------+--------------
     shared_qos_haswell_hostname | 94b2de5d | cori.slurm.haswell_shared | N/A      |           -1


    Polling Jobs in 5 seconds
    ________________________________________
    Job Queue: [43313766]


    Pending Jobs
    ________________________________________


    +-----------------------------+---------------------------+----------+----------+
    |            name             |         executor          |  jobID   | jobstate |
    +-----------------------------+---------------------------+----------+----------+
    | shared_qos_haswell_hostname | cori.slurm.haswell_shared | 43313766 | PENDING  |
    +-----------------------------+---------------------------+----------+----------+


    Polling Jobs in 5 seconds
    ________________________________________
    Job Queue: [43313766]


    Pending Jobs
    ________________________________________


    +-----------------------------+---------------------------+----------+----------+
    |            name             |         executor          |  jobID   | jobstate |
    +-----------------------------+---------------------------+----------+----------+
    | shared_qos_haswell_hostname | cori.slurm.haswell_shared | 43313766 | PENDING  |
    +-----------------------------+---------------------------+----------+----------+


    Polling Jobs in 5 seconds
    ________________________________________
    Job Queue: [43313766]


    Pending Jobs
    ________________________________________


    +-----------------------------+---------------------------+----------+----------+
    |            name             |         executor          |  jobID   | jobstate |
    +-----------------------------+---------------------------+----------+----------+
    | shared_qos_haswell_hostname | cori.slurm.haswell_shared | 43313766 | PENDING  |
    +-----------------------------+---------------------------+----------+----------+


    Polling Jobs in 5 seconds
    ________________________________________
    Cancelling Job because duration time: 21.177340 sec exceeds max pend time: 15 sec
    Job Queue: [43313766]


    Pending Jobs
    ________________________________________


    +-----------------------------+---------------------------+----------+-----------+
    |            name             |         executor          |  jobID   | jobstate  |
    +-----------------------------+---------------------------+----------+-----------+
    | shared_qos_haswell_hostname | cori.slurm.haswell_shared | 43313766 | CANCELLED |
    +-----------------------------+---------------------------+----------+-----------+


    Polling Jobs in 5 seconds
    ________________________________________
    Job Queue: []
    Cancelled Tests:
    shared_qos_haswell_hostname
    After polling all jobs we found no valid builders to process

.. _cray_burstbuffer_datawarp:

Cray Burst Buffer & Data Warp
-------------------------------

For Cray systems, you may want to stage-in or stage-out into your burst buffer this
can be configured using the ``#DW`` directive. For a list of data warp examples see
section on `DataWarp Job Script Commands <https://pubs.cray.com/bundle/XC_Series_DataWarp_User_Guide_CLE60UP01_S-2558_include_only_UP01/page/DataWarp_Job_Script_Commands.html>`_

In buildtest we support properties ``BB`` and ``DW`` which is a list of job directives
that get inserted as **#BW** and **#DW** into the test script. To demonstrate let's start
off with an example where we create a persistent burst buffer named ``databuffer`` of size
10GB striped. We access the burst buffer using the `DW` directive. Finally we
cd into the databuffer and write a 5GB random file.

.. Note:: BB and DW directives are generated after scheduler directives. The ``#BB``
   comes before ``#DW``. buildtest will automatically add the directive **#BB**
   and **#DW** when using properties BB and DW

.. code-block:: yaml
    :emphasize-lines: 13-16
    :linenos:

    version: "1.0"
    buildspecs:
      create_burst_buffer:
        type: script
        executor: cori.slurm.debug
        batch:
          nodecount: "1"
          timelimit: "5"
          cpucount: "1"
        sbatch: ["-C knl"]
        description: Create a burst buffer
        tags: [jobs]
        BB:
          - create_persistent name=databuffer capacity=10GB access_mode=striped type=scratch
        DW:
          - persistentdw name=databuffer
        run: |
          cd $DW_PERSISTENT_STRIPED_databuffer
          pwd
          dd if=/dev/urandom of=random.txt bs=1G count=5 iflags=fullblock
          ls -lh $DW_PERSISTENT_STRIPED_databuffer/

Next we run this test and inspect the generated test we will see that ``#BB`` and ``#DW`` directives
are inserted after the scheduler directives

.. code-block:: shell
    :emphasize-lines: 8-9

    #!/bin/bash
    #SBATCH --nodes=1
    #SBATCH --time=5
    #SBATCH --ntasks=1
    #SBATCH --job-name=create_burst_buffer
    #SBATCH --output=create_burst_buffer.out
    #SBATCH --error=create_burst_buffer.err
    #BB create_persistent name=databuffer capacity=10GB access_mode=striped type=scratch
    #DW persistentdw name=databuffer
    cd $DW_PERSISTENT_STRIPED_databuffer
    pwd
    dd if=/dev/urandom of=random.txt bs=1G count=5 iflag=fullblock
    ls -lh $DW_PERSISTENT_STRIPED_databuffer


We can confirm their is an active burst buffer by running the following

.. code-block:: console

    $ scontrol show burst | grep databuffer
        Name=databuffer CreateTime=2020-10-29T13:06:21 Pool=wlm_pool Size=20624MiB State=allocated UserID=siddiq90(92503)
