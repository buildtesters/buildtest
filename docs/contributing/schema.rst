Contributing to Schemas
==========================

Schema Docs
------------

Schema Documentation are hosted on branch `gh-pages <https://github.com/buildtesters/buildtest/tree/gh-pages>`_
which is hosted via GitHub Pages at https://buildtesters.github.io/buildtest/.

There is an automated workflow `jsonschema2md <https://github.com/buildtesters/buildtest/blob/devel/.github/workflows/jsonschemadocs.yml>`_
which publishes schemas, documentation and examples. If you want to edit top-level page
`README.md <https://github.com/buildtesters/buildtest/blob/gh-pages/README.md>`_ please
send a pull-request to `gh-pages` branch.


Adding a new schema
----------------------

If you want to add a new schema to buildtest you need to do the following:

 1. Add schema file in `buildtest/schemas <https://github.com/buildtesters/buildtest/tree/devel/buildtest/schemas>`_ and schema file must end in **.schema.json**. If it's a sub-schema it must in format ``<name>-<version>.schema.json``. For example a schema name ``script-v2.0.schema.json`` will be sub-schema script and version 2.0.
 2. Their should be a folder that corresponds to name of schema in `examples <https://github.com/buildtesters/buildtest/tree/devel/buildtest/schemas/examples>`_ directory.
 3. There should be a list of invalid and valid examples for schema.
 4. There should be regression testfile in `schema_tests <https://github.com/buildtesters/buildtest/tree/devel/tests/schema_tests>`_ to test the schema.

Be sure to update properties and take account for:
  - a property being required or not
  - Make use of `additionalProperties: false` when defining properties so that additional keys in properties are not passed in.
  - requirements for the values provided (types, lengths, etc.)
  - If you need help, see :ref:`resources` or reach out to someone in Slack.

Running Schema Tests
---------------------

The schema tests are found in folder ``tests/schema_tests`` which has regression
test for each schema. The purpose for schema test is to ensure Buildspecs are
written according to specification outlined in schemas. Furthermore, we have edge cases
to test invalid Buildspec recipes to ensure schemas are working as expected.

To run all schema test you can run via marker::

  pytest -v -m schema


JSON Definitions
------------------

We store all JSON definitions in `defintions.schema.json <https://github.com/buildtesters/buildtest/blob/devel/buildtest/schemas/definitions.schema.json>`_ which
are fields need to be reused in other schemas. A JSON definition is defined
under ``defintions`` field, in this example we define a definition anchor **list_of_strings**
that declares an array of string::

    {
      "definitions": {
        "list_of_strings": {
          "type": "array",
          "uniqueItems": true,
          "minItems": 1,
          "items": {"type": "string"}
        },
      }
    }

A definition anchor can be referenced using **$ref** keyword. In example below we
declare a definitions **string_or_list** that uses ``$ref`` that points to
anchor ``list_of_strings``::

    "string_or_list": {
      "oneOf": [
        {"type": "string"},
        {"$ref": "#/definitions/list_of_strings"}
      ]
    },

For example the ``tags`` field is defined in **definitions.schema.json** that
references definition ``string_or_list``::

    "tags": {
      "description": "Classify tests using a tag name, this can be used for categorizing test and building tests using ``--tags`` option",
      "$ref": "#/definitions/string_or_list"
    },

The tags field is used in other schemas like **compiler.schema.json**
and **script.schema.json**. In this example we declare **tags** field and
reference tags anchor from definitions.schema.json::

    "tags": {
      "$ref": "definitions.schema.json#/definitions/tags"
    }

It's worth noting each schema must have a **$id** in order for JSON to resolve references
(``$ref``). For example the definitions schema has the following id::

    "$id": "definitions.schema.json"

It's recommended each schema has a **$schema**, **$title**, **description** field for
each schema. Currently, we support JSON Schema Draft7 so our schema field must be set to the following::

    "$schema": "http://json-schema.org/draft-07/schema#",


.. _resources:

Resources
----------

The following sites (along with the files here) can be useful to help with your development
of a schema.

 - `json-schema.org <https://json-schema.org/>`_
 - `json schema readthedocs <https://python-jsonschema.readthedocs.io/en/stable/>`_

If you have issues with writing json schema please join the `JSON-SCHEMA Slack Channel <http://json-schema.slack.com>`_