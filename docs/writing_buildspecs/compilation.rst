Compilation Example
====================

Hello World Example
--------------------

In this section, we will show to compile source code with compiler and compiler flags. To get started,
let's start with a simple hello world example we have available in C and C++ as shown below

.. literalinclude:: ../tutorials/compilation/hello.c
   :language: c

.. literalinclude:: ../tutorials/compilation/hello.cpp
   :language: c++

Shown below is an example buildspec file that will compile the above source code with the gcc compiler.
The ``compilers`` section is used to specify the compiler to use that is selected via the ``name`` property which applies
a regular expression to search for compiler. The compilers are defined in buildtest configuration file see :ref:`compilers`
for more details.

.. literalinclude:: ../tutorials/compilation/hello_world_compilation.yml
   :language: yaml
   :emphasize-lines: 6-7, 9-10

Buildtest will define environment variables like ``BUILDTEST_CC`` and ``BUILDTEST_CXX`` that point to the C and C++
compiler wrapper for the selected compiler.

Let's try to run the code and inspect the test output and test file.

.. dropdown:: ``buildtest build -b tutorials/compilation/hello_world_compilation.yml``

    .. command-output:: buildtest build -b tutorials/compilation/hello_world_compilation.yml

    .. command-output:: buildtest inspect query -o -t hello_world_c_cpp

Please note that the compiler definition for ``builtin_gcc`` is a canonical name to reference to system GNU
compiler that is set to **/usr/bin/gcc**, **/usr/bin/g++**. The compiler details can be extracted from the configuration
file via ``buildtest config compilers list`` command. Shown below is the YAML output of the compiler details.

.. command-output:: buildtest config compilers list --yaml

STREAM Benchmark Example
------------------------

In this next section, we will run the `STREAM <https://www.cs.virginia.edu/stream/>`_ memory benchmark. In order to run this example,
we will need to download the source code and compile the source code. We will use the ``curl`` command to download the source code. The
``default`` section is used to specify default compiler settings for compiler, this may include compiler options and environment variables.
The `cflags` option is responsible for setting C compiler flags which is set to environment variable ``BUILDTEST_CFLAGS`` that we can access in
the ``run`` section. The ``env`` section is used to set environment variables that are used in the ``run`` section.

.. literalinclude:: ../tutorials/compilation/stream.yml
   :language: yaml
   :emphasize-lines: 9-13,16

.. dropdown:: ``buildtest build -b tutorials/compilation/stream.yml``

    .. command-output:: buildtest build -b tutorials/compilation/stream.yml

    .. command-output:: buildtest inspect query -o -t stream_openmp_c