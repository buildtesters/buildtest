.. _buildspec_overview:

Buildspec Overview
========================

What is a buildspec?
---------------------

In buildtest, we refer to **buildspec** as a YAML file that defines your test that
buildtest will parse using the provided schemas and build a shell script from the buildspec file. Every buildspec is
validated with a global schema which you can find more if you click :ref:`here <global_schema>`.

.. _buildspec_example:

Example
--------

Let's start off with a simple example that declares two variables **X** and **Y** and
prints the sum of X+Y.

.. literalinclude:: ../tutorials/add_numbers.yml
   :language: yaml

buildtest will validate the entire file with ``global.schema.json``, the schema
requires **version** and **buildspec** in order to validate file. The **buildspec**
is where you define each test. The name of the test is **add_numbers**.
The test requires a **type** field which is the sub-schema used to validate the
test section. In this example ``type: script`` informs buildtest to use the :ref:`script_schema`
when validating test section.

Each subschema has a list of field attributes that are supported, for example the
fields: **type**, **executor**, **vars** and **run** are all valid fields supported
by the *script* schema. The **version** field informs which version of subschema to use.
Currently all sub-schemas are at version ``1.0`` where buildtest will validate
with a schema ``script-v1.0.schema.json``. In future, we can support multiple versions
of subschema for backwards compatibility.


Let's look at a more interesting example, shown below is a multi line run
example using the `script` schema with test name called
**systemd_default_target**, shown below is the content of test:

.. literalinclude:: ../../general_tests/configuration/systemd-default-target.yml
    :language: yaml

The test name **systemd_default_target** defined in **buildspec** section is
validated with the following pattern ``"^[A-Za-z_][A-Za-z0-9_]*$"``. This test
will use the executor **generic.local.bash** which means it will use the Local Executor
with an executor name `bash` defined in the buildtest settings. The default
buildtest settings will provide a bash executor as follows:

.. code-block:: yaml

    system:
      generic:
        hostnames: ["localhost"]
        executors:
          local:
            bash:
              description: submit jobs on local machine using bash shell
              shell: bash

The ``shell: bash`` indicates this executor will use `bash` to run the test scripts.
To reference this executor use the format ``<system>.<type>.<name>`` in this case **generic.local.bash**
refers to bash executor.

The ``description`` field is an optional key that can be used to provide a brief
summary of the test. In this example we can a full multi-line run section, this
is achieved in YAML using ``run: |`` followed by content of run section tab indented
2 spaces.

.. _script_schema:

Script Schema
---------------

The script schema is used for writing simple scripts (bash, sh, python) in Buildspec.
To use this schema you must set ``type: script``. The ``run`` field is responsible
for writing the content of test.


Shown below is schema header for `script-v1.0.schema.json <https://github.com/buildtesters/buildtest/blob/devel/buildtest/schemas/script-v1.0.schema.json>`_.

.. literalinclude:: ../../buildtest/schemas/script-v1.0.schema.json
   :language: json
   :lines: 1-8

The ``"type": "object"`` means sub-schema is a JSON `object <http://json-schema.org/understanding-json-schema/reference/object.html>`_
where we define a list of key/value pair. The ``"required"`` field specifies a list of
fields that must be specified in order to validate the Buildspec. In this example, ``type``, ``run``, and ``executor``
are required fields. The ``additionalProperties: false`` informs schema to reject
any extra properties not defined in the schema.

The **executor** key is required for all sub-schemas which instructs buildtest
which executor to use when running the test. The executors are defined in
:ref:`configuring_buildtest`. In our :ref:`first example <buildspec_example>` we define variables using the
``vars`` property which is a Key/Value pair for variable assignment.
The **run** section is required for script schema which defines the content of
the test script.

For more details on script schema see schema docs at https://buildtesters.github.io/buildtest/

.. _environment_variables:

Declaring Environment Variables
--------------------------------

You can define environment variables using the ``env`` property, this is compatible
with shells: ``bash``, ``sh``, ``zsh``, ``csh`` and ``tcsh``. It does not work with
``shell: python``. In example below we declare three tests using environment
variable with default shell (bash), csh, and tcsh

.. literalinclude:: ../tutorials/environment.yml
   :language: yaml

This test can be run by issuing the following command: ``buildtest build -b tutorials/environment.yml``.
If we inspect one of the test script we will see that buildtest generates a build script that invokes the test using the
shell wrapper `/bin/csh` for the csh test and gets the returncode.

.. code-block:: shell

    #!/bin/bash


    ############# START VARIABLE DECLARATION ########################
    export BUILDTEST_TEST_NAME=csh_env_declaration
    export BUILDTEST_TEST_ROOT=/Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.csh/environment/csh_env_declaration/0
    export BUILDTEST_BUILDSPEC_DIR=/Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials
    export BUILDTEST_STAGE_DIR=/Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.csh/environment/csh_env_declaration/0/stage
    export BUILDTEST_TEST_ID=501ec5d3-e614-4ae8-9c1e-4849ce340c76
    ############# END VARIABLE DECLARATION   ########################


    # source executor startup script
    source /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/executor/generic.local.csh/before_script.sh
    # Run generated script
    /bin/csh /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.csh/environment/csh_env_declaration/0/stage/csh_env_declaration.csh
    # Get return code
    returncode=$?
    # Exit with return code
    exit $returncode

This generated test looks something like this

.. code-block:: shell

    #!/bin/csh
    # Declare environment variables
    setenv SHELL_NAME csh


    # Content of run section
    echo "This is running $SHELL_NAME"


Environment variables are defined using ``export`` in bash, sh, zsh while csh and
tcsh use ``setenv``.

.. _variables:

Declaring Variables
----------------------

