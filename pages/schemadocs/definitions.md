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

| Property        | Type     | Required | Nullable       | Defined by                                                                                                                               |
| :-------------- | :------- | :------- | :------------- | :--------------------------------------------------------------------------------------------------------------------------------------- |
| [regex](#regex) | `object` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-regex.md "definitions.schema.json#/definitions/metrics_field/properties/regex") |

### regex

Perform regular expression search using `re.search` python module on stdout/stderr stream for reporting if test `PASS`.

`regex`

*   is optional

*   Type: `object` ([Details](definitions-definitions-regex.md))

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-regex.md "definitions.schema.json#/definitions/metrics_field/properties/regex")

#### regex Type

`object` ([Details](definitions-definitions-regex.md))

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

## Definitions group cc

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/cc"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group fc

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/fc"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group cxx

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/cxx"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group cflags

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/cflags"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group fflags

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/fflags"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group cxxflags

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/cxxflags"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group ldflags

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/ldflags"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group cppflags

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/cppflags"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |

## Definitions group run

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/run"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | :--- | :------- | :------- | :--------- |
