# Untitled object in JSON Schema Definitions File.  Schema

```txt
definitions.schema.json#/definitions/metrics_field/properties/regex
```

Perform regular expression search using `re.search` python module on stdout/stderr stream for reporting if test `PASS`.

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                        |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [definitions.schema.json*](../out/definitions.schema.json "open original schema") |

## regex Type

`object` ([Details](definitions-definitions-regex.md))

# regex Properties

| Property          | Type     | Required | Nullable       | Defined by                                                                                                                                          |
| :---------------- | :------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------- |
| [stream](#stream) | `string` | Required | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-regex-properties-stream.md "definitions.schema.json#/definitions/regex/properties/stream") |
| [exp](#exp)       | `string` | Required | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-regex-properties-exp.md "definitions.schema.json#/definitions/regex/properties/exp")       |

## stream

The stream field can be stdout or stderr. buildtest will read the output or error stream after completion of test and check if regex matches in stream

`stream`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-regex-properties-stream.md "definitions.schema.json#/definitions/regex/properties/stream")

### stream Type

`string`

### stream Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value      | Explanation |
| :--------- | :---------- |
| `"stdout"` |             |
| `"stderr"` |             |

## exp

Specify a regular expression to run with input stream specified by `stream` field. buildtest uses re.search when performing regex

`exp`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-regex-properties-exp.md "definitions.schema.json#/definitions/regex/properties/exp")

### exp Type

`string`
