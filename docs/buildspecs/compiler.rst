.. _compiler_schema:

Compiler Schema
=================

The compiler schema is used for compilation of programs, currently we support
single source file compilation. In order to use the compiler schema you must set ``type: compiler`` in your
sub-schema. See `compiler schema docs <https://buildtesters.github.io/buildtest/pages/schemadocs/compiler-v1.html>`_


Setup
-------

In order to complete this part of the tutorial you will need `docker` installed on your machine which you can get
by `installing docker <https://docs.docker.com/get-docker/>`_.

To get started we will pull a docker container and start interactive shell.

.. code-block:: console

    $ docker pull ecpe4s/ubuntu20.04-runner-x86_64:2021-10-01
    $ docker run -it -v $BUILDTEST_ROOT:/tmp ecpe4s/ubuntu20.04-runner-x86_64:2021-10-01 bash

.. note::

    All commands below are run inside the container

Inside the docker container you will need to install buildtest. We have bind mount our host directory **$BUILDTEST_ROOT** to
`/tmp` in container. To get started we must navigate to ``/tmp`` and install buildtest


.. code-block:: console

    $ cd /tmp
    $ source setup.sh
    Installing buildtest dependencies
    BUILDTEST_ROOT: /tmp
    buildtest command: /tmp/bin/buildtest

For these examples we will use a custom configuration file for this container. Please set the environment `BUILDTEST_CONFIGFILE` to the
following configuration file.

.. code-block:: console

    $ export BUILDTEST_CONFIGFILE=$BUILDTEST_ROOT/buildtest/settings/e4s_container_config.yml

Let's confirm the configuration is valid by using ``buildtest config validate``. Buildtest will read the configuration
file pointed by ``BUILDTEST_CONFIGFILE`` instead of passing configuration file via command line or copying to **$HOME/.buildtest/config.yml**.

.. code-block:: console

    $ buildtest config validate
    /tmp/buildtest/settings/e4s_container_config.yml is valid

Compilation Examples
----------------------

We assume the reader has basic understanding of :ref:`global_schema`
validation. Shown below is the schema header definition for `compiler-v1.0.schema.json <https://github.com/buildtesters/buildtest/blob/devel/buildtest/schemas/compiler-v1.0.schema.json>`_:

.. literalinclude:: ../../buildtest/schemas/compiler-v1.0.schema.json
   :language: json
   :lines: 1-12

The required fields for compiler schema are **type**, **compilers**, **source**
and **executor**.

Shown below is a test name ``hello_f`` that compiles Fortran code with GNU compiler.

.. literalinclude:: ../tutorials/compilers/gnu_hello_fortran.yml
   :language: yaml

The ``source`` property is used to specify input program for
compilation, this can be a file relative to buildspec file or an absolute path.
In this example the source file ``src/hello.f90`` is relative to buildspec file.
The ``compilers`` section specifies compiler configuration, the ``name``
field is required property which is used to search compilers based on regular expression.
In this example we use the **builtin_gcc** compiler as regular expression which is the system
gcc compiler provided by buildtest. The ``default`` section specifies default compiler
configuration applicable to a specific compiler group.

Shown below is an example build for the buildspec example

.. code-block:: console

    $ buildtest build -b tutorials/compilers/gnu_hello_fortran.yml
    ╭──────────────────────────────────── buildtest summary ────────────────────────────────────╮
    │                                                                                           │
    │ User:               root                                                                  │
    │ Hostname:           ec1164c68c64                                                          │
    │ Platform:           Linux                                                                 │
    │ Current Time:       2021/10/13 12:05:32                                                   │
    │ buildtest path:     /tmp/bin/buildtest                                                    │
    │ buildtest version:  0.11.0                                                                │
    │ python path:        /usr/bin/python                                                       │
    │ python version:     3.8.10                                                                │
    │ Configuration File: /tmp/buildtest/settings/e4s_container_config.yml                      │
    │ Test Directory:     /tmp/var/tests                                                        │
    │ Command:            /tmp/bin/buildtest build -b tutorials/compilers/gnu_hello_fortran.yml │
    │                                                                                           │
    ╰───────────────────────────────────────────────────────────────────────────────────────────╯
    ────────────────────────────────────────────────────────────────────────────────  Discovering Buildspecs ────────────────────────────────────────────────────────────────────────────────
    Discovered Buildspecs:  1
    Excluded Buildspecs:  0
    Detected Buildspecs after exclusion:  1
                  Discovered buildspecs
    ╔════════════════════════════════════════════════╗
    ║ Buildspecs                                     ║
    ╟────────────────────────────────────────────────╢
    ║ /tmp/tutorials/compilers/gnu_hello_fortran.yml ║
    ╚════════════════════════════════════════════════╝
    ────────────────────────────────────────────────────────────────────────────────── Parsing Buildspecs ───────────────────────────────────────────────────────────────────────────────────
    Valid Buildspecs: 1
    Invalid Buildspecs: 0
    /tmp/tutorials/compilers/gnu_hello_fortran.yml: VALID


    Total builder objects created: 1


                                                          Builder Details
    ┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Builder          ┃ Executor           ┃ description                     ┃ buildspecs                                     ┃
    ┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ hello_f/6cbeda04 │ generic.local.bash │ Hello World Fortran Compilation │ /tmp/tutorials/compilers/gnu_hello_fortran.yml │
    └──────────────────┴────────────────────┴─────────────────────────────────┴────────────────────────────────────────────────┘
    ───────────────────────────────────────────────────────────────────────────────────── Building Test ─────────────────────────────────────────────────────────────────────────────────────
    [12:05:32] hello_f/6cbeda04: Creating test directory - /tmp/var/tests/generic.local.bash/gnu_hello_fortran/hello_f/6cbeda04                                                   base.py:440
               hello_f/6cbeda04: Creating stage directory - /tmp/var/tests/generic.local.bash/gnu_hello_fortran/hello_f/6cbeda04/stage                                            base.py:450
               hello_f/6cbeda04: Writing build script: /tmp/var/tests/generic.local.bash/gnu_hello_fortran/hello_f/6cbeda04/hello_f_build.sh                                      base.py:567
    ───────────────────────────────────────────────────────────────────────────────────── Running Tests ─────────────────────────────────────────────────────────────────────────────────────
    ______________________________
    Launching test: hello_f/6cbeda04
    hello_f/6cbeda04: Running Test script /tmp/var/tests/generic.local.bash/gnu_hello_fortran/hello_f/6cbeda04/hello_f_build.sh
    hello_f/6cbeda04: completed with returncode: 0
    hello_f/6cbeda04: Writing output file -  /tmp/var/tests/generic.local.bash/gnu_hello_fortran/hello_f/6cbeda04/hello_f.out
    hello_f/6cbeda04: Writing error file - /tmp/var/tests/generic.local.bash/gnu_hello_fortran/hello_f/6cbeda04/hello_f.err
                                                     Test Summary
    ┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━┓
    ┃ Builder          ┃ executor           ┃ status ┃ Checks (ReturnCode, Regex, Runtime) ┃ ReturnCode ┃ Runtime ┃
    ┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━┩
    │ hello_f/6cbeda04 │ generic.local.bash │ PASS   │ N/A N/A N/A                         │ 0          │ 0.40491 │
    └──────────────────┴────────────────────┴────────┴─────────────────────────────────────┴────────────┴─────────┘



    Passed Tests: 1/1 Percentage: 100.000%
    Failed Tests: 0/1 Percentage: 0.000%


    Writing Logfile to: /tmp/buildtest_xqglkm0j.log
    A copy of logfile can be found at $BUILDTEST_ROOT/buildtest.log -  /tmp/buildtest.log

The generated test for test name **hello_f** is the following:

.. code-block:: shell

    $ cat $(buildtest path -t hello_f/d686b23d)
    #!/usr/bin/bash


    # name of executable
    _EXEC=hello.f90.exe
    # Compilation Line
    gfortran -Wall -o $_EXEC /tmp/tutorials/compilers/src/hello.f90


    # Run executable
    ./$_EXEC


buildtest will use compiler wrappers specified in your settings
to build the test, however these values can be overridden in buildspec file which
will be discussed later.

You can see the compiler declaration from our configuration file by running ``buildtest config compilers -y``
which will display output in YAML format. Note that for each compiler instance one can define name of compiler
and path to ``cc``, ``fc``, ``cxx`` wrapper.

.. code-block:: console

    $ buildtest config compilers -y
    gcc:
      builtin_gcc:
        cc: /usr/bin/gcc
        cxx: /usr/bin/g++
        fc: /usr/bin/gfortran
      gcc_11.2.0:
        cc: /bootstrap/view/bin/gcc
        cxx: /bootstrap/view/bin/g++
        fc: /bootstrap/view/bin/gfortran

buildtest will detect the file extension of source file to detect programming language
and generate the appropriate C, C++, or Fortran compilation line based on language detected.
In this example, buildtest detects a **.f90** file extension and determines this is a Fortran program.

Shown below is the file extension table buildtest uses for determining the programming
language.

