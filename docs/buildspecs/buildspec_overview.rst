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
   :emphasize-lines: 1-3,7-10

buildtest will validate the entire buildspec with `global.schema.json <https://github.com/buildtesters/buildtest/blob/devel/buildtest/schemas/global.schema.json>`_,
and use one of the sub-schema to validate the test defined in *buildspec* section. The **buildspec**
is where you define a test, in the example above the name of the test is **add_numbers**.
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
    :emphasize-lines: 7-14

The test name **systemd_default_target** defined in **buildspec** section is
validated with the following pattern ``"^[A-Za-z_][A-Za-z0-9_]*$"``. This test
will use the executor **generic.local.bash** which means it will use the Local Executor
with an executor name `bash` defined in the buildtest settings. The default
buildtest settings will provide a bash executor as follows:

.. code-block:: yaml
   :emphasize-lines: 4-8

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
   :lines: 1-12

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

.. _environment_variables:

Declaring Environment Variables
--------------------------------

You can define environment variables using the ``env`` property, this is compatible
with shells: ``bash``, ``sh``, ``zsh``, ``csh`` and ``tcsh``. It does not work with
``shell: python``. In example below we declare three tests using environment
variable with default shell (bash), csh, and tcsh

.. literalinclude:: ../tutorials/environment.yml
   :language: yaml
   :emphasize-lines: 6-8,20,22-23,30,32-33

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
   :emphasize-lines: 7-17

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
    :emphasize-lines: 6


If tags is a list, it must contain atleast **one** item.


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