.. _compiler_schema:

Compiler Schema
=================

The compiler schema is used for compilation of programs, currently we support
single source file compilation. In order to use the compiler schema you must set ``type: compiler`` in your
sub-schema. See `compiler schema docs <https://buildtesters.github.io/buildtest/pages/schemadocs/compiler-v1.html>`_


Compilation Examples
----------------------

We assume the reader has basic understanding of :ref:`global_schema`
validation. Shown below is the schema header definition for `compiler-v1.0.schema.json <https://github.com/buildtesters/buildtest/blob/devel/buildtest/schemas/compiler-v1.0.schema.json>`_:

.. code-block:: json

      "$id": "compiler-v1.0.schema.json",
      "$schema": "http://json-schema.org/draft-07/schema#",
      "title": "compiler schema version 1.0",
      "description": "The compiler schema is of ``type: compiler`` in sub-schema which is used for compiling and running programs",
      "type": "object",
      "required": [
        "type",
        "source",
        "compilers",
        "executor"
      ],

The required fields for compiler schema are **type**, **compilers**, **source**
and **executor**.

Shown below is a test name ``hello_f`` that compiles Fortran code with GNU compiler.

.. program-output:: cat ../tutorials/compilers/gnu_hello_fortran.yml

The ``source`` property is used to specify input program for
compilation, this can be a file relative to buildspec file or an absolute path.
In this example the source file ``src/hello.f90`` is relative to buildspec file.
The ``compilers`` section specifies compiler configuration, the ``name``
field is required property which is used to search compilers based on regular expression.
In this example we use the **builtin_gcc** compiler as regular expression which is the system
gcc compiler provided by buildtest. The ``default`` section specifies default compiler
configuration applicable to a specific compiler group.

Shown below is an example build for the buildspec example

.. program-output:: cat docgen/schemas/gnu_hello.txt

The generated test for test name **hello_f** is the following:

.. code-block:: shell

    #!/bin/bash
    _EXEC=hello.f90.exe
    gfortran -o $_EXEC /Users/siddiq90/Documents/buildtest/tutorials/compilers/src/hello.f90
    ./$_EXEC


buildtest will use compiler wrappers specified in your settings
to build the test, however these values can be overridden in buildspec file which
will be discussed later.

The ``builtin_gcc`` compiler is defined below this can be retrieved by running
``buildtest config compilers``. The ``-y`` will display compilers in YAML format.

.. code-block:: console

    $ buildtest config compilers -y
    gcc:
      builtin_gcc:
        cc: /usr/bin/gcc
        cxx: /usr/bin/g++
        fc: /usr/bin/gfortran

buildtest will compile and run the code depending on the compiler flags. buildtest,
will detect the file extension of source file (``source`` property) to detect
programming language and finally generate the appropriate C, C++, or Fortran
compilation based on language detected. In this example, buildtest detects a
**.f90** file extension and determines this is a Fortran program.

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
applied for available compilers defined in buildtest configuration. In example below
we select all compilers with regular expression ``^(builtin_gcc|gcc)`` that is specified in line ``name: ["^(builtin_gcc|gcc)"]``

.. program-output:: cat ../tutorials/compilers/vecadd.yml

Currently, we have 3 compilers defined in buildtest settings, shown below is a listing
of all compilers. We used ``buildtest config compilers find`` to :ref:`detect compilers <detect_compilers>`.

.. code-block:: console

    $ buildtest config compilers
    builtin_gcc
    gcc/9.3.0-n7p74fd
    gcc/10.2.0-37fmsw7

.. note::
   This example may vary on your machine depending on compilers available via ``module`` command.


We expect buildtest to select all three compilers based on our regular expression. In the following
build, notice we have three tests for ``vecadd_gnu`` one for each compiler:

.. code-block:: console

    $ buildtest build -b tutorials/compilers/vecadd.yml


    User:  siddiq90
    Hostname:  DOE-7086392.local
    Platform:  Darwin
    Current Time:  2021/06/10 21:52:32
    buildtest path: /Users/siddiq90/Documents/GitHubDesktop/buildtest/bin/buildtest
    buildtest version:  0.9.5
    python path: /Users/siddiq90/.local/share/virtualenvs/buildtest-KLOcDrW0/bin/python
    python version:  3.7.3
    Test Directory:  /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests
    Configuration File:  /Users/siddiq90/.buildtest/config.yml
    Command: /Users/siddiq90/Documents/GitHubDesktop/buildtest/bin/buildtest build -b tutorials/compilers/vecadd.yml

    +-------------------------------+
    | Stage: Discovering Buildspecs |
    +-------------------------------+

    +----------------------------------------------------------------------------------+
    | Discovered Buildspecs                                                            |
    +==================================================================================+
    | /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/compilers/vecadd.yml |
    +----------------------------------------------------------------------------------+
    Discovered Buildspecs:  1
    Excluded Buildspecs:  0
    Detected Buildspecs after exclusion:  1

    +---------------------------+
    | Stage: Parsing Buildspecs |
    +---------------------------+

     schemafile                | validstate   | buildspec
    ---------------------------+--------------+----------------------------------------------------------------------------------
     compiler-v1.0.schema.json | True         | /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/compilers/vecadd.yml



    name        description
    ----------  -----------------------------------------
    vecadd_gnu  Vector Addition example with GNU compiler
    vecadd_gnu  Vector Addition example with GNU compiler
    vecadd_gnu  Vector Addition example with GNU compiler

    +----------------------+
    | Stage: Building Test |
    +----------------------+



     name       | id       | type     | executor           | tags                     | compiler           | testpath
    ------------+----------+----------+--------------------+--------------------------+--------------------+------------------------------------------------------------------------------------------------------------------------
     vecadd_gnu | 6f6b16e1 | compiler | generic.local.bash | ['tutorials', 'compile'] | builtin_gcc        | /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.bash/vecadd/vecadd_gnu/2/vecadd_gnu_build.sh
     vecadd_gnu | a76dd163 | compiler | generic.local.bash | ['tutorials', 'compile'] | gcc/9.3.0-n7p74fd  | /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.bash/vecadd/vecadd_gnu/3/vecadd_gnu_build.sh
     vecadd_gnu | 82360702 | compiler | generic.local.bash | ['tutorials', 'compile'] | gcc/10.2.0-37fmsw7 | /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.bash/vecadd/vecadd_gnu/4/vecadd_gnu_build.sh

    +---------------------+
    | Stage: Running Test |
    +---------------------+

     name       | id       | executor           | status   |   returncode
    ------------+----------+--------------------+----------+--------------
     vecadd_gnu | 6f6b16e1 | generic.local.bash | PASS     |            0
     vecadd_gnu | a76dd163 | generic.local.bash | PASS     |            0
     vecadd_gnu | 82360702 | generic.local.bash | PASS     |            0

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Passed Tests: 3/3 Percentage: 100.000%
    Failed Tests: 0/3 Percentage: 0.000%


    Writing Logfile to: /Users/siddiq90/buildtest/buildtest_b0jwyoyv.log
    A copy of logfile can be found at $BUILDTEST_ROOT/buildtest.log -  /Users/siddiq90/Documents/GitHubDesktop/buildtest/buildtest.log

