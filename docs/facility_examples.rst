Facility Test Examples
========================

We will discuss a few test examples implemented at NERSC that are available at https://github.com/buildtesters/buildtest-cori/.

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
   :emphasize-lines: 9-19

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
test to run against every gcc, intel and PrgEnv-cray compiler module.

MPI Example
------------

In this example we run a MPI Laplace code using 4 process on a KNL node using
the ``intel/19.1.2.254`` compiler. This test is run on Cori through batch queue
system. We can define **#SBATCH** parameters using ``sbatch`` property. This program
is compiled using ``mpiicc`` wrapper that can be defined using ``cc`` parameter.


buildtest would infer `icc` as compiler wrapper however since this is a MPI program we must specify `mpiicc` as the compiler wrapper to compile this MPI C program.
It's worth noting buildtest will detect the compiler wrapper under the compiler group defined under `default` such as `intel`, `gnu`, etc... since `cc` property is
a property of ``intel`` this will inform buildtest to use the Intel provided wrappers.

This program is run using ``srun`` job launcher, we can control
how test is executed using the ``run`` property. This test required we swap intel
modules and load `impi/2020` module.

.. code-block:: yaml
    :linenos:
    :emphasize-lines: 12,15,17-21

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

The generated test script is show below, notice that ``mpicc`` is used to compile the program and run via srun.

.. code-block:: shell

    (buildtest) siddiq90@cori05> buildtest inspect query -t laplace_mpi
    ───────────────────────────────────────────────────────────────────── laplace_mpi/6752ca70-c808-4ee2-96df-0fccce4f7bfc ──────────────────────────────────────────────────────────────────────
    Executor: cori.slurm.knl_debug
    Description: Laplace MPI code in C
    State: PASS
    Returncode: 0
    Runtime: 153.396612 sec
    Starttime: 2022/01/11 07:01:52
    Endtime: 2022/01/11 07:04:25
    Command: bash --norc --noprofile -eo pipefail laplace_mpi_build.sh
    Test Script: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/laplace_mpi/laplace_mpi/6752ca70/laplace_mpi.sh
    Build Script: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/laplace_mpi/laplace_mpi/6752ca70/laplace_mpi_build.sh
    Output File: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/laplace_mpi/laplace_mpi/6752ca70/laplace_mpi.out
    Error File: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/laplace_mpi/laplace_mpi/6752ca70/laplace_mpi.err
    Log File: /global/u1/s/siddiq90/github/buildtest/var/logs/buildtest_hs5i33eb.log
    ───────────────────────────── Test File: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/laplace_mpi/laplace_mpi/6752ca70/laplace_mpi.sh ──────────────────────────────
       1 #!/bin/bash
       2 ####### START OF SCHEDULER DIRECTIVES #######
       3 #SBATCH -N 1
       4 #SBATCH -n 4
       5 #SBATCH --job-name=laplace_mpi
       6 #SBATCH --output=laplace_mpi.out
       7 #SBATCH --error=laplace_mpi.err
       8 ####### END OF SCHEDULER DIRECTIVES   #######
       9
      10
      11 # name of executable
      12 _EXEC=laplace_mpi.c.exe
      13 # Loading modules
      14 module swap intel intel/19.1.2.254
      15 module load impi/2020
      16 # Compilation Line
      17 mpiicc -O3 -o $_EXEC /global/u1/s/siddiq90/github/buildtest-cori/buildspecs/apps/mpi/src/laplace_mpi.c
      18
      19
      20 # Run executable
      21 srun -n 4 $_EXEC
      22
      23

OpenMP Hello Processor Scaling Test
-------------------------------------

In this example we have a OpenMP test that will be run across a set of processes. We define environment ``OMP_NUM_THREADS`` variable that will
take value of ``BUILDTEST_NUMPROCS`` which is set when using ``buildtest build --procs``. Our compiler of choice is ``PrgEnv-intel``,
the job will run via slurm scheduler. To compile OpenMP code for intel we use ``-qopenmp`` flag.
Shown below is the source code and buildspec for this test.

.. code-block:: c


    // OpenMP program to print Hello World
    // using C language

    // OpenMP header
    #include <omp.h>

    #include <stdio.h>
    #include <stdlib.h>

    int main(int argc, char* argv[])
    {

        // Beginning of parallel region
        #pragma omp parallel
        {

            printf("Hello World... from thread = %d\n",
                   omp_get_thread_num());
        }
        // Ending of parallel region
    }

