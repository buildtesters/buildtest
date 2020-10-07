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
by the *script* schema. The **version** field informs which version of subschema to use.
Currently all sub-schemas are at version ``1.0`` where buildtest will validate
with a schema ``script-v1.0.schema.json``. In future, we can support multiple versions
of subschema for backwards compatibility.


Shown below is schema definition for script-v1.0.schema.json ::

    {
      "$id": "script-v1.0.schema.json",
      "$schema": "http://json-schema.org/draft-07/schema#",
      "title": "script schema version 1.0",
      "description": "The script schema is of ``type: script`` in sub-schema which is used for running shell scripts",
      "type": "object",
      "required": ["type", "run", "executor"],
      "additionalProperties": false,
      ...
    }

The ``"type": "object"`` means sub-schema is a JSON `object <http://json-schema.org/understanding-json-schema/reference/object.html>`_
where we define a list of key/value pair. The sub-schemas are of type ``object``
and have a list of required fields that must be provided when using the schema.
The ``"required"`` field specifies a list of fields that must be specified in
order to validate the Buildspec. In this example, ``type``, ``run``, ``executor``
are required fields. The ``additionProperties: false`` informs schema to reject
any extra properties not defined in schema. In our previous example, the JSON
object is ``variables``.

The **executor** key is required for all sub-schemas which instructs buildtest
which executor to use when running the test. The executors are defined in your
buildtest settings in :ref:`configuring_buildtest`.

In this example we define variables using the ``vars`` property which is a Key/Value
pair for variable assignment. The **run** section is required for script schema which
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
for writing the content of test.

For more details on script schema see schema docs at https://buildtesters.github.io/buildtest/


Return Code Matching
---------------------

buildtest can report PASS/FAIL based on returncode, by default a 0 exit code is PASS
and everything else is FAIL. The returncode can be a list of exit codes to match.
In this example we have four tests called ``exit1_fail``, ``exit1_pass``,
``returncode_list_mismatch`` and ``returncode_int_match``.  We expect **exit1_fail** and
**returncode_mismatch** to FAIL while **exit1_pass** and **returncode_int_match**
will PASS.

.. program-output:: cat ../tutorials/pass_returncode.yml

To demonstrate we will build this test and pay close attention to the **Status**
column in output.

.. program-output:: cat docgen/schemas/pass_returncode.txt


The ``returncode`` field can be an integer or list of integers. If you specify
a list of exit codes, buildtest will ``PASS`` test if actual exit code is found in
list.

A floating point exit-code is invalid::

  returncode: 1.5

If **returncode** is a list, all items must be integers and unique items.
The list must contain **atleast** one item. The following examples are invalid
values for returncode::

  returncode: []

  returncode: [1, 1.5]

  returncode: [1, 2, 5, 5]

Classifying tests with tags
----------------------------

The ``tags`` field can be used to classify tests which can be used to organize tests
or :ref:`build_by_tags` (``buildtest build --tags <TAGNAME>``).
Tags can be defined as a string or list of strings. In this example, the test
``string_tag`` defines a tag name **network** while test ``list_of_strings_tags``
define a list of tags named ``network`` and ``ping``.

.. program-output:: cat ../tutorials/tags_example.yml

Each item in tags must be a string and no duplicates are allowed, for example in
this test, we define a duplicate tag **network** which is not allowed.

.. program-output:: cat ../tutorials/invalid_tags.yml

If we run this test and inspect the logs we will see an error message in schema validation::

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

By default buildtest will default to ``bash``, but we can configure shell
option using the ``shell`` field. The shell field is defined in schema as follows::

    "shell": {
          "type": "string",
          "description": "Specify a shell launcher to use when running jobs. This sets the shebang line in your test script. The ``shell`` key can be used with ``run`` section to describe content of script and how its executed",
          "pattern": "^(/bin/bash|/bin/sh|sh|bash|python).*"
        },

The shell pattern is a regular expression where one can specify a shell name along
with shell options. The shell will configure the `Shebang Line <https://en.wikipedia.org/wiki/Shebang_(Unix)>`_
in the test-script. In this example, we illustrate a few tests using different shell
field.

.. program-output:: cat tutorials/shell_examples.yml

The generated test-script for buildspec *_bin_sh_shell* will specify shebang
**/bin/sh** because we specified ``shell: /bin/sh``::

    #!/bin/sh
    source /Users/siddiq90/Documents/buildtest/var/executors/local.sh/before_script.sh
    bzip2 --help
    source /Users/siddiq90/Documents/buildtest/var/executors/local.sh/after_script.sh

