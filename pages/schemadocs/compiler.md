# compiler schema Schema

```txt
compiler.schema.json
```

The compiler schema is of `type: compiler` in sub-schema which is used for compiling and running programs

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                 |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------- |
| Can be instantiated | Yes        | Unknown status | No           | Forbidden         | Forbidden             | none                | [compiler.schema.json](../out/compiler.schema.json "open original schema") |

## compiler schema Type

`object` ([compiler schema](compiler.md))

# compiler schema Properties

| Property                    | Type      | Required | Nullable       | Defined by                                                                                           |
| :-------------------------- | :-------- | :------- | :------------- | :--------------------------------------------------------------------------------------------------- |
| [type](#type)               | `string`  | Required | cannot be null | [compiler schema](compiler-properties-type.md "compiler.schema.json#/properties/type")               |
| [description](#description) | `string`  | Optional | cannot be null | [compiler schema](compiler-properties-description.md "compiler.schema.json#/properties/description") |
| [summary](#summary)         | `string`  | Optional | cannot be null | [compiler schema](compiler-properties-summary.md "compiler.schema.json#/properties/summary")         |
| [needs](#needs)             | `array`   | Optional | cannot be null | [compiler schema](definitions-definitions-needs.md "compiler.schema.json#/properties/needs")         |
| [compilers](#compilers)     | `object`  | Required | cannot be null | [compiler schema](compiler-properties-compilers.md "compiler.schema.json#/properties/compilers")     |
| [source](#source)           | `string`  | Required | cannot be null | [compiler schema](compiler-properties-source.md "compiler.schema.json#/properties/source")           |
| [executor](#executor)       | `string`  | Required | cannot be null | [compiler schema](compiler-properties-executor.md "compiler.schema.json#/properties/executor")       |
| [skip](#skip)               | `boolean` | Optional | cannot be null | [compiler schema](compiler-properties-skip.md "compiler.schema.json#/properties/skip")               |
| [tags](#tags)               | Merged    | Optional | cannot be null | [compiler schema](compiler-properties-tags.md "compiler.schema.json#/properties/tags")               |
| [metrics](#metrics)         | `object`  | Optional | cannot be null | [compiler schema](definitions-definitions-metrics.md "compiler.schema.json#/properties/metrics")     |

## type

Select schema type to use when validating buildspec. This must be of set to `compiler`.

`type`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-properties-type.md "compiler.schema.json#/properties/type")

### type Type

`string`

### type Constraints

**pattern**: the string must match the following regular expression:&#x20;

```regexp
^compiler$
```

[try pattern](https://regexr.com/?expression=%5Ecompiler%24 "try regular expression with regexr.com")

## description

The `description` field is used to document what the test is doing

`description`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-properties-description.md "compiler.schema.json#/properties/description")

### description Type

`string`

### description Constraints

**maximum length**: the maximum number of characters for this string is: `80`

## summary

The `summary` field is used to document what the test is doing and can be a multi-line string

`summary`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-properties-summary.md "compiler.schema.json#/properties/summary")

### summary Type

`string`

## needs

A list of test names that are dependency before runnning job

`needs`

*   is optional

*   Type: an array where each item follows the corresponding schema in the following list:

    1.  [Untitled undefined type in JSON Schema Definitions File. ](definitions-definitions-needs-items-0.md "check type definition")

*   cannot be null

*   defined in: [compiler schema](definitions-definitions-needs.md "compiler.schema.json#/properties/needs")

### needs Type

an array where each item follows the corresponding schema in the following list:

1.  [Untitled undefined type in JSON Schema Definitions File. ](definitions-definitions-needs-items-0.md "check type definition")

## compilers



`compilers`

*   is required

*   Type: `object` ([Details](compiler-properties-compilers.md))

*   cannot be null

*   defined in: [compiler schema](compiler-properties-compilers.md "compiler.schema.json#/properties/compilers")

### compilers Type

`object` ([Details](compiler-properties-compilers.md))

## source

Specify a source file for compilation, the file can be relative path to buildspec or an absolute path

`source`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-properties-source.md "compiler.schema.json#/properties/source")

### source Type

`string`

## executor

Select one of the executor name defined in your configuration file (`config.yml`). Every buildspec must have an executor which is responsible for running job.

`executor`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-properties-executor.md "compiler.schema.json#/properties/executor")

### executor Type

`string`

## skip

The `skip` is a boolean field that can be used to skip tests during builds. By default buildtest will build and run all tests in your buildspec file, if `skip: True` is set it will skip the buildspec.

`skip`

*   is optional

*   Type: `boolean`

*   cannot be null

*   defined in: [compiler schema](compiler-properties-skip.md "compiler.schema.json#/properties/skip")

### skip Type

`boolean`

## tags

Classify tests using a tag name, this can be used for categorizing test and building tests using `--tags` option

`tags`

*   is optional

*   Type: merged type ([Details](compiler-properties-tags.md))

*   cannot be null

*   defined in: [compiler schema](compiler-properties-tags.md "compiler.schema.json#/properties/tags")

### tags Type

merged type ([Details](compiler-properties-tags.md))

one (and only one) of

*   [Untitled string in JSON Schema Definitions File. ](definitions-definitions-string_or_list-oneof-0.md "check type definition")

*   [Untitled array in JSON Schema Definitions File. ](definitions-definitions-list_of_strings.md "check type definition")

## metrics

This field is used for defining one or more metrics that is recorded for each test. A metric must have a unique name which is recorded in the test metadata.

`metrics`

*   is optional

*   Type: `object` ([Details](definitions-definitions-metrics.md))

*   cannot be null

*   defined in: [compiler schema](definitions-definitions-metrics.md "compiler.schema.json#/properties/metrics")

### metrics Type

`object` ([Details](definitions-definitions-metrics.md))

# compiler schema Definitions

## Definitions group cc

Reference this group by using

```json
{"$ref":"compiler.schema.json#/definitions/cc"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group fc

Reference this group by using

```json
{"$ref":"compiler.schema.json#/definitions/fc"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group cxx

Reference this group by using

```json
{"$ref":"compiler.schema.json#/definitions/cxx"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group cflags

Reference this group by using

```json
{"$ref":"compiler.schema.json#/definitions/cflags"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group fflags

Reference this group by using

```json
{"$ref":"compiler.schema.json#/definitions/fflags"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group cxxflags

Reference this group by using

```json
{"$ref":"compiler.schema.json#/definitions/cxxflags"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group ldflags

Reference this group by using

```json
{"$ref":"compiler.schema.json#/definitions/ldflags"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group cppflags

Reference this group by using

```json
{"$ref":"compiler.schema.json#/definitions/cppflags"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group pre\_build

Reference this group by using

```json
{"$ref":"compiler.schema.json#/definitions/pre_build"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group post\_build

Reference this group by using

```json
{"$ref":"compiler.schema.json#/definitions/post_build"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group pre\_run

Reference this group by using

```json
{"$ref":"compiler.schema.json#/definitions/pre_run"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group post\_run

Reference this group by using

```json
{"$ref":"compiler.schema.json#/definitions/post_run"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group run

Reference this group by using

```json
{"$ref":"compiler.schema.json#/definitions/run"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group default\_compiler\_all

Reference this group by using

```json
{"$ref":"compiler.schema.json#/definitions/default_compiler_all"}
```

| Property                   | Type     | Required | Nullable       | Defined by                                                                                                                                                           |
| :------------------------- | :------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [sbatch](#sbatch)          | `array`  | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_all-properties-sbatch.md "compiler.schema.json#/definitions/default_compiler_all/properties/sbatch")         |
| [bsub](#bsub)              | `array`  | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_all-properties-bsub.md "compiler.schema.json#/definitions/default_compiler_all/properties/bsub")             |
| [cobalt](#cobalt)          | `array`  | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_all-properties-cobalt.md "compiler.schema.json#/definitions/default_compiler_all/properties/cobalt")         |
| [pbs](#pbs)                | `array`  | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_all-properties-pbs.md "compiler.schema.json#/definitions/default_compiler_all/properties/pbs")               |
| [BB](#bb)                  | `array`  | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_all-properties-bb.md "compiler.schema.json#/definitions/default_compiler_all/properties/BB")                 |
| [DW](#dw)                  | `array`  | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_all-properties-dw.md "compiler.schema.json#/definitions/default_compiler_all/properties/DW")                 |
| [env](#env)                | `object` | Optional | cannot be null | [compiler schema](definitions-definitions-env.md "compiler.schema.json#/definitions/default_compiler_all/properties/env")                                            |
| [vars](#vars)              | `object` | Optional | cannot be null | [compiler schema](definitions-definitions-env.md "compiler.schema.json#/definitions/default_compiler_all/properties/vars")                                           |
| [status](#status)          | `object` | Optional | cannot be null | [compiler schema](definitions-definitions-status.md "compiler.schema.json#/definitions/default_compiler_all/properties/status")                                      |
| [pre\_build](#pre_build)   | `string` | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_all-properties-pre_build.md "compiler.schema.json#/definitions/default_compiler_all/properties/pre_build")   |
| [post\_build](#post_build) | `string` | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_all-properties-post_build.md "compiler.schema.json#/definitions/default_compiler_all/properties/post_build") |
| [pre\_run](#pre_run)       | `string` | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_all-properties-pre_run.md "compiler.schema.json#/definitions/default_compiler_all/properties/pre_run")       |
| [post\_run](#post_run)     | `string` | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_all-properties-post_run.md "compiler.schema.json#/definitions/default_compiler_all/properties/post_run")     |
| [run](#run)                | `string` | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_all-properties-run.md "compiler.schema.json#/definitions/default_compiler_all/properties/run")               |

### sbatch

This field is used for specifying #SBATCH options in test script.

`sbatch`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_all-properties-sbatch.md "compiler.schema.json#/definitions/default_compiler_all/properties/sbatch")

#### sbatch Type

`string[]`

#### sbatch Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

### bsub

This field is used for specifying #BSUB options in test script.

`bsub`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_all-properties-bsub.md "compiler.schema.json#/definitions/default_compiler_all/properties/bsub")

#### bsub Type

`string[]`

#### bsub Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

### cobalt

This field is used for specifying #COBALT options in test script.

`cobalt`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_all-properties-cobalt.md "compiler.schema.json#/definitions/default_compiler_all/properties/cobalt")

#### cobalt Type

`string[]`

#### cobalt Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

### pbs

This field is used for specifying #PBS directives in test script.

`pbs`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_all-properties-pbs.md "compiler.schema.json#/definitions/default_compiler_all/properties/pbs")

#### pbs Type

`string[]`

#### pbs Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

### BB

Create burst buffer space, this specifies #BB options in your test.

`BB`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_all-properties-bb.md "compiler.schema.json#/definitions/default_compiler_all/properties/BB")

#### BB Type

`string[]`

#### BB Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

### DW

Specify Data Warp option (#DW) when using burst buffer.

`DW`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_all-properties-dw.md "compiler.schema.json#/definitions/default_compiler_all/properties/DW")

#### DW Type

`string[]`

#### DW Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

### env

One or more key value pairs for an environment (key=value)

`env`

*   is optional

*   Type: `object` ([Details](definitions-definitions-env.md))

*   cannot be null

*   defined in: [compiler schema](definitions-definitions-env.md "compiler.schema.json#/definitions/default_compiler_all/properties/env")

#### env Type

`object` ([Details](definitions-definitions-env.md))

#### env Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

### vars

One or more key value pairs for an environment (key=value)

`vars`

*   is optional

*   Type: `object` ([Details](definitions-definitions-env.md))

*   cannot be null

*   defined in: [compiler schema](definitions-definitions-env.md "compiler.schema.json#/definitions/default_compiler_all/properties/vars")

#### vars Type

`object` ([Details](definitions-definitions-env.md))

#### vars Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

### status

The status section describes how buildtest detects PASS/FAIL on test. By default returncode 0 is a PASS and anything else is a FAIL, however buildtest can support other types of PASS/FAIL conditions.

`status`

*   is optional

*   Type: `object` ([Details](definitions-definitions-status.md))

*   cannot be null

*   defined in: [compiler schema](definitions-definitions-status.md "compiler.schema.json#/definitions/default_compiler_all/properties/status")

#### status Type

`object` ([Details](definitions-definitions-status.md))

### pre\_build

Run commands before building program

`pre_build`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_all-properties-pre_build.md "compiler.schema.json#/definitions/default_compiler_all/properties/pre_build")

#### pre\_build Type

`string`

### post\_build

Run commands after building program

`post_build`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_all-properties-post_build.md "compiler.schema.json#/definitions/default_compiler_all/properties/post_build")

#### post\_build Type

`string`

### pre\_run

Run commands before running program

`pre_run`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_all-properties-pre_run.md "compiler.schema.json#/definitions/default_compiler_all/properties/pre_run")

#### pre\_run Type

`string`

### post\_run

Run commands after running program

`post_run`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_all-properties-post_run.md "compiler.schema.json#/definitions/default_compiler_all/properties/post_run")

#### post\_run Type

`string`

### run

Run command for launching compiled binary

`run`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_all-properties-run.md "compiler.schema.json#/definitions/default_compiler_all/properties/run")

#### run Type

`string`

## Definitions group default\_compiler\_config

Reference this group by using

```json
{"$ref":"compiler.schema.json#/definitions/default_compiler_config"}
```

| Property                     | Type     | Required | Nullable       | Defined by                                                                                                                                                                 |
| :--------------------------- | :------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [cc](#cc)                    | `string` | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_config-properties-cc.md "compiler.schema.json#/definitions/default_compiler_config/properties/cc")                 |
| [fc](#fc)                    | `string` | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_config-properties-fc.md "compiler.schema.json#/definitions/default_compiler_config/properties/fc")                 |
| [cxx](#cxx)                  | `string` | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_config-properties-cxx.md "compiler.schema.json#/definitions/default_compiler_config/properties/cxx")               |
| [cflags](#cflags)            | `string` | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_config-properties-cflags.md "compiler.schema.json#/definitions/default_compiler_config/properties/cflags")         |
| [fflags](#fflags)            | `string` | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_config-properties-fflags.md "compiler.schema.json#/definitions/default_compiler_config/properties/fflags")         |
| [cxxflags](#cxxflags)        | `string` | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_config-properties-cxxflags.md "compiler.schema.json#/definitions/default_compiler_config/properties/cxxflags")     |
| [ldflags](#ldflags)          | `string` | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_config-properties-ldflags.md "compiler.schema.json#/definitions/default_compiler_config/properties/ldflags")       |
| [cppflags](#cppflags)        | `string` | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_config-properties-cppflags.md "compiler.schema.json#/definitions/default_compiler_config/properties/cppflags")     |
| [sbatch](#sbatch-1)          | `array`  | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_config-properties-sbatch.md "compiler.schema.json#/definitions/default_compiler_config/properties/sbatch")         |
| [bsub](#bsub-1)              | `array`  | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_config-properties-bsub.md "compiler.schema.json#/definitions/default_compiler_config/properties/bsub")             |
| [cobalt](#cobalt-1)          | `array`  | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_config-properties-cobalt.md "compiler.schema.json#/definitions/default_compiler_config/properties/cobalt")         |
| [pbs](#pbs-1)                | `array`  | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_config-properties-pbs.md "compiler.schema.json#/definitions/default_compiler_config/properties/pbs")               |
| [BB](#bb-1)                  | `array`  | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_config-properties-bb.md "compiler.schema.json#/definitions/default_compiler_config/properties/BB")                 |
| [DW](#dw-1)                  | `array`  | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_config-properties-dw.md "compiler.schema.json#/definitions/default_compiler_config/properties/DW")                 |
| [env](#env-1)                | `object` | Optional | cannot be null | [compiler schema](definitions-definitions-env.md "compiler.schema.json#/definitions/default_compiler_config/properties/env")                                               |
| [vars](#vars-1)              | `object` | Optional | cannot be null | [compiler schema](definitions-definitions-env.md "compiler.schema.json#/definitions/default_compiler_config/properties/vars")                                              |
| [status](#status-1)          | `object` | Optional | cannot be null | [compiler schema](definitions-definitions-status.md "compiler.schema.json#/definitions/default_compiler_config/properties/status")                                         |
| [pre\_build](#pre_build-1)   | `string` | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_config-properties-pre_build.md "compiler.schema.json#/definitions/default_compiler_config/properties/pre_build")   |
| [post\_build](#post_build-1) | `string` | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_config-properties-post_build.md "compiler.schema.json#/definitions/default_compiler_config/properties/post_build") |
| [pre\_run](#pre_run-1)       | `string` | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_config-properties-pre_run.md "compiler.schema.json#/definitions/default_compiler_config/properties/pre_run")       |
| [post\_run](#post_run-1)     | `string` | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_config-properties-post_run.md "compiler.schema.json#/definitions/default_compiler_config/properties/post_run")     |
| [run](#run-1)                | `string` | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_config-properties-run.md "compiler.schema.json#/definitions/default_compiler_config/properties/run")               |

### cc

Set C compiler wrapper

`cc`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_config-properties-cc.md "compiler.schema.json#/definitions/default_compiler_config/properties/cc")

#### cc Type

`string`

### fc

Set Fortran compiler wrapper

`fc`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_config-properties-fc.md "compiler.schema.json#/definitions/default_compiler_config/properties/fc")

#### fc Type

`string`

### cxx

Set C++ compiler wrapper

`cxx`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_config-properties-cxx.md "compiler.schema.json#/definitions/default_compiler_config/properties/cxx")

#### cxx Type

`string`

### cflags

Set C compiler flags.

`cflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_config-properties-cflags.md "compiler.schema.json#/definitions/default_compiler_config/properties/cflags")

#### cflags Type

`string`

### fflags

Set Fortran compiler flags.

`fflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_config-properties-fflags.md "compiler.schema.json#/definitions/default_compiler_config/properties/fflags")

#### fflags Type

`string`

### cxxflags

Set C++ compiler flags.

`cxxflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_config-properties-cxxflags.md "compiler.schema.json#/definitions/default_compiler_config/properties/cxxflags")

#### cxxflags Type

`string`

### ldflags

Set linker flags

`ldflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_config-properties-ldflags.md "compiler.schema.json#/definitions/default_compiler_config/properties/ldflags")

#### ldflags Type

`string`

### cppflags

Set C or C++ preprocessor flags

`cppflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_config-properties-cppflags.md "compiler.schema.json#/definitions/default_compiler_config/properties/cppflags")

#### cppflags Type

`string`

### sbatch

This field is used for specifying #SBATCH options in test script.

`sbatch`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_config-properties-sbatch.md "compiler.schema.json#/definitions/default_compiler_config/properties/sbatch")

#### sbatch Type

`string[]`

#### sbatch Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

### bsub

This field is used for specifying #BSUB options in test script.

`bsub`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_config-properties-bsub.md "compiler.schema.json#/definitions/default_compiler_config/properties/bsub")

#### bsub Type

`string[]`

#### bsub Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

### cobalt

This field is used for specifying #COBALT options in test script.

`cobalt`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_config-properties-cobalt.md "compiler.schema.json#/definitions/default_compiler_config/properties/cobalt")

#### cobalt Type

`string[]`

#### cobalt Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

### pbs

This field is used for specifying #PBS directives in test script.

`pbs`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_config-properties-pbs.md "compiler.schema.json#/definitions/default_compiler_config/properties/pbs")

#### pbs Type

`string[]`

#### pbs Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

### BB

Create burst buffer space, this specifies #BB options in your test.

`BB`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_config-properties-bb.md "compiler.schema.json#/definitions/default_compiler_config/properties/BB")

#### BB Type

`string[]`

#### BB Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

### DW

Specify Data Warp option (#DW) when using burst buffer.

`DW`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_config-properties-dw.md "compiler.schema.json#/definitions/default_compiler_config/properties/DW")

#### DW Type

`string[]`

#### DW Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

### env

One or more key value pairs for an environment (key=value)

`env`

*   is optional

*   Type: `object` ([Details](definitions-definitions-env.md))

*   cannot be null

*   defined in: [compiler schema](definitions-definitions-env.md "compiler.schema.json#/definitions/default_compiler_config/properties/env")

#### env Type

`object` ([Details](definitions-definitions-env.md))

#### env Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

### vars

One or more key value pairs for an environment (key=value)

`vars`

*   is optional

*   Type: `object` ([Details](definitions-definitions-env.md))

*   cannot be null

*   defined in: [compiler schema](definitions-definitions-env.md "compiler.schema.json#/definitions/default_compiler_config/properties/vars")

#### vars Type

`object` ([Details](definitions-definitions-env.md))

#### vars Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

### status

The status section describes how buildtest detects PASS/FAIL on test. By default returncode 0 is a PASS and anything else is a FAIL, however buildtest can support other types of PASS/FAIL conditions.

`status`

*   is optional

*   Type: `object` ([Details](definitions-definitions-status.md))

*   cannot be null

*   defined in: [compiler schema](definitions-definitions-status.md "compiler.schema.json#/definitions/default_compiler_config/properties/status")

#### status Type

`object` ([Details](definitions-definitions-status.md))

### pre\_build

Run commands before building program

`pre_build`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_config-properties-pre_build.md "compiler.schema.json#/definitions/default_compiler_config/properties/pre_build")

#### pre\_build Type

`string`

### post\_build

Run commands after building program

`post_build`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_config-properties-post_build.md "compiler.schema.json#/definitions/default_compiler_config/properties/post_build")

#### post\_build Type

`string`

### pre\_run

Run commands before running program

`pre_run`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_config-properties-pre_run.md "compiler.schema.json#/definitions/default_compiler_config/properties/pre_run")

#### pre\_run Type

`string`

### post\_run

Run commands after running program

`post_run`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_config-properties-post_run.md "compiler.schema.json#/definitions/default_compiler_config/properties/post_run")

