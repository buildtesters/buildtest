Script Schema
==============

The script schema is used for writing simple scripts (bash, sh, python) in Buildspec,
for more details see `Script Schema Documentation <https://buildtesters.github.io/schemas/script/>`_.


Schema Files
-------------

- `Production Schema <https://raw.githubusercontent.com/buildtesters/buildtest/devel/buildtest/buildsystem/schemas/script/script-v1.0.schema.json>`_
- `Development Schema <https://buildtesters.github.io/schemas/script/script-v1.0.schema.json>`_

script-v1.0.schema.json
-------------------------

.. program-output:: cat docgen/schemas/script-json.txt

Examples
---------

The script schema examples can be retrieved via
``buildtest schema -n script-v1.0.schema.json -e``. Shown below we show valid and
invalid examples. The examples are validated with the schema ``script-v1.0.schema.json``.

.. program-output:: cat docgen/schemas/script-examples.txt