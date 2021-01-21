# script schema version 1.0 Schema

```txt
script-v1.0.schema.json
```

The script schema is of `type: script` in sub-schema which is used for running shell scripts

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                       |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [script-v1.0.schema.json](../out/script-v1.0.schema.json "open original schema") |

## script schema version 1.0 Type

`object` ([script schema version 1.0](script-v1.md))

# script schema version 1.0 Properties

| Property                    | Type      | Required | Nullable       | Defined by                                                                                                            |
| :-------------------------- | :-------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------- |
| [type](#type)               | `string`  | Required | cannot be null | [script schema version 1.0](script-v1-properties-type.md "script-v1.0.schema.json#/properties/type")                  |
| [description](#description) | `string`  | Optional | cannot be null | [script schema version 1.0](definitions-definitions-description.md "script-v1.0.schema.json#/properties/description") |
| [sbatch](#sbatch)           | `array`   | Optional | cannot be null | [script schema version 1.0](script-v1-properties-sbatch.md "script-v1.0.schema.json#/properties/sbatch")              |
| [bsub](#bsub)               | `array`   | Optional | cannot be null | [script schema version 1.0](script-v1-properties-bsub.md "script-v1.0.schema.json#/properties/bsub")                  |
| [cobalt](#cobalt)           | `array`   | Optional | cannot be null | [script schema version 1.0](script-v1-properties-cobalt.md "script-v1.0.schema.json#/properties/cobalt")              |
| [batch](#batch)             | `object`  | Optional | cannot be null | [script schema version 1.0](definitions-definitions-batch.md "script-v1.0.schema.json#/properties/batch")             |
| [BB](#bb)                   | `array`   | Optional | cannot be null | [script schema version 1.0](script-v1-properties-bb.md "script-v1.0.schema.json#/properties/BB")                      |
| [DW](#dw)                   | `array`   | Optional | cannot be null | [script schema version 1.0](script-v1-properties-dw.md "script-v1.0.schema.json#/properties/DW")                      |
| [env](#env)                 | `object`  | Optional | cannot be null | [script schema version 1.0](definitions-definitions-env.md "script-v1.0.schema.json#/properties/env")                 |
| [vars](#vars)               | `object`  | Optional | cannot be null | [script schema version 1.0](definitions-definitions-env.md "script-v1.0.schema.json#/properties/vars")                |
| [executor](#executor)       | `string`  | Required | cannot be null | [script schema version 1.0](definitions-definitions-executor.md "script-v1.0.schema.json#/properties/executor")       |
| [run_only](#run_only)       | `object`  | Optional | cannot be null | [script schema version 1.0](definitions-definitions-run_only.md "script-v1.0.schema.json#/properties/run_only")       |
| [shell](#shell)             | `string`  | Optional | cannot be null | [script schema version 1.0](script-v1-properties-shell.md "script-v1.0.schema.json#/properties/shell")                |
| [shebang](#shebang)         | `string`  | Optional | cannot be null | [script schema version 1.0](script-v1-properties-shebang.md "script-v1.0.schema.json#/properties/shebang")            |
| [run](#run)                 | `string`  | Required | cannot be null | [script schema version 1.0](script-v1-properties-run.md "script-v1.0.schema.json#/properties/run")                    |
| [status](#status)           | `object`  | Optional | cannot be null | [script schema version 1.0](definitions-definitions-status.md "script-v1.0.schema.json#/properties/status")           |
| [skip](#skip)               | `boolean` | Optional | cannot be null | [script schema version 1.0](definitions-definitions-skip.md "script-v1.0.schema.json#/properties/skip")               |
| [tags](#tags)               | Merged    | Optional | cannot be null | [script schema version 1.0](script-v1-properties-tags.md "script-v1.0.schema.json#/properties/tags")                  |

## type

Select schema type to use when validating buildspec. This must be of set to 'script'

`type`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [script schema version 1.0](script-v1-properties-type.md "script-v1.0.schema.json#/properties/type")

### type Type

`string`

### type Constraints

**pattern**: the string must match the following regular expression: 

```regexp
^script$
```

[try pattern](https://regexr.com/?expression=%5Escript%24 "try regular expression with regexr.com")

## description

The `description` field is used to document what the test is doing

`description`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version 1.0](definitions-definitions-description.md "script-v1.0.schema.json#/properties/description")

### description Type

`string`

### description Constraints

**maximum length**: the maximum number of characters for this string is: `80`

## sbatch

This field is used for specifying #SBATCH options in test script. buildtest will insert #SBATCH in front of each value

`sbatch`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [script schema version 1.0](script-v1-properties-sbatch.md "script-v1.0.schema.json#/properties/sbatch")

### sbatch Type

`string[]`

### sbatch Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## bsub

This field is used for specifying #BSUB options in test script. buildtest will insert #BSUB in front of each value

`bsub`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [script schema version 1.0](script-v1-properties-bsub.md "script-v1.0.schema.json#/properties/bsub")

### bsub Type

`string[]`

### bsub Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## cobalt

This field is used for specifying #COBALT options in test script. buildtest will insert #COBALT in front of each value

`cobalt`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [script schema version 1.0](script-v1-properties-cobalt.md "script-v1.0.schema.json#/properties/cobalt")

### cobalt Type

`string[]`

### cobalt Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## batch

The `batch` field is used to specify scheduler agnostic directives that are translated to #SBATCH or #BSUB based on your scheduler. This is an experimental feature that supports a subset of scheduler parameters.

`batch`

*   is optional

*   Type: `object` ([Details](definitions-definitions-batch.md))

*   cannot be null

*   defined in: [script schema version 1.0](definitions-definitions-batch.md "script-v1.0.schema.json#/properties/batch")

### batch Type

`object` ([Details](definitions-definitions-batch.md))

## BB

Create burst buffer space, this specifies #BB options in your test.

`BB`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [script schema version 1.0](script-v1-properties-bb.md "script-v1.0.schema.json#/properties/BB")

### BB Type

`string[]`

### BB Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## DW

Specify Data Warp option (#DW) when using burst buffer.

`DW`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [script schema version 1.0](script-v1-properties-dw.md "script-v1.0.schema.json#/properties/DW")

### DW Type

`string[]`

### DW Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## env

One or more key value pairs for an environment (key=value)

`env`

*   is optional

*   Type: `object` ([Details](definitions-definitions-env.md))

*   cannot be null

*   defined in: [script schema version 1.0](definitions-definitions-env.md "script-v1.0.schema.json#/properties/env")

### env Type

`object` ([Details](definitions-definitions-env.md))

### env Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

## vars

One or more key value pairs for an environment (key=value)

`vars`

*   is optional

*   Type: `object` ([Details](definitions-definitions-env.md))

*   cannot be null

*   defined in: [script schema version 1.0](definitions-definitions-env.md "script-v1.0.schema.json#/properties/vars")

### vars Type

`object` ([Details](definitions-definitions-env.md))

### vars Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

## executor

Select one of the executor name defined in your configuration file (`config.yml`). Every buildspec must have an executor which is responsible for running job.

`executor`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [script schema version 1.0](definitions-definitions-executor.md "script-v1.0.schema.json#/properties/executor")

### executor Type

`string`

## run_only

A set of conditions to specify when running tests. All conditions must pass in order to process test.

`run_only`

*   is optional

*   Type: `object` ([Details](definitions-definitions-run_only.md))

*   cannot be null

*   defined in: [script schema version 1.0](definitions-definitions-run_only.md "script-v1.0.schema.json#/properties/run_only")

### run_only Type

`object` ([Details](definitions-definitions-run_only.md))

## shell

Specify a shell launcher to use when running jobs. This sets the shebang line in your test script. The `shell` key can be used with `run` section to describe content of script and how its executed

`shell`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version 1.0](script-v1-properties-shell.md "script-v1.0.schema.json#/properties/shell")

### shell Type

`string`

### shell Constraints

**pattern**: the string must match the following regular expression: 

```regexp
^(/bin/bash|/bin/sh|/bin/csh|/bin/tcsh|/bin/zsh|bash|sh|csh|tcsh|zsh|python).*
```

[try pattern](https://regexr.com/?expression=%5E\(%2Fbin%2Fbash%7C%2Fbin%2Fsh%7C%2Fbin%2Fcsh%7C%2Fbin%2Ftcsh%7C%2Fbin%2Fzsh%7Cbash%7Csh%7Ccsh%7Ctcsh%7Czsh%7Cpython\).\* "try regular expression with regexr.com")

## shebang

Specify a custom shebang line. If not specified buildtest will automatically add it in the test script.

`shebang`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version 1.0](script-v1-properties-shebang.md "script-v1.0.schema.json#/properties/shebang")

### shebang Type

`string`

## run

A script to run using the default shell.

`run`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [script schema version 1.0](script-v1-properties-run.md "script-v1.0.schema.json#/properties/run")

### run Type

`string`

## status

The status section describes how buildtest detects PASS/FAIL on test. By default returncode 0 is a PASS and anything else is a FAIL, however buildtest can support other types of PASS/FAIL conditions.

`status`

*   is optional

*   Type: `object` ([Details](definitions-definitions-status.md))

*   cannot be null

*   defined in: [script schema version 1.0](definitions-definitions-status.md "script-v1.0.schema.json#/properties/status")

### status Type

`object` ([Details](definitions-definitions-status.md))

## skip

The `skip` is a boolean field that can be used to skip tests during builds. By default buildtest will build and run all tests in your buildspec file, if `skip: True` is set it will skip the buildspec.

`skip`

*   is optional

*   Type: `boolean`

*   cannot be null

*   defined in: [script schema version 1.0](definitions-definitions-skip.md "script-v1.0.schema.json#/properties/skip")

### skip Type

`boolean`

## tags

Classify tests using a tag name, this can be used for categorizing test and building tests using `--tags` option

`tags`

*   is optional

*   Type: merged type ([Details](script-v1-properties-tags.md))

*   cannot be null

*   defined in: [script schema version 1.0](script-v1-properties-tags.md "script-v1.0.schema.json#/properties/tags")

### tags Type

merged type ([Details](script-v1-properties-tags.md))

one (and only one) of

*   [Untitled string in JSON Schema Definitions File. ](definitions-definitions-string_or_list-oneof-0.md "check type definition")

*   [Untitled array in JSON Schema Definitions File. ](definitions-definitions-list_of_strings.md "check type definition")
