# Buildtest Schema

This repository contains the schemas used by buildtest. 

buildtest schema docs can be found at https://buildtesters.github.io/buildtest/

Currently, we support the following schemas:
- [global](https://buildtesters.github.io/buildtest/docs/global.html): The global schema inherited by all sub-schemas
- [compiler-v1.0](https://buildtesters.github.io/buildtest/docs/compiler-v1.html): Compiler sub-schema version 1.0 using ``type: compiler``
- [script-v1.0](https://buildtesters.github.io/buildtest/docs/script-v1.html): Script sub-schema version 1.0 using ``type: script``
- [settings](https://buildtesters.github.io/buildtest/docs/settings.html): This schema defines the content of buildtest settings file to configure buildtest.

The schemas are published at https://github.com/buildtesters/buildtest/tree/gh-pages/schemas  
## What is a schema?

A schema defines the structure of how to write and validate a JSON file. Since,
python can load YAML and JSON files we write our Buildspecs in YAML and validate
them with a schema file that is in json. 

We make use of [python-jsonschema](https://python-jsonschema.readthedocs.io/en/stable/)
to validate a Buildspec (YAML) with one of the schema file. 
 
## Resources

The following sites (along with the files here) can be useful to help with your development
of a schema.

 - [json-schema.org](https://json-schema.org/)
 - [json schema readthedocs](https://python-jsonschema.readthedocs.io/en/stable/)
 
If you have issues with writing json schema please join the [JSON-SCHEMA Slack Channel](http://json-schema.slack.com)
 
## How are schemas defined in buildtest?

buildtest stores the schemas in top-level folder [buildtest/schemas](https://github.com/buildtesters/buildtest/tree/devel/buildtest/schemas).
The schemas [examples](https://github.com/buildtesters/buildtest/tree/devel/buildtest/schemas/examples) are grouped into directories named by
schemafile so you will see the following

```
  $ ls -1 buildtest/schemas/examples 

  compiler-v1.0.schema.json
  global.schema.json
  script-v1.0.schema.json
  settings.schema.json
```

The format for sub-schema is `<name>-vX.Y.schema.json`.  All schemas must end in **.schema.json**

For every schema including (global, script, compiler) will have a ``valid`` and ``invalid`` directory that
contains a list of valid and invalid examples for each schema. These examples are run during regression test.

The schema tests can be run as follows 

```
  $ pytest -vra tests/schema_tests
```

## How to contribute

### Adding a new schema

If you want to add a new schema to buildtest you need to do the following:
 
 1. Add schema file in [buildtest/schemas](https://github.com/buildtesters/buildtest/tree/devel/buildtest/schemas) and schema file must end in **.schema.json**. If it's a sub-schema it must in format ``<name>-<version>.schema.json``. For example a schema name ``script-v2.0.schema.json`` will be sub-schema script and version 2.0.
 2. Their should be a folder that corresponds to name of schema in [examples](https://github.com/buildtesters/buildtest/tree/devel/buildtest/schemas/examples) directory.  
 3. There should be a list of invalid and valid examples for schema. 
 4. There should be regression testfile in [schema_tests](https://github.com/buildtesters/buildtest/tree/devel/tests/schema_tests) to test the schema.
 
Be sure to update properties and take account for:
  - a property being required or not
  - Make use of `additionalProperties: false` when defining properties so that additional keys in properties are not passed in.
  - requirements for the values provided (types, lengths, etc.) 
  - If you need help, see [resources](#resources) or reach out to someone in Slack.