buildtest will use compiler settings including module configuration from buildtest
settings (``config.yml``). In example below we show the compiler definitions for the
three gcc compilers. The ``module`` section is the declaration of modules to load, by default
we disable purge (``purge: False``) which instructs buildtest to not insert ``module purge``.
The ``load`` is a list of modules to load via ``module load``.

Shown below is the compiler configuration.

.. code-block:: yaml
    :emphasize-lines: 14-17,22-25
    :linenos:

    compilers:
      find:
        gcc: ^(gcc)
      compiler:
        gcc:
          builtin_gcc:
            cc: gcc
            fc: gfortran
            cxx: g++
          gcc/9.3.0-n7p74fd:
            cc: gcc
            cxx: g++
            fc: gfortran
            module:
              load:
              - gcc/9.3.0-n7p74fd
              purge: false
          gcc/10.2.0-37fmsw7:
            cc: gcc
            cxx: g++
            fc: gfortran
            module:
              load:
              - gcc/10.2.0-37fmsw7
              purge: false

If we take a closer look at the generated test we see the `module load` command in the test script.

.. code-block:: shell
    :emphasize-lines: 3
    :linenos:

    #!/bin/bash
    _EXEC=vecAdd.c.exe
    module load gcc/10.2.0-37fmsw7
    gcc -o $_EXEC /Users/siddiq90/Documents/buildtest/tutorials/compilers/src/vecAdd.c
    ./$_EXEC


.. code-block:: shell
    :emphasize-lines: 3
    :linenos:

    #!/bin/bash
    _EXEC=vecAdd.c.exe
    module load gcc/9.3.0-n7p74fd
    gcc -o $_EXEC /Users/siddiq90/Documents/buildtest/tutorials/compilers/src/vecAdd.c
    ./$_EXEC

Excluding Compilers
--------------------

The ``exclude`` property is part of compilers section which allows one to exclude compilers
upon discovery by ``name`` field. The exclude property is a list of compiler names that
will be removed from test generation which is done prior to build phase. buildtest will exclude
any compilers specified in ``exclude`` if they were found based on regular
expression in ``name`` field. In this example, we slightly modified previous example
by excluding ``gcc/10.2.0-37fmsw7`` compiler. This is specified by ``exclude: [gcc/10.2.0-37fmsw7]``.

.. program-output:: cat ../tutorials/compilers/compiler_exclude.yml

Notice when we build this test, buildtest will exclude **gcc/10.2.0-37fmsw7** compiler
and test is not created during build phase.

.. code-block:: console
    :linenos:
    :emphasize-lines: 28

    $ buildtest build -b tutorials/compilers/compiler_exclude.yml


    User:  siddiq90
    Hostname:  DOE-7086392.local
    Platform:  Darwin
    Current Time:  2021/06/10 21:56:11
    buildtest path: /Users/siddiq90/Documents/GitHubDesktop/buildtest/bin/buildtest
    buildtest version:  0.9.5
    python path: /Users/siddiq90/.local/share/virtualenvs/buildtest-KLOcDrW0/bin/python
    python version:  3.7.3
    Test Directory:  /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests
    Configuration File:  /Users/siddiq90/.buildtest/config.yml
    Command: /Users/siddiq90/Documents/GitHubDesktop/buildtest/bin/buildtest build -b tutorials/compilers/compiler_exclude.yml

    +-------------------------------+
    | Stage: Discovering Buildspecs |
    +-------------------------------+

    +--------------------------------------------------------------------------------------------+
    | Discovered Buildspecs                                                                      |
    +============================================================================================+
    | /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/compilers/compiler_exclude.yml |
    +--------------------------------------------------------------------------------------------+
    Discovered Buildspecs:  1
    Excluded Buildspecs:  0
    Detected Buildspecs after exclusion:  1
    Excluding compiler: gcc/10.2.0-37fmsw7 from test generation

    +---------------------------+
    | Stage: Parsing Buildspecs |
    +---------------------------+

     schemafile                | validstate   | buildspec
    ---------------------------+--------------+--------------------------------------------------------------------------------------------
     compiler-v1.0.schema.json | True         | /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/compilers/compiler_exclude.yml



    name                description
    ------------------  -----------------------------------------------------------------
    vecadd_gnu_exclude  Vector Addition example with GNU compilers but exclude gcc@10.2.0

    +----------------------+
    | Stage: Building Test |
    +----------------------+



     name               | id       | type     | executor           | tags                     | compiler          | testpath
    --------------------+----------+----------+--------------------+--------------------------+-------------------+--------------------------------------------------------------------------------------------------------------------------------------------------
     vecadd_gnu_exclude | a7373d09 | compiler | generic.local.bash | ['tutorials', 'compile'] | gcc/9.3.0-n7p74fd | /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.bash/compiler_exclude/vecadd_gnu_exclude/0/vecadd_gnu_exclude_build.sh

    +---------------------+
    | Stage: Running Test |
    +---------------------+

     name               | id       | executor           | status   |   returncode
    --------------------+----------+--------------------+----------+--------------
     vecadd_gnu_exclude | a7373d09 | generic.local.bash | PASS     |            0

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Passed Tests: 1/1 Percentage: 100.000%
    Failed Tests: 0/1 Percentage: 0.000%


    Writing Logfile to: /Users/siddiq90/buildtest/buildtest_4szlay_j.log
    A copy of logfile can be found at $BUILDTEST_ROOT/buildtest.log -  /Users/siddiq90/Documents/GitHubDesktop/buildtest/buildtest.log