.. code-block:: yaml

    buildspecs:
      hello_world_openmp:
        type: compiler
        executor: cori.slurm.knl_debug
        source: src/hello.c
        description: Hello World OpenMP scaling example with processor count
        tags: [openmp]
        compilers:
          name: ["^PrgEnv-intel/6.0.5"]
          default:
            intel:
              env:
                OMP_NUM_THREADS: "$BUILDTEST_NUMPROCS"
              cflags: -qopenmp
              sbatch: ["-t 10"]


Next, we will run this test with 8, 16, and 24 processes. buildtest will create three builder objects for these test and each will run through slurm
scheduler. The values will be set for ``OMP_NUM_THREADS``. Shown below is the test execution

.. code-block:: console

    (buildtest) siddiq90@cori03> buildtest bd -b buildspecs/apps/openmp/openmp_scale.yml --procs 8 16 24
    ╭──────────────────────────────────────────────────────────── buildtest summary ────────────────────────────────────────────────────────────╮
    │                                                                                                                                           │
    │ User:               siddiq90                                                                                                              │
    │ Hostname:           cori03                                                                                                                │
    │ Platform:           Linux                                                                                                                 │
    │ Current Time:       2022/01/14 08:30:52                                                                                                   │
    │ buildtest path:     /global/homes/s/siddiq90/github/buildtest/bin/buildtest                                                               │
    │ buildtest version:  0.12.0                                                                                                                │
    │ python path:        /usr/common/software/python/3.8-anaconda-2020.11/bin/python3                                                          │
    │ python version:     3.8.5                                                                                                                 │
    │ Configuration File: /global/u1/s/siddiq90/github/buildtest-cori/config.yml                                                                │
    │ Test Directory:     /global/u1/s/siddiq90/github/buildtest/var/tests                                                                      │
    │ Command:            /global/homes/s/siddiq90/github/buildtest/bin/buildtest bd -b buildspecs/apps/openmp/openmp_scale.yml --procs 8 16 24 │
    │                                                                                                                                           │
    ╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
    ──────────────────────────────────────────────────────────────────────────────────  Discovering Buildspecs ──────────────────────────────────────────────────────────────────────────────────
    Discovered Buildspecs:  1
    Excluded Buildspecs:  0
    Detected Buildspecs after exclusion:  1
                                     Discovered buildspecs
    ╔═════════════════════════════════════════════════════════════════════════════════════╗
    ║ Buildspecs                                                                          ║
    ╟─────────────────────────────────────────────────────────────────────────────────────╢
    ║ /global/u1/s/siddiq90/github/buildtest-cori/buildspecs/apps/openmp/openmp_scale.yml ║
    ╚═════════════════════════════════════════════════════════════════════════════════════╝
    ──────────────────────────────────────────────────────────────────────────────────── Parsing Buildspecs ─────────────────────────────────────────────────────────────────────────────────────
    Valid Buildspecs: 1
    Invalid Buildspecs: 0
    /global/u1/s/siddiq90/github/buildtest-cori/buildspecs/apps/openmp/openmp_scale.yml: VALID
    Total builder objects created: 3
    Total compiler builder: 3
    Total script builder: 0
    Total spack builder: 0
                                                                                      Compiler Builder Details
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Builder                     ┃ Executor             ┃ Compiler           ┃ description                                            ┃ buildspecs                                             ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ hello_world_openmp/a34fe818 │ cori.slurm.knl_debug │ PrgEnv-intel/6.0.5 │ Hello World OpenMP scaling example with processor      │ /global/u1/s/siddiq90/github/buildtest-cori/buildspecs │
    │                             │                      │                    │ count                                                  │ /apps/openmp/openmp_scale.yml                          │
    ├─────────────────────────────┼──────────────────────┼────────────────────┼────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
    │ hello_world_openmp/4c03a59d │ cori.slurm.knl_debug │ PrgEnv-intel/6.0.5 │ Hello World OpenMP scaling example with processor      │ /global/u1/s/siddiq90/github/buildtest-cori/buildspecs │
    │                             │                      │                    │ count                                                  │ /apps/openmp/openmp_scale.yml                          │
    ├─────────────────────────────┼──────────────────────┼────────────────────┼────────────────────────────────────────────────────────┼────────────────────────────────────────────────────────┤
    │ hello_world_openmp/69b3eeb1 │ cori.slurm.knl_debug │ PrgEnv-intel/6.0.5 │ Hello World OpenMP scaling example with processor      │ /global/u1/s/siddiq90/github/buildtest-cori/buildspecs │
    │                             │                      │                    │ count                                                  │ /apps/openmp/openmp_scale.yml                          │
    └─────────────────────────────┴──────────────────────┴────────────────────┴────────────────────────────────────────────────────────┴────────────────────────────────────────────────────────┘
                                                                 Batch Job Builders
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Builder                     ┃ Executor             ┃ buildspecs                                                                          ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ hello_world_openmp/a34fe818 │ cori.slurm.knl_debug │ /global/u1/s/siddiq90/github/buildtest-cori/buildspecs/apps/openmp/openmp_scale.yml │
    ├─────────────────────────────┼──────────────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
    │ hello_world_openmp/4c03a59d │ cori.slurm.knl_debug │ /global/u1/s/siddiq90/github/buildtest-cori/buildspecs/apps/openmp/openmp_scale.yml │
    ├─────────────────────────────┼──────────────────────┼─────────────────────────────────────────────────────────────────────────────────────┤
    │ hello_world_openmp/69b3eeb1 │ cori.slurm.knl_debug │ /global/u1/s/siddiq90/github/buildtest-cori/buildspecs/apps/openmp/openmp_scale.yml │
    └─────────────────────────────┴──────────────────────┴─────────────────────────────────────────────────────────────────────────────────────┘
                                                                Batch Job Builders by Processors
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Builder                     ┃ Executor             ┃ Processor ┃ buildspecs                                                                          ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ hello_world_openmp/a34fe818 │ cori.slurm.knl_debug │ 8         │ /global/u1/s/siddiq90/github/buildtest-cori/buildspecs/apps/openmp/openmp_scale.yml │
    ├─────────────────────────────┼──────────────────────┼───────────┼─────────────────────────────────────────────────────────────────────────────────────┤
    │ hello_world_openmp/4c03a59d │ cori.slurm.knl_debug │ 16        │ /global/u1/s/siddiq90/github/buildtest-cori/buildspecs/apps/openmp/openmp_scale.yml │
    ├─────────────────────────────┼──────────────────────┼───────────┼─────────────────────────────────────────────────────────────────────────────────────┤
    │ hello_world_openmp/69b3eeb1 │ cori.slurm.knl_debug │ 24        │ /global/u1/s/siddiq90/github/buildtest-cori/buildspecs/apps/openmp/openmp_scale.yml │
    └─────────────────────────────┴──────────────────────┴───────────┴─────────────────────────────────────────────────────────────────────────────────────┘
    ─────────────────────────────────────────────────────────────────────────────────────── Building Test ───────────────────────────────────────────────────────────────────────────────────────
    hello_world_openmp/a34fe818: Creating test directory: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/a34fe818
    hello_world_openmp/a34fe818: Creating the stage directory: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/a34fe818/stage
    hello_world_openmp/a34fe818: Writing build script: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/a34fe818/hello_world_openmp_build.sh
    hello_world_openmp/4c03a59d: Creating test directory: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/4c03a59d
    hello_world_openmp/4c03a59d: Creating the stage directory: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/4c03a59d/stage
    hello_world_openmp/4c03a59d: Writing build script: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/4c03a59d/hello_world_openmp_build.sh
    hello_world_openmp/69b3eeb1: Creating test directory: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/69b3eeb1
    hello_world_openmp/69b3eeb1: Creating the stage directory: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/69b3eeb1/stage
    hello_world_openmp/69b3eeb1: Writing build script: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/69b3eeb1/hello_world_openmp_build.sh
    ─────────────────────────────────────────────────────────────────────────────────────── Running Tests ───────────────────────────────────────────────────────────────────────────────────────
    ______________________________
    Launching test: hello_world_openmp/a34fe818
    ______________________________
    Launching test: hello_world_openmp/4c03a59d
    ______________________________
    Launching test: hello_world_openmp/69b3eeb1
    hello_world_openmp/a34fe818: Running Test via command: bash --norc --noprofile -eo pipefail hello_world_openmp_build.sh
    hello_world_openmp/4c03a59d: Running Test via command: bash --norc --noprofile -eo pipefail hello_world_openmp_build.sh
    hello_world_openmp/a34fe818: JobID 53187458 dispatched to scheduler
    hello_world_openmp/69b3eeb1: Running Test via command: bash --norc --noprofile -eo pipefail hello_world_openmp_build.sh
    hello_world_openmp/4c03a59d: JobID 53187459 dispatched to scheduler
    hello_world_openmp/69b3eeb1: JobID 53187460 dispatched to scheduler
    Polling Jobs in 30 seconds
                                         Pending Jobs
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┓
    ┃ Builder                     ┃ executor             ┃ JobID    ┃ JobState ┃ runtime ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━┩
    │ hello_world_openmp/4c03a59d │ cori.slurm.knl_debug │ 53187459 │ PENDING  │ 30.851  │
    │ hello_world_openmp/a34fe818 │ cori.slurm.knl_debug │ 53187458 │ PENDING  │ 30.955  │
    │ hello_world_openmp/69b3eeb1 │ cori.slurm.knl_debug │ 53187460 │ RUNNING  │ 30.637  │
    └─────────────────────────────┴──────────────────────┴──────────┴──────────┴─────────┘
    Polling Jobs in 30 seconds
    hello_world_openmp/69b3eeb1: Job 53187460 is complete!
    hello_world_openmp/69b3eeb1: Writing output file -  /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/69b3eeb1/hello_world_openmp.out
    hello_world_openmp/69b3eeb1: Writing error file - /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/69b3eeb1/hello_world_openmp.err
                                         Pending Jobs
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┓
    ┃ Builder                     ┃ executor             ┃ JobID    ┃ JobState ┃ runtime ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━┩
    │ hello_world_openmp/4c03a59d │ cori.slurm.knl_debug │ 53187459 │ PENDING  │ 61.203  │
    │ hello_world_openmp/a34fe818 │ cori.slurm.knl_debug │ 53187458 │ PENDING  │ 61.311  │
    └─────────────────────────────┴──────────────────────┴──────────┴──────────┴─────────┘
    Polling Jobs in 30 seconds
                                         Pending Jobs
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┓
    ┃ Builder                     ┃ executor             ┃ JobID    ┃ JobState ┃ runtime ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━┩
    │ hello_world_openmp/4c03a59d │ cori.slurm.knl_debug │ 53187459 │ PENDING  │ 91.899  │
    │ hello_world_openmp/a34fe818 │ cori.slurm.knl_debug │ 53187458 │ PENDING  │ 92.003  │
    └─────────────────────────────┴──────────────────────┴──────────┴──────────┴─────────┘
    Polling Jobs in 30 seconds
                                         Pending Jobs
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┓
    ┃ Builder                     ┃ executor             ┃ JobID    ┃ JobState ┃ runtime ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━┩
    │ hello_world_openmp/4c03a59d │ cori.slurm.knl_debug │ 53187459 │ PENDING  │ 122.139 │
    │ hello_world_openmp/a34fe818 │ cori.slurm.knl_debug │ 53187458 │ PENDING  │ 122.247 │
    └─────────────────────────────┴──────────────────────┴──────────┴──────────┴─────────┘
    Polling Jobs in 30 seconds
                                         Pending Jobs
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┓
    ┃ Builder                     ┃ executor             ┃ JobID    ┃ JobState ┃ runtime ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━┩
    │ hello_world_openmp/4c03a59d │ cori.slurm.knl_debug │ 53187459 │ PENDING  │ 152.386 │
    │ hello_world_openmp/a34fe818 │ cori.slurm.knl_debug │ 53187458 │ PENDING  │ 152.495 │
    └─────────────────────────────┴──────────────────────┴──────────┴──────────┴─────────┘
    Polling Jobs in 30 seconds
                                         Pending Jobs
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┓
    ┃ Builder                     ┃ executor             ┃ JobID    ┃ JobState ┃ runtime ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━┩
    │ hello_world_openmp/4c03a59d │ cori.slurm.knl_debug │ 53187459 │ RUNNING  │ 182.635 │
    │ hello_world_openmp/a34fe818 │ cori.slurm.knl_debug │ 53187458 │ RUNNING  │ 182.739 │
    └─────────────────────────────┴──────────────────────┴──────────┴──────────┴─────────┘
    Polling Jobs in 30 seconds
    hello_world_openmp/4c03a59d: Job 53187459 is complete!
    hello_world_openmp/4c03a59d: Writing output file -  /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/4c03a59d/hello_world_openmp.out
    hello_world_openmp/4c03a59d: Writing error file - /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/4c03a59d/hello_world_openmp.err
    hello_world_openmp/a34fe818: Job 53187458 is complete!
    hello_world_openmp/a34fe818: Writing output file -  /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/a34fe818/hello_world_openmp.out
    hello_world_openmp/a34fe818: Writing error file - /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/a34fe818/hello_world_openmp.err
                       Pending Jobs
    ┏━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┓
    ┃ Builder ┃ executor ┃ JobID ┃ JobState ┃ runtime ┃
    ┡━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━┩
    └─────────┴──────────┴───────┴──────────┴─────────┘
                                          Completed Jobs
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━┓
    ┃ Builder                     ┃ executor             ┃ JobID    ┃ JobState  ┃ runtime    ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━┩
    │ hello_world_openmp/69b3eeb1 │ cori.slurm.knl_debug │ 53187460 │ COMPLETED │ 60.992638  │
    │ hello_world_openmp/a34fe818 │ cori.slurm.knl_debug │ 53187458 │ COMPLETED │ 213.335162 │
    │ hello_world_openmp/4c03a59d │ cori.slurm.knl_debug │ 53187459 │ COMPLETED │ 212.88734  │
    └─────────────────────────────┴──────────────────────┴──────────┴───────────┴────────────┘
                                                             Test Summary
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┓
    ┃ Builder                     ┃ executor             ┃ status ┃ Checks (ReturnCode, Regex, Runtime) ┃ ReturnCode ┃ Runtime    ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━┩
    │ hello_world_openmp/69b3eeb1 │ cori.slurm.knl_debug │ PASS   │ N/A N/A N/A                         │ 0          │ 60.992638  │
    ├─────────────────────────────┼──────────────────────┼────────┼─────────────────────────────────────┼────────────┼────────────┤
    │ hello_world_openmp/a34fe818 │ cori.slurm.knl_debug │ PASS   │ N/A N/A N/A                         │ 0          │ 213.335162 │
    ├─────────────────────────────┼──────────────────────┼────────┼─────────────────────────────────────┼────────────┼────────────┤
    │ hello_world_openmp/4c03a59d │ cori.slurm.knl_debug │ PASS   │ N/A N/A N/A                         │ 0          │ 212.88734  │
    └─────────────────────────────┴──────────────────────┴────────┴─────────────────────────────────────┴────────────┴────────────┘



    Passed Tests: 3/3 Percentage: 100.000%
    Failed Tests: 0/3 Percentage: 0.000%


    Adding 3 test results to /global/u1/s/siddiq90/github/buildtest/var/report.json
    Writing Logfile to: /global/u1/s/siddiq90/github/buildtest/var/logs/buildtest_rcvotmq_.log

