Compiler
=========

The compiler schema is used for compiling programs with a compiler in a Buildspec
file. For more details see `Compiler Schema Documentation <https://buildtesters.github.io/schemas/compiler/>`_.


Schema Files
-------------

- `Production Schema <https://raw.githubusercontent.com/buildtesters/buildtest/devel/buildtest/buildsystem/schemas/compiler/compiler-v1.0.schema.json>`_
- `Development Schema <https://buildtesters.github.io/schemas/compiler/compiler-v1.0.schema.json>`_

compiler-v1.0.schema.json
-------------------------

.. program-output:: cat docgen/schemas/compiler-json.txt

Examples
---------

The compiler schema examples can be retrieved via ``buildtest schema -n compiler-v1.0.schema.json -e``
which shows a list of valid/invalid buildspec examples using ``type: compiler``.
Each example is validated with schema ``compiler-v1.0.schema.json`` and error
message from invalid examples are also shown in example output.

.. program-output:: cat docgen/schemas/compiler-examples.txt

