.. _schema_examples:

Buildtest Schemas
==========================

Schema Naming Convention
------------------------

All schema files use the file extension **.schema.json** to distinguish itself
as a json schema definition from an ordinary json file. The schema files are located
in `buildtest/schemas <https://github.com/buildtesters/buildtest/tree/devel/buildtest/schemas>`_
directory.

Schema Examples
------------------

The schema examples are great way to help write your buildspecs and
help you understand the edge cases that can lead to an invalid buildspec. The
schema examples are used in buildtest regression test for validating the schemas.
We expose the examples through buildtest client so its accessible for everyone.

In order to view an example you can run::

  buildtest schema -n <schema> --example

Definition Schema
-------------------

This schema is used for declaring `definitions <https://json-schema.org/understanding-json-schema/structuring.html>`_ that need to be
reused in multiple schemas. We use ``$ref`` keyword to reference definitions from this file.

Schema Content
~~~~~~~~~~~~~~

.. program-output:: cat docgen/schemas/definitions_json.txt


Settings Schema
-----------------

This schema defines how :ref:`buildtest configuration <configuring_buildtest>` file is validated.

Schema Content
~~~~~~~~~~~~~~~~~

.. program-output:: cat docgen/schemas/settings_json.txt

Schema Examples
~~~~~~~~~~~~~~~~

.. program-output:: cat docgen/schemas/settings_examples.txt


Global Schema
--------------

This schema is used for validating buildspec file and validates outer level structure of test. This is referred as :ref:`global_schema`


Schema Content
~~~~~~~~~~~~~~~~~

.. program-output:: cat docgen/schemas/global_json.txt

Schema Examples
~~~~~~~~~~~~~~~~

.. program-output:: cat docgen/schemas/global_examples.txt

Script Schema
---------------

This is the script schema used for writing scripts (bash, csh, sh, zsh, tcsh, python) and this is used for validating test instance when
``type: script`` is specified. For more details on script schema see :ref:`script_schema`.

Schema Content
~~~~~~~~~~~~~~~

.. program-output:: cat docgen/schemas/script_json.txt

Schema Examples
~~~~~~~~~~~~~~~

.. program-output:: cat docgen/schemas/script_examples.txt


Compiler Schema
---------------

This is the compiler schema used for validating buildspecs that define test using ``type: compiler``.
This schema is used for compiling a single source code. For more details see :ref:`compiler_schema`

Schema Content
~~~~~~~~~~~~~~~~

.. program-output:: cat docgen/schemas/compiler_json.txt

Schema Examples
~~~~~~~~~~~~~~~~

.. program-output:: cat docgen/schemas/compiler_examples.txt

Spack Schema
-------------

This schema is used for writing tests with `spack package manager <https://spack.readthedocs.io/>`_ using ``type: spack`` field. For more details
see :ref:`spack_schema`.


Schema Content
~~~~~~~~~~~~~~~

.. program-output:: cat docgen/schemas/spack_json.txt

Schema Examples
~~~~~~~~~~~~~~~

.. program-output:: cat docgen/schemas/spack_examples.txt