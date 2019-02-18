.. _Suite:

Test Suite
===========

Test suite is a collection of yaml files and source code grouped in a directory of
similar types of test.

Currently, there is 3 test suites **compilers**, **cuda**, **openmp**. The test suites
can be found at https://github.com/HPC-buildtest/buildtest-configs/tree/master/buildtest/suite

Hello World C++
----------------

Let's take a look at a hello world C++ example that will be compiled with gcc

.. program-output:: cat scripts/build_subcommand/suite/hello_gnu.yml

The first line ``testblock: singlesource`` inform buildtest that this is a single source
compilation and buildtest will use the appropriate Class to build this test. Currently,
``testblock`` only supports singlesource at this moment.

The second line ``test:`` indicate this is the start of a test region where you will specify the test
configuration.

The third line ``source: hello.cpp`` is the source file, this file will need to reside in **src** directory
wherever you have your yml file.

The fourth line ``flags: -O3`` will insert the build flag **-O3** during compilation

The fifth line ``compiler: gnu`` is to indicate we will use the gnu compiler during compilation.

The sixth line ``module:`` is a list of **module loads** you want in your test that is
lower case and it specifies the name of the module without the version. In this case,
we only specify one module ``gcc`` and buildtest will load this module if found in ``BUILDTEST_MODULE_ROOT``.

Next let's see the generated test script

.. program-output:: cat scripts/build_subcommand/suite/hello_gnu.yml.sh

Couple things to note.

- buildtest will purge and load the module that is found in your system in this case it will load ``module load GCC``
- The test script will be named with the yml file and the appropriate shell extension ``.sh``, ``.bash``, ``.csh``.
- buildtest will ``cd`` into the test directory where test script is found
- buildtest will detect the compiler based on extension type specified in ``source`` tag. In this case it will be ``g++`` since we specified  ``compiler: gnu``
- buildtest will compile the source file that was defined in ``source`` tag. buildtest will figure out the full path to file.
- The name of the executable will be the name of the source code with ``.exe`` extension.
- Finally buildtest will run executable and remove it upon completion.

This test is found in ``compilers`` suite. So you can run this via

::

    buildtest build -S compilers

Shown below is the output

.. program-output:: cat scripts/build_subcommand/suite/build_compilers.txt

To run the compiler test suite you can run

::

    buildtest run -S compilers

Below is the output of the run

.. program-output:: cat scripts/build_subcommand/suite/run_compilers.txt

All test will be run and the output will be stored in the ``.run`` file which contains
output of test run along with additional details buildtest was able to capture for your site.

OpenMP Example
---------------

Let's take a look at a OpenMP yml example for computing vector dot product

.. program-output:: cat scripts/build_subcommand/suite/omp_dotprod.c.yml

To run a OpenMP example you typically set the environment variable ``OMP_NUM_THREADS``
to declare number of threads during execution.

This can be configured used ``vars:`` keyword that takes a list of of key-value to set
environment variable in the test script. In this example we set ``OMP_NUM_THREADS=2``

To specify flags to linker ``(ld)`` then use key ``ldflags``. In this case, to compile
openmp with gnu compiler you need to specify ``-fopenmp``.

Let's see the test script

.. program-output:: cat scripts/build_subcommand/suite/omp_dotprod.c.yml.sh

Let's build  ``openmp`` test suite by running the following

::

    buildtest build -S openmp

.. program-output:: cat scripts/build_subcommand/suite/build_openmp.txt

Next let's run the test by running

::

    buildtest run -S openmp


.. program-output:: cat scripts/build_subcommand/suite/run_openmp.txt     
