.. _compiler_schema:

Compiler Schema
=================

The compiler schema is used for compilation of programs, currently we support
single source file compilation. In order to use the compiler schema you must set ``type: compiler`` in your
test. For more details see `compiler schema docs <https://buildtesters.github.io/buildtest/pages/schemadocs/compiler-v1.html>`_

We assume the reader has basic understanding of :ref:`global_schema` validation. Shown below
is the schema header definition for `compiler-v1.0.schema.json <https://github.com/buildtesters/buildtest/blob/devel/buildtest/schemas/compiler-v1.0.schema.json>`_:

.. literalinclude:: ../../buildtest/schemas/compiler-v1.0.schema.json
   :language: json
   :lines: 1-12

The required fields for compiler schema are **type**, **compilers**, **source**
and **executor**.

First Example - Hello World
-------------------------------

We will start out with compilation a Hello World program in Fortran using the GNU compiler.
In this example we have a test called ``hello_f``.  The ``type: compiler`` is set to signify this
test will be validated with **compiler-v1.0.schema.json**.

The ``source`` property is used to specify the source code to compile, this can be a
relative path to buildspec file or an absolute path.
In this example the source file ``src/hello.f90`` is relative path to where buildspec file is located.
The ``compilers`` section declares compiler configuration, the ``name``
property is required that is used to search compiler names from our buildtest configuration via regular
expression. In this example we use the **builtin_gcc** compiler as regular expression which is the system
gcc compiler provided by buildtest. The ``default`` section specifies default compiler
configuration applicable to a specific compiler group like `gcc`. Within each compiler group we can specify
options like ``cflags``, ``fflags``, ``cxxflags``, ``ldflags`` to customize compilation line.

.. literalinclude:: ../../examples/compilers/gnu_hello_fortran.yml
   :language: yaml
   :emphasize-lines: 8-13

Shown below is an example build for this test.

.. program-output:: cat buildtest_tutorial_examples/compilers/build/gnu_hello_fortran.txt

The generated test for test name **hello_f** is the following:

.. program-output:: cat buildtest_tutorial_examples/compilers/inspect/gnu_hello_fortran.txt

How does compiler search work?
-------------------------------

Compilers are defined in your configuration file that is used by buildtest to search compilers
via ``name`` property when building test. In :ref:`configuring compilers <compilers>` you will
learn how one can define compiler, each compiler instance will have a unique name and be under one
of the compiler groups like ``gcc``, ``intel``, ``cray``, ``pgi``, ``cuda``, ``clang``, etc...

You can see the compiler declaration from our configuration file by running ``buildtest config compilers -y``
which will display compiler settings in YAML format. Note that for each compiler instance one can define name of compiler
and path to ``cc``, ``fc``, ``cxx`` wrapper. In addition one can specify ``module`` property to map compiler instance
to modulefile. If `module` property is defined you can specify list of modules to load via ``load`` property and buildtest will
automatically load these modules when using the compiler.

.. program-output:: cat buildtest_tutorial_examples/compilers/compilers_list.txt

How does buildtest detect programming language?
-------------------------------------------------

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
compile an OpenACC code that will compute vector addition. We specify all `gcc` compilers
are used for building this test via the **name** property. The ``-fopenacc`` compiler flag
enables GNU compilers to compile OpenACC code, we can set this via ``fflags`` property.
We can specify linker flags via ``ldflags`` during compilation, this code requires we specify ``-lm`` flag
to link with math library.

.. literalinclude:: ../../examples/compilers/vecadd.yml
   :language: yaml

We expect buildtest to select ``gcc_6.5.0`` and ``gcc_8.3.0`` compiler instance based on the regular expression. We
can see there are two tests one for each compiler.

.. program-output:: cat buildtest_tutorial_examples/compilers/build/vecadd.txt

Customize Compiler Option
---------------------------

We can specify custom compiler options per compiler instance using the ``config`` property.
In this next example, we have a Hello World C example that will specify different ``cflags``
based on compiler name. We can specify default compiler setting via ``default`` property. In this
example the default is ``-O1``. The ``config`` section can be used to specify custom compiler
options for each compiler name.

.. literalinclude:: ../../examples/compilers/gnu_hello_c.yml
    :language: yaml
    :emphasize-lines: 14-18

Let's build this test, we will see there is one builder instance for each compiler.

.. program-output:: cat buildtest_tutorial_examples/compilers/build/gnu_hello_c.txt

If we inspect the following test, we see each test has its own compiler flags. The default cflag
is ``-O1`` while **gcc_6.5.0** will use ``-O2`` and **gcc_8.3.0** will use ``-O3``.

.. program-output:: cat buildtest_tutorial_examples/compilers/inspect/gnu_hello_c.txt

Excluding Compilers
--------------------

The ``exclude`` property allows one to exclude compilers upon discovery which is a list of compiler
names that will be removed prior to building test. buildtest will exclude any compilers if they were
found based on regular expression via ``name`` property.  In this next example, we will exclude
``gcc_6.5.0`` compiler from building

.. literalinclude:: ../../examples/compilers/compiler_exclude.yml
    :language: yaml
    :emphasize-lines: 11

Now if we run this test, we will notice that there is only one build for this test even though buildtest
discovered both ``gcc_6.5.0`` and ``gcc_8.3.0`` compilers.

