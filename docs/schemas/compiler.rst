Compiler
=========

The compiler schema is used for compilation of programs, currently we support
single source file compilation. For more details see `Compiler Schema Documentation <https://buildtesters.github.io/schemas/compiler/>`_.


Schema Files
-------------

- `Production Schema <https://raw.githubusercontent.com/buildtesters/buildtest/devel/buildtest/buildsystem/schemas/compiler/compiler-v1.0.schema.json>`_
- `Development Schema <https://buildtesters.github.io/schemas/compiler/compiler-v1.0.schema.json>`_


Compilation Examples
----------------------

In order to use the compiler schema you must set ``type: compiler`` in your
sub-schema. We assume the reader has basic understanding of :ref:`global_schema`
validation.

The **type**, **compiler**, and **executor** are required keys for the schema.

Shown below are 6 test examples performing Hello World compilation with C, C++,
and Fortran using GNU compiler::

    version: "1.0"
    buildspecs:
      hello_f:
        type: compiler
        description: "Hello World Fortran Compilation"
        executor: local.bash
        compiler:
          source: "src/hello.f90"
          name: gnu
          fflags: -Wall

      hello_c:
        type: compiler
        description: "Hello World C Compilation"
        executor: local.bash
        compiler:
          source: "src/hello.c"
          name: gnu
          cflags: -Wall

      hello_cplusplus:
        type: compiler
        description: "Hello World C++ Compilation"
        executor: local.bash
        compiler:
          source: "src/hello.cpp"
          name: gnu
          cxxflags: -Wall

      cc_example:
        type: compiler
        description: Example by using cc to set C compiler
        executor: local.bash
        compiler:
          source: "src/hello.c"
          name: gnu
          cc: gcc

      fc_example:
        type: compiler
        description: Example by using fc to set Fortran compiler
        executor: local.bash
        compiler:
          source: "src/hello.f90"
          name: gnu
          fc: gfortran

      cxx_example:
        type: compiler
        description: Example by using cxx to set C++ compiler
        executor: local.bash
        compiler:
          source: "src/hello.cpp"
          name: gnu
          cxx: g++

The tests ``hello_f``, ``hello_c`` and ``hello_cplusplus`` rely on buildtest to
detect compiler wrappers while tests ``cc_example``, ``fc_example``, ``cxx_example``
rely on user to specify compiler wrappers manually.

The ``compiler`` object is start of compilation section, the required
keys are ``source`` and ``name``. The **source** key requires an input program for
compilation, this can be a file relative to buildspec file or an absolute path.
In this example our source examples are in ``src`` directory. The ``name`` field
informs buildtest to auto-detect compiler wrappers (``cc``, ``fc``, ``cxx``).

The compilation pattern buildtest utilizes is the following::

    # C example
    $cc $cppflags $cflags -o <executable> $SOURCE $ldflags

    # Fortran example
    $cxx $cppflags $cxxflags -o <executable> $SOURCE $ldflags

    # Fortran example
    $fc $cppflags $fflags -o <executable> $SOURCE $ldflags

If you specify ``cc``, ``fc`` and ``cxx`` field attributes you are responsible for
selecting the correct compiler wrapper. You can use ``cflags``, ``cxxflags`` and
``fflags`` field to pass compiler options to C, C++ and Fortran compilers.