Now let's query the result via **buildtest inspect query** and examine the run. First we will need to specify the appropriate builder ids, we can specify
builder name in quotes to specify a regular expression which buildtest understands when fetching record. In this test, we see that **BUILDTEST_NUMPROCS** is
set for each test corresponding to value specified via ``--procs``. In the build script you will notice the ``sbatch`` line for submitting the job will take into
account the processor value. In the output we see each thread will print **Hello World... from thread** followed by name of thread where number of threads for these
tests are controlled by value set by ``OMP_NUM_THREADS``.

.. code-block:: console

    (buildtest) siddiq90@cori03> buildtest inspect query -t -o -b "hello_world_openmp/(69|a3|4c)"
    ────────────────────────────────────────────────────────────────── hello_world_openmp/4c03a59d-55ed-43eb-9932-da3f5a856607 ──────────────────────────────────────────────────────────────────
    Executor: cori.slurm.knl_debug
    Description: Hello World OpenMP scaling example with processor count
    State: PASS
    Returncode: 0
    Runtime: 212.88734 sec
    Starttime: 2022/01/14 08:30:52
    Endtime: 2022/01/14 08:34:25
    Command: bash --norc --noprofile -eo pipefail hello_world_openmp_build.sh
    Test Script: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/4c03a59d/hello_world_openmp.sh
    Build Script: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/4c03a59d/hello_world_openmp_build.sh
    Output File: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/4c03a59d/hello_world_openmp.out
    Error File: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/4c03a59d/hello_world_openmp.err
    Log File: /global/u1/s/siddiq90/github/buildtest/var/logs/buildtest_rcvotmq_.log
    ──────────────────── Output File: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/4c03a59d/hello_world_openmp.out ─────────────────────
    Hello World... from thread = 4
    Hello World... from thread = 5
    Hello World... from thread = 3
    Hello World... from thread = 1
    Hello World... from thread = 7
    Hello World... from thread = 2
    Hello World... from thread = 13
    Hello World... from thread = 14
    Hello World... from thread = 0
    Hello World... from thread = 15
    Hello World... from thread = 11
    Hello World... from thread = 10
    Hello World... from thread = 9
    Hello World... from thread = 12
    Hello World... from thread = 6
    Hello World... from thread = 8

    ────────────────────── Test File: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/4c03a59d/hello_world_openmp.sh ──────────────────────
       1 #!/bin/bash
       2 ####### START OF SCHEDULER DIRECTIVES #######
       3 #SBATCH -t 10
       4 #SBATCH --job-name=hello_world_openmp
       5 #SBATCH --output=hello_world_openmp.out
       6 #SBATCH --error=hello_world_openmp.err
       7 ####### END OF SCHEDULER DIRECTIVES   #######
       8
       9
      10 # name of executable
      11 _EXEC=hello.c.exe
      12 # Declare environment variables
      13 export OMP_NUM_THREADS=$BUILDTEST_NUMPROCS
      14
      15
      16 # Loading modules
      17 module load PrgEnv-intel/6.0.5
      18 # Compilation Line
      19 cc -qopenmp -o $_EXEC /global/u1/s/siddiq90/github/buildtest-cori/buildspecs/apps/openmp/src/hello.c
      20
      21
      22 # Run executable
      23 ./$_EXEC
      24
      25
    ─────────────────── Test File: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/4c03a59d/hello_world_openmp_build.sh ───────────────────
       1 #!/bin/bash
       2
       3
       4 ############# START VARIABLE DECLARATION ########################
       5 export BUILDTEST_TEST_NAME=hello_world_openmp
       6 export BUILDTEST_TEST_ROOT=/global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/4c03a59d
       7 export BUILDTEST_BUILDSPEC_DIR=/global/u1/s/siddiq90/github/buildtest-cori/buildspecs/apps/openmp
       8 export BUILDTEST_STAGE_DIR=/global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/4c03a59d/stage
       9 export BUILDTEST_TEST_ID=4c03a59d-55ed-43eb-9932-da3f5a856607
      10 export BUILDTEST_NUMPROCS=16
      11 ############# END VARIABLE DECLARATION   ########################
      12
      13
      14 # source executor startup script
      15 source /global/u1/s/siddiq90/github/buildtest/var/executor/cori.slurm.knl_debug/before_script.sh
      16 # Run generated script
      17 sbatch --parsable -q debug --clusters=cori -n 16 -C knl,quad,cache /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/4c03a59d/stage/
      18 # Get return code
      19 returncode=$?
      20 # Exit with return code
      21 exit $returncode
    ────────────────────────────────────────────────────────────────── hello_world_openmp/a34fe818-e0a6-4749-85d6-a88dad6d8434 ──────────────────────────────────────────────────────────────────
    Executor: cori.slurm.knl_debug
    Description: Hello World OpenMP scaling example with processor count
    State: PASS
    Returncode: 0
    Runtime: 213.335162 sec
    Starttime: 2022/01/14 08:30:52
    Endtime: 2022/01/14 08:34:26
    Command: bash --norc --noprofile -eo pipefail hello_world_openmp_build.sh
    Test Script: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/a34fe818/hello_world_openmp.sh
    Build Script: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/a34fe818/hello_world_openmp_build.sh
    Output File: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/a34fe818/hello_world_openmp.out
    Error File: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/a34fe818/hello_world_openmp.err
    Log File: /global/u1/s/siddiq90/github/buildtest/var/logs/buildtest_rcvotmq_.log
    ──────────────────── Output File: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/a34fe818/hello_world_openmp.out ─────────────────────
    Hello World... from thread = 0
    Hello World... from thread = 3
    Hello World... from thread = 2
    Hello World... from thread = 1
    Hello World... from thread = 4
    Hello World... from thread = 6
    Hello World... from thread = 5
    Hello World... from thread = 7

    ────────────────────── Test File: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/a34fe818/hello_world_openmp.sh ──────────────────────
       1 #!/bin/bash
       2 ####### START OF SCHEDULER DIRECTIVES #######
       3 #SBATCH -t 10
       4 #SBATCH --job-name=hello_world_openmp
       5 #SBATCH --output=hello_world_openmp.out
       6 #SBATCH --error=hello_world_openmp.err
       7 ####### END OF SCHEDULER DIRECTIVES   #######
       8
       9
      10 # name of executable
      11 _EXEC=hello.c.exe
      12 # Declare environment variables
      13 export OMP_NUM_THREADS=$BUILDTEST_NUMPROCS
      14
      15
      16 # Loading modules
      17 module load PrgEnv-intel/6.0.5
      18 # Compilation Line
      19 cc -qopenmp -o $_EXEC /global/u1/s/siddiq90/github/buildtest-cori/buildspecs/apps/openmp/src/hello.c
      20
      21
      22 # Run executable
      23 ./$_EXEC
      24
      25
    ─────────────────── Test File: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/a34fe818/hello_world_openmp_build.sh ───────────────────
       1 #!/bin/bash
       2
       3
       4 ############# START VARIABLE DECLARATION ########################
       5 export BUILDTEST_TEST_NAME=hello_world_openmp
       6 export BUILDTEST_TEST_ROOT=/global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/a34fe818
       7 export BUILDTEST_BUILDSPEC_DIR=/global/u1/s/siddiq90/github/buildtest-cori/buildspecs/apps/openmp
       8 export BUILDTEST_STAGE_DIR=/global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/a34fe818/stage
       9 export BUILDTEST_TEST_ID=a34fe818-e0a6-4749-85d6-a88dad6d8434
      10 export BUILDTEST_NUMPROCS=8
      11 ############# END VARIABLE DECLARATION   ########################
      12
      13
      14 # source executor startup script
      15 source /global/u1/s/siddiq90/github/buildtest/var/executor/cori.slurm.knl_debug/before_script.sh
      16 # Run generated script
      17 sbatch --parsable -q debug --clusters=cori -n 8 -C knl,quad,cache /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/a34fe818/stage/h
      18 # Get return code
      19 returncode=$?
      20 # Exit with return code
      21 exit $returncode
    ────────────────────────────────────────────────────────────────── hello_world_openmp/69b3eeb1-51c1-400d-8655-b115cef634d7 ──────────────────────────────────────────────────────────────────
    Executor: cori.slurm.knl_debug
    Description: Hello World OpenMP scaling example with processor count
    State: PASS
    Returncode: 0
    Runtime: 60.992638 sec
    Starttime: 2022/01/14 08:30:53
    Endtime: 2022/01/14 08:31:54
    Command: bash --norc --noprofile -eo pipefail hello_world_openmp_build.sh
    Test Script: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/69b3eeb1/hello_world_openmp.sh
    Build Script: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/69b3eeb1/hello_world_openmp_build.sh
    Output File: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/69b3eeb1/hello_world_openmp.out
    Error File: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/69b3eeb1/hello_world_openmp.err
    Log File: /global/u1/s/siddiq90/github/buildtest/var/logs/buildtest_rcvotmq_.log
    ──────────────────── Output File: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/69b3eeb1/hello_world_openmp.out ─────────────────────
    Hello World... from thread = 16
    Hello World... from thread = 17
    Hello World... from thread = 5
    Hello World... from thread = 0
    Hello World... from thread = 1
    Hello World... from thread = 19
    Hello World... from thread = 8
    Hello World... from thread = 12
    Hello World... from thread = 20
    Hello World... from thread = 13
    Hello World... from thread = 9
    Hello World... from thread = 11
    Hello World... from thread = 3
    Hello World... from thread = 23
    Hello World... from thread = 22
    Hello World... from thread = 2
    Hello World... from thread = 14
    Hello World... from thread = 15
    Hello World... from thread = 4
    Hello World... from thread = 7
    Hello World... from thread = 6
    Hello World... from thread = 10
    Hello World... from thread = 18
    Hello World... from thread = 21

    ────────────────────── Test File: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/69b3eeb1/hello_world_openmp.sh ──────────────────────
       1 #!/bin/bash
       2 ####### START OF SCHEDULER DIRECTIVES #######
       3 #SBATCH -t 10
       4 #SBATCH --job-name=hello_world_openmp
       5 #SBATCH --output=hello_world_openmp.out
       6 #SBATCH --error=hello_world_openmp.err
       7 ####### END OF SCHEDULER DIRECTIVES   #######
       8
       9
      10 # name of executable
      11 _EXEC=hello.c.exe
      12 # Declare environment variables
      13 export OMP_NUM_THREADS=$BUILDTEST_NUMPROCS
      14
      15
      16 # Loading modules
      17 module load PrgEnv-intel/6.0.5
      18 # Compilation Line
      19 cc -qopenmp -o $_EXEC /global/u1/s/siddiq90/github/buildtest-cori/buildspecs/apps/openmp/src/hello.c
      20
      21
      22 # Run executable
      23 ./$_EXEC
      24
      25
    ─────────────────── Test File: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/69b3eeb1/hello_world_openmp_build.sh ───────────────────
       1 #!/bin/bash
       2
       3
       4 ############# START VARIABLE DECLARATION ########################
       5 export BUILDTEST_TEST_NAME=hello_world_openmp
       6 export BUILDTEST_TEST_ROOT=/global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/69b3eeb1
       7 export BUILDTEST_BUILDSPEC_DIR=/global/u1/s/siddiq90/github/buildtest-cori/buildspecs/apps/openmp
       8 export BUILDTEST_STAGE_DIR=/global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/69b3eeb1/stage
       9 export BUILDTEST_TEST_ID=69b3eeb1-51c1-400d-8655-b115cef634d7
      10 export BUILDTEST_NUMPROCS=24
      11 ############# END VARIABLE DECLARATION   ########################
      12
      13
      14 # source executor startup script
      15 source /global/u1/s/siddiq90/github/buildtest/var/executor/cori.slurm.knl_debug/before_script.sh
      16 # Run generated script
      17 sbatch --parsable -q debug --clusters=cori -n 24 -C knl,quad,cache /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/69b3eeb1/stage/
      18 # Get return code
      19 returncode=$?
      20 # Exit with return code
      21 exit $returncode