.. csv-table:: File Extension Language Mapping
    :header: "Language", "File Extension"
    :widths: 30, 80

    "**C**", ".c"
    "**C++**", ".cc .cxx .cpp .c++"
    "**Fortran**", ".f90 .F90 .f95 .f .F .FOR .for .FTN .ftn"

Compiler Selection
---------------------

buildtest selects compiler based on ``name`` property which is a list of regular expression
applied for available compilers defined in buildtest configuration. In this next example, we will
compile an OpenACC code that will compute vector addition. For this test we will use ``gcc_11.2.0`` compiler
instance specified in the **name** property

.. literalinclude:: ../tutorials/compilers/vecadd.yml
   :language: yaml

We expect buildtest to select the ``gcc_11.2.0`` compiler based on our regular expression.

.. code-block:: console

    $ buildtest build -b tutorials/compilers/vecadd.yml
    ╭────────────────────────────── buildtest summary ───────────────────────────────╮
    │                                                                                │
    │ User:               root                                                       │
    │ Hostname:           ec1164c68c64                                               │
    │ Platform:           Linux                                                      │
    │ Current Time:       2021/10/13 13:15:10                                        │
    │ buildtest path:     /tmp/bin/buildtest                                         │
    │ buildtest version:  0.11.0                                                     │
    │ python path:        /usr/bin/python                                            │
    │ python version:     3.8.10                                                     │
    │ Configuration File: /tmp/buildtest/settings/e4s_container_config.yml           │
    │ Test Directory:     /tmp/var/tests                                             │
    │ Command:            /tmp/bin/buildtest build -b tutorials/compilers/vecadd.yml │
    │                                                                                │
    ╰────────────────────────────────────────────────────────────────────────────────╯
    ────────────────────────────────────────────────────────────────────────────────  Discovering Buildspecs ────────────────────────────────────────────────────────────────────────────────
    Discovered Buildspecs:  1
    Excluded Buildspecs:  0
    Detected Buildspecs after exclusion:  1
             Discovered buildspecs
    ╔═════════════════════════════════════╗
    ║ Buildspecs                          ║
    ╟─────────────────────────────────────╢
    ║ /tmp/tutorials/compilers/vecadd.yml ║
    ╚═════════════════════════════════════╝
    ────────────────────────────────────────────────────────────────────────────────── Parsing Buildspecs ───────────────────────────────────────────────────────────────────────────────────
    Valid Buildspecs: 1
    Invalid Buildspecs: 0
    /tmp/tutorials/compilers/vecadd.yml: VALID


    Total builder objects created: 1


                                                           Builder Details
    ┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Builder             ┃ Executor           ┃ description                               ┃ buildspecs                          ┃
    ┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ vecadd_gnu/3125c7bf │ generic.local.bash │ Vector Addition example with GNU compiler │ /tmp/tutorials/compilers/vecadd.yml │
    └─────────────────────┴────────────────────┴───────────────────────────────────────────┴─────────────────────────────────────┘
    ───────────────────────────────────────────────────────────────────────────────────── Building Test ─────────────────────────────────────────────────────────────────────────────────────
    [13:15:10] vecadd_gnu/3125c7bf: Creating test directory - /tmp/var/tests/generic.local.bash/vecadd/vecadd_gnu/3125c7bf                                                        base.py:440
               vecadd_gnu/3125c7bf: Creating stage directory - /tmp/var/tests/generic.local.bash/vecadd/vecadd_gnu/3125c7bf/stage                                                 base.py:450
               vecadd_gnu/3125c7bf: Writing build script: /tmp/var/tests/generic.local.bash/vecadd/vecadd_gnu/3125c7bf/vecadd_gnu_build.sh                                        base.py:567
    ───────────────────────────────────────────────────────────────────────────────────── Running Tests ─────────────────────────────────────────────────────────────────────────────────────
    ______________________________
    Launching test: vecadd_gnu/3125c7bf
    vecadd_gnu/3125c7bf: Running Test script /tmp/var/tests/generic.local.bash/vecadd/vecadd_gnu/3125c7bf/vecadd_gnu_build.sh
    vecadd_gnu/3125c7bf: completed with returncode: 0
    vecadd_gnu/3125c7bf: Writing output file -  /tmp/var/tests/generic.local.bash/vecadd/vecadd_gnu/3125c7bf/vecadd_gnu.out
    vecadd_gnu/3125c7bf: Writing error file - /tmp/var/tests/generic.local.bash/vecadd/vecadd_gnu/3125c7bf/vecadd_gnu.err
                                                       Test Summary
    ┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┓
    ┃ Builder             ┃ executor           ┃ status ┃ Checks (ReturnCode, Regex, Runtime) ┃ ReturnCode ┃ Runtime  ┃
    ┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━┩
    │ vecadd_gnu/3125c7bf │ generic.local.bash │ PASS   │ N/A N/A N/A                         │ 0          │ 0.271582 │
    └─────────────────────┴────────────────────┴────────┴─────────────────────────────────────┴────────────┴──────────┘



    Passed Tests: 1/1 Percentage: 100.000%
    Failed Tests: 0/1 Percentage: 0.000%


    Writing Logfile to: /tmp/buildtest_0pfzll80.log
    A copy of logfile can be found at $BUILDTEST_ROOT/buildtest.log -  /tmp/buildtest.log

In this next example we will see how one can select multiple compiler instance and specify custom compiler
options for each compiler instance. This example is a simple Hello World in C using **builtin_gcc** and
**gcc_11.2.0** compiler since we have defined the regular expression ``name: ["^(builtin_gcc|gcc)"]``.


.. literalinclude:: ../tutorials/compilers/gnu_hello_c.yml
    :language: yaml

Next we run this test, and we get two tests for test name **hello_c** for each compiler.

.. code-block:: console

    $ buildtest build -b tutorials/compilers/gnu_hello_c.yml
    ╭───────────────────────────────── buildtest summary ─────────────────────────────────╮
    │                                                                                     │
    │ User:               root                                                            │
    │ Hostname:           ec1164c68c64                                                    │
    │ Platform:           Linux                                                           │
    │ Current Time:       2021/10/13 13:17:31                                             │
    │ buildtest path:     /tmp/bin/buildtest                                              │
    │ buildtest version:  0.11.0                                                          │
    │ python path:        /usr/bin/python                                                 │
    │ python version:     3.8.10                                                          │
    │ Configuration File: /tmp/buildtest/settings/e4s_container_config.yml                │
    │ Test Directory:     /tmp/var/tests                                                  │
    │ Command:            /tmp/bin/buildtest build -b tutorials/compilers/gnu_hello_c.yml │
    │                                                                                     │
    ╰─────────────────────────────────────────────────────────────────────────────────────╯
    ────────────────────────────────────────────────────────────────────────────────  Discovering Buildspecs ────────────────────────────────────────────────────────────────────────────────
    Discovered Buildspecs:  1
    Excluded Buildspecs:  0
    Detected Buildspecs after exclusion:  1
               Discovered buildspecs
    ╔══════════════════════════════════════════╗
    ║ Buildspecs                               ║
    ╟──────────────────────────────────────────╢
    ║ /tmp/tutorials/compilers/gnu_hello_c.yml ║
    ╚══════════════════════════════════════════╝
    ────────────────────────────────────────────────────────────────────────────────── Parsing Buildspecs ───────────────────────────────────────────────────────────────────────────────────
    Valid Buildspecs: 1
    Invalid Buildspecs: 0
    /tmp/tutorials/compilers/gnu_hello_c.yml: VALID


    Total builder objects created: 2


                                                    Builder Details
    ┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Builder          ┃ Executor           ┃ description               ┃ buildspecs                               ┃
    ┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ hello_c/f3bb0e93 │ generic.local.bash │ Hello World C Compilation │ /tmp/tutorials/compilers/gnu_hello_c.yml │
    ├──────────────────┼────────────────────┼───────────────────────────┼──────────────────────────────────────────┤
    │ hello_c/65f96c7c │ generic.local.bash │ Hello World C Compilation │ /tmp/tutorials/compilers/gnu_hello_c.yml │
    └──────────────────┴────────────────────┴───────────────────────────┴──────────────────────────────────────────┘
    ───────────────────────────────────────────────────────────────────────────────────── Building Test ─────────────────────────────────────────────────────────────────────────────────────
    [13:17:31] hello_c/f3bb0e93: Creating test directory - /tmp/var/tests/generic.local.bash/gnu_hello_c/hello_c/f3bb0e93                                                         base.py:440
               hello_c/f3bb0e93: Creating stage directory - /tmp/var/tests/generic.local.bash/gnu_hello_c/hello_c/f3bb0e93/stage                                                  base.py:450
               hello_c/f3bb0e93: Writing build script: /tmp/var/tests/generic.local.bash/gnu_hello_c/hello_c/f3bb0e93/hello_c_build.sh                                            base.py:567
               hello_c/65f96c7c: Creating test directory - /tmp/var/tests/generic.local.bash/gnu_hello_c/hello_c/65f96c7c                                                         base.py:440
               hello_c/65f96c7c: Creating stage directory - /tmp/var/tests/generic.local.bash/gnu_hello_c/hello_c/65f96c7c/stage                                                  base.py:450
    [13:17:32] hello_c/65f96c7c: Writing build script: /tmp/var/tests/generic.local.bash/gnu_hello_c/hello_c/65f96c7c/hello_c_build.sh                                            base.py:567
    ───────────────────────────────────────────────────────────────────────────────────── Running Tests ─────────────────────────────────────────────────────────────────────────────────────
    ______________________________
    Launching test: hello_c/f3bb0e93
    hello_c/f3bb0e93: Running Test script /tmp/var/tests/generic.local.bash/gnu_hello_c/hello_c/f3bb0e93/hello_c_build.sh
    ______________________________
    Launching test: hello_c/65f96c7c
    hello_c/65f96c7c: Running Test script /tmp/var/tests/generic.local.bash/gnu_hello_c/hello_c/65f96c7c/hello_c_build.sh
    hello_c/65f96c7c: completed with returncode: 0
    hello_c/65f96c7c: Writing output file -  /tmp/var/tests/generic.local.bash/gnu_hello_c/hello_c/65f96c7c/hello_c.out
    hello_c/65f96c7c: Writing error file - /tmp/var/tests/generic.local.bash/gnu_hello_c/hello_c/65f96c7c/hello_c.err
    hello_c/f3bb0e93: completed with returncode: 0
    hello_c/f3bb0e93: Writing output file -  /tmp/var/tests/generic.local.bash/gnu_hello_c/hello_c/f3bb0e93/hello_c.out
    hello_c/f3bb0e93: Writing error file - /tmp/var/tests/generic.local.bash/gnu_hello_c/hello_c/f3bb0e93/hello_c.err
                                                      Test Summary
    ┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┓
    ┃ Builder          ┃ executor           ┃ status ┃ Checks (ReturnCode, Regex, Runtime) ┃ ReturnCode ┃ Runtime  ┃
    ┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━┩
    │ hello_c/65f96c7c │ generic.local.bash │ PASS   │ N/A N/A N/A                         │ 0          │ 0.195124 │
    ├──────────────────┼────────────────────┼────────┼─────────────────────────────────────┼────────────┼──────────┤
    │ hello_c/f3bb0e93 │ generic.local.bash │ PASS   │ N/A N/A N/A                         │ 0          │ 0.313136 │
    └──────────────────┴────────────────────┴────────┴─────────────────────────────────────┴────────────┴──────────┘



    Passed Tests: 2/2 Percentage: 100.000%
    Failed Tests: 0/2 Percentage: 0.000%


    Writing Logfile to: /tmp/buildtest_dmdm8zga.log
    A copy of logfile can be found at $BUILDTEST_ROOT/buildtest.log -  /tmp/buildtest.log

