.. _script_schema:

Script Schema
==============

The script schema is used for writing simple scripts (bash, sh, python) in Buildspec.
The buildtest must use ``type: script`` in order to use the script schema for validation.


Schema Files
-------------

- `Production Schema <https://raw.githubusercontent.com/buildtesters/buildtest/devel/buildtest/schemas/script-v1.0.schema.json>`_
- `Development Schema <https://buildtesters.github.io/schemas/schemas/script-v1.0.schema.json>`_

Examples
---------

The script schema examples can be retrieved via
``buildtest schema -n script-v1.0.schema.json -e``. Shown below we show valid and
invalid examples. The examples are validated with the schema ``script-v1.0.schema.json``.

.. program-output:: cat docgen/schemas/script-examples.txt

script-v1.0.schema.json
-------------------------

.. program-output:: cat docgen/schemas/script-json.txt