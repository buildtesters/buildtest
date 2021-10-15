Advanced Section
=================

Single Test Multiple Compilers
-------------------------------

It's possible to run single test across multiple compilers (gcc, intel, cray, etc...). In the
next example, we will build an OpenMP reduction test using gcc, intel and cray compilers. In this
test, we use ``name`` field to select compilers that start with **gcc**, **intel** and **PrgEnv-cray**
as compiler names. The ``default`` section is organized by compiler groups which inherits compiler flags
for all compilers. OpenMP flag for gcc, intel and cray differ for instance one must use ``-fopenmp`` for gcc,
``--qopenmp`` for intel and ``-h omp`` for cray.

.. code-block:: yaml
   :linenos:
   :emphasize-lines: 10-20

    version: "1.0"
    buildspecs:
      reduction:
        type: compiler
        executor: local.bash
        source: src/reduction.c
        description: OpenMP reduction example using gcc, intel and cray compiler
        tags: [openmp]
        compilers:
          name: ["^(gcc|intel|PrgEnv-cray)"]
          default:
            all:
              env:
                OMP_NUM_THREADS: 4
            gcc:
              cflags: -fopenmp
            intel:
              cflags: -qopenmp
            cray:
              cflags: -h omp

In this example `OMP_NUM_THREADS` environment variable under the ``all`` section which
will be used for all compiler groups. This example was built on Cori, we expect this
test to run against every gcc, intel and PrgEnv-cray compiler module:

