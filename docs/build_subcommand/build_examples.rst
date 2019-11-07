Build Examples
===============

.. _mpi_example:

MPI Example
------------

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

OpenACC Example
----------------

Building an OpenACC code is pretty simple. If you have a GNU compiler that supports OpenACC, you will need to use
the ``-fopenacc`` flag. Shown below we have a test configuration to build the program **vecAdd.c** which is a
vector Addition calcuation using OpenACC.

.. program-output:: cat scripts/build_subcommand/tutorial.openacc.vecAdd.c.yml

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

.. program-output:: cat scripts/build-openacc-example.txt

The executable can be run on the GPU or CPU. Shown below, we run the test script locally::

    $ /tmp/ssi29/buildtest/tests/Intel/Haswell/x86_64/rhel/7.6/build_9/vecAdd.c.yml.0xbd4b1809.sh
    Restoring modules from user's GCC
    final result: 1.000000


Building Test for Scheduler
----------------------------

buildtest supports creation of job scripts for LSF and SLURM scheduler which can be used to submit jobs to scheduler.

LSF Job Example
----------------

To enable the LSF mode ``scheduler: LSF`` must be set in the test configuration.

Let's see an example configuration for LSF job

.. program-output:: cat ../toolkit/suite/compilers/helloworld/hello_lsf.yml

By setting ``scheduler: LSF`` this enables the ``bsub`` key that is responsible for adding the **#BSUB** directive in
the test script. Shown below is an example build for LSF job.

.. program-output:: cat scripts/build-lsf-example.txt

The ``bsub`` keys are mapped to the #BSUB options which makes it easy to associate #BSUB options to the ``bsub`` dictionary.


You can run ``buildtest show -k singlesource`` to see description of all keys or refer to  :ref:`show_keys` for list of all keys.

Submitting Jobs to LSF
-----------------------

.. Note:: This is an experimental feature

buildtest provides a wrapper to **bsub** command that allows buildtest to submit jobs to scheduler.
This can be achieved by using ``buildtest build bsub`` command. Shown below are the list of options available
with bsub.

.. program-output:: cat docgen/buildtest_build_bsub_-h.txt

To see the bsub command without submitting to scheduler use the ``--dry-run`` option. buildtest will
require a **build ID** in order to submit job. buildtest will use the build ID to fetch the test script
that will be submitted to LSF.

Here are a few examples.

1. Submitting a job to **admin** queue with **10 minute** walltime, requesting **50M** of memory
and job name is **testjob** for build **ID=0**::

    $ buildtest build bsub -q admin -W 00:10 -M 50M -J testjob 0 --dry-run
    bsub -q admin -M 50M -J testjob -W 00:10 < /tmp/ssi29/buildtest/tests/Intel/Haswell/x86_64/rhel/7.6/build_0/args.c.yml.0xe93836d1.sh

2. Submitting a job to **admin** queue with 2 tasks on resource of **type=X86_64**::

    $ buildtest build bsub -q admin -n 2 -R "type==X86_64"  2
    bsub -q admin -n 2 -R type==X86_64 < /tmp/ssi29/buildtest/tests/Intel/Haswell/x86_64/rhel/7.6/build_2/args.c.yml.0x722fa01.sh
    Job <54218287> is submitted to queue <admin>.
    Submitting Job: /tmp/ssi29/buildtest/tests/Intel/Haswell/x86_64/rhel/7.6/build_2/args.c.yml.0x722fa01.sh to scheduler

Options to bsub wrapper in buildtest are of type string which are passed in directly to ``bsub`` command.
This was intended to leverage bsub syntax as users are accustomed to without reinventing a new
syntax language. For example, ``bsub -R`` has a very complex syntax requirement that requires a
string format to process the information.


SLURM Job Example
------------------

To enable SLURM mode set ``scheduler: SLURM`` in the test configuration.

See example below:

.. program-output:: cat ../toolkit/suite/compilers/helloworld/hello_slurm.yml

The ``scheduler: SLURM`` will enable ``sbatch`` key that is used for adding **#SBATCH** directive in test script.
Also note that ``CXXFLAGS:`` will be used for passing options to C++ compiler (g++)

.. program-output:: cat scripts/build-slurm-example.txt