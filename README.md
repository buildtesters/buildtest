![buildtest logo](https://github.com/buildtesters/buildtest/blob/devel/logos/BuildTest_Primary_Center_4x3.png)

# Buildtest Schema

This repository contains the schemas used by buildtest. 

buildtest schema docs can be found at [https://buildtesters.github.io/buildtest/](https://buildtesters.github.io/buildtest/) which can be used 
to reference the schema and assist you when you are [writing buildspecs](https://buildtest.readthedocs.io/en/devel/buildspec_tutorial.html). Please
refer to the [buildtest documentation](https://buildtest.readthedocs.io) for help with buildtest.


Currently, we support the following schemas:

- [definitions.schema.json](https://buildtesters.github.io/buildtest/pages/schemadocs/definitions.html): This schema definitions JSON definitions that are referenced by other schemas.
- [global.schema.json](https://buildtesters.github.io/buildtest/pages/schemadocs/global.html): The global schema inherited by all sub-schemas
- [compiler.schema.json](https://buildtesters.github.io/buildtest/pages/schemadocs/compiler.html): Compiler Schema for buildspec used when specifying ``type:: compiler``
- [script.schema.json](https://buildtesters.github.io/buildtest/pages/schemadocs/script.html): Script schema for buildspec used when specifying ``type:: script``
- [spack.schema.json](https://buildtesters.github.io/buildtest/pages/schemadocs/spack.html): Spack schema for buildspec used when specifying ``type:: spack``
- [settings.schema.json](https://buildtesters.github.io/buildtest/pages/schemadocs/settings.html): This schema defines the content of buildtest settings file to configure buildtest.

The schemas are published in [schemas](https://github.com/buildtesters/buildtest/tree/gh-pages/pages/schemas) folder


## What is a schema?

A [JSON-Schema](https://json-schema.org/) is used to annotate and validate JSON documents. We write schemas in JSON and validate our Buildspecs
(YAML) with one of the JSON Schemas. We make use of [python-jsonschema](https://python-jsonschema.readthedocs.io/en/stable/)
to validate a Buildspec (YAML). 

## Schema Examples

The schema examples are used for testing each schema during regression test and serve as a documentation guide. The schemas
and examples can be accessed via ``buildtest schema`` command. Shown below is a list of examples for each schema.

### Examples for global.schema.json
- [valid-examples](https://buildtesters.github.io/buildtest/pages/examples/global.schema.json/valid/examples.yml)
- [invalid-examples](https://github.com/buildtesters/buildtest/tree/gh-pages/pages/examples/global.schema.json/invalid)

### Examples for script.schema.json

- [valid-examples](https://buildtesters.github.io/buildtest/pages/examples/script.schema.json/valid/examples.yml)
- [invalid-examples](https://buildtesters.github.io/buildtest/pages/examples/script.schema.json/invalid/examples.yml)

### Examples for compiler.schema.json
- [valid-examples](https://buildtesters.github.io/buildtest/pages/examples/compiler.schema.json/valid/examples.yml)
- [invalid-examples](https://buildtesters.github.io/buildtest/pages/examples/compiler.schema.json/invalid/examples.yml)

### Examples for spack.schema.json
- [valid-examples](https://buildtesters.github.io/buildtest/pages/examples/spack.schema.json/valid/examples.yml)
- [invalid-examples](https://buildtesters.github.io/buildtest/pages/examples/spack.schema.json/invalid/examples.yml)

### Examples for settings.schema.json
- [valid-examples](https://github.com/buildtesters/buildtest/tree/gh-pages/pages/examples/settings.schema.json/valid)

 
## How are schemas defined in buildtest?

buildtest stores the schemas in top-level folder [buildtest/schemas](https://github.com/buildtesters/buildtest/tree/devel/buildtest/schemas).
The schemas [examples](https://github.com/buildtesters/buildtest/tree/devel/buildtest/schemas/examples) are grouped into directories named by
schemafile so you will see the following:

```
  $ ls -1 buildtest/schemas/examples 
  compiler.schema.json
  global.schema.json
  script.schema.json
  settings.schema.json
  spack.schema.json
```

The format for the schemas is `<name>.schema.json` where all schemas must end in **.schema.json**. The schemas and documentation are published
through this [workflow](https://github.com/buildtesters/buildtest/blob/devel/.github/workflows/jsonschemadocs.yml). The pages are auto-generated and 
pushed to top-level folder [pages](https://github.com/buildtesters/buildtest/tree/gh-pages/pages). **Please do not write any files to this directory as your files will be removed as part of the workflow**. 
