Build Examples
===============

.. _mpi_example:

MPI Example
------------

.. Note:: This is an experimental feature

buildtest supports building MPI test. To demonstrate see the following test configuration.
For the example below, ``${BUILDTEST_ROOT}`` refers to where you cloned the build test
repository. There is a folder of examples provided here under ``toolkit/suite/tutorial``.

.. command-output:: cat ${BUILDTEST_ROOT}/toolkit/suite/tutorial/mpi/hello.c.yml
   :shell:

To enable mpi test, you must specify ``mpi: True`` in the test configuration. The ``mpi`` key is not
a required key, if it is omitted from the test configuration then buildtest will assume mpi is disabled.
By setting ``mpi: True`` enables the **mpi** key in program section.

The mpi key comes with three keys **flavor**, **launcher** and **launcher_opts**. The ``flavor`` key is used to specify the
MPI implementation (``openmpi``, ``mpich``, ``intelmpi``, etc...) which is used to detect the mpi wrapper for compiling
MPI programs. The user must specify the launcher configuration via **launcher** and **launcher_opts** in order to build
the proper run command.

When ``launcher: mpirun`` and ``launcher_opts: -n 2`` is set in configuration this will translate to::

    mpirun -n 2 <executable>

Let's build this test with buildtest. Notice that ``$CC=mpicc`` is automatically detected based on the ``flavor``. We
loaded the OpenMPI module prior to building this test and buildtest injected the active modules into the test script.
The key ``pre_build: mpicc --version`` will run shell command before compilation, likewise the ``post_run: mpirun --version``
will run the shell command after execution of mpi program.

.. program-output:: cat scripts/build-mpi-example.txt

OpenACC Example
----------------

Building an OpenACC code is pretty simple. If you have a GNU compiler that supports OpenACC, you will need to use
the ``-fopenacc`` flag. Shown below we have a test configuration to build the program **vecAdd.c** which is a
vector Addition calcuation using OpenACC.

.. command-output:: cat ${BUILDTEST_ROOT}/toolkit/suite/tutorial/openacc/vecAdd.c.yml
   :shell:

The source file **vecAdd.c** calls the math library (**#include <math.h>**) which needs to be linked at compile time
which can be passed using ``ldflags: -lm``. The ``ldflags`` key will set the variable **$LDFLAGS** in the test script
and append the linker flags to the compilation.

For this build we will use a module collection named **GCC** to build this test. Most standard
linux distribution come with GCC 4.x version, and these version dont support OpenACC so we have to use a newer version
that supports OpenACC compilation.

For this test we use GCC version 8.3.0 that is shown in the GCC user collection::

    $ module describe GCC
    Collection "GCC" contains:
       1) GCCcore/8.3.0    2) zlib/1.2.11-GCCcore-8.3.0    3) binutils/2.32-GCCcore-8.3.0    4) GCC


Notice below, $LDFLAGS is set in the testscript and referenced in the compilation. The ``-fopenacc`` is set for $CFLAGS.

.. program-output:: cat docgen/tutorial.openacc.vecAdd.c.yml.txt

The executable can be run on the GPU or CPU. Shown below, we run the test script locally::

    $ /tmp/ssi29/buildtest/tests/Intel/Haswell/x86_64/rhel/7.6/build_9/vecAdd.c.yml.0xbd4b1809.sh
    Restoring modules from user's GCC
    final result: 1.000000


Intel Example
--------------

In order to build via intel compiler we can set ``compiler:intel`` in the test configuration. Also you must
load the intel module or have it set in your $PATH somehow before you run the build. In this build we perform
a hello world example in Fortran using Intel compiler.

.. command-output:: cat ${BUILDTEST_ROOT}/toolkit/suite/tutorial/compilers/hello.f.yml
   :shell:

In order to compiler Fortran code we must use ``ifort`` which is set as ``$FC=ifort``. Flags to fortran compiler are
passed via ``FFLAGS`` which is set as a shell variable and referenced in the build step.

.. program-output:: cat docgen/tutorial.compilers.hello.f.yml.txt

PGI Example
--------------

buildtest supports PGI compiler, which can be done by setting ``compiler:pgi`` in test configuration.
Shown below is a **vecAdd** OpenACC example compiled with PGI compiler.


.. command-output:: cat ${BUILDTEST_ROOT}/toolkit/suite/tutorial/openacc/vecAdd.c_pgi.yml
   :shell:

For this build we specify ``-acc`` in order to build the code for the accelerator device. In addition this code
requires linking with math library so ``ldflags: -lm`` will set ``LDFLAGS="-lm"`` in the script and $LDFLAGS will be
referenced during the build step. The example below shows a dry run (``--dry``) for the build.

.. program-output:: cat docgen/tutorial.openacc.vecAdd.c_pgi.yml.txt

To actually build this test you can remove the ``--dry`` run option and consider running this test on a GPU machine,
otherwise the test will run on the CPU by default.

Clang Example
--------------

buildtest support Clang compiler, this can be set when ``compiler:clang`` is set in test configuration.

In this test example, we are building a OpenMP hello world example with Clang compiler using 2 threads.

.. command-output:: cat ${BUILDTEST_ROOT}/toolkit/suite/tutorial/openmp/clang_hello.c.yml
   :shell:

When we build this test, buildtest will detect Clang language detection phase and set ``$CC=clang`` in
the test script. The ``OMP_NUM_THREADS`` defines how many OpenMP threads to use when running the code. Also
recall ``pre_exec: OMP_NUM_THREADS=2`` will inject the command before the executable. This will result in::

   OMP_NUM_THREADS=2 $EXECUTABLE

This type of execution is one way of defining environment variable at runtime. However the environment ``OMP_NUM_THREADS``
will not persist across sub-shells which can be done if environment was exported (i.e ``export OMP_NUM_THREADS=2``)

See example build below

.. program-output:: cat docgen/tutorial.openmp.clang_hello.c.yml.txt

