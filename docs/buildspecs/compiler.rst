Compiler Schema
=================

The compiler schema is used for compilation of programs, currently we support
single source file compilation. In order to use the compiler schema you must set ``type: compiler`` in your
sub-schema. See `compiler schema docs <https://buildtesters.github.io/buildtest/pages/schemadocs/compiler-v1.html>`_


Compilation Examples
----------------------

We assume the reader has basic understanding of :ref:`global_schema`
validation. Shown below is the schema definition for compiler schema::

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

The generated test for test name **hello_f** is the following::

    #!/bin/bash
    source /Users/siddiq90/Documents/buildtest/var/executors/local.bash/before_script.sh
    _EXEC=hello.f90.exe
    /usr/local/bin/gfortran -o $_EXEC /Users/siddiq90/Documents/buildtest/tutorials/compilers/src/hello.f90
    ./$_EXEC
    source /Users/siddiq90/Documents/buildtest/var/executors/local.bash/after_script.sh


buildtest will use compiler wrappers specified in your settings
to build the test, however these values can be overridden in buildspec file which
will be discussed later.

The ``builtin_gcc`` compiler is defined below this can be retrieved by running
``buildtest config compilers``. The ``-y`` will display compilers in YAML format.

::

    $ buildtest config compilers -y
    gcc:
      builtin_gcc:
        cc: /usr/bin/gcc
        cxx: /usr/bin/g++
        fc: /usr/bin/gfortran

buildtest will compile and run the code depending on the compiler flags. buildtest,
will detect the file extension of source file (`source` property) to detect
programming language and finally generate the appropriate C, C++, or Fortran
compilation based on language detected. In this example, buildtest detects a
**.f90** file extension and buildtest infers this is a Fortran program.

Shown below is the file extension table for your reference

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
we select all compilers that starts with string ``gcc`` that is specified in line ``name: ["^(gcc)"]``

.. program-output:: cat ../tutorials/compilers/vecadd.yml

Currently, we have 3 compilers defined in buildtest settings, shown below is a listing
of all compilers::

    $ buildtest config compilers -l
    builtin_gcc
    gcc@10.2.0
    gcc@9.3.0

We expect buildtest to select ``gcc@10.2.0`` and ``gcc@9.3.0`` based on our regular expression. In the following
build, notice we have two tests for ``vecadd_gnu`` one for each compiler::

    $ buildtest build -b tutorials/compilers/vecadd.yml

    +-------------------------------+
    | Stage: Discovering Buildspecs |
    +-------------------------------+


    Discovered Buildspecs:

    /Users/siddiq90/Documents/buildtest/tutorials/compilers/vecadd.yml

    +---------------------------+
    | Stage: Parsing Buildspecs |
    +---------------------------+

     schemafile                | validstate   | buildspec
    ---------------------------+--------------+--------------------------------------------------------------------
     compiler-v1.0.schema.json | True         | /Users/siddiq90/Documents/buildtest/tutorials/compilers/vecadd.yml

    +----------------------+
    | Stage: Building Test |
    +----------------------+



     name       | id       | type     | executor   | tags                     | compiler   | testpath
    ------------+----------+----------+------------+--------------------------+------------+-------------------------------------------------------------------------------------------------
     vecadd_gnu | 6eaa56e1 | compiler | local.bash | ['tutorials', 'compile'] | gcc@10.2.0 | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/vecadd/vecadd_gnu/16/stage/generate.sh
     vecadd_gnu | 5f1359f6 | compiler | local.bash | ['tutorials', 'compile'] | gcc@9.3.0  | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/vecadd/vecadd_gnu/17/stage/generate.sh

    +----------------------+
    | Stage: Running Test  |
    +----------------------+

     name       | id       | executor   | status   |   returncode | testpath
    ------------+----------+------------+----------+--------------+-------------------------------------------------------------------------------------------------
     vecadd_gnu | 6eaa56e1 | local.bash | PASS     |            0 | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/vecadd/vecadd_gnu/16/stage/generate.sh
     vecadd_gnu | 5f1359f6 | local.bash | PASS     |            0 | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/vecadd/vecadd_gnu/17/stage/generate.sh

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Executed 2 tests
    Passed Tests: 2/2 Percentage: 100.000%
    Failed Tests: 0/2 Percentage: 0.000%


