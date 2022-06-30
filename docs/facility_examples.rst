Facility Test Examples
========================

We will discuss a few test examples implemented at NERSC that are available at https://github.com/buildtesters/buildtest-nersc/.

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
        executor: cori.local.bash
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
                load: [impi/2020.up4]
                swap: [intel, intel/19.1.2.254]

The generated test script is show below, notice that ``mpiicc`` is used to compile the program and run via srun.

.. code-block:: shell

    $ buildtest inspect query -t laplace_mpi/1a4c7a6f
    ─────────────────────────────────────────────── laplace_mpi/1a4c7a6f-0f69-40e7-b451-f9f62843eee5 ────────────────────────────────────────────────
    Executor: cori.slurm.knl_debug
    Description: Laplace MPI code in C
    State: PASS
    Returncode: 0
    Runtime: 31.496144 sec
    Starttime: 2022/06/30 14:35:34
    Endtime: 2022/06/30 14:36:06
    Command: bash --norc --noprofile -eo pipefail laplace_mpi_build.sh
    Test Script: /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/laplace_mpi/laplace_mpi/1a4c7a6f/laplace_mpi.sh
    Build Script: /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/laplace_mpi/laplace_mpi/1a4c7a6f/laplace_mpi_build.sh
    Output File: /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/laplace_mpi/laplace_mpi/1a4c7a6f/laplace_mpi.out
    Error File: /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/laplace_mpi/laplace_mpi/1a4c7a6f/laplace_mpi.err
    Log File: /global/u1/s/siddiq90/gitrepos/buildtest/var/logs/buildtest_e5cuwqhf.log
    ────── Test File: /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/laplace_mpi/laplace_mpi/1a4c7a6f/laplace_mpi.sh ───────
    #!/bin/bash
    #SBATCH -N 1
    #SBATCH -n 4
    #SBATCH --job-name=laplace_mpi
    #SBATCH --output=laplace_mpi.out
    #SBATCH --error=laplace_mpi.err


    # name of executable
    _EXEC=laplace_mpi.c.exe
    # Loading modules
    module swap intel intel/19.1.2.254
    module load impi/2020.up4
    # Compilation Line
    mpiicc -O3 -o $_EXEC /global/u1/s/siddiq90/gitrepos/buildtest-nersc/buildspecs/apps/mpi/src/laplace_mpi.c


    # Run executable
    srun -n 4 $_EXEC


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

    $ buildtest bd -b openmp_scale.yml --procs 8 16 24
    ╭───────────────────────────────────────────────── buildtest summary ──────────────────────────────────────────────────╮
    │                                                                                                                      │
    │ User:               siddiq90                                                                                         │
    │ Hostname:           cori10                                                                                           │
    │ Platform:           Linux                                                                                            │
    │ Current Time:       2022/06/30 14:39:12                                                                              │
    │ buildtest path:     /global/homes/s/siddiq90/gitrepos/buildtest/bin/buildtest                                        │
    │ buildtest version:  0.14.0                                                                                           │
    │ python path:        /global/u1/s/siddiq90/.local/share/virtualenvs/buildtest-WqshQcL1/bin/python3                    │
    │ python version:     3.9.7                                                                                            │
    │ Configuration File: /global/u1/s/siddiq90/gitrepos/buildtest-nersc/config.yml                                        │
    │ Test Directory:     /global/u1/s/siddiq90/gitrepos/buildtest/var/tests                                               │
    │ Report File:        /global/u1/s/siddiq90/gitrepos/buildtest/var/report.json                                         │
    │ Command:            /global/homes/s/siddiq90/gitrepos/buildtest/bin/buildtest bd -b openmp_scale.yml --procs 8 16 24 │
    │                                                                                                                      │
    ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
    ────────────────────────────────────────────────────────────  Discovering Buildspecs ────────────────────────────────────────────────────────────
                                      Discovered buildspecs
    ╔════════════════════════════════════════════════════════════════════════════════════════╗
    ║ buildspec                                                                              ║
    ╟────────────────────────────────────────────────────────────────────────────────────────╢
    ║ /global/u1/s/siddiq90/gitrepos/buildtest-nersc/buildspecs/apps/openmp/openmp_scale.yml ║
    ╚════════════════════════════════════════════════════════════════════════════════════════╝


    Total Discovered Buildspecs:  1
    Total Excluded Buildspecs:  0
    Detected Buildspecs after exclusion:  1
    ────────────────────────────────────────────────────────────── Parsing Buildspecs ───────────────────────────────────────────────────────────────
    Buildtest will parse 1 buildspecs
    Valid Buildspecs: 1
    Invalid Buildspecs: 0
    /global/u1/s/siddiq90/gitrepos/buildtest-nersc/buildspecs/apps/openmp/openmp_scale.yml: VALID
    Total builder objects created: 4
    Total compiler builder: 4
    Total script builder: 0
    Total spack builder: 0
                                                                Compiler Builder Details
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ builder                   ┃ executor             ┃ compiler           ┃ nodes ┃ procs ┃ description               ┃ buildspecs                ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ hello_world_openmp/a7de0… │ cori.slurm.knl_debug │ PrgEnv-intel/6.0.5 │ None  │ None  │ Hello World OpenMP        │ /global/u1/s/siddiq90/gi… │
    │                           │                      │                    │       │       │ scaling example with      │                           │
    │                           │                      │                    │       │       │ processor count           │                           │
    ├───────────────────────────┼──────────────────────┼────────────────────┼───────┼───────┼───────────────────────────┼───────────────────────────┤
    │ hello_world_openmp/ce755… │ cori.slurm.knl_debug │ PrgEnv-intel/6.0.5 │ None  │ 8     │ Hello World OpenMP        │ /global/u1/s/siddiq90/gi… │
    │                           │                      │                    │       │       │ scaling example with      │                           │
    │                           │                      │                    │       │       │ processor count           │                           │
    ├───────────────────────────┼──────────────────────┼────────────────────┼───────┼───────┼───────────────────────────┼───────────────────────────┤
    │ hello_world_openmp/fa271… │ cori.slurm.knl_debug │ PrgEnv-intel/6.0.5 │ None  │ 16    │ Hello World OpenMP        │ /global/u1/s/siddiq90/gi… │
    │                           │                      │                    │       │       │ scaling example with      │                           │
    │                           │                      │                    │       │       │ processor count           │                           │
    ├───────────────────────────┼──────────────────────┼────────────────────┼───────┼───────┼───────────────────────────┼───────────────────────────┤
    │ hello_world_openmp/0fe29… │ cori.slurm.knl_debug │ PrgEnv-intel/6.0.5 │ None  │ 24    │ Hello World OpenMP        │ /global/u1/s/siddiq90/gi… │
    │                           │                      │                    │       │       │ scaling example with      │                           │
    │                           │                      │                    │       │       │ processor count           │                           │
    └───────────────────────────┴──────────────────────┴────────────────────┴───────┴───────┴───────────────────────────┴───────────────────────────┘
                                                                  Batch Job Builders
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ builder                     ┃ executor             ┃ buildspecs                                                                             ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ hello_world_openmp/a7de0abb │ cori.slurm.knl_debug │ /global/u1/s/siddiq90/gitrepos/buildtest-nersc/buildspecs/apps/openmp/openmp_scale.yml │
    ├─────────────────────────────┼──────────────────────┼────────────────────────────────────────────────────────────────────────────────────────┤
    │ hello_world_openmp/ce755367 │ cori.slurm.knl_debug │ /global/u1/s/siddiq90/gitrepos/buildtest-nersc/buildspecs/apps/openmp/openmp_scale.yml │
    ├─────────────────────────────┼──────────────────────┼────────────────────────────────────────────────────────────────────────────────────────┤
    │ hello_world_openmp/fa271571 │ cori.slurm.knl_debug │ /global/u1/s/siddiq90/gitrepos/buildtest-nersc/buildspecs/apps/openmp/openmp_scale.yml │
    ├─────────────────────────────┼──────────────────────┼────────────────────────────────────────────────────────────────────────────────────────┤
    │ hello_world_openmp/0fe298ae │ cori.slurm.knl_debug │ /global/u1/s/siddiq90/gitrepos/buildtest-nersc/buildspecs/apps/openmp/openmp_scale.yml │
    └─────────────────────────────┴──────────────────────┴────────────────────────────────────────────────────────────────────────────────────────┘
                                                            Batch Job Builders by Processors
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ builder                     ┃ executor             ┃ procs ┃ buildspecs                                                                       ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ hello_world_openmp/ce755367 │ cori.slurm.knl_debug │ 8     │ /global/u1/s/siddiq90/gitrepos/buildtest-nersc/buildspecs/apps/openmp/openmp_sca │
    │                             │                      │       │ le.yml                                                                           │
    ├─────────────────────────────┼──────────────────────┼───────┼──────────────────────────────────────────────────────────────────────────────────┤
    │ hello_world_openmp/fa271571 │ cori.slurm.knl_debug │ 16    │ /global/u1/s/siddiq90/gitrepos/buildtest-nersc/buildspecs/apps/openmp/openmp_sca │
    │                             │                      │       │ le.yml                                                                           │
    ├─────────────────────────────┼──────────────────────┼───────┼──────────────────────────────────────────────────────────────────────────────────┤
    │ hello_world_openmp/0fe298ae │ cori.slurm.knl_debug │ 24    │ /global/u1/s/siddiq90/gitrepos/buildtest-nersc/buildspecs/apps/openmp/openmp_sca │
    │                             │                      │       │ le.yml                                                                           │
    └─────────────────────────────┴──────────────────────┴───────┴──────────────────────────────────────────────────────────────────────────────────┘
    ───────────────────────────────────────────────────────────────── Building Test ─────────────────────────────────────────────────────────────────
    hello_world_openmp/a7de0abb: Creating test directory:
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/a7de0abb
    hello_world_openmp/a7de0abb: Creating the stage directory:
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/a7de0abb/stage
    hello_world_openmp/a7de0abb: Writing build script:
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/a7de0abb/hello_world_openmp_build.sh
    hello_world_openmp/ce755367: Creating test directory:
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/ce755367
    hello_world_openmp/ce755367: Creating the stage directory:
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/ce755367/stage
    hello_world_openmp/ce755367: Writing build script:
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/ce755367/hello_world_openmp_build.sh
    hello_world_openmp/fa271571: Creating test directory:
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/fa271571
    hello_world_openmp/fa271571: Creating the stage directory:
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/fa271571/stage
    hello_world_openmp/fa271571: Writing build script:
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/fa271571/hello_world_openmp_build.sh
    hello_world_openmp/0fe298ae: Creating test directory:
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/0fe298ae
    hello_world_openmp/0fe298ae: Creating the stage directory:
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/0fe298ae/stage
    hello_world_openmp/0fe298ae: Writing build script:
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/0fe298ae/hello_world_openmp_build.sh
    ───────────────────────────────────────────────────────────────── Running Tests ─────────────────────────────────────────────────────────────────
    Spawning 64 processes for processing builders
    ────────────────────────────────────────────────────────────────── Iteration 1 ──────────────────────────────────────────────────────────────────
    hello_world_openmp/a7de0abb does not have any dependencies adding test to queue
    hello_world_openmp/0fe298ae does not have any dependencies adding test to queue
    hello_world_openmp/fa271571 does not have any dependencies adding test to queue
    hello_world_openmp/ce755367 does not have any dependencies adding test to queue
    In this iteration we are going to run the following tests: [hello_world_openmp/a7de0abb, hello_world_openmp/0fe298ae, hello_world_openmp/fa271571, hello_world_openmp/ce755367]
    hello_world_openmp/0fe298ae: Running Test via command: bash --norc --noprofile -eo pipefail hello_world_openmp_build.sh
    hello_world_openmp/ce755367: Running Test via command: bash --norc --noprofile -eo pipefail hello_world_openmp_build.sh
    hello_world_openmp/a7de0abb: Running Test via command: bash --norc --noprofile -eo pipefail hello_world_openmp_build.sh
    hello_world_openmp/fa271571: Running Test via command: bash --norc --noprofile -eo pipefail hello_world_openmp_build.sh
    hello_world_openmp/0fe298ae: JobID 60681274 dispatched to scheduler
    hello_world_openmp/a7de0abb: JobID 60681275 dispatched to scheduler
    hello_world_openmp/ce755367: JobID 60681276 dispatched to scheduler
    hello_world_openmp/fa271571: JobID 60681277 dispatched to scheduler
    Polling Jobs in 30 seconds
    hello_world_openmp/0fe298ae: Job 60681274 is complete!
    hello_world_openmp/0fe298ae: Test completed in 31.868266 seconds
    hello_world_openmp/0fe298ae: Test completed with returncode: 0
    hello_world_openmp/0fe298ae: Writing output file -
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/0fe298ae/hello_world_openmp.out
    hello_world_openmp/0fe298ae: Writing error file -
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/0fe298ae/hello_world_openmp.err
    hello_world_openmp/ce755367: Job 60681276 is complete!
    hello_world_openmp/ce755367: Test completed in 32.010719 seconds
    hello_world_openmp/ce755367: Test completed with returncode: 0
    hello_world_openmp/ce755367: Writing output file -
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/ce755367/hello_world_openmp.out
    hello_world_openmp/ce755367: Writing error file -
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/ce755367/hello_world_openmp.err
                                         Running Jobs
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┓
    ┃ builder                     ┃ executor             ┃ jobid    ┃ jobstate ┃ runtime ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━┩
    │ hello_world_openmp/a7de0abb │ cori.slurm.knl_debug │ 60681275 │ RUNNING  │ 31.957  │
    │ hello_world_openmp/fa271571 │ cori.slurm.knl_debug │ 60681277 │ RUNNING  │ 31.987  │
    └─────────────────────────────┴──────────────────────┴──────────┴──────────┴─────────┘
                                         Completed Jobs
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┓
    ┃ builder                     ┃ executor             ┃ jobid    ┃ jobstate  ┃ runtime   ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━┩
    │ hello_world_openmp/0fe298ae │ cori.slurm.knl_debug │ 60681274 │ COMPLETED │ 31.868266 │
    │ hello_world_openmp/ce755367 │ cori.slurm.knl_debug │ 60681276 │ COMPLETED │ 32.010719 │
    └─────────────────────────────┴──────────────────────┴──────────┴───────────┴───────────┘
    Polling Jobs in 30 seconds
    hello_world_openmp/fa271571: Job 60681277 is complete!
    hello_world_openmp/fa271571: Test completed in 62.153829 seconds
    hello_world_openmp/fa271571: Test completed with returncode: 0
    hello_world_openmp/fa271571: Writing output file -
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/fa271571/hello_world_openmp.out
    hello_world_openmp/fa271571: Writing error file -
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/fa271571/hello_world_openmp.err
                                         Running Jobs
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┓
    ┃ builder                     ┃ executor             ┃ jobid    ┃ jobstate ┃ runtime ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━┩
    │ hello_world_openmp/a7de0abb │ cori.slurm.knl_debug │ 60681275 │ RUNNING  │ 62.132  │
    └─────────────────────────────┴──────────────────────┴──────────┴──────────┴─────────┘
                                         Completed Jobs
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┓
    ┃ builder                     ┃ executor             ┃ jobid    ┃ jobstate  ┃ runtime   ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━┩
    │ hello_world_openmp/fa271571 │ cori.slurm.knl_debug │ 60681277 │ COMPLETED │ 62.153829 │
    └─────────────────────────────┴──────────────────────┴──────────┴───────────┴───────────┘
    Polling Jobs in 30 seconds
    hello_world_openmp/a7de0abb: Job 60681275 is complete!
    hello_world_openmp/a7de0abb: Test completed in 92.278197 seconds
    hello_world_openmp/a7de0abb: Test completed with returncode: 0
    hello_world_openmp/a7de0abb: Writing output file -
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/a7de0abb/hello_world_openmp.out
    hello_world_openmp/a7de0abb: Writing error file -
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/a7de0abb/hello_world_openmp.err
                                         Completed Jobs
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┓
    ┃ builder                     ┃ executor             ┃ jobid    ┃ jobstate  ┃ runtime   ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━┩
    │ hello_world_openmp/a7de0abb │ cori.slurm.knl_debug │ 60681275 │ COMPLETED │ 92.278197 │
    └─────────────────────────────┴──────────────────────┴──────────┴───────────┴───────────┘
                                                             Test Summary
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━┓
    ┃ builder                     ┃ executor             ┃ status ┃ checks (ReturnCode, Regex, Runtime) ┃ returnCode ┃ runtime   ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━┩
    │ hello_world_openmp/0fe298ae │ cori.slurm.knl_debug │ PASS   │ N/A N/A N/A                         │ 0          │ 31.868266 │
    ├─────────────────────────────┼──────────────────────┼────────┼─────────────────────────────────────┼────────────┼───────────┤
    │ hello_world_openmp/a7de0abb │ cori.slurm.knl_debug │ PASS   │ N/A N/A N/A                         │ 0          │ 92.278197 │
    ├─────────────────────────────┼──────────────────────┼────────┼─────────────────────────────────────┼────────────┼───────────┤
    │ hello_world_openmp/fa271571 │ cori.slurm.knl_debug │ PASS   │ N/A N/A N/A                         │ 0          │ 62.153829 │
    ├─────────────────────────────┼──────────────────────┼────────┼─────────────────────────────────────┼────────────┼───────────┤
    │ hello_world_openmp/ce755367 │ cori.slurm.knl_debug │ PASS   │ N/A N/A N/A                         │ 0          │ 32.010719 │
    └─────────────────────────────┴──────────────────────┴────────┴─────────────────────────────────────┴────────────┴───────────┘



    Passed Tests: 4/4 Percentage: 100.000%
    Failed Tests: 0/4 Percentage: 0.000%


    Adding 4 test results to /global/u1/s/siddiq90/gitrepos/buildtest/var/report.json
    Writing Logfile to: /global/u1/s/siddiq90/gitrepos/buildtest/var/logs/buildtest_ptr4xf10.log


