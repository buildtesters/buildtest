# Untitled object in buildtest configuration schema Schema

```txt
https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers
```

Declare compiler section for defining system compilers that can be referenced in buildspec.


| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | ---------- | -------------- | ------------ | :---------------- | --------------------- | ------------------- | ---------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [settings.schema.json\*](../out/settings.schema.json "open original schema") |

## compilers Type

`object` ([Details](settings-properties-compilers.md))

# undefined Properties

| Property        | Type     | Required | Nullable       | Defined by                                                                                                                                                                                              |
| :-------------- | -------- | -------- | -------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [find](#find)   | `object` | Optional | cannot be null | [buildtest configuration schema](settings-properties-compilers-properties-find.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/find")   |
| [gcc](#gcc)     | `object` | Optional | cannot be null | [buildtest configuration schema](settings-properties-compilers-properties-gcc.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/gcc")     |
| [intel](#intel) | `object` | Optional | cannot be null | [buildtest configuration schema](settings-properties-compilers-properties-intel.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/intel") |
| [cray](#cray)   | `object` | Optional | cannot be null | [buildtest configuration schema](settings-properties-compilers-properties-cray.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/cray")   |
| [pgi](#pgi)     | `object` | Optional | cannot be null | [buildtest configuration schema](settings-properties-compilers-properties-pgi.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/pgi")     |
| [clang](#clang) | `object` | Optional | cannot be null | [buildtest configuration schema](settings-properties-compilers-properties-clang.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/clang") |
| [cuda](#cuda)   | `object` | Optional | cannot be null | [buildtest configuration schema](settings-properties-compilers-properties-cuda.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/cuda")   |

## find

Find compilers based on module names


`find`

-   is optional
-   Type: `object` ([Details](settings-properties-compilers-properties-find.md))
-   cannot be null
-   defined in: [buildtest configuration schema](settings-properties-compilers-properties-find.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/find")

### find Type

`object` ([Details](settings-properties-compilers-properties-find.md))

## gcc

Declaration of one or more GNU compilers where we define C, C++ and Fortran compiler. The GNU compiler wrapper are `gcc`, `g++` and `gfortran`. 


`gcc`

-   is optional
-   Type: `object` ([Details](settings-properties-compilers-properties-gcc.md))
-   cannot be null
-   defined in: [buildtest configuration schema](settings-properties-compilers-properties-gcc.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/gcc")

### gcc Type

`object` ([Details](settings-properties-compilers-properties-gcc.md))

## intel

Declaration of one or more Intel compilers where we define C, C++ and Fortran compiler. The Intel compiler wrapper are `icc`, `icpc` and `ifort`. 


`intel`

-   is optional
-   Type: `object` ([Details](settings-properties-compilers-properties-intel.md))
-   cannot be null
-   defined in: [buildtest configuration schema](settings-properties-compilers-properties-intel.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/intel")

### intel Type

`object` ([Details](settings-properties-compilers-properties-intel.md))

## cray

Declaration of one or more Cray compilers where we define C, C++ and Fortran compiler. The Cray compiler wrapper are `cc`, `CC` and `ftn`.


`cray`

-   is optional
-   Type: `object` ([Details](settings-properties-compilers-properties-cray.md))
-   cannot be null
-   defined in: [buildtest configuration schema](settings-properties-compilers-properties-cray.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/cray")

### cray Type

`object` ([Details](settings-properties-compilers-properties-cray.md))

## pgi

Declaration of one or more PGI compilers where we define C, C++ and Fortran compiler. The PGI compiler wrapper are `pgcc`, `pgc++` and `pgfortran`.


`pgi`

-   is optional
-   Type: `object` ([Details](settings-properties-compilers-properties-pgi.md))
-   cannot be null
-   defined in: [buildtest configuration schema](settings-properties-compilers-properties-pgi.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/pgi")

### pgi Type

`object` ([Details](settings-properties-compilers-properties-pgi.md))

## clang

Declaration of one or more Clang compilers where we define C, C++ compiler. The Clang compiler wrapper are `clang`, `clang++`.


`clang`

-   is optional
-   Type: `object` ([Details](settings-properties-compilers-properties-clang.md))
-   cannot be null
-   defined in: [buildtest configuration schema](settings-properties-compilers-properties-clang.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/clang")

### clang Type

`object` ([Details](settings-properties-compilers-properties-clang.md))

## cuda

Declaration of one or more Cuda compilers where we define C compiler. The Cuda compiler wrapper is `nvcc`. 


`cuda`

-   is optional
-   Type: `object` ([Details](settings-properties-compilers-properties-cuda.md))
-   cannot be null
-   defined in: [buildtest configuration schema](settings-properties-compilers-properties-cuda.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/cuda")

### cuda Type

`object` ([Details](settings-properties-compilers-properties-cuda.md))