Variables can be defined using ``vars`` property, this is compatible with all shells
except for ``python``. The variables are defined slightly different in csh, tcsh as pose
to bash, sh, and zsh. In example below we define tests with bash and csh.

In YAML strings can be specified with or without quotes however in bash, variables
need to be enclosed in quotes ``"`` if you are defining a multi word string (``name="First Last"``).

If you need define a literal string it is recommended
to use the literal block ``|`` that is a special character in YAML.
If you want to specify ``"`` or ``'`` in string you can use the escape character
``\`` followed by any of the special character. In example below we define
several variables such as **X**, **Y** that contain numbers, variable **literalstring**
is a literal string processed by YAML. The variable **singlequote** and **doublequote**
defines a variable with the special character ``'`` and ``"``. The variables
**current_user** and **num_files** store result of a shell command. This can
be done using ``var=$(<command>)`` or ``var=`<command>``` where ``<command>`` is
a Linux command.

.. literalinclude::  ../tutorials/vars.yml
   :language: yaml

Next we build this test by running ``buildtest build -b $BUILDTEST_ROOT/tutorials/vars.yml``.

.. command-output:: buildtest build -b $BUILDTEST_ROOT/tutorials/vars.yml
    :shell:

Let's check the generated script from the previous build, you can run ``buildtest inspect query -o variables_bash`` where
`-o` refers to output file for testname `variables_bash`. Take note of the output file we

.. command-output:: buildtest inspect query -o variables_bash

.. _status:

Test Status
-----------

buildtest will record state of each test which can be ``PASS`` or ``FAIL``. By default a 0 exit code is
PASS and everything else is a FAIL. The ``status`` property can be used to determine how test will report its state.
Currently, we can match state based on :ref:`returncode <returncode>`, :ref:`runtime <runtime>`, or
:ref:`regular expression <regex>`.

.. _returncode:

Return Code Matching
~~~~~~~~~~~~~~~~~~~~~

buildtest can report PASS/FAIL based on returncode, by default a 0 exit code is PASS
and everything else is FAIL. The returncode can be a list of exit codes to match.
In this example we have four tests called ``exit1_fail``, ``exit1_pass``,
``returncode_list_mismatch`` and ``returncode_int_match``.  We expect **exit1_fail** and
**returncode_mismatch** to ``FAIL`` while **exit1_pass** and **returncode_int_match**
will ``PASS``.

.. literalinclude:: ../tutorials/pass_returncode.yml
   :language: yaml
   :emphasize-lines: 17-18,26-27,35-36

Let's build this test and pay close attention to the **status**
column in output.

.. command-output:: buildtest build -b tutorials/pass_returncode.yml
   :shell:

The ``returncode`` field can be an integer or list of integers but it may not accept
duplicate values. If you specify a list of exit codes, buildtest will check actual returncode
with list of expected returncodes specified by `returncode` field.

Shown below are examples of invalid returncodes:

.. code-block:: yaml

      # empty list is not allowed
      returncode: []

      # floating point is not accepted in list
      returncode: [1, 1.5]

      # floating point not accepted
      returncode: 1.5

      # duplicates are not allowed
      returncode: [1, 2, 5, 5]

.. _regex:

Passing Test based on regular expression
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

buildtest can configure PASS/FAIL of test based on regular expression on output or error file. This can be useful
if you are expecting a certain output from the test as pose to returncode check.

In this example we introduce, the ``regex`` field which is part of **status** that expects
a regular expression via ``exp``. The ``stream`` property must be  **stdout** or **stderr** which indicates
buildtest will read output or error file and apply regular expression. If there is a match, buildtest will record the
test state as **PASS** otherwise it will be a **FAIL**. In this example, we have two tests that will apply regular expression
on output file.

.. literalinclude:: ../tutorials/status_regex.yml
   :language: yaml
   :emphasize-lines: 9-12,20-23

Now if we run this test, we will see first test will pass while second one will fail even though the returncode is
a 0. Take a close look at the **status** property

.. command-output:: buildtest build -b tutorials/status_regex.yml

.. _runtime:

Passing Test based on runtime
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

buildtest can determine state of test based on `runtime` property which is part of
``status`` object. This can be used if you want to control how test `PASS` or `FAIL` based on
execution time of test. In example below we have five tests that make use of **runtime** property
for passing a test.  The runtime property support ``min`` and ``max`` property that can mark test
pass based on minimum and maximum runtime. A test will pass if it's execution time is greater than ``min``
time and less than ``max`` time. If `min` is specified without `max` property the upperbound is not set, likewise
`max` without `min` will pass if test is less than **max** time. The lower bound is not set, but test runtime
will be greater than 0 sec.

In test **timelimit_min**, we sleep for 2 seconds and it will pass because minimum runtime is 1.0 seconds. Similarly,
**timelimit_max** will pass because we sleep for 2 seconds with a max time of 5.0.

.. literalinclude:: ../tutorials/runtime_status_test.yml
   :language: yaml
   :emphasize-lines: 9-12,21-23,31-33,42-44,52-54

.. command-output:: buildtest build -b tutorials/runtime_status_test.yml

If we look at the test results, we expect the first three tests **timelimit_min**, **timelimit_max**, **timelimit_min_max**
will pass while the last two tests fail because it fails to comply with runtime property.

.. command-output:: buildtest report --filter buildspec=tutorials/runtime_status_test.yml --format name,id,state,runtime --latest

Explicitly Declaring Status of Test
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can explicitly define status of test regardless of what buildtest does for checking status of test. This
can be useful if you want to explicitly mark a test as **PASS** or **FAIL** regardless of how test behaves. This can be done via
``state`` property which expects one of two types **PASS** or **FAIL**. If ``state`` property is specified, buildtest will ignore any checks
including returncode, regex, or runtime match.

