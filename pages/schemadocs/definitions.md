# JSON Schema Definitions File.  Schema

```txt
definitions.schema.json
```

This file is used for declaring definitions that are referenced from other schemas

| Abstract               | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                       |
| :--------------------- | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------- |
| Cannot be instantiated | Yes        | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [definitions.schema.json](../out/definitions.schema.json "open original schema") |

## JSON Schema Definitions File.  Type

unknown ([JSON Schema Definitions File. ](definitions.md))

# JSON Schema Definitions File.  Definitions

## Definitions group list_of_strings

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/list_of_strings"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group string_or_list

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/string_or_list"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group list_of_ints

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/list_of_ints"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group int_or_list

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/int_or_list"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group regex

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/regex"}
```

| Property          | Type     | Required | Nullable       | Defined by                                                                                                                                          |
| :---------------- | :------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------- |
| [stream](#stream) | `string` | Required | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-regex-properties-stream.md "definitions.schema.json#/definitions/regex/properties/stream") |
| [exp](#exp)       | `string` | Required | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-regex-properties-exp.md "definitions.schema.json#/definitions/regex/properties/exp")       |

### stream

The stream field can be stdout or stderr. buildtest will read the output or error stream after completion of test and check if regex matches in stream

`stream`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-regex-properties-stream.md "definitions.schema.json#/definitions/regex/properties/stream")

#### stream Type

`string`

#### stream Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value      | Explanation |
| :--------- | :---------- |
| `"stdout"` |             |
| `"stderr"` |             |

### exp

Specify a regular expression to run with input stream specified by `stream` field. buildtest uses re.search when performing regex

`exp`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-regex-properties-exp.md "definitions.schema.json#/definitions/regex/properties/exp")

#### exp Type

`string`

## Definitions group env

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/env"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group description

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/description"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group tags

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/tags"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group skip

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/skip"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group executor

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/executor"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group metrics_field

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/metrics_field"}
```

| Property        | Type     | Required | Nullable       | Defined by                                                                                                                                                      |
| :-------------- | :------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [regex](#regex) | `object` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-regex.md "definitions.schema.json#/definitions/metrics_field/properties/regex")                        |
| [vars](#vars)   | `string` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-metrics_field-properties-vars.md "definitions.schema.json#/definitions/metrics_field/properties/vars") |
| [env](#env)     | `string` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-metrics_field-properties-env.md "definitions.schema.json#/definitions/metrics_field/properties/env")   |

### regex

Perform regular expression search using `re.search` python module on stdout/stderr stream for reporting if test `PASS`.

`regex`

*   is optional

*   Type: `object` ([Details](definitions-definitions-regex.md))

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-regex.md "definitions.schema.json#/definitions/metrics_field/properties/regex")

#### regex Type

`object` ([Details](definitions-definitions-regex.md))

### vars

Assign value to metric based on variable name

`vars`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-metrics_field-properties-vars.md "definitions.schema.json#/definitions/metrics_field/properties/vars")

#### vars Type

`string`

### env

Assign value to metric based on environment variable

`env`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-metrics_field-properties-env.md "definitions.schema.json#/definitions/metrics_field/properties/env")

#### env Type

`string`

## Definitions group metrics

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/metrics"}
```

| Property | Type     | Required | Nullable       | Defined by                                                                                                                                       |
| :------- | :------- | :------- | :------------- | :----------------------------------------------------------------------------------------------------------------------------------------------- |
| `^.*$`   | `object` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-metrics_field.md "definitions.schema.json#/definitions/metrics/patternProperties/^.*$") |

### Pattern: `^.*$`

Name of metric

`^.*$`

*   is optional

*   Type: `object` ([Details](definitions-definitions-metrics_field.md))

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-metrics_field.md "definitions.schema.json#/definitions/metrics/patternProperties/^.\*$")

#### ^.\*$ Type

`object` ([Details](definitions-definitions-metrics_field.md))

## Definitions group run_only

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/run_only"}
```

| Property                      | Type     | Required | Nullable       | Defined by                                                                                                                                                            |
| :---------------------------- | :------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [scheduler](#scheduler)       | `string` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-run_only-properties-scheduler.md "definitions.schema.json#/definitions/run_only/properties/scheduler")       |
| [user](#user)                 | `string` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-run_only-properties-user.md "definitions.schema.json#/definitions/run_only/properties/user")                 |
| [platform](#platform)         | `string` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-run_only-properties-platform.md "definitions.schema.json#/definitions/run_only/properties/platform")         |
| [linux_distro](#linux_distro) | `array`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-run_only-properties-linux_distro.md "definitions.schema.json#/definitions/run_only/properties/linux_distro") |

### scheduler

Test will run only if scheduler is available. We assume binaries are available in $PATH

`scheduler`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-run_only-properties-scheduler.md "definitions.schema.json#/definitions/run_only/properties/scheduler")

#### scheduler Type

`string`

#### scheduler Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value      | Explanation |
| :--------- | :---------- |
| `"lsf"`    |             |
| `"slurm"`  |             |
| `"cobalt"` |             |
| `"pbs"`    |             |

### user

Test will run only if current user matches this field, otherwise test will be skipped

`user`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-run_only-properties-user.md "definitions.schema.json#/definitions/run_only/properties/user")

#### user Type

`string`

### platform

This test will run if target system is Linux or Darwin. We check target system using `platform.system()` and match with input field

`platform`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-run_only-properties-platform.md "definitions.schema.json#/definitions/run_only/properties/platform")

#### platform Type

`string`

#### platform Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value      | Explanation |
| :--------- | :---------- |
| `"Linux"`  |             |
| `"Darwin"` |             |

### linux_distro

Specify a list of Linux Distros to check when processing test. If target system matches one of input field, test will be processed.

`linux_distro`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-run_only-properties-linux_distro.md "definitions.schema.json#/definitions/run_only/properties/linux_distro")

