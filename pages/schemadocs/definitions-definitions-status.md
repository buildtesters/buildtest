# Untitled object in JSON Schema Definitions File.  Schema

```txt
definitions.schema.json#/definitions/executors/patternProperties/^.*$/properties/status
```

The status section describes how buildtest detects PASS/FAIL on test. By default returncode 0 is a PASS and anything else is a FAIL, however buildtest can support other types of PASS/FAIL conditions.

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                         |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [definitions.schema.json\*](../out/definitions.schema.json "open original schema") |

## status Type

`object` ([Details](definitions-definitions-status.md))

# status Properties

| Property                              | Type     | Required | Nullable       | Defined by                                                                                                                                                              |
| :------------------------------------ | :------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [slurm\_job\_state](#slurm_job_state) | `string` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-status-properties-slurm_job_state.md "definitions.schema.json#/definitions/status/properties/slurm_job_state") |
| [pbs\_job\_state](#pbs_job_state)     | `string` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-status-properties-pbs_job_state.md "definitions.schema.json#/definitions/status/properties/pbs_job_state")     |
| [returncode](#returncode)             | Merged   | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-int_or_list.md "definitions.schema.json#/definitions/status/properties/returncode")                            |
| [regex](#regex)                       | `object` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-regex.md "definitions.schema.json#/definitions/status/properties/regex")                                       |
| [runtime](#runtime)                   | `object` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-status-properties-runtime.md "definitions.schema.json#/definitions/status/properties/runtime")                 |
| [state](#state)                       | `string` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-state.md "definitions.schema.json#/definitions/status/properties/state")                                       |

## slurm\_job\_state

This field can be used to pass test based on Slurm Job State, if there is a match buildtest will report as `PASS`

`slurm_job_state`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-status-properties-slurm_job_state.md "definitions.schema.json#/definitions/status/properties/slurm_job_state")

### slurm\_job\_state Type

`string`

### slurm\_job\_state Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value             | Explanation |
| :---------------- | :---------- |
| `"COMPLETED"`     |             |
| `"FAILED"`        |             |
| `"OUT_OF_MEMORY"` |             |
| `"TIMEOUT"`       |             |

## pbs\_job\_state

This field can be used to pass test based on PBS Job State, if there is a match buildtest will report as `PASS`

`pbs_job_state`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-status-properties-pbs_job_state.md "definitions.schema.json#/definitions/status/properties/pbs_job_state")

### pbs\_job\_state Type

`string`

### pbs\_job\_state Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value | Explanation |
| :---- | :---------- |
| `"H"` |             |
| `"S"` |             |
| `"F"` |             |

## returncode

Specify a list of returncodes to match with script's exit code. buildtest will PASS test if script's exit code is found in list of returncodes. You must specify unique numbers as list and a minimum of 1 item in array

`returncode`

*   is optional

*   Type: merged type ([Details](definitions-definitions-int_or_list.md))

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-int_or_list.md "definitions.schema.json#/definitions/status/properties/returncode")

### returncode Type

merged type ([Details](definitions-definitions-int_or_list.md))

one (and only one) of

*   [Untitled integer in JSON Schema Definitions File. ](definitions-definitions-int_or_list-oneof-0.md "check type definition")

*   [Untitled array in JSON Schema Definitions File. ](definitions-definitions-list_of_ints.md "check type definition")

## regex

Perform regular expression search using `re.search` python module on stdout/stderr stream for reporting if test `PASS`.

`regex`

*   is optional

*   Type: `object` ([Details](definitions-definitions-regex.md))

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-regex.md "definitions.schema.json#/definitions/status/properties/regex")

### regex Type

`object` ([Details](definitions-definitions-regex.md))

## runtime

The runtime section will pass test based on min and max values and compare with actual runtime.

`runtime`

*   is optional

*   Type: `object` ([Details](definitions-definitions-status-properties-runtime.md))

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-status-properties-runtime.md "definitions.schema.json#/definitions/status/properties/runtime")

### runtime Type

`object` ([Details](definitions-definitions-status-properties-runtime.md))

## state

explicitly mark state of test regardless of status calculation

`state`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-state.md "definitions.schema.json#/definitions/status/properties/state")

### state Type

`string`

### state Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value    | Explanation |
| :------- | :---------- |
| `"PASS"` |             |
| `"FAIL"` |             |
