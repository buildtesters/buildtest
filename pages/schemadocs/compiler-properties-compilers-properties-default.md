# Untitled object in compiler schema Schema

```txt
compiler.schema.json#/properties/compilers/properties/default
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [compiler.schema.json\*](../out/compiler.schema.json "open original schema") |

## default Type

`object` ([Details](compiler-properties-compilers-properties-default.md))

# default Properties

| Property        | Type     | Required | Nullable       | Defined by                                                                                                                                          |
| :-------------- | :------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------- |
| [all](#all)     | `object` | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_all.md "compiler.schema.json#/properties/compilers/properties/default/properties/all")      |
| [gcc](#gcc)     | `object` | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_config.md "compiler.schema.json#/properties/compilers/properties/default/properties/gcc")   |
| [intel](#intel) | `object` | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_config.md "compiler.schema.json#/properties/compilers/properties/default/properties/intel") |
| [pgi](#pgi)     | `object` | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_config.md "compiler.schema.json#/properties/compilers/properties/default/properties/pgi")   |
| [cray](#cray)   | `object` | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_config.md "compiler.schema.json#/properties/compilers/properties/default/properties/cray")  |
| [clang](#clang) | `object` | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_config.md "compiler.schema.json#/properties/compilers/properties/default/properties/clang") |
| [cuda](#cuda)   | `object` | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_config.md "compiler.schema.json#/properties/compilers/properties/default/properties/cuda")  |
| [upcxx](#upcxx) | `object` | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_config.md "compiler.schema.json#/properties/compilers/properties/default/properties/upcxx") |
| [nvhpc](#nvhpc) | `object` | Optional | cannot be null | [compiler schema](compiler-definitions-default_compiler_config.md "compiler.schema.json#/properties/compilers/properties/default/properties/nvhpc") |

## all

Specify compiler configuration for all compiler groups. Use the `all` property if configuration is shared across compiler groups. This property can be overridden in compiler group or named compiler in `config` section.

`all`

*   is optional

*   Type: `object` ([Details](compiler-definitions-default_compiler_all.md))

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_all.md "compiler.schema.json#/properties/compilers/properties/default/properties/all")

### all Type

`object` ([Details](compiler-definitions-default_compiler_all.md))

## gcc

Specify compiler configuration for group of compilers. Use this property if you want to define common configuration for all compilers of same group. This property overrides `all` property.

`gcc`

*   is optional

*   Type: `object` ([Details](compiler-definitions-default_compiler_config.md))

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_config.md "compiler.schema.json#/properties/compilers/properties/default/properties/gcc")

### gcc Type

`object` ([Details](compiler-definitions-default_compiler_config.md))

## intel

Specify compiler configuration for group of compilers. Use this property if you want to define common configuration for all compilers of same group. This property overrides `all` property.

`intel`

*   is optional

*   Type: `object` ([Details](compiler-definitions-default_compiler_config.md))

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_config.md "compiler.schema.json#/properties/compilers/properties/default/properties/intel")

### intel Type

`object` ([Details](compiler-definitions-default_compiler_config.md))

## pgi

Specify compiler configuration for group of compilers. Use this property if you want to define common configuration for all compilers of same group. This property overrides `all` property.

`pgi`

*   is optional

*   Type: `object` ([Details](compiler-definitions-default_compiler_config.md))

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_config.md "compiler.schema.json#/properties/compilers/properties/default/properties/pgi")

### pgi Type

`object` ([Details](compiler-definitions-default_compiler_config.md))

## cray

Specify compiler configuration for group of compilers. Use this property if you want to define common configuration for all compilers of same group. This property overrides `all` property.

`cray`

*   is optional

*   Type: `object` ([Details](compiler-definitions-default_compiler_config.md))

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_config.md "compiler.schema.json#/properties/compilers/properties/default/properties/cray")

### cray Type

`object` ([Details](compiler-definitions-default_compiler_config.md))

## clang

Specify compiler configuration for group of compilers. Use this property if you want to define common configuration for all compilers of same group. This property overrides `all` property.

`clang`

*   is optional

*   Type: `object` ([Details](compiler-definitions-default_compiler_config.md))

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_config.md "compiler.schema.json#/properties/compilers/properties/default/properties/clang")

### clang Type

`object` ([Details](compiler-definitions-default_compiler_config.md))

## cuda

Specify compiler configuration for group of compilers. Use this property if you want to define common configuration for all compilers of same group. This property overrides `all` property.

`cuda`

*   is optional

*   Type: `object` ([Details](compiler-definitions-default_compiler_config.md))

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_config.md "compiler.schema.json#/properties/compilers/properties/default/properties/cuda")

### cuda Type

`object` ([Details](compiler-definitions-default_compiler_config.md))

## upcxx

Specify compiler configuration for group of compilers. Use this property if you want to define common configuration for all compilers of same group. This property overrides `all` property.

`upcxx`

*   is optional

*   Type: `object` ([Details](compiler-definitions-default_compiler_config.md))

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_config.md "compiler.schema.json#/properties/compilers/properties/default/properties/upcxx")

### upcxx Type

`object` ([Details](compiler-definitions-default_compiler_config.md))

## nvhpc

Specify compiler configuration for group of compilers. Use this property if you want to define common configuration for all compilers of same group. This property overrides `all` property.

`nvhpc`

*   is optional

*   Type: `object` ([Details](compiler-definitions-default_compiler_config.md))

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-default_compiler_config.md "compiler.schema.json#/properties/compilers/properties/default/properties/nvhpc")

### nvhpc Type

`object` ([Details](compiler-definitions-default_compiler_config.md))