Compiler Defaults and Override Default Settings
-------------------------------------------------

Sometimes you may want to set default compiler flags (**cflags**, **fflags**, **cxxflags**),
preprocessor (**cppflags**) or linker flags (**ldflags**) for compiler group (gcc, intel, pgi, etc...).
This can be achieved using the ``default`` property that is part of **compilers** section.

The ``default`` field is organized into compiler groups, in example below we set default C compiler flags
(``cflags: -O1``). In addition, we can override default settings using the
``config`` property where one must specify the compiler name to override.
In example below we can override compiler settings for ``gcc/9.3.0-n7p74fd`` to use ``-O2``
and ``gcc/10.2.0-37fmsw7`` to use ``-O3`` for **cflags** .

.. program-output:: cat ../tutorials/compilers/gnu_hello_c.yml

Next we run this test, and we get three tests for test name **hello_c**.

.. code-block:: console

    $ buildtest build -b tutorials/compilers/gnu_hello_c.yml


    User:  siddiq90
    Hostname:  DOE-7086392.local
    Platform:  Darwin
    Current Time:  2021/06/10 22:00:08
    buildtest path: /Users/siddiq90/Documents/GitHubDesktop/buildtest/bin/buildtest
    buildtest version:  0.9.5
    python path: /Users/siddiq90/.local/share/virtualenvs/buildtest-KLOcDrW0/bin/python
    python version:  3.7.3
    Test Directory:  /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests
    Configuration File:  /Users/siddiq90/.buildtest/config.yml
    Command: /Users/siddiq90/Documents/GitHubDesktop/buildtest/bin/buildtest build -b tutorials/compilers/gnu_hello_c.yml

    +-------------------------------+
    | Stage: Discovering Buildspecs |
    +-------------------------------+

    +---------------------------------------------------------------------------------------+
    | Discovered Buildspecs                                                                 |
    +=======================================================================================+
    | /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/compilers/gnu_hello_c.yml |
    +---------------------------------------------------------------------------------------+
    Discovered Buildspecs:  1
    Excluded Buildspecs:  0
    Detected Buildspecs after exclusion:  1

    +---------------------------+
    | Stage: Parsing Buildspecs |
    +---------------------------+

     schemafile                | validstate   | buildspec
    ---------------------------+--------------+---------------------------------------------------------------------------------------
     compiler-v1.0.schema.json | True         | /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/compilers/gnu_hello_c.yml



    name     description
    -------  -------------------------
    hello_c  Hello World C Compilation
    hello_c  Hello World C Compilation
    hello_c  Hello World C Compilation

    +----------------------+
    | Stage: Building Test |
    +----------------------+



     name    | id       | type     | executor           | tags                     | compiler           | testpath
    ---------+----------+----------+--------------------+--------------------------+--------------------+-----------------------------------------------------------------------------------------------------------------------
     hello_c | afa92b9d | compiler | generic.local.bash | ['tutorials', 'compile'] | builtin_gcc        | /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.bash/gnu_hello_c/hello_c/2/hello_c_build.sh
     hello_c | 498010d3 | compiler | generic.local.bash | ['tutorials', 'compile'] | gcc/9.3.0-n7p74fd  | /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.bash/gnu_hello_c/hello_c/3/hello_c_build.sh
     hello_c | ee753488 | compiler | generic.local.bash | ['tutorials', 'compile'] | gcc/10.2.0-37fmsw7 | /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.bash/gnu_hello_c/hello_c/4/hello_c_build.sh

    +---------------------+
    | Stage: Running Test |
    +---------------------+

     name    | id       | executor           | status   |   returncode
    ---------+----------+--------------------+----------+--------------
     hello_c | afa92b9d | generic.local.bash | PASS     |            0
     hello_c | 498010d3 | generic.local.bash | PASS     |            0
     hello_c | ee753488 | generic.local.bash | PASS     |            0

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Passed Tests: 3/3 Percentage: 100.000%
    Failed Tests: 0/3 Percentage: 0.000%


    Writing Logfile to: /Users/siddiq90/buildtest/buildtest_dtyx0ags.log
    A copy of logfile can be found at $BUILDTEST_ROOT/buildtest.log -  /Users/siddiq90/Documents/GitHubDesktop/buildtest/buildtest.log



    Writing Logfile to: /private/tmp/buildtest/buildtest_hh9k7vm6.log

If we inspect the following test, we see the compiler flags are associated with the compiler. The test below
is for `builtin_gcc` which use the default ``-O1`` compiler flag as shown below.

.. code-block:: shell
    :emphasize-lines: 4
    :linenos:

    #!/bin/bash
    _EXEC=hello.c.exe
    gcc -O1 -o $_EXEC /Users/siddiq90/Documents/buildtest/tutorials/compilers/src/hello.c
    ./$_EXEC

The test for **gcc/10.2.0-37fmsw7** and **gcc/9.3.0-n7p74fd** have cflags ``-O3`` and ``-O2`` set in their respective tests.

.. code-block:: shell
    :emphasize-lines: 4
    :linenos:

    #!/bin/bash
    _EXEC=hello.c.exe
    module load gcc/10.2.0-37fmsw7
    gcc -O3 -o $_EXEC /Users/siddiq90/Documents/buildtest/tutorials/compilers/src/hello.c
    ./$_EXEC

.. code-block:: shell
    :emphasize-lines: 4
    :linenos:

    #!/bin/bash
    _EXEC=hello.c.exe
    module load gcc/9.3.0-n7p74fd
    gcc -O2 -o $_EXEC /Users/siddiq90/Documents/buildtest/tutorials/compilers/src/hello.c
    ./$_EXEC

Setting environment variables
------------------------------

Environment variables can be set using ``env`` property which is a list of
key/value pair to assign environment variables. This property can be used in ``default``
section within a compiler group. In example below we have an OpenMP Hello World example in C
where we define `OMP_NUM_THREADS` environment variable which controls number of OpenMP
threads to use when running program. In this example we use 2 threads for all gcc
compiler group

.. program-output:: cat ../tutorials/compilers/openmp_hello.yml

Shown below is one of the generated test. Notice on line 4 buildtest will set OMP_NUM_THREADS
environment variable.