Shown below is an example build for the buildspec example shown above::

    $ buildtest build -b gnu_hello.yml
    Paths:
    __________
    Prefix: /global/u1/s/siddiq90/cache
    Buildspec Search Path: ['/global/homes/s/siddiq90/.buildtest/site']
    Test Directory: /global/u1/s/siddiq90/cache/tests

    Stage: Discovered Buildspecs


    +-------------------------------+
    | Stage: Discovered Buildspecs  |
    +-------------------------------+

    /global/u1/s/siddiq90/tutorials/examples/serial/gnu_hello.yml

    Excluded Buildspecs:  []

    +----------------------+
    | Stage: Building Test |
    +----------------------+

    Name                      Schema Validation File    TestPath                                 Buildspec
    ________________________________________________________________________________________________________________________________________________________________
    hello_f                   compiler-v1.0.schema.json /global/u1/s/siddiq90/cache/tests/gnu_hello/hello_f.sh /global/u1/s/siddiq90/tutorials/examples/serial/gnu_hello.yml
    hello_c                   compiler-v1.0.schema.json /global/u1/s/siddiq90/cache/tests/gnu_hello/hello_c.sh /global/u1/s/siddiq90/tutorials/examples/serial/gnu_hello.yml
    hello_cplusplus           compiler-v1.0.schema.json /global/u1/s/siddiq90/cache/tests/gnu_hello/hello_cplusplus.sh /global/u1/s/siddiq90/tutorials/examples/serial/gnu_hello.yml
    cc_example                compiler-v1.0.schema.json /global/u1/s/siddiq90/cache/tests/gnu_hello/cc_example.sh /global/u1/s/siddiq90/tutorials/examples/serial/gnu_hello.yml
    fc_example                compiler-v1.0.schema.json /global/u1/s/siddiq90/cache/tests/gnu_hello/fc_example.sh /global/u1/s/siddiq90/tutorials/examples/serial/gnu_hello.yml
    cxx_example               compiler-v1.0.schema.json /global/u1/s/siddiq90/cache/tests/gnu_hello/cxx_example.sh /global/u1/s/siddiq90/tutorials/examples/serial/gnu_hello.yml

    +----------------------+
    | Stage: Running Test  |
    +----------------------+

    Name                 Executor             Status               Return Code          Buildspec Path
    ________________________________________________________________________________________________________________________
    hello_f              local.bash           PASS                 0                    /global/u1/s/siddiq90/tutorials/examples/serial/gnu_hello.yml
    hello_c              local.bash           PASS                 0                    /global/u1/s/siddiq90/tutorials/examples/serial/gnu_hello.yml
    hello_cplusplus      local.bash           PASS                 0                    /global/u1/s/siddiq90/tutorials/examples/serial/gnu_hello.yml
    cc_example           local.bash           PASS                 0                    /global/u1/s/siddiq90/tutorials/examples/serial/gnu_hello.yml
    fc_example           local.bash           PASS                 0                    /global/u1/s/siddiq90/tutorials/examples/serial/gnu_hello.yml
    cxx_example          local.bash           PASS                 0                    /global/u1/s/siddiq90/tutorials/examples/serial/gnu_hello.yml

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Executed 6 tests
    Passed Tests: 6/6 Percentage: 100.000%
    Failed Tests: 0/6 Percentage: 0.000%

The generated test for test name **hello_f** is the following::

    #!/bin/bash
    gfortran -Wall -o hello.f90.exe /global/u1/s/siddiq90/tutorials/examples/serial/src/hello.f90
    ./hello.f90.exe

buildtest will fill in the compilation line based on compilation pattern. buildtest,
will detect the file extensions and perform a lookup to find the programming language,
and finally generate the appropriate C, C++, or Fortran compilation based on language
detected. Recall that test **hello_f** had the following content and we relied
on buildtest to detect compiler options::

      hello_f:
        type: compiler
        description: "Hello World Fortran Compilation"
        executor: local.bash
        compiler:
          source: "src/hello.f90"
          name: gnu
          fflags: -Wall

buildtest detects the programming language and it finds **.f90** file extension
and infers it must be Fortran program, hence ``gfortran`` was selected. The
executable name is generated by adding ``.exe`` to end of source file name
so we get ``hello.f90.exe``. Finally, we run the executable.

File Extension Language Table
-----------------------------

Shown below is the file extension table for your reference

.. csv-table:: File Extension Language Mapping
    :header: "Language", "File Extension"
    :widths: 30, 80

    "**C**", ".c"
    "**C++**", ".cc .cxx .cpp .c++"
    "**Fortran**", ".f90 .F90 .f95 .f .F .FOR .for .FTN .ftn"

More Examples
--------------

