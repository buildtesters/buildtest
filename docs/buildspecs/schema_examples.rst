.. _schema_examples:

Buildtest Schemas
==========================

Schema Naming Convention
------------------------

All schema files use the file extension **.schema.json** to distinguish itself
as a json schema definition from an ordinary json file. The schema files are located
in `buildtest/schemas <https://github.com/buildtesters/buildtest/tree/devel/buildtest/schemas>`_
directory.

- **definitions.schema.json**: This schema is used for declaring `definitions <https://json-schema.org/understanding-json-schema/structuring.html>`_ that need to be reused in multiple schemas. We use ``$ref`` keyword to reference definitions from this file.
- **global.schema.json**: This schema is used for validating buildspec file and validates outer level structure of test. This is referred as **Global Schema**.
- **compiler-v1.0.schema.json**: This is the compiler schema used for validating test instance when ``type: compiler``. This schema is used for compiling source code with applications
- **script-v1.0.schema.json**: This is the script schema used for writing scripts (bash, csh, sh, zsh, tcsh, python) and this is used for validating test instance when ``type: script`` is specified.
- **settings.schema.json**: This schema defines how :ref:`buildtest configuration <configuring_buildtest>` file is validated.


Schema Examples
------------------

The schema examples are great way to help write your buildspecs and
help you understand the edge cases that can lead to an invalid buildspec. The
schema examples are used in buildtest regression test for validating the schemas.
We expose the examples through buildtest client so its accessible for everyone.

In order to view an example you can run::

  buildtest schema -n <schema> --example

Schema - definitions.schema.json
---------------------------------------

.. program-output:: cat docgen/schemas/definitions-json.txt

Schema - global.schema.json
-----------------------------

.. program-output:: cat docgen/schemas/global-json.txt

Schema Examples - global.schema.json
-------------------------------------

.. program-output:: cat docgen/schemas/global-examples.txt

Schema - script-v1.0.schema.json
----------------------------------

.. program-output:: cat docgen/schemas/script-json.txt

Schema Examples - script-v1.0.schema.json
------------------------------------------

.. program-output:: cat docgen/schemas/script-examples.txt


Schema - compiler-v1.0.schema.json
-----------------------------------

.. program-output:: cat docgen/schemas/compiler-json.txt


Schema Examples - compiler-v1.0.schema.json
---------------------------------------------

.. program-output:: cat docgen/schemas/compiler-examples.txt
