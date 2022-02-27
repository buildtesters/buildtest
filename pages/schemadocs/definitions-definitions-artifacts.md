# Untitled object in script schema version Schema

```txt
script.schema.json#/properties/artifacts
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                               |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :----------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [script.schema.json\*](../out/script.schema.json "open original schema") |

## artifacts Type

`object` ([Details](definitions-definitions-artifacts.md))

# artifacts Properties

| Property          | Type      | Required | Nullable       | Defined by                                                                                                                                                  |
| :---------------- | :-------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [output](#output) | `boolean` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-artifacts-properties-output.md "definitions.schema.json#/definitions/artifacts/properties/output") |
| [error](#error)   | `boolean` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-artifacts-properties-error.md "definitions.schema.json#/definitions/artifacts/properties/error")   |
| [files](#files)   | `array`   | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-list_of_strings.md "definitions.schema.json#/definitions/artifacts/properties/files")              |

## output

Save output file

`output`

*   is optional

*   Type: `boolean`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-artifacts-properties-output.md "definitions.schema.json#/definitions/artifacts/properties/output")

### output Type

`boolean`

## error

Save error file

`error`

*   is optional

*   Type: `boolean`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-artifacts-properties-error.md "definitions.schema.json#/definitions/artifacts/properties/error")

### error Type

`boolean`

## files

List of files to save as artifacts for job dependency

`files`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-list_of_strings.md "definitions.schema.json#/definitions/artifacts/properties/files")

### files Type

`string[]`

### files Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.
