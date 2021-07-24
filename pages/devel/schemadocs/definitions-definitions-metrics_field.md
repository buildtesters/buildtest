# Untitled object in JSON Schema Definitions File.  Schema

```txt
definitions.schema.json#/definitions/metrics/patternProperties/^.*$
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                        |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [definitions.schema.json*](../out/definitions.schema.json "open original schema") |

## ^.\*$ Type

`object` ([Details](definitions-definitions-metrics_field.md))

# ^.\*$ Properties

| Property        | Type     | Required | Nullable       | Defined by                                                                                                                                                      |
| :-------------- | :------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [regex](#regex) | `object` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-regex.md "definitions.schema.json#/definitions/metrics_field/properties/regex")                        |
| [vars](#vars)   | `string` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-metrics_field-properties-vars.md "definitions.schema.json#/definitions/metrics_field/properties/vars") |
| [env](#env)     | `string` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-metrics_field-properties-env.md "definitions.schema.json#/definitions/metrics_field/properties/env")   |

## regex

Perform regular expression search using `re.search` python module on stdout/stderr stream for reporting if test `PASS`.

`regex`

*   is optional

*   Type: `object` ([Details](definitions-definitions-regex.md))

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-regex.md "definitions.schema.json#/definitions/metrics_field/properties/regex")

### regex Type

`object` ([Details](definitions-definitions-regex.md))

## vars



`vars`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-metrics_field-properties-vars.md "definitions.schema.json#/definitions/metrics_field/properties/vars")

### vars Type

`string`

## env



`env`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-metrics_field-properties-env.md "definitions.schema.json#/definitions/metrics_field/properties/env")

### env Type

`string`
