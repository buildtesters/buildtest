Building a MPI Test
====================

To build an mpi program use the ``mpi:`` section in test configuration to define
mpi configuration. The mpi section follows up with the mpi launcher, currently buildtest
supports (``mpirun``, ``srun``) followed by options for the respective job launchers.

Simple Example
---------------

In lines 3-5, we are compiling a MPI hello.c program using the mpirun launcher.

.. code-block::
   :linenos:
   :emphasize-lines: 3-5

    source: hello.c
    compiler: gnu
    mpi:
      mpirun:
       n: '2'
    flags: -O2
    maintainer:
    - shahzeb siddiqui shahzebmsiddiqui@gmail.com
    testblock: singlesource

To build this program, load an MPI module before building. For this example, we have loaded
the ``foss/2019a`` toolchain into our module environment. Next we save the modules
into buildtest module collection and list the collection using ``buildtest module collection``
command.

::

    $ ml

    Currently Loaded Modules:
      1) GCCcore/8.2.0                   5) numactl/2.0.12-GCCcore-8.2.0      9) hwloc/1.11.11-GCCcore-8.2.0      13) FFTW/3.3.8-gompi-2019a
      2) zlib/1.2.11-GCCcore-8.2.0       6) XZ/5.2.4-GCCcore-8.2.0           10) OpenMPI/3.1.3-GCC-8.2.0-2.31.1   14) ScaLAPACK/2.0.2-gompi-2019a-OpenBLAS-0.3.5
      3) binutils/2.31.1-GCCcore-8.2.0   7) libxml2/2.9.8-GCCcore-8.2.0      11) OpenBLAS/0.3.5-GCC-8.2.0-2.31.1  15) foss/2019a
      4) GCC/8.2.0-2.31.1                8) libpciaccess/0.14-GCCcore-8.2.0  12) gompi/2019a

    $ buildtest module collection -a
    {
        "collection": [
            [
                "GCCcore/8.2.0",
                "zlib/1.2.11-GCCcore-8.2.0",
                "binutils/2.31.1-GCCcore-8.2.0",
                "GCC/8.2.0-2.31.1",
                "numactl/2.0.12-GCCcore-8.2.0",
                "XZ/5.2.4-GCCcore-8.2.0",
                "libxml2/2.9.8-GCCcore-8.2.0",
                "libpciaccess/0.14-GCCcore-8.2.0",
                "hwloc/1.11.11-GCCcore-8.2.0",
                "OpenMPI/3.1.3-GCC-8.2.0-2.31.1",
                "OpenBLAS/0.3.5-GCC-8.2.0-2.31.1",
                "gompi/2019a",
                "FFTW/3.3.8-gompi-2019a",
                "ScaLAPACK/2.0.2-gompi-2019a-OpenBLAS-0.3.5",
                "foss/2019a"
            ]
        ]
    }

    $ buildtest module collection -l
    0: ['GCCcore/8.2.0', 'zlib/1.2.11-GCCcore-8.2.0', 'binutils/2.31.1-GCCcore-8.2.0', 'GCC/8.2.0-2.31.1', 'numactl/2.0.12-GCCcore-8.2.0', 'XZ/5.2.4-GCCcore-8.2.0', 'libxml2/2.9.8-GCCcore-8.2.0', 'libpciaccess/0.14-GCCcore-8.2.0', 'hwloc/1.11.11-GCCcore-8.2.0', 'OpenMPI/3.1.3-GCC-8.2.0-2.31.1', 'OpenBLAS/0.3.5-GCC-8.2.0-2.31.1', 'gompi/2019a', 'FFTW/3.3.8-gompi-2019a', 'ScaLAPACK/2.0.2-gompi-2019a-OpenBLAS-0.3.5', 'foss/2019a']

Next we build the MPI test using the module collection ``0`` using the option ``-mc 0``

.. program-output:: cat scripts/build-mpi-example1.txt


Running MPI program with srun
------------------------------

If your site has the SLURM batch scheduler, then one should be running their program
via ``srun`` and specify the slurm configuration (i.e ``#SBATCH``) command in test script.

Recall that slurm configuration can be specified via ``slurm:`` key refer to :ref:`show_keys` for yaml keys.

Shown below is a MPI ping test using ``srun`` launcher using 1 node, 2 tasks, and 200M of memory.
The slurm configuration is defined in line 3-6 and mpi configuration is found on line 7-8.

.. code-block::
   :linenos:
   :emphasize-lines: 3-8

    source: mpi_ping.c
    compiler: gnu
    slurm:
      mem: 200M
      ntasks: '2'
      nodes: '1'
    mpi:
      srun: ''

    flags: -O2
    maintainer:
    - shahzeb siddiqui shahzebmsiddiqui@gmail.com
    testblock: singlesource

To build this test, we will use the module collection **0** using option ``-mc 0`` to load
the foss toolchain that is needed to build the program mpi_ping.c. When ``slurm:`` directive
is defined in test configuration, buildtest will use the ``.slurm`` extension when writing test


.. program-output:: cat scripts/build-mpi-example2.txt

