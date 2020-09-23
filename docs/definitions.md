# JSON Schema Definitions File. This file is used for declaring definitions that are referenced from other schemas Schema

```txt
definitions.schema.json
```




| Abstract               | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                       |
| :--------------------- | ---------- | -------------- | ----------------------- | :---------------- | --------------------- | ------------------- | -------------------------------------------------------------------------------- |
| Cannot be instantiated | Yes        | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [definitions.schema.json](../out/definitions.schema.json "open original schema") |

## JSON Schema Definitions File. This file is used for declaring definitions that are referenced from other schemas Type

unknown ([JSON Schema Definitions File. This file is used for declaring definitions that are referenced from other schemas](definitions.md))

# JSON Schema Definitions File. This file is used for declaring definitions that are referenced from other schemas Definitions

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

## Definitions group status

Reference this group by using

```json
{"$ref":"definitions.schema.json#/definitions/status"}
```

| Property                            | Type     | Required | Nullable       | Defined by                                                                                                                                                                                                                                                |
| :---------------------------------- | -------- | -------- | -------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [slurm_job_state](#slurm_job_state) | `string` | Optional | cannot be null | [JSON Schema Definitions File. This file is used for declaring definitions that are referenced from other schemas](definitions-definitions-status-properties-slurm_job_state.md "definitions.schema.json#/definitions/status/properties/slurm_job_state") |
| [returncode](#returncode)           | Merged   | Optional | cannot be null | [JSON Schema Definitions File. This file is used for declaring definitions that are referenced from other schemas](definitions-definitions-int_or_list.md "definitions.schema.json#/definitions/status/properties/returncode")                            |
| [regex](#regex)                     | `object` | Optional | cannot be null | [JSON Schema Definitions File. This file is used for declaring definitions that are referenced from other schemas](definitions-definitions-status-properties-regex.md "definitions.schema.json#/definitions/status/properties/regex")                     |

### slurm_job_state

This field can be used for checking Slurm Job State, if there is a match buildtest will report as `PASS` 


`slurm_job_state`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [JSON Schema Definitions File. This file is used for declaring definitions that are referenced from other schemas](definitions-definitions-status-properties-slurm_job_state.md "definitions.schema.json#/definitions/status/properties/slurm_job_state")

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
-   defined in: [JSON Schema Definitions File. This file is used for declaring definitions that are referenced from other schemas](definitions-definitions-int_or_list.md "definitions.schema.json#/definitions/status/properties/returncode")

#### returncode Type

merged type ([Details](definitions-definitions-int_or_list.md))

one (and only one) of

-   [Untitled integer in JSON Schema Definitions File. This file is used for declaring definitions that are referenced from other schemas](definitions-definitions-int_or_list-oneof-0.md "check type definition")
-   [Untitled array in JSON Schema Definitions File. This file is used for declaring definitions that are referenced from other schemas](definitions-definitions-list_of_ints.md "check type definition")

### regex

Perform regular expression search using `re.search` python module on stdout/stderr stream for reporting if test `PASS`. 


`regex`

-   is optional
-   Type: `object` ([Details](definitions-definitions-status-properties-regex.md))
-   cannot be null
-   defined in: [JSON Schema Definitions File. This file is used for declaring definitions that are referenced from other schemas](definitions-definitions-status-properties-regex.md "definitions.schema.json#/definitions/status/properties/regex")

#### regex Type

`object` ([Details](definitions-definitions-status-properties-regex.md))
