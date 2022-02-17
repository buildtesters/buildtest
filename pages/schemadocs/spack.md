# spack schema version Schema

```txt
spack.schema.json
```

The spack schema is referenced using `type: spack` which is used for generating tests using spack package manager

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                           |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------- |
| Can be instantiated | Yes        | Unknown status | No           | Forbidden         | Forbidden             | none                | [spack.schema.json](../out/spack.schema.json "open original schema") |

## spack schema version Type

`object` ([spack schema version](spack.md))

# spack schema version Properties

| Property                    | Type      | Required | Nullable       | Defined by                                                                                                 |
| :-------------------------- | :-------- | :------- | :------------- | :--------------------------------------------------------------------------------------------------------- |
| [type](#type)               | `string`  | Required | cannot be null | [spack schema version](spack-properties-type.md "spack.schema.json#/properties/type")                      |
| [description](#description) | `string`  | Optional | cannot be null | [spack schema version](definitions-definitions-description.md "spack.schema.json#/properties/description") |
| [executor](#executor)       | `string`  | Required | cannot be null | [spack schema version](definitions-definitions-executor.md "spack.schema.json#/properties/executor")       |
| [env](#env)                 | `object`  | Optional | cannot be null | [spack schema version](definitions-definitions-env.md "spack.schema.json#/properties/env")                 |
| [vars](#vars)               | `object`  | Optional | cannot be null | [spack schema version](definitions-definitions-env.md "spack.schema.json#/properties/vars")                |
| [sbatch](#sbatch)           | `array`   | Optional | cannot be null | [spack schema version](spack-properties-sbatch.md "spack.schema.json#/properties/sbatch")                  |
| [bsub](#bsub)               | `array`   | Optional | cannot be null | [spack schema version](spack-properties-bsub.md "spack.schema.json#/properties/bsub")                      |
| [cobalt](#cobalt)           | `array`   | Optional | cannot be null | [spack schema version](spack-properties-cobalt.md "spack.schema.json#/properties/cobalt")                  |
| [pbs](#pbs)                 | `array`   | Optional | cannot be null | [spack schema version](spack-properties-pbs.md "spack.schema.json#/properties/pbs")                        |
| [BB](#bb)                   | `array`   | Optional | cannot be null | [spack schema version](spack-properties-bb.md "spack.schema.json#/properties/BB")                          |
| [DW](#dw)                   | `array`   | Optional | cannot be null | [spack schema version](spack-properties-dw.md "spack.schema.json#/properties/DW")                          |
| [skip](#skip)               | `boolean` | Optional | cannot be null | [spack schema version](definitions-definitions-skip.md "spack.schema.json#/properties/skip")               |
| [tags](#tags)               | Merged    | Optional | cannot be null | [spack schema version](spack-properties-tags.md "spack.schema.json#/properties/tags")                      |
| [status](#status)           | `object`  | Optional | cannot be null | [spack schema version](definitions-definitions-status.md "spack.schema.json#/properties/status")           |
| [metrics](#metrics)         | `object`  | Optional | cannot be null | [spack schema version](definitions-definitions-metrics.md "spack.schema.json#/properties/metrics")         |
| [executors](#executors)     | `object`  | Optional | cannot be null | [spack schema version](definitions-definitions-executors.md "spack.schema.json#/properties/executors")     |
| [pre\_cmds](#pre_cmds)      | `string`  | Optional | cannot be null | [spack schema version](spack-properties-pre_cmds.md "spack.schema.json#/properties/pre_cmds")              |
| [post\_cmds](#post_cmds)    | `string`  | Optional | cannot be null | [spack schema version](spack-properties-post_cmds.md "spack.schema.json#/properties/post_cmds")            |
| [needs](#needs)             | `array`   | Optional | cannot be null | [spack schema version](spack-properties-needs.md "spack.schema.json#/properties/needs")                    |
| [spack](#spack)             | `object`  | Required | cannot be null | [spack schema version](spack-properties-spack.md "spack.schema.json#/properties/spack")                    |

## type

Select schema type to use when validating buildspec. This must be set to 'spack'

`type`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [spack schema version](spack-properties-type.md "spack.schema.json#/properties/type")

### type Type

`string`

### type Constraints

**pattern**: the string must match the following regular expression:&#x20;

```regexp
^spack$
```

[try pattern](https://regexr.com/?expression=%5Espack%24 "try regular expression with regexr.com")

## description

The `description` field is used to document what the test is doing

`description`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [spack schema version](definitions-definitions-description.md "spack.schema.json#/properties/description")

### description Type

`string`

### description Constraints

**maximum length**: the maximum number of characters for this string is: `80`

## executor

Select one of the executor name defined in your configuration file (`config.yml`). Every buildspec must have an executor which is responsible for running job.

`executor`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [spack schema version](definitions-definitions-executor.md "spack.schema.json#/properties/executor")

### executor Type

`string`

## env

One or more key value pairs for an environment (key=value)

`env`

*   is optional

*   Type: `object` ([Details](definitions-definitions-env.md))

*   cannot be null

*   defined in: [spack schema version](definitions-definitions-env.md "spack.schema.json#/properties/env")

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

*   defined in: [spack schema version](definitions-definitions-env.md "spack.schema.json#/properties/vars")

### vars Type

`object` ([Details](definitions-definitions-env.md))

### vars Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

## sbatch

This field is used for specifying #SBATCH options in test script.

`sbatch`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [spack schema version](spack-properties-sbatch.md "spack.schema.json#/properties/sbatch")

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

*   defined in: [spack schema version](spack-properties-bsub.md "spack.schema.json#/properties/bsub")

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

*   defined in: [spack schema version](spack-properties-cobalt.md "spack.schema.json#/properties/cobalt")

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

*   defined in: [spack schema version](spack-properties-pbs.md "spack.schema.json#/properties/pbs")

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

*   defined in: [spack schema version](spack-properties-bb.md "spack.schema.json#/properties/BB")

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

*   defined in: [spack schema version](spack-properties-dw.md "spack.schema.json#/properties/DW")

### DW Type

`string[]`

### DW Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## skip

The `skip` is a boolean field that can be used to skip tests during builds. By default buildtest will build and run all tests in your buildspec file, if `skip: True` is set it will skip the buildspec.

`skip`

*   is optional

*   Type: `boolean`

*   cannot be null

*   defined in: [spack schema version](definitions-definitions-skip.md "spack.schema.json#/properties/skip")

### skip Type

`boolean`

## tags

Classify tests using a tag name, this can be used for categorizing test and building tests using `--tags` option

`tags`

*   is optional

*   Type: merged type ([Details](spack-properties-tags.md))

*   cannot be null

*   defined in: [spack schema version](spack-properties-tags.md "spack.schema.json#/properties/tags")

### tags Type

merged type ([Details](spack-properties-tags.md))

one (and only one) of

*   [Untitled string in JSON Schema Definitions File. ](definitions-definitions-string_or_list-oneof-0.md "check type definition")

*   [Untitled array in JSON Schema Definitions File. ](definitions-definitions-list_of_strings.md "check type definition")

## status

The status section describes how buildtest detects PASS/FAIL on test. By default returncode 0 is a PASS and anything else is a FAIL, however buildtest can support other types of PASS/FAIL conditions.

`status`

*   is optional

*   Type: `object` ([Details](definitions-definitions-status.md))

*   cannot be null

*   defined in: [spack schema version](definitions-definitions-status.md "spack.schema.json#/properties/status")

### status Type

`object` ([Details](definitions-definitions-status.md))

## metrics

This field is used for defining one or more metrics that is recorded for each test. A metric must have a unique name which is recorded in the test metadata.

`metrics`

*   is optional

*   Type: `object` ([Details](definitions-definitions-metrics.md))

*   cannot be null

*   defined in: [spack schema version](definitions-definitions-metrics.md "spack.schema.json#/properties/metrics")

### metrics Type

`object` ([Details](definitions-definitions-metrics.md))

## executors

Define executor specific configuration

`executors`

*   is optional

*   Type: `object` ([Details](definitions-definitions-executors.md))

*   cannot be null

*   defined in: [spack schema version](definitions-definitions-executors.md "spack.schema.json#/properties/executors")

### executors Type

`object` ([Details](definitions-definitions-executors.md))

## pre\_cmds

Shell commands run before spack

`pre_cmds`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [spack schema version](spack-properties-pre_cmds.md "spack.schema.json#/properties/pre_cmds")

### pre\_cmds Type

`string`

## post\_cmds

Shell commands run after spack

`post_cmds`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [spack schema version](spack-properties-post_cmds.md "spack.schema.json#/properties/post_cmds")

### post\_cmds Type

`string`

## needs

A list of test names that are dependency before runnning job

`needs`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [spack schema version](spack-properties-needs.md "spack.schema.json#/properties/needs")

### needs Type

`string[]`

### needs Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## spack

Entry point to spack configuration

`spack`

*   is required

*   Type: `object` ([Details](spack-properties-spack.md))

*   cannot be null

*   defined in: [spack schema version](spack-properties-spack.md "spack.schema.json#/properties/spack")

### spack Type

`object` ([Details](spack-properties-spack.md))

# spack schema version Definitions

## Definitions group env

Reference this group by using

```json
{"$ref":"spack.schema.json#/definitions/env"}
```

| Property                  | Type      | Required | Nullable       | Defined by                                                                                                                        |
| :------------------------ | :-------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------- |
| [create](#create)         | `object`  | Optional | cannot be null | [spack schema version](spack-definitions-env-properties-create.md "spack.schema.json#/definitions/env/properties/create")         |
| [activate](#activate)     | `object`  | Optional | cannot be null | [spack schema version](spack-definitions-env-properties-activate.md "spack.schema.json#/definitions/env/properties/activate")     |
| [rm](#rm)                 | `object`  | Optional | cannot be null | [spack schema version](spack-definitions-env-properties-rm.md "spack.schema.json#/definitions/env/properties/rm")                 |
| [mirror](#mirror)         | `object`  | Optional | cannot be null | [spack schema version](definitions-definitions-env.md "spack.schema.json#/definitions/env/properties/mirror")                     |
| [specs](#specs)           | `array`   | Optional | cannot be null | [spack schema version](definitions-definitions-list_of_strings.md "spack.schema.json#/definitions/env/properties/specs")          |
| [concretize](#concretize) | `boolean` | Optional | cannot be null | [spack schema version](spack-definitions-env-properties-concretize.md "spack.schema.json#/definitions/env/properties/concretize") |

### create

Create a spack environment via `spack env create`

`create`

*   is optional

*   Type: `object` ([Details](spack-definitions-env-properties-create.md))

*   cannot be null

*   defined in: [spack schema version](spack-definitions-env-properties-create.md "spack.schema.json#/definitions/env/properties/create")

#### create Type

`object` ([Details](spack-definitions-env-properties-create.md))

### activate

Activate a spack environment via `spack env activate`

`activate`

*   is optional

*   Type: `object` ([Details](spack-definitions-env-properties-activate.md))

*   cannot be null

*   defined in: [spack schema version](spack-definitions-env-properties-activate.md "spack.schema.json#/definitions/env/properties/activate")

#### activate Type

`object` ([Details](spack-definitions-env-properties-activate.md))

### rm

Remove an existing spack environment via `spack env rm`.

`rm`

*   is optional

*   Type: `object` ([Details](spack-definitions-env-properties-rm.md))

*   cannot be null

*   defined in: [spack schema version](spack-definitions-env-properties-rm.md "spack.schema.json#/definitions/env/properties/rm")

#### rm Type

`object` ([Details](spack-definitions-env-properties-rm.md))

### mirror

One or more key value pairs for an environment (key=value)

`mirror`

*   is optional

*   Type: `object` ([Details](definitions-definitions-env.md))

*   cannot be null

*   defined in: [spack schema version](definitions-definitions-env.md "spack.schema.json#/definitions/env/properties/mirror")

#### mirror Type

`object` ([Details](definitions-definitions-env.md))

#### mirror Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

### specs

Add specs to environment by running `spack add <specs>`. The `specs` is a list of string which expect the argument to be name of spack package.

`specs`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [spack schema version](definitions-definitions-list_of_strings.md "spack.schema.json#/definitions/env/properties/specs")

#### specs Type

`string[]`

#### specs Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

### concretize

If `concretize: true` is set, we will concretize spack environment by running `spack concretize -f` otherwise this line will be ignored.

`concretize`

*   is optional

*   Type: `boolean`

*   cannot be null

*   defined in: [spack schema version](spack-definitions-env-properties-concretize.md "spack.schema.json#/definitions/env/properties/concretize")

#### concretize Type

`boolean`

## Definitions group install

Reference this group by using

```json
{"$ref":"spack.schema.json#/definitions/install"}
```

| Property            | Type     | Required | Nullable       | Defined by                                                                                                                          |
| :------------------ | :------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------- |
| [options](#options) | `string` | Optional | cannot be null | [spack schema version](spack-definitions-install-properties-options.md "spack.schema.json#/definitions/install/properties/options") |
| [specs](#specs-1)   | `array`  | Optional | cannot be null | [spack schema version](definitions-definitions-list_of_strings.md "spack.schema.json#/definitions/install/properties/specs")        |

### options

Pass options to `spack install` command

`options`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [spack schema version](spack-definitions-install-properties-options.md "spack.schema.json#/definitions/install/properties/options")

#### options Type

`string`

### specs

List of specs to install using `spack install` command

`specs`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [spack schema version](definitions-definitions-list_of_strings.md "spack.schema.json#/definitions/install/properties/specs")

#### specs Type

`string[]`

#### specs Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## Definitions group test

Reference this group by using

```json
{"$ref":"spack.schema.json#/definitions/test"}
```

| Property                       | Type      | Required | Nullable       | Defined by                                                                                                                              |
| :----------------------------- | :-------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| [remove\_tests](#remove_tests) | `boolean` | Optional | cannot be null | [spack schema version](spack-definitions-test-properties-remove_tests.md "spack.schema.json#/definitions/test/properties/remove_tests") |
| [run](#run)                    | `object`  | Required | cannot be null | [spack schema version](spack-definitions-test-properties-run.md "spack.schema.json#/definitions/test/properties/run")                   |
| [results](#results)            | Merged    | Required | cannot be null | [spack schema version](spack-definitions-test-properties-results.md "spack.schema.json#/definitions/test/properties/results")           |

### remove\_tests

Remove all test suites in spack before running test via `spack test run`. If set to `True` we will run `spack test remove -y` which will remove all test suites.

`remove_tests`

*   is optional

*   Type: `boolean`

*   cannot be null

*   defined in: [spack schema version](spack-definitions-test-properties-remove_tests.md "spack.schema.json#/definitions/test/properties/remove_tests")

#### remove\_tests Type

`boolean`

### run

Run tests using spack via `spack test run` command. This command requires specs are installed in your spack instance prior to running tests.

`run`

*   is required

*   Type: `object` ([Details](spack-definitions-test-properties-run.md))

*   cannot be null

*   defined in: [spack schema version](spack-definitions-test-properties-run.md "spack.schema.json#/definitions/test/properties/run")

#### run Type

`object` ([Details](spack-definitions-test-properties-run.md))

### results

View test results via `spack test results` after running tests via `spack test run`. Results can be viewed using suitename or installed specs or both.

`results`

*   is required

*   Type: `object` ([Details](spack-definitions-test-properties-results.md))

*   cannot be null

*   defined in: [spack schema version](spack-definitions-test-properties-results.md "spack.schema.json#/definitions/test/properties/results")

#### results Type

`object` ([Details](spack-definitions-test-properties-results.md))

any of

*   [Untitled undefined type in spack schema version](spack-definitions-test-properties-results-anyof-0.md "check type definition")

*   [Untitled undefined type in spack schema version](spack-definitions-test-properties-results-anyof-1.md "check type definition")

*   [Untitled undefined type in spack schema version](spack-definitions-test-properties-results-anyof-2.md "check type definition")