#### linux_distro Type

`string[]`

#### linux_distro Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## Definitions group status

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/status"}
```

| Property                            | Type     | Required | Nullable       | Defined by                                                                                                                                                              |
| :---------------------------------- | :------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [slurm_job_state](#slurm_job_state) | `string` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-status-properties-slurm_job_state.md "definitions.schema.json#/definitions/status/properties/slurm_job_state") |
| [returncode](#returncode)           | Merged   | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-int_or_list.md "definitions.schema.json#/definitions/status/properties/returncode")                            |
| [regex](#regex-1)                   | `object` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-regex.md "definitions.schema.json#/definitions/status/properties/regex")                                       |
| [runtime](#runtime)                 | `object` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-status-properties-runtime.md "definitions.schema.json#/definitions/status/properties/runtime")                 |
| [state](#state)                     | `string` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-status-properties-state.md "definitions.schema.json#/definitions/status/properties/state")                     |

### slurm_job_state

This field can be used for checking Slurm Job State, if there is a match buildtest will report as `PASS`

`slurm_job_state`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-status-properties-slurm_job_state.md "definitions.schema.json#/definitions/status/properties/slurm_job_state")

#### slurm_job_state Type

`string`

#### slurm_job_state Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value             | Explanation |
| :---------------- | :---------- |
| `"COMPLETED"`     |             |
| `"FAILED"`        |             |
| `"OUT_OF_MEMORY"` |             |
| `"TIMEOUT"`       |             |

### returncode

Specify a list of returncodes to match with script's exit code. buildtest will PASS test if script's exit code is found in list of returncodes. You must specify unique numbers as list and a minimum of 1 item in array

`returncode`

*   is optional

*   Type: merged type ([Details](definitions-definitions-int_or_list.md))

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-int_or_list.md "definitions.schema.json#/definitions/status/properties/returncode")

#### returncode Type

merged type ([Details](definitions-definitions-int_or_list.md))

one (and only one) of

*   [Untitled integer in JSON Schema Definitions File. ](definitions-definitions-int_or_list-oneof-0.md "check type definition")

*   [Untitled array in JSON Schema Definitions File. ](definitions-definitions-list_of_ints.md "check type definition")

### regex

Perform regular expression search using `re.search` python module on stdout/stderr stream for reporting if test `PASS`.

`regex`

*   is optional

*   Type: `object` ([Details](definitions-definitions-regex.md))

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-regex.md "definitions.schema.json#/definitions/status/properties/regex")

#### regex Type

`object` ([Details](definitions-definitions-regex.md))

### runtime

The runtime section will pass test based on min and max values and compare with actual runtime.

`runtime`

*   is optional

*   Type: `object` ([Details](definitions-definitions-status-properties-runtime.md))

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-status-properties-runtime.md "definitions.schema.json#/definitions/status/properties/runtime")

#### runtime Type

`object` ([Details](definitions-definitions-status-properties-runtime.md))

### state

explicitly mark state of test regardless of status calculation

`state`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-status-properties-state.md "definitions.schema.json#/definitions/status/properties/state")

#### state Type

`string`

#### state Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value    | Explanation |
| :------- | :---------- |
| `"PASS"` |             |
| `"FAIL"` |             |

## Definitions group BB

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/BB"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group DW

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/DW"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group sbatch

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/sbatch"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group bsub

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/bsub"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group cobalt

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/cobalt"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group pbs

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/pbs"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group executors

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/executors"}
```

| Property      | Type          | Required | Nullable       | Defined by                                                                                                                                                        |
| :------------ | :------------ | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `description` | Not specified | Optional | cannot be null | [Untitled schema](undefined.md "undefined#undefined")                                                                                                             |
| `^.*$`        | Not specified | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-executors-patternproperties-.md "definitions.schema.json#/definitions/executors/patternProperties/^.*$") |

### Pattern: `description`

no description

`description`

*   is optional

*   Type: unknown

*   cannot be null

*   defined in: [Untitled schema](undefined.md "undefined#undefined")

#### Untitled schema Type

unknown

### Pattern: `^.*$`



`^.*$`

*   is optional

*   Type: unknown

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-executors-patternproperties-.md "definitions.schema.json#/definitions/executors/patternProperties/^.\*$")

#### ^.\*$ Type

unknown