If you want to pass options to executable command use the ``exec_args`` key. Shown
below is an example test::

    version: "1.0"
    buildspecs:
      executable_arguments:
        type: compiler
        description: Passing arguments example
        executor: local.bash
        compiler:
          source: "src/argc.c"
          name: gnu
          cflags: -Wall
          exec_args: "1 2 3"

The exec_args will pass options to the executable, use this if your binary
requires input arguments. Shown below is a generated test::

    #!/bin/bash
    gcc -Wall -o argc.c.exe /global/u1/s/siddiq90/tutorials/examples/serial/src/argc.c
    ./argc.c.exe 1 2 3

Next, we will make use of an OpenACC vector addition example shown below is an
example test::

    version: "1.0"
    buildspecs:
      vecadd_gnu:
        type: compiler
        description: Vector Addition example with GNU compiler
        executor: local.bash
        compiler:
          name: gnu
          source: src/vecAdd.c
          cflags: -fopenacc
          ldflags: -lm
        status:
          regex:
            stream: stdout
            exp: "^final result: 1.000000$"

To compile OpenACC program with gnu compiler we must use ``-fopenacc`` flag, this
program requires linking with math library so we can specify linker flags (ldflags)
using ``ldflags: -lm``.

The output of this test will generate a single line output as follows::

    final result: 1.000000

The ``status`` field with ``regex`` is used for checking output stream using ``stream: stdout``
and ``exp`` key to specify regular expression to use. If we are to build this test,
you will notice the run section will have a Status of ``PASS``::

    $ buildtest build -b vecadd.yml
    Paths:
    __________
    Prefix: /global/u1/s/siddiq90/cache
    Buildspec Search Path: ['/global/homes/s/siddiq90/.buildtest/site']
    Test Directory: /global/u1/s/siddiq90/cache/tests

    Stage: Discovered Buildspecs


    +-------------------------------+
    | Stage: Discovered Buildspecs  |
    +-------------------------------+

    /global/u1/s/siddiq90/tutorials/examples/openacc/vecadd.yml

    Excluded Buildspecs:  []

    +----------------------+
    | Stage: Building Test |
    +----------------------+

    Name                      Schema Validation File    TestPath                                 Buildspec
    ________________________________________________________________________________________________________________________________________________________________
    vecadd_gnu                compiler-v1.0.schema.json /global/u1/s/siddiq90/cache/tests/vecadd/vecadd_gnu.sh /global/u1/s/siddiq90/tutorials/examples/openacc/vecadd.yml

    +----------------------+
    | Stage: Running Test  |
    +----------------------+

    Name                 Executor             Status               Return Code          Buildspec Path
    ________________________________________________________________________________________________________________________
    vecadd_gnu           local.bash           PASS                 0                    /global/u1/s/siddiq90/tutorials/examples/openacc/vecadd.yml

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Executed 1 tests
    Passed Tests: 1/1 Percentage: 100.000%
    Failed Tests: 0/1 Percentage: 0.000%

The regular expression is performed using `re.search <https://docs.python.org/3/library/re.html#re.search>`_, for example if we can change
the ```exp`` field as follows::

    exp: "^final result: 0.99$"

Next if we re-run test we will notice the Status is ``FAIL`` even though we
have a Return Code of **0**::

    +----------------------+
    | Stage: Running Test  |
    +----------------------+

    Name                 Executor             Status               Return Code          Buildspec Path
    ________________________________________________________________________________________________________________________
    vecadd_gnu           local.bash           FAIL                 0                    /global/u1/s/siddiq90/tutorials/examples/openacc/vecadd.yml



Compiler Schema Examples
-------------------------

The compiler schema examples can be retrieved via ``buildtest schema -n compiler-v1.0.schema.json -e``
which shows a list of valid/invalid buildspec examples using ``type: compiler``.
Each example is validated with schema ``compiler-v1.0.schema.json`` and error
message from invalid examples are also shown in example output.

.. program-output:: cat docgen/schemas/compiler-examples.txt

compiler-v1.0.schema.json
-------------------------

.. program-output:: cat docgen/schemas/compiler-json.txt