.. code-block:: console

    $ buildtest build -b buildspecs/apps/openmp/reduction.yml


    User:  siddiq90
    Hostname:  cori02
    Platform:  Linux
    Current Time:  2021/06/11 08:42:54
    buildtest path: /global/homes/s/siddiq90/github/buildtest/bin/buildtest
    buildtest version:  0.9.5
    python path: /global/homes/s/siddiq90/.conda/envs/buildtest/bin/python
    python version:  3.8.8
    Test Directory:  /global/u1/s/siddiq90/github/buildtest/var/tests
    Configuration File:  /global/u1/s/siddiq90/.buildtest/config.yml
    Command: /global/homes/s/siddiq90/github/buildtest/bin/buildtest build -b buildspecs/apps/openmp/reduction.yml

    +-------------------------------+
    | Stage: Discovering Buildspecs |
    +-------------------------------+

    +----------------------------------------------------------------------------------+
    | Discovered Buildspecs                                                            |
    +==================================================================================+
    | /global/u1/s/siddiq90/github/buildtest-cori/buildspecs/apps/openmp/reduction.yml |
    +----------------------------------------------------------------------------------+
    Discovered Buildspecs:  1
    Excluded Buildspecs:  0
    Detected Buildspecs after exclusion:  1

    +---------------------------+
    | Stage: Parsing Buildspecs |
    +---------------------------+

     schemafile                | validstate   | buildspec
    ---------------------------+--------------+----------------------------------------------------------------------------------
     compiler-v1.0.schema.json | True         | /global/u1/s/siddiq90/github/buildtest-cori/buildspecs/apps/openmp/reduction.yml



    name       description
    ---------  ---------------------------------------------------------------
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler

    +----------------------+
    | Stage: Building Test |
    +----------------------+



     name      | id       | type     | executor        | tags       | compiler                                | testpath
    -----------+----------+----------+-----------------+------------+-----------------------------------------+------------------------------------------------------------------------------------------------------------
     reduction | fd93fdcb | compiler | cori.local.bash | ['openmp'] | gcc/6.1.0                               | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/25/reduction_build.sh
     reduction | 43737191 | compiler | cori.local.bash | ['openmp'] | gcc/7.3.0                               | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/26/reduction_build.sh
     reduction | 6e2e95cd | compiler | cori.local.bash | ['openmp'] | gcc/8.1.0                               | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/27/reduction_build.sh
     reduction | c48a8d8d | compiler | cori.local.bash | ['openmp'] | gcc/8.2.0                               | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/28/reduction_build.sh
     reduction | a6201c48 | compiler | cori.local.bash | ['openmp'] | gcc/8.3.0                               | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/29/reduction_build.sh
     reduction | aa06b1be | compiler | cori.local.bash | ['openmp'] | gcc/9.3.0                               | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/30/reduction_build.sh
     reduction | 02b8e7aa | compiler | cori.local.bash | ['openmp'] | gcc/10.1.0                              | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/31/reduction_build.sh
     reduction | bd9abd7e | compiler | cori.local.bash | ['openmp'] | gcc/6.3.0                               | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/32/reduction_build.sh
     reduction | 9409a86f | compiler | cori.local.bash | ['openmp'] | gcc/8.1.1-openacc-gcc-8-branch-20190215 | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/33/reduction_build.sh
     reduction | b9700a0f | compiler | cori.local.bash | ['openmp'] | PrgEnv-cray/6.0.5                       | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/34/reduction_build.sh
     reduction | a605c970 | compiler | cori.local.bash | ['openmp'] | PrgEnv-cray/6.0.7                       | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/35/reduction_build.sh
     reduction | 9ef915a9 | compiler | cori.local.bash | ['openmp'] | PrgEnv-cray/6.0.9                       | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/36/reduction_build.sh
     reduction | 4f9e4242 | compiler | cori.local.bash | ['openmp'] | intel/19.0.3.199                        | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/37/reduction_build.sh
     reduction | e37befed | compiler | cori.local.bash | ['openmp'] | intel/19.1.2.254                        | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/38/reduction_build.sh
     reduction | 1e9b0ab5 | compiler | cori.local.bash | ['openmp'] | intel/16.0.3.210                        | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/39/reduction_build.sh
     reduction | 4e6d6f8a | compiler | cori.local.bash | ['openmp'] | intel/17.0.1.132                        | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/40/reduction_build.sh
     reduction | ad1e44af | compiler | cori.local.bash | ['openmp'] | intel/17.0.2.174                        | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/41/reduction_build.sh
     reduction | 49acf44b | compiler | cori.local.bash | ['openmp'] | intel/18.0.1.163                        | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/42/reduction_build.sh
     reduction | 4192750c | compiler | cori.local.bash | ['openmp'] | intel/18.0.3.222                        | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/43/reduction_build.sh
     reduction | 06584529 | compiler | cori.local.bash | ['openmp'] | intel/19.0.0.117                        | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/44/reduction_build.sh
     reduction | 82fd9bab | compiler | cori.local.bash | ['openmp'] | intel/19.0.8.324                        | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/45/reduction_build.sh
     reduction | 6140e8b4 | compiler | cori.local.bash | ['openmp'] | intel/19.1.0.166                        | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/46/reduction_build.sh
     reduction | ac509e2e | compiler | cori.local.bash | ['openmp'] | intel/19.1.1.217                        | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/47/reduction_build.sh
     reduction | 9c39818e | compiler | cori.local.bash | ['openmp'] | intel/19.1.2.275                        | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/48/reduction_build.sh
     reduction | 2cb3acd1 | compiler | cori.local.bash | ['openmp'] | intel/19.1.3.304                        | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/49/reduction_build.sh

    +---------------------+
    | Stage: Running Test |
    +---------------------+

     name      | id       | executor        | status   |   returncode
    -----------+----------+-----------------+----------+--------------
     reduction | fd93fdcb | cori.local.bash | PASS     |            0
     reduction | 43737191 | cori.local.bash | PASS     |            0
     reduction | 6e2e95cd | cori.local.bash | PASS     |            0
     reduction | c48a8d8d | cori.local.bash | PASS     |            0
     reduction | a6201c48 | cori.local.bash | PASS     |            0
     reduction | aa06b1be | cori.local.bash | PASS     |            0
     reduction | 02b8e7aa | cori.local.bash | PASS     |            0
     reduction | bd9abd7e | cori.local.bash | PASS     |            0
     reduction | 9409a86f | cori.local.bash | PASS     |            0
     reduction | b9700a0f | cori.local.bash | PASS     |            0
     reduction | a605c970 | cori.local.bash | PASS     |            0
     reduction | 9ef915a9 | cori.local.bash | PASS     |            0
     reduction | 4f9e4242 | cori.local.bash | PASS     |            0
     reduction | e37befed | cori.local.bash | PASS     |            0
     reduction | 1e9b0ab5 | cori.local.bash | PASS     |            0
     reduction | 4e6d6f8a | cori.local.bash | PASS     |            0
     reduction | ad1e44af | cori.local.bash | PASS     |            0
     reduction | 49acf44b | cori.local.bash | PASS     |            0
     reduction | 4192750c | cori.local.bash | PASS     |            0
     reduction | 06584529 | cori.local.bash | PASS     |            0
     reduction | 82fd9bab | cori.local.bash | PASS     |            0
     reduction | 6140e8b4 | cori.local.bash | PASS     |            0
     reduction | ac509e2e | cori.local.bash | PASS     |            0
     reduction | 9c39818e | cori.local.bash | PASS     |            0
     reduction | 2cb3acd1 | cori.local.bash | PASS     |            0

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Passed Tests: 25/25 Percentage: 100.000%
    Failed Tests: 0/25 Percentage: 0.000%


    Writing Logfile to: /tmp/buildtest_sq87154s.log
    A copy of logfile can be found at $BUILDTEST_ROOT/buildtest.log -  /global/homes/s/siddiq90/github/buildtest/buildtest.log