.. code-block:: shell
    :emphasize-lines: 4
    :linenos:

    #!/bin/bash
    _EXEC=hello_omp.c.exe
    export OMP_NUM_THREADS=2
    module load gcc/10.2.0-37fmsw7
    gcc -fopenmp -o $_EXEC /Users/siddiq90/Documents/buildtest/tutorials/compilers/src/hello_omp.c
    ./$_EXEC


Similarly, one can define environment variables at the compiler level in ``config`` section.
buildtest will override value defined in ``default`` section. In this example, we
make slight modification to the test, so that ``gcc/10.2.0-37fmsw7`` will use 4 threads
when running program. This will override the default value of 2.

.. program-output:: cat ../tutorials/compilers/envvar_override.yml

Next we build this test as follows:

.. code-block:: console


    $ buildtest build -b tutorials/compilers/envvar_override.yml


    User:  siddiq90
    Hostname:  DOE-7086392.local
    Platform:  Darwin
    Current Time:  2021/06/10 22:04:19
    buildtest path: /Users/siddiq90/Documents/GitHubDesktop/buildtest/bin/buildtest
    buildtest version:  0.9.5
    python path: /Users/siddiq90/.local/share/virtualenvs/buildtest-KLOcDrW0/bin/python
    python version:  3.7.3
    Test Directory:  /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests
    Configuration File:  /Users/siddiq90/.buildtest/config.yml
    Command: /Users/siddiq90/Documents/GitHubDesktop/buildtest/bin/buildtest build -b tutorials/compilers/envvar_override.yml

    +-------------------------------+
    | Stage: Discovering Buildspecs |
    +-------------------------------+

    +-------------------------------------------------------------------------------------------+
    | Discovered Buildspecs                                                                     |
    +===========================================================================================+
    | /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/compilers/envvar_override.yml |
    +-------------------------------------------------------------------------------------------+
    Discovered Buildspecs:  1
    Excluded Buildspecs:  0
    Detected Buildspecs after exclusion:  1

    +---------------------------+
    | Stage: Parsing Buildspecs |
    +---------------------------+

     schemafile                | validstate   | buildspec
    ---------------------------+--------------+-------------------------------------------------------------------------------------------
     compiler-v1.0.schema.json | True         | /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/compilers/envvar_override.yml



    name                      description
    ------------------------  --------------------------------------
    override_environmentvars  override default environment variables
    override_environmentvars  override default environment variables

    +----------------------+
    | Stage: Building Test |
    +----------------------+



     name                     | id       | type     | executor           | tags                     | compiler           | testpath
    --------------------------+----------+----------+--------------------+--------------------------+--------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------
     override_environmentvars | 72619a4b | compiler | generic.local.bash | ['tutorials', 'compile'] | gcc/9.3.0-n7p74fd  | /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.bash/envvar_override/override_environmentvars/0/override_environmentvars_build.sh
     override_environmentvars | 31098506 | compiler | generic.local.bash | ['tutorials', 'compile'] | gcc/10.2.0-37fmsw7 | /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.bash/envvar_override/override_environmentvars/1/override_environmentvars_build.sh

    +---------------------+
    | Stage: Running Test |
    +---------------------+

     name                     | id       | executor           | status   |   returncode
    --------------------------+----------+--------------------+----------+--------------
     override_environmentvars | 72619a4b | generic.local.bash | PASS     |            0
     override_environmentvars | 31098506 | generic.local.bash | PASS     |            0

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Passed Tests: 2/2 Percentage: 100.000%
    Failed Tests: 0/2 Percentage: 0.000%


    Writing Logfile to: /Users/siddiq90/buildtest/buildtest_p3wdnl1t.log
    A copy of logfile can be found at $BUILDTEST_ROOT/buildtest.log -  /Users/siddiq90/Documents/GitHubDesktop/buildtest/buildtest.log

Now let's inspect the test by running ``buildtest inspect name`` and we notice there are two test records for `override_environmentvars` using
**gcc/9.3.0-n7p74fd** and **gcc/10.2.0-37fmsw7**.


