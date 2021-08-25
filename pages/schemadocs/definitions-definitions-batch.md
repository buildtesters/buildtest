# Untitled object in JSON Schema Definitions File.  Schema

```txt
definitions.schema.json#/definitions/batch
```

The `batch` field is used to specify scheduler agnostic directives that are translated to #SBATCH or #BSUB based on your scheduler. This is an experimental feature that supports a subset of scheduler parameters.

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                        |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [definitions.schema.json*](../out/definitions.schema.json "open original schema") |

## batch Type

`object` ([Details](definitions-definitions-batch.md))

# batch Properties

| Property                              | Type      | Required | Nullable       | Defined by                                                                                                                                                              |
| :------------------------------------ | :-------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [account](#account)                   | `string`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-batch-properties-account.md "definitions.schema.json#/definitions/batch/properties/account")                   |
| [begintime](#begintime)               | `string`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-batch-properties-begintime.md "definitions.schema.json#/definitions/batch/properties/begintime")               |
| [cpucount](#cpucount)                 | `string`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-batch-properties-cpucount.md "definitions.schema.json#/definitions/batch/properties/cpucount")                 |
| [email-address](#email-address)       | `string`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-batch-properties-email-address.md "definitions.schema.json#/definitions/batch/properties/email-address")       |
| [exclusive](#exclusive)               | `boolean` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-batch-properties-exclusive.md "definitions.schema.json#/definitions/batch/properties/exclusive")               |
| [memory](#memory)                     | `string`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-batch-properties-memory.md "definitions.schema.json#/definitions/batch/properties/memory")                     |
| [network](#network)                   | `string`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-batch-properties-network.md "definitions.schema.json#/definitions/batch/properties/network")                   |
| [nodecount](#nodecount)               | `string`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-batch-properties-nodecount.md "definitions.schema.json#/definitions/batch/properties/nodecount")               |
| [qos](#qos)                           | `string`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-batch-properties-qos.md "definitions.schema.json#/definitions/batch/properties/qos")                           |
| [queue](#queue)                       | `string`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-batch-properties-queue.md "definitions.schema.json#/definitions/batch/properties/queue")                       |
| [tasks-per-core](#tasks-per-core)     | `string`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-batch-properties-tasks-per-core.md "definitions.schema.json#/definitions/batch/properties/tasks-per-core")     |
| [tasks-per-node](#tasks-per-node)     | `string`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-batch-properties-tasks-per-node.md "definitions.schema.json#/definitions/batch/properties/tasks-per-node")     |
| [tasks-per-socket](#tasks-per-socket) | `string`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-batch-properties-tasks-per-socket.md "definitions.schema.json#/definitions/batch/properties/tasks-per-socket") |
| [timelimit](#timelimit)               | `string`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-batch-properties-timelimit.md "definitions.schema.json#/definitions/batch/properties/timelimit")               |

## account

Specify Account to charge job

`account`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-batch-properties-account.md "definitions.schema.json#/definitions/batch/properties/account")

### account Type

`string`

## begintime

Specify begin time when job will start allocation

`begintime`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-batch-properties-begintime.md "definitions.schema.json#/definitions/batch/properties/begintime")

### begintime Type

`string`

## cpucount

Specify number of CPU to allocate

`cpucount`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-batch-properties-cpucount.md "definitions.schema.json#/definitions/batch/properties/cpucount")

### cpucount Type

`string`

## email-address

Email Address to notify on Job State Changes

`email-address`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-batch-properties-email-address.md "definitions.schema.json#/definitions/batch/properties/email-address")

### email-address Type

`string`

## exclusive

Specify if job needs to run in exclusive mode

`exclusive`

*   is optional

*   Type: `boolean`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-batch-properties-exclusive.md "definitions.schema.json#/definitions/batch/properties/exclusive")

### exclusive Type

`boolean`

## memory

Specify Memory Size for Job

`memory`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-batch-properties-memory.md "definitions.schema.json#/definitions/batch/properties/memory")

### memory Type

`string`

## network

Specify network resource requirement for job

`network`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-batch-properties-network.md "definitions.schema.json#/definitions/batch/properties/network")

### network Type

`string`

## nodecount

Specify number of Nodes to allocate

`nodecount`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-batch-properties-nodecount.md "definitions.schema.json#/definitions/batch/properties/nodecount")

### nodecount Type

`string`

## qos

Specify Quality of Service (QOS)

`qos`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-batch-properties-qos.md "definitions.schema.json#/definitions/batch/properties/qos")

### qos Type

`string`

## queue

Specify Job Queue

`queue`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-batch-properties-queue.md "definitions.schema.json#/definitions/batch/properties/queue")

### queue Type

`string`

## tasks-per-core

Request number of tasks to be invoked on each core.

`tasks-per-core`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-batch-properties-tasks-per-core.md "definitions.schema.json#/definitions/batch/properties/tasks-per-core")

### tasks-per-core Type

`string`

## tasks-per-node

Request number of tasks to be invoked on each node.

`tasks-per-node`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-batch-properties-tasks-per-node.md "definitions.schema.json#/definitions/batch/properties/tasks-per-node")

### tasks-per-node Type

`string`

## tasks-per-socket

Request the maximum tasks to be invoked on each socket.

`tasks-per-socket`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-batch-properties-tasks-per-socket.md "definitions.schema.json#/definitions/batch/properties/tasks-per-socket")

### tasks-per-socket Type

`string`

## timelimit

Specify Job timelimit

`timelimit`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-batch-properties-timelimit.md "definitions.schema.json#/definitions/batch/properties/timelimit")

### timelimit Type

`string`
