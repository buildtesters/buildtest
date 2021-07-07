# Buildtest Schema

This repository contains the schemas used by buildtest. 

buildtest schema docs can be found at [https://buildtesters.github.io/buildtest/](https://buildtesters.github.io/buildtest/) which can be used 
to reference the schema and assist you when you are [Writing Buildspecs](https://buildtest.readthedocs.io/en/devel/writing_buildspecs.html). Please
refer to official [buildtest documentation](https://buildtest.readthedocs.io) for help with buildtest.


Currently, we support the following schemas:

- [definitions.schema.json](https://buildtesters.github.io/buildtest/pages/devel/schemadocs/definitions.html): This schema definitions JSON definitions that are referenced by other schemas.
- [global.schema.json](https://buildtesters.github.io/buildtest/pages/devel/schemadocs/global.html): The global schema inherited by all sub-schemas
- [compiler-v1.0.schema.json](https://buildtesters.github.io/buildtest/pages/devel/schemadocs/compiler-v1.html): Compiler schema version 1.0 
- [script-v1.0.schema.json](https://buildtesters.github.io/buildtest/pages/devel/schemadocs/script-v1.html): Script schema version 1.0 
- [spack-v1.0.schema.json](https://buildtesters.github.io/buildtest/pages/devel/schemadocs/spack-v1.html): Spack schema version 1.0
- [settings.schema.json](https://buildtesters.github.io/buildtest/pages/devel/schemadocs/settings.html): This schema defines the content of buildtest settings file to configure buildtest.

The schemas are published in [schemas](https://github.com/buildtesters/buildtest/tree/gh-pages/pages/devel/schemas) folder


## What is a schema?

A [JSON-Schema](https://json-schema.org/) is used to annotate and validate JSON documents. We write schemas in JSON and validate our Buildspecs
(YAML) with one of the JSON Schemas. We make use of [python-jsonschema](https://python-jsonschema.readthedocs.io/en/stable/)
to validate a Buildspec (YAML). 

## Schema Examples

The schema examples are used for testing each schema during regression test and serve as a documentation guide. The schemas
and examples can be accessed via ``buildtest schema`` command. Shown below is a list of examples for each schema.

### Examples for global.schema.json
- [valid-examples](https://buildtesters.github.io/buildtest/pages/devel/examples/global.schema.json/valid/examples.yml)
- [invalid-examples](https://github.com/buildtesters/buildtest/tree/gh-pages/pages/devel/examples/global.schema.json/invalid)

### Examples for script-v1.0.schema.json

- [valid-examples](https://buildtesters.github.io/buildtest/pages/devel/examples/script-v1.0.schema.json/valid/examples.yml)
- [invalid-examples](https://buildtesters.github.io/buildtest/pages/devel/examples/script-v1.0.schema.json/invalid/examples.yml)

### Examples for compiler-v1.0.schema.json
- [valid-examples](https://buildtesters.github.io/buildtest/pages/devel/examples/compiler-v1.0.schema.json/valid/examples.yml)
- [invalid-examples](https://buildtesters.github.io/buildtest/pages/devel/examples/compiler-v1.0.schema.json/invalid/examples.yml)

### Examples for spack-v1.0.schema.json
- [valid-examples](https://buildtesters.github.io/buildtest/pages/devel/examples/spack-v1.0.schema.json/valid/examples.yml)
- [invalid-examples](https://buildtesters.github.io/buildtest/pages/devel/examples/spack-v1.0.schema.json/invalid/examples.yml)

### Examples for settings.schema.json
- [valid-examples](https://github.com/buildtesters/buildtest/tree/gh-pages/pages/devel/examples/settings.schema.json/valid)

 
## How are schemas defined in buildtest?

buildtest stores the schemas in top-level folder [buildtest/schemas](https://github.com/buildtesters/buildtest/tree/devel/buildtest/schemas).
The schemas [examples](https://github.com/buildtesters/buildtest/tree/devel/buildtest/schemas/examples) are grouped into directories named by
schemafile so you will see the following:

```
  $ ls -1 buildtest/schemas/examples 
  compiler-v1.0.schema.json
  global.schema.json
  script-v1.0.schema.json
  settings.schema.json
  spack-v1.0.schema.json
```

The format for sub-schema is `<name>-vX.Y.schema.json`.  All schemas must end in **.schema.json**. The schemas and documentation are published
through this [workflow](https://github.com/buildtesters/buildtest/blob/devel/.github/workflows/jsonschemadocs.yml). The pages are auto-generated and 
pushed to top-level folder [pages](https://github.com/buildtesters/buildtest/tree/gh-pages/pages). **Please do not write any files to this directory as 
your files will be removed as part of the workflow**. 
