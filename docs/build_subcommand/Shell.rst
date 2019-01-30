Shell Types (``buildtest build --shell <shell>``)
====================================================



Currently, buildtest supports the following shell types

- sh (default)
- bash
- csh

To create tests for different shell types use ``buildtest build --shell <shell-type>``.
You may set the environment variable ``BUILDTEST_SHELL`` or set this in your
``config.yaml``


Let's build test for ``CMake/3.9.5-GCCcore-6.4.0`` with ``csh`` support by
running ``buildtest build -s CMake/3.9.5-GCCcore-6.4.0 --shell csh``


.. program-output:: cat scripts/Shell/CMake-3.9.5-GCCcore-6.4.0_csh.txt

Now let's check the test files

.. program-output:: cat scripts/Shell/CMake-3.9.5-GCCcore-6.4.0_csh_listing.txt


Let's rerun this with bash: ``buildtest build -s CMake/3.9.5-GCCcore-6.4.0 --shell bash``


.. program-output:: cat scripts/Shell/CMake-3.9.5-GCCcore-6.4.0_bash.txt

You will notice the test scripts for ``csh`` and ``bash`` are indicated with shell
extension to avoid name conflict.

.. program-output:: cat scripts/Shell/CMake-3.9.5-GCCcore-6.4.0_bash_listing.txt

Let's take a look at the ``CMakeList.txt`` file
which contains the test parameter required to run tests via ``ctest``. Everytime a
test is created it is added in CMakeList.txt if you check the file you will
notice the extension is also configured in CMakeList.txt

.. program-output:: cat scripts/Shell/CMake-3.9.5-GCCcore-6.4.0_CMakelists.txt

Configuring Environment Variable for different shells
-----------------------------------------------------

Let's dive deeper into a OpenMP helloworld example that changes its test output
according to different shells. For instance, we have the following yaml file that
will build OpenMP hello world program using multi-threading.

.. code::

    name: omp_hello.f
    source:  omp_hello.f
    buildopts: -O2 -fopenmp
    environment:
            OMP_NUM_THREADS : 2

You will notice the key ``environment`` will declare the environment variable according to the shell
used for generating the test. For ``bash`` and ``sh`` the keyword ``export`` is used whereas for ``csh``
the keyword is ``setenv``

If you run ``buildtest build -s GCCcore/6.4.0 --shell bash`` to build the following test and look at generated test ``omp_hello_f.bash`` you
will see the environment variable is set using keyword ``export``

.. program-output:: cat scripts/Shell/GCCcore-6.4.0_omp_hello.f.bash



If you compare this with ``csh`` test script for ``omp_hello_f``  the only difference will be the lines responsible for setting environment
variable ``OMP_NUM_THREADS``

.. program-output:: cat scripts/Shell/GCCcore-6.4.0_omp_hello.f.csh


.. Note:: Notice that ``environment`` doesn't specify whether to use **export** or **setenv** but rather
    keeps configuration generic and buildtest will figure out what keyword to append in front depending
    on the shell type.