.. code-block:: console
    :linenos:
    :emphasize-lines: 12,41

    $ buildtest inspect name override_environmentvars
    Reading Report File: /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/report.json

    {
      "override_environmentvars": [
        {
          "id": "72619a4b",
          "full_id": "72619a4b-3ed2-489c-aebd-2e0cacbf2d6a",
          "description": "override default environment variables",
          "schemafile": "compiler-v1.0.schema.json",
          "executor": "generic.local.bash",
          "compiler": "gcc/9.3.0-n7p74fd",
          "hostname": "DOE-7086392.local",
          "user": "siddiq90",
          "testroot": "/Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.bash/envvar_override/override_environmentvars/0",
          "testpath": "/Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.bash/envvar_override/override_environmentvars/0/stage/override_environmentvars.sh",
          "stagedir": "/Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.bash/envvar_override/override_environmentvars/0/stage",
          "command": "sh override_environmentvars_build.sh",
          "outfile": "/Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.bash/envvar_override/override_environmentvars/0/override_environmentvars.out",
          "errfile": "/Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.bash/envvar_override/override_environmentvars/0/override_environmentvars.err",
          "buildspec_content": "version: \"1.0\"\nbuildspecs:\n  override_environmentvars:\n    type: compiler\n    description: override default environment variables\n    executor: generic.local.bash\n    tags: [tutorials, compile]\n    source: \"src/hello_omp.c\"\n    compilers:\n      name: [\"^(gcc)\"]\n      default:\n        gcc:\n          cflags: -fopenmp\n          env:\n            OMP_NUM_THREADS: 2\n      config:\n        gcc/10.2.0-37fmsw7:\n          env:\n            OMP_NUM_THREADS: 4",
          "test_content": "#!/bin/bash \n_EXEC=hello_omp.c.exe\nexport OMP_NUM_THREADS=2\nmodule load gcc/9.3.0-n7p74fd\ngcc -fopenmp -o $_EXEC /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/compilers/src/hello_omp.c\n./$_EXEC",
          "logpath": "/Users/siddiq90/buildtest/buildtest_p3wdnl1t.log",
          "tags": "tutorials compile",
          "starttime": "2021/06/10 22:04:19",
          "endtime": "2021/06/10 22:04:20",
          "runtime": 0.727095,
          "state": "PASS",
          "returncode": 0,
          "output": "Hello World from thread = 0\nHello World from thread = 1\n",
          "error": "The following have been reloaded with a version change:\n  1) gcc/10.2.0-37fmsw7 => gcc/9.3.0-n7p74fd\n",
          "job": null,
          "build_script": "/Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.bash/envvar_override/override_environmentvars/0/override_environmentvars_build.sh"
        },
        {
          "id": "31098506",
          "full_id": "31098506-2bbf-4a50-8386-2fcd5bcddff5",
          "description": "override default environment variables",
          "schemafile": "compiler-v1.0.schema.json",
          "executor": "generic.local.bash",
          "compiler": "gcc/10.2.0-37fmsw7",
          "hostname": "DOE-7086392.local",
          "user": "siddiq90",
          "testroot": "/Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.bash/envvar_override/override_environmentvars/1",
          "testpath": "/Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.bash/envvar_override/override_environmentvars/1/stage/override_environmentvars.sh",
          "stagedir": "/Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.bash/envvar_override/override_environmentvars/1/stage",
          "command": "sh override_environmentvars_build.sh",
          "outfile": "/Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.bash/envvar_override/override_environmentvars/1/override_environmentvars.out",
          "errfile": "/Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.bash/envvar_override/override_environmentvars/1/override_environmentvars.err",
          "buildspec_content": "version: \"1.0\"\nbuildspecs:\n  override_environmentvars:\n    type: compiler\n    description: override default environment variables\n    executor: generic.local.bash\n    tags: [tutorials, compile]\n    source: \"src/hello_omp.c\"\n    compilers:\n      name: [\"^(gcc)\"]\n      default:\n        gcc:\n          cflags: -fopenmp\n          env:\n            OMP_NUM_THREADS: 2\n      config:\n        gcc/10.2.0-37fmsw7:\n          env:\n            OMP_NUM_THREADS: 4",
          "test_content": "#!/bin/bash \n_EXEC=hello_omp.c.exe\nexport OMP_NUM_THREADS=4\nmodule load gcc/10.2.0-37fmsw7\ngcc -fopenmp -o $_EXEC /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/compilers/src/hello_omp.c\n./$_EXEC",
          "logpath": "/Users/siddiq90/buildtest/buildtest_p3wdnl1t.log",
          "tags": "tutorials compile",
          "starttime": "2021/06/10 22:04:20",
          "endtime": "2021/06/10 22:04:20",
          "runtime": 0.482645,
          "state": "PASS",
          "returncode": 0,
          "output": "Hello World from thread = 1\nHello World from thread = 3\nHello World from thread = 2\nHello World from thread = 0\n",
          "error": "",
          "job": null,
          "build_script": "/Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.bash/envvar_override/override_environmentvars/1/override_environmentvars_build.sh"
        }
      ]
    }

Tweak how test are passed
--------------------------

The ``status`` property can be used to determine how buildtest will pass the test. By
default, buildtest will use returncode to determine if test ``PASS`` or ``FAIL`` with
exitcode 0 as PASS and anything else is FAIL.

Sometimes, it may be useful check output of test to determine using regular expression. This
can be done via ``status`` property. In this example, we define two tests, the first one defines ``status``
property in the default **gcc** group. This means all compilers that belong to gcc
group will be matched with the regular expression.

In second example we override the status ``regex`` property for **gcc/10.2.0-37fmsw7**. We expect
the test to produce an output of ``final result: 1.000000`` so we expect one failure from
**gcc/10.2.0-37fmsw7**.

.. program-output:: cat ../tutorials/compilers/compiler_status_regex.yml


If we build this test, notice that test id **9320ca41** failed which corresponds to
``gcc/10.2.0-37fmsw7`` compiler test. The test fails because it fails to pass on
regular expression even though we have a returncode of 0.

.. code-block:: console
    :linenos:
    :emphasize-lines: 68

    $ buildtest build -b tutorials/compilers/compiler_status_regex.yml


    User:  siddiq90
    Hostname:  DOE-7086392.local
    Platform:  Darwin
    Current Time:  2021/06/10 22:08:03
    buildtest path: /Users/siddiq90/Documents/GitHubDesktop/buildtest/bin/buildtest
    buildtest version:  0.9.5
    python path: /Users/siddiq90/.local/share/virtualenvs/buildtest-KLOcDrW0/bin/python
    python version:  3.7.3
    Test Directory:  /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests
    Configuration File:  /Users/siddiq90/.buildtest/config.yml
    Command: /Users/siddiq90/Documents/GitHubDesktop/buildtest/bin/buildtest build -b tutorials/compilers/compiler_status_regex.yml

    +-------------------------------+
    | Stage: Discovering Buildspecs |
    +-------------------------------+

    +-------------------------------------------------------------------------------------------------+
    | Discovered Buildspecs                                                                           |
    +=================================================================================================+
    | /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/compilers/compiler_status_regex.yml |
    +-------------------------------------------------------------------------------------------------+
    Discovered Buildspecs:  1
    Excluded Buildspecs:  0
    Detected Buildspecs after exclusion:  1

    +---------------------------+
    | Stage: Parsing Buildspecs |
    +---------------------------+

     schemafile                | validstate   | buildspec
    ---------------------------+--------------+-------------------------------------------------------------------------------------------------
     compiler-v1.0.schema.json | True         | /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/compilers/compiler_status_regex.yml



    name                   description
    ---------------------  -----------------------------------------------------------
    default_status_regex   Regular expression check in stdout for gcc group
    default_status_regex   Regular expression check in stdout for gcc group
    override_status_regex  Override regular expression for compiler gcc/10.2.0-37fmsw7
    override_status_regex  Override regular expression for compiler gcc/10.2.0-37fmsw7

    +----------------------+
    | Stage: Building Test |
    +----------------------+



     name                  | id       | type     | executor           | tags                     | compiler           | testpath
    -----------------------+----------+----------+--------------------+--------------------------+--------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------
     default_status_regex  | a023a2c2 | compiler | generic.local.bash | ['tutorials', 'compile'] | gcc/9.3.0-n7p74fd  | /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.bash/compiler_status_regex/default_status_regex/0/default_status_regex_build.sh
     default_status_regex  | 155865c3 | compiler | generic.local.bash | ['tutorials', 'compile'] | gcc/10.2.0-37fmsw7 | /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.bash/compiler_status_regex/default_status_regex/1/default_status_regex_build.sh
     override_status_regex | 3411bddf | compiler | generic.local.bash | ['tutorials', 'compile'] | gcc/9.3.0-n7p74fd  | /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.bash/compiler_status_regex/override_status_regex/0/override_status_regex_build.sh
     override_status_regex | 295310a4 | compiler | generic.local.bash | ['tutorials', 'compile'] | gcc/10.2.0-37fmsw7 | /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.bash/compiler_status_regex/override_status_regex/1/override_status_regex_build.sh

    +---------------------+
    | Stage: Running Test |
    +---------------------+

     name                  | id       | executor           | status   |   returncode
    -----------------------+----------+--------------------+----------+--------------
     default_status_regex  | a023a2c2 | generic.local.bash | PASS     |            0
     default_status_regex  | 155865c3 | generic.local.bash | PASS     |            0
     override_status_regex | 3411bddf | generic.local.bash | PASS     |            0
     override_status_regex | 295310a4 | generic.local.bash | FAIL     |            0

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Passed Tests: 3/4 Percentage: 75.000%
    Failed Tests: 1/4 Percentage: 25.000%


    Writing Logfile to: /Users/siddiq90/buildtest/buildtest_hp7_gpbn.log
    A copy of logfile can be found at $BUILDTEST_ROOT/buildtest.log -  /Users/siddiq90/Documents/GitHubDesktop/buildtest/buildtest.log

