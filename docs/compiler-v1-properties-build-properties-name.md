# Untitled string in compiler schema version 1.0 Schema

```txt
https://buildtesters.github.io/buildtest/schemas/compiler-v1.0.schema.json#/properties/build/properties/name
```

Select the compiler class to use, buildtest will set cc, cxx, and fc compiler wrapper based on compiler name


| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                             |
| :------------------ | ---------- | -------------- | ----------------------- | :---------------- | --------------------- | ------------------- | -------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [compiler-v1.0.schema.json\*](../out/compiler-v1.0.schema.json "open original schema") |

## name Type

`string`

## name Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value     | Explanation |
| :-------- | ----------- |
| `"gnu"`   |             |
| `"intel"` |             |
| `"pgi"`   |             |
| `"cray"`  |             |
