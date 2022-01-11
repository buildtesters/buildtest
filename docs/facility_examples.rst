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
test to run against every gcc, intel and PrgEnv-cray compiler module.

This test is available at https://github.com/buildtesters/buildtest-cori/blob/devel/buildspecs/apps/openmp/reduction.yml

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

You can find this test at https://github.com/buildtesters/buildtest-cori/blob/devel/buildspecs/apps/mpi/laplace_mpi.yml