Single Test Multiple Compilers
-------------------------------

It's possible to run single test across multiple compilers (gcc, intel, cray, etc...). In the
next example, we will build an OpenMP reduction test using gcc, intel and cray compilers. In this
test, we use ``name`` field to select compilers that start with **gcc**, **intel** and **PrgEnv-cray**
as compiler names. The ``default`` section is organized by compiler groups which inherits compiler flags
for all compilers. OpenMP flag for gcc, intel and cray differ for instance one must use ``-fopenmp`` for gcc,
``--qopenmp`` for intel and ``-h omp`` for cray.

.. code-block:: yaml

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

    cori$ buildtest build -b reduction.yml

    +-------------------------------+
    | Stage: Discovering Buildspecs |
    +-------------------------------+


    Discovered Buildspecs:

    /global/u1/s/siddiq90/buildtest-cori/apps/openmp/reduction.yml

    +---------------------------+
    | Stage: Parsing Buildspecs |
    +---------------------------+

     schemafile                | validstate   | buildspec
    ---------------------------+--------------+----------------------------------------------------------------
     compiler-v1.0.schema.json | True         | /global/u1/s/siddiq90/buildtest-cori/apps/openmp/reduction.yml

    +----------------------+
    | Stage: Building Test |
    +----------------------+



     name      | id       | type     | executor   | tags       | compiler                                | testpath
    -----------+----------+----------+------------+------------+-----------------------------------------+-----------------------------------------------------------------------------------------------
     reduction | 4eb31800 | compiler | local.bash | ['openmp'] | gcc/6.1.0                               | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/72/stage/generate.sh
     reduction | 514a32a1 | compiler | local.bash | ['openmp'] | gcc/7.3.0                               | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/73/stage/generate.sh
     reduction | 9bb7a57c | compiler | local.bash | ['openmp'] | gcc/8.1.0                               | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/74/stage/generate.sh
     reduction | 91e61ba6 | compiler | local.bash | ['openmp'] | gcc/8.2.0                               | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/75/stage/generate.sh
     reduction | f6a8d54e | compiler | local.bash | ['openmp'] | gcc/8.3.0                               | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/76/stage/generate.sh
     reduction | 29490f3a | compiler | local.bash | ['openmp'] | gcc/9.3.0                               | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/77/stage/generate.sh
     reduction | 5e58e1cf | compiler | local.bash | ['openmp'] | gcc/10.1.0                              | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/78/stage/generate.sh
     reduction | a4e696d3 | compiler | local.bash | ['openmp'] | gcc/6.3.0                               | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/79/stage/generate.sh
     reduction | c571b53e | compiler | local.bash | ['openmp'] | gcc/8.1.1-openacc-gcc-8-branch-20190215 | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/80/stage/generate.sh
     reduction | b7cba893 | compiler | local.bash | ['openmp'] | PrgEnv-cray/6.0.5                       | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/81/stage/generate.sh
     reduction | 67f9d327 | compiler | local.bash | ['openmp'] | PrgEnv-cray/6.0.7                       | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/82/stage/generate.sh
     reduction | 16713092 | compiler | local.bash | ['openmp'] | PrgEnv-cray/6.0.9                       | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/83/stage/generate.sh
     reduction | f5982111 | compiler | local.bash | ['openmp'] | intel/19.0.3.199                        | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/84/stage/generate.sh
     reduction | c2b22eff | compiler | local.bash | ['openmp'] | intel/19.1.2.254                        | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/85/stage/generate.sh
     reduction | e3f6faa4 | compiler | local.bash | ['openmp'] | intel/16.0.3.210                        | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/86/stage/generate.sh
     reduction | d95a3883 | compiler | local.bash | ['openmp'] | intel/17.0.1.132                        | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/87/stage/generate.sh
     reduction | 0aee1fee | compiler | local.bash | ['openmp'] | intel/17.0.2.174                        | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/88/stage/generate.sh
     reduction | 853d3ff4 | compiler | local.bash | ['openmp'] | intel/18.0.1.163                        | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/89/stage/generate.sh
     reduction | 0e66bc4a | compiler | local.bash | ['openmp'] | intel/18.0.3.222                        | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/90/stage/generate.sh
     reduction | 69826793 | compiler | local.bash | ['openmp'] | intel/19.0.0.117                        | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/91/stage/generate.sh
     reduction | f67d8953 | compiler | local.bash | ['openmp'] | intel/19.0.8.324                        | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/92/stage/generate.sh
     reduction | e12ac611 | compiler | local.bash | ['openmp'] | intel/19.1.0.166                        | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/93/stage/generate.sh
     reduction | fc8386f4 | compiler | local.bash | ['openmp'] | intel/19.1.1.217                        | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/94/stage/generate.sh
     reduction | 80e39fa5 | compiler | local.bash | ['openmp'] | intel/19.1.2.275                        | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/95/stage/generate.sh
     reduction | b9181f22 | compiler | local.bash | ['openmp'] | intel/19.1.3.304                        | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/96/stage/generate.sh

    +----------------------+
    | Stage: Running Test  |
    +----------------------+

     name      | id       | executor   | status   |   returncode | testpath
    -----------+----------+------------+----------+--------------+-----------------------------------------------------------------------------------------------
     reduction | 4eb31800 | local.bash | PASS     |            0 | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/72/stage/generate.sh
     reduction | 514a32a1 | local.bash | PASS     |            0 | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/73/stage/generate.sh
     reduction | 9bb7a57c | local.bash | PASS     |            0 | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/74/stage/generate.sh
     reduction | 91e61ba6 | local.bash | PASS     |            0 | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/75/stage/generate.sh
     reduction | f6a8d54e | local.bash | PASS     |            0 | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/76/stage/generate.sh
     reduction | 29490f3a | local.bash | PASS     |            0 | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/77/stage/generate.sh
     reduction | 5e58e1cf | local.bash | PASS     |            0 | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/78/stage/generate.sh
     reduction | a4e696d3 | local.bash | PASS     |            0 | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/79/stage/generate.sh
     reduction | c571b53e | local.bash | PASS     |            0 | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/80/stage/generate.sh
     reduction | b7cba893 | local.bash | PASS     |            0 | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/81/stage/generate.sh
     reduction | 67f9d327 | local.bash | PASS     |            0 | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/82/stage/generate.sh
     reduction | 16713092 | local.bash | PASS     |            0 | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/83/stage/generate.sh
     reduction | f5982111 | local.bash | PASS     |            0 | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/84/stage/generate.sh
     reduction | c2b22eff | local.bash | PASS     |            0 | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/85/stage/generate.sh
     reduction | e3f6faa4 | local.bash | PASS     |            0 | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/86/stage/generate.sh
     reduction | d95a3883 | local.bash | PASS     |            0 | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/87/stage/generate.sh
     reduction | 0aee1fee | local.bash | PASS     |            0 | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/88/stage/generate.sh
     reduction | 853d3ff4 | local.bash | PASS     |            0 | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/89/stage/generate.sh
     reduction | 0e66bc4a | local.bash | PASS     |            0 | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/90/stage/generate.sh
     reduction | 69826793 | local.bash | PASS     |            0 | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/91/stage/generate.sh
     reduction | f67d8953 | local.bash | PASS     |            0 | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/92/stage/generate.sh
     reduction | e12ac611 | local.bash | PASS     |            0 | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/93/stage/generate.sh
     reduction | fc8386f4 | local.bash | PASS     |            0 | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/94/stage/generate.sh
     reduction | 80e39fa5 | local.bash | PASS     |            0 | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/95/stage/generate.sh
     reduction | b9181f22 | local.bash | PASS     |            0 | /global/u1/s/siddiq90/buildtest/var/tests/local.bash/reduction/reduction/96/stage/generate.sh

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Executed 25 tests
    Passed Tests: 25/25 Percentage: 100.000%
    Failed Tests: 0/25 Percentage: 0.000%

    Writing Logfile to: /private/tmp/buildtest/buildtest_b41hm3n7.log

