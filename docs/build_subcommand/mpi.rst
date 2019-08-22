Building a MPI Test
====================

To build an mpi program use the ``mpi:`` section in test configuration to define
the start of mpi configuration.

Simple Example
---------------

In lines 3-5, we are compiling a MPI hello.c program using the OpenMPI
implementation.

.. code-block::
   :linenos:
   :emphasize-lines: 3-5

    source: hello.c
    compiler: gnu
    mpi:
      openmpi:
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

.. program-output:: cat scripts/build-openmpi-example1.txt

Notice, buildtest is using ``orterun`` as the job launcher when writing the
test script which is the job launcher for OpenMPI.

Running MPI with MPICH
-----------------------

If you want to build MPI program using MPICH, then make use of ``mpich`` key
that hints buildtest to make use of ``mpiexec.hydra`` as the job launcher for
running MPI jobs. In example below, we have same program (hello.c) that is
built with MPICH


.. code-block::
   :linenos:
   :emphasize-lines: 3-5

    source: hello.c
    compiler: gnu
    mpi:
      mpich:
       n: '2'
    flags: -O2
    maintainer:
    - shahzeb siddiqui shahzebmsiddiqui@gmail.com
    testblock: singlesource

For this test, we are using ``gmpich/2017.08`` toolchain that consist of
``MPICH/3.2.1-GCC-7.2.0-2.29`` and its deps built using easybuild. This module
is added to module collection as index **1**.

::

    $ buildtest module collection -l
    0: ['GCCcore/8.2.0', 'zlib/1.2.11-GCCcore-8.2.0', 'binutils/2.31.1-GCCcore-8.2.0', 'GCC/8.2.0-2.31.1', 'numactl/2.0.12-GCCcore-8.2.0', 'XZ/5.2.4-GCCcore-8.2.0', 'libxml2/2.9.8-GCCcore-8.2.0', 'libpciaccess/0.14-GCCcore-8.2.0', 'hwloc/1.11.11-GCCcore-8.2.0', 'OpenMPI/3.1.3-GCC-8.2.0-2.31.1', 'OpenBLAS/0.3.5-GCC-8.2.0-2.31.1', 'gompi/2019a', 'FFTW/3.3.8-gompi-2019a', 'ScaLAPACK/2.0.2-gompi-2019a-OpenBLAS-0.3.5', 'foss/2019a']
    1: ['GCCcore/7.2.0', 'zlib/1.2.11-GCCcore-7.2.0', 'binutils/2.29-GCCcore-7.2.0', 'GCC/7.2.0-2.29', 'MPICH/3.2.1-GCC-7.2.0-2.29', 'gmpich/2017.08']

To build this test use the ``-mc 1`` to load the MPICH module into test script.

.. program-output:: cat scripts/build-mpich-example1.txt

Notice ``mpiexec.hydra`` is being invoked on the executable ``hello.c.exe``.

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


.. program-output:: cat scripts/build-srun-example1.txt


MPI Example with Binding and Process Mapping
---------------------------------------------

To retrieve bindings for launched process and mapped located of each process,
then one can use the ``--report-bindings`` and ``--display-map`` option that
is part of ``orterun``. In buildtest this can be set using the
``report-bindings`` and ``display-map`` keys. Since this is an optional
argument, we set value to an empty string.


.. code-block::
   :linenos:
   :emphasize-lines: 7-8

    source: mpi_mm.f
    compiler: gnu
    mpi:
      openmpi:
        n: '2'
        npernode: '2'
        report-bindings: ''
        display-map: ''
    flags: -O2


    maintainer:
    - shahzeb siddiqui shahzebmsiddiqui@gmail.com
    testblock: singlesource


Next we will build this test using collection ``0`` (**foss/2019a**).

.. program-output:: cat scripts/build-openmpi-example2.txt

Notice the options ``--report-bindings`` and ``--display-map`` are added to
the ``orterun`` command. If we run this test manually we will see the process
mapping at start of execution::


    $ sh /tmp/ec2-user/buildtest/tests/suite/mpi/matrixmux/mm_mpi.f.yml.sh
     Data for JOB [15602,1] offset 0 Total slots allocated 2

     ========================   JOB MAP   ========================

     Data for node: buildtest       Num slots: 2    Max slots: 0    Num procs: 2
            Process OMPI jobid: [15602,1] App: 0 Process rank: 0 Bound: socket 0[core 0[hwt 0]]:[B/.]
            Process OMPI jobid: [15602,1] App: 0 Process rank: 1 Bound: socket 0[core 1[hwt 0]]:[./B]

     =============================================================
    [buildtest:17659] MCW rank 0 bound to socket 0[core 0[hwt 0]]: [B/.]
    [buildtest:17659] MCW rank 1 bound to socket 0[core 1[hwt 0]]: [./B]
     task ID=            0
        sending           7  cols to task           1
     task ID=            1
          0.00   1015.00   2030.00   3045.00   4060.00   5075.00   6090.00
          0.00   1120.00   2240.00   3360.00   4480.00   5600.00   6720.00
          0.00   1225.00   2450.00   3675.00   4900.00   6125.00   7350.00
          0.00   1330.00   2660.00   3990.00   5320.00   6650.00   7980.00
          0.00   1435.00   2870.00   4305.00   5740.00   7175.00   8610.00