.. _cray_burstbuffer_datawarp:

Cray Burst Buffer & Data Warp
-------------------------------

For Cray systems, you may want to stage-in or stage-out into your burst buffer to perform some computation. We can do this
via ``#DW`` directive. You can see some example jobs using Burst Buffer at NERSC https://docs.nersc.gov/jobs/examples/#burst-buffer

In buildtest we support properties ``BB`` and ``DW`` which is a list of job directives
that get inserted as **#BW** and **#DW** into the test script. We will create a persistent burst buffer
named **databuffer** of size 10GB striped. We access the burst buffer using the `DW` directive. Finally we
cd into the databuffer and write a 5GB random file.

.. Note:: BB and DW directives are generated after scheduler directives. The ``#BB``
   comes before ``#DW``. buildtest will automatically add the directive **#BB**
   and **#DW** when using properties BB and DW

.. code-block:: yaml
    :emphasize-lines: 9-12
    :linenos:

    buildspecs:
      create_burst_buffer:
        type: script
        executor: cori.slurm.knl_debug
        description: Create a burst buffer
        tags: [jobs, cray]
        sbatch: ["-N 1", "-t 5", "-n 1"]
        BB:
          - create_persistent name=databuffer capacity=10GB access_mode=striped type=scratch
        DW:
          - persistentdw name=databuffer
        run: |
          cd $DW_PERSISTENT_STRIPED_databuffer
          pwd
          dd if=/dev/urandom of=random.txt bs=1G count=5 iflag=fullblock
          ls -lh $DW_PERSISTENT_STRIPED_databuffer/