buildtest will use compiler settings including module configuration from buildtest
settings (``config.yml``). The module configuration for ``gcc@9.3.0`` and ``gcc@10.2.0``
is shown below. The ``module`` section is the declaration of modules to load, by default
we disable purge (``purge: False``) which instructs buildtest to not insert ``module purge``.
The ``load`` is a list of modules to load via ``module load``.

Shown below is the compiler configuration.

.. code-block::
    :emphasize-lines: 11-14,19-22
    :linenos:

    buildtest config compilers -y
    gcc:
      builtin_gcc:
        cc: /usr/bin/gcc
        cxx: /usr/bin/g++
        fc: /usr/local/bin/gfortran
      gcc@10.2.0:
        cc: gcc
        cxx: g++
        fc: gfortran
        module:
          load:
          - gcc/10.2.0-37fmsw7
          purge: false
      gcc@9.3.0:
        cc: gcc
        cxx: g++
        fc: gfortran
        module:
          load:
          - gcc/9.3.0-n7p74fd
          purge: false

If we take a closer look at the generated test we see the modules are loaded into the test script.

.. code-block::
    :emphasize-lines: 4
    :linenos:

    #!/bin/bash
    source /Users/siddiq90/Documents/buildtest/var/executors/local.bash/before_script.sh
    _EXEC=vecAdd.c.exe
    module load gcc/10.2.0-37fmsw7
    gcc -o $_EXEC /Users/siddiq90/Documents/buildtest/tutorials/compilers/src/vecAdd.c
    ./$_EXEC
    source /Users/siddiq90/Documents/buildtest/var/executors/local.bash/after_script.sh


.. code-block::
    :emphasize-lines: 4
    :linenos:

    #!/bin/bash
    source /Users/siddiq90/Documents/buildtest/var/executors/local.bash/before_script.sh
    _EXEC=vecAdd.c.exe
    module load gcc/9.3.0-n7p74fd
    gcc -o $_EXEC /Users/siddiq90/Documents/buildtest/tutorials/compilers/src/vecAdd.c
    ./$_EXEC
    source /Users/siddiq90/Documents/buildtest/var/executors/local.bash/after_script.sh

Excluding Compilers
--------------------

The ``exclude`` property is part of compilers section which allows one to exclude compilers
upon discovery by ``name`` field. The exclude property is a list of compiler names that
will be removed from test generation which is done prior to build phase. buildtest will exclude
any compilers specified in ``exclude`` if they were found based on regular
expression in ``name`` field. In this example, we slightly modified previous example
by excluding ``gcc@10.2.0`` compiler. This is specified by ``exclude: [gcc@10.2.0]``.

.. program-output:: cat ../tutorials/compilers/compiler_exclude.yml

Notice when we build this test, buildtest will exclude ``gcc@10.2.0`` compiler
and test is not created during build phase.

.. code-block::
    :linenos:
    :emphasize-lines: 12

    $ buildtest build -b tutorials/compilers/compiler_exclude.yml

    +-------------------------------+
    | Stage: Discovering Buildspecs |
    +-------------------------------+


    Discovered Buildspecs:


    /Users/siddiq90/Documents/buildtest/tutorials/compilers/compiler_exclude.yml
    Excluding compiler: gcc@10.2.0 from test generation

    +---------------------------+
    | Stage: Parsing Buildspecs |
    +---------------------------+

     schemafile                | validstate   | buildspec
    ---------------------------+--------------+------------------------------------------------------------------------------
     compiler-v1.0.schema.json | True         | /Users/siddiq90/Documents/buildtest/tutorials/compilers/compiler_exclude.yml

    +----------------------+
    | Stage: Building Test |
    +----------------------+



     name               | id       | type     | executor   | tags                     | compiler   | testpath
    --------------------+----------+----------+------------+--------------------------+------------+------------------------------------------------------------------------------------------------------------------
     vecadd_gnu_exclude | 02b34a10 | compiler | local.bash | ['tutorials', 'compile'] | gcc@9.3.0  | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/compiler_exclude/vecadd_gnu_exclude/1/stage/generate.sh

    +----------------------+
    | Stage: Running Test  |
    +----------------------+

     name               | id       | executor   | status   |   returncode | testpath
    --------------------+----------+------------+----------+--------------+------------------------------------------------------------------------------------------------------------------
     vecadd_gnu_exclude | 02b34a10 | local.bash | PASS     |            0 | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/compiler_exclude/vecadd_gnu_exclude/1/stage/generate.sh

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Executed 1 tests
    Passed Tests: 1/1 Percentage: 100.000%
    Failed Tests: 0/1 Percentage: 0.000%

