# Untitled array in compiler schema Schema

```txt
compiler.schema.json#/definitions/default_compiler_config/properties/sbatch
```

This field is used for specifying #SBATCH options in test script.

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [compiler.schema.json\*](../out/compiler.schema.json "open original schema") |

## sbatch Type

`string[]`

## sbatch Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.
