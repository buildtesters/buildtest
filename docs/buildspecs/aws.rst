.. _buildtest_aws:

Buildtest Tutorial on AWS
=========================

Setup
-----

This section of tutorial will be completed in `Amazon Web Services (AWS) <https://aws.amazon.com/>`_ environment. Once you have access to system,
please :ref:`installing_buildtest` and then proceed to the next section.

Once you are done, please run the following commands to ensure you are using the correct configuration file

.. code-block:: bash

    export BUILDTEST_CONFIGFILE=$BUILDTEST_ROOT/buildtest/settings/aws.yml
    buildtest config path

You can verify the configuration is valid by runnning the following::

    buildtest config validate

If you see no errors, then you are ready to proceed to the next section.

Hello World Compilation
-----------------------

Let's start off with a simple hello world compilation in C using the GNU compiler. We have the following buildspec
that will compile a code source code ``hello.c`` using the ``gcc`` compiler wrapper.

.. literalinclude:: ../../aws_tutorial/hello_world/hello.yml
    :language: yaml
    :emphasize-lines: 7-8

The source code is the following

.. literalinclude:: ../../aws_tutorial/hello_world/hello.c
    :language: c

Let's try building this example and inspect the test results to see what happens.

.. dropdown:: ``buildtest build -b $BUILDTEST_ROOT/aws_tutorial/hello_world/hello.yml``

    .. program-output:: cat aws_examples/hello_build.txt

    .. program-output:: cat aws_examples/hello_inspect.txt

Multi Compiler Test
-------------------

Buildtest supports multiple test creation based on compiler selection using ``compilers`` property. This can be useful to test
a single test with multiple compilers. In this next example, we will attempt to compile the Hello World test in previous example using
2 versions of GNU compiler. The ``name`` property is used to search for compilers in the configuration file. The :ref:`compilers` section
covers in detail how to define compilers in buildtest configuration.

.. literalinclude:: ../../aws_tutorial/hello_world/multi_compiler_hello.yml
    :language: yaml
    :emphasize-lines: 6-7

Let's try building this example, you will see there are now 2 tests created, one for each compiler.

.. dropdown:: ``buildtest build -b $BUILDTEST_ROOT/aws_tutorial/hello_world/multi_compiler_hello.yml``

    .. program-output:: cat aws_examples/multi_compiler_hello_build.txt

    Take note in the generated test output, the variables **BUILDTEST_CC**, **BUILDTEST_CXX** and **BUILDTEST_FC** are using the compiler wrappers
    for each compiler.

    .. program-output:: cat aws_examples/multi_compiler_hello_inspect.txt

We can see the compiler configuration using the command ``buildtest config compilers list --yaml`` which will print the output in YAML format.
Shown below is the compiler declaration

.. program-output:: cat aws_examples/compiler_list_yaml.txt

OpenMP Test with custom compiler configuration
----------------------------------------------

In this next example, we will compile a OpenMP code using GNU compiler and specify custom compiler flags and environment variable. We will
work with a Hello World OpenMP code that uses OpenMP pragma to parallelize the code. The source code is the following

.. literalinclude:: ../../aws_tutorial/openmp_hello.c
    :language: c

In order to build OpenMP code, we need to use ``-fopenmp`` flag to enable OpenMP support. We will set ``OMP_NUM_THREADS`` environment variable
to specify number of OpenMP theads which will differ for each compiler test. We introduce a keyword ``config`` that allows us to specify
customize compiler flags and environment variables. The ``env`` property is used to set environment variable for each compiler test and ``cflags`` is
used to set compiler flags inorder to compile the test. This value is stored in environment **BUILDTEST_CFLAGS** that will be used in ``run`` section
for compiling the source code.

.. literalinclude:: ../../aws_tutorial/openmp_example_custom_compiler.yml
    :language: yaml
    :emphasize-lines: 6-19


Let's try building this example and inspect the test results to see what happens.

.. dropdown:: ``buildtest build -b $BUILDTEST_ROOT/aws_tutorial/openmp_example_custom_compiler.yml``

    .. program-output:: cat aws_examples/openmp_example_build.txt

    We will see in the generated test the values ``OMP_NUM_THREADS`` and ``BUILDTEST_CFLAGS`` are set for each compiler test. The ``OMP_NUM_THREADS``
    will impact the number of threads used to run code therefore we will see different output for each compiler test.

    .. program-output:: cat aws_examples/openmp_example_inspect.txt

Testing a MPI Code
--------------------

This image comes with several MPI flavors such as OpenMPI, mvapich2. In the next example we will run a MPI Proc Name test
on login node that will run with 8 processes. The source code is available in the ``$HOME/examples`` directory as part of the image.

.. literalinclude:: ../../aws_tutorial/mpiproc.yml
    :language: yaml
    :emphasize-lines: 8-9

We can run this test using the following command

.. dropdown:: ``buildtest build -b $BUILDTEST_ROOT/aws_tutorial/mpiproc.yml``

    .. program-output:: cat aws_examples/mpiproc_build.txt

    We can see this test prints Hello World message from each process.

    .. program-output:: cat aws_examples/mpiproc_inspect.txt

MPI Job Submission
------------------

This cluster comes with PBS/Torque scheduler. We can run the MPI test to batch scheduler. Shown below is an example
buildspec. We will use an executor named a torque executor named ``generic.torque.e4spro-cluster`` that is mapped to
a queue named ``e4spro-cluster``. The ``pbs`` property is used to specify PBS directives. We will run this test
on a single node using 2 processors with a wall time of 1hr.

.. literalinclude:: ../../aws_tutorial/mpi_job_submission.yml
    :language: yaml
    :emphasize-lines: 4,6

