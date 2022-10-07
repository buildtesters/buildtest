.. _buildspec_overview:

Buildspec Overview
========================

What is a buildspec?
---------------------

A **buildspec** is a YAML file that defines your test in buildtest which is validated by schema followed
by building a shell script and running the generated test. Buildtest will parse the buildspec with the
:ref:`global schema file <global_schema>` which defines the top-level structure of buildspec file.

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
by the *script* schema.

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
summary of the test. The `description` field is limited to 80 characters. 
In this example we can specify multiple commands in ``run`` section, this
can be done in YAML using ``run: |`` followed by content of run section tab indented
2 spaces.

In this next example, we introduce the ``summary`` field, which can be used as an extended description of test. It has no 
impact on the test. Unlike the ``description`` field, the summary field has no limit on character count and one can define multi-line
string using the pipe symbol **|**. 

.. literalinclude:: ../tutorials/summary_example.yml
    :language: yaml
    :emphasize-lines: 5,7,8,9



.. _script_schema:

Script Schema
---------------

The script schema is used for writing simple scripts (bash, sh, python) in Buildspec.
To use this schema you must set ``type: script``. The ``run`` field is responsible
for writing the content of test.


Shown below is schema header for `script.schema.json <https://github.com/buildtesters/buildtest/blob/devel/buildtest/schemas/script.schema.json>`_.

.. literalinclude:: ../../buildtest/schemas/script.schema.json
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

.. literalinclude:: ../tutorials/test_status/pass_returncode.yml
   :language: yaml
   :emphasize-lines: 17,26,35

Let's build this test and pay close attention to the **status**
column in output.

.. command-output:: buildtest build -b tutorials/test_status/pass_returncode.yml
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

.. literalinclude:: ../tutorials/test_status/status_regex.yml
   :language: yaml
   :emphasize-lines: 9-11,20-22

Now if we run this test, we will see first test will pass while second one will fail even though the returncode is
a 0. Take a close look at the **status** property

.. command-output:: buildtest build -b tutorials/test_status/status_regex.yml

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

.. literalinclude:: ../tutorials/test_status/runtime_status_test.yml
   :language: yaml
   :emphasize-lines: 9-11,20-21,30-31,40-41,50-51

.. command-output:: buildtest build -b tutorials/test_status/runtime_status_test.yml

If we look at the test results, we expect the first three tests **timelimit_min**, **timelimit_max**, **timelimit_min_max**
will pass while the last two tests fail because it fails to comply with runtime property.

.. command-output:: buildtest report --filter buildspec=tutorials/test_status/runtime_status_test.yml --format name,id,state,runtime --latest

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

.. literalinclude:: ../tutorials/test_status/explicit_state.yml
   :language: yaml
   :emphasize-lines: 8,16,22-25,31-34

If we build this test, we expect buildtest to honor the value of ``state`` property

.. command-output:: buildtest build -b tutorials/test_status/explicit_state.yml

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
    :emphasize-lines: 6,13

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
   :emphasize-lines: 6,14,22,30,38

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
   :emphasize-lines: 6,14

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

Skipping a buildspec
---------------------

Sometimes you may want to skip all test in a buildspec instead of updating every test with ``skip`` property, this can be done by setting
**skip** at the top-level. This can be useful if you are running several test in a directory such as ``buildtest build -b dir1/`` and you don't
want to explicitly exclude file via ``-x``  option every time, instead you can hardcode this into the buildspec. A typical use-case of skipping
test is when a test is broken and you don't want to run it then its good idea to set ``skip: yes`` on the buildspec and fix it later.

In this next example we set ``skip: yes``, buildtest will skip the buildspec and no test will be processed even if ``skip`` is set in each test.

.. literalinclude:: ../tutorials/skip_buildspec.yml
   :language: yaml
   :emphasize-lines: 1

If you try building this buildspec, you will see buildtest will skip the buildspec and terminate.

