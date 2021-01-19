# Untitled object in compiler schema version 1.0 Schema

```txt
compiler-v1.0.schema.json#/properties/compilers/properties/default
```




| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                             |
| :------------------ | ---------- | -------------- | ------------ | :---------------- | --------------------- | ------------------- | -------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [compiler-v1.0.schema.json\*](../out/compiler-v1.0.schema.json "open original schema") |

## default Type

`object` ([Details](compiler-v1-properties-compilers-properties-default.md))

# undefined Properties

| Property        | Type     | Required | Nullable       | Defined by                                                                                                                                                              |
| :-------------- | -------- | -------- | -------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [all](#all)     | `object` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-default_compiler_all.md "compiler-v1.0.schema.json#/properties/compilers/properties/default/properties/all")      |
| [gcc](#gcc)     | `object` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-default_compiler_config.md "compiler-v1.0.schema.json#/properties/compilers/properties/default/properties/gcc")   |
| [intel](#intel) | `object` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-default_compiler_config.md "compiler-v1.0.schema.json#/properties/compilers/properties/default/properties/intel") |
| [pgi](#pgi)     | `object` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-default_compiler_config.md "compiler-v1.0.schema.json#/properties/compilers/properties/default/properties/pgi")   |
| [cray](#cray)   | `object` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-default_compiler_config.md "compiler-v1.0.schema.json#/properties/compilers/properties/default/properties/cray")  |
| [clang](#clang) | `object` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-default_compiler_config.md "compiler-v1.0.schema.json#/properties/compilers/properties/default/properties/clang") |

## all

Specify compiler configuration for all compiler groups. Use the `all` property if configuration is shared across compiler groups. This property can be overridden in compiler group or named compiler in `config` section.


`all`

-   is optional
-   Type: `object` ([Details](compiler-v1-definitions-default_compiler_all.md))
-   cannot be null
-   defined in: [compiler schema version 1.0](compiler-v1-definitions-default_compiler_all.md "compiler-v1.0.schema.json#/properties/compilers/properties/default/properties/all")

### all Type

`object` ([Details](compiler-v1-definitions-default_compiler_all.md))

## gcc

Specify compiler configuration for group of compilers. Use this property if you want to define common configuration for all compilers of same group. This property overrides `all` property. 


`gcc`

-   is optional
-   Type: `object` ([Details](compiler-v1-definitions-default_compiler_config.md))
-   cannot be null
-   defined in: [compiler schema version 1.0](compiler-v1-definitions-default_compiler_config.md "compiler-v1.0.schema.json#/properties/compilers/properties/default/properties/gcc")

### gcc Type

`object` ([Details](compiler-v1-definitions-default_compiler_config.md))

## intel

Specify compiler configuration for group of compilers. Use this property if you want to define common configuration for all compilers of same group. This property overrides `all` property. 


`intel`

-   is optional
-   Type: `object` ([Details](compiler-v1-definitions-default_compiler_config.md))
-   cannot be null
-   defined in: [compiler schema version 1.0](compiler-v1-definitions-default_compiler_config.md "compiler-v1.0.schema.json#/properties/compilers/properties/default/properties/intel")

### intel Type

`object` ([Details](compiler-v1-definitions-default_compiler_config.md))

## pgi

Specify compiler configuration for group of compilers. Use this property if you want to define common configuration for all compilers of same group. This property overrides `all` property. 


`pgi`

-   is optional
-   Type: `object` ([Details](compiler-v1-definitions-default_compiler_config.md))
-   cannot be null
-   defined in: [compiler schema version 1.0](compiler-v1-definitions-default_compiler_config.md "compiler-v1.0.schema.json#/properties/compilers/properties/default/properties/pgi")

### pgi Type

`object` ([Details](compiler-v1-definitions-default_compiler_config.md))

## cray

Specify compiler configuration for group of compilers. Use this property if you want to define common configuration for all compilers of same group. This property overrides `all` property. 


`cray`

-   is optional
-   Type: `object` ([Details](compiler-v1-definitions-default_compiler_config.md))
-   cannot be null
-   defined in: [compiler schema version 1.0](compiler-v1-definitions-default_compiler_config.md "compiler-v1.0.schema.json#/properties/compilers/properties/default/properties/cray")

### cray Type

`object` ([Details](compiler-v1-definitions-default_compiler_config.md))

## clang

Specify compiler configuration for group of compilers. Use this property if you want to define common configuration for all compilers of same group. This property overrides `all` property. 


`clang`

-   is optional
-   Type: `object` ([Details](compiler-v1-definitions-default_compiler_config.md))
-   cannot be null
-   defined in: [compiler schema version 1.0](compiler-v1-definitions-default_compiler_config.md "compiler-v1.0.schema.json#/properties/compilers/properties/default/properties/clang")

### clang Type

`object` ([Details](compiler-v1-definitions-default_compiler_config.md))