Compiler Defaults and Override Default Settings
-------------------------------------------------

Sometimes you may want to set default compiler flags (cflags, fflags, cxxflags) including
preprocessor (cppflags) or linker flags (ldflags) for compiler group (gcc, intel, pgi, etc...).
This can be achieved using the ``default`` property that is part of **compilers** section.

In the next example, we will use the three compilers: ``builtin_gcc``, ``gcc@9.3.0`` and ``gcc@10.2.0``
based on regular expression ``name: ["^(builtin_gcc|gcc)"]``. The ``default`` is
organized into compiler groups, in example below we set default C compiler flags
(``cflags: -O1``). In addition, we can override default settings using the
``config`` property where one must specify the compiler name to override.
In example below we will override ``gcc@9.3.0`` to use ``-O2`` for `cflags` and ``gcc@10.2.0`` will
use ``-O3``.

.. program-output:: cat ../tutorials/compilers/gnu_hello_c.yml

Next we run this test, and we get three tests for test name **hello_c**::

    $ buildtest build -b tutorials/compilers/gnu_hello_c.yml

    +-------------------------------+
    | Stage: Discovering Buildspecs |
    +-------------------------------+


    Discovered Buildspecs:

    /Users/siddiq90/Documents/buildtest/tutorials/compilers/gnu_hello_c.yml

    +---------------------------+
    | Stage: Parsing Buildspecs |
    +---------------------------+

     schemafile                | validstate   | buildspec
    ---------------------------+--------------+-------------------------------------------------------------------------
     compiler-v1.0.schema.json | True         | /Users/siddiq90/Documents/buildtest/tutorials/compilers/gnu_hello_c.yml

    +----------------------+
    | Stage: Building Test |
    +----------------------+



     name    | id       | type     | executor   | tags                     | compiler    | testpath
    ---------+----------+----------+------------+--------------------------+-------------+--------------------------------------------------------------------------------------------------
     hello_c | 23f6fd75 | compiler | local.bash | ['tutorials', 'compile'] | builtin_gcc | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/gnu_hello_c/hello_c/0/stage/generate.sh
     hello_c | 2eae9c20 | compiler | local.bash | ['tutorials', 'compile'] | gcc@10.2.0  | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/gnu_hello_c/hello_c/1/stage/generate.sh
     hello_c | d87b62e5 | compiler | local.bash | ['tutorials', 'compile'] | gcc@9.3.0   | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/gnu_hello_c/hello_c/2/stage/generate.sh

    +----------------------+
    | Stage: Running Test  |
    +----------------------+

     name    | id       | executor   | status   |   returncode | testpath
    ---------+----------+------------+----------+--------------+--------------------------------------------------------------------------------------------------
     hello_c | 23f6fd75 | local.bash | PASS     |            0 | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/gnu_hello_c/hello_c/0/stage/generate.sh
     hello_c | 2eae9c20 | local.bash | PASS     |            0 | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/gnu_hello_c/hello_c/1/stage/generate.sh
     hello_c | d87b62e5 | local.bash | PASS     |            0 | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/gnu_hello_c/hello_c/2/stage/generate.sh

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Executed 3 tests
    Passed Tests: 3/3 Percentage: 100.000%
    Failed Tests: 0/3 Percentage: 0.000%



If we inspect the following test, we see the compiler flags are associated with the compiler. The test below
is for `builtin_gcc` which use the default ``-O1`` compiler flag as shown below.

.. code-block::
    :emphasize-lines: 4
    :linenos:

    #!/bin/bash
    source /Users/siddiq90/Documents/buildtest/var/executors/local.bash/before_script.sh
    _EXEC=hello.c.exe
    /usr/bin/gcc -O1 -o $_EXEC /Users/siddiq90/Documents/buildtest/tutorials/compilers/src/hello.c
    ./$_EXEC

The test for `gcc@10.3.0` and `gcc@9.3.0` have cflags `-O3` and `-O2` set in their respective tests.

