# Untitled array in JSON Schema Definitions File. This file is used for declaring definitions that are referenced from other schemas Schema

```txt
https://buildtesters.github.io/buildtest/schemas/_definitions.schema.json#/definitions/status/properties/returncode
```

Specify a list of returncodes to match with script's exit code. buildtest will PASS test if script's exit code is found in list of returncodes. You must specify unique numbers as list and a minimum of 1 item in array


| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                            |
| :------------------ | ---------- | -------------- | ----------------------- | :---------------- | --------------------- | ------------------- | ------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [\_definitions.schema.json\*](../out/_definitions.schema.json "open original schema") |

## returncode Type

`integer[]`

## returncode Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.
