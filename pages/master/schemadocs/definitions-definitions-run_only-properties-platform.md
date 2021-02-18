# Untitled string in JSON Schema Definitions File.  Schema

```txt
definitions.schema.json#/definitions/run_only/properties/platform
```

This test will run if target system is Linux or Darwin. We check target system using `platform.system()` and match with input field

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                        |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [definitions.schema.json*](../out/definitions.schema.json "open original schema") |

## platform Type

`string`

## platform Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value      | Explanation |
| :--------- | :---------- |
| `"Linux"`  |             |
| `"Darwin"` |             |