MPI Example
------------

In this example we run a MPI Laplace code using 4 process on a KNL node using
the ``intel/19.1.2.254`` compiler. This test is run on Cori through batch queue
system. We can define **#SBATCH** parameters using ``sbatch`` property. This program
is compiled using ``mpiicc`` wrapper this can be defined using ``cc`` parameter.

Currently, buildtest cannot detect if program is serial or MPI to infer appropriate
compiler wrapper. If ``cc`` wasn't specified, buildtest would infer `icc` as compiler
wrapper for C program. This program is run using ``srun`` job launcher, we can control
how test is executed using the ``run`` property. This test required we swap intel
modules and load `impi/2020` module.

.. code-block:: yaml
    :linenos:
    :emphasize-lines: 13,16,18-22

    version: "1.0"
    buildspecs:
      laplace_mpi:
        type: compiler
        description: Laplace MPI code in C
        executor: slurm.knl_debug
        tags: ["mpi"]
        source: src/laplace_mpi.c
        compilers:
          name: ["^(intel/19.1.2.254)$"]
          default:
            all:
              sbatch: ["-N 1", "-n 4"]
              run: srun -n 4 $_EXEC
            intel:
              cc: mpiicc
              cflags: -O3
          config:
            intel/19.1.2.254:
              module:
                load: [impi/2020]
                swap: [intel, intel/19.1.2.254]

Shown below is a sample build for this buildspec, buildtest will dispatch and poll
job until its complete.