We can run this test by running the following commands. The ``--pollinterval 10`` will be used to poll job every 10 sec and
retrieve job status. Buildtest will keep polling job until job is complete. The ``--display output --display test`` will show
content of output, error and generated test files during the build phase. You will notice the generated build script (**_build.sh**)
will invoke ``qsub`` command to a generated test.

.. dropdown:: ``buildtest build -b $BUILDTEST_ROOT/aws_tutorial/mpi_job_submission.yml --pollinterval 10 --display output --display test``

    .. program-output:: cat aws_examples/mpi_job_submission_build.txt


OSU Microbenchmark
-------------------

The `OSU Microbenchmark <https://mvapich.cse.ohio-state.edu/benchmarks/>`_ is a collection of MPI-based benchmarks developed at Ohio State University.
This benchmark is used to measure performance of MPI libraries and is a popular benchmark suite for MPI. We will run the ``osu_bw`` test
which measures bandwidth. The test requires we specify 2 processes.

In this next example, we will run 2 tests, the first is simply invoking the ``osu_bw`` test with 2 processes, and the second test will
run the same test and use :ref:`comparison_operators <comparison_operators>` to compare the bandwidth result. The ``metrics`` property is used to
capture performance metrics that can be used for comparison. We will use the :ref:`assert_ge <assert_ge>` status check that
will do a greater than or equal comparison with reference value. The metrics will capture performance results for message length **16384** and
perform a comparison with reference value of 10000. If the test result is greater than or equal to 10000, the test will pass otherwise it will fail.

.. literalinclude:: ../../aws_tutorial/osu_bandwidth_test.yml
    :language: yaml
    :emphasize-lines: 6, 13-24

Let's run the test and see the results.

.. dropdown:: ``buildtest build -b $BUILDTEST_ROOT/aws_tutorial/osu_bandwidth_test.yml``

    .. program-output:: cat aws_examples/osu_bandwidth_test_build.txt

    Take note in the output of the second test, we will see a list of performance metrics captured in table output. If metrics is not captured,
    the value will be undefined.

    .. program-output:: cat aws_examples/osu_bandwidth_test_inspect.txt

Tensorflow Test
---------------

In this next exercise, we provide a tensorflow test in python that train a model and generate a predicition model. We have the following source code

.. literalinclude:: ../../aws_tutorial/tensorflow_model.py
    :language: python

The buildspec for this test is the following, where we run the test using ``python3`` interpreter.

.. literalinclude:: ../../aws_tutorial/tensorflow.yml
    :language: yaml

Please run the test yourself and inspect the output. You will want to run the following commands::

    buildtest build -b $BUILDTEST_ROOT/aws_tutorial/tensorflow.yml
    buildtest inspect query -o run_tensorflow_model

Running Tests in Containers
----------------------------

Buildtest has support for :ref:`running tests in containers <running_tests_containers>` such as ``docker`` and ``singularity``. In this
next examples, we will show how to run a hello world test in ``docker`` and ``singularity`` container. Let's start off with ``docker``, we
introduce a new property ``container`` that allows us to specify the container settings. The ``platform`` and ``image`` are required properties
that specifies the container platform (e.g., docker, singularity, podman) and the image name.

.. literalinclude:: ../tutorials/containers/hello_world.yml
   :language: yaml
   :emphasize-lines: 6-8

Let's run the test and inspect the output, you will notice the test output will print a message from the container. This test will run in a docker container,
if you look at the generated test content you will see a ``docker run`` invocation.

.. dropdown:: ``buildtest build -b $BUILDTEST_ROOT/tutorials/containers/hello_world.yml``

    .. program-output:: cat aws_examples/docker_helloworld_build.txt

    .. program-output:: cat aws_examples/docker_helloworld_inspect.txt

In the next example, we will run the same test in a ``singularity`` container. To do this we will simply change the
``platform`` to ``singularity`` and specify the ``image`` name. Since singularity can pull images from different registries we will specify
``docker:://`` prefix to pull the image from docker hub.

.. literalinclude:: ../tutorials/containers/hello_world_singularity.yml
   :language: yaml
   :emphasize-lines: 6-8

Buildtest will invoke ``singularity run`` and bind mount the stage directory into the container and execute test from the container. Take note that
that singularity will volume mount test into ``/buildtest`` in the container and then run test from that directory.

.. dropdown:: ``buildtest build -b $BUILDTEST_ROOT/tutorials/containers/hello_world_singularity.yml``

    .. program-output:: cat aws_examples/singularity_helloworld_build.txt

    .. program-output:: cat aws_examples/singularity_helloworld_inspect.txt

In this last example, we will run a test using a :ref:`container executor <container_executor>` by defining a custom executor based on a container
image. In all of our previous examples, we were running tests using executor ``generic.local.bash`` which is a generic executor
that runs tests on the local system using ``bash`` shell.

Let's take a look at the executor configuration by running the following command. The ``container`` keyword under ``executors`` section is used
to define container executors. We can specify arbitrary name for the executor and specify the container image and platform.

.. program-output:: cat aws_examples/container_executor_list.txt

We have the following buildspec that will run test using a custom executor ``generic.container.ubuntu``.

.. literalinclude:: ../tutorials/containers/container_executor/ubuntu.yml
   :language: yaml
   :emphasize-lines: 4

Let's run the test and inspect the output. You will notice the test is run in a ubuntu 20.04 container. In the output of ``df -h`` you will
see the filesystem is from the container image with an entry ``/buildtest`` that is bind mounted from the host system.

.. dropdown:: ``buildtest build -b $BUILDTEST_ROOT/tutorials/containers/container_executor/ubuntu.yml``

    .. program-output:: cat aws_examples/container_executor_build.txt

    .. program-output:: cat aws_examples/container_executor_inspect.txt
