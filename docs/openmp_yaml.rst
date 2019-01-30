.. _OpenMP_yaml:

Building OpenMP program with YAML configuration
===============================================

.. contents::
   :backlinks: none


OpenMP YAML example
-------------------

.. program-output:: cat scripts/OpenMP_yaml/omp_getEnvInfo.c.yaml

This OpenMP test example can be build for GCC software as follows

::

   buildtest build -s GCCcore/6.4.0 --shell csh

This will generate the following script

.. program-output:: cat scripts/OpenMP_yaml/omp_getEnvInfo.csh

buildtest can generate a range of tests for parameterizing OMP_NUM_THREADS by
using threadrange keyword. This can be useful for viewing performance of application
by varying thread count.


Matrix Multiplication with OpenMP Parameterization
--------------------------------------------------

For instance we have a matrix multiplication example we want to build with buildtest for varying parameters, we can do that as follows.

Let's create a YAML file with the content

.. program-output:: cat scripts/OpenMP_yaml/omp_mm.c.yaml

This will generate the following test scripts.


.. program-output:: cat scripts/OpenMP_yaml/omp_mm_listing.txt


buildtest will generate the same test script with different values of OMP_NUM_THREAD before running the program.

.. program-output:: cat scripts/OpenMP_yaml/omp_mm.c_nthread_2.csh


.. _example: https://github.com/HPC-buildtest/buildtest-configs/blob/devel/ebapps/GCC/code/omp_mm.c
