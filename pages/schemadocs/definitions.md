# JSON Schema Definitions File.  Schema

```txt
definitions.schema.json
```

This file is used for declaring definitions that are referenced from other schemas


| Abstract               | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                       |
| :--------------------- | ---------- | -------------- | ----------------------- | :---------------- | --------------------- | ------------------- | -------------------------------------------------------------------------------- |
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
| :------- | ---- | -------- | -------- | :--------- |

## Definitions group string_or_list

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/string_or_list"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | ---- | -------- | -------- | :--------- |

## Definitions group list_of_ints

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/list_of_ints"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | ---- | -------- | -------- | :--------- |

## Definitions group int_or_list

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/int_or_list"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | ---- | -------- | -------- | :--------- |

## Definitions group env

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/env"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | ---- | -------- | -------- | :--------- |

## Definitions group description

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/description"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | ---- | -------- | -------- | :--------- |

## Definitions group tags

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/tags"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | ---- | -------- | -------- | :--------- |

## Definitions group skip

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/skip"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | ---- | -------- | -------- | :--------- |

## Definitions group executor

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/executor"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | ---- | -------- | -------- | :--------- |

## Definitions group sbatch

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/sbatch"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | ---- | -------- | -------- | :--------- |

## Definitions group bsub

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/bsub"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | ---- | -------- | -------- | :--------- |

## Definitions group batch

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/batch"}
```

| Property                | Type      | Required | Nullable       | Defined by                                                                                                                                                |
| :---------------------- | --------- | -------- | -------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [queue](#queue)         | `string`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-batch-properties-queue.md "definitions.schema.json#/definitions/batch/properties/queue")         |
| [nodecount](#nodecount) | `string`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-batch-properties-nodecount.md "definitions.schema.json#/definitions/batch/properties/nodecount") |
| [cpucount](#cpucount)   | `string`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-batch-properties-cpucount.md "definitions.schema.json#/definitions/batch/properties/cpucount")   |
| [timelimit](#timelimit) | `string`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-batch-properties-timelimit.md "definitions.schema.json#/definitions/batch/properties/timelimit") |
| [memory](#memory)       | `string`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-batch-properties-memory.md "definitions.schema.json#/definitions/batch/properties/memory")       |
| [account](#account)     | `string`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-batch-properties-account.md "definitions.schema.json#/definitions/batch/properties/account")     |
| [exclusive](#exclusive) | `boolean` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-batch-properties-exclusive.md "definitions.schema.json#/definitions/batch/properties/exclusive") |

### queue

Specify Job Queue


`queue`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [JSON Schema Definitions File. ](definitions-definitions-batch-properties-queue.md "definitions.schema.json#/definitions/batch/properties/queue")

#### queue Type

`string`

### nodecount

Specify number of Nodes to allocate


`nodecount`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [JSON Schema Definitions File. ](definitions-definitions-batch-properties-nodecount.md "definitions.schema.json#/definitions/batch/properties/nodecount")

#### nodecount Type

`string`

### cpucount

Specify number of CPU to allocate


`cpucount`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [JSON Schema Definitions File. ](definitions-definitions-batch-properties-cpucount.md "definitions.schema.json#/definitions/batch/properties/cpucount")

#### cpucount Type

`string`

### timelimit

Specify Job timelimit


`timelimit`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [JSON Schema Definitions File. ](definitions-definitions-batch-properties-timelimit.md "definitions.schema.json#/definitions/batch/properties/timelimit")

#### timelimit Type

`string`

### memory

Specify Memory Size for Job


`memory`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [JSON Schema Definitions File. ](definitions-definitions-batch-properties-memory.md "definitions.schema.json#/definitions/batch/properties/memory")

#### memory Type

`string`

### account

Specify Account to charge job


`account`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [JSON Schema Definitions File. ](definitions-definitions-batch-properties-account.md "definitions.schema.json#/definitions/batch/properties/account")

#### account Type

`string`

### exclusive

Specify if job needs to run in exclusive mode


`exclusive`

-   is optional
-   Type: `boolean`
-   cannot be null
-   defined in: [JSON Schema Definitions File. ](definitions-definitions-batch-properties-exclusive.md "definitions.schema.json#/definitions/batch/properties/exclusive")

#### exclusive Type

`boolean`

## Definitions group status

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/status"}
```

| Property                            | Type     | Required | Nullable       | Defined by                                                                                                                                                              |
| :---------------------------------- | -------- | -------- | -------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [slurm_job_state](#slurm_job_state) | `string` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-status-properties-slurm_job_state.md "definitions.schema.json#/definitions/status/properties/slurm_job_state") |
| [returncode](#returncode)           | Merged   | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-int_or_list.md "definitions.schema.json#/definitions/status/properties/returncode")                            |
| [regex](#regex)                     | `object` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-status-properties-regex.md "definitions.schema.json#/definitions/status/properties/regex")                     |

### slurm_job_state

This field can be used for checking Slurm Job State, if there is a match buildtest will report as `PASS` 


`slurm_job_state`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [JSON Schema Definitions File. ](definitions-definitions-status-properties-slurm_job_state.md "definitions.schema.json#/definitions/status/properties/slurm_job_state")

#### slurm_job_state Type

`string`

#### slurm_job_state Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value             | Explanation |
| :---------------- | ----------- |
| `"COMPLETED"`     |             |
| `"FAILED"`        |             |
| `"OUT_OF_MEMORY"` |             |
| `"TIMEOUT"`       |             |

### returncode

Specify a list of returncodes to match with script's exit code. buildtest will PASS test if script's exit code is found in list of returncodes. You must specify unique numbers as list and a minimum of 1 item in array


`returncode`

-   is optional
-   Type: merged type ([Details](definitions-definitions-int_or_list.md))
-   cannot be null
-   defined in: [JSON Schema Definitions File. ](definitions-definitions-int_or_list.md "definitions.schema.json#/definitions/status/properties/returncode")

#### returncode Type

merged type ([Details](definitions-definitions-int_or_list.md))

one (and only one) of

-   [Untitled integer in JSON Schema Definitions File. ](definitions-definitions-int_or_list-oneof-0.md "check type definition")
-   [Untitled array in JSON Schema Definitions File. ](definitions-definitions-list_of_ints.md "check type definition")

### regex

Perform regular expression search using `re.search` python module on stdout/stderr stream for reporting if test `PASS`. 


`regex`

-   is optional
-   Type: `object` ([Details](definitions-definitions-status-properties-regex.md))
-   cannot be null
-   defined in: [JSON Schema Definitions File. ](definitions-definitions-status-properties-regex.md "definitions.schema.json#/definitions/status/properties/regex")

#### regex Type

`object` ([Details](definitions-definitions-status-properties-regex.md))
