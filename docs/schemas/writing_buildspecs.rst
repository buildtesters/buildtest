.. writing_buildspecs:

Writing buildspecs
===================

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
example using the `script` schema with test name called `systemd_default_target`
which is used to check default target on system.

::

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
in output::


    $ buildtest build -b pass_returncode.yml
    Paths:
    __________
    Prefix: /private/tmp
    Buildspec Search Path: ['/private/tmp/github.com/buildtesters/buildtest-cori', '/Users/siddiq90/.buildtest/site']
    Test Directory: /private/tmp/tests

    Stage: Discovered Buildspecs


    +-------------------------------+
    | Stage: Discovered Buildspecs  |
    +-------------------------------+

    /Users/siddiq90/Documents/tutorials/examples/pass_returncode.yml

    Excluded Buildspecs:  []

    +----------------------+
    | Stage: Building Test |
    +----------------------+

    Name                      Schema Validation File    TestPath                                 Buildspec
    ________________________________________________________________________________________________________________________________________________________________
    exit1_fail                script-v1.0.schema.json   /private/tmp/tests/pass_returncode/exit1_fail.sh /Users/siddiq90/Documents/tutorials/examples/pass_returncode.yml
    exit1_pass                script-v1.0.schema.json   /private/tmp/tests/pass_returncode/exit1_pass.sh /Users/siddiq90/Documents/tutorials/examples/pass_returncode.yml
    returncode_mismatch       script-v1.0.schema.json   /private/tmp/tests/pass_returncode/returncode_mismatch.sh /Users/siddiq90/Documents/tutorials/examples/pass_returncode.yml

    +----------------------+
    | Stage: Running Test  |
    +----------------------+

    Name                 Executor             Status               Return Code          Buildspec Path
    ________________________________________________________________________________________________________________________
    exit1_fail           local.sh             FAIL                 1                    /Users/siddiq90/Documents/tutorials/examples/pass_returncode.yml
    exit1_pass           local.sh             PASS                 1                    /Users/siddiq90/Documents/tutorials/examples/pass_returncode.yml
    returncode_mismatch  local.sh             FAIL                 2                    /Users/siddiq90/Documents/tutorials/examples/pass_returncode.yml

    +----------------------+
    | Stage: Test Summary  |
    +----------------------+

    Executed 3 tests
    Passed Tests: 1/3 Percentage: 33.333%
    Failed Tests: 2/3 Percentage: 66.667%


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
        description: "Calculate circle of area given a radius"
        run: |
          import math
          radius = 2
          area = math.pi * radius * radius
          print("Circle Radius ", radius)
          print("Area of circle ", area)


Python scripts are very picky when it comes to formatting, in the ``run`` section
if you are defining multiline python script you must remember to use 2 space indent
to register multiline string. buildtest will extract the content from run section
and inject in your test script. To ensure proper formatting for a more complex python
script you may be better of writing a python script in separate file and call it
in ``run`` section.