.. code-block::
    :emphasize-lines: 5
    :linenos:

    #!/bin/bash
    source /Users/siddiq90/Documents/buildtest/var/executors/local.bash/before_script.sh
    _EXEC=hello.c.exe
    module load gcc/10.2.0-37fmsw7
    gcc -O3 -o $_EXEC /Users/siddiq90/Documents/buildtest/tutorials/compilers/src/hello.c
    ./$_EXEC
    source /Users/siddiq90/Documents/buildtest/var/executors/local.bash/after_script.sh

.. code-block::
    :emphasize-lines: 5
    :linenos:

    #!/bin/bash
    source /Users/siddiq90/Documents/buildtest/var/executors/local.bash/before_script.sh
    _EXEC=hello.c.exe
    module load gcc/9.3.0-n7p74fd
    gcc -O2 -o $_EXEC /Users/siddiq90/Documents/buildtest/tutorials/compilers/src/hello.c
    ./$_EXEC
    source /Users/siddiq90/Documents/buildtest/var/executors/local.bash/after_script.sh

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

.. code-block::
    :emphasize-lines: 4
    :linenos:

    #!/bin/bash
    source /Users/siddiq90/Documents/buildtest/var/executors/local.bash/before_script.sh
    _EXEC=hello_omp.c.exe
    export OMP_NUM_THREADS=2
    module load gcc/10.2.0-37fmsw7
    gcc -fopenmp -o $_EXEC /Users/siddiq90/Documents/buildtest/tutorials/compilers/src/hello_omp.c
    ./$_EXEC
    source /Users/siddiq90/Documents/buildtest/var/executors/local.bash/after_script.sh


Similarly, one can define environment variables at the compiler level in ``config`` section.
buildtest will override value defined in ``default`` section. In this example, we
make slight modification to the test, so that ``gcc@10.2.0`` will use 4 threads
when running program. This will override the default value of 2.

.. program-output:: cat ../tutorials/compilers/envvar_override.yml

Next we build this test as follows::


    $ buildtest build -b tutorials/compilers/envvar_override.yml

    +-------------------------------+
    | Stage: Discovering Buildspecs |
    +-------------------------------+


    Discovered Buildspecs:

    /Users/siddiq90/Documents/buildtest/tutorials/compilers/envvar_override.yml

    +---------------------------+
    | Stage: Parsing Buildspecs |
    +---------------------------+

     schemafile                | validstate   | buildspec
    ---------------------------+--------------+-----------------------------------------------------------------------------
     compiler-v1.0.schema.json | True         | /Users/siddiq90/Documents/buildtest/tutorials/compilers/envvar_override.yml

    +----------------------+
    | Stage: Building Test |
    +----------------------+



     name                     | id       | type     | executor   | tags                     | compiler   | testpath
    --------------------------+----------+----------+------------+--------------------------+------------+-----------------------------------------------------------------------------------------------------------------------
     override_environmentvars | 87d53c7f | compiler | local.bash | ['tutorials', 'compile'] | gcc@10.2.0 | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/envvar_override/override_environmentvars/0/stage/generate.sh
     override_environmentvars | 9a59ea35 | compiler | local.bash | ['tutorials', 'compile'] | gcc@9.3.0  | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/envvar_override/override_environmentvars/1/stage/generate.sh

    +----------------------+
    | Stage: Running Test  |
    +----------------------+

     name                     | id       | executor   | status   |   returncode | testpath
    --------------------------+----------+------------+----------+--------------+-----------------------------------------------------------------------------------------------------------------------
     override_environmentvars | 87d53c7f | local.bash | PASS     |            0 | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/envvar_override/override_environmentvars/0/stage/generate.sh
     override_environmentvars | 9a59ea35 | local.bash | PASS     |            0 | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/envvar_override/override_environmentvars/1/stage/generate.sh

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Executed 2 tests
    Passed Tests: 2/2 Percentage: 100.000%
    Failed Tests: 0/2 Percentage: 0.000%


Now let's inspect the test for **gcc@10.2.0** and notice buildtest is using 4 threads for running OpenMP example

