.. _Suite:

Test Suite
===========

Test suite is a collection of yaml files and source code grouped in a directory of
similar types of test.

Currently, there is 3 test suites **compilers**, **cuda**, **openmp**. The test suites
can be found at https://github.com/HPC-buildtest/buildtest-framework/tree/master/toolkit/buildtest/suite

Hello World C++
----------------

Let's take a look at a hello world C++ example that will be compiled with gcc

.. program-output:: cat scripts/configuration/hello_gnu.yml

The first line ``compiler: gnu`` is to indicate we will use the gnu compiler
during compilation.

The ``flags: -O3`` will insert the build flag **-O3** during compilation

The key ``maintainer`` is a list of maintainers that are primary
contact for the test & configuration file

The key ``source: hello.cpp`` is the source file, this file will need to
reside in **src** directory wherever you have your yml file

Finally, ``testblock: singlesource`` inform buildtest that this
is a single source compilation and buildtest will use the appropriate Class to
build this test. Currently, ``testblock`` only supports singlesource at this moment.



Next let's see the generated test script

.. program-output:: cat scripts/tests/hello_gnu.yml.sh

Couple things to note.

- buildtest will purge and load the module that is active in your shell
- The test script will be named with the yml file and the appropriate shell extension ``.sh``, ``.bash``, ``.csh``.
- buildtest will ``cd`` into the test directory where test script is found
- buildtest will detect the compiler based on extension type specified in ``source`` tag. In this case it will be ``g++`` since we specified  ``compiler: gnu``
- buildtest will compile the source file that was defined in ``source`` tag. buildtest will figure out the full path to file.
- The name of the executable will be the name of the source code with ``.exe`` extension.
- Finally buildtest will run executable and remove it upon completion.

This test is found in ``compilers`` suite and you can build the test suite
by running ``buildtest build -S compilers``


Shown below is the output

.. program-output:: cat scripts/build-compilers-suite.txt

To run the compiler test suite you can run ``buildtest run -S compilers``

Below is the output of the run

.. program-output:: cat scripts/run-compilers-suite.txt

All test will be run and the output will be stored in the ``.run`` file which contains
output of test run along with additional details buildtest was able to capture for your site.

OpenMP Example
---------------

Let's take a look at a OpenMP yml example for computing vector dot product

.. program-output:: cat scripts/configuration/omp_dotprod.c.yml

To run a OpenMP example you typically set the environment variable ``OMP_NUM_THREADS``
to declare number of threads during execution.

This can be configured used ``vars:`` keyword that takes a list of of key-value to set
environment variable in the test script. In this example we set ``OMP_NUM_THREADS=2``

To specify flags to linker ``(ld)`` then use key ``ldflags``. In this case, to compile
openmp with gnu compiler you need to specify ``-fopenmp``.

Let's see the test script

.. program-output:: cat scripts/tests/omp_dotprod.c.yml.sh

Let's build  ``openmp`` test suite by running the following ``buildtest
build -S openmp``

.. program-output:: cat scripts/build-openmp-suite.txt

Next let's run the test suite by running ``buildtest run -S openmp``

.. program-output:: cat scripts/run-openmp-suite.txt

.. _Testing_With_Modules:

Testing with modules
--------------------

Now that we have built a couple test, we want to leverage modules to test
a particular test with different modules. This may be particularly useful if
you have some test that you want to compare with different compilers, MPI,
etc...

Let's take the same hello world example and build it with different gcc
compilers.

Recall the first test was the following

.. program-output:: cat scripts/tests/hello_gnu.yml.sh

In buildtest, just load the modules of interest before you build the test and
it will insert all the modules in  the test script.

For this example we have the following modules loaded

::

    $ ml

    Currently Loaded Modules:
      1) eb/2018   2) GCCcore/6.4.0   3) binutils/2.28-GCCcore-6.4.0   4) GCC/6.4.0-2.28

Let's rebuild the test and notice how the modules are loaded in the test


.. code-block:: console
    :linenos:
    :emphasize-lines: 19-23

    $ buildtest build -c $BUILDTEST_ROOT/toolkit/buildtest/suite/compilers/helloworld/hello_gnu.yml -vv
    ________________________________________________________________________________
    compiler: gnu
    flags: -O3
    maintainer:
    - shahzeb siddiqui shahzebmsiddiqui@gmail.com
    source: hello.cpp
    testblock: singlesource

    ________________________________________________________________________________
    Key Check PASSED for file /home/siddis14/buildtest-framework/toolkit/buildtest/suite/compilers/helloworld/hello_gnu.yml
    Source File /home/siddis14/buildtest-framework/toolkit/buildtest/suite/compilers/helloworld/src/hello.cpp exists!
    Programming Language Detected: c++
    Compiler Check Passed
    Writing Test: /home/siddis14/buildtest/suite/compilers/helloworld/hello_gnu.yml.sh
    Changing permission to 755 for test: /home/siddis14/buildtest/suite/compilers/helloworld/hello_gnu.yml.sh
    ________________________________________________________________________________
    #!/bin/sh
    module purge
    module load eb/2018
    module load GCCcore/6.4.0
    module load binutils/2.28-GCCcore-6.4.0
    module load GCC/6.4.0-2.28
    cd /home/siddis14/buildtest/suite/compilers/helloworld
    g++ -O3 -o hello.cpp.exe /home/siddis14/buildtest-framework/toolkit/buildtest/suite/compilers/helloworld/src/hello.cpp
    ./hello.cpp.exe
    rm ./hello.cpp.exe
    ________________________________________________________________________________


buildtest will run ``module purge`` and load all the active modules by
running ``module -t list`` and insert each module in a separate line. This
gives user freedom to load whatever module they want when creating test, though
this puts responsibility on user to understand the testscript.

