Compilation Example
==================

Hello World Example
-------------------

In this section, we will show to compile source code with compiler and compiler flags. To get started,
let's start with a simple hello world example we have available in C and C++ as shown below

.. literalinclude:: ../../tutorials/compilation/hello_world.c
   :language: c
   :linenos:

.. literalinclude:: ../../tutorials/compilation/hello_world.cpp
   :language: c++
   :linenos:

Shown below is an example buildspec file that will compile the above source code with the gcc compiler.
The ``compilers`` section is used to specify the compiler to use that is selected via the ``name`` property which applies
a regular expression to search for compiler. The compilers are defined in buildtest configuration file see :ref:`compilers`
for more details.

.. literalinclude:: ../../tutorials/compilation/hello_world_buildspec.yml
   :language: yaml
   :linenos:
   :emphasize-lines: 6-7, 9-10

Buildtest will define environment variables like ``BUILDTEST_CC`` and ``BUILDTEST_CXX`` that point to compiler wrapper
for the selected compiler.

Let's try to run the code and inspect the test output and test file.

.. dropdown:: ``buildtest build -b tutorials/compilation_examples/hello_world_buildspec.yml``

    .. command-output:: buildtest build -b tutorials/compilation_examples/hello_world_buildspec.yml

    .. command-output:: buildtest inspect query -o -t hello_world_c_cpp

STREAM Benchmark Example
------------------------

In this next section, we will run the `STREAM <https://www.cs.virginia.edu/stream/>`_ memory benchmark. In order to run this example,
we will need to download the source code and compile the source code. We will use the ``curl`` command to download the source code. The
``default`` section is used to specify default compiler settings for compiler, this may include compiler options and environment variables.
The `cflags` option is responsible for setting C compiler flags which is set to environment variable ``BUILDTEST_CFLAGS`` that we can access in
the ``run`` section. The ``env`` section is used to set environment variables that are used in the ``run`` section.

.. literalinclude:: ../../tutorials/compilation/stream.yml
   :language: c
   :linenos:
   :emphasize-lines: 9-13,16

.. dropdown:: ``buildtest build -b tutorials/compilation_examples/stream.yml``

    .. command-output:: buildtest build -b tutorials/compilation_examples/stream.yml

    .. command-output:: buildtest inspect query -t stream_openmp_c