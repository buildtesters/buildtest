.. _schema_examples:

Buildtest Schemas
==========================

buildtest uses JSON Schema for validating buildspecs and :ref:`buildtest configuration file <configuring_buildtest>`.
The json schemas are published at https://buildtesters.github.io/buildtest/ and we
provide a command line interface to view schema files and examples.

Schema Naming Convention
------------------------

All schema files use the file extension **.schema.json** to distinguish itself
as a json schema definition from an ordinary json file. The schema files are located
in `buildtest/schemas <https://github.com/buildtesters/buildtest/tree/devel/buildtest/schemas>`_
directory.

.. _buildtest_schemas:

CLI for buildtest schemas (``buildtest schema``)
-------------------------------------------------


You can use ``buildtest schema`` command to see the list of schemas
supported by buildtest. The schema files are denoted by ``.schema.json`` file extension.

.. dropdown:: ``buildtest schema``

    .. command-output:: buildtest schema

Shown below is the command usage of ``buildtest schema``

.. dropdown:: ``buildtest schema --help``

    .. command-output:: buildtest schema --help

You must use the ``--name`` option to select a schema, for instance if you want to view the JSON Schema for
**script.schema.json** you can run the following::

    buildtest schema --name script.schema.json --json

Schema Files
--------------

Definition Schema
~~~~~~~~~~~~~~~~~~

This schema is used for declaring `definitions <https://json-schema.org/understanding-json-schema/structuring.html>`_ that need to be
reused in multiple schemas. We use ``$ref`` keyword to reference definitions from this file.

.. dropdown:: definitions.schema.json

    .. literalinclude:: ../buildtest/schemas/definitions.schema.json
       :language: json

Settings Schema
~~~~~~~~~~~~~~~

This schema defines how :ref:`buildtest configuration <configuring_buildtest>` file is validated.

.. dropdown:: settings.schema.json

    .. literalinclude:: ../buildtest/schemas/settings.schema.json
       :language: json


Global Schema
~~~~~~~~~~~~~~

This schema is used for validating buildspec file and validates outer level structure of test. This is referred as :ref:`global_schema`

.. dropdown:: global.schema.json

    .. literalinclude:: ../buildtest/schemas/global.schema.json
       :language: json


Script Schema
~~~~~~~~~~~~~~

This is the script schema used for writing scripts (bash, csh, sh, zsh, tcsh, python) and this is used for validating test instance when
``type: script`` is specified. For more details on script schema see :ref:`script_schema`.

.. dropdown:: script.schema.json

    .. literalinclude:: ../buildtest/schemas/script.schema.json
       :language: json

Spack Schema
~~~~~~~~~~~~~~

This schema is used for writing tests with `spack package manager <https://spack.readthedocs.io/>`_ using ``type: spack`` field. For more details
see :ref:`buildtest_spack_integration`.

.. dropdown:: spack.schema.json

    .. literalinclude:: ../buildtest/schemas/spack.schema.json
       :language: json

Schema Examples
------------------

The schema examples are great way to help write your buildspecs and
help you understand the edge cases that can lead to an invalid buildspec. The
schema examples are used in buildtest regression test for validating the schemas.
We expose the examples through buildtest client so its accessible for everyone.

In order to view an example you can run::

  buildtest schema -n <schema> --example

Settings Schema Examples
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. dropdown:: ``buildtest schema -n settings.schema.json --example``

    .. command-output:: buildtest schema -n settings.schema.json --example

Global Schema Examples
~~~~~~~~~~~~~~~~~~~~~~~

.. dropdown:: ``buildtest schema -n global.schema.json --example``

    .. command-output:: buildtest schema -n global.schema.json --example

Script Schema Examples
~~~~~~~~~~~~~~~~~~~~~~~~

.. dropdown:: ``buildtest schema -n script.schema.json --example``

    .. command-output:: buildtest schema -n script.schema.json --example


Spack Schema Examples
~~~~~~~~~~~~~~~~~~~~~~

.. dropdown:: ``buildtest schema -n spack.schema.json --example``

    .. command-output:: buildtest schema -n spack.schema.json --example