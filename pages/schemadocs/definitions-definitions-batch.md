# Untitled object in script schema version 1.0 Schema

```txt
script-v1.0.schema.json#/properties/batch
```

The `batch` field is used to specify scheduler agnostic directives that are translated to #SBATCH or #BSUB based on your scheduler. This is an experimental feature that supports a subset of scheduler parameters.


| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                         |
| :------------------ | ---------- | -------------- | ------------ | :---------------- | --------------------- | ------------------- | ---------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [script-v1.0.schema.json\*](../out/script-v1.0.schema.json "open original schema") |

## batch Type

`object` ([Details](definitions-definitions-batch.md))

# undefined Properties

| Property                | Type      | Required | Nullable       | Defined by                                                                                                                                                |
| :---------------------- | --------- | -------- | -------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [queue](#queue)         | `string`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-batch-properties-queue.md "definitions.schema.json#/definitions/batch/properties/queue")         |
| [nodecount](#nodecount) | `string`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-batch-properties-nodecount.md "definitions.schema.json#/definitions/batch/properties/nodecount") |
| [cpucount](#cpucount)   | `string`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-batch-properties-cpucount.md "definitions.schema.json#/definitions/batch/properties/cpucount")   |
| [timelimit](#timelimit) | `string`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-batch-properties-timelimit.md "definitions.schema.json#/definitions/batch/properties/timelimit") |
| [memory](#memory)       | `string`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-batch-properties-memory.md "definitions.schema.json#/definitions/batch/properties/memory")       |
| [account](#account)     | `string`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-batch-properties-account.md "definitions.schema.json#/definitions/batch/properties/account")     |
| [exclusive](#exclusive) | `boolean` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-batch-properties-exclusive.md "definitions.schema.json#/definitions/batch/properties/exclusive") |

## queue

Specify Job Queue


`queue`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [JSON Schema Definitions File. ](definitions-definitions-batch-properties-queue.md "definitions.schema.json#/definitions/batch/properties/queue")

### queue Type

`string`

## nodecount

Specify number of Nodes to allocate


`nodecount`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [JSON Schema Definitions File. ](definitions-definitions-batch-properties-nodecount.md "definitions.schema.json#/definitions/batch/properties/nodecount")

### nodecount Type

`string`

## cpucount

Specify number of CPU to allocate


`cpucount`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [JSON Schema Definitions File. ](definitions-definitions-batch-properties-cpucount.md "definitions.schema.json#/definitions/batch/properties/cpucount")

### cpucount Type

`string`

## timelimit

Specify Job timelimit


`timelimit`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [JSON Schema Definitions File. ](definitions-definitions-batch-properties-timelimit.md "definitions.schema.json#/definitions/batch/properties/timelimit")

### timelimit Type

`string`

## memory

Specify Memory Size for Job


`memory`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [JSON Schema Definitions File. ](definitions-definitions-batch-properties-memory.md "definitions.schema.json#/definitions/batch/properties/memory")

### memory Type

`string`

## account

Specify Account to charge job


`account`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [JSON Schema Definitions File. ](definitions-definitions-batch-properties-account.md "definitions.schema.json#/definitions/batch/properties/account")

### account Type

`string`

## exclusive

Specify if job needs to run in exclusive mode


`exclusive`

-   is optional
-   Type: `boolean`
-   cannot be null
-   defined in: [JSON Schema Definitions File. ](definitions-definitions-batch-properties-exclusive.md "definitions.schema.json#/definitions/batch/properties/exclusive")

### exclusive Type

`boolean`
