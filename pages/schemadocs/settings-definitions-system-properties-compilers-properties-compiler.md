# Untitled object in buildtest configuration schema Schema

```txt
settings.schema.json#/definitions/system/properties/compilers/properties/compiler
```

Start of compiler declaration

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [settings.schema.json\*](../out/settings.schema.json "open original schema") |

## compiler Type

`object` ([Details](settings-definitions-system-properties-compilers-properties-compiler.md))

# compiler Properties

| Property        | Type     | Required | Nullable       | Defined by                                                                                                                                                                                                                      |
| :-------------- | :------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [gcc](#gcc)     | `object` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-compiler-properties-gcc.md "settings.schema.json#/definitions/system/properties/compilers/properties/compiler/properties/gcc")     |
| [intel](#intel) | `object` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-compiler-properties-intel.md "settings.schema.json#/definitions/system/properties/compilers/properties/compiler/properties/intel") |
| [cray](#cray)   | `object` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-compiler-properties-cray.md "settings.schema.json#/definitions/system/properties/compilers/properties/compiler/properties/cray")   |
| [pgi](#pgi)     | `object` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-compiler-properties-pgi.md "settings.schema.json#/definitions/system/properties/compilers/properties/compiler/properties/pgi")     |
| [clang](#clang) | `object` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-compiler-properties-clang.md "settings.schema.json#/definitions/system/properties/compilers/properties/compiler/properties/clang") |
| [cuda](#cuda)   | `object` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-compiler-properties-cuda.md "settings.schema.json#/definitions/system/properties/compilers/properties/compiler/properties/cuda")   |
| [upcxx](#upcxx) | `object` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-compiler-properties-upcxx.md "settings.schema.json#/definitions/system/properties/compilers/properties/compiler/properties/upcxx") |
| [nvhpc](#nvhpc) | `object` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-compiler-properties-nvhpc.md "settings.schema.json#/definitions/system/properties/compilers/properties/compiler/properties/nvhpc") |

## gcc

Declaration of one or more GNU compilers.

`gcc`

*   is optional

*   Type: `object` ([Details](settings-definitions-system-properties-compilers-properties-compiler-properties-gcc.md))

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-compiler-properties-gcc.md "settings.schema.json#/definitions/system/properties/compilers/properties/compiler/properties/gcc")

### gcc Type

`object` ([Details](settings-definitions-system-properties-compilers-properties-compiler-properties-gcc.md))

## intel

Declaration of one or more Intel compilers.

`intel`

*   is optional

*   Type: `object` ([Details](settings-definitions-system-properties-compilers-properties-compiler-properties-intel.md))

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-compiler-properties-intel.md "settings.schema.json#/definitions/system/properties/compilers/properties/compiler/properties/intel")

### intel Type

`object` ([Details](settings-definitions-system-properties-compilers-properties-compiler-properties-intel.md))

## cray

Declaration of one or more Cray compilers.

`cray`

*   is optional

*   Type: `object` ([Details](settings-definitions-system-properties-compilers-properties-compiler-properties-cray.md))

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-compiler-properties-cray.md "settings.schema.json#/definitions/system/properties/compilers/properties/compiler/properties/cray")

### cray Type

`object` ([Details](settings-definitions-system-properties-compilers-properties-compiler-properties-cray.md))

## pgi

Declaration of one or more PGI compilers.

`pgi`

*   is optional

*   Type: `object` ([Details](settings-definitions-system-properties-compilers-properties-compiler-properties-pgi.md))

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-compiler-properties-pgi.md "settings.schema.json#/definitions/system/properties/compilers/properties/compiler/properties/pgi")

### pgi Type

`object` ([Details](settings-definitions-system-properties-compilers-properties-compiler-properties-pgi.md))

## clang

Declaration of one or more Clang compilers.

`clang`

*   is optional

*   Type: `object` ([Details](settings-definitions-system-properties-compilers-properties-compiler-properties-clang.md))

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-compiler-properties-clang.md "settings.schema.json#/definitions/system/properties/compilers/properties/compiler/properties/clang")

### clang Type

`object` ([Details](settings-definitions-system-properties-compilers-properties-compiler-properties-clang.md))

## cuda

Declaration of one or more CUDA compilers.

`cuda`

*   is optional

*   Type: `object` ([Details](settings-definitions-system-properties-compilers-properties-compiler-properties-cuda.md))

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-compiler-properties-cuda.md "settings.schema.json#/definitions/system/properties/compilers/properties/compiler/properties/cuda")

### cuda Type

`object` ([Details](settings-definitions-system-properties-compilers-properties-compiler-properties-cuda.md))

## upcxx

Declaration of one or more UPCXX compilers.

`upcxx`

*   is optional

*   Type: `object` ([Details](settings-definitions-system-properties-compilers-properties-compiler-properties-upcxx.md))

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-compiler-properties-upcxx.md "settings.schema.json#/definitions/system/properties/compilers/properties/compiler/properties/upcxx")

### upcxx Type

`object` ([Details](settings-definitions-system-properties-compilers-properties-compiler-properties-upcxx.md))

## nvhpc

Declaration of one or more NVHPC compilers.

`nvhpc`

*   is optional

*   Type: `object` ([Details](settings-definitions-system-properties-compilers-properties-compiler-properties-nvhpc.md))

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-compiler-properties-nvhpc.md "settings.schema.json#/definitions/system/properties/compilers/properties/compiler/properties/nvhpc")

### nvhpc Type

`object` ([Details](settings-definitions-system-properties-compilers-properties-compiler-properties-nvhpc.md))
