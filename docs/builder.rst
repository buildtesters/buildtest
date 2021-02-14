.. _build_and_test_process:

Build and Test Process
======================

Pipeline
---------

buildtest will process all buildspecs that are discovered see diagram :ref:`discover_buildspecs`.
The **BuildspecParser** class is responsible for validating the buildspec. The
validation is performed using `jsonschema.validate <https://python-jsonschema.readthedocs.io/en/stable/validate/#jsonschema.validate>`_.
The parser will validate every buildspec with the global schema named `global.schema.json <https://github.com/buildtesters/buildtest/blob/gh-pages/pages/schemas/global.schema.json>`_
which validates the top-level structure.

The build pipeline is comprised of 5 stages shown below. Every buildspec goes
through this pipeline, if one stage fails, buildtest will skip the test. For instance,
a buildspec that fails ``Parse`` stage will not be built. It is possible a
buildspec passes ``Parse`` stage but fails to build because we have an :ref:`invalid_buildspecs`
for example an invalid executor name.

.. image:: _static/GeneralPipeline.jpg

.. _parse_stage:

Parse Stage
------------

A buildspec file may contain one or more test sections specified via ``buildspec``
field. Each test is validated by a sub-schema specified by ``type`` field.
buildtest will validate the buildspec with global schema first followed by sub-schema
by using the ``version`` field to look up the schema version for sub-schema. buildtest
will look up the schema from its schema library and validate the test section ``hello_world``
with schema ``script-v1.0.schema.json``.

.. image:: _static/ParserSchemaValidationDiagram.png