# Untitled object in buildtest configuration schema Schema

```txt
settings.schema.json#/definitions/system/properties/compilers/properties/find
```

Find compilers by specifying regular expression that is applied to modulefile names

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [settings.schema.json\*](../out/settings.schema.json "open original schema") |

## find Type

`object` ([Details](settings-definitions-system-properties-compilers-properties-find.md))

# find Properties

| Property        | Type     | Required | Nullable       | Defined by                                                                                                                                                                                                              |
| :-------------- | :------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [gcc](#gcc)     | `string` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-find-properties-gcc.md "settings.schema.json#/definitions/system/properties/compilers/properties/find/properties/gcc")     |
| [intel](#intel) | `string` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-find-properties-intel.md "settings.schema.json#/definitions/system/properties/compilers/properties/find/properties/intel") |
| [cray](#cray)   | `string` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-find-properties-cray.md "settings.schema.json#/definitions/system/properties/compilers/properties/find/properties/cray")   |
| [clang](#clang) | `string` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-find-properties-clang.md "settings.schema.json#/definitions/system/properties/compilers/properties/find/properties/clang") |
| [cuda](#cuda)   | `string` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-find-properties-cuda.md "settings.schema.json#/definitions/system/properties/compilers/properties/find/properties/cuda")   |
| [pgi](#pgi)     | `string` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-find-properties-pgi.md "settings.schema.json#/definitions/system/properties/compilers/properties/find/properties/pgi")     |
| [upcxx](#upcxx) | `string` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-find-properties-upcxx.md "settings.schema.json#/definitions/system/properties/compilers/properties/find/properties/upcxx") |
| [nvhpc](#nvhpc) | `string` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-find-properties-nvhpc.md "settings.schema.json#/definitions/system/properties/compilers/properties/find/properties/nvhpc") |

## gcc

Specify a regular expression to search for gcc compilers from your module stack

`gcc`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-find-properties-gcc.md "settings.schema.json#/definitions/system/properties/compilers/properties/find/properties/gcc")

### gcc Type

`string`

## intel

Specify a regular expression to search for intel compilers from your module stack

`intel`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-find-properties-intel.md "settings.schema.json#/definitions/system/properties/compilers/properties/find/properties/intel")

### intel Type

`string`

## cray

Specify a regular expression to search for cray compilers from your module stack

`cray`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-find-properties-cray.md "settings.schema.json#/definitions/system/properties/compilers/properties/find/properties/cray")

### cray Type

`string`

## clang

Specify a regular expression to search for clang compilers from your module stack

`clang`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-find-properties-clang.md "settings.schema.json#/definitions/system/properties/compilers/properties/find/properties/clang")

### clang Type

`string`

## cuda

Specify a regular expression to search for cuda compilers from your module stack

`cuda`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-find-properties-cuda.md "settings.schema.json#/definitions/system/properties/compilers/properties/find/properties/cuda")

### cuda Type

`string`

## pgi

Specify a regular expression to search for pgi compilers from your module stack

`pgi`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-find-properties-pgi.md "settings.schema.json#/definitions/system/properties/compilers/properties/find/properties/pgi")

### pgi Type

`string`

## upcxx

Specify a regular expression to search for upcxx compilers from your module stack

`upcxx`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-find-properties-upcxx.md "settings.schema.json#/definitions/system/properties/compilers/properties/find/properties/upcxx")

### upcxx Type

`string`

## nvhpc

Specify a regular expression to search for nvhpc compilers from your module stack

`nvhpc`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-find-properties-nvhpc.md "settings.schema.json#/definitions/system/properties/compilers/properties/find/properties/nvhpc")

### nvhpc Type

`string`
