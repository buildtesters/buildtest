# Untitled array in JSON Schema Definitions File.  Schema

```txt
definitions.schema.json#/definitions/run_only/properties/linux_distro
```

Specify a list of Linux Distros to check when processing test. If target system matches one of input field, test will be processed.

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                        |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [definitions.schema.json*](../out/definitions.schema.json "open original schema") |

## linux_distro Type

`string[]`

## linux_distro Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.