Next we ran this test and inspect the generated test, we see that buildtest will insert the ``#BB`` and ``#DW`` directives as specified in the buildspec. In the output we see a
5GB file called ``random.txt`` was written to the burst buffer.

.. code-block:: console

    (buildtest) siddiq90@cori03> buildtest inspect query -o -t create_burst_buffer/b5f8d28b
    ───────────────────────────────────────────────────────────────── create_burst_buffer/b5f8d28b-3636-43a8-a526-d2cfde491182 ──────────────────────────────────────────────────────────────────
    Executor: cori.slurm.knl_debug
    Description: Create a burst buffer
    State: PASS
    Returncode: 0
    Runtime: 153.018352 sec
    Starttime: 2022/01/14 08:58:55
    Endtime: 2022/01/14 09:01:28
    Command: bash --norc --noprofile -eo pipefail create_burst_buffer_build.sh
    Test Script: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/create_buffer/create_burst_buffer/b5f8d28b/create_burst_buffer.sh
    Build Script: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/create_buffer/create_burst_buffer/b5f8d28b/create_burst_buffer_build.sh
    Output File: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/create_buffer/create_burst_buffer/b5f8d28b/create_burst_buffer.out
    Error File: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/create_buffer/create_burst_buffer/b5f8d28b/create_burst_buffer.err
    Log File: /global/u1/s/siddiq90/github/buildtest/var/logs/buildtest_4083nndh.log
    ─────────────────── Output File: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/create_buffer/create_burst_buffer/b5f8d28b/create_burst_buffer.out ───────────────────
    /var/opt/cray/dws/mounts/batch/databuffer_53189126_striped_scratch
    total 5.0G
    -rw-rw-r-- 1 siddiq90 siddiq90 5.0G Jan 14 08:59 random.txt

    ──────────────────── Test File: /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/create_buffer/create_burst_buffer/b5f8d28b/create_burst_buffer.sh ─────────────────────
       1 #!/bin/bash
       2 ####### START OF SCHEDULER DIRECTIVES #######
       3 #SBATCH -N 1
       4 #SBATCH -t 5
       5 #SBATCH -n 1
       6 #SBATCH --job-name=create_burst_buffer
       7 #SBATCH --output=create_burst_buffer.out
       8 #SBATCH --error=create_burst_buffer.err
       9 ####### END OF SCHEDULER DIRECTIVES   #######
      10 ####### START OF BURST BUFFER DIRECTIVES #######
      11 #BB create_persistent name=databuffer capacity=10GB access_mode=striped type=scratch
      12 ####### END OF BURST BUFFER DIRECTIVES   #######
      13 ####### START OF DATAWARP DIRECTIVES #######
      14 #DW persistentdw name=databuffer
      15 ####### END OF DATAWARP DIRECTIVES   #######
      16 # Content of run section
      17 cd $DW_PERSISTENT_STRIPED_databuffer
      18 pwd
      19 dd if=/dev/urandom of=random.txt bs=1G count=5 iflag=fullblock
      20 ls -lh $DW_PERSISTENT_STRIPED_databuffer/
      21
