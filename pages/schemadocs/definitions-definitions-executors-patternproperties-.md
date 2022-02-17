# Untitled undefined type in JSON Schema Definitions File.  Schema

```txt
definitions.schema.json#/definitions/executors/patternProperties/^.*$
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                         |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [definitions.schema.json\*](../out/definitions.schema.json "open original schema") |

## ^.\*$ Type

unknown

# ^.\*$ Properties

| Property            | Type     | Required | Nullable       | Defined by                                                                                                                                                             |
| :------------------ | :------- | :------- | :------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [env](#env)         | `object` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-env.md "definitions.schema.json#/definitions/executors/patternProperties/^.*$/properties/env")                |
| [vars](#vars)       | `object` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-env.md "definitions.schema.json#/definitions/executors/patternProperties/^.*$/properties/vars")               |
| [sbatch](#sbatch)   | `array`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-list_of_strings.md "definitions.schema.json#/definitions/executors/patternProperties/^.*$/properties/sbatch") |
| [bsub](#bsub)       | `array`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-list_of_strings.md "definitions.schema.json#/definitions/executors/patternProperties/^.*$/properties/bsub")   |
| [pbs](#pbs)         | `array`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-list_of_strings.md "definitions.schema.json#/definitions/executors/patternProperties/^.*$/properties/pbs")    |
| [cobalt](#cobalt)   | `array`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-list_of_strings.md "definitions.schema.json#/definitions/executors/patternProperties/^.*$/properties/cobalt") |
| [BB](#bb)           | `array`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-list_of_strings.md "definitions.schema.json#/definitions/executors/patternProperties/^.*$/properties/BB")     |
| [DW](#dw)           | `array`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-list_of_strings.md "definitions.schema.json#/definitions/executors/patternProperties/^.*$/properties/DW")     |
| [status](#status)   | `object` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-status.md "definitions.schema.json#/definitions/executors/patternProperties/^.*$/properties/status")          |
| [metrics](#metrics) | `object` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-metrics.md "definitions.schema.json#/definitions/executors/patternProperties/^.*$/properties/metrics")        |

## env

One or more key value pairs for an environment (key=value)

`env`

*   is optional

*   Type: `object` ([Details](definitions-definitions-env.md))

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-env.md "definitions.schema.json#/definitions/executors/patternProperties/^.*$/properties/env")

### env Type

`object` ([Details](definitions-definitions-env.md))

### env Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

## vars

One or more key value pairs for an environment (key=value)

`vars`

*   is optional

*   Type: `object` ([Details](definitions-definitions-env.md))

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-env.md "definitions.schema.json#/definitions/executors/patternProperties/^.*$/properties/vars")

### vars Type

`object` ([Details](definitions-definitions-env.md))

### vars Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

## sbatch



`sbatch`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-list_of_strings.md "definitions.schema.json#/definitions/executors/patternProperties/^.*$/properties/sbatch")

### sbatch Type

`string[]`

### sbatch Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## bsub



`bsub`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-list_of_strings.md "definitions.schema.json#/definitions/executors/patternProperties/^.*$/properties/bsub")

### bsub Type

`string[]`

### bsub Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## pbs



`pbs`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-list_of_strings.md "definitions.schema.json#/definitions/executors/patternProperties/^.*$/properties/pbs")

### pbs Type

`string[]`

### pbs Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## cobalt



`cobalt`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-list_of_strings.md "definitions.schema.json#/definitions/executors/patternProperties/^.*$/properties/cobalt")

### cobalt Type

`string[]`

### cobalt Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## BB

Create burst buffer space, this specifies #BB options in your test.

`BB`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-list_of_strings.md "definitions.schema.json#/definitions/executors/patternProperties/^.*$/properties/BB")

### BB Type

`string[]`

### BB Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## DW

Specify Data Warp option (#DW) when using burst buffer.

`DW`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-list_of_strings.md "definitions.schema.json#/definitions/executors/patternProperties/^.*$/properties/DW")

### DW Type

`string[]`

### DW Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## status

The status section describes how buildtest detects PASS/FAIL on test. By default returncode 0 is a PASS and anything else is a FAIL, however buildtest can support other types of PASS/FAIL conditions.

`status`

*   is optional

*   Type: `object` ([Details](definitions-definitions-status.md))

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-status.md "definitions.schema.json#/definitions/executors/patternProperties/^.*$/properties/status")

### status Type

`object` ([Details](definitions-definitions-status.md))

## metrics

This field is used for defining one or more metrics that is recorded for each test. A metric must have a unique name which is recorded in the test metadata.

`metrics`

*   is optional

*   Type: `object` ([Details](definitions-definitions-metrics.md))

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-metrics.md "definitions.schema.json#/definitions/executors/patternProperties/^.*$/properties/metrics")

### metrics Type

`object` ([Details](definitions-definitions-metrics.md))
