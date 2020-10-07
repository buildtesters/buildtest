# Untitled object in script schema version 1.0 Schema

```txt
script-v1.0.schema.json#/properties/run_only
```

A set of conditions to specify when running tests. All conditions must pass in order to process test.


| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                         |
| :------------------ | ---------- | -------------- | ------------ | :---------------- | --------------------- | ------------------- | ---------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [script-v1.0.schema.json\*](../out/script-v1.0.schema.json "open original schema") |

## run_only Type

`object` ([Details](definitions-definitions-run_only.md))

# undefined Properties

| Property                      | Type     | Required | Nullable       | Defined by                                                                                                                                                            |
| :---------------------------- | -------- | -------- | -------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [scheduler](#scheduler)       | `string` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-run_only-properties-scheduler.md "definitions.schema.json#/definitions/run_only/properties/scheduler")       |
| [user](#user)                 | `string` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-run_only-properties-user.md "definitions.schema.json#/definitions/run_only/properties/user")                 |
| [platform](#platform)         | `string` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-run_only-properties-platform.md "definitions.schema.json#/definitions/run_only/properties/platform")         |
| [linux_distro](#linux_distro) | `array`  | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-run_only-properties-linux_distro.md "definitions.schema.json#/definitions/run_only/properties/linux_distro") |

## scheduler

Test will run only if scheduler is available. We assume binaries are available in $PATH


`scheduler`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [JSON Schema Definitions File. ](definitions-definitions-run_only-properties-scheduler.md "definitions.schema.json#/definitions/run_only/properties/scheduler")

### scheduler Type

`string`

### scheduler Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value     | Explanation |
| :-------- | ----------- |
| `"lsf"`   |             |
| `"slurm"` |             |

## user

Test will run only if current user matches this field, otherwise test will be skipped


`user`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [JSON Schema Definitions File. ](definitions-definitions-run_only-properties-user.md "definitions.schema.json#/definitions/run_only/properties/user")

### user Type

`string`

## platform

This test will run if target system is Linux or Darwin. We check target system using `platform.system()` and match with input field


`platform`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [JSON Schema Definitions File. ](definitions-definitions-run_only-properties-platform.md "definitions.schema.json#/definitions/run_only/properties/platform")

### platform Type

`string`

### platform Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value      | Explanation |
| :--------- | ----------- |
| `"Linux"`  |             |
| `"Darwin"` |             |

## linux_distro

Specify a list of Linux Distros to check when processing test. If target system matches one of input field, test will be processed.


`linux_distro`

-   is optional
-   Type: `string[]`
-   cannot be null
-   defined in: [JSON Schema Definitions File. ](definitions-definitions-run_only-properties-linux_distro.md "definitions.schema.json#/definitions/run_only/properties/linux_distro")

### linux_distro Type

`string[]`

### linux_distro Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.
