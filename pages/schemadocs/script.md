# script schema version Schema

```txt
script.schema.json
```

The script schema is of `type: script` in sub-schema which is used for running shell scripts

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                             |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------- |
| Can be instantiated | Yes        | Unknown status | No           | Forbidden         | Forbidden             | none                | [script.schema.json](../out/script.schema.json "open original schema") |

## script schema version Type

`object` ([script schema version](script.md))

# script schema version Properties

| Property                    | Type      | Required | Nullable       | Defined by                                                                                                   |
| :-------------------------- | :-------- | :------- | :------------- | :----------------------------------------------------------------------------------------------------------- |
| [type](#type)               | `string`  | Required | cannot be null | [script schema version](script-properties-type.md "script.schema.json#/properties/type")                     |
| [description](#description) | `string`  | Optional | cannot be null | [script schema version](definitions-definitions-description.md "script.schema.json#/properties/description") |
| [summary](#summary)         | `string`  | Optional | cannot be null | [script schema version](definitions-definitions-summary.md "script.schema.json#/properties/summary")         |
| [sbatch](#sbatch)           | `array`   | Optional | cannot be null | [script schema version](script-properties-sbatch.md "script.schema.json#/properties/sbatch")                 |
| [bsub](#bsub)               | `array`   | Optional | cannot be null | [script schema version](script-properties-bsub.md "script.schema.json#/properties/bsub")                     |
| [cobalt](#cobalt)           | `array`   | Optional | cannot be null | [script schema version](script-properties-cobalt.md "script.schema.json#/properties/cobalt")                 |
| [pbs](#pbs)                 | `array`   | Optional | cannot be null | [script schema version](script-properties-pbs.md "script.schema.json#/properties/pbs")                       |
| [BB](#bb)                   | `array`   | Optional | cannot be null | [script schema version](script-properties-bb.md "script.schema.json#/properties/BB")                         |
| [DW](#dw)                   | `array`   | Optional | cannot be null | [script schema version](script-properties-dw.md "script.schema.json#/properties/DW")                         |
| [env](#env)                 | `object`  | Optional | cannot be null | [script schema version](definitions-definitions-env.md "script.schema.json#/properties/env")                 |
| [vars](#vars)               | `object`  | Optional | cannot be null | [script schema version](definitions-definitions-env.md "script.schema.json#/properties/vars")                |
| [executor](#executor)       | `string`  | Required | cannot be null | [script schema version](definitions-definitions-executor.md "script.schema.json#/properties/executor")       |
| [needs](#needs)             | `array`   | Optional | cannot be null | [script schema version](definitions-definitions-needs.md "script.schema.json#/properties/needs")             |
| [shell](#shell)             | `string`  | Optional | cannot be null | [script schema version](script-properties-shell.md "script.schema.json#/properties/shell")                   |
| [shebang](#shebang)         | `string`  | Optional | cannot be null | [script schema version](script-properties-shebang.md "script.schema.json#/properties/shebang")               |
| [run](#run)                 | `string`  | Required | cannot be null | [script schema version](definitions-definitions-run.md "script.schema.json#/properties/run")                 |
| [status](#status)           | `object`  | Optional | cannot be null | [script schema version](definitions-definitions-status.md "script.schema.json#/properties/status")           |
| [skip](#skip)               | `boolean` | Optional | cannot be null | [script schema version](definitions-definitions-skip.md "script.schema.json#/properties/skip")               |
| [tags](#tags)               | Merged    | Optional | cannot be null | [script schema version](script-properties-tags.md "script.schema.json#/properties/tags")                     |
| [metrics](#metrics)         | `object`  | Optional | cannot be null | [script schema version](definitions-definitions-metrics.md "script.schema.json#/properties/metrics")         |
| [executors](#executors)     | `object`  | Optional | cannot be null | [script schema version](definitions-definitions-executors.md "script.schema.json#/properties/executors")     |
| [compilers](#compilers)     | `object`  | Optional | cannot be null | [script schema version](script-properties-compilers.md "script.schema.json#/properties/compilers")           |

## type

Select schema type to use when validating buildspec. This must be of set to 'script'

`type`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](script-properties-type.md "script.schema.json#/properties/type")

### type Type

`string`

### type Constraints

**pattern**: the string must match the following regular expression:&#x20;

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

*   defined in: [script schema version](definitions-definitions-description.md "script.schema.json#/properties/description")

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

*   defined in: [script schema version](definitions-definitions-summary.md "script.schema.json#/properties/summary")

### summary Type

`string`

## sbatch

This field is used for specifying #SBATCH options in test script.

`sbatch`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [script schema version](script-properties-sbatch.md "script.schema.json#/properties/sbatch")

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

*   defined in: [script schema version](script-properties-bsub.md "script.schema.json#/properties/bsub")

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

*   defined in: [script schema version](script-properties-cobalt.md "script.schema.json#/properties/cobalt")

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

*   defined in: [script schema version](script-properties-pbs.md "script.schema.json#/properties/pbs")

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

*   defined in: [script schema version](script-properties-bb.md "script.schema.json#/properties/BB")

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

*   defined in: [script schema version](script-properties-dw.md "script.schema.json#/properties/DW")

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

*   defined in: [script schema version](definitions-definitions-env.md "script.schema.json#/properties/env")

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

*   defined in: [script schema version](definitions-definitions-env.md "script.schema.json#/properties/vars")

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

*   defined in: [script schema version](definitions-definitions-executor.md "script.schema.json#/properties/executor")

### executor Type

`string`

## needs

A list of test names that are dependency before runnning job

`needs`

*   is optional

*   Type: an array where each item follows the corresponding schema in the following list:

    1.  [Untitled undefined type in JSON Schema Definitions File. ](definitions-definitions-needs-items-0.md "check type definition")

*   cannot be null

*   defined in: [script schema version](definitions-definitions-needs.md "script.schema.json#/properties/needs")

### needs Type

an array where each item follows the corresponding schema in the following list:

1.  [Untitled undefined type in JSON Schema Definitions File. ](definitions-definitions-needs-items-0.md "check type definition")

## shell

Specify a shell launcher to use when running jobs. This sets the shebang line in your test script. The `shell` key can be used with `run` section to describe content of script and how its executed

`shell`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](script-properties-shell.md "script.schema.json#/properties/shell")

### shell Type

`string`

## shebang

Specify a custom shebang line. If not specified buildtest will automatically add it in the test script.

`shebang`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](script-properties-shebang.md "script.schema.json#/properties/shebang")

### shebang Type

`string`

## run

Specify a series of commands to run.

`run`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-run.md "script.schema.json#/properties/run")

### run Type

`string`

## status

The status section describes how buildtest detects PASS/FAIL on test. By default returncode 0 is a PASS and anything else is a FAIL, however buildtest can support other types of PASS/FAIL conditions.

`status`

*   is optional

*   Type: `object` ([Details](definitions-definitions-status.md))

*   cannot be null

*   defined in: [script schema version](definitions-definitions-status.md "script.schema.json#/properties/status")

### status Type

`object` ([Details](definitions-definitions-status.md))

## skip

The `skip` is a boolean field that can be used to skip tests during builds. By default buildtest will build and run all tests in your buildspec file, if `skip: True` is set it will skip the buildspec.

`skip`

*   is optional

*   Type: `boolean`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-skip.md "script.schema.json#/properties/skip")

### skip Type

`boolean`

## tags

Classify tests using a tag name, this can be used for categorizing test and building tests using `--tags` option

`tags`

*   is optional

*   Type: merged type ([Details](script-properties-tags.md))

*   cannot be null

*   defined in: [script schema version](script-properties-tags.md "script.schema.json#/properties/tags")

### tags Type

merged type ([Details](script-properties-tags.md))

one (and only one) of

*   [Untitled string in JSON Schema Definitions File. ](definitions-definitions-string_or_list-oneof-0.md "check type definition")

*   [Untitled array in JSON Schema Definitions File. ](definitions-definitions-list_of_strings.md "check type definition")

## metrics

This field is used for defining one or more metrics that is recorded for each test. A metric must have a unique name which is recorded in the test metadata.

`metrics`

*   is optional

*   Type: `object` ([Details](definitions-definitions-metrics.md))

*   cannot be null

*   defined in: [script schema version](definitions-definitions-metrics.md "script.schema.json#/properties/metrics")

### metrics Type

`object` ([Details](definitions-definitions-metrics.md))

## executors

Define executor specific configuration

`executors`

*   is optional

*   Type: `object` ([Details](definitions-definitions-executors.md))

*   cannot be null

*   defined in: [script schema version](definitions-definitions-executors.md "script.schema.json#/properties/executors")

### executors Type

`object` ([Details](definitions-definitions-executors.md))

## compilers



`compilers`

*   is optional

*   Type: `object` ([Details](script-properties-compilers.md))

*   cannot be null

*   defined in: [script schema version](script-properties-compilers.md "script.schema.json#/properties/compilers")

### compilers Type

`object` ([Details](script-properties-compilers.md))

# script schema version Definitions

## Definitions group compiler\_declaration

Reference this group by using

```json
{"$ref":"script.schema.json#/definitions/compiler_declaration"}
```

| Property              | Type     | Required | Nullable       | Defined by                                                                                                                              |
| :-------------------- | :------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| [cc](#cc)             | `string` | Optional | cannot be null | [script schema version](definitions-definitions-cc.md "script.schema.json#/definitions/compiler_declaration/properties/cc")             |
| [fc](#fc)             | `string` | Optional | cannot be null | [script schema version](definitions-definitions-fc.md "script.schema.json#/definitions/compiler_declaration/properties/fc")             |
| [cxx](#cxx)           | `string` | Optional | cannot be null | [script schema version](definitions-definitions-cxx.md "script.schema.json#/definitions/compiler_declaration/properties/cxx")           |
| [cflags](#cflags)     | `string` | Optional | cannot be null | [script schema version](definitions-definitions-cflags.md "script.schema.json#/definitions/compiler_declaration/properties/cflags")     |
| [fflags](#fflags)     | `string` | Optional | cannot be null | [script schema version](definitions-definitions-fflags.md "script.schema.json#/definitions/compiler_declaration/properties/fflags")     |
| [cxxflags](#cxxflags) | `string` | Optional | cannot be null | [script schema version](definitions-definitions-cxxflags.md "script.schema.json#/definitions/compiler_declaration/properties/cxxflags") |
| [ldflags](#ldflags)   | `string` | Optional | cannot be null | [script schema version](definitions-definitions-ldflags.md "script.schema.json#/definitions/compiler_declaration/properties/ldflags")   |
| [cppflags](#cppflags) | `string` | Optional | cannot be null | [script schema version](definitions-definitions-cppflags.md "script.schema.json#/definitions/compiler_declaration/properties/cppflags") |
| [env](#env-1)         | `object` | Optional | cannot be null | [script schema version](definitions-definitions-env.md "script.schema.json#/definitions/compiler_declaration/properties/env")           |
| [vars](#vars-1)       | `object` | Optional | cannot be null | [script schema version](definitions-definitions-env.md "script.schema.json#/definitions/compiler_declaration/properties/vars")          |
| [status](#status-1)   | `object` | Optional | cannot be null | [script schema version](definitions-definitions-status.md "script.schema.json#/definitions/compiler_declaration/properties/status")     |
| [run](#run-1)         | `string` | Optional | cannot be null | [script schema version](definitions-definitions-run.md "script.schema.json#/definitions/compiler_declaration/properties/run")           |
| [module](#module)     | `object` | Optional | cannot be null | [script schema version](definitions-definitions-module.md "script.schema.json#/definitions/compiler_declaration/properties/module")     |

### cc

Set C compiler wrapper

`cc`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-cc.md "script.schema.json#/definitions/compiler_declaration/properties/cc")

#### cc Type

`string`

### fc

Set Fortran compiler wrapper

`fc`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-fc.md "script.schema.json#/definitions/compiler_declaration/properties/fc")

#### fc Type

`string`

### cxx

Set C++ compiler wrapper

`cxx`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-cxx.md "script.schema.json#/definitions/compiler_declaration/properties/cxx")

#### cxx Type

`string`

### cflags

Set C compiler flags.

`cflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-cflags.md "script.schema.json#/definitions/compiler_declaration/properties/cflags")

#### cflags Type

`string`

### fflags

Set Fortran compiler flags.

`fflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-fflags.md "script.schema.json#/definitions/compiler_declaration/properties/fflags")

#### fflags Type

`string`

### cxxflags

Set C++ compiler flags.

`cxxflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-cxxflags.md "script.schema.json#/definitions/compiler_declaration/properties/cxxflags")

#### cxxflags Type

`string`

### ldflags

Set linker flags

`ldflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-ldflags.md "script.schema.json#/definitions/compiler_declaration/properties/ldflags")

#### ldflags Type

`string`

### cppflags

Set C or C++ preprocessor flags

`cppflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-cppflags.md "script.schema.json#/definitions/compiler_declaration/properties/cppflags")

#### cppflags Type

`string`

### env

One or more key value pairs for an environment (key=value)

`env`

*   is optional

*   Type: `object` ([Details](definitions-definitions-env.md))

*   cannot be null

*   defined in: [script schema version](definitions-definitions-env.md "script.schema.json#/definitions/compiler_declaration/properties/env")

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

*   defined in: [script schema version](definitions-definitions-env.md "script.schema.json#/definitions/compiler_declaration/properties/vars")

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

*   defined in: [script schema version](definitions-definitions-status.md "script.schema.json#/definitions/compiler_declaration/properties/status")

#### status Type

`object` ([Details](definitions-definitions-status.md))

### run

Specify a series of commands to run.

`run`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-run.md "script.schema.json#/definitions/compiler_declaration/properties/run")

#### run Type

`string`

### module



`module`

*   is optional

*   Type: `object` ([Details](definitions-definitions-module.md))

*   cannot be null

*   defined in: [script schema version](definitions-definitions-module.md "script.schema.json#/definitions/compiler_declaration/properties/module")

#### module Type

`object` ([Details](definitions-definitions-module.md))

## Definitions group default\_compiler\_config

Reference this group by using

```json
{"$ref":"script.schema.json#/definitions/default_compiler_config"}
```

| Property                | Type     | Required | Nullable       | Defined by                                                                                                                                 |
| :---------------------- | :------- | :------- | :------------- | :----------------------------------------------------------------------------------------------------------------------------------------- |
| [cc](#cc-1)             | `string` | Optional | cannot be null | [script schema version](definitions-definitions-cc.md "script.schema.json#/definitions/default_compiler_config/properties/cc")             |
| [fc](#fc-1)             | `string` | Optional | cannot be null | [script schema version](definitions-definitions-fc.md "script.schema.json#/definitions/default_compiler_config/properties/fc")             |
| [cxx](#cxx-1)           | `string` | Optional | cannot be null | [script schema version](definitions-definitions-cxx.md "script.schema.json#/definitions/default_compiler_config/properties/cxx")           |
| [cflags](#cflags-1)     | `string` | Optional | cannot be null | [script schema version](definitions-definitions-cflags.md "script.schema.json#/definitions/default_compiler_config/properties/cflags")     |
| [fflags](#fflags-1)     | `string` | Optional | cannot be null | [script schema version](definitions-definitions-fflags.md "script.schema.json#/definitions/default_compiler_config/properties/fflags")     |
| [cxxflags](#cxxflags-1) | `string` | Optional | cannot be null | [script schema version](definitions-definitions-cxxflags.md "script.schema.json#/definitions/default_compiler_config/properties/cxxflags") |
| [ldflags](#ldflags-1)   | `string` | Optional | cannot be null | [script schema version](definitions-definitions-ldflags.md "script.schema.json#/definitions/default_compiler_config/properties/ldflags")   |
| [cppflags](#cppflags-1) | `string` | Optional | cannot be null | [script schema version](definitions-definitions-cppflags.md "script.schema.json#/definitions/default_compiler_config/properties/cppflags") |
| [env](#env-2)           | `object` | Optional | cannot be null | [script schema version](definitions-definitions-env.md "script.schema.json#/definitions/default_compiler_config/properties/env")           |
| [vars](#vars-2)         | `object` | Optional | cannot be null | [script schema version](definitions-definitions-env.md "script.schema.json#/definitions/default_compiler_config/properties/vars")          |
| [status](#status-2)     | `object` | Optional | cannot be null | [script schema version](definitions-definitions-status.md "script.schema.json#/definitions/default_compiler_config/properties/status")     |
| [run](#run-2)           | `string` | Optional | cannot be null | [script schema version](definitions-definitions-run.md "script.schema.json#/definitions/default_compiler_config/properties/run")           |

### cc

Set C compiler wrapper

`cc`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-cc.md "script.schema.json#/definitions/default_compiler_config/properties/cc")

#### cc Type

`string`

### fc

Set Fortran compiler wrapper

`fc`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-fc.md "script.schema.json#/definitions/default_compiler_config/properties/fc")

#### fc Type

`string`

### cxx

Set C++ compiler wrapper

`cxx`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-cxx.md "script.schema.json#/definitions/default_compiler_config/properties/cxx")

#### cxx Type

`string`

### cflags

Set C compiler flags.

`cflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-cflags.md "script.schema.json#/definitions/default_compiler_config/properties/cflags")

#### cflags Type

`string`

### fflags

Set Fortran compiler flags.

`fflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-fflags.md "script.schema.json#/definitions/default_compiler_config/properties/fflags")

#### fflags Type

`string`

### cxxflags

Set C++ compiler flags.

`cxxflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-cxxflags.md "script.schema.json#/definitions/default_compiler_config/properties/cxxflags")

#### cxxflags Type

`string`

### ldflags

Set linker flags

`ldflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-ldflags.md "script.schema.json#/definitions/default_compiler_config/properties/ldflags")

#### ldflags Type

`string`

### cppflags

Set C or C++ preprocessor flags

`cppflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-cppflags.md "script.schema.json#/definitions/default_compiler_config/properties/cppflags")

#### cppflags Type

`string`

### env

One or more key value pairs for an environment (key=value)

`env`

*   is optional

*   Type: `object` ([Details](definitions-definitions-env.md))

*   cannot be null

*   defined in: [script schema version](definitions-definitions-env.md "script.schema.json#/definitions/default_compiler_config/properties/env")

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

*   defined in: [script schema version](definitions-definitions-env.md "script.schema.json#/definitions/default_compiler_config/properties/vars")

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

*   defined in: [script schema version](definitions-definitions-status.md "script.schema.json#/definitions/default_compiler_config/properties/status")

#### status Type

`object` ([Details](definitions-definitions-status.md))

### run

Specify a series of commands to run.

`run`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-run.md "script.schema.json#/definitions/default_compiler_config/properties/run")

#### run Type

`string`