In this next example we will demonstrate how one can use ``state`` property for marking test state. In this
example we have four tests. The first test ``always_pass`` will **PASS** even though we have a non-zero returncode. The
second test ``always_fail`` will **FAIL** even though it has a 0 returncode. The last two test demonstrate how one
can define state regardless of what is specified for returncode match. buildtest will honor the ``state`` property even if
their is a match on the returncode.

.. literalinclude:: ../tutorials/explicit_state.yml
   :language: yaml

If we build this test, we expect buildtest to honor the value of ``state`` property

.. command-output:: buildtest build -b tutorials/explicit_state.yml

.. _define_tags:

Defining Tags
-------------

The ``tags`` field can be used to classify tests which can be used to organize tests
or if you want to :ref:`build_by_tags` (``buildtest build --tags <TAGNAME>``).
Tags can be defined as a string or list of strings. In this example, the test
``string_tag`` defines a tag name **network** while test ``list_of_strings_tags``
define a list of tags named ``network`` and ``ping``.

.. literalinclude:: ../tutorials/tags_example.yml
    :language: yaml

Each item in tags must be a string and no duplicates are allowed, for example in
this test, we define a duplicate tag **network** which is not allowed.

.. literalinclude:: ../tutorials/invalid_tags.yml
    :language: yaml

If we run this test and inspect the logs we will see an error message in schema validation:

.. code-block:: console

    2020-09-29 10:56:43,175 [parser.py:179 - _validate() ] - [INFO] Validating test - 'duplicate_string_tags' with schemafile: script-v1.0.schema.json
    2020-09-29 10:56:43,175 [buildspec.py:397 - parse_buildspecs() ] - [ERROR] ['network', 'network'] is not valid under any of the given schemas

    Failed validating 'oneOf' in schema['properties']['tags']:
        {'oneOf': [{'type': 'string'},
                   {'$ref': '#/definitions/list_of_strings'}]}

    On instance['tags']:
        ['network', 'network']

If tags is a list, it must contain one item, therefore an empty list (i.e ``tags: []``)
is invalid.

Customize Shell
-----------------

Shell Type
~~~~~~~~~~

buildtest will default to ``bash`` shell when running test, but we can configure shell
option using the ``shell`` field. The shell field is defined in schema as follows:

.. code-block:: json

    "shell": {
      "type": "string",
      "description": "Specify a shell launcher to use when running jobs. This sets the shebang line in your test script. The ``shell`` key can be used with ``run`` section to describe content of script and how its executed",
      "pattern": "^(/bin/bash|/bin/sh|/bin/csh|/bin/tcsh|/bin/zsh|bash|sh|csh|tcsh|zsh|python).*"
    },

The shell pattern is a regular expression where one can specify a shell name along
with shell options. The shell will configure the `shebang <https://en.wikipedia.org/wiki/Shebang_(Unix)>`_
in the test-script. In this example, we illustrate a few tests using different shell
field.

.. literalinclude:: ../tutorials/shell_examples.yml
   :language: yaml

The generated test-script for buildspec **_bin_sh_shell** will specify shebang
**/bin/sh** because we specified ``shell: /bin/sh``:

.. code-block:: shell

    #!/bin/sh
    # Content of run section
    bzip2 --help

If you don't specify a shell path such as ``shell: sh``, then buildtest will resolve
path by looking in $PATH and build the shebang line.

In test **shell_options** we specify ``shell: "sh -x"``, buildtest will tack on the
shell options into the called script as follows:

.. code-block:: shell
    :emphasize-lines: 16

    #!/bin/bash


    ############# START VARIABLE DECLARATION ########################
    export BUILDTEST_TEST_NAME=shell_options
    export BUILDTEST_TEST_ROOT=/Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.sh/shell_examples/shell_options/0
    export BUILDTEST_BUILDSPEC_DIR=/Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials
    export BUILDTEST_STAGE_DIR=/Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.sh/shell_examples/shell_options/0/stage
    export BUILDTEST_TEST_ID=95c11f54-bbb1-4154-849d-44313e4417c2
    ############# END VARIABLE DECLARATION   ########################


    # source executor startup script
    source /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/executor/generic.local.sh/before_script.sh
    # Run generated script
    sh -x /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.sh/shell_examples/shell_options/0/stage/shell_options.sh
    # Get return code
    returncode=$?
    # Exit with return code
    exit $returncode


If you prefer **csh** or **tcsh** for writing scripts just set ``shell: csh`` or
``shell: tcsh``, note you will need to match this with appropriate executor. For now
use ``executor: generic.local.csh`` to run your csh/tcsh scripts. In this example below
we define a script using csh, take note of ``run`` section we can write csh style.

.. literalinclude:: ../tutorials/csh_shell_examples.yml
   :language: yaml

Customize Shebang
~~~~~~~~~~~~~~~~~~

You may customize the shebang line in testscript using ``shebang`` field. This
takes precedence over the ``shell`` property which automatically detects the shebang
based on shell path.

In next example we have two tests **bash_login_shebang** and **bash_nonlogin_shebang**
which tests if shell is Login or Non-Login. The ``#!/bin/bash -l`` indicates we
want to run in login shell and expects an output of ``Login Shell`` while
test **bash_nonlogin_shebang** should run in default behavior which is non-login
shell and expects output ``Not Login Shell``. We match this with regular expression
with stdout stream.

.. literalinclude:: ../tutorials/shebang.yml
    :language: yaml

Now let's run this test as we see the following.

.. command-output:: buildtest build -b tutorials/shebang.yml

If we look at the generated test for **bash_login_shebang** we see the shebang line
is passed into the script:

.. code-block:: shell
    :emphasize-lines: 1

    #!/bin/bash -l
    # Content of run section
    shopt -q login_shell && echo 'Login Shell' || echo 'Not Login Shell'

Python Shell
~~~~~~~~~~~~~

You can use **script** schema to write python scripts using the ``run`` property. In order to write python code you
must set ``shell`` property to python interpreter such as ```shell: python`` or full path to python wrapper such
as ``shell: /usr/bin/python``.

Here is a python example calculating area of circle

.. literalinclude:: ../tutorials/python-shell.yml
   :language: yaml


.. note::
    Python scripts are very picky when it comes to formatting, in the ``run`` section
    if you are defining multiline python script you must remember to use 2 space indent
    to register multiline string. buildtest will extract the content from run section
    and inject in your test script. To ensure proper formatting for a more complex python
    script you may be better off writing a python script in separate file and invoke the
    python script in the ``run`` section.

Skipping test
-------------

By default, buildtest will run all tests defined in ``buildspecs`` section, if you
want to skip a test use the ``skip`` field which expects a boolean value. Shown
below is an example test.

.. literalinclude:: ../tutorials/skip_tests.yml
   :language: yaml

The first test **skip** will be ignored by buildtest because ``skip: true`` is defined
while **unskipped** will be processed as usual.

.. Note::

    YAML and JSON have different representation for boolean. For json schema
    valid values are ``true`` and ``false`` see https://json-schema.org/understanding-json-schema/reference/boolean.html
    however YAML has many more representation for boolean see https://yaml.org/type/bool.html. You
    may use any of the YAML boolean, however it's best to stick with json schema values
    ``true`` and ``false``.


Here is an example build, notice message ``[skip] test is skipped`` during the build
stage

.. command-output:: buildtest build -b tutorials/skip_tests.yml

.. _metrics:

Defining Metrics
------------------

buildtest provides a method to define test metrics in the buildspecs which can be used to
store arbitrary content from the output/error file into named metric. A metric is
defined using the ``metrics`` property where each element under the **metrics** property
is the name of the metric which must be a unique name. A metric can apply regular expression
on stdout, stderr like in this example below. The metrics are captured in the test report which can
be queried via ``buildtest report`` or ``buildtest inspect``. Shown below is an example
where we define two metrics named ``hpcg_rating`` and ``hpcg_state``.

.. literalinclude:: ../tutorials/metrics_regex.yml
    :language: yaml
    :emphasize-lines: 9-18

The metrics will not impact behavior of test, it will only impact the test report. By default
a metric will be an empty dictionary if there is no ``metrics`` property. If we fail to match
a regular expression, the metric will be defined as an empty string.

.. Note::
   If your regular expression contains an escape character ``\`` you must surround your
   string in single quotes ``'`` as pose to double quotes ``"``

Let's build this test.

.. command-output:: buildtest build -b tutorials/metrics_regex.yml

We can query the metrics via ``buildtest report`` which will display all metrics as a comma separted
**Key/Value** pair. We can use ``buildtest report --format metrics`` to extract all metrics for a test.
Internally, we store the metrics as a dictionary but when we print them out via ``buildtest report`` we
join them together into a single string. Shown below is the metrics for the previous build.


.. command-output:: buildtest report --filter buildspec=tutorials/metrics_regex.yml --format name,metrics

You can define a metric based on :ref:`variables <variables>` or :ref:`environment variables <environment_variables>`
which requires you have set ``vars`` or ``env`` property in the buildspec. The ``vars`` and
``env`` is a property under the metric name that can be used to reference name
of variable or environment variable. If you reference an invalid name, buildtest will assign the metric an empty string.
In this next example, we define two metrics ``gflop`` and ``foo`` that are assigned to variable ``GFLOPS`` and
environment variable ``FOO``.

.. literalinclude:: ../../tutorials/metrics_variable.yml
    :language: yaml
    :emphasize-lines: 15-19

Now let's build the test.

.. command-output:: buildtest build -b tutorials/metrics_variable.yml

Now if we query the previous test, we will see the two metrics ``gflops`` and ``foo`` are captured in the test.

.. command-output:: buildtest report --filter buildspec=tutorials/metrics_variable.yml --format name,metrics


You can also define metrics with the :ref:`compiler schema <compiler_schema>` which works slightly different
when it comes to variable and environment assignment. Since you can define ``vars`` and ``env`` in ``defaults``
or ``config`` section. Let's take a look at this next example where we compile an openmp code
that will use the `OMP_NUM_THREADS` environment as the metric that is assigned to name ``openmp_threads``. Since
we have defined ``OMP_NUM_THREADS`` under the ``defaults`` and ``config`` section we will use the
environment variable that corresponds to each compiler.


.. literalinclude:: ../../examples/compilers/metrics_openmp.yml
   :language: yaml

.. Note:: This test uses a custom site configuration that defines gcc multiple compilers.

Let's build this test as follows

