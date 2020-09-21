# Untitled string in global schema Schema

```txt
https://buildtesters.github.io/buildtest/schemas/global.schema.json#/definitions/status/properties/regex/properties/stream
```

The stream field can be stdout or stderr. buildtest will read the output or error stream after completion of test and check if regex matches in stream


| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                               |
| :------------------ | ---------- | -------------- | ----------------------- | :---------------- | --------------------- | ------------------- | ------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [global.schema.json\*](../out/global.schema.json "open original schema") |

## stream Type

`string`

## stream Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value      | Explanation |
| :--------- | ----------- |
| `"stdout"` |             |
| `"stderr"` |             |
