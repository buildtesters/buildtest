# Untitled array in script schema version 1.0 Schema

```txt
script-v1.0.schema.json#/properties/bsub
```

This field is used for specifying #BSUB options in test script. buildtest will insert #BSUB in front of each value

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                        |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [script-v1.0.schema.json*](../out/script-v1.0.schema.json "open original schema") |

## bsub Type

`string[]`

## bsub Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.
