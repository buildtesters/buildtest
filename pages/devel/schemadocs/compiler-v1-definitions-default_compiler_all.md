# Untitled object in compiler schema version 1.0 Schema

```txt
compiler-v1.0.schema.json#/properties/compilers/properties/default/properties/all
```

Specify compiler configuration for all compiler groups. Use the `all` property if configuration is shared across compiler groups. This property can be overridden in compiler group or named compiler in `config` section.

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                            |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [compiler-v1.0.schema.json*](../out/compiler-v1.0.schema.json "open original schema") |

## all Type

`object` ([Details](compiler-v1-definitions-default_compiler_all.md))

# undefined Properties

| Property                  | Type     | Required | Nullable       | Defined by                                                                                                                                                                       |
| :------------------------ | :------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [sbatch](#sbatch)         | `array`  | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-default_compiler_all-properties-sbatch.md "compiler-v1.0.schema.json#/definitions/default_compiler_all/properties/sbatch") |
| [bsub](#bsub)             | `array`  | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-default_compiler_all-properties-bsub.md "compiler-v1.0.schema.json#/definitions/default_compiler_all/properties/bsub")     |
| [cobalt](#cobalt)         | `array`  | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-default_compiler_all-properties-cobalt.md "compiler-v1.0.schema.json#/definitions/default_compiler_all/properties/cobalt") |
| [batch](#batch)           | `object` | Optional | cannot be null | [compiler schema version 1.0](definitions-definitions-batch.md "compiler-v1.0.schema.json#/definitions/default_compiler_all/properties/batch")                                   |
| [BB](#bb)                 | `array`  | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-default_compiler_all-properties-bb.md "compiler-v1.0.schema.json#/definitions/default_compiler_all/properties/BB")         |
| [DW](#dw)                 | `array`  | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-default_compiler_all-properties-dw.md "compiler-v1.0.schema.json#/definitions/default_compiler_all/properties/DW")         |
| [env](#env)               | `object` | Optional | cannot be null | [compiler schema version 1.0](definitions-definitions-env.md "compiler-v1.0.schema.json#/definitions/default_compiler_all/properties/env")                                       |
| [vars](#vars)             | `object` | Optional | cannot be null | [compiler schema version 1.0](definitions-definitions-env.md "compiler-v1.0.schema.json#/definitions/default_compiler_all/properties/vars")                                      |
| [status](#status)         | `object` | Optional | cannot be null | [compiler schema version 1.0](definitions-definitions-status.md "compiler-v1.0.schema.json#/definitions/default_compiler_all/properties/status")                                 |
| [pre_build](#pre_build)   | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-pre_build.md "compiler-v1.0.schema.json#/definitions/default_compiler_all/properties/pre_build")                           |
| [post_build](#post_build) | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-post_build.md "compiler-v1.0.schema.json#/definitions/default_compiler_all/properties/post_build")                         |
| [pre_run](#pre_run)       | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-pre_run.md "compiler-v1.0.schema.json#/definitions/default_compiler_all/properties/pre_run")                               |
| [post_run](#post_run)     | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-post_run.md "compiler-v1.0.schema.json#/definitions/default_compiler_all/properties/post_run")                             |
| [run](#run)               | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-run.md "compiler-v1.0.schema.json#/definitions/default_compiler_all/properties/run")                                       |

## sbatch

This field is used for specifying #SBATCH options in test script. buildtest will insert #SBATCH in front of each value

`sbatch`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [compiler schema version 1.0](compiler-v1-definitions-default_compiler_all-properties-sbatch.md "compiler-v1.0.schema.json#/definitions/default_compiler_all/properties/sbatch")

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

*   defined in: [compiler schema version 1.0](compiler-v1-definitions-default_compiler_all-properties-bsub.md "compiler-v1.0.schema.json#/definitions/default_compiler_all/properties/bsub")

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

*   defined in: [compiler schema version 1.0](compiler-v1-definitions-default_compiler_all-properties-cobalt.md "compiler-v1.0.schema.json#/definitions/default_compiler_all/properties/cobalt")

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

*   defined in: [compiler schema version 1.0](definitions-definitions-batch.md "compiler-v1.0.schema.json#/definitions/default_compiler_all/properties/batch")

### batch Type

`object` ([Details](definitions-definitions-batch.md))

## BB

Create burst buffer space, this specifies #BB options in your test.

`BB`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [compiler schema version 1.0](compiler-v1-definitions-default_compiler_all-properties-bb.md "compiler-v1.0.schema.json#/definitions/default_compiler_all/properties/BB")

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

*   defined in: [compiler schema version 1.0](compiler-v1-definitions-default_compiler_all-properties-dw.md "compiler-v1.0.schema.json#/definitions/default_compiler_all/properties/DW")

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

*   defined in: [compiler schema version 1.0](definitions-definitions-env.md "compiler-v1.0.schema.json#/definitions/default_compiler_all/properties/env")

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

*   defined in: [compiler schema version 1.0](definitions-definitions-env.md "compiler-v1.0.schema.json#/definitions/default_compiler_all/properties/vars")

### vars Type

`object` ([Details](definitions-definitions-env.md))

### vars Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

## status

The status section describes how buildtest detects PASS/FAIL on test. By default returncode 0 is a PASS and anything else is a FAIL, however buildtest can support other types of PASS/FAIL conditions.

`status`

*   is optional

*   Type: `object` ([Details](definitions-definitions-status.md))

*   cannot be null

*   defined in: [compiler schema version 1.0](definitions-definitions-status.md "compiler-v1.0.schema.json#/definitions/default_compiler_all/properties/status")

### status Type

`object` ([Details](definitions-definitions-status.md))

## pre_build

Run commands before building program

`pre_build`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema version 1.0](compiler-v1-definitions-pre_build.md "compiler-v1.0.schema.json#/definitions/default_compiler_all/properties/pre_build")

### pre_build Type

`string`

## post_build

Run commands after building program

`post_build`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema version 1.0](compiler-v1-definitions-post_build.md "compiler-v1.0.schema.json#/definitions/default_compiler_all/properties/post_build")

### post_build Type

`string`

## pre_run

Run commands before running program

`pre_run`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema version 1.0](compiler-v1-definitions-pre_run.md "compiler-v1.0.schema.json#/definitions/default_compiler_all/properties/pre_run")

### pre_run Type

`string`

## post_run

Run commands after running program

`post_run`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema version 1.0](compiler-v1-definitions-post_run.md "compiler-v1.0.schema.json#/definitions/default_compiler_all/properties/post_run")

### post_run Type

`string`

## run

Run command for launching compiled binary

`run`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema version 1.0](compiler-v1-definitions-run.md "compiler-v1.0.schema.json#/definitions/default_compiler_all/properties/run")

### run Type

`string`