If we inspect one of these tests from each compiler group we will see OMP_NUM_THREADS
is set in all tests along with the appropriate compiler flag.

.. code-block:: shell
   :linenos:
   :emphasize-lines: 4-6

    #!/bin/bash
    source /global/u1/s/siddiq90/buildtest/var/executors/local.bash/before_script.sh
    _EXEC=reduction.c.exe
    export OMP_NUM_THREADS=4
    module load gcc/6.1.0
    gcc -fopenmp -o $_EXEC /global/u1/s/siddiq90/buildtest-cori/apps/openmp/src/reduction.c
    ./$_EXEC
    source /global/u1/s/siddiq90/buildtest/var/executors/local.bash/after_script.sh

.. code-block:: shell
   :linenos:
   :emphasize-lines: 4-6

    #!/bin/bash
    source /global/u1/s/siddiq90/buildtest/var/executors/local.bash/before_script.sh
    _EXEC=reduction.c.exe
    export OMP_NUM_THREADS=4
    module load PrgEnv-cray/6.0.5
    cc -h omp -o $_EXEC /global/u1/s/siddiq90/buildtest-cori/apps/openmp/src/reduction.c
    ./$_EXEC
    source /global/u1/s/siddiq90/buildtest/var/executors/local.bash/after_script.sh

.. code-block:: shell
   :linenos:
   :emphasize-lines: 4-6

    #!/bin/bash
    source /global/u1/s/siddiq90/buildtest/var/executors/local.bash/before_script.sh
    _EXEC=reduction.c.exe
    export OMP_NUM_THREADS=4
    module load intel/19.0.3.199
    icc -qopenmp -o $_EXEC /global/u1/s/siddiq90/buildtest-cori/apps/openmp/src/reduction.c
    ./$_EXEC
    source /global/u1/s/siddiq90/buildtest/var/executors/local.bash/after_script.sh

Customize Run Line
-------------------

buildtest will define variable ``_EXEC`` in the job script that can be used to reference
the generated binary. By default, buildtest will run the program standalone, but sometimes you
may want to customize how job is run. This may include passing arguments or running
binary through a job/mpi launcher. The ``run`` property expects user to specify how to launch
program. buildtest will change directory to the called script before running executable. The compiled
executable will be present in local directory which can be accessed via ``./$_EXEC``. In example below
we pass arguments ``1 3 5`` for gcc group and ``100 200`` for compiler ``gcc/10.2.0-37fmsw7``.

.. program-output:: cat ../tutorials/compilers/custom_run.yml

If we build this test and see generated test, we notice buildtest customized the run line
for launching binary. buildtest will directly replace content in ``run`` section into the
shell-script. If no ``run`` field is specified buildtest will run the binary in standalone mode (``./$_EXEC``).

.. code-block:: shell
   :linenos:
   :emphasize-lines: 6

    #!/bin/bash
    source /Users/siddiq90/Documents/buildtest/var/executors/local.bash/before_script.sh
    _EXEC=argc.c.exe
    module load gcc/10.2.0-37fmsw7
    gcc -o $_EXEC /Users/siddiq90/Documents/buildtest/tutorials/compilers/src/argc.c
    ./$_EXEC 100 120
    source /Users/siddiq90/Documents/buildtest/var/executors/local.bash/after_script.sh