.. program-output:: cat buildtest_tutorial_examples/compilers/build/compiler_exclude.txt

Setting environment variables
------------------------------

We can define environment variables using ``env`` property which is a list of
key/value pair where key is environment name and value is a string assigned to the environment.
The ``env`` property can be used in ``default`` or ``config`` section within a compiler instance.
In this next example we have an OpenMP Hello World example which defines environment variable
`OMP_NUM_THREADS` that controls number of OpenMP threads to use when running program. In this example
we will set ``OMP_NUM_THREADS=2``

.. literalinclude:: ../../examples/compilers/openmp_hello.yml
    :language: yaml
    :emphasize-lines: 14-15

Now let's build this test.

.. program-output:: cat buildtest_tutorial_examples/compilers/build/openmp_hello.txt

We can see the generated test using ``buildtest inspect query`` given the name of test. Take a close
look at the ``export OMP_NUM_THREADS`` in the generated test.

.. program-output:: cat buildtest_tutorial_examples/compilers/inspect/openmp_hello.txt

We can define environment variables per compiler instance. buildtest will automatically override
any key in ``defaults`` with one matched under ``config`` for the compiler name. In this next example,
we will define OMP_NUM_THREADS to 4 for `gcc_8.3.0` while the default is 2 for all gcc compilers.

.. literalinclude:: ../../examples/compilers/envvar_override.yml
    :language: yaml
    :emphasize-lines: 14-15,18-19

We can build this test by running::

    buildtest build -b $BUILDTEST_ROOT/examples/compilers/envvar_override.yml

Next, let's see the generated test by running ``buildtest inspect query -d all -t override_environmentvars``. The
``-d all`` will display all test records for ``override_environmentvars``. Take a note that we have
``export OMP_NUM_THREADS=4`` for `gcc_8.3.0` test and ``export OMP_NUM_THREADS=2`` for system gcc.

.. program-output:: cat buildtest_tutorial_examples/compilers/inspect/envvar_override.txt

Tweak how test are passed
--------------------------

The ``status`` property is used to determine how buildtest will determine status of test (PASS/FAIL).
By default, an exitcode 0 is a PASS and anything else is FAIL.

Sometimes, it may be useful check output of test to determine using regular expression. This
can be done via ``regex`` property. In this example, we define two tests, the first one defines ``status``
property in the default **gcc** group. This means all compilers that belong to gcc
group will be matched based on returncode.

In second test we override the ``status`` property for a given compiler instance under the ``config`` section.
The test is expected to produce output of ``final result: 1.000000`` but we will specify a different value in order to
show this test will fail.

.. literalinclude:: ../../examples/compilers/compiler_status_regex.yml
    :language: yaml
    :emphasize-lines: 15-16,30-31,34-37

If we build this test, we should expect the first test example should pass based on
returncode 0. If the returncode doesn't match buildtest will report failure. For the second test example,
we have have specified test will pass if we get a returncode 1 based on ``default`` property however for
``gcc_8.3.0`` compiler test we have defined a ``status`` property to check based on regular expression.
We will expect both tests to fail since we will have a mismatch on returncode and regular expression

.. program-output:: cat buildtest_tutorial_examples/compilers/build/compiler_status_regex.txt

For the second test, we see the generated output is **final result: 1.000000** but our regular expression
has a different expected value therefore this test will fail even though we have a exitcode of 0.

.. program-output:: cat buildtest_tutorial_examples/compilers/inspect/compiler_status_regex.txt


Customize Run Line
-------------------

buildtest will define variable ``_EXEC`` in the job script that can be used to reference
the generated binary. By default, buildtest will run the program standalone, but sometimes you
may want to customize how job is run. This may include passing arguments or running
binary through a job/mpi launcher. The ``run`` property can be used to configure how program is executed.
The compiled executable will be present in local directory which can be accessed via ``./$_EXEC``. In example below
we pass arguments ``1 3`` for **builtin_gcc** compiler and ``100 200`` for **gcc_8.3.0** compiler.

.. literalinclude:: ../../examples/compilers/custom_run.yml
    :language: yaml
    :emphasize-lines: 13,15

You can build this test by running the following::

    buildtest build -b $BUILDTEST_ROOT/examples/compilers/custom_run.yml

Once test is complete let's inspect the generated test. We see that buildtest will insert the line specified
by ``run`` property after compilation and run the executable.

.. program-output::  cat buildtest_tutorial_examples/compilers/inspect/custom_run.txt

Pre/Post sections for build and run section
--------------------------------------------

We can specify arbitrary shell commands before/after compilation or running binary via
``pre_build``, ``post_build``, ``pre_run`` and ``post_run`` property. This can be useful
if you want to specify additional commands required to compile or run executable that are not
generated automatically

This next example illustrates how one can use these properties to have more control over the generated
test.

.. literalinclude:: ../../examples/compilers/pre_post_build_run.yml
    :language: yaml
    :emphasize-lines: 14-21

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

    buildtest build -b $BUILDTEST_ROOT/examples/compilers/pre_post_build_run.yml

If we inspect the content of test we see that buildtest will insert the shell commands
for ``pre_build``, ``post_build``, ``pre_run`` and ``post_run`` in its corresponding section.

.. program-output:: cat buildtest_tutorial_examples/compilers/inspect/pre_post_build_run.txt