# Untitled object in buildtest configuration schema Schema

```txt
settings.schema.json#/definitions/system/properties/compilers/properties/compiler
```

Start of compiler declaration

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                  |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [settings.schema.json*](../out/settings.schema.json "open original schema") |

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

## gcc

Declaration of one or more GNU compilers where we define C, C++ and Fortran compiler. The GNU compiler wrapper are `gcc`, `g++` and `gfortran`.

`gcc`

*   is optional

*   Type: `object` ([Details](settings-definitions-system-properties-compilers-properties-compiler-properties-gcc.md))

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-compiler-properties-gcc.md "settings.schema.json#/definitions/system/properties/compilers/properties/compiler/properties/gcc")

### gcc Type

`object` ([Details](settings-definitions-system-properties-compilers-properties-compiler-properties-gcc.md))

## intel

Declaration of one or more Intel compilers where we define C, C++ and Fortran compiler. The Intel compiler wrapper are `icc`, `icpc` and `ifort`.

`intel`

*   is optional

*   Type: `object` ([Details](settings-definitions-system-properties-compilers-properties-compiler-properties-intel.md))

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-compiler-properties-intel.md "settings.schema.json#/definitions/system/properties/compilers/properties/compiler/properties/intel")

### intel Type

`object` ([Details](settings-definitions-system-properties-compilers-properties-compiler-properties-intel.md))

## cray

Declaration of one or more Cray compilers where we define C, C++ and Fortran compiler. The Cray compiler wrapper are `cc`, `CC` and `ftn`.

`cray`

*   is optional

*   Type: `object` ([Details](settings-definitions-system-properties-compilers-properties-compiler-properties-cray.md))

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-compiler-properties-cray.md "settings.schema.json#/definitions/system/properties/compilers/properties/compiler/properties/cray")

### cray Type

`object` ([Details](settings-definitions-system-properties-compilers-properties-compiler-properties-cray.md))

## pgi

Declaration of one or more PGI compilers where we define C, C++ and Fortran compiler. The PGI compiler wrapper are `pgcc`, `pgc++` and `pgfortran`.

`pgi`

*   is optional

*   Type: `object` ([Details](settings-definitions-system-properties-compilers-properties-compiler-properties-pgi.md))

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-compiler-properties-pgi.md "settings.schema.json#/definitions/system/properties/compilers/properties/compiler/properties/pgi")

### pgi Type

`object` ([Details](settings-definitions-system-properties-compilers-properties-compiler-properties-pgi.md))

## clang

Declaration of one or more Clang compilers where we define C, C++ compiler. The Clang compiler wrapper are `clang`, `clang++`.

`clang`

*   is optional

*   Type: `object` ([Details](settings-definitions-system-properties-compilers-properties-compiler-properties-clang.md))

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-compiler-properties-clang.md "settings.schema.json#/definitions/system/properties/compilers/properties/compiler/properties/clang")

### clang Type

`object` ([Details](settings-definitions-system-properties-compilers-properties-compiler-properties-clang.md))

## cuda

Declaration of one or more Cuda compilers where we define C compiler. The Cuda compiler wrapper is `nvcc`.

`cuda`

*   is optional

*   Type: `object` ([Details](settings-definitions-system-properties-compilers-properties-compiler-properties-cuda.md))

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-compiler-properties-cuda.md "settings.schema.json#/definitions/system/properties/compilers/properties/compiler/properties/cuda")

### cuda Type

`object` ([Details](settings-definitions-system-properties-compilers-properties-compiler-properties-cuda.md))

## upcxx

Declaration of one or more UPCXX compilers where we define C, C++ compiler. The UPCXX compiler wrapper are `upcxx`.

`upcxx`

*   is optional

*   Type: `object` ([Details](settings-definitions-system-properties-compilers-properties-compiler-properties-upcxx.md))

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-compiler-properties-upcxx.md "settings.schema.json#/definitions/system/properties/compilers/properties/compiler/properties/upcxx")

### upcxx Type

`object` ([Details](settings-definitions-system-properties-compilers-properties-compiler-properties-upcxx.md))
