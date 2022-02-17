# Untitled string in compiler schema Schema

```txt
compiler.schema.json#/properties/type
```

Select schema type to use when validating buildspec. This must be of set to `compiler`.

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [compiler.schema.json\*](../out/compiler.schema.json "open original schema") |

## type Type

`string`

## type Constraints

**pattern**: the string must match the following regular expression:&#x20;

```regexp
^compiler$
```

[try pattern](https://regexr.com/?expression=%5Ecompiler%24 "try regular expression with regexr.com")