.. code-block:: console


    $ buildtest -c config/laptop.yml build -b tutorials/compilers/metrics_openmp.yml


    User:  siddiq90
    Hostname:  DOE-7086392.local
    Platform:  Darwin
    Current Time:  2021/07/24 00:14:33
    buildtest path: /Users/siddiq90/Documents/GitHubDesktop/buildtest/bin/buildtest
    buildtest version:  0.10.0
    python path: /Users/siddiq90/.local/share/virtualenvs/buildtest-KLOcDrW0/bin/python
    python version:  3.7.3
    Test Directory:  /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests
    Configuration File:  /Users/siddiq90/Documents/GitHubDesktop/buildtest/config/laptop.yml
    Command: /Users/siddiq90/Documents/GitHubDesktop/buildtest/bin/buildtest -c config/laptop.yml build -b tutorials/compilers/metrics_openmp.yml

    +-------------------------------+
    | Stage: Discovering Buildspecs |
    +-------------------------------+

    +------------------------------------------------------------------------------------------+
    | Discovered Buildspecs                                                                    |
    +==========================================================================================+
    | /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/compilers/metrics_openmp.yml |
    +------------------------------------------------------------------------------------------+
    Discovered Buildspecs:  1
    Excluded Buildspecs:  0
    Detected Buildspecs after exclusion:  1

    +---------------------------+
    | Stage: Parsing Buildspecs |
    +---------------------------+

     schemafile                | validstate   | buildspec
    ---------------------------+--------------+------------------------------------------------------------------------------------------
     compiler-v1.0.schema.json | True         | /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/compilers/metrics_openmp.yml



    name                       description
    -------------------------  -----------------------------------
    metrics_variable_compiler  define metrics with compiler schema
    metrics_variable_compiler  define metrics with compiler schema
    metrics_variable_compiler  define metrics with compiler schema

    +----------------------+
    | Stage: Building Test |
    +----------------------+





     name                      | id       | type     | executor           | tags                     | compiler           | testpath
    ---------------------------+----------+----------+--------------------+--------------------------+--------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------
     metrics_variable_compiler | e45976b8 | compiler | generic.local.bash | ['tutorials', 'compile'] | builtin_gcc        | /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.bash/metrics_openmp/metrics_variable_compiler/11/metrics_variable_compiler_build.sh
     metrics_variable_compiler | 8bc71f19 | compiler | generic.local.bash | ['tutorials', 'compile'] | gcc/9.3.0-n7p74fd  | /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.bash/metrics_openmp/metrics_variable_compiler/12/metrics_variable_compiler_build.sh
     metrics_variable_compiler | 7127eb46 | compiler | generic.local.bash | ['tutorials', 'compile'] | gcc/10.2.0-37fmsw7 | /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic.local.bash/metrics_openmp/metrics_variable_compiler/13/metrics_variable_compiler_build.sh

    +---------------------+
    | Stage: Running Test |
    +---------------------+

     name                      | id       | executor           | status   |   returncode
    ---------------------------+----------+--------------------+----------+--------------
     metrics_variable_compiler | e45976b8 | generic.local.bash | FAIL     |          127
     metrics_variable_compiler | 8bc71f19 | generic.local.bash | PASS     |            0
     metrics_variable_compiler | 7127eb46 | generic.local.bash | PASS     |            0

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Passed Tests: 2/3 Percentage: 66.667%
    Failed Tests: 1/3 Percentage: 33.333%


    Writing Logfile to: /Users/siddiq90/buildtest/buildtest_0a04808e.log
    A copy of logfile can be found at $BUILDTEST_ROOT/buildtest.log -  /Users/siddiq90/Documents/GitHubDesktop/buildtest/buildtest.log

Now if we filter the results, notice that ``builtin_gcc`` got metrics ``openmp_threads=1`` since
that is the value set under the ``builtin_gcc`` compiler instance under the ``config`` section. The ``gcc/9.3.0-n7p74fd`` compiler
got value of **2** because we have an entry defined under the ``config`` section while ``gcc/10.2.0-37fmsw7``
compiler got the value of **4** from the ``default`` section that is inherited for all gcc compilers.


.. code-block:: console

    $ buildtest report --filter buildspec=tutorials/compilers/metrics_openmp.yml --format name,compiler,metrics
    Reading report file: /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/report.json

    +---------------------------+--------------------+------------------+
    | name                      | compiler           | metrics          |
    +===========================+====================+==================+
    | metrics_variable_compiler | builtin_gcc        | openmp_threads=1 |
    +---------------------------+--------------------+------------------+
    | metrics_variable_compiler | gcc/9.3.0-n7p74fd  | openmp_threads=2 |
    +---------------------------+--------------------+------------------+
    | metrics_variable_compiler | gcc/10.2.0-37fmsw7 | openmp_threads=4 |
    +---------------------------+--------------------+------------------+

.. _multiple_executors:

Running test across multiple executors
----------------------------------------

The `executor` property can support regular expression to search for compatible
executors, this can be used if you want to run a test across multiple executors. In buildtest,
we use `re.fullmatch <https://docs.python.org/3/library/re.html#re.fullmatch>`_ with the input
pattern defined by **executor** property against a list of available executors defined in configuration file.
You can retrieve a list of executors by running ``buildtest config executors``.

In example below we will run this test on `generic.local.bash` and `generic.local.sh` executor based
on the regular expression.

.. literalinclude:: ../tutorials/executor_regex_script.yml
   :language: yaml

If we build this test, notice that there are two tests, one for each executor.

.. command-output:: buildtest build -b tutorials/executor_regex_script.yml

Multiple Executors
~~~~~~~~~~~~~~~~~~~

.. Note:: This feature is in active development

.. Note:: This feature is compatible with ``type: script`` and ``type: spack``.

The ``executors`` property can be used to define executor specific configuration
for each test, currently this field can be used with :ref:`vars <variables>`, :ref:`env <environment_variables>`
, scheduler directives: ``sbatch``, ``bsub``, ``pbs``, ``cobalt`` and :ref:`cray burst buffer/data warp <cray_burstbuffer_datawarp>`.
The ``executors`` field is a JSON object that expects name of executor followed by property set per executor. In this next example,
we define variables ``X``, ``Y`` and environment ``SHELL`` based on executors **generic.local.sh** and **generic.local.bash**.

.. literalinclude:: ../tutorials/script/multiple_executors.yml
   :language: yaml

Let's build this test.

.. command-output:: buildtest build -b tutorials/script/multiple_executors.yml

