.. _buildspec_overview:

Buildspec Overview
========================

.. _what_is_buildspec:

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

.. dropdown:: ``buildtest build -b $BUILDTEST_ROOT/tutorials/vars.yml``

   .. command-output:: buildtest build -b $BUILDTEST_ROOT/tutorials/vars.yml
      :shell:

Let's check the generated script from the previous build, you can run ``buildtest inspect query -o variables_bash`` where
`-o` refers to output file for testname `variables_bash`. Take note of the output file we

.. dropdown:: ``buildtest inspect query -o variables_bash``

   .. command-output:: buildtest inspect query -o variables_bash

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


If tags is a list, it must contain atleast **one** item.

.. _status:

Test Status
-----------

buildtest will record state of each test which can be ``PASS`` or ``FAIL``. By default a 0 exit code is
PASS and everything else is a FAIL. The ``status`` property can be used to determine how test will report its state.
Currently, we can match state based on the following:

  - :ref:`Return Code <returncode>`
  - :ref:`Runtime <runtime>`
  - :ref:`Regular Expression <regex>`
  - :ref:`Performance Check <perf_checks>`
  - :ref:`Explicit Test Status <explicit_status>`
  - :ref:`File Checks <file_checks>`

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

.. dropdown:: ``buildtest build -b tutorials/test_status/pass_returncode.yml``

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

.. dropdown:: ``buildtest build -b tutorials/test_status/status_regex.yml``

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

.. dropdown:: ``buildtest build -b tutorials/test_status/runtime_status_test.yml``

   .. command-output:: buildtest build -b tutorials/test_status/runtime_status_test.yml

If we look at the test results, we expect the first three tests **timelimit_min**, **timelimit_max**, **timelimit_min_max**
will pass while the last two tests fail because it fails to comply with runtime property.

.. dropdown:: ``buildtest report --filter buildspec=tutorials/test_status/runtime_status_test.yml --format name,id,state,runtime --latest``

   .. command-output:: buildtest report --filter buildspec=tutorials/test_status/runtime_status_test.yml --format name,id,state,runtime --latest

.. _explicit_status:

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

.. dropdown:: ``buildtest build -b tutorials/test_status/explicit_state.yml``

   .. command-output:: buildtest build -b tutorials/test_status/explicit_state.yml

.. _file_checks:

File Checks
~~~~~~~~~~~~~

buildtest supports various file checks that can be used as means for passing test.

For instance, if you want to check for file existence, you can use  ``exists`` property
which expects a list of file or directory names to check. This can be useful if your test
will write some output file or directory and test will pass based on existence of file/directory.

In the example below we have two tests, first test will pass, where all files exist. We check for
files and directory path, note variable and shell expansion is supported.

In the second example, we expect this test to fail because filename **bar** does not exist.

.. literalinclude:: ../tutorials/test_status/exists.yml
   :language: yaml
   :emphasize-lines: 10-15,21-23

We can run this test by running the following, take note of the output.

.. dropdown:: ``buildtest build -b tutorials/test_status/exists.yml``

   .. command-output:: buildtest build -b tutorials/test_status/exists.yml

Each item in the ``exists`` field must be a string, which can lead to issue in example
below let's assume we want a test to pass based on a directory name **1**, if we specify
as follows, this test will fail validation.

.. literalinclude:: ../tutorials/test_status/file_exists_exception.yml
   :language: yaml
   :emphasize-lines: 7-8

We can validate this buildspec by running the following

.. dropdown:: ``buildtest bc validate -b tutorials/test_status/file_exists_exception.yml``
   :color: warning

    .. command-output:: buildtest bc validate -b tutorials/test_status/file_exists_exception.yml
       :returncode: 1

In order to run this test, we need to enclose each item in quotes. Shown below is the same test with quotations.

.. literalinclude:: ../tutorials/test_status/file_exists_with_number.yml
   :language: yaml
   :emphasize-lines: 7-8

Let's validate and build this test.


.. dropdown:: ``buildtest bc validate -b tutorials/test_status/file_exists_with_number.yml``

    .. command-output:: buildtest bc validate -b tutorials/test_status/file_exists_with_number.yml

.. dropdown:: ``buildtest build -b tutorials/test_status/file_exists_with_number.yml``

    .. command-output:: buildtest build -b tutorials/test_status/file_exists_with_number.yml

In the next example, we introduce checks for files and directory via ``is_file`` and
``is_dir`` property, which behaves similar to ``exists`` except they will check if each item
is a file or directory. We expect the first test to fail, because **$HOME/.bashrc** is
not a directory but a file. The second test will incorporate the same test and
use ``is_file`` for status check.

.. literalinclude:: ../tutorials/test_status/file_and_dir_check.yml
   :language: yaml
   :emphasize-lines: 7-11,17-22

Let's build the test and see the output.

.. dropdown:: ``buildtest build -b tutorials/test_status/file_and_dir_check.yml``

   .. command-output:: buildtest build -b tutorials/test_status/file_and_dir_check.yml

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

.. dropdown:: ``buildtest build -b tutorials/skip_tests.yml``

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

.. dropdown:: ``buildtest build -b tutorials/skip_buildspec.yml``

    .. command-output:: buildtest build -b tutorials/skip_buildspec.yml
       :returncode: 1