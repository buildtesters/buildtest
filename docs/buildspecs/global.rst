.. _global_schema:

Global Schema
==============

The global schema is validated with for all schema types and is the top-level
schema when defining a Buildspec.

For more details see `Global Schema Documentation <https://buildtesters.github.io/schemas/schemadocs/global>`_.

Schema Files
-------------

- `Production Schema <https://raw.githubusercontent.com/buildtesters/buildtest/devel/buildtest/schemas/global.schema.json>`_
- `Development Schema <https://buildtesters.github.io/schemas/schemas/global.schema.json>`_

Global Keys in buildspec
--------------------------

The global keys required for buildspec are ``version`` and ``buildspecs``. The
version key is required to validate with sub-schema when used with ``type`` field.
The ``buildspecs`` is the start of test section. The ``maintainers`` is an optional
field that is an array which can be used to identity maintainer of test. To understand
how buildtest validates the buildspec see :ref:`parse_stage`.

Shown below is an example buildspec.

.. program-output:: cat ../tutorials/hello_world.yml


In this example, the global schema validates the following section::

    version: "1.0"
    buildspecs:
      hello_world:

    maintainers:
      - "@shahzebsiddiqui"

The field ``version`` ``buildspecs`` and ``maintainers`` are validated with **global.schema.json**
using `jsonschema.validate <https://python-jsonschema.readthedocs.io/en/stable/_modules/jsonschema/validators/#validate>`_
method. The sub-schema is the following section which is validated with the ``type`` schema::

    hello_world:
      executor: local.bash
      type: script
      description: "hello world example"
      run: echo "hello world!"

Every sub-schema requires **type** field in this case, ``type: script`` directs
buildtest to validate with the script schema. All type schemas have a version,
currently buildtest supports **1.0** version for all type schemas. The
``version: "1.0"`` is used to select the version of the type schema,
in this example we validate with the schema `script-v1.0.schema.json <https://buildtesters.github.io/schemas/schemas/script-v1.0.schema.json>`_.

Test Names
-----------

The **buildspecs** is an object that defines one or more test, the
test names take the following pattern ``"^[A-Za-z_][A-Za-z0-9_]*$"`` and limited
to 32 characters.

In the previous example the test name is **hello_world**. You must have unique
testname in your **buildspecs** section, otherwise you will have an invalid buildspec
file.

The ``description`` field is used to document the test and limited to 80 characters.

.. Note:: We refer to the entire YAML content as **buildspec file**, this is not to be confused with the **buildspecs** field.


You may define multiple tests in a single buildspec file, shown below is an example
using both script and compiler schema::

    version: "1.0"
    buildspecs:
      hello_f:
        type: compiler
        description: "Hello World Fortran Compilation"
        executor: local.bash
        module:
          - "module purge && module load gcc"
        build:
          source: "src/hello.f90"
          name: gnu
          fflags: -Wall

      environment_variables:
        executor: local.bash
        type: script
        env:
          FIRST_NAME: avocado
          LAST_NAME: dinosaur
        run: |
          hostname
          whoami
          echo $USER
          printf "${FIRST_NAME} ${LAST_NAME}\n"

In this example we have two tests **hello_f** and **environment_variables**. The
test ``hello_f`` is using the `compiler-v1.0.schema.json <https://buildtesters.github.io/schemas/schemas/compiler-v1.0.schema.json>`_
for validation because ``type: compiler`` is set in sub-schema while ``environment_variables`` test
is using `script-v1.0.schema.json <https://buildtesters.github.io/schemas/schemas/script-v1.0.schema.json>`_
for validation because ``type: script`` is set.


Schema Naming Convention
------------------------

All schema files use the file extension **.schema.json** to distinguish itself
as a json schema definition from an ordinary json file. All sub-schemas
must be versioned, with the exception of ``global.schema.json``.

If you have got this far you may proceed with :ref:`buildspec_overview`

Global Schema and Examples
-----------------------------

You can see view the content of ``global.schema.json`` by running::

    $ buildtest schema -n global.schema.json --json

If you want to review example buildspecs for this schema you can run::

    $ buildtest schema -n global.schema.json --example

