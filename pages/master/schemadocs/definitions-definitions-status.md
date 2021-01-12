# Untitled object in script schema version 1.0 Schema

```txt
script-v1.0.schema.json#/properties/status
```

The status section describes how buildtest detects PASS/FAIL on test. By default returncode 0 is a PASS and anything else is a FAIL, however buildtest can support other types of PASS/FAIL conditions.


| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                         |
| :------------------ | ---------- | -------------- | ------------ | :---------------- | --------------------- | ------------------- | ---------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [script-v1.0.schema.json\*](../out/script-v1.0.schema.json "open original schema") |

## status Type

`object` ([Details](definitions-definitions-status.md))

# undefined Properties

| Property                            | Type     | Required | Nullable       | Defined by                                                                                                                                                              |
| :---------------------------------- | -------- | -------- | -------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [slurm_job_state](#slurm_job_state) | `string` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-status-properties-slurm_job_state.md "definitions.schema.json#/definitions/status/properties/slurm_job_state") |
| [returncode](#returncode)           | Merged   | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-int_or_list.md "definitions.schema.json#/definitions/status/properties/returncode")                            |
| [regex](#regex)                     | `object` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-status-properties-regex.md "definitions.schema.json#/definitions/status/properties/regex")                     |

## slurm_job_state

This field can be used for checking Slurm Job State, if there is a match buildtest will report as `PASS` 


`slurm_job_state`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [JSON Schema Definitions File. ](definitions-definitions-status-properties-slurm_job_state.md "definitions.schema.json#/definitions/status/properties/slurm_job_state")

### slurm_job_state Type

`string`

### slurm_job_state Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value             | Explanation |
| :---------------- | ----------- |
| `"COMPLETED"`     |             |
| `"FAILED"`        |             |
| `"OUT_OF_MEMORY"` |             |
| `"TIMEOUT"`       |             |

## returncode

Specify a list of returncodes to match with script's exit code. buildtest will PASS test if script's exit code is found in list of returncodes. You must specify unique numbers as list and a minimum of 1 item in array


`returncode`

-   is optional
-   Type: merged type ([Details](definitions-definitions-int_or_list.md))
-   cannot be null
-   defined in: [JSON Schema Definitions File. ](definitions-definitions-int_or_list.md "definitions.schema.json#/definitions/status/properties/returncode")

### returncode Type

merged type ([Details](definitions-definitions-int_or_list.md))

one (and only one) of

-   [Untitled integer in JSON Schema Definitions File. ](definitions-definitions-int_or_list-oneof-0.md "check type definition")
-   [Untitled array in JSON Schema Definitions File. ](definitions-definitions-list_of_ints.md "check type definition")

## regex

Perform regular expression search using `re.search` python module on stdout/stderr stream for reporting if test `PASS`. 


`regex`

-   is optional
-   Type: `object` ([Details](definitions-definitions-status-properties-regex.md))
-   cannot be null
-   defined in: [JSON Schema Definitions File. ](definitions-definitions-status-properties-regex.md "definitions.schema.json#/definitions/status/properties/regex")

### regex Type

`object` ([Details](definitions-definitions-status-properties-regex.md))
