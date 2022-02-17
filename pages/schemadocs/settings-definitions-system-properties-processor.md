# Untitled object in buildtest configuration schema Schema

```txt
settings.schema.json#/definitions/system/properties/processor
```

Specify processor information

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [settings.schema.json\*](../out/settings.schema.json "open original schema") |

## processor Type

`object` ([Details](settings-definitions-system-properties-processor.md))

# processor Properties

| Property                                | Type      | Required | Nullable       | Defined by                                                                                                                                                                                                    |
| :-------------------------------------- | :-------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [numcpus](#numcpus)                     | `integer` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-processor-properties-numcpus.md "settings.schema.json#/definitions/system/properties/processor/properties/numcpus")                   |
| [sockets](#sockets)                     | `integer` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-processor-properties-sockets.md "settings.schema.json#/definitions/system/properties/processor/properties/sockets")                   |
| [cores](#cores)                         | `integer` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-processor-properties-cores.md "settings.schema.json#/definitions/system/properties/processor/properties/cores")                       |
| [threads\_per\_core](#threads_per_core) | `integer` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-processor-properties-threads_per_core.md "settings.schema.json#/definitions/system/properties/processor/properties/threads_per_core") |
| [core\_per\_socket](#core_per_socket)   | `integer` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-processor-properties-core_per_socket.md "settings.schema.json#/definitions/system/properties/processor/properties/core_per_socket")   |
| [model](#model)                         | `string`  | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-processor-properties-model.md "settings.schema.json#/definitions/system/properties/processor/properties/model")                       |
| [arch](#arch)                           | `string`  | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-processor-properties-arch.md "settings.schema.json#/definitions/system/properties/processor/properties/arch")                         |
| [vendor](#vendor)                       | `string`  | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-processor-properties-vendor.md "settings.schema.json#/definitions/system/properties/processor/properties/vendor")                     |

## numcpus

Specify Total Number of CPUs

`numcpus`

*   is optional

*   Type: `integer`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-processor-properties-numcpus.md "settings.schema.json#/definitions/system/properties/processor/properties/numcpus")

### numcpus Type

`integer`

### numcpus Constraints

**minimum**: the value of this number must greater than or equal to: `1`

## sockets

Specify Number of CPU Sockets

`sockets`

*   is optional

*   Type: `integer`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-processor-properties-sockets.md "settings.schema.json#/definitions/system/properties/processor/properties/sockets")

### sockets Type

`integer`

### sockets Constraints

**minimum**: the value of this number must greater than or equal to: `1`

## cores

Specify Number of Physical Cores

`cores`

*   is optional

*   Type: `integer`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-processor-properties-cores.md "settings.schema.json#/definitions/system/properties/processor/properties/cores")

### cores Type

`integer`

### cores Constraints

**minimum**: the value of this number must greater than or equal to: `1`

## threads\_per\_core

Specify Threads per Core

`threads_per_core`

*   is optional

*   Type: `integer`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-processor-properties-threads_per_core.md "settings.schema.json#/definitions/system/properties/processor/properties/threads_per_core")

### threads\_per\_core Type

`integer`

### threads\_per\_core Constraints

**minimum**: the value of this number must greater than or equal to: `1`

## core\_per\_socket

Specify Cores per Socket

`core_per_socket`

*   is optional

*   Type: `integer`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-processor-properties-core_per_socket.md "settings.schema.json#/definitions/system/properties/processor/properties/core_per_socket")

### core\_per\_socket Type

`integer`

### core\_per\_socket Constraints

**minimum**: the value of this number must greater than or equal to: `1`

## model

Specify Processor Model

`model`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-processor-properties-model.md "settings.schema.json#/definitions/system/properties/processor/properties/model")

### model Type

`string`

## arch

Specify processor architecture

`arch`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-processor-properties-arch.md "settings.schema.json#/definitions/system/properties/processor/properties/arch")

### arch Type

`string`

## vendor

Vendor Name

`vendor`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-processor-properties-vendor.md "settings.schema.json#/definitions/system/properties/processor/properties/vendor")

### vendor Type

`string`