If we inspect the following test, we see the compiler flags are associated with the compiler. The test below
is for `gcc_11.2.0` which use the flag ``-O2`` compiler flag.

.. code-block:: shell
    :emphasize-lines: 8

    $ cat $(buildtest path -t hello_c/65f96c7c)
    #!/usr/bin/bash


    # name of executable
    _EXEC=hello.c.exe
    # Compilation Line
    /bootstrap/view/bin/gcc -O2 -o $_EXEC /tmp/tutorials/compilers/src/hello.c


    # Run executable
    ./$_EXEC

The system compiler will use `-O1` for its compiler flag since this was defined in `default` section which will apply
compiler options for all *gcc* compilers. Alternately, you may specify compiler setting under ``config`` property which
is applied per compiler instance.

.. code-block:: console
    :emphasize-lines: 8

    $ cat $(buildtest path -t hello_c/f3bb0e93)
    #!/usr/bin/bash


    # name of executable
    _EXEC=hello.c.exe
    # Compilation Line
    /usr/bin/gcc -O1 -o $_EXEC /tmp/tutorials/compilers/src/hello.c


    # Run executable
    ./$_EXEC

Excluding Compilers
--------------------

The ``exclude`` property is part of compilers section which allows one to exclude compilers
upon discovery by ``name`` field. The exclude property is a list of compiler names that
will be removed from test generation which is done prior to build phase. buildtest will exclude
any compilers specified in ``exclude`` if they were found based on regular
expression in ``name`` field. In this example we have selected both `gcc_11.2.0` and `builtin_gcc` compiler
according to regular expression however we will exclude **builtin_gcc** which is configured using
``exclude: [builtin_gcc]``.

.. literalinclude:: ../tutorials/compilers/compiler_exclude.yml
    :language: yaml

Now if we run this test, we will notice that there is only one build for this test even though we selected
both compilers.

.. code-block:: console

    $ buildtest build -b tutorials/compilers/compiler_exclude.yml
    ╭─────────────────────────────────── buildtest summary ────────────────────────────────────╮
    │                                                                                          │
    │ User:               root                                                                 │
    │ Hostname:           ec1164c68c64                                                         │
    │ Platform:           Linux                                                                │
    │ Current Time:       2021/10/13 13:45:53                                                  │
    │ buildtest path:     /tmp/bin/buildtest                                                   │
    │ buildtest version:  0.11.0                                                               │
    │ python path:        /usr/bin/python                                                      │
    │ python version:     3.8.10                                                               │
    │ Configuration File: /tmp/buildtest/settings/e4s_container_config.yml                     │
    │ Test Directory:     /tmp/var/tests                                                       │
    │ Command:            /tmp/bin/buildtest build -b tutorials/compilers/compiler_exclude.yml │
    │                                                                                          │
    ╰──────────────────────────────────────────────────────────────────────────────────────────╯
    ───────────────────────────────────────────────────────────────────────────────  Discovering Buildspecs ────────────────────────────────────────────────────────────────────────────────
    Discovered Buildspecs:  1
    Excluded Buildspecs:  0
    Detected Buildspecs after exclusion:  1
                  Discovered buildspecs
    ╔═══════════════════════════════════════════════╗
    ║ Buildspecs                                    ║
    ╟───────────────────────────────────────────────╢
    ║ /tmp/tutorials/compilers/compiler_exclude.yml ║
    ╚═══════════════════════════════════════════════╝
    ────────────────────────────────────────────────────────────────────────────────── Parsing Buildspecs ──────────────────────────────────────────────────────────────────────────────────
    Excluding compiler: builtin_gcc from test generation
    Valid Buildspecs: 1
    Invalid Buildspecs: 0
    /tmp/tutorials/compilers/compiler_exclude.yml: VALID


    Total builder objects created: 1


                                                                                Builder Details
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Builder                     ┃ Executor           ┃ description                                                       ┃ buildspecs                                    ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ vecadd_gnu_exclude/908ffe39 │ generic.local.bash │ Vector Addition example with GNU compilers but exclude gcc@10.2.0 │ /tmp/tutorials/compilers/compiler_exclude.yml │
    └─────────────────────────────┴────────────────────┴───────────────────────────────────────────────────────────────────┴───────────────────────────────────────────────┘
    ──────────────────────────────────────────────────────────────────────────────────── Building Test ─────────────────────────────────────────────────────────────────────────────────────
    [13:45:53] vecadd_gnu_exclude/908ffe39: Creating test directory - /tmp/var/tests/generic.local.bash/compiler_exclude/vecadd_gnu_exclude/908ffe39                             base.py:440
               vecadd_gnu_exclude/908ffe39: Creating stage directory - /tmp/var/tests/generic.local.bash/compiler_exclude/vecadd_gnu_exclude/908ffe39/stage                      base.py:450
               vecadd_gnu_exclude/908ffe39: Writing build script: /tmp/var/tests/generic.local.bash/compiler_exclude/vecadd_gnu_exclude/908ffe39/vecadd_gnu_exclude_build.sh     base.py:567
    ──────────────────────────────────────────────────────────────────────────────────── Running Tests ─────────────────────────────────────────────────────────────────────────────────────
    ______________________________
    Launching test: vecadd_gnu_exclude/908ffe39
    vecadd_gnu_exclude/908ffe39: Running Test script /tmp/var/tests/generic.local.bash/compiler_exclude/vecadd_gnu_exclude/908ffe39/vecadd_gnu_exclude_build.sh
    vecadd_gnu_exclude/908ffe39: completed with returncode: 0
    vecadd_gnu_exclude/908ffe39: Writing output file -  /tmp/var/tests/generic.local.bash/compiler_exclude/vecadd_gnu_exclude/908ffe39/vecadd_gnu_exclude.out
    vecadd_gnu_exclude/908ffe39: Writing error file - /tmp/var/tests/generic.local.bash/compiler_exclude/vecadd_gnu_exclude/908ffe39/vecadd_gnu_exclude.err
                                                           Test Summary
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┓
    ┃ Builder                     ┃ executor           ┃ status ┃ Checks (ReturnCode, Regex, Runtime) ┃ ReturnCode ┃ Runtime  ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━┩
    │ vecadd_gnu_exclude/908ffe39 │ generic.local.bash │ PASS   │ N/A N/A N/A                         │ 0          │ 0.179337 │
    └─────────────────────────────┴────────────────────┴────────┴─────────────────────────────────────┴────────────┴──────────┘



    Passed Tests: 1/1 Percentage: 100.000%
    Failed Tests: 0/1 Percentage: 0.000%


    Writing Logfile to: /tmp/buildtest_itked2qb.log
    A copy of logfile can be found at $BUILDTEST_ROOT/buildtest.log -  /tmp/buildtest.log