Now let's look at the generated content of the test as follows. We will see that buildtest will
set **X=1**, **Y=3** and **SHELL=bash** for ``generic.local.bash`` and **X=2**, **Y=4** and **SHELL=sh** for
``generic.local.sh``

.. command-output:: buildtest inspect query -t executors_vars_env_declaration

Scheduler Directives
~~~~~~~~~~~~~~~~~~~~~~

We can also define scheduler directives based on executor type, in this example we define
``sbatch`` property per executor type. Note that ``sbatch`` property in the ``executors`` section
will override the ``sbatch`` property defined in the top-level file otherwise it will use the default.


.. literalinclude:: ../tutorials/script/executor_scheduler.yml
   :language: yaml


.. command-output:: buildtest build -b tutorials/script/executor_scheduler.yml

If we inspect this test, we will see each each test have different ``#SBATCH`` directives for each test
based on the ``sbatch`` property defined in the ``executors`` field.

.. command-output:: buildtest inspect query -t executors_sbatch_declaration

Cray Burst Buffer and Data Warp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also define ``BB`` and ``DW`` directives in the ``executors`` field to override
cray burst buffer and data warp settings per executor. buildtest will use the fields ``BB``
and ``DW`` and insert the ``#BB`` and ``#DW`` directives in the job script. For more details
see :ref:`cray_burstbuffer_datawarp`.

.. literalinclude:: ../tutorials/burstbuffer_datawarp_executors.yml
    :language: yaml


Status and Metrics Field
~~~~~~~~~~~~~~~~~~~~~~~~~

The :ref:`status <status>` and :ref:`metrics <metrics>` field are supported in ``executors``
which can be defined within the named executor. In this next example, we will define `generic.local.bash` to match
test based on returncode **0** or **2** and define metrics named ``firstname`` that is assigned the value
from variable **FIRST**. The second test using `generic.local.sh` will match returncode of **1** and
define a metrics named ``lastname`` that will store the value defined by variable **LAST**.

.. literalinclude:: ../tutorials/script/status_by_executors.yml
    :language: yaml
    :emphasize-lines: 13-25

Now let's run this test and we will see the test using **generic.local.sh** will fail because
we have a returncode mismatch even though both tests got a 0 returncode as its actual value.

.. command-output:: buildtest build -b tutorials/script/status_by_executors.yml

Now let's see the test results by inspecting the metrics field using ``buildtest report``. We see one test
has the metrics name **firstname=Michael** and second test has **lastname=Jackson**.

.. command-output:: buildtest report --format id,name,metrics --filter name=status_returncode_by_executors

run_only
---------

The ``run_only`` property is used for running test given a specific condition has met.
For example, you may want a test to run only if its particular system (Linux, Darwin),
operating system, scheduler, etc...

run_only -  user
~~~~~~~~~~~~~~~~~~~~~~

buildtest will skip test if any of the conditions are not met. Let's take an example
in this buildspec we define a test name **run_only_as_root** that requires **root** user
to run test. The **run_only** is a property of key/value pairs and **user** is one
of the field. buildtest will only build & run test if current user matches ``user`` field.
We detect current user using ``$USER`` and match with input field ``user``.
buildtest will skip test if there is no match.


.. literalinclude:: ../tutorials/root_user.yml
   :language: yaml

Now if we run this test we see buildtest will skip test **run_only_as_root** because
current user is not root.

.. command-output:: buildtest build -b tutorials/root_user.yml
    :returncode: 1

run_only - platform
~~~~~~~~~~~~~~~~~~~~

Similarly, we can run test if it matches target platform. In this example we have
two tests **run_only_platform_darwin** and **run_only_platform_linux** that are
run if target platform is Darwin or Linux. This is configured using ``platform``
field which is a property of ``run_only`` object. buildtest will match
target platform using `platform.system() <https://docs.python.org/3/library/platform.html#platform.system>`_
with field **platform**, if there is no match buildtest will skip test. In this test,
we define a python shell using ``shell: python`` and run ``platform.system()``. We
expect the output of each test to have **Darwin** and **Linux** which we match
with stdout using regular expression.

.. literalinclude:: ../tutorials/run_only_platform.yml
   :language: yaml

This test was ran on a MacOS (Darwin) so we expect test **run_only_platform_linux**
to be skipped.