Now let's query the result via **buildtest inspect query** and examine the run. First we will need to specify the appropriate builder ids, we can specify
builder name in quotes to specify a regular expression which buildtest understands when fetching record. In this test, we see that **BUILDTEST_NUMPROCS** is
set for each test corresponding to value specified via ``--procs``. In the build script you will notice the ``sbatch`` line for submitting the job will take into
account the processor value. In the output we see each thread will print **Hello World... from thread** followed by name of thread where number of threads for these
tests are controlled by value set by ``OMP_NUM_THREADS``.

.. code-block:: console

    $ buildtest inspect query -t -o -b "hello_world_openmp/(fa|ce|0f)"
    ──────────────────────────────────────────── hello_world_openmp/fa271571-40e7-4a28-808c-f2ed38b47538 ────────────────────────────────────────────
    Executor: cori.slurm.knl_debug
    Description: Hello World OpenMP scaling example with processor count
    State: PASS
    Returncode: 0
    Runtime: 62.153829 sec
    Starttime: 2022/06/30 14:39:12
    Endtime: 2022/06/30 14:40:14
    Command: bash --norc --noprofile -eo pipefail hello_world_openmp_build.sh
    Test Script:
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/fa271571/hello_world_openmp.sh
    Build Script:
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/fa271571/hello_world_openmp_build.sh
    Output File:
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/fa271571/hello_world_openmp.out
    Error File:
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/fa271571/hello_world_openmp.err
    Log File: /global/u1/s/siddiq90/gitrepos/buildtest/var/logs/buildtest_ptr4xf10.log
    ─ Output File: /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/fa271571/hello_world_op… ─
    Hello World... from thread = 0
    Hello World... from thread = 12
    Hello World... from thread = 13
    Hello World... from thread = 8
    Hello World... from thread = 4
    Hello World... from thread = 9
    Hello World... from thread = 5
    Hello World... from thread = 14
    Hello World... from thread = 11
    Hello World... from thread = 6
    Hello World... from thread = 10
    Hello World... from thread = 7
    Hello World... from thread = 1
    Hello World... from thread = 3
    Hello World... from thread = 2
    Hello World... from thread = 15

    ─ Test File: /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/fa271571/hello_world_open… ─
    #!/bin/bash
    #SBATCH -t 10
    #SBATCH --job-name=hello_world_openmp
    #SBATCH --output=hello_world_openmp.out
    #SBATCH --error=hello_world_openmp.err


    # name of executable
    _EXEC=hello.c.exe
    export OMP_NUM_THREADS="$BUILDTEST_NUMPROCS"
    # Loading modules
    module load PrgEnv-intel/6.0.5
    # Compilation Line
    cc -qopenmp -o $_EXEC /global/u1/s/siddiq90/gitrepos/buildtest-nersc/buildspecs/apps/openmp/src/hello.c


    # Run executable
    ./$_EXEC


    ─ Test File: /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/fa271571/hello_world_open… ─
    #!/bin/bash
    export BUILDTEST_TEST_NAME=hello_world_openmp
    export BUILDTEST_TEST_ROOT=/global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/fa271571
    export BUILDTEST_BUILDSPEC_DIR=/global/u1/s/siddiq90/gitrepos/buildtest-nersc/buildspecs/apps/openmp
    export BUILDTEST_STAGE_DIR=/global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/fa271571/stage
    export BUILDTEST_NUMPROCS=16
    # source executor startup script
    source /global/u1/s/siddiq90/gitrepos/buildtest/var/executor/cori.slurm.knl_debug/before_script.sh
    # Run generated script
    sbatch --parsable -q debug --clusters=cori -n 16 -C knl,quad,cache /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp
    # Get return code
    returncode=$?
    # Exit with return code
    exit $returncode
    ──────────────────────────────────────────── hello_world_openmp/0fe298ae-6704-4a3c-8253-1767e25e6edb ────────────────────────────────────────────
    Executor: cori.slurm.knl_debug
    Description: Hello World OpenMP scaling example with processor count
    State: PASS
    Returncode: 0
    Runtime: 31.868266 sec
    Starttime: 2022/06/30 14:39:12
    Endtime: 2022/06/30 14:39:44
    Command: bash --norc --noprofile -eo pipefail hello_world_openmp_build.sh
    Test Script:
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/0fe298ae/hello_world_openmp.sh
    Build Script:
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/0fe298ae/hello_world_openmp_build.sh
    Output File:
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/0fe298ae/hello_world_openmp.out
    Error File:
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/0fe298ae/hello_world_openmp.err
    Log File: /global/u1/s/siddiq90/gitrepos/buildtest/var/logs/buildtest_ptr4xf10.log
    ─ Output File: /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/0fe298ae/hello_world_op… ─
    Hello World... from thread = 0
    Hello World... from thread = 8
    Hello World... from thread = 12
    Hello World... from thread = 16
    Hello World... from thread = 13
    Hello World... from thread = 9
    Hello World... from thread = 20
    Hello World... from thread = 17
    Hello World... from thread = 21
    Hello World... from thread = 15
    Hello World... from thread = 10
    Hello World... from thread = 19
    Hello World... from thread = 14
    Hello World... from thread = 18
    Hello World... from thread = 4
    Hello World... from thread = 5
    Hello World... from thread = 11
    Hello World... from thread = 1
    Hello World... from thread = 23
    Hello World... from thread = 22
    Hello World... from thread = 3
    Hello World... from thread = 7
    Hello World... from thread = 6
    Hello World... from thread = 2

    ─ Test File: /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/0fe298ae/hello_world_open… ─
    #!/bin/bash
    #SBATCH -t 10
    #SBATCH --job-name=hello_world_openmp
    #SBATCH --output=hello_world_openmp.out
    #SBATCH --error=hello_world_openmp.err


    # name of executable
    _EXEC=hello.c.exe
    export OMP_NUM_THREADS="$BUILDTEST_NUMPROCS"
    # Loading modules
    module load PrgEnv-intel/6.0.5
    # Compilation Line
    cc -qopenmp -o $_EXEC /global/u1/s/siddiq90/gitrepos/buildtest-nersc/buildspecs/apps/openmp/src/hello.c


    # Run executable
    ./$_EXEC


    ─ Test File: /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/0fe298ae/hello_world_open… ─
    #!/bin/bash
    export BUILDTEST_TEST_NAME=hello_world_openmp
    export BUILDTEST_TEST_ROOT=/global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/0fe298ae
    export BUILDTEST_BUILDSPEC_DIR=/global/u1/s/siddiq90/gitrepos/buildtest-nersc/buildspecs/apps/openmp
    export BUILDTEST_STAGE_DIR=/global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/0fe298ae/stage
    export BUILDTEST_NUMPROCS=24
    # source executor startup script
    source /global/u1/s/siddiq90/gitrepos/buildtest/var/executor/cori.slurm.knl_debug/before_script.sh
    # Run generated script
    sbatch --parsable -q debug --clusters=cori -n 24 -C knl,quad,cache /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp
    # Get return code
    returncode=$?
    # Exit with return code
    exit $returncode
    ──────────────────────────────────────────── hello_world_openmp/ce755367-4155-4721-adfd-2bd2aad36f46 ────────────────────────────────────────────
    Executor: cori.slurm.knl_debug
    Description: Hello World OpenMP scaling example with processor count
    State: PASS
    Returncode: 0
    Runtime: 32.010719 sec
    Starttime: 2022/06/30 14:39:12
    Endtime: 2022/06/30 14:39:44
    Command: bash --norc --noprofile -eo pipefail hello_world_openmp_build.sh
    Test Script:
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/ce755367/hello_world_openmp.sh
    Build Script:
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/ce755367/hello_world_openmp_build.sh
    Output File:
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/ce755367/hello_world_openmp.out
    Error File:
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/ce755367/hello_world_openmp.err
    Log File: /global/u1/s/siddiq90/gitrepos/buildtest/var/logs/buildtest_ptr4xf10.log
    ─ Output File: /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/ce755367/hello_world_op… ─
    Hello World... from thread = 0
    Hello World... from thread = 3
    Hello World... from thread = 4
    Hello World... from thread = 6
    Hello World... from thread = 5
    Hello World... from thread = 1
    Hello World... from thread = 2
    Hello World... from thread = 7

    ─ Test File: /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/ce755367/hello_world_open… ─
    #!/bin/bash
    #SBATCH -t 10
    #SBATCH --job-name=hello_world_openmp
    #SBATCH --output=hello_world_openmp.out
    #SBATCH --error=hello_world_openmp.err


    # name of executable
    _EXEC=hello.c.exe
    export OMP_NUM_THREADS="$BUILDTEST_NUMPROCS"
    # Loading modules
    module load PrgEnv-intel/6.0.5
    # Compilation Line
    cc -qopenmp -o $_EXEC /global/u1/s/siddiq90/gitrepos/buildtest-nersc/buildspecs/apps/openmp/src/hello.c


    # Run executable
    ./$_EXEC


    ─ Test File: /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/ce755367/hello_world_open… ─
    #!/bin/bash
    export BUILDTEST_TEST_NAME=hello_world_openmp
    export BUILDTEST_TEST_ROOT=/global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/ce755367
    export BUILDTEST_BUILDSPEC_DIR=/global/u1/s/siddiq90/gitrepos/buildtest-nersc/buildspecs/apps/openmp
    export BUILDTEST_STAGE_DIR=/global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_scale/hello_world_openmp/ce755367/stage
    export BUILDTEST_NUMPROCS=8
    # source executor startup script
    source /global/u1/s/siddiq90/gitrepos/buildtest/var/executor/cori.slurm.knl_debug/before_script.sh
    # Run generated script
    sbatch --parsable -q debug --clusters=cori -n 8 -C knl,quad,cache /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/openmp_
    # Get return code
    returncode=$?
    # Exit with return code
    exit $returncode

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

    $ buildtest inspect query -o -t create_burst_buffer
    ─────────────────────────────────────────── create_burst_buffer/2bc01707-c910-4091-ab9c-b14e5f6d56e5 ────────────────────────────────────────────
    Executor: cori.slurm.knl_debug
    Description: Create a burst buffer
    State: PASS
    Returncode: 0
    Runtime: 120.848841 sec
    Starttime: 2022/06/30 14:46:45
    Endtime: 2022/06/30 14:48:46
    Command: bash --norc --noprofile -eo pipefail create_burst_buffer_build.sh
    Test Script:
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/create_buffer/create_burst_buffer/2bc01707/create_burst_buffer.sh
    Build Script:
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/create_buffer/create_burst_buffer/2bc01707/create_burst_buffer_build.sh
    Output File:
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/create_buffer/create_burst_buffer/2bc01707/create_burst_buffer.out
    Error File:
    /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/create_buffer/create_burst_buffer/2bc01707/create_burst_buffer.err
    Log File: /global/u1/s/siddiq90/gitrepos/buildtest/var/logs/buildtest_yw8xatj8.log
    ─ Output File: /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/create_buffer/create_burst_buffer/2bc01707/create_burst… ─
    /var/opt/cray/dws/mounts/batch/databuffer_60681470_striped_scratch
    total 5.0G
    -rw-rw-r-- 1 siddiq90 siddiq90 5.0G Jun 30 14:46 random.txt

    ─ Test File: /global/u1/s/siddiq90/gitrepos/buildtest/var/tests/cori.slurm.knl_debug/create_buffer/create_burst_buffer/2bc01707/create_burst_b… ─
    #!/bin/bash
    #SBATCH -N 1
    #SBATCH -t 5
    #SBATCH -n 1
    #SBATCH --job-name=create_burst_buffer
    #SBATCH --output=create_burst_buffer.out
    #SBATCH --error=create_burst_buffer.err
    ####### START OF BURST BUFFER DIRECTIVES #######
    #BB create_persistent name=databuffer capacity=10GB access_mode=striped type=scratch
    ####### END OF BURST BUFFER DIRECTIVES   #######
    ####### START OF DATAWARP DIRECTIVES #######
    #DW persistentdw name=databuffer
    ####### END OF DATAWARP DIRECTIVES   #######
    # Content of run section
    cd $DW_PERSISTENT_STRIPED_databuffer
    pwd
    dd if=/dev/urandom of=random.txt bs=1G count=5 iflag=fullblock
    ls -lh $DW_PERSISTENT_STRIPED_databuffer/