Setting environment variables
------------------------------

Environment variables can be set using ``env`` property which is a list of
key/value pair to assign environment variables. This property can be used in ``default`` or ``config``
section within a compiler instance. In this next example we have an OpenMP Hello World example in C
where we define environment variable `OMP_NUM_THREADS` which controls number of OpenMP
threads to use when running program. In this example we use 2 threads for all gcc
compiler group but we have set ``gcc_11.2.0`` to use 4 threads

.. literalinclude:: ../tutorials/compilers/openmp_hello.yml
    :language: yaml

Next let's build this test.

.. code-block:: console

    $ buildtest build -b tutorials/compilers/envvar_override.yml
    ╭─────────────────────────────────── buildtest summary ───────────────────────────────────╮
    │                                                                                         │
    │ User:               root                                                                │
    │ Hostname:           ec1164c68c64                                                        │
    │ Platform:           Linux                                                               │
    │ Current Time:       2021/10/13 14:50:50                                                 │
    │ buildtest path:     /tmp/bin/buildtest                                                  │
    │ buildtest version:  0.11.0                                                              │
    │ python path:        /usr/bin/python                                                     │
    │ python version:     3.8.10                                                              │
    │ Configuration File: /tmp/buildtest/settings/e4s_container_config.yml                    │
    │ Test Directory:     /tmp/var/tests                                                      │
    │ Command:            /tmp/bin/buildtest build -b tutorials/compilers/envvar_override.yml │
    │                                                                                         │
    ╰─────────────────────────────────────────────────────────────────────────────────────────╯
    ───────────────────────────────────────────────────────────────────────────────  Discovering Buildspecs ────────────────────────────────────────────────────────────────────────────────
    Discovered Buildspecs:  1
    Excluded Buildspecs:  0
    Detected Buildspecs after exclusion:  1
                 Discovered buildspecs
    ╔══════════════════════════════════════════════╗
    ║ Buildspecs                                   ║
    ╟──────────────────────────────────────────────╢
    ║ /tmp/tutorials/compilers/envvar_override.yml ║
    ╚══════════════════════════════════════════════╝
    ────────────────────────────────────────────────────────────────────────────────── Parsing Buildspecs ──────────────────────────────────────────────────────────────────────────────────
    Valid Buildspecs: 1
    Invalid Buildspecs: 0
    /tmp/tutorials/compilers/envvar_override.yml: VALID


    Total builder objects created: 2


                                                                     Builder Details
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Builder                           ┃ Executor           ┃ description                            ┃ buildspecs                                   ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ override_environmentvars/0f373822 │ generic.local.bash │ override default environment variables │ /tmp/tutorials/compilers/envvar_override.yml │
    ├───────────────────────────────────┼────────────────────┼────────────────────────────────────────┼──────────────────────────────────────────────┤
    │ override_environmentvars/fdbd68af │ generic.local.bash │ override default environment variables │ /tmp/tutorials/compilers/envvar_override.yml │
    └───────────────────────────────────┴────────────────────┴────────────────────────────────────────┴──────────────────────────────────────────────┘
    ──────────────────────────────────────────────────────────────────────────────────── Building Test ─────────────────────────────────────────────────────────────────────────────────────
    [14:50:50] override_environmentvars/0f373822: Creating test directory - /tmp/var/tests/generic.local.bash/envvar_override/override_environmentvars/0f373822                  base.py:440
               override_environmentvars/0f373822: Creating stage directory - /tmp/var/tests/generic.local.bash/envvar_override/override_environmentvars/0f373822/stage           base.py:450
    [14:50:51] override_environmentvars/0f373822: Writing build script:                                                                                                          base.py:567
               /tmp/var/tests/generic.local.bash/envvar_override/override_environmentvars/0f373822/override_environmentvars_build.sh
               override_environmentvars/fdbd68af: Creating test directory - /tmp/var/tests/generic.local.bash/envvar_override/override_environmentvars/fdbd68af                  base.py:440
               override_environmentvars/fdbd68af: Creating stage directory - /tmp/var/tests/generic.local.bash/envvar_override/override_environmentvars/fdbd68af/stage           base.py:450
               override_environmentvars/fdbd68af: Writing build script:                                                                                                          base.py:567
               /tmp/var/tests/generic.local.bash/envvar_override/override_environmentvars/fdbd68af/override_environmentvars_build.sh
    ──────────────────────────────────────────────────────────────────────────────────── Running Tests ─────────────────────────────────────────────────────────────────────────────────────
    ______________________________
    Launching test: override_environmentvars/0f373822
    override_environmentvars/0f373822: Running Test script /tmp/var/tests/generic.local.bash/envvar_override/override_environmentvars/0f373822/override_environmentvars_build.sh
    ______________________________
    Launching test: override_environmentvars/fdbd68af
    override_environmentvars/fdbd68af: Running Test script /tmp/var/tests/generic.local.bash/envvar_override/override_environmentvars/fdbd68af/override_environmentvars_build.sh
    override_environmentvars/fdbd68af: completed with returncode: 0
    override_environmentvars/0f373822: completed with returncode: 0
    override_environmentvars/fdbd68af: Writing output file -  /tmp/var/tests/generic.local.bash/envvar_override/override_environmentvars/fdbd68af/override_environmentvars.out
    override_environmentvars/fdbd68af: Writing error file - /tmp/var/tests/generic.local.bash/envvar_override/override_environmentvars/fdbd68af/override_environmentvars.err
    override_environmentvars/0f373822: Writing output file -  /tmp/var/tests/generic.local.bash/envvar_override/override_environmentvars/0f373822/override_environmentvars.out
    override_environmentvars/0f373822: Writing error file - /tmp/var/tests/generic.local.bash/envvar_override/override_environmentvars/0f373822/override_environmentvars.err
                                                              Test Summary
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┓
    ┃ Builder                           ┃ executor           ┃ status ┃ Checks (ReturnCode, Regex, Runtime) ┃ ReturnCode ┃ Runtime  ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━┩
    │ override_environmentvars/fdbd68af │ generic.local.bash │ PASS   │ N/A N/A N/A                         │ 0          │ 0.259626 │
    ├───────────────────────────────────┼────────────────────┼────────┼─────────────────────────────────────┼────────────┼──────────┤
    │ override_environmentvars/0f373822 │ generic.local.bash │ PASS   │ N/A N/A N/A                         │ 0          │ 0.276015 │
    └───────────────────────────────────┴────────────────────┴────────┴─────────────────────────────────────┴────────────┴──────────┘



    Passed Tests: 2/2 Percentage: 100.000%
    Failed Tests: 0/2 Percentage: 0.000%


    Writing Logfile to: /tmp/buildtest_dn_8ofyn.log
    A copy of logfile can be found at $BUILDTEST_ROOT/buildtest.log -  /tmp/buildtest.log

We can see the generated test using ``buildtest inspect query`` which can show output of multiple tests. In example below we see the two test runs
and take note of ``export OMP_NUM_THREADS`` defined per test. The ``-d all`` will fetch all records for test name **override_environmentvars** and
``-t`` will fetch the test script.

.. code-block:: console

    $ buildtest inspect query -d all -t override_environmentvars
    ──────────────────────────────────────────────────────────── override_environmentvars/fdbd68af-5ade-4489-a9de-173ca05d9e36 ─────────────────────────────────────────────────────────────
    executor:  generic.local.bash
    description:  override default environment variables
    state:  PASS
    returncode:  0
    runtime:  0.259626
    starttime:  2021/10/13 14:50:51
    endtime:  2021/10/13 14:50:51
    ────────────────────────────── Test File: /tmp/var/tests/generic.local.bash/envvar_override/override_environmentvars/fdbd68af/override_environmentvars.sh ──────────────────────────────
       1 #!/usr/bin/bash
       2
       3
       4 # name of executable
       5 _EXEC=hello_omp.c.exe
       6 # Declare environment variables
       7 export OMP_NUM_THREADS=4
       8
       9
      10 # Compilation Line
      11 /bootstrap/view/bin/gcc -fopenmp -o $_EXEC /tmp/tutorials/compilers/src/hello_omp.c
      12
      13
      14 # Run executable
      15 ./$_EXEC
      16
      17
    ──────────────────────────────────────────────────────────── override_environmentvars/0f373822-82be-4069-bc6a-2f9584ea70c1 ─────────────────────────────────────────────────────────────
    executor:  generic.local.bash
    description:  override default environment variables
    state:  PASS
    returncode:  0
    runtime:  0.276015
    starttime:  2021/10/13 14:50:51
    endtime:  2021/10/13 14:50:51
    ────────────────────────────── Test File: /tmp/var/tests/generic.local.bash/envvar_override/override_environmentvars/0f373822/override_environmentvars.sh ──────────────────────────────
       1 #!/usr/bin/bash
       2
       3
       4 # name of executable
       5 _EXEC=hello_omp.c.exe
       6 # Declare environment variables
       7 export OMP_NUM_THREADS=2
       8
       9
      10 # Compilation Line
      11 /usr/bin/gcc -fopenmp -o $_EXEC /tmp/tutorials/compilers/src/hello_omp.c
      12
      13
      14 # Run executable
      15 ./$_EXEC
      16
      17

