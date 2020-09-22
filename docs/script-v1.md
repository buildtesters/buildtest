# script schema version 1.0 Schema

```txt
https://buildtesters.github.io/buildtest/schemas/script-v1.0.schema.json
```

The script schema is of `type: script` in sub-schema which is used for running shell scripts


| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                       |
| :------------------ | ---------- | -------------- | ------------ | :---------------- | --------------------- | ------------------- | -------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [script-v1.0.schema.json](../out/script-v1.0.schema.json "open original schema") |

## script schema version 1.0 Type

`object` ([script schema version 1.0](script-v1.md))

# script schema version 1.0 Properties

| Property                    | Type          | Required | Nullable       | Defined by                                                                                                                                                               |
| :-------------------------- | ------------- | -------- | -------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [type](#type)               | `string`      | Required | cannot be null | [script schema version 1.0](script-v1-properties-type.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/script-v1.0.schema.json#/properties/type")               |
| [description](#description) | Not specified | Optional | cannot be null | [script schema version 1.0](script-v1-properties-description.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/script-v1.0.schema.json#/properties/description") |
| [sbatch](#sbatch)           | Not specified | Optional | cannot be null | [script schema version 1.0](script-v1-properties-sbatch.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/script-v1.0.schema.json#/properties/sbatch")           |
| [bsub](#bsub)               | Not specified | Optional | cannot be null | [script schema version 1.0](script-v1-properties-bsub.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/script-v1.0.schema.json#/properties/bsub")               |
| [env](#env)                 | Not specified | Optional | cannot be null | [script schema version 1.0](script-v1-properties-env.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/script-v1.0.schema.json#/properties/env")                 |
| [vars](#vars)               | Not specified | Optional | cannot be null | [script schema version 1.0](script-v1-properties-vars.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/script-v1.0.schema.json#/properties/vars")               |
| [executor](#executor)       | Not specified | Required | cannot be null | [script schema version 1.0](script-v1-properties-executor.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/script-v1.0.schema.json#/properties/executor")       |
| [shell](#shell)             | `string`      | Optional | cannot be null | [script schema version 1.0](script-v1-properties-shell.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/script-v1.0.schema.json#/properties/shell")             |
| [shebang](#shebang)         | `string`      | Optional | cannot be null | [script schema version 1.0](script-v1-properties-shebang.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/script-v1.0.schema.json#/properties/shebang")         |
| [run](#run)                 | `string`      | Required | cannot be null | [script schema version 1.0](script-v1-properties-run.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/script-v1.0.schema.json#/properties/run")                 |
| [status](#status)           | Not specified | Optional | cannot be null | [script schema version 1.0](script-v1-properties-status.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/script-v1.0.schema.json#/properties/status")           |
| [skip](#skip)               | Not specified | Optional | cannot be null | [script schema version 1.0](script-v1-properties-skip.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/script-v1.0.schema.json#/properties/skip")               |
| [tags](#tags)               | Not specified | Optional | cannot be null | [script schema version 1.0](script-v1-properties-tags.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/script-v1.0.schema.json#/properties/tags")               |

## type

Select schema type to use when validating buildspec. This must be of set to 'script'


`type`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [script schema version 1.0](script-v1-properties-type.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/script-v1.0.schema.json#/properties/type")

### type Type

`string`

### type Constraints

**pattern**: the string must match the following regular expression: 

```regexp
^script$
```

[try pattern](https://regexr.com/?expression=%5Escript%24 "try regular expression with regexr.com")

## description




`description`

-   is optional
-   Type: unknown
-   cannot be null
-   defined in: [script schema version 1.0](script-v1-properties-description.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/script-v1.0.schema.json#/properties/description")

### description Type

unknown

## sbatch




`sbatch`

-   is optional
-   Type: unknown
-   cannot be null
-   defined in: [script schema version 1.0](script-v1-properties-sbatch.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/script-v1.0.schema.json#/properties/sbatch")

### sbatch Type

unknown

## bsub




`bsub`

-   is optional
-   Type: unknown
-   cannot be null
-   defined in: [script schema version 1.0](script-v1-properties-bsub.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/script-v1.0.schema.json#/properties/bsub")

### bsub Type

unknown

## env




`env`

-   is optional
-   Type: unknown
-   cannot be null
-   defined in: [script schema version 1.0](script-v1-properties-env.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/script-v1.0.schema.json#/properties/env")

### env Type

unknown

## vars




`vars`

-   is optional
-   Type: unknown
-   cannot be null
-   defined in: [script schema version 1.0](script-v1-properties-vars.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/script-v1.0.schema.json#/properties/vars")

### vars Type

unknown

## executor




`executor`

-   is required
-   Type: unknown
-   cannot be null
-   defined in: [script schema version 1.0](script-v1-properties-executor.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/script-v1.0.schema.json#/properties/executor")

### executor Type

unknown

## shell

Specify a shell launcher to use when running jobs. This sets the shebang line in your test script. The `shell` key can be used with `run` section to describe content of script and how its executed


`shell`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [script schema version 1.0](script-v1-properties-shell.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/script-v1.0.schema.json#/properties/shell")

### shell Type

`string`

### shell Constraints

**pattern**: the string must match the following regular expression: 

```regexp
^(/bin/bash|/bin/sh|sh|bash|python).*
```

[try pattern](https://regexr.com/?expression=%5E(%2Fbin%2Fbash%7C%2Fbin%2Fsh%7Csh%7Cbash%7Cpython).* "try regular expression with regexr.com")

## shebang

Specify a custom shebang line. If not specified buildtest will automatically add it in the test script.


`shebang`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [script schema version 1.0](script-v1-properties-shebang.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/script-v1.0.schema.json#/properties/shebang")

### shebang Type

`string`

## run

A script to run using the default shell.


`run`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [script schema version 1.0](script-v1-properties-run.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/script-v1.0.schema.json#/properties/run")

### run Type

`string`

## status




`status`

-   is optional
-   Type: unknown
-   cannot be null
-   defined in: [script schema version 1.0](script-v1-properties-status.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/script-v1.0.schema.json#/properties/status")

### status Type

unknown

## skip




`skip`

-   is optional
-   Type: unknown
-   cannot be null
-   defined in: [script schema version 1.0](script-v1-properties-skip.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/script-v1.0.schema.json#/properties/skip")

### skip Type

unknown

## tags




`tags`

-   is optional
-   Type: unknown
-   cannot be null
-   defined in: [script schema version 1.0](script-v1-properties-tags.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/script-v1.0.schema.json#/properties/tags")

### tags Type

unknown
