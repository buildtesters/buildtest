.. _MPI_yaml:

Building MPI programs with YAML configuration
=============================================


.. contents::
   :backlinks: none


MPI YAML example
----------------

Below is an example of building a matrix multiplication example_ in C with OpenMPI 2.0.0,  GCC-5.4.0-2.27 with 4 processes

**MPI YAML script**

.. program-output:: cat scripts/MPI_yaml/mpi_mm_c.yaml

**MPI testscript generated from YAML**

.. program-output:: cat scripts/MPI_yaml/mpi_mm_c.sh



Parameterize MPI Procs example
------------------------------


If you want to build your MPI test program with different process count then you can use **procrange** key in YAML. buidltest will 
generate multiple test scripts with varying arguments to **-np <proc>**. In buildtest we achieve this by creating the first test script, read
it and loop over **procrange** by interval  and create other test script by modifying the mpi launcher line.

To illustrate this example, lets look at a helloworld MPI program that has the following YAML file.

.. program-output:: cat scripts/MPI_yaml/hello_arg.c.yaml

This will generate a list of hello world program

.. program-output:: cat scripts/MPI_yaml/hello_arg_c_listing.txt


The MPI helloworld for 2 process will have **-np 2**. The file name has the word **_nproc_<proc>** where <proc> is the MPI process used in this test. 

.. program-output:: cat scripts/MPI_yaml/hello_arg.c_nproc_2.sh

.. _example: https://github.com/HPC-buildtest/buildtest-configs/blob/master/mpi/code/mpi_mm.c