Tweak how test are passed
--------------------------

The ``status`` property can be used to determine how buildtest will pass the test. By
default, buildtest will use returncode to determine if test ``PASS`` or ``FAIL`` with
exitcode 0 as PASS and anything else is FAIL.

Sometimes, it may be useful check output of test to determine using regular expression. This
can be done via ``status`` property. In this example, we define two tests, the first one defines ``status``
property in the default **gcc** group. This means all compilers that belong to gcc
group will be matched based on returncode.

In second test we override the ``status`` property for a given compiler instance under the ``config`` section.
The test is expected to produce output of ``final result: 1.000000`` but we will specify a different value in order to
show this test will fail.

.. literalinclude:: ../tutorials/compilers/compiler_status_regex.yml
    :language: yaml


If we build this test, we should expect the first test example ``default_status_returncode`` should pass based on
returncode 0. If the returncode doesn't match buildtest will report failure. For the second test example, we have set that
test will pass based on returncode 0 based on ``default`` property however for `gcc_11.2.0` test we have defined a ``status``
property to check based on regular expression. We will expect both tests to fail if run these test.

.. code-block:: console

    $ buildtest build -b tutorials/compilers/compiler_status_regex.yml
    ╭────────────────────────────────────── buildtest summary ──────────────────────────────────────╮
    │                                                                                               │
    │ User:               root                                                                      │
    │ Hostname:           ec1164c68c64                                                              │
    │ Platform:           Linux                                                                     │
    │ Current Time:       2021/10/13 14:05:39                                                       │
    │ buildtest path:     /tmp/bin/buildtest                                                        │
    │ buildtest version:  0.11.0                                                                    │
    │ python path:        /usr/bin/python                                                           │
    │ python version:     3.8.10                                                                    │
    │ Configuration File: /tmp/buildtest/settings/e4s_container_config.yml                          │
    │ Test Directory:     /tmp/var/tests                                                            │
    │ Command:            /tmp/bin/buildtest build -b tutorials/compilers/compiler_status_regex.yml │
    │                                                                                               │
    ╰───────────────────────────────────────────────────────────────────────────────────────────────╯
    ───────────────────────────────────────────────────────────────────────────────  Discovering Buildspecs ────────────────────────────────────────────────────────────────────────────────
    Discovered Buildspecs:  1
    Excluded Buildspecs:  0
    Detected Buildspecs after exclusion:  1
                    Discovered buildspecs
    ╔════════════════════════════════════════════════════╗
    ║ Buildspecs                                         ║
    ╟────────────────────────────────────────────────────╢
    ║ /tmp/tutorials/compilers/compiler_status_regex.yml ║
    ╚════════════════════════════════════════════════════╝
    ────────────────────────────────────────────────────────────────────────────────── Parsing Buildspecs ──────────────────────────────────────────────────────────────────────────────────
    Valid Buildspecs: 1
    Invalid Buildspecs: 0
    /tmp/tutorials/compilers/compiler_status_regex.yml: VALID


    Total builder objects created: 4


                                                                      Builder Details
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Builder                            ┃ Executor           ┃ description                      ┃ buildspecs                                         ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ default_status_returncode/dfee4a1e │ generic.local.bash │ status check based on returncode │ /tmp/tutorials/compilers/compiler_status_regex.yml │
    ├────────────────────────────────────┼────────────────────┼──────────────────────────────────┼────────────────────────────────────────────────────┤
    │ default_status_returncode/6b725310 │ generic.local.bash │ status check based on returncode │ /tmp/tutorials/compilers/compiler_status_regex.yml │
    ├────────────────────────────────────┼────────────────────┼──────────────────────────────────┼────────────────────────────────────────────────────┤
    │ override_status_regex/3e99f85a     │ generic.local.bash │ custom status for gcc_11.2.0     │ /tmp/tutorials/compilers/compiler_status_regex.yml │
    ├────────────────────────────────────┼────────────────────┼──────────────────────────────────┼────────────────────────────────────────────────────┤
    │ override_status_regex/e0d47271     │ generic.local.bash │ custom status for gcc_11.2.0     │ /tmp/tutorials/compilers/compiler_status_regex.yml │
    └────────────────────────────────────┴────────────────────┴──────────────────────────────────┴────────────────────────────────────────────────────┘
    ──────────────────────────────────────────────────────────────────────────────────── Building Test ─────────────────────────────────────────────────────────────────────────────────────
    [14:05:39] default_status_returncode/dfee4a1e: Creating test directory - /tmp/var/tests/generic.local.bash/compiler_status_regex/default_status_returncode/dfee4a1e          base.py:440
               default_status_returncode/dfee4a1e: Creating stage directory - /tmp/var/tests/generic.local.bash/compiler_status_regex/default_status_returncode/dfee4a1e/stage   base.py:450
               default_status_returncode/dfee4a1e: Writing build script:                                                                                                         base.py:567
               /tmp/var/tests/generic.local.bash/compiler_status_regex/default_status_returncode/dfee4a1e/default_status_returncode_build.sh
               default_status_returncode/6b725310: Creating test directory - /tmp/var/tests/generic.local.bash/compiler_status_regex/default_status_returncode/6b725310          base.py:440
               default_status_returncode/6b725310: Creating stage directory - /tmp/var/tests/generic.local.bash/compiler_status_regex/default_status_returncode/6b725310/stage   base.py:450
               default_status_returncode/6b725310: Writing build script:                                                                                                         base.py:567
               /tmp/var/tests/generic.local.bash/compiler_status_regex/default_status_returncode/6b725310/default_status_returncode_build.sh
               override_status_regex/3e99f85a: Creating test directory - /tmp/var/tests/generic.local.bash/compiler_status_regex/override_status_regex/3e99f85a                  base.py:440
               override_status_regex/3e99f85a: Creating stage directory - /tmp/var/tests/generic.local.bash/compiler_status_regex/override_status_regex/3e99f85a/stage           base.py:450
               override_status_regex/3e99f85a: Writing build script:                                                                                                             base.py:567
               /tmp/var/tests/generic.local.bash/compiler_status_regex/override_status_regex/3e99f85a/override_status_regex_build.sh
    [14:05:40] override_status_regex/e0d47271: Creating test directory - /tmp/var/tests/generic.local.bash/compiler_status_regex/override_status_regex/e0d47271                  base.py:440
               override_status_regex/e0d47271: Creating stage directory - /tmp/var/tests/generic.local.bash/compiler_status_regex/override_status_regex/e0d47271/stage           base.py:450
               override_status_regex/e0d47271: Writing build script:                                                                                                             base.py:567
               /tmp/var/tests/generic.local.bash/compiler_status_regex/override_status_regex/e0d47271/override_status_regex_build.sh
    ──────────────────────────────────────────────────────────────────────────────────── Running Tests ─────────────────────────────────────────────────────────────────────────────────────
    ______________________________
    Launching test: default_status_returncode/dfee4a1e
    default_status_returncode/dfee4a1e: Running Test script /tmp/var/tests/generic.local.bash/compiler_status_regex/default_status_returncode/dfee4a1e/default_status_returncode_build.sh
    ______________________________
    Launching test: default_status_returncode/6b725310
    default_status_returncode/6b725310: Running Test script /tmp/var/tests/generic.local.bash/compiler_status_regex/default_status_returncode/6b725310/default_status_returncode_build.sh
    ______________________________
    Launching test: override_status_regex/3e99f85a
    override_status_regex/3e99f85a: Running Test script /tmp/var/tests/generic.local.bash/compiler_status_regex/override_status_regex/3e99f85a/override_status_regex_build.sh
    ______________________________
    Launching test: override_status_regex/e0d47271
    override_status_regex/e0d47271: Running Test script /tmp/var/tests/generic.local.bash/compiler_status_regex/override_status_regex/e0d47271/override_status_regex_build.sh
    default_status_returncode/6b725310: completed with returncode: 0
    default_status_returncode/6b725310: Writing output file -  /tmp/var/tests/generic.local.bash/compiler_status_regex/default_status_returncode/6b725310/default_status_returncode.out
    default_status_returncode/6b725310: Writing error file - /tmp/var/tests/generic.local.bash/compiler_status_regex/default_status_returncode/6b725310/default_status_returncode.err
    default_status_returncode/6b725310: Checking returncode - 0 is matched in list [0]
    default_status_returncode/dfee4a1e: completed with returncode: 127
    default_status_returncode/dfee4a1e: Writing output file -  /tmp/var/tests/generic.local.bash/compiler_status_regex/default_status_returncode/dfee4a1e/default_status_returncode.out
    default_status_returncode/dfee4a1e: Writing error file - /tmp/var/tests/generic.local.bash/compiler_status_regex/default_status_returncode/dfee4a1e/default_status_returncode.err
    default_status_returncode/dfee4a1e: Checking returncode - 127 is matched in list [0]
    override_status_regex/e0d47271: completed with returncode: 0
    override_status_regex/e0d47271: Writing output file -  /tmp/var/tests/generic.local.bash/compiler_status_regex/override_status_regex/e0d47271/override_status_regex.out
    override_status_regex/e0d47271: Writing error file - /tmp/var/tests/generic.local.bash/compiler_status_regex/override_status_regex/e0d47271/override_status_regex.err
    override_status_regex/e0d47271: performing regular expression - '^final result: 0.99$' on file:
    /tmp/var/tests/generic.local.bash/compiler_status_regex/override_status_regex/e0d47271/override_status_regex.out
    override_status_regex/e0d47271: Regular Expression Match - Failed!
    override_status_regex/3e99f85a: completed with returncode: 127
    override_status_regex/3e99f85a: Writing output file -  /tmp/var/tests/generic.local.bash/compiler_status_regex/override_status_regex/3e99f85a/override_status_regex.out
    override_status_regex/3e99f85a: Writing error file - /tmp/var/tests/generic.local.bash/compiler_status_regex/override_status_regex/3e99f85a/override_status_regex.err
    override_status_regex/3e99f85a: Checking returncode - 127 is matched in list [0]
                                                               Test Summary
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┓
    ┃ Builder                            ┃ executor           ┃ status ┃ Checks (ReturnCode, Regex, Runtime) ┃ ReturnCode ┃ Runtime  ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━┩
    │ default_status_returncode/dfee4a1e │ generic.local.bash │ FAIL   │ False False False                   │ 127        │ 0.322336 │
    ├────────────────────────────────────┼────────────────────┼────────┼─────────────────────────────────────┼────────────┼──────────┤
    │ default_status_returncode/6b725310 │ generic.local.bash │ PASS   │ True False False                    │ 0          │ 0.272139 │
    ├────────────────────────────────────┼────────────────────┼────────┼─────────────────────────────────────┼────────────┼──────────┤
    │ override_status_regex/3e99f85a     │ generic.local.bash │ FAIL   │ False False False                   │ 127        │ 0.332581 │
    ├────────────────────────────────────┼────────────────────┼────────┼─────────────────────────────────────┼────────────┼──────────┤
    │ override_status_regex/e0d47271     │ generic.local.bash │ FAIL   │ False False False                   │ 0          │ 0.238165 │
    └────────────────────────────────────┴────────────────────┴────────┴─────────────────────────────────────┴────────────┴──────────┘



    Passed Tests: 1/4 Percentage: 25.000%
    Failed Tests: 3/4 Percentage: 75.000%


    Writing Logfile to: /tmp/buildtest_59954269.log
    A copy of logfile can be found at $BUILDTEST_ROOT/buildtest.log -  /tmp/buildtest.log

