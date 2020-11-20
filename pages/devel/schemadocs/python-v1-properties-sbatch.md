# Untitled array in python schema version 1.0 Schema

```txt
https://buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/sbatch
```

This field is used for specifying #SBATCH options in test script. buildtest will insert #SBATCH in front of each value


| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                         |
| :------------------ | ---------- | -------------- | ----------------------- | :---------------- | --------------------- | ------------------- | ---------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [python-v1.0.schema.json\*](../out/python-v1.0.schema.json "open original schema") |

## sbatch Type

`string[]`

## sbatch Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.
