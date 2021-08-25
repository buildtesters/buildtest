# Untitled object in compiler schema version 1.0 Schema

```txt
compiler-v1.0.schema.json#/properties/compilers/properties/config/patternProperties/^.*$
```

Specify compiler configuration at compiler level. The `config` section has highest precedence when searching compiler configuration. This overrides fields found in compiler group and `all` property

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                            |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [compiler-v1.0.schema.json*](../out/compiler-v1.0.schema.json "open original schema") |

## ^.\*$ Type

`object` ([Details](compiler-v1-definitions-compiler_declaration.md))

# ^.\*$ Properties

| Property                  | Type     | Required | Nullable       | Defined by                                                                                                                                                                       |
| :------------------------ | :------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [cc](#cc)                 | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-cc.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/cc")                                         |
| [fc](#fc)                 | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-fc.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/fc")                                         |
| [cxx](#cxx)               | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-cxx.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/cxx")                                       |
| [cflags](#cflags)         | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-cflags.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/cflags")                                 |
| [fflags](#fflags)         | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-fflags.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/fflags")                                 |
| [cxxflags](#cxxflags)     | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-cxxflags.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/cxxflags")                             |
| [ldflags](#ldflags)       | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-ldflags.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/ldflags")                               |
| [cppflags](#cppflags)     | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-cppflags.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/cppflags")                             |
| [sbatch](#sbatch)         | `array`  | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-sbatch.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/sbatch") |
| [bsub](#bsub)             | `array`  | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-bsub.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/bsub")     |
| [cobalt](#cobalt)         | `array`  | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-cobalt.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/cobalt") |
| [pbs](#pbs)               | `array`  | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-pbs.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/pbs")       |
| [BB](#bb)                 | `array`  | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-bb.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/BB")         |
| [DW](#dw)                 | `array`  | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-dw.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/DW")         |
| [env](#env)               | `object` | Optional | cannot be null | [compiler schema version 1.0](definitions-definitions-env.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/env")                                       |
| [vars](#vars)             | `object` | Optional | cannot be null | [compiler schema version 1.0](definitions-definitions-env.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/vars")                                      |
| [status](#status)         | `object` | Optional | cannot be null | [compiler schema version 1.0](definitions-definitions-status.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/status")                                 |
| [pre_build](#pre_build)   | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-pre_build.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/pre_build")                           |
| [post_build](#post_build) | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-post_build.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/post_build")                         |
| [pre_run](#pre_run)       | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-pre_run.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/pre_run")                               |
| [post_run](#post_run)     | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-post_run.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/post_run")                             |
| [run](#run)               | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-run.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/run")                                       |
| [module](#module)         | `object` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-module.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/module") |

## cc

Set C compiler wrapper

`cc`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema version 1.0](compiler-v1-definitions-cc.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/cc")

### cc Type

`string`

## fc

Set Fortran compiler wrapper

`fc`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema version 1.0](compiler-v1-definitions-fc.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/fc")

### fc Type

`string`

## cxx

Set C++ compiler wrapper

`cxx`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema version 1.0](compiler-v1-definitions-cxx.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/cxx")

### cxx Type

`string`

## cflags

Set C compiler flags.

`cflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema version 1.0](compiler-v1-definitions-cflags.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/cflags")

### cflags Type

`string`

## fflags

Set Fortran compiler flags.

`fflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema version 1.0](compiler-v1-definitions-fflags.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/fflags")

### fflags Type

`string`

## cxxflags

Set C++ compiler flags.

`cxxflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema version 1.0](compiler-v1-definitions-cxxflags.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/cxxflags")

### cxxflags Type

`string`

## ldflags

Set linker flags

`ldflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema version 1.0](compiler-v1-definitions-ldflags.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/ldflags")

### ldflags Type

`string`

## cppflags

Set C or C++ preprocessor flags

`cppflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema version 1.0](compiler-v1-definitions-cppflags.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/cppflags")

### cppflags Type

`string`

## sbatch

This field is used for specifying #SBATCH options in test script.

`sbatch`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-sbatch.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/sbatch")

### sbatch Type

`string[]`

### sbatch Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## bsub

This field is used for specifying #BSUB options in test script.

`bsub`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-bsub.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/bsub")

### bsub Type

`string[]`

### bsub Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## cobalt

This field is used for specifying #COBALT options in test script.

`cobalt`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-cobalt.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/cobalt")

### cobalt Type

`string[]`

### cobalt Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## pbs

This field is used for specifying #PBS directives in test script.

`pbs`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-pbs.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/pbs")

### pbs Type

`string[]`

### pbs Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## BB

Create burst buffer space, this specifies #BB options in your test.

`BB`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-bb.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/BB")

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

*   defined in: [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-dw.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/DW")

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

*   defined in: [compiler schema version 1.0](definitions-definitions-env.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/env")

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

*   defined in: [compiler schema version 1.0](definitions-definitions-env.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/vars")

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

*   defined in: [compiler schema version 1.0](definitions-definitions-status.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/status")

### status Type

`object` ([Details](definitions-definitions-status.md))

## pre_build

Run commands before building program

`pre_build`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema version 1.0](compiler-v1-definitions-pre_build.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/pre_build")

### pre_build Type

`string`

## post_build

Run commands after building program

`post_build`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema version 1.0](compiler-v1-definitions-post_build.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/post_build")

### post_build Type

`string`

## pre_run

Run commands before running program

`pre_run`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema version 1.0](compiler-v1-definitions-pre_run.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/pre_run")

### pre_run Type

`string`

## post_run

Run commands after running program

`post_run`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema version 1.0](compiler-v1-definitions-post_run.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/post_run")

### post_run Type

`string`

## run

Run command for launching compiled binary

`run`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema version 1.0](compiler-v1-definitions-run.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/run")

### run Type

`string`

## module



`module`

*   is optional

*   Type: `object` ([Details](compiler-v1-definitions-compiler_declaration-properties-module.md))

*   cannot be null

*   defined in: [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-module.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/module")

### module Type

`object` ([Details](compiler-v1-definitions-compiler_declaration-properties-module.md))