Customize Run Line
-------------------

buildtest will define variable ``_EXEC`` in the job script that can be used to reference
the generated binary. By default, buildtest will run the program standalone, but sometimes you
may want to customize how job is run. This may include passing arguments or running
binary through a job/mpi launcher. The ``run`` property can be used to configure how program is executed.
The compiled executable will be present in local directory which can be accessed via ``./$_EXEC``. In example below
we pass arguments ``1 3`` for **builtin_gcc** compiler and ``100 200`` for **gcc_11.2.0** compiler.

.. literalinclude:: ../tutorials/compilers/custom_run.yml
    :language: yaml

You can build this test by running ``buildtest build -b tutorials/compilers/custom_run.yml``. Once test is complete let's inspect the generated
test. We see that buildtest will insert the line specified by ``run`` property after compilation and run the executable.

.. code-block:: shell

    $ buildtest inspect query -d all -b  -t custom_run_by_compilers
    ───────────────────────────────────────────────────────────── custom_run_by_compilers/1438d9e1-a472-4759-a3e4-145afd020a3e ─────────────────────────────────────────────────────────────
    executor:  generic.local.bash
    description:  Customize binary launch based on compiler
    state:  PASS
    returncode:  0
    runtime:  0.234103
    starttime:  2021/10/13 14:49:17
    endtime:  2021/10/13 14:49:17
    ───────────────────────────────── Test File: /tmp/var/tests/generic.local.bash/custom_run/custom_run_by_compilers/1438d9e1/custom_run_by_compilers.sh ──────────────────────────────────
       1 #!/usr/bin/bash
       2
       3
       4 # name of executable
       5 _EXEC=argc.c.exe
       6 # Compilation Line
       7 /usr/bin/gcc -o $_EXEC /tmp/tutorials/compilers/src/argc.c
       8
       9
      10 # Run executable
      11 ./$_EXEC 1 3
      12
      13
    ────────────────────────────── Test File: /tmp/var/tests/generic.local.bash/custom_run/custom_run_by_compilers/1438d9e1/custom_run_by_compilers_build.sh ───────────────────────────────
       1 #!/bin/bash
       2
       3
       4 ############# START VARIABLE DECLARATION ########################
       5 export BUILDTEST_TEST_NAME=custom_run_by_compilers
       6 export BUILDTEST_TEST_ROOT=/tmp/var/tests/generic.local.bash/custom_run/custom_run_by_compilers/1438d9e1
       7 export BUILDTEST_BUILDSPEC_DIR=/tmp/tutorials/compilers
       8 export BUILDTEST_STAGE_DIR=/tmp/var/tests/generic.local.bash/custom_run/custom_run_by_compilers/1438d9e1/stage
       9 export BUILDTEST_TEST_ID=1438d9e1-a472-4759-a3e4-145afd020a3e
      10 ############# END VARIABLE DECLARATION   ########################
      11
      12
      13 # source executor startup script
      14 source /tmp/var/executor/generic.local.bash/before_script.sh
      15 # Run generated script
      16 /tmp/var/tests/generic.local.bash/custom_run/custom_run_by_compilers/1438d9e1/stage/custom_run_by_compilers.sh
      17 # Get return code
      18 returncode=$?
      19 # Exit with return code
      20 exit $returncode
    ───────────────────────────────────────────────────────────── custom_run_by_compilers/563afffd-6d23-4817-9fed-294363416242 ─────────────────────────────────────────────────────────────
    executor:  generic.local.bash
    description:  Customize binary launch based on compiler
    state:  PASS
    returncode:  0
    runtime:  0.24476
    starttime:  2021/10/13 14:49:17
    endtime:  2021/10/13 14:49:17
    ───────────────────────────────── Test File: /tmp/var/tests/generic.local.bash/custom_run/custom_run_by_compilers/563afffd/custom_run_by_compilers.sh ──────────────────────────────────
       1 #!/usr/bin/bash
       2
       3
       4 # name of executable
       5 _EXEC=argc.c.exe
       6 # Compilation Line
       7 /bootstrap/view/bin/gcc -o $_EXEC /tmp/tutorials/compilers/src/argc.c
       8
       9
      10 # Run executable
      11 ./$_EXEC 100 120
      12
      13
    ────────────────────────────── Test File: /tmp/var/tests/generic.local.bash/custom_run/custom_run_by_compilers/563afffd/custom_run_by_compilers_build.sh ───────────────────────────────
       1 #!/bin/bash
       2
       3
       4 ############# START VARIABLE DECLARATION ########################
       5 export BUILDTEST_TEST_NAME=custom_run_by_compilers
       6 export BUILDTEST_TEST_ROOT=/tmp/var/tests/generic.local.bash/custom_run/custom_run_by_compilers/563afffd
       7 export BUILDTEST_BUILDSPEC_DIR=/tmp/tutorials/compilers
       8 export BUILDTEST_STAGE_DIR=/tmp/var/tests/generic.local.bash/custom_run/custom_run_by_compilers/563afffd/stage
       9 export BUILDTEST_TEST_ID=563afffd-6d23-4817-9fed-294363416242
      10 ############# END VARIABLE DECLARATION   ########################
      11
      12
      13 # source executor startup script
      14 source /tmp/var/executor/generic.local.bash/before_script.sh
      15 # Run generated script
      16 /tmp/var/tests/generic.local.bash/custom_run/custom_run_by_compilers/563afffd/stage/custom_run_by_compilers.sh
      17 # Get return code
      18 returncode=$?
      19 # Exit with return code
      20 exit $returncode

Pre/Post sections for build and run section
--------------------------------------------

The compiler schema comes with ``pre_build``, ``post_build``, ``pre_run`` and
``post_run`` fields where you can insert shell commands before and after  compilation and
running binary.

Shown below is an example buildspec with pre/post section.

.. literalinclude:: ../tutorials/compilers/pre_post_build_run.yml
    :language: yaml


The format of the test structure is as follows.

.. code-block:: shell

    #!{shebang path} -- defaults to #!/bin/bash depends on executor name (local.bash, local.sh)
    {job directives} -- sbatch or bsub field
    {environment variables} -- env field
    {variable declaration} -- vars field
    {module commands} -- modules field

    {pre build commands} -- pre_build field
    {compile program} -- build field
    {post build commands} -- post_build field

    {pre run commands} -- pre_run field
    {run executable} -- run field
    {post run commands} -- post_run field

You can run this example by running the following command::

    buildtest build -b tutorials/compilers/pre_post_build_run.yml

If we inspect the content of test we see that buildtest will insert the shell commands
for ``pre_build``, ``post_build``, ``pre_run`` and ``post_run`` in its corresponding section.

