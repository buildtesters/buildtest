# Untitled array in spack schema version 1.0 Schema

```txt
spack-v1.0.schema.json#/definitions/test/properties/results/properties/specs
```

Report result by spec name by running `spack test run -- <specs>`.

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                      |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [spack-v1.0.schema.json*](../out/spack-v1.0.schema.json "open original schema") |

## specs Type

`string[]`

## specs Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.