.. code-block:: console

    $ buildtest build -b buildspecs/apps/mpi/laplace_mpi.yml


    User:  siddiq90
    Hostname:  cori02
    Platform:  Linux
    Current Time:  2021/06/11 09:11:16
    buildtest path: /global/homes/s/siddiq90/github/buildtest/bin/buildtest
    buildtest version:  0.9.5
    python path: /global/homes/s/siddiq90/.conda/envs/buildtest/bin/python
    python version:  3.8.8
    Test Directory:  /global/u1/s/siddiq90/github/buildtest/var/tests
    Configuration File:  /global/u1/s/siddiq90/.buildtest/config.yml
    Command: /global/homes/s/siddiq90/github/buildtest/bin/buildtest build -b buildspecs/apps/mpi/laplace_mpi.yml

    +-------------------------------+
    | Stage: Discovering Buildspecs |
    +-------------------------------+

    +---------------------------------------------------------------------------------+
    | Discovered Buildspecs                                                           |
    +=================================================================================+
    | /global/u1/s/siddiq90/github/buildtest-cori/buildspecs/apps/mpi/laplace_mpi.yml |
    +---------------------------------------------------------------------------------+
    Discovered Buildspecs:  1
    Excluded Buildspecs:  0
    Detected Buildspecs after exclusion:  1

    +---------------------------+
    | Stage: Parsing Buildspecs |
    +---------------------------+

     schemafile                | validstate   | buildspec
    ---------------------------+--------------+---------------------------------------------------------------------------------
     compiler-v1.0.schema.json | True         | /global/u1/s/siddiq90/github/buildtest-cori/buildspecs/apps/mpi/laplace_mpi.yml



    name         description
    -----------  ---------------------
    laplace_mpi  Laplace MPI code in C

    +----------------------+
    | Stage: Building Test |
    +----------------------+



     name        | id       | type     | executor             | tags    | compiler         | testpath
    -------------+----------+----------+----------------------+---------+------------------+----------------------------------------------------------------------------------------------------------------------
     laplace_mpi | a6087b86 | compiler | cori.slurm.knl_debug | ['mpi'] | intel/19.1.2.254 | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/laplace_mpi/laplace_mpi/0/laplace_mpi_build.sh

    +---------------------+
    | Stage: Running Test |
    +---------------------+

    [laplace_mpi] JobID: 43308598 dispatched to scheduler
     name        | id       | executor             | status   |   returncode
    -------------+----------+----------------------+----------+--------------
     laplace_mpi | a6087b86 | cori.slurm.knl_debug | N/A      |           -1


    Polling Jobs in 30 seconds
    ________________________________________
    Job Queue: [43308598]


    Pending Jobs
    ________________________________________


    +-------------+----------------------+----------+-----------+
    |    name     |       executor       |  jobID   | jobstate  |
    +-------------+----------------------+----------+-----------+
    | laplace_mpi | cori.slurm.knl_debug | 43308598 | COMPLETED |
    +-------------+----------------------+----------+-----------+


    Polling Jobs in 30 seconds
    ________________________________________
    Job Queue: []


    Completed Jobs
    ________________________________________


    +-------------+----------------------+----------+-----------+
    |    name     |       executor       |  jobID   | jobstate  |
    +-------------+----------------------+----------+-----------+
    | laplace_mpi | cori.slurm.knl_debug | 43308598 | COMPLETED |
    +-------------+----------------------+----------+-----------+

    +---------------------------------------------+
    | Stage: Final Results after Polling all Jobs |
    +---------------------------------------------+

     name        | id       | executor             | status   |   returncode
    -------------+----------+----------------------+----------+--------------
     laplace_mpi | a6087b86 | cori.slurm.knl_debug | PASS     |            0

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Passed Tests: 1/1 Percentage: 100.000%
    Failed Tests: 0/1 Percentage: 0.000%


    Writing Logfile to: /tmp/buildtest_wgptyp8v.log
    A copy of logfile can be found at $BUILDTEST_ROOT/buildtest.log -  /global/homes/s/siddiq90/github/buildtest/buildtest.log

The generated test is as follows, note that buildtest will insert the #SBATCH directives at the top of script, and ``module load``
are done before ``module swap`` command.

.. code-block:: shell
    :linenos:
    :emphasize-lines: 2-3, 8-10

    #!/bin/bash
    #SBATCH -N 1
    #SBATCH -n 4
    #SBATCH --job-name=laplace_mpi
    #SBATCH --output=laplace_mpi.out
    #SBATCH --error=laplace_mpi.err
    _EXEC=laplace_mpi.c.exe
    module load impi/2020
    module swap intel intel/19.1.2.254
    mpiicc -O3 -o $_EXEC /global/u1/s/siddiq90/github/buildtest-cori/buildspecs/apps/mpi/src/laplace_mpi.c
    srun -n 4 $_EXEC

The master script that buildtest will invoke is the following, notice that our generated script (shown above) is invoked via `sbatch` with its
options. The options ``sbatch -q debug --clusters=cori -C knl,quad,cache`` was inserted by our executor configuration. We add the ``--parsable``
option for Slurm jobs in order to get the JobID when this script is invoked so that buildtest can poll the job.

.. code-block:: shell
    :linenos:
    :emphasize-lines: 3

    #!/bin/bash
    source /global/u1/s/siddiq90/github/buildtest/var/executor/cori.slurm.knl_debug/before_script.sh
    sbatch --parsable -q debug --clusters=cori -C knl,quad,cache /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/laplace_mpi/laplace_mpi/0/stage/laplace_mpi.sh
    returncode=$?
    exit $returncode