If you don't specify a shell path such as ``shell: sh``, then buildtest will resolve
path by looking in $PATH and build the shebang line.

In test *shell_options* we specify ``shell: "sh -x"``, buildtest will tack on the
shell options into the shebang line. The generated test for this script is the following::

    #!/bin/sh -x
    source /Users/siddiq90/Documents/buildtest/var/executors/local.sh/before_script.sh
    echo $SHELL
    hostname
    source /Users/siddiq90/Documents/buildtest/var/executors/local.sh/after_script.sh

Customize Shebang
-----------------

You may customize the shebang line in testscript using ``shebang`` field. This
takes precedence over the `shell` option which automatically detects the shebang
based on shell path.

In next example we have two tests **bash_login_shebang** and **bash_nonlogin_shebang**
which tests if shell is Login or Non-Login. The ``#!/bin/bash -l`` indicates we
want to run in login shell and expects an output of **Login Shell** while
test **bash_nonlogin_shebang** should run in default behavior which is non-login
shell and expects output **Not Login Shell**. We match this with regular expression
with stdout stream.

.. program-output:: cat tutorials/shebang.yml

Now let's run this test as we see the following.

.. program-output:: cat docgen/getting_started/shebang.txt

If we look at the generated test for **bash_login_shebang** we see the shebang line
is passed into the script::

    #!/bin/bash -l
    source /Users/siddiq90/Documents/buildtest/var/executors/local.bash/before_script.sh
    shopt -q login_shell && echo 'Login Shell' || echo 'Not Login Shell'
    source /Users/siddiq90/Documents/buildtest/var/executors/local.bash/after_script.sh


Python Shell
---------------

You can use *script* schema to write python scripts using the run section. This
can be achieved if you use the ``local.python`` executor assuming you have this
defined in your buildtest configuration.

Here is a python example calculating area of circle

.. program-output:: cat ../tutorials/python-shell.yml


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
below is an example test.

.. program-output:: cat ../tutorials/skip_tests.yml

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

run_only
---------

The ``run_only`` property is used for running test given a specific condition has met.
For example, you may want a test to run only if its particular system (Linux, Darwin),
operating system, scheduler, etc...

run_only -  user
~~~~~~~~~~~~~~~~~~~~~~

buildtest will skip test if any of the conditions are not met. Let's take an example
in this buildspec we define a test name **run_only_as_root** that requires **root** user
to run test. The *run_only* is a property of key/value pairs and **user** is one
of the field. buildtest will only build & run test if current user matches ``user`` field.
We detect current user using ``$USER`` and match with input field ``user``.
buildtest will skip test if there is no match.


.. program-output:: cat ../tutorials/root_user.yml

Now if we run this test we see buildtest will skip test **run_only_as_root** because
current user is not root.

.. program-output:: cat docgen/schemas/root_user.txt

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

.. program-output:: cat ../tutorials/run_only_platform.yml

This test was run on a Mac OS (Darwin) so we expect **run_only_platform_linux**
to be skipped.

.. program-output:: cat docgen/schemas/run_only_platform.txt

run_only - scheduler
~~~~~~~~~~~~~~~~~~~~~

buildtest can run test if a particular scheduler is available. In this example,
we introduce a new field ``scheduler`` that is part of ``run_only`` property. This
field expects ``lsf`` or ``slurm`` as valid values and buildtest will check if target
system supports the scheduler. In this example we require **lsf** scheduler because
this test runs **bmgroup** which is a LSF binary.

.. note:: buildtest assumes scheduler binaries are available in $PATH, if no scheduler is found buildtest sets this to an empty list

.. program-output:: cat ../general_tests/sched/lsf/bmgroups.yml

If we build this test on a target system without LSF notice that buildtest skips
test **show_host_groups**.

.. program-output:: cat docgen/schemas/bmgroups.txt


run_only - linux_distro
~~~~~~~~~~~~~~~~~~~~~~~~

buildtest can run test if it matches a Linux distro, this is configured using
``linux_distro`` field that is a list of Linux distros that is returned via
`distro.id() <https://distro.readthedocs.io/en/latest/#distro.id>`_. In this example,
we run test only if host distro is ``darwin``.

.. program-output:: cat ../tutorials/run_only_distro.yml

This test will run successfully because this was ran on a Mac OS (darwin) system.

.. program-output:: cat docgen/schemas/run_only_distro.txt

