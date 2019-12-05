Build Reference Table
========================

Program Language Detection
----------------------------

Buildtest detects the Program Language based on the file extension of the source
file. The source file being the one specified by ``source:`` key.

Here is a breakdown of  how Program Language is detected based on the various file
extensions

.. csv-table:: Langage Mapping
    :header: "Langage", "File Extension"
    :widths: 20,80

    "c", ".c"
    "c++", ".cc .cxx .cpp .c++ .C"
    "fortran", ".f90 .f95 .f03 .f .F .F90 .FPP .FOR .FTN .for .ftn"
    "cuda", ".cu"

Compiler Detection
--------------------

Once the Programming Language is detected, buildtest can detect the compiler wrapper
by checking the value of ``compiler:`` key. Here is a breakdown of the compiler breakdown
by programming language

.. csv-table:: Compiler Mapping
    :header: "compiler", "language=c", "language=c++", "language=fortran"
    :widths: 20,20,20,20

    "gnu", "gcc", "g++", "gfortran"
    "intel", "icc", "icpc", "ifort"
    "pgi", "pgcc", "pgc++", "pgfortran"
    "clang", "clang", "clang++", "N/A"
    "cuda", "nvcc", "nvcc", "N/A"

MPI Detection
--------------------

Similarly, the MPI wrapper detection is calculated based on Programming Language. In the
test configuration, the key ``mpi:flavor:`` is to tell buildtest which MPI flavor to use
when retrieving the mpi wrapper. Shown below is a table of MPI wrapper based on flavors.


.. csv-table:: MPI Flavor Mapping
    :header: "MPI Flavor", "language=c", "language=c++", "language=fortran"
    :widths: 20,20,20,20

    "openmpi", "mpicc", "mpicxx", "mpif90"
    "intelmpi", "mpiicc", "mpiicpc", "mpiifort"
    "mpich", "mpicc", "mpicxx", "mpif90"