.. code-block::
    :linenos:
    :emphasize-lines: 25-28, 44

    $ buildtest inspect 87d53c7f
    {
      "id": "87d53c7f",
      "full_id": "87d53c7f-bee7-4d7b-8aa5-0e86e7a52998",
      "testroot": "/Users/siddiq90/Documents/buildtest/var/tests/local.bash/envvar_override/override_environmentvars/0",
      "testpath": "/Users/siddiq90/Documents/buildtest/var/tests/local.bash/envvar_override/override_environmentvars/0/stage/generate.sh",
      "command": "/Users/siddiq90/Documents/buildtest/var/tests/local.bash/envvar_override/override_environmentvars/0/stage/generate.sh",
      "outfile": "/Users/siddiq90/Documents/buildtest/var/tests/local.bash/envvar_override/override_environmentvars/0/run/override_environmentvars.out",
      "errfile": "/Users/siddiq90/Documents/buildtest/var/tests/local.bash/envvar_override/override_environmentvars/0/run/override_environmentvars.err",
      "schemafile": "compiler-v1.0.schema.json",
      "executor": "local.bash",
      "tags": "tutorials compile",
      "starttime": "2021/01/04 23:28:12",
      "endtime": "2021/01/04 23:28:13",
      "runtime": 0.6284978139999999,
      "state": "PASS",
      "returncode": 0,
      "job": null
    }



    Output File
    ______________________________
    Hello World from thread = 0
    Hello World from thread = 3
    Hello World from thread = 1
    Hello World from thread = 2




    Error File
    ______________________________




    Test Content
    ______________________________
    #!/bin/bash
    source /Users/siddiq90/Documents/buildtest/var/executors/local.bash/before_script.sh
    _EXEC=hello_omp.c.exe
    export OMP_NUM_THREADS=4
    module load gcc/10.2.0-37fmsw7
    gcc -fopenmp -o $_EXEC /Users/siddiq90/Documents/buildtest/tutorials/compilers/src/hello_omp.c
    ./$_EXEC
    source /Users/siddiq90/Documents/buildtest/var/executors/local.bash/after_script.sh



    buildspec:  /Users/siddiq90/Documents/buildtest/tutorials/compilers/envvar_override.yml
    ______________________________
    version: "1.0"
    buildspecs:
      override_environmentvars:
        type: compiler
        description: override default environment variables
        executor: local.bash
        tags: [tutorials, compile]
        source: "src/hello_omp.c"
        compilers:
          name: ["^(gcc)"]
          default:
            gcc:
              cflags: -fopenmp
              env:
                OMP_NUM_THREADS: 2
          config:
            gcc@10.2.0:
              env:
                OMP_NUM_THREADS: 4


Tweak how test are passed
--------------------------

The ``status`` property can be used to determine how buildtest will pass the test. By
default, buildtest will use returncode to determine if test ``PASS`` or ``FAIL`` with
exitcode 0 as PASS and anything else is FAIL.

Sometimes, it may be useful check output of test to determine using regular expression. This
can be done via ``status`` property. In this example, we define two tests, the first one defines ``status``
property in the default **gcc** group. This means all compilers that belong to gcc
group will be matched with the regular expression.

In second example we override the status ``regex`` property for **gcc@10.2.0**. We expect
the test to produce an output of ``final result: 1.000000`` so we expect one failure from
**gcc@10.2.0**.

.. program-output:: cat ../tutorials/compilers/compiler_status_regex.yml


If we build this test, notice that test id **e5426d1f** failed which corresponds to
``gcc@10.2.0`` compiler test. The test fails because it fails to pass on
regular expression even though we have a returncode of 0.

