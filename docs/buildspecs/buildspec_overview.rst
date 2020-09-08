.. _buildspec_overview:

Buildspecs Overview
========================

buildspec is your test recipe that buildtest processes to generate a test script.
A buildspec can be composed of several test sections. The buildspec file is
validated with the :ref:`global_schema` and each test section is validated with
a sub-schema defined by the ``type`` field.

Let's start off with an example::

    version: "1.0"
    buildspecs:
      variables:
        type: script
        executor: local.bash
        vars:
          X: 1
          Y: 2
        run: echo "$X+$Y=" $(($X+$Y))

buildtest will validate the entire file with ``global.schema.json``, the schema
requires **version** and **buildspec** in order to validate file. The **buildspec**
is where you define each test. In this example their is one test called **variables**.
The test requires a **type** field which is the sub-schema used to validate the
test section. In this example ``type: script`` informs buildtest to use the :ref:`script_schema`
when validating test section.

Each subschema has a list of field attributes that are supported, for example the
fields: **type**, **executor**, **vars** and **run** are all valid fields supported
by the script schema. The **version** field informs which version of subschema to use.
Currently all sub-schemas are at version ``1.0`` where buildtest will validate
with a schema ``script-v1.0.schema.json``. In future, we can support multiple versions
of subschema for backwards compatibility.

The **executor** key is required for all sub-schemas which instructs buildtest
which executor to use when running the test. The executors are defined in your
buildtest settings in :ref:`configuring_buildtest`.

In this example we define variables using the `vars` section which is a Key/Value
pair for variable assignment. The `run` section is required for script schema which
defines the content of the test script.

Let's look at a more interesting example, shown below is a multi line run
example using the `script` schema with test name called
`systemd_default_target`, shown below is the content of test::

    version: "1.0"
    buildspecs:
      systemd_default_target:
        executor: local.bash
        type: script
        description: check if default target is multi-user.target
        run: |
          if [ "multi-user.target" == `systemctl get-default` ]; then
            echo "multi-user is the default target";
            exit 0
          fi
          echo "multi-user is not the default target";
          exit 1
        status:
          returncode: 0

The test name **systemd_default_target** defined in **buildspec** section is
validated with the following pattern ``"^[A-Za-z_][A-Za-z0-9_]*$"``. This test
will use the executor **local.bash** which means it will use the Local Executor
with an executor name `bash` defined in the buildtest settings. The default
buildtest settings will provide a bash executor as follows::

    executors:
      local:
        bash:
          description: submit jobs on local machine using bash shell
          shell: bash

The ``shell: bash`` indicates this executor will use `bash` to run the test scripts.
To reference this executor use the format ``<type>.<name>`` in this case **local.bash**
refers to bash executor.

The ``description`` field is an optional key that can be used to provide a brief
summary of the test. In this example we can a full multi-line run section, this
is achieved in YAML using ``run: |`` followed by content of run section tab indented
2 spaces.

In this example we introduce a new field `status` that is used for controlling how
buildtest will mark test state. By default, a returncode of **0** is PASS and non-zero
is a **FAIL**. Currently buildtest reports only two states: ``PASS``, ``FAIL``.
In this example, buildtest will match the actual returncode with one defined
in key `returncode` in the status section.

.. _script_schema:

Script Schema
---------------

The script schema is used for writing simple scripts (bash, sh, python) in Buildspec.
To use this schema you must set ``type: script``. The `run` field is responsible
for writing the content of test. The `Production Schema <https://raw.githubusercontent.com/buildtesters/buildtest/devel/buildtest/schemas/script-v1.0.schema.json>`_
and `Development Schema <https://buildtesters.github.io/schemas/schemas/script-v1.0.schema.json>`_
are kept in sync where any schema development is done in **Development Schema** followed
by merge to **Production Schema**.

Return Code Matching
---------------------

In this next example we will illustrate the concept of returncode match with
different exit codes. In this example we have three tests called ``exit1_fail``,
``exit1_pass`` and ``returncode_mismatch``. All test are using the ``local.sh``
executor which is using ``sh`` to run the test. We expect **exit1_fail** and
**returncode_mismatch** to FAIL while **exit1_pass** will PASS since returncode matches

::

    version: "1.0"
    buildspecs:

      exit1_fail:
        executor: local.sh
        type: script
        description: exit 1 by default is FAIL
        run: exit 1

      exit1_pass:
        executor: local.sh
        type: script
        description: report exit 1 as PASS
        run: exit 1
        status:
          returncode: 1

      returncode_mismatch:
        executor: local.sh
        type: script
        description: exit 2 failed since it failed to match returncode 1
        run: exit 2
        status:
          returncode: 1

To demonstrate we will build this test and pay close attention to the Status field
in output

.. program-output:: cat docgen/schemas/pass_returncode.txt

Python example
---------------

You can use *script* schema to write python scripts using the run section. This
can be achieved if you use the ``local.python`` executor assuming you have this
defined in your buildtest configuration.

Here is a python example calculating area of circle::

    version: "1.0"
    buildspecs:
      circle_area:
        executor: local.python
        type: script
        shell: python
        description: "Calculate circle of area given a radius"
        tags: ["python"]
        run: |
          import math
          radius = 2
          area = math.pi * radius * radius
          print("Circle Radius ", radius)
          print("Area of circle ", area)


The ``shell: python`` will let us write python script in the ``run`` section.
The ``tags`` field can be used to classify test, the field expects an array of
string items.

.. note::
    Python scripts are very picky when it comes to formatting, in the ``run`` section
    if you are defining multiline python script you must remember to use 2 space indent
    to register multiline string. buildtest will extract the content from run section
    and inject in your test script. To ensure proper formatting for a more complex python
    script you may be better of writing a python script in separate file and call it
    in ``run`` section.

Skipping test
-------------

By default, buildtest will run all tests defined in ``buildspecs`` section, if you
want to skip a test use the ``skip:`` field which expects a boolean value. Shown
below is an example test::

    version: "1.0"
    buildspecs:
      skip:
        type: script
        executor: local.bash
        skip: true
        run: hostname

      unskipped:
        type: script
        executor: local.bash
        skip: false
        run: hostname

The first test `skip` will be skipped by buildtest because ``skip: true`` is defined.

.. note::

    YAML and JSON have different representation for boolean. For json schema
    valid values are ``true`` and ``false`` see https://json-schema.org/understanding-json-schema/reference/boolean.html
    however YAML has many more representation for boolean see https://yaml.org/type/bool.html. You
    may use any of the YAML boolean, however it's best to stick with json schema values
    ``true`` and ``false``.


Here is an example build, notice message ``[skip] test is skipped`` during the build
stage

.. program-output:: cat docgen/schemas/skip_tests.txt

Script Schema and Examples
---------------------------------------

buildtest command line interface provides access to schemas and example buildspecs
for each schemas.

To retrieve the full json schema of script schema you can run the following::

  $ buildtest schema -n script-v1.0.schema.json --json

To retrieve buildspec examples for **script-v1.0.schema.json** you can run the following::

  $ buildtest schema -n script-v1.0.schema.json --example

