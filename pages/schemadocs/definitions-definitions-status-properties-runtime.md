# Untitled object in JSON Schema Definitions File.  Schema

```txt
definitions.schema.json#/definitions/status/properties/runtime
```

The runtime section will pass test based on min and max values and compare with actual runtime.

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                         |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [definitions.schema.json\*](../out/definitions.schema.json "open original schema") |

## runtime Type

`object` ([Details](definitions-definitions-status-properties-runtime.md))

# runtime Properties

| Property    | Type     | Required | Nullable       | Defined by                                                                                                                                                                            |
| :---------- | :------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [min](#min) | `number` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-status-properties-runtime-properties-min.md "definitions.schema.json#/definitions/status/properties/runtime/properties/min") |
| [max](#max) | `number` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-status-properties-runtime-properties-max.md "definitions.schema.json#/definitions/status/properties/runtime/properties/max") |

## min

Specify a minimum runtime in seconds. The test will PASS if actual runtime exceeds min time.

`min`

*   is optional

*   Type: `number`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-status-properties-runtime-properties-min.md "definitions.schema.json#/definitions/status/properties/runtime/properties/min")

### min Type

`number`

### min Constraints

**minimum**: the value of this number must greater than or equal to: `0`

## max

Specify a maximum runtime in seconds. The test will PASS if actual runtime is less than max time

`max`

*   is optional

*   Type: `number`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-status-properties-runtime-properties-max.md "definitions.schema.json#/definitions/status/properties/runtime/properties/max")

### max Type

`number`

### max Constraints

**minimum**: the value of this number must greater than or equal to: `0`