.. code-block:: shell

    $ buildtest inspect query -d all -t pre_post_build_run
    ─────────────────────────────────────────────────────────────── pre_post_build_run/72644b22-9cf1-40b9-8357-46e9170649a6 ────────────────────────────────────────────────────────────────
    executor:  generic.local.bash
    description:  example using pre_build, post_build, pre_run, post_run example
    state:  PASS
    returncode:  0
    runtime:  0.196161
    starttime:  2021/10/13 14:31:01
    endtime:  2021/10/13 14:31:02
    ────────────────────────────────── Test File: /tmp/var/tests/generic.local.bash/pre_post_build_run/pre_post_build_run/72644b22/pre_post_build_run.sh ───────────────────────────────────
       1 #!/usr/bin/bash
       2
       3
       4 # name of executable
       5 _EXEC=hello.c.exe
       6 ### START OF PRE BUILD SECTION ###
       7 echo "These are commands run before compilation"
       8
       9 ### END OF PRE BUILD SECTION   ###
      10
      11
      12 # Compilation Line
      13 /usr/bin/gcc -Wall -o $_EXEC /tmp/tutorials/compilers/src/hello.c
      14
      15
      16 ### START OF POST BUILD SECTION ###
      17 echo "These are commands run after compilation"
      18
      19 ### END OF POST BUILD SECTION ###
      20
      21
      22 ### START OF PRE RUN SECTION ###
      23 echo "These are commands run before running script"
      24
      25 ### END OF PRE RUN SECTION   ###
      26
      27
      28 # Run executable
      29 ./$_EXEC
      30
      31
      32 ### START OF POST RUN SECTION ###
      33 echo "These are commands run after running script"
      34 ### END OF POST RUN SECTION   ###
      35
      36



Single Test Multiple Compilers
-------------------------------

It's possible to run single test across multiple compilers (gcc, intel, cray, etc...). In the
next example, we will build an OpenMP reduction test using gcc, intel and cray compilers. In this
test, we use ``name`` field to select compilers that start with **gcc**, **intel** and **PrgEnv-cray**
as compiler names. The ``default`` section is organized by compiler groups which inherits compiler flags
for all compilers. OpenMP flag for gcc, intel and cray differ for instance one must use ``-fopenmp`` for gcc,
``--qopenmp`` for intel and ``-h omp`` for cray.

.. code-block:: yaml
   :linenos:
   :emphasize-lines: 10-20

    version: "1.0"
    buildspecs:
      reduction:
        type: compiler
        executor: local.bash
        source: src/reduction.c
        description: OpenMP reduction example using gcc, intel and cray compiler
        tags: [openmp]
        compilers:
          name: ["^(gcc|intel|PrgEnv-cray)"]
          default:
            all:
              env:
                OMP_NUM_THREADS: 4
            gcc:
              cflags: -fopenmp
            intel:
              cflags: -qopenmp
            cray:
              cflags: -h omp

In this example `OMP_NUM_THREADS` environment variable under the ``all`` section which
will be used for all compiler groups. This example was built on Cori, we expect this
test to run against every gcc, intel and PrgEnv-cray compiler module:

.. code-block:: console

    $ buildtest build -b buildspecs/apps/openmp/reduction.yml


    User:  siddiq90
    Hostname:  cori02
    Platform:  Linux
    Current Time:  2021/06/11 08:42:54
    buildtest path: /global/homes/s/siddiq90/github/buildtest/bin/buildtest
    buildtest version:  0.9.5
    python path: /global/homes/s/siddiq90/.conda/envs/buildtest/bin/python
    python version:  3.8.8
    Test Directory:  /global/u1/s/siddiq90/github/buildtest/var/tests
    Configuration File:  /global/u1/s/siddiq90/.buildtest/config.yml
    Command: /global/homes/s/siddiq90/github/buildtest/bin/buildtest build -b buildspecs/apps/openmp/reduction.yml

    +-------------------------------+
    | Stage: Discovering Buildspecs |
    +-------------------------------+

    +----------------------------------------------------------------------------------+
    | Discovered Buildspecs                                                            |
    +==================================================================================+
    | /global/u1/s/siddiq90/github/buildtest-cori/buildspecs/apps/openmp/reduction.yml |
    +----------------------------------------------------------------------------------+
    Discovered Buildspecs:  1
    Excluded Buildspecs:  0
    Detected Buildspecs after exclusion:  1

    +---------------------------+
    | Stage: Parsing Buildspecs |
    +---------------------------+

     schemafile                | validstate   | buildspec
    ---------------------------+--------------+----------------------------------------------------------------------------------
     compiler-v1.0.schema.json | True         | /global/u1/s/siddiq90/github/buildtest-cori/buildspecs/apps/openmp/reduction.yml



    name       description
    ---------  ---------------------------------------------------------------
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler
    reduction  OpenMP reduction example using gcc, intel, PrgEnv-cray compiler

    +----------------------+
    | Stage: Building Test |
    +----------------------+



     name      | id       | type     | executor        | tags       | compiler                                | testpath
    -----------+----------+----------+-----------------+------------+-----------------------------------------+------------------------------------------------------------------------------------------------------------
     reduction | fd93fdcb | compiler | cori.local.bash | ['openmp'] | gcc/6.1.0                               | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/25/reduction_build.sh
     reduction | 43737191 | compiler | cori.local.bash | ['openmp'] | gcc/7.3.0                               | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/26/reduction_build.sh
     reduction | 6e2e95cd | compiler | cori.local.bash | ['openmp'] | gcc/8.1.0                               | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/27/reduction_build.sh
     reduction | c48a8d8d | compiler | cori.local.bash | ['openmp'] | gcc/8.2.0                               | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/28/reduction_build.sh
     reduction | a6201c48 | compiler | cori.local.bash | ['openmp'] | gcc/8.3.0                               | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/29/reduction_build.sh
     reduction | aa06b1be | compiler | cori.local.bash | ['openmp'] | gcc/9.3.0                               | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/30/reduction_build.sh
     reduction | 02b8e7aa | compiler | cori.local.bash | ['openmp'] | gcc/10.1.0                              | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/31/reduction_build.sh
     reduction | bd9abd7e | compiler | cori.local.bash | ['openmp'] | gcc/6.3.0                               | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/32/reduction_build.sh
     reduction | 9409a86f | compiler | cori.local.bash | ['openmp'] | gcc/8.1.1-openacc-gcc-8-branch-20190215 | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/33/reduction_build.sh
     reduction | b9700a0f | compiler | cori.local.bash | ['openmp'] | PrgEnv-cray/6.0.5                       | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/34/reduction_build.sh
     reduction | a605c970 | compiler | cori.local.bash | ['openmp'] | PrgEnv-cray/6.0.7                       | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/35/reduction_build.sh
     reduction | 9ef915a9 | compiler | cori.local.bash | ['openmp'] | PrgEnv-cray/6.0.9                       | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/36/reduction_build.sh
     reduction | 4f9e4242 | compiler | cori.local.bash | ['openmp'] | intel/19.0.3.199                        | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/37/reduction_build.sh
     reduction | e37befed | compiler | cori.local.bash | ['openmp'] | intel/19.1.2.254                        | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/38/reduction_build.sh
     reduction | 1e9b0ab5 | compiler | cori.local.bash | ['openmp'] | intel/16.0.3.210                        | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/39/reduction_build.sh
     reduction | 4e6d6f8a | compiler | cori.local.bash | ['openmp'] | intel/17.0.1.132                        | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/40/reduction_build.sh
     reduction | ad1e44af | compiler | cori.local.bash | ['openmp'] | intel/17.0.2.174                        | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/41/reduction_build.sh
     reduction | 49acf44b | compiler | cori.local.bash | ['openmp'] | intel/18.0.1.163                        | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/42/reduction_build.sh
     reduction | 4192750c | compiler | cori.local.bash | ['openmp'] | intel/18.0.3.222                        | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/43/reduction_build.sh
     reduction | 06584529 | compiler | cori.local.bash | ['openmp'] | intel/19.0.0.117                        | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/44/reduction_build.sh
     reduction | 82fd9bab | compiler | cori.local.bash | ['openmp'] | intel/19.0.8.324                        | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/45/reduction_build.sh
     reduction | 6140e8b4 | compiler | cori.local.bash | ['openmp'] | intel/19.1.0.166                        | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/46/reduction_build.sh
     reduction | ac509e2e | compiler | cori.local.bash | ['openmp'] | intel/19.1.1.217                        | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/47/reduction_build.sh
     reduction | 9c39818e | compiler | cori.local.bash | ['openmp'] | intel/19.1.2.275                        | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/48/reduction_build.sh
     reduction | 2cb3acd1 | compiler | cori.local.bash | ['openmp'] | intel/19.1.3.304                        | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.local.bash/reduction/reduction/49/reduction_build.sh

    +---------------------+
    | Stage: Running Test |
    +---------------------+

     name      | id       | executor        | status   |   returncode
    -----------+----------+-----------------+----------+--------------
     reduction | fd93fdcb | cori.local.bash | PASS     |            0
     reduction | 43737191 | cori.local.bash | PASS     |            0
     reduction | 6e2e95cd | cori.local.bash | PASS     |            0
     reduction | c48a8d8d | cori.local.bash | PASS     |            0
     reduction | a6201c48 | cori.local.bash | PASS     |            0
     reduction | aa06b1be | cori.local.bash | PASS     |            0
     reduction | 02b8e7aa | cori.local.bash | PASS     |            0
     reduction | bd9abd7e | cori.local.bash | PASS     |            0
     reduction | 9409a86f | cori.local.bash | PASS     |            0
     reduction | b9700a0f | cori.local.bash | PASS     |            0
     reduction | a605c970 | cori.local.bash | PASS     |            0
     reduction | 9ef915a9 | cori.local.bash | PASS     |            0
     reduction | 4f9e4242 | cori.local.bash | PASS     |            0
     reduction | e37befed | cori.local.bash | PASS     |            0
     reduction | 1e9b0ab5 | cori.local.bash | PASS     |            0
     reduction | 4e6d6f8a | cori.local.bash | PASS     |            0
     reduction | ad1e44af | cori.local.bash | PASS     |            0
     reduction | 49acf44b | cori.local.bash | PASS     |            0
     reduction | 4192750c | cori.local.bash | PASS     |            0
     reduction | 06584529 | cori.local.bash | PASS     |            0
     reduction | 82fd9bab | cori.local.bash | PASS     |            0
     reduction | 6140e8b4 | cori.local.bash | PASS     |            0
     reduction | ac509e2e | cori.local.bash | PASS     |            0
     reduction | 9c39818e | cori.local.bash | PASS     |            0
     reduction | 2cb3acd1 | cori.local.bash | PASS     |            0

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Passed Tests: 25/25 Percentage: 100.000%
    Failed Tests: 0/25 Percentage: 0.000%


    Writing Logfile to: /tmp/buildtest_sq87154s.log
    A copy of logfile can be found at $BUILDTEST_ROOT/buildtest.log -  /global/homes/s/siddiq90/github/buildtest/buildtest.log

