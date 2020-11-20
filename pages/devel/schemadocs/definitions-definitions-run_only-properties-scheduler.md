# Untitled string in JSON Schema Definitions File.  Schema

```txt
definitions.schema.json#/definitions/run_only/properties/scheduler
```

Test will run only if scheduler is available. We assume binaries are available in $PATH


| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                         |
| :------------------ | ---------- | -------------- | ----------------------- | :---------------- | --------------------- | ------------------- | ---------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [definitions.schema.json\*](../out/definitions.schema.json "open original schema") |

## scheduler Type

`string`

## scheduler Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value      | Explanation |
| :--------- | ----------- |
| `"lsf"`    |             |
| `"slurm"`  |             |
| `"cobalt"` |             |