.. code-block::
    :linenos:
    :emphasize-lines: 30,41

    $ buildtest build -b tutorials/compilers/compiler_status_regex.yml

    +-------------------------------+
    | Stage: Discovering Buildspecs |
    +-------------------------------+


    Discovered Buildspecs:

    /Users/siddiq90/Documents/buildtest/tutorials/compilers/compiler_status_regex.yml

    +---------------------------+
    | Stage: Parsing Buildspecs |
    +---------------------------+

     schemafile                | validstate   | buildspec
    ---------------------------+--------------+-----------------------------------------------------------------------------------
     compiler-v1.0.schema.json | True         | /Users/siddiq90/Documents/buildtest/tutorials/compilers/compiler_status_regex.yml

    +----------------------+
    | Stage: Building Test |
    +----------------------+



     name                  | id       | type     | executor   | tags                     | compiler   | testpath
    -----------------------+----------+----------+------------+--------------------------+------------+--------------------------------------------------------------------------------------------------------------------------
     default_status_regex  | 2b63294c | compiler | local.bash | ['tutorials', 'compile'] | gcc@10.2.0 | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/compiler_status_regex/default_status_regex/0/stage/generate.sh
     default_status_regex  | 7be847e8 | compiler | local.bash | ['tutorials', 'compile'] | gcc@9.3.0  | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/compiler_status_regex/default_status_regex/1/stage/generate.sh
     override_status_regex | e5426d1f | compiler | local.bash | ['tutorials', 'compile'] | gcc@10.2.0 | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/compiler_status_regex/override_status_regex/0/stage/generate.sh
     override_status_regex | 1bcc7942 | compiler | local.bash | ['tutorials', 'compile'] | gcc@9.3.0  | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/compiler_status_regex/override_status_regex/1/stage/generate.sh

    +----------------------+
    | Stage: Running Test  |
    +----------------------+

     name                  | id       | executor   | status   |   returncode | testpath
    -----------------------+----------+------------+----------+--------------+--------------------------------------------------------------------------------------------------------------------------
     default_status_regex  | 2b63294c | local.bash | PASS     |            0 | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/compiler_status_regex/default_status_regex/0/stage/generate.sh
     default_status_regex  | 7be847e8 | local.bash | PASS     |            0 | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/compiler_status_regex/default_status_regex/1/stage/generate.sh
     override_status_regex | e5426d1f | local.bash | FAIL     |            0 | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/compiler_status_regex/override_status_regex/0/stage/generate.sh
     override_status_regex | 1bcc7942 | local.bash | PASS     |            0 | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/compiler_status_regex/override_status_regex/1/stage/generate.sh

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Executed 4 tests
    Passed Tests: 3/4 Percentage: 75.000%
    Failed Tests: 1/4 Percentage: 25.000%



Passing Arguments
-------------------

If you want to pass options to executable command use the ``args`` key. Shown
below is an example test

.. program-output:: cat ../tutorials/compilers/passing_args.yml

The exec_args will pass options to the executable, use this if your binary
requires input arguments. Shown below is a generated test::

    #!/bin/bash
    gcc -Wall -o argc.c.exe /global/u1/s/siddiq90/tutorials/examples/serial/src/argc.c
    ./argc.c.exe 1 2 3

OpenMP Example
----------------

Here is an example OpenMP reduction test that runs on 1 node using 32 tasks on a
haswell node::

    version: "1.0"
    buildspecs:
      reduction:
        type: compiler
        executor: slurm.debug
        sbatch: ["-N 1", "--ntasks-per-node 32", "-C haswell", "-t 1"]
        module:
          swap: [PrgEnv-intel, PrgEnv-gnu]
        env:
          OMP_NUM_THREADS: 32
          OMP_PROC_BIND: spread
          OMP_PLACES: cores
        build:
          source: src/reduction.c
          name: gnu
          cflags: -fopenmp
        tags: [openmp]

In this example, we use the SlurmExecutor ``slurm.debug``, the source file is
``src/reduction.c`` that is relative to buildspec file. The environment variables
are defined using ``env`` section. To enable openmp flag, for GNU compilers we
pass ``-fopenmp`` to C compiler. By default, `PrgEnv-intel` module is loaded at startup
on Cori system so we can use ``swap`` property to swap **PrgEnv-intel** with **PrgEnv-gnu**.
Finally we classify this test using ``tags`` key which is set to `openmp`.

The generated test looks as follows::

    #!/bin/bash
    #SBATCH -N 1
    #SBATCH --ntasks-per-node 32
    #SBATCH -C haswell
    #SBATCH -t 1
    #SBATCH --job-name=reduction
    #SBATCH --output=reduction.out
    #SBATCH --error=reduction.err
    source /global/u1/s/siddiq90/buildtest/var/executors/slurm.debug/before_script.sh
    export OMP_NUM_THREADS=32
    export OMP_PROC_BIND=spread
    export OMP_PLACES=cores
    module swap PrgEnv-intel PrgEnv-gnu
    gcc -fopenmp -o reduction.c.exe src/reduction.c
    ./reduction.c.exe
    source /global/u1/s/siddiq90/buildtest/var/executors/slurm.debug/after_script.sh

MPI Example
------------