MPI Example
------------

In this example we run a MPI Laplace code using 4 process on a KNL node using
the ``intel/19.1.2.254`` compiler. This test is run on Cori through batch queue
system. We can define **#SBATCH** parameters using ``sbatch`` property. This program
is compiled using ``mpiicc`` wrapper this can be defined using ``cc`` parameter.

Currently, buildtest cannot detect if program is serial or MPI to infer appropriate
compiler wrapper. If ``cc`` wasn't specified, buildtest would infer `icc` as compiler
wrapper for C program. This program is run using ``srun`` job launcher, we can control
how test is executed using the ``run`` property. This test required we swap intel
modules and load `impi/2020` module.

.. code-block:: yaml
    :linenos:
    :emphasize-lines: 13,16,18-22

    version: "1.0"
    buildspecs:
      laplace_mpi:
        type: compiler
        description: Laplace MPI code in C
        executor: slurm.knl_debug
        tags: ["mpi"]
        source: src/laplace_mpi.c
        compilers:
          name: ["^(intel/19.1.2.254)$"]
          default:
            all:
              sbatch: ["-N 1", "-n 4"]
              run: srun -n 4 $_EXEC
            intel:
              cc: mpiicc
              cflags: -O3
          config:
            intel/19.1.2.254:
              module:
                load: [impi/2020]
                swap: [intel, intel/19.1.2.254]

Shown below is a sample build for this buildspec, buildtest will dispatch and poll
job until its complete.

.. code-block:: console

    $ buildtest build -b buildspecs/apps/mpi/laplace_mpi.yml


    User:  siddiq90
    Hostname:  cori02
    Platform:  Linux
    Current Time:  2021/06/11 09:11:16
    buildtest path: /global/homes/s/siddiq90/github/buildtest/bin/buildtest
    buildtest version:  0.9.5
    python path: /global/homes/s/siddiq90/.conda/envs/buildtest/bin/python
    python version:  3.8.8
    Test Directory:  /global/u1/s/siddiq90/github/buildtest/var/tests
    Configuration File:  /global/u1/s/siddiq90/.buildtest/config.yml
    Command: /global/homes/s/siddiq90/github/buildtest/bin/buildtest build -b buildspecs/apps/mpi/laplace_mpi.yml

    +-------------------------------+
    | Stage: Discovering Buildspecs |
    +-------------------------------+

    +---------------------------------------------------------------------------------+
    | Discovered Buildspecs                                                           |
    +=================================================================================+
    | /global/u1/s/siddiq90/github/buildtest-cori/buildspecs/apps/mpi/laplace_mpi.yml |
    +---------------------------------------------------------------------------------+
    Discovered Buildspecs:  1
    Excluded Buildspecs:  0
    Detected Buildspecs after exclusion:  1

    +---------------------------+
    | Stage: Parsing Buildspecs |
    +---------------------------+

     schemafile                | validstate   | buildspec
    ---------------------------+--------------+---------------------------------------------------------------------------------
     compiler-v1.0.schema.json | True         | /global/u1/s/siddiq90/github/buildtest-cori/buildspecs/apps/mpi/laplace_mpi.yml



    name         description
    -----------  ---------------------
    laplace_mpi  Laplace MPI code in C

    +----------------------+
    | Stage: Building Test |
    +----------------------+



     name        | id       | type     | executor             | tags    | compiler         | testpath
    -------------+----------+----------+----------------------+---------+------------------+----------------------------------------------------------------------------------------------------------------------
     laplace_mpi | a6087b86 | compiler | cori.slurm.knl_debug | ['mpi'] | intel/19.1.2.254 | /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/laplace_mpi/laplace_mpi/0/laplace_mpi_build.sh

    +---------------------+
    | Stage: Running Test |
    +---------------------+

    [laplace_mpi] JobID: 43308598 dispatched to scheduler
     name        | id       | executor             | status   |   returncode
    -------------+----------+----------------------+----------+--------------
     laplace_mpi | a6087b86 | cori.slurm.knl_debug | N/A      |           -1


    Polling Jobs in 30 seconds
    ________________________________________
    Job Queue: [43308598]


    Pending Jobs
    ________________________________________


    +-------------+----------------------+----------+-----------+
    |    name     |       executor       |  jobID   | jobstate  |
    +-------------+----------------------+----------+-----------+
    | laplace_mpi | cori.slurm.knl_debug | 43308598 | COMPLETED |
    +-------------+----------------------+----------+-----------+


    Polling Jobs in 30 seconds
    ________________________________________
    Job Queue: []


    Completed Jobs
    ________________________________________


    +-------------+----------------------+----------+-----------+
    |    name     |       executor       |  jobID   | jobstate  |
    +-------------+----------------------+----------+-----------+
    | laplace_mpi | cori.slurm.knl_debug | 43308598 | COMPLETED |
    +-------------+----------------------+----------+-----------+

    +---------------------------------------------+
    | Stage: Final Results after Polling all Jobs |
    +---------------------------------------------+

     name        | id       | executor             | status   |   returncode
    -------------+----------+----------------------+----------+--------------
     laplace_mpi | a6087b86 | cori.slurm.knl_debug | PASS     |            0

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Passed Tests: 1/1 Percentage: 100.000%
    Failed Tests: 0/1 Percentage: 0.000%


    Writing Logfile to: /tmp/buildtest_wgptyp8v.log
    A copy of logfile can be found at $BUILDTEST_ROOT/buildtest.log -  /global/homes/s/siddiq90/github/buildtest/buildtest.log

The generated test is as follows, note that buildtest will insert the #SBATCH directives at the top of script, and ``module load``
are done before ``module swap`` command.

.. code-block:: shell
    :linenos:
    :emphasize-lines: 2-3, 8-10

    #!/bin/bash
    #SBATCH -N 1
    #SBATCH -n 4
    #SBATCH --job-name=laplace_mpi
    #SBATCH --output=laplace_mpi.out
    #SBATCH --error=laplace_mpi.err
    _EXEC=laplace_mpi.c.exe
    module load impi/2020
    module swap intel intel/19.1.2.254
    mpiicc -O3 -o $_EXEC /global/u1/s/siddiq90/github/buildtest-cori/buildspecs/apps/mpi/src/laplace_mpi.c
    srun -n 4 $_EXEC

The master script that buildtest will invoke is the following, notice that our generated script (shown above) is invoked via `sbatch` with its
options. The options ``sbatch -q debug --clusters=cori -C knl,quad,cache`` was inserted by our executor configuration. We add the ``--parsable``
option for Slurm jobs in order to get the JobID when this script is invoked so that buildtest can poll the job.

.. code-block:: shell
    :linenos:
    :emphasize-lines: 3

    #!/bin/bash
    source /global/u1/s/siddiq90/github/buildtest/var/executor/cori.slurm.knl_debug/before_script.sh
    sbatch --parsable -q debug --clusters=cori -C knl,quad,cache /global/u1/s/siddiq90/github/buildtest/var/tests/cori.slurm.knl_debug/laplace_mpi/laplace_mpi/0/stage/laplace_mpi.sh
    returncode=$?
    exit $returncode