#### post\_run Type

`string`

### run

Run command for launching compiled binary

`run`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_config-properties-run.md "compiler.schema.json#/definitions/default_compiler_config/properties/run")

#### run Type

`string`

## Definitions group compiler\_declaration

Reference this group by using

```json
{"$ref":"compiler.schema.json#/definitions/compiler_declaration"}
```

| Property                     | Type     | Required | Nullable       | Defined by                                                                                                                                                           |
| :--------------------------- | :------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [cc](#cc-1)                  | `string` | Optional | cannot be null | [compiler schema](compiler-definitions-compiler_declaration-properties-cc.md "compiler.schema.json#/definitions/compiler_declaration/properties/cc")                 |
| [fc](#fc-1)                  | `string` | Optional | cannot be null | [compiler schema](compiler-definitions-compiler_declaration-properties-fc.md "compiler.schema.json#/definitions/compiler_declaration/properties/fc")                 |
| [cxx](#cxx-1)                | `string` | Optional | cannot be null | [compiler schema](compiler-definitions-compiler_declaration-properties-cxx.md "compiler.schema.json#/definitions/compiler_declaration/properties/cxx")               |
| [cflags](#cflags-1)          | `string` | Optional | cannot be null | [compiler schema](compiler-definitions-compiler_declaration-properties-cflags.md "compiler.schema.json#/definitions/compiler_declaration/properties/cflags")         |
| [fflags](#fflags-1)          | `string` | Optional | cannot be null | [compiler schema](compiler-definitions-compiler_declaration-properties-fflags.md "compiler.schema.json#/definitions/compiler_declaration/properties/fflags")         |
| [cxxflags](#cxxflags-1)      | `string` | Optional | cannot be null | [compiler schema](compiler-definitions-compiler_declaration-properties-cxxflags.md "compiler.schema.json#/definitions/compiler_declaration/properties/cxxflags")     |
| [ldflags](#ldflags-1)        | `string` | Optional | cannot be null | [compiler schema](compiler-definitions-compiler_declaration-properties-ldflags.md "compiler.schema.json#/definitions/compiler_declaration/properties/ldflags")       |
| [cppflags](#cppflags-1)      | `string` | Optional | cannot be null | [compiler schema](compiler-definitions-compiler_declaration-properties-cppflags.md "compiler.schema.json#/definitions/compiler_declaration/properties/cppflags")     |
| [sbatch](#sbatch-2)          | `array`  | Optional | cannot be null | [compiler schema](compiler-definitions-compiler_declaration-properties-sbatch.md "compiler.schema.json#/definitions/compiler_declaration/properties/sbatch")         |
| [bsub](#bsub-2)              | `array`  | Optional | cannot be null | [compiler schema](compiler-definitions-compiler_declaration-properties-bsub.md "compiler.schema.json#/definitions/compiler_declaration/properties/bsub")             |
| [cobalt](#cobalt-2)          | `array`  | Optional | cannot be null | [compiler schema](compiler-definitions-compiler_declaration-properties-cobalt.md "compiler.schema.json#/definitions/compiler_declaration/properties/cobalt")         |
| [pbs](#pbs-2)                | `array`  | Optional | cannot be null | [compiler schema](compiler-definitions-compiler_declaration-properties-pbs.md "compiler.schema.json#/definitions/compiler_declaration/properties/pbs")               |
| [BB](#bb-2)                  | `array`  | Optional | cannot be null | [compiler schema](compiler-definitions-compiler_declaration-properties-bb.md "compiler.schema.json#/definitions/compiler_declaration/properties/BB")                 |
| [DW](#dw-2)                  | `array`  | Optional | cannot be null | [compiler schema](compiler-definitions-compiler_declaration-properties-dw.md "compiler.schema.json#/definitions/compiler_declaration/properties/DW")                 |
| [env](#env-2)                | `object` | Optional | cannot be null | [compiler schema](definitions-definitions-env.md "compiler.schema.json#/definitions/compiler_declaration/properties/env")                                            |
| [vars](#vars-2)              | `object` | Optional | cannot be null | [compiler schema](definitions-definitions-env.md "compiler.schema.json#/definitions/compiler_declaration/properties/vars")                                           |
| [status](#status-2)          | `object` | Optional | cannot be null | [compiler schema](definitions-definitions-status.md "compiler.schema.json#/definitions/compiler_declaration/properties/status")                                      |
| [pre\_build](#pre_build-2)   | `string` | Optional | cannot be null | [compiler schema](compiler-definitions-compiler_declaration-properties-pre_build.md "compiler.schema.json#/definitions/compiler_declaration/properties/pre_build")   |
| [post\_build](#post_build-2) | `string` | Optional | cannot be null | [compiler schema](compiler-definitions-compiler_declaration-properties-post_build.md "compiler.schema.json#/definitions/compiler_declaration/properties/post_build") |
| [pre\_run](#pre_run-2)       | `string` | Optional | cannot be null | [compiler schema](compiler-definitions-compiler_declaration-properties-pre_run.md "compiler.schema.json#/definitions/compiler_declaration/properties/pre_run")       |
| [post\_run](#post_run-2)     | `string` | Optional | cannot be null | [compiler schema](compiler-definitions-compiler_declaration-properties-post_run.md "compiler.schema.json#/definitions/compiler_declaration/properties/post_run")     |
| [run](#run-2)                | `string` | Optional | cannot be null | [compiler schema](compiler-definitions-compiler_declaration-properties-run.md "compiler.schema.json#/definitions/compiler_declaration/properties/run")               |
| [module](#module)            | `object` | Optional | cannot be null | [compiler schema](definitions-definitions-module.md "compiler.schema.json#/definitions/compiler_declaration/properties/module")                                      |

### cc

Set C compiler wrapper

`cc`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-compiler_declaration-properties-cc.md "compiler.schema.json#/definitions/compiler_declaration/properties/cc")

#### cc Type

`string`

### fc

Set Fortran compiler wrapper

`fc`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-compiler_declaration-properties-fc.md "compiler.schema.json#/definitions/compiler_declaration/properties/fc")

#### fc Type

`string`

### cxx

Set C++ compiler wrapper

`cxx`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-compiler_declaration-properties-cxx.md "compiler.schema.json#/definitions/compiler_declaration/properties/cxx")

#### cxx Type

`string`

### cflags

Set C compiler flags.

`cflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-compiler_declaration-properties-cflags.md "compiler.schema.json#/definitions/compiler_declaration/properties/cflags")

#### cflags Type

`string`

### fflags

Set Fortran compiler flags.

`fflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-compiler_declaration-properties-fflags.md "compiler.schema.json#/definitions/compiler_declaration/properties/fflags")

#### fflags Type

`string`

### cxxflags

Set C++ compiler flags.

`cxxflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-compiler_declaration-properties-cxxflags.md "compiler.schema.json#/definitions/compiler_declaration/properties/cxxflags")

#### cxxflags Type

`string`

### ldflags

Set linker flags

`ldflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-compiler_declaration-properties-ldflags.md "compiler.schema.json#/definitions/compiler_declaration/properties/ldflags")

#### ldflags Type

`string`

### cppflags

Set C or C++ preprocessor flags

`cppflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-compiler_declaration-properties-cppflags.md "compiler.schema.json#/definitions/compiler_declaration/properties/cppflags")

#### cppflags Type

`string`

### sbatch

This field is used for specifying #SBATCH options in test script.

`sbatch`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-compiler_declaration-properties-sbatch.md "compiler.schema.json#/definitions/compiler_declaration/properties/sbatch")

#### sbatch Type

`string[]`

#### sbatch Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

### bsub

This field is used for specifying #BSUB options in test script.

`bsub`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-compiler_declaration-properties-bsub.md "compiler.schema.json#/definitions/compiler_declaration/properties/bsub")

#### bsub Type

`string[]`

#### bsub Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

### cobalt

This field is used for specifying #COBALT options in test script.

`cobalt`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-compiler_declaration-properties-cobalt.md "compiler.schema.json#/definitions/compiler_declaration/properties/cobalt")

#### cobalt Type

`string[]`

#### cobalt Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

### pbs

This field is used for specifying #PBS directives in test script.

`pbs`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-compiler_declaration-properties-pbs.md "compiler.schema.json#/definitions/compiler_declaration/properties/pbs")

#### pbs Type

`string[]`

#### pbs Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

### BB

Create burst buffer space, this specifies #BB options in your test.

`BB`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-compiler_declaration-properties-bb.md "compiler.schema.json#/definitions/compiler_declaration/properties/BB")

#### BB Type

`string[]`

#### BB Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

### DW

Specify Data Warp option (#DW) when using burst buffer.

`DW`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-compiler_declaration-properties-dw.md "compiler.schema.json#/definitions/compiler_declaration/properties/DW")

#### DW Type

`string[]`

#### DW Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

### env

One or more key value pairs for an environment (key=value)

`env`

*   is optional

*   Type: `object` ([Details](definitions-definitions-env.md))

*   cannot be null

*   defined in: [compiler schema](definitions-definitions-env.md "compiler.schema.json#/definitions/compiler_declaration/properties/env")

#### env Type

`object` ([Details](definitions-definitions-env.md))

#### env Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

### vars

One or more key value pairs for an environment (key=value)

`vars`

*   is optional

*   Type: `object` ([Details](definitions-definitions-env.md))

*   cannot be null

*   defined in: [compiler schema](definitions-definitions-env.md "compiler.schema.json#/definitions/compiler_declaration/properties/vars")

#### vars Type

`object` ([Details](definitions-definitions-env.md))

#### vars Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

### status

The status section describes how buildtest detects PASS/FAIL on test. By default returncode 0 is a PASS and anything else is a FAIL, however buildtest can support other types of PASS/FAIL conditions.

`status`

*   is optional

*   Type: `object` ([Details](definitions-definitions-status.md))

*   cannot be null

*   defined in: [compiler schema](definitions-definitions-status.md "compiler.schema.json#/definitions/compiler_declaration/properties/status")

#### status Type

`object` ([Details](definitions-definitions-status.md))

### pre\_build

Run commands before building program

`pre_build`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-compiler_declaration-properties-pre_build.md "compiler.schema.json#/definitions/compiler_declaration/properties/pre_build")

#### pre\_build Type

`string`

### post\_build

Run commands after building program

`post_build`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-compiler_declaration-properties-post_build.md "compiler.schema.json#/definitions/compiler_declaration/properties/post_build")

#### post\_build Type

`string`

### pre\_run

Run commands before running program

`pre_run`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-compiler_declaration-properties-pre_run.md "compiler.schema.json#/definitions/compiler_declaration/properties/pre_run")

#### pre\_run Type

`string`

### post\_run

Run commands after running program

`post_run`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-compiler_declaration-properties-post_run.md "compiler.schema.json#/definitions/compiler_declaration/properties/post_run")

#### post\_run Type

`string`

### run

Run command for launching compiled binary

`run`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-compiler_declaration-properties-run.md "compiler.schema.json#/definitions/compiler_declaration/properties/run")

#### run Type

`string`

### module



`module`

*   is optional

*   Type: `object` ([Details](definitions-definitions-module.md))

*   cannot be null

*   defined in: [compiler schema](definitions-definitions-module.md "compiler.schema.json#/definitions/compiler_declaration/properties/module")

#### module Type

`object` ([Details](definitions-definitions-module.md))
