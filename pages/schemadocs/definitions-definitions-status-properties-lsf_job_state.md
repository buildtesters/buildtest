# Untitled string in JSON Schema Definitions File.  Schema

```txt
definitions.schema.json#/definitions/status/properties/lsf_job_state
```

This field can be used to pass test based on LSF Job State, if there is a match buildtest will report as `PASS`

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                         |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [definitions.schema.json\*](../out/definitions.schema.json "open original schema") |

## lsf\_job\_state Type

`string`

## lsf\_job\_state Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value    | Explanation |
| :------- | :---------- |
| `"DONE"` |             |
| `"EXIT"` |             |