.. code-block:: shell
   :linenos:
   :emphasize-lines: 6

    #!/bin/bash
    source /Users/siddiq90/Documents/buildtest/var/executors/local.bash/before_script.sh
    _EXEC=argc.c.exe
    module load gcc/9.3.0-n7p74fd
    gcc -o $_EXEC /Users/siddiq90/Documents/buildtest/tutorials/compilers/src/argc.c
    ./$_EXEC 1 3 5
    source /Users/siddiq90/Documents/buildtest/var/executors/local.bash/after_script.sh

MPI Example
------------

In this example we run a MPI Laplace code using 4 process on a KNL node using
the ``intel/19.1.2.254`` compiler. This test is run on Cori through batch queue
system. We can define #SBATCH parameters using ``sbatch`` property. This program
is compiled using ``mpiicc`` wrapper this can be defined using ``cc`` parameter.

Currently, buildtest cannot detect if program is serial or MPI to infer appropriate
compiler wrapper. If ``cc`` wasn't specified, buildtest would infer `icc` as compiler
wrapper for C program. This program is run using ``srun`` job launcher, we can control
how test is executed using the ``run`` property. This test required we swap intel
modules and load `impi/2020` module.

.. code-block:: yaml

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

The generated test is as follows, note that buildtest will insert ``module load`` before ``module swap``
command.

.. code-block:: shell

    #!/bin/bash
    #SBATCH -N 1
    #SBATCH -n 4
    #SBATCH --job-name=laplace_mpi
    #SBATCH --output=laplace_mpi.out
    #SBATCH --error=laplace_mpi.err
    source /global/u1/s/siddiq90/buildtest/var/executors/slurm.knl_debug/before_script.sh
    _EXEC=laplace_mpi.c.exe
    module load impi/2020
    module swap intel intel/19.1.2.254
    mpiicc -O3 -o $_EXEC /global/u1/s/siddiq90/buildtest-cori/apps/mpi/src/laplace_mpi.c
    srun -n 4 $_EXEC
    source /global/u1/s/siddiq90/buildtest/var/executors/slurm.knl_debug/after_script.sh


Shown below is a sample build for this buildspec, buildtest will dispatch  job and poll
job until its complete.

.. code-block:: console

    $ buildtest build -b laplace_mpi.yml

    +-------------------------------+
    | Stage: Discovering Buildspecs |
    +-------------------------------+


    Discovered Buildspecs:

    /global/u1/s/siddiq90/buildtest-cori/apps/mpi/laplace_mpi.yml

    +---------------------------+
    | Stage: Parsing Buildspecs |
    +---------------------------+

     schemafile                | validstate   | buildspec
    ---------------------------+--------------+---------------------------------------------------------------
     compiler-v1.0.schema.json | True         | /global/u1/s/siddiq90/buildtest-cori/apps/mpi/laplace_mpi.yml

    +----------------------+
    | Stage: Building Test |
    +----------------------+



     name        | id       | type     | executor        | tags    | compiler         | testpath
    -------------+----------+----------+-----------------+---------+------------------+-------------------------------------------------------------------------------------------------------
     laplace_mpi | 0c1e082e | compiler | slurm.knl_debug | ['mpi'] | intel/19.1.2.254 | /global/u1/s/siddiq90/buildtest/var/tests/slurm.knl_debug/laplace_mpi/laplace_mpi/4/stage/generate.sh

    +----------------------+
    | Stage: Running Test  |
    +----------------------+

    [laplace_mpi] JobID: 37707966 dispatched to scheduler
     name        | id       | executor        | status   |   returncode | testpath
    -------------+----------+-----------------+----------+--------------+-------------------------------------------------------------------------------------------------------
     laplace_mpi | 0c1e082e | slurm.knl_debug | N/A      |           -1 | /global/u1/s/siddiq90/buildtest/var/tests/slurm.knl_debug/laplace_mpi/laplace_mpi/4/stage/generate.sh


    Polling Jobs in 10 seconds
    ________________________________________
    [laplace_mpi]: JobID 37707966 in RUNNING state


    Polling Jobs in 10 seconds
    ________________________________________
    [laplace_mpi]: JobID 37707966 in RUNNING state


    Polling Jobs in 10 seconds
    ________________________________________
    [laplace_mpi]: JobID 37707966 in RUNNING state


    Polling Jobs in 10 seconds
    ________________________________________
    [laplace_mpi]: JobID 37707966 in RUNNING state


    Polling Jobs in 10 seconds
    ________________________________________
    [laplace_mpi]: JobID 37707966 in COMPLETED state


    Polling Jobs in 10 seconds
    ________________________________________

        +---------------------------------------------+
        | Stage: Final Results after Polling all Jobs |
        +---------------------------------------------+

     name        | id       | executor        | status   |   returncode | testpath
    -------------+----------+-----------------+----------+--------------+-------------------------------------------------------------------------------------------------------
     laplace_mpi | 0c1e082e | slurm.knl_debug | PASS     |            0 | /global/u1/s/siddiq90/buildtest/var/tests/slurm.knl_debug/laplace_mpi/laplace_mpi/4/stage/generate.sh

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Executed 1 tests
    Passed Tests: 1/1 Percentage: 100.000%
    Failed Tests: 0/1 Percentage: 0.000%

    Writing Logfile to: /private/tmp/buildtest/buildtest_b41hm3n7.log

Pre/Post sections for build and run section
--------------------------------------------

The compiler schema comes with ``pre_build``, ``post_build``, ``pre_run`` and
``post_run`` fields where you can insert commands before and after ``build`` or
``run`` section. The **build** section is where we compile code, and **run**
section is where compiled binary is executed.

Shown below is an example buildspec with pre/post section.

.. program-output:: cat ../tutorials/compilers/pre_post_build_run.yml


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

The generated test for this buildspec is the following:

.. code-block:: shell

    #!/bin/bash
    source /Users/siddiq90/Documents/buildtest/var/executors/local.bash/before_script.sh
    _EXEC=hello.c.exe
    echo "This is a pre-build section"
    gcc --version

    /usr/bin/gcc -o $_EXEC /Users/siddiq90/Documents/buildtest/tutorials/compilers/src/hello.c
    echo "This is post-build section"

    echo "This is pre-run section"
    export FOO=BAR

    ./$_EXEC
    echo "This is post-run section"

    source /Users/siddiq90/Documents/buildtest/var/executors/local.bash/after_script.sh
