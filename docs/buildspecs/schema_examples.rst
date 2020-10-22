Buildtest Schemas
==========================

Schema Naming Convention
------------------------

All schema files use the file extension **.schema.json** to distinguish itself
as a json schema definition from an ordinary json file. All sub-schemas
must be versioned, with the exception of ``global.schema.json``.

Schema Examples
------------------

The schema examples are great way to help write your buildspecs and
help you understand the edge cases that can lead to an invalid buildspec. The
schema examples are used in buildtest regression test for validating the schemas.
We expose the examples through buildtest client so its accessible for everyone.

In order to view an example you can run::

  buildtest schema -n <schema> --example

If you want to validate the schema examples you can run::

  buildtest schema -n <schema> --validate

You may combine ``--examples`` and ``--validate`` option if you want to view
and validate schema examples.

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