.. command-output:: buildtest build -b tutorials/skip_buildspec.yml
   :returncode: 1

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
    :emphasize-lines: 8-17

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


Test Dependency
---------------


.. Note:: This feature is subject to change


Buildtest can support test dependencies which allows one to specify condition before running a test. Let's take a look
at this next example, we have a buildspec with three tests ``jobA``, ``jobB``, and ``jobC``. The test `jobA` will run immediately
but now we introduce a new keyword ``needs`` which is a list of test names as dependency. We want test `jobB` to run after jobA is
complete, and `jobC` to run once jobA and jobB is complete.

.. literalinclude:: ../tutorials/job_dependency/ex1.yml
   :language: yaml
   :emphasize-lines: 2,10,14,19,23

The ``needs`` property expects a list of strings, and values must match name of test.  If you specify an invalid
test name in `needs` property then buildtest will ignore the value. If multiple tests are specified in `needs` property then
all test must finish prior to running test.

Let's run this test, and take a note that buildtest will run test `jobA`, followed by `jobB` then `jobC`.

.. command-output:: buildtest build -b tutorials/job_dependency/ex1.yml

Test Dependency by returncode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this next example, we can control behavior of job dependency based on returncode for a given test. This test has three
tests: ``test1``, ``test2`` and ``test3``. The first test will exit with returncode 1 but this test will pass because we have
set ``state: PASS`` to override the status check. The next test ``test2`` requires **test1** to have a returncode of 1 in order
to satisfy dependency. The ``returncode`` property expects a valid returncode and it can be a list of returncode similar to
how one specify ``returncode`` under the **status** property see :ref:`returncode`. The ``needs`` property can support multiple
test with returncode, in ``test3`` we require ``test1`` to have returncode 1 while ``test2`` has a returncode of 2. We expect `test2`
to return a returncode of 2 because of ``exit 2`` statement so we expect all three tests to run.

.. literalinclude:: ../tutorials/job_dependency/ex2.yml
   :language: yaml
   :emphasize-lines: 2,7-8,10,17-19,21,28-32

Let's build this test and take note of execution order of test.

.. command-output:: buildtest build -b tutorials/job_dependency/ex2.yml

Test Dependency by state
~~~~~~~~~~~~~~~~~~~~~~~~~

You can specify ``state`` as a property to check for test state when specify test dependency. In this next example, we have
have four tests **pass_test**, **fail_test**, **pass_and_fail_test**, and **final_test**. The first test will be a PASS because
we have ``state: PASS``. The test ``fail_test`` depends on `pass_test` only if it has ``state: PASS``, if value is mismatch then test
will be skipped. Note that buildtest will skip test until next iteration if test is not executed, however if test is complete then buildtest
will cancel dependent test. We can specify multiple test dependencies with `state` property such as test **pass_and_fail_test** which expects
``pass_test`` to have `state: PASS` and ``fail_test`` to have `state: FAIL`. In test ``final_test``, shows how you can combine the format, the
``needs`` property is a list of object where each element is name of test. If no properties are associated with test name then buildtest will
wait until job is complete to execute test. In this example, the test expects both ``pass_test`` and ``fail_test`` to run while ``pass_and_fail_test``
must have returncode of 1.

.. literalinclude:: ../tutorials/job_dependency/ex3.yml
   :language: yaml
   :emphasize-lines: 2,6-7,12,18-20,25,29-33,40,44-48

Let's build this test and take note all tests are run.

.. command-output:: buildtest build -b tutorials/job_dependency/ex3.yml


In this next example, we have three tests the first test will ``runtime_test`` will sleep for 5 seconds but it will fail due to runtime
requirement of 2sec. The next two tests ``runtime_test_pass`` and ``runtime_test_fail`` both depend on ``runtime_test`` however due to condition
only one of them can be run because ``runtime_test_pass`` expects `runtime_test` to have `state: PASS` while ``runtime_test_fail`` expects `runtime_test`
to have `state: FAIL`. This type of workflow can be used if you want to run a set of test based on one condition while running a different set of
test based on the negative condition.