.. code-block:: console

     bash-3.2$ buildtest build -b tutorials/run_only_platform.yml
    ╭───────────────────────────────────────────────── buildtest summary ──────────────────────────────────────────────────╮
    │                                                                                                                      │
    │ User:               siddiq90                                                                                         │
    │ Hostname:           DOE-7086392.local                                                                                │
    │ Platform:           Darwin                                                                                           │
    │ Current Time:       2021/12/07 22:51:45                                                                              │
    │ buildtest path:     /Users/siddiq90/Documents/GitHubDesktop/buildtest/bin/buildtest                                  │
    │ buildtest version:  0.11.0                                                                                           │
    │ python path:        /Users/siddiq90/.local/share/virtualenvs/buildtest-KLOcDrW0/bin/python                           │
    │ python version:     3.7.3                                                                                            │
    │ Configuration File: /Users/siddiq90/Documents/GitHubDesktop/buildtest/buildtest/settings/config.yml                  │
    │ Test Directory:     /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests                                      │
    │ Command:            /Users/siddiq90/Documents/GitHubDesktop/buildtest/bin/buildtest build -b                         │
    │ tutorials/run_only_platform.yml                                                                                      │
    │                                                                                                                      │
    ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
    ───────────────────────────────────────────────  Discovering Buildspecs ────────────────────────────────────────────────
    Discovered Buildspecs:  1
    Excluded Buildspecs:  0
    Detected Buildspecs after exclusion:  1
                                    Discovered buildspecs
    ╔═══════════════════════════════════════════════════════════════════════════════════╗
    ║ Buildspecs                                                                        ║
    ╟───────────────────────────────────────────────────────────────────────────────────╢
    ║ /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/run_only_platform.yml ║
    ╚═══════════════════════════════════════════════════════════════════════════════════╝
    ────────────────────────────────────────────────── Parsing Buildspecs ──────────────────────────────────────────────────
    [run_only_platform_linux][/Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/run_only_platform.yml]: test is skipped because this test is expected to run on platform: Linux but detected platform: Darwin.
    Valid Buildspecs: 1
    Invalid Buildspecs: 0
    /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/run_only_platform.yml: VALID


    Total builder objects created: 1


                                                        Builder Details
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Builder                        ┃ Executor           ┃ description                   ┃ buildspecs                     ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ run_only_platform_darwin/9bc44 │ generic.local.bash │ This test will only run if    │ /Users/siddiq90/Documents/GitH │
    │ 2db                            │                    │ target platform is Darwin     │ ubDesktop/buildtest/tutorials/ │
    │                                │                    │                               │ run_only_platform.yml          │
    └────────────────────────────────┴────────────────────┴───────────────────────────────┴────────────────────────────────┘
    ──────────────────────────────────────────────────── Building Test ─────────────────────────────────────────────────────
    [22:51:45] run_only_platform_darwin/9bc442db: Creating test directory: /Users/siddiq90/Documents/GitHubDeskt base.py:421
               op/buildtest/var/tests/generic.local.bash/run_only_platform/run_only_platform_darwin/9bc442db
               run_only_platform_darwin/9bc442db: Creating the stage directory: /Users/siddiq90/Documents/GitHub base.py:432
               Desktop/buildtest/var/tests/generic.local.bash/run_only_platform/run_only_platform_darwin/9bc442d
               b/stage
               run_only_platform_darwin/9bc442db: Writing build script: /Users/siddiq90/Documents/GitHubDesktop/ base.py:550
               buildtest/var/tests/generic.local.bash/run_only_platform/run_only_platform_darwin/9bc442db/run_on
               ly_platform_darwin_build.sh
    ──────────────────────────────────────────────────── Running Tests ─────────────────────────────────────────────────────
    ______________________________
    Launching test: run_only_platform_darwin/9bc442db
    run_only_platform_darwin/9bc442db: Running Test via command: bash --norc --noprofile -eo pipefail
    run_only_platform_darwin_build.sh
    run_only_platform_darwin/9bc442db: Test completed with returncode: 0
    run_only_platform_darwin/9bc442db: Test completed in 0.281197 seconds
    run_only_platform_darwin/9bc442db: Writing output file -  /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/ge
    neric.local.bash/run_only_platform/run_only_platform_darwin/9bc442db/run_only_platform_darwin.out
    run_only_platform_darwin/9bc442db: Writing error file - /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/gene
    ric.local.bash/run_only_platform/run_only_platform_darwin/9bc442db/run_only_platform_darwin.err
    run_only_platform_darwin/9bc442db: performing regular expression - '^Darwin$' on file: /Users/siddiq90/Documents/GitHubD
    esktop/buildtest/var/tests/generic.local.bash/run_only_platform/run_only_platform_darwin/9bc442db/run_only_platform_darw
    in.out
    run_only_platform_darwin/9bc442db: Regular Expression Match - Success!
                                                          Test Summary
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┓
    ┃ Builder                       ┃ executor           ┃ status ┃ Checks (ReturnCode, Regex,     ┃ ReturnCode ┃ Runtime  ┃
    ┃                               ┃                    ┃        ┃ Runtime)                       ┃            ┃          ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━┩
    │ run_only_platform_darwin/9bc4 │ generic.local.bash │ PASS   │ False True False               │ 0          │ 0.281197 │
    │ 42db                          │                    │        │                                │            │          │
    └───────────────────────────────┴────────────────────┴────────┴────────────────────────────────┴────────────┴──────────┘



    Passed Tests: 1/1 Percentage: 100.000%
    Failed Tests: 0/1 Percentage: 0.000%


    Writing Logfile to: /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/logs/buildtest_1edlfmz_.log


run_only - scheduler
~~~~~~~~~~~~~~~~~~~~~

buildtest can run test if a particular scheduler is available. In this example,
we introduce a new field ``scheduler`` that is part of ``run_only`` property. This
field expects one of the following values: [``lsf``, ``slurm``, ``cobalt``, ``pbs``]
and buildtest will check if target system supports detects the scheduler. In this example we require
**lsf** scheduler because this test runs **bmgroup** which is a LSF binary.

.. note:: buildtest assumes scheduler binaries are available in $PATH, if no scheduler is found buildtest sets this to an empty list

.. literalinclude:: ../general_tests/sched/lsf/bmgroups.yml
   :language: yaml

If we build this test on a target system without LSF notice that buildtest skips
test **show_host_groups**.

.. command-output:: buildtest build -b general_tests/sched/lsf/bmgroups.yml
    :returncode: 1

run_only - linux_distro
~~~~~~~~~~~~~~~~~~~~~~~~

buildtest can run test if it matches a Linux distro, this is configured using
``linux_distro`` field that is a list of Linux distros that is returned via
`distro.id() <https://distro.readthedocs.io/en/latest/#distro.id>`_. In this example,
we run test only if host distro is ``darwin``.

.. literalinclude:: ../tutorials/run_only_distro.yml
   :language: yaml

This test will run successfully because this was ran on a Mac OS (darwin) system.

