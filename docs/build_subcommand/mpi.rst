Building a MPI Test
====================

.. Note:: This is an experimental feature

buildtest supports building MPI test. To demonstrate see the following test configuration

.. program-output:: cat scripts/build_subcommand/mpi.hello.hello.c.yml

To enable mpi test, you must specify ``mpi: True`` in the test configuration. The ``mpi`` key is not
a required key, if it is omitted from the test configuration then buildtest will assume mpi is disabled.
By setting ``mpi: True`` enables the **mpi** key in program section.

The mpi key comes with three keys **flavor**, **launcher** and **launcher_opts**. The ``flavor*`` key is used to specify the
MPI implementation (``openmpi``, ``mpich``, ``intelmpi``, ``mvapich2``, etc...) Currently, not implemented, buildtest
can use the flavor key to detect the mpi launcher based on MPI flavor. At the moment, user must specify the *launcher*
and *launcher_opts* in order to build the proper run command. The ``launcher: mpirun`` with ``launcher_opts: -n 2``
will create a run command such as::

    mpirun -n 2 <executable>

Let's build this test with buildtest. Notice that ``$CC=mpicc`` is automatically detected based on the ``flavor``. We
loaded the OpenMPI module prior to building this test and buildtest injected the active modules into the test script.
The key ``pre_build: mpicc --version`` will run shell command before compilation, likewise the ``post_run: mpirun --version``
will run the shell command after execution of mpi program.

.. program-output:: cat scripts/build-mpi-example.txt