In this example we run a MPI Laplace code using 4 process on a KNL node using
the module ``PrgEnv-intel`` and ``intel/19.1.2.254``. The executable is launched
using ``srun``, that is set via ``launcher`` field. The source code
``src/laplace_mpi.c`` must be run with 4 process, for this test we allocate 1
node with 4 tasks.

The ``name`` field is a required field, buildtest uses this field to select the
appropriate subclass, when you set ``name: intel`` buildtest will select the IntelCompiler
subclass which sets the ``cc``, ``fc`` and ``cxx`` variables automatically. If you
want to specify your compiler variables you can use ``cc``, ``fc`` and ``cxx`` fields
and buildtest will honor your options.

::

    version: "1.0"
    buildspecs:
      laplace_mpi:
        type: compiler
        description: Laplace MPI code in C
        sbatch: ["-C knl", "-N 1", "-n 4"]
        executor: slurm.debug
        tags: ["mpi"]
        module:
          load: [PrgEnv-intel, intel/19.1.2.254]
        build:
          name: intel
          source: src/laplace_mpi.c
          cflags: -O3
        run:
          launcher: srun -n 4

The generated test is as follows::

    #!/bin/bash
    #SBATCH -C knl
    #SBATCH -N 1
    #SBATCH -n 4
    #SBATCH --job-name=laplace_mpi
    #SBATCH --output=laplace_mpi.out
    #SBATCH --error=laplace_mpi.err
    source /global/u1/s/siddiq90/buildtest/var/executors/slurm.debug/before_script.sh
    module load PrgEnv-intel
    module load intel/19.1.2.254
    icc -O3 -o laplace_mpi.c.exe src/laplace_mpi.c
    srun -n 4 ./laplace_mpi.c.exe
    source /global/u1/s/siddiq90/buildtest/var/executors/slurm.debug/after_script.sh


Shown below is a sample build for this buildspec::

    $ buildtest build -b apps/mpi/laplace_mpi.yml

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

     name        | id       | type     | executor    | tags    | testpath
    -------------+----------+----------+-------------+---------+---------------------------------------------------------------------------------------------------
     laplace_mpi | fdad3653 | compiler | slurm.debug | ['mpi'] | /global/u1/s/siddiq90/buildtest/var/tests/slurm.debug/laplace_mpi/laplace_mpi/0/stage/generate.sh

    +----------------------+
    | Stage: Running Test  |
    +----------------------+

    [laplace_mpi] JobID: 36779045 dispatched to scheduler
     name        | id       | executor    | status   |   returncode | testpath
    -------------+----------+-------------+----------+--------------+---------------------------------------------------------------------------------------------------
     laplace_mpi | fdad3653 | slurm.debug | N/A      |           -1 | /global/u1/s/siddiq90/buildtest/var/tests/slurm.debug/laplace_mpi/laplace_mpi/0/stage/generate.sh


    Polling Jobs in 10 seconds
    ________________________________________
    [laplace_mpi]: JobID 36779045 in COMPLETED state


    Polling Jobs in 10 seconds
    ________________________________________

    +---------------------------------------------+
    | Stage: Final Results after Polling all Jobs |
    +---------------------------------------------+

     name        | id       | executor    | status   |   returncode | testpath
    -------------+----------+-------------+----------+--------------+---------------------------------------------------------------------------------------------------
     laplace_mpi | fdad3653 | slurm.debug | PASS     |            0 | /global/u1/s/siddiq90/buildtest/var/tests/slurm.debug/laplace_mpi/laplace_mpi/0/stage/generate.sh

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Executed 1 tests
    Passed Tests: 1/1 Percentage: 100.000%
    Failed Tests: 0/1 Percentage: 0.000%


OpenACC Examples
-----------------

Next, we will make use of an OpenACC vector addition example shown below is an
example test

.. program-output:: cat ../tutorials/compilers/vecadd.yml

To compile OpenACC program with gnu compiler we must use ``-fopenacc`` flag, this
program requires linking with math library so we can specify linker flags (ldflags)
using ``ldflags: -lm``.

The output of this test will generate a single line output as follows::

    final result: 1.000000

The ``status`` field with ``regex`` is used for checking output stream using ``stream: stdout``
and ``exp`` key to specify regular expression to use. If we are to build this test,
you will notice the run section will have a Status of ``PASS``

.. program-output:: cat docgen/schemas/vecadd.txt