.. literalinclude:: ../tutorials/job_dependency/ex4.yml
   :language: yaml
   :emphasize-lines: 2,6-8,11,15-17,20,24-26

Let's build this test and take note that we only run two tests and **runtime_test_fail** was skipped because test **runtime_test** has a
``state: PASS``.

.. command-output:: buildtest build -b tutorials/job_dependency/ex4.yml

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

.. literalinclude:: ../tutorials/multi_executors/executor_regex_script.yml
   :language: yaml

If we build this test, notice that there are two tests, one for each executor.

.. command-output:: buildtest build -b tutorials/multi_executors/executor_regex_script.yml

Multiple Executors
~~~~~~~~~~~~~~~~~~~

.. Note:: This feature is in active development

.. Note:: This feature is compatible with ``type: script`` and ``type: spack``.

The ``executors`` property can be used to define executor specific configuration
for each test, currently this field can be used with :ref:`vars <variables>`, :ref:`env <environment_variables>`
, scheduler directives: ``sbatch``, ``bsub``, ``pbs``, ``cobalt`` and :ref:`cray burst buffer/data warp <cray_burstbuffer_datawarp>`.
The ``executors`` field is a JSON object that expects name of executor followed by property set per executor. In this next example,
we define variables ``X``, ``Y`` and environment ``SHELL`` based on executors **generic.local.sh** and **generic.local.bash**.

.. literalinclude:: ../tutorials/multi_executors/executors_var_env_declaration.yml
   :language: yaml
   :emphasize-lines: 12-23

Let's build this test.

.. command-output:: buildtest build -b tutorials/multi_executors/executors_var_env_declaration.yml

Now let's look at the generated content of the test as follows. We will see that buildtest will
set **X=1**, **Y=3** and **SHELL=bash** for ``generic.local.bash`` and **X=2**, **Y=4** and **SHELL=sh** for
``generic.local.sh``

.. command-output:: buildtest inspect query -t executors_vars_env_declaration/

Scheduler Directives
~~~~~~~~~~~~~~~~~~~~~~

We can also define scheduler directives based on executor type, in this example we define
``sbatch`` property per executor type. Note that ``sbatch`` property in the ``executors`` section
will override the ``sbatch`` property defined in the top-level file otherwise it will use the default.


.. literalinclude:: ../tutorials/multi_executors/executor_scheduler.yml
   :language: yaml


.. command-output:: buildtest build -b tutorials/multi_executors/executor_scheduler.yml

If we inspect this test, we will see each each test have different ``#SBATCH`` directives for each test
based on the ``sbatch`` property defined in the ``executors`` field.

.. command-output:: buildtest inspect query -t executors_sbatch_declaration/

Cray Burst Buffer and Data Warp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also define ``BB`` and ``DW`` directives in the ``executors`` field to override
cray burst buffer and data warp settings per executor. buildtest will use the fields ``BB``
and ``DW`` and insert the ``#BB`` and ``#DW`` directives in the job script. For more details
see :ref:`cray_burstbuffer_datawarp`.

.. literalinclude:: ../tutorials/burstbuffer_datawarp_executors.yml
    :language: yaml


Custom Status by Executor
~~~~~~~~~~~~~~~~~~~~~~~~~

The :ref:`status <status>` and :ref:`metrics <metrics>` field are supported in ``executors``
which can be defined within the named executor. In this next example, we will define executor ``generic.local.bash`` to
match for returncode **0** or **2** while second test will use executor ``generic.local.sh`` to match returncode of **1**.

.. literalinclude:: ../tutorials/multi_executors/status_by_executors.yml
    :language: yaml
    :emphasize-lines: 8-14

Now let's run this test and we will see the test using executor **generic.local.sh** will fail because
we have a returncode mismatch even though both tests got a 0 returncode as its actual value.

.. command-output:: buildtest build -b tutorials/multi_executors/status_by_executors.yml