.. code-block:: console


    bash-3.2$ buildtest build -b tutorials/run_only_distro.yml
    ╭───────────────────────────────────────────────── buildtest summary ──────────────────────────────────────────────────╮
    │                                                                                                                      │
    │ User:               siddiq90                                                                                         │
    │ Hostname:           DOE-7086392.local                                                                                │
    │ Platform:           Darwin                                                                                           │
    │ Current Time:       2021/12/07 22:50:22                                                                              │
    │ buildtest path:     /Users/siddiq90/Documents/GitHubDesktop/buildtest/bin/buildtest                                  │
    │ buildtest version:  0.11.0                                                                                           │
    │ python path:        /Users/siddiq90/.local/share/virtualenvs/buildtest-KLOcDrW0/bin/python                           │
    │ python version:     3.7.3                                                                                            │
    │ Configuration File: /Users/siddiq90/Documents/GitHubDesktop/buildtest/buildtest/settings/config.yml                  │
    │ Test Directory:     /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests                                      │
    │ Command:            /Users/siddiq90/Documents/GitHubDesktop/buildtest/bin/buildtest build -b                         │
    │ tutorials/run_only_distro.yml                                                                                        │
    │                                                                                                                      │
    ╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
    ───────────────────────────────────────────────  Discovering Buildspecs ────────────────────────────────────────────────
    Discovered Buildspecs:  1
    Excluded Buildspecs:  0
    Detected Buildspecs after exclusion:  1
                                   Discovered buildspecs
    ╔═════════════════════════════════════════════════════════════════════════════════╗
    ║ Buildspecs                                                                      ║
    ╟─────────────────────────────────────────────────────────────────────────────────╢
    ║ /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/run_only_distro.yml ║
    ╚═════════════════════════════════════════════════════════════════════════════════╝
    ────────────────────────────────────────────────── Parsing Buildspecs ──────────────────────────────────────────────────
    [run_only_linux_distro][/Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/run_only_distro.yml]: test is skipped because this test is expected to run on linux distro: ['centos'] but detected linux distro: darwin.
    Valid Buildspecs: 1
    Invalid Buildspecs: 0
    /Users/siddiq90/Documents/GitHubDesktop/buildtest/tutorials/run_only_distro.yml: VALID


    Total builder objects created: 1


                                                        Builder Details
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ Builder                        ┃ Executor           ┃ description                    ┃ buildspecs                    ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
    │ run_only_macos_distro/6c9a59e7 │ generic.local.bash │ Run test only if distro is     │ /Users/siddiq90/Documents/Git │
    │                                │                    │ darwin.                        │ HubDesktop/buildtest/tutorial │
    │                                │                    │                                │ s/run_only_distro.yml         │
    └────────────────────────────────┴────────────────────┴────────────────────────────────┴───────────────────────────────┘
    ──────────────────────────────────────────────────── Building Test ─────────────────────────────────────────────────────
    [22:50:22] run_only_macos_distro/6c9a59e7: Creating test directory: /Users/siddiq90/Documents/GitHubDesktop/ base.py:421
               buildtest/var/tests/generic.local.bash/run_only_distro/run_only_macos_distro/6c9a59e7
               run_only_macos_distro/6c9a59e7: Creating the stage directory: /Users/siddiq90/Documents/GitHubDes base.py:432
               ktop/buildtest/var/tests/generic.local.bash/run_only_distro/run_only_macos_distro/6c9a59e7/stage
               run_only_macos_distro/6c9a59e7: Writing build script: /Users/siddiq90/Documents/GitHubDesktop/bui base.py:550
               ldtest/var/tests/generic.local.bash/run_only_distro/run_only_macos_distro/6c9a59e7/run_only_macos
               _distro_build.sh
    ──────────────────────────────────────────────────── Running Tests ─────────────────────────────────────────────────────
    ______________________________
    Launching test: run_only_macos_distro/6c9a59e7
    run_only_macos_distro/6c9a59e7: Running Test via command: bash --norc --noprofile -eo pipefail
    run_only_macos_distro_build.sh
    run_only_macos_distro/6c9a59e7: Test completed with returncode: 0
    run_only_macos_distro/6c9a59e7: Test completed in 0.104622 seconds
    run_only_macos_distro/6c9a59e7: Writing output file -  /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/gener
    ic.local.bash/run_only_distro/run_only_macos_distro/6c9a59e7/run_only_macos_distro.out
    run_only_macos_distro/6c9a59e7: Writing error file - /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/tests/generic
    .local.bash/run_only_distro/run_only_macos_distro/6c9a59e7/run_only_macos_distro.err
    run_only_macos_distro/6c9a59e7: performing regular expression - '^Darwin$' on file: /Users/siddiq90/Documents/GitHubDesk
    top/buildtest/var/tests/generic.local.bash/run_only_distro/run_only_macos_distro/6c9a59e7/run_only_macos_distro.out
    run_only_macos_distro/6c9a59e7: Regular Expression Match - Success!
                                                          Test Summary
    ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┓
    ┃ Builder                        ┃ executor           ┃ status ┃ Checks (ReturnCode, Regex,    ┃ ReturnCode ┃ Runtime  ┃
    ┃                                ┃                    ┃        ┃ Runtime)                      ┃            ┃          ┃
    ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━┩
    │ run_only_macos_distro/6c9a59e7 │ generic.local.bash │ PASS   │ False True False              │ 0          │ 0.104622 │
    └────────────────────────────────┴────────────────────┴────────┴───────────────────────────────┴────────────┴──────────┘



    Passed Tests: 1/1 Percentage: 100.000%
    Failed Tests: 0/1 Percentage: 0.000%


    Writing Logfile to: /Users/siddiq90/Documents/GitHubDesktop/buildtest/var/logs/buildtest_h1bbn_wt.log