The regular expression is performed using `re.search <https://docs.python.org/3/library/re.html#re.search>`_, for example if we can change
the ``exp`` field as follows::

    exp: "^final result: 0.99$"

Next if we re-run test we will notice the Status is ``FAIL`` even though we
have a Return Code of **0**::

    name       | id       | executor   | status   |   returncode | testpath
    ------------+----------+------------+----------+--------------+------------------------------------------------------------------------------------------------
     vecadd_gnu | 6a7d6b67 | local.bash | FAIL     |            0 | /Users/siddiq90/Documents/buildtest/var/tests/local.bash/vecadd/vecadd_gnu/3/stage/generate.sh

In the next example, we extend the previous buildspec test to run at Cori GPU
machine using Slurm scheduler. We use the executor ``slurm.gpu`` where our executor
is defined as follows::

    gpu:
      description: submit jobs to GPU partition
      options: ["-C gpu"]
      cluster: escori

In order to submit job to the Cori GPU cluster we must use ``sbatch -C gpu -M escori`` which
is what ``slurm.gpu`` executor is doing.

In this example we make use of ``module`` field to load modules into the test, for
this test we load the modules ``cuda`` and ``gcc/8.1.1-openacc-gcc-8-branch-20190215``.
This test will launch job via ``srun`` and check job state code is ``COMPLETED``.

::

    version: "1.0"
    buildspecs:
      vecadd_openacc_gnu:
        type: compiler
        description: Vector Addition example with GNU compiler
        executor: slurm.gpu
        sbatch: ["-G 1", "-t 5", "-N 1"]
        module:
          load: [cuda, gcc/8.1.1-openacc-gcc-8-branch-20190215]
        build:
          name: gnu
          source: src/vecAdd.c
          cflags: -fopenacc
          ldflags: -lm
        run:
          launcher: srun
        status:
          slurm_job_state: COMPLETED

buildtest will generate the following test, buildtest will add the #SBATCH directives
followed by module commands. The executable is run via ``srun`` because we specify the ``launcher`` field. ::

    #!/bin/bash
    #SBATCH -G 1
    #SBATCH -t 5
    #SBATCH -N 1
    #SBATCH --job-name=vecadd_openacc_gnu
    #SBATCH --output=vecadd_openacc_gnu.out
    #SBATCH --error=vecadd_openacc_gnu.err
    source /global/u1/s/siddiq90/buildtest/var/executors/slurm.gpu/before_script.sh
    module load cuda
    module load gcc/8.1.1-openacc-gcc-8-branch-20190215
    gcc -fopenacc -o vecAdd.c.exe src/vecAdd.c -lm
    srun ./vecAdd.c.exe
    source /global/u1/s/siddiq90/buildtest/var/executors/slurm.gpu/after_script.sh

In this next example, we build same test using `hpcsdk <https://docs.nvidia.com/hpc-sdk/index.html>`_
compiler by NVIDIA that recently acquired PGI compiler. At Cori, we must load ``hpcsdk``
and ``cuda`` module in order to use the hpcsdk compiler. The ``name`` is a
required field however buildtest will ignore since we specify
``cc`` field. NVIDIA changed their compiler names instead of ``pgcc`` we must use
``nvc`` with flag ``-acc`` to offload to GPU. For CoriGPU we must use
``srun`` to acquire GPU access hence ``launcher`` field is set to srun.

::

    version: "1.0"
    buildspecs:
      vecadd_hpcsdk_gnu:
        type: compiler
        description: Vector Addition example with hpcsdk (pgi) compiler
        executor: slurm.gpu
        sbatch: ["-G 1", "-t 5", "-N 1"]
        module:
          load: [hpcsdk, cuda]
        build:
          name: pgi
          cc: nvc
          source: src/vecAdd.c
          cflags: -acc
          ldflags: -lm
        run:
          launcher: srun


Pre/Post sections for build and run section
--------------------------------------------

The compiler schema comes with ``pre_build``, ``post_build``, ``pre_run`` and
``post_run`` fields where you can insert commands before and after ``build`` or
``run`` section. The **build** section is where we compile code, and **run**
section is where compiled binary is executed.

Shown below is an example buildspec with pre/post section.

.. program-output:: cat ../tutorials/compilers/pre_post_build_run.yml


The format of the test structure is the following::

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

The generated test for this buildspec is the following::

